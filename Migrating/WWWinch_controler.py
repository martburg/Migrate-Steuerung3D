from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox
from WWWinch_achsmemory import Achsmemory
from WWWinch_state_machine import AxisStateMachine
from multiprocessing import shared_memory

from input.input_manager import InputManager
from input.pygame_joystick import PygameJoystickInput


import subprocess,pprint
import sys,json
import os,hashlib
import time,signal



MEM_NAME_GUI2HW = "achse_controler_to_hw"
MEM_NAME_HW2GUI = "achse_hw_to_controler"

bindings = {
    "SpeedSoll": {"source": "axis_1", "scale": 32767},
    "Enable": {"source": "button_5"},
    "acc_inc": {"source": "button_2"},
    "acc_dec": {"source": "button_0"},
    "dcc_inc": {"source": "button_3"},
    "dcc_dec": {"source": "button_1"},
}

class TimingDiagnostics:
    def __init__(self):
        self.last_frame = None
        self.stale_counter = 0

    def check_backend_timing(self, frame_data: dict, label: str = "Backend"):
        sync_tag = frame_data.get("SyncTag")
        frame_id = frame_data.get("Frame")
        timestamp = frame_data.get("Timestamp")

        if sync_tag != 0xCAFEBABE:
            print(f"[{label}] SyncTag mismatch or missing (got {sync_tag})")
            return

        if frame_id is not None:
            if frame_id == self.last_frame:
                self.stale_counter += 1
                if self.stale_counter > 5:
                    print(f"[{label}] Warning: Frame {frame_id} repeated {self.stale_counter} times")
            else:
                self.stale_counter = 0
                self.last_frame = frame_id

        if timestamp:
            age_ms = (time.time() - timestamp) * 1000
            print(f"[{label}] Frame {frame_id}, age: {age_ms:.2f} ms")
            if age_ms > 200:
                print(f"[{label}] Warning: Frame is stale (>200ms)")
        else:
            print(f"[{label}] No Timestamp in frame")

class Controller:
    def __init__(self, ui):

        self.clean_memory()

        self.ui = ui  # Reference to the UI widget (AchseWidget)

        self.GUI2HW  = Achsmemory(MEM_NAME_GUI2HW, create=True)
        self.HW2GUI = Achsmemory(MEM_NAME_HW2GUI, create=True)

        self.backend_proc = None

        self._last_frame_id = None
        self._repeat_count = 0


        self.Controler_Codec = None  # Defer instantiation
        self.input_manager = InputManager(PygameJoystickInput(), bindings)
        self.state_machine = AxisStateMachine()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.step_count = 0  # Used for simulated testing

        self.ui.axis_selected.connect(self.handle_axis_selection)
        self.ui.edit_setPosProps_requested.connect(self.handle_edit_PosProps)
        self.ui.edit_setVelProps_requested.connect(self.handle_edit_VelProps)
        self.ui.edit_setFilterProps_requested.connect(self.handle_edit_FilterProps)
        self.ui.edit_setGuideProps_requested.connect(self.handle_edit_GuideProps)
        self.ui.edit_cancel_requested.connect(self.handle_cancel_edit)
        self.ui.edit_commit_requested.connect(self.handle_commit_edit)
        self.ui.click_EsReset_requested.connect(self.handle_click_EsReset)
        self.ui.click_EStop_requested.connect(self.handle_click_EStop)
        self.ui.click_Recover_requested.connect(self.handle_click_Recover)
        self,ui.click_ReSync_requested.connect(self.handle_click_Resync)
        self.ui.click_AxisReset_requested.connect(self.handle_click_AxisReset)
        self.ui.click_GuideReset_requested.connect(self.handle_click_GuideReset)


        self._selected_axis_name = None
        self._prev_state = None
        self._write_countdown = 0
        self.frame_count = 0
        self._timing_diag = TimingDiagnostics()

        self._last_update_time = time.perf_counter()

        self.estop_latch = False
        self.EsReady_state = False
        self.EStoprequested = False
        self._estop_bit_initial = None

        self._pending_config_hash = None
        self._last_sent_setprop = None

        self._resend_attempts = 0
        self._last_sent_guide_setprop = None

        self._acc_tuned = 0.0
        self._dcc_tuned = 0.0


    def ensure_codec(self, axis_name):
        if axis_name == 'SIMUL':
            from WWWinch_sim_codec import SimCodec
            self.Controler_Codec = SimCodec()
        else:
            from WWWinch_codec import Codec
            self.Controler_Codec = Codec()

    def start(self, interval_ms=10):
        """Start the periodic update timer."""
        self.timer.start(interval_ms)

    def stop(self):
        self.timer.stop()

    def update(self):
        self.step_count += 1
        now = time.perf_counter()
        self.dt = now - self._last_update_time
        self._last_update_time = now

        # Step 0: Get selected axis name from UI
        axis_name = self.ui.ui.cmbAxisName.currentText().strip() if hasattr(self.ui.ui, "cmbAxisName") else ""

        # Step 1: Ensure codec is available
        if not self.Controler_Codec:
            if not axis_name:
                return  # No axis selected and no codec — nothing to do
            self.ensure_codec(axis_name)

        if not self.Controler_Codec:
            return  # Defensive: codec creation failed

        # Step 2: Read backend state → unpack into codec
        raw_props = self.get_props()
        #self._timing_diag.check_backend_timing(raw_props)
        self.Controler_Codec.unpack(raw_props)

        # Step 3: Inject joystick input and re-unpack
        self.handle_joystick_commands(raw_props)

        # Step 4: State machine update
        prev_state = getattr(self, '_prev_state', None)
        current_state = self.state_machine.update(
            self.Controler_Codec.ActProp,
            self.Controler_Codec.EStop,
            self.Controler_Codec.SetProp
        )

        # Step 5: Transition hook (trigger even on first-ever transition)
        if prev_state is None or prev_state != current_state or current_state == 'waiting_write_confirm':
            self._on_state_transition(current_state)

        # Always update stored state after transition check
        self._prev_state = current_state

        if self.step_count % 10 == 0:
            # Debugging output every 10 steps
            print(f"[Controller] Step {self.step_count}: Current State={current_state}, AxisName={axis_name}")  

        # Step 5.5: Reset Modus if needed
        self._handle_write_countdown()        

        # Step 6: Push updated properties to backend
        if self.Controler_Codec:
            self.set_props(self.Controler_Codec.to_dict({}))


        # Step 7: Update UI
        backend_state = self.HW2GUI.read_confirmed()
        if backend_state:
            self.Controler_Codec.unpack(backend_state)
        self.update_ui()

    def _on_state_transition(self, state):
        match state:
            case "to_init":
                print("[Controller] Entering to_init: preparing for init...")
                self.ui_edits(True)
            case "init":
                print("[Controller] Entering init: waiting for EStop clear...")
                self.ui_edits(True)
            case "to_idle":
                print("[Controller] Entering to_idle: preparing for idle...")
            case "idle":
                print("[Controller] Entering idle: updating EStop UI and enabling reset button...")
                self.ui_edits(True)
            case "moving":
                print("[Controller] Entering moving: update UI for movement...")
            case "fault":
                print("[Controller] Entering fault: show fault dialog or indicator...")
                self.ui_edits(True)
            case "offline":
                print("[Controller] Entering offline: disable controls...")
                if self.Controler_Codec:
                    print("[Controller] Destroying codec instance.")
                    self.Controler_Codec = None
            case "online_waiting":
                print("[Controller] Entering online_waiting: waiting for backend readiness...")
                self.Controler_Codec.ActProp.InitAchse = 1
                self.set_props(self.Controler_Codec.to_dict({}))
                self.state_machine.update(
                self.Controler_Codec.ActProp,
                self.Controler_Codec.EStop,
                self.Controler_Codec.SetProp)
            case "online":
                print("[Controller] Entering online: ready for init or idle state...")
            case "to_e_PosProps":
                print("[Controller] Preparing to enter edit_PosProps...")
                self.to_e_PosProps()
            case "edit_PosProps":
                print("[Controller] Editing position properties...")
            case "to_e_VelProps":
                print("[Controller] Preparing to enter edit_VelProps...")
                self.to_e_VelProps()
            case "edit_VelProps":
                print("[Controller] Editing velocity properties...")
            case "to_e_FilterProps":
                print("[Controller] Preparing to enter edit_FilterProps...")
                self.to_e_FilterProps()
            case "edit_FilterProps":
                print("[Controller] Editing filter properties...")
            case "to_e_GuideProps":
                print("[Controller] Preparing to enter edit_GuideProps...")
                self.to_e_GuideProps()
            case "edit_GuideProps":
                print("[Controller] Editing guider properties...")
            case "moving" | "holding":
                self.ui_edits(False)
            case "waiting_estop_clear":
                print("[Controller] Waiting for EStop clear from backend...")
                self.Controler_Codec.ActProp.EStopReset = True
                self.ui_edits(False)  # Disable UI 
            case "waiting_estop_engage":
                print("[Controller] Waiting for EStop engage to be confirmed...")
                self.Controler_Codec.ActProp.EStopReset = False
                self.ui_edits(False)         
            case "waiting_write_confirm":
                print("[Controller] Waiting for write confirmation from backend...")
                chk = self._check_write_ack()
                if chk == 0:
                    print("[Controller] Write confirmed by backend.")
                    self._resend_attempts = 0  # reset on success
                elif chk == -1:
                    print("[Controller] No pending write to confirm.")
                elif chk == -2:
                    print(f"[Controller] Write not confirmed yet, resending SetProp (attempt {self._resend_attempts+1})...")
                    if  self._last_sent_setprop:
                        props = self.Controler_Codec.to_dict({})

                        # Overwrite with last intended values
                        props["SetProp"] = self._last_sent_setprop.copy()
                        if "Guide" not in props:
                            props["Guide"] = {}
                        props["Guide"]["SetProp"] = self._last_sent_guide_setprop.copy() if self._last_sent_guide_setprop else {}

                        props["SyncTag"] = 0xCAFEBABE
                        props["Frame"] = self.frame_count
                        self.GUI2HW.write_pending(props)
                        self.frame_count += 1
                        self._resend_attempts += 1

                        if self._resend_attempts >= 10:
                            print("[Controller] Warning: 10 consecutive resend attempts — possible backend stall.")
            case _:
                print(f"[Controller] Entering {state}: no specific handler.")

    def ui_edits(self,value):
        """
        Update EStop checkboxes and enable btnEsReset when entering idle.
        """
        ui = self.ui.ui
        try:
            if hasattr(ui, 'btnEsReset'):
                ui.btnEsReset.setEnabled(value)
            if hasattr(ui, 'btnPosEdit'):
                ui.btnPosEdit.setEnabled(value)
            if hasattr(ui, 'btnVelEdit'):
                ui.btnVelEdit.setEnabled(value)
            if hasattr(ui, 'btnGuideEdit'):
                ui.btnGuideEdit.setEnabled(value)
            if hasattr(ui, 'btnFilterEdit'):
                ui.btnFilterEdit.setEnabled(value)           
        except Exception as e:
            print(f"[Controller] Error updating EStop UI: {e}")
        # Optionally, update other EStop-related UI elements here as needed

    def handle_axis_selection(self, axis_name: str):
            axis_name = axis_name.strip()
            print(f"[Controller] handle_axis_selection: axis_name='{axis_name}'")
            self.set_axis(axis_name)

    def set_axis(self, axis_name: str):
        """Safely switch to a new axis context, replacing codec and backend expectations."""
        if axis_name == self._selected_axis_name:
            return  # No change
        if axis_name == "":
            axis_name = 'SIMUL'

        # Check if valid
        if hasattr(self.ui.ui, 'cmbAxisName'):
            available_axes = [self.ui.ui.cmbAxisName.itemText(i) for i in range(self.ui.ui.cmbAxisName.count())]
            if axis_name not in available_axes:
                QMessageBox.warning(self.ui, "Invalid Axis", f"Axis '{axis_name}' is not available.")
                return

        # Confirm change if needed
        if self.Controler_Codec and self._selected_axis_name:
            reply = QMessageBox.question(
                self.ui,
                "Reassign Axis",
                f"Reassign from '{self._selected_axis_name}' to '{axis_name}'?",
                QMessageBox.Ok | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            if reply != QMessageBox.Ok:
                return

        # Destroy and re-instantiate codec
        print(f"[Controller] Switching to new axis: {axis_name}")
        self._selected_axis_name = axis_name
        self.ensure_codec(axis_name)
        self.Controler_Codec.SetProp.Name = axis_name

        self.restart_backend(axis_name)
        self.HW2GUI.write_pending(self.Controler_Codec.to_dict({}))

    def handle_edit_PosProps(self):
        """Handler for entering edit_SetProps state when edit buttons are pressed."""
        print("[Controller] Edit SetProps requested: entering to_e_PosProps state.")
        if hasattr(self.state_machine, 't_e_PosProps'):
            print("[Controller] Attempting to trigger init -> t_e_PosProps ")
            self.state_machine.t_e_PosProps()
        else:
            print("[Controller] State machine does not support t_e_PosProps transition.")

    def handle_edit_VelProps(self):
        """Handler for entering edit_VelProps state when edit buttons are pressed."""
        print("[Controller] Edit VelProps requested: entering to_e_VelProps state.")
        if hasattr(self.state_machine, 't_e_VelProps'):
            print("[Controller] Attempting to trigger init -> to_e_VelProps ")
            self.state_machine.t_e_VelProps()
        else:
            print("[Controller] State machine does not support t_edit_VelProps transition.")

    def handle_edit_FilterProps(self):
        """Handler for entering edit_FilterProps state when edit buttons are pressed."""
        print("[Controller] Edit FilterProps requested: entering to_e_FilterProps state.")
        if hasattr(self.state_machine, 't_e_FilterProps'):
            print("[Controller] Attempting to trigger init -> t_e_FilterProps ")
            self.state_machine.t_e_FilterProps()
        else:
            print("[Controller] State machine does not support t_e_FilterProps transition.")

    def handle_edit_GuideProps(self):
        print("[Controller] Edit GuideProps requested: entering to_e_GuideProps state.")
        if hasattr(self.state_machine, 't_e_GuideProps'):
            self.state_machine.t_e_GuideProps()
        else:
            print("[Controller] State machine does not support t_e_GuideProps transition.")

    def handle_cancel_edit(self, group):
        print(f"[Controller] Cancel requested for {group} properties.")
        try:
            if group == "Pos":
                self.restore_backup(self._Pos_backup, self.Controler_Codec.SetProp)
            elif group == "Vel":
                self.restore_backup(self._Pos_backup, self.Controler_Codec.SetProp)
            elif group == "Filter":
                self.restore_backup(self._filter_backup, self.Controler_Codec.SetProp)
            elif group == "Guide":
                self.restore_backup(self._guide_backup, self.Controler_Codec.Guide.SetProp)
            else:
                print(f"[Controller] Unknown cancel group: {group}")
                return

            self.set_props(self.Controler_Codec.to_dict({}))

            print("[Controller] Cancelled edit — attempting to return to INIT via finish_edit.")
            if hasattr(self.state_machine, "t_finish_edit"):
                self.state_machine.t_finish_edit()
            else:
                print("[Controller] Warning: finish_edit transition not available")

            self._prev_state = self.state_machine.state
            self.ui_edits(True)

            ui = self.ui.ui

            if group == "Pos":
                for name in ["txtHardMax", "txtUserMax", "txtPosOffset", "txtUserMin", "txtHardMin", "txtPosWin"]:
                    widget = getattr(ui, name, None)
                    if widget: widget.setEnabled(False)
                for name in ["btnPosWrite", "btnPosCancel"]:
                    btn = getattr(ui, name, None)
                    if btn: btn.setEnabled(False)
                if hasattr(ui, "btnPosEdit"):
                    ui.btnPosEdit.setEnabled(True)

            elif group == "Vel":
                for name in ["txtVelMax", "txtAccMax", "txtDccMax", "txtAccMove", "txtMaxAmp", "txtVelWin"]:
                    widget = getattr(ui, name, None)
                    if widget: widget.setEnabled(False)
                for name in ["btnVelWrite", "btnVelCancel"]:
                    btn = getattr(ui, name, None)
                    if btn: btn.setEnabled(False)
                if hasattr(ui, "btnVelEdit"):
                    ui.btnVelEdit.setEnabled(True)

            elif group == "Filter":
                for name in ["txtFilterP", "txtFilterI", "txtFilterD", "txtFilterIL"]:
                    widget = getattr(ui, name, None)
                    if widget: widget.setEnabled(False)
                for name in ["btnFilterWrite", "btnFilterCancel"]:
                    btn = getattr(ui, name, None)
                    if btn: btn.setEnabled(False)
                if hasattr(ui, "btnFilterEdit"):
                    ui.btnFilterEdit.setEnabled(True)

            elif group == "Guide":
                for name in ["txtGuidePitch", "txtGuidePosMax", "txtGuidePosMaxMax", "txtGuidePosMin"]:
                    widget = getattr(ui, name, None)
                    if widget: widget.setEnabled(False)
                for name in ["btnGuideWrite", "btnGuideCancel"]:
                    btn = getattr(ui, name, None)
                    if btn: btn.setEnabled(False)
                if hasattr(ui, "btnGuideEdit"):
                    ui.btnGuideEdit.setEnabled(True)


        except Exception as e:
            print(f"[Controller] Error during cancel for {group}: {e}")

    def compute_hash(self, obj: dict) -> str:
        return hashlib.sha1(json.dumps(obj, sort_keys=True).encode()).hexdigest()

    def handle_commit_edit(self, group):
        print(f"[Controller] Write requested for {group} properties.")
        try:
            ui = self.ui.ui

            if group == "Pos":
                bindings = {
                    "txtHardMax":  ("SetProp", "HardMax"),
                    "txtUserMax":  ("SetProp", "UserMax"),
                    "txtPosOffset":("SetProp", "PosOffset"),
                    "txtUserMin":  ("SetProp", "UserMin"),
                    "txtHardMin":  ("SetProp", "HardMin"),
                    "txtPosWin":   ("SetProp", "PosWin"),
                }
            elif group == "Vel":
                bindings = {
                    "txtVelMax":   ("SetProp", "VelMax"),
                    "txtAccMax":   ("SetProp", "AccMax"),
                    "txtDccMax":   ("SetProp", "DccMax"),
                    "txtAccMove":  ("SetProp", "AccMove"),
                    "txtMaxAmp":   ("SetProp", "MaxAmp"),
                    "txtVelWin":   ("SetProp", "VelWin"),
                }
            elif group == "Filter":
                bindings = {
                    "txtFilterP":  ("SetProp", "FilterP"),
                    "txtFilterI":  ("SetProp", "FilterI"),
                    "txtFilterD":  ("SetProp", "FilterD"),
                    "txtFilterIL": ("SetProp", "FilterIL"),
                }
            elif group == "Guide":
                bindings = {
                    "txtGuidePitch":     ("Guide.SetProp", "GuidePitch"),
                    "txtGuidePosMax":    ("Guide.SetProp", "GuidePosMax"),
                    "txtGuidePosMaxMax": ("Guide.SetProp", "GuidePosMaxMax"),
                    "txtGuidePosMin":    ("Guide.SetProp", "GuidePosMin"),
                }
            else:
                print(f"[Controller] Unknown write group: {group}")
                return

            # 1. Apply UI values to Codec
            for widget_name, (path_root, attr) in bindings.items():
                widget = getattr(ui, widget_name, None)
                if not widget:
                    continue
                text = widget.text()
                target = self.Controler_Codec
                for part in path_root.split("."):
                    target = getattr(target, part)

                # Coerce to type of existing attribute if possible
                try:
                    old_val = getattr(target, attr)
                    new_val = type(old_val)(text)
                except Exception:
                    new_val = text  # fallback to raw string

                setattr(target, attr, new_val)

            # 2. Push props
            self.Controler_Codec.ActProp.Modus = "w"
            #self.set_props(self.Controler_Codec.to_dict({}))
            setprop = self.Controler_Codec.to_dict({}).get("SetProp", {})
            self._last_sent_setprop = setprop.copy()
            self._last_sent_guide_setprop = self.Controler_Codec.to_dict({}).get("Guide", {}).get("SetProp", {}).copy()
            combined_config = {
                "SetProp": self._last_sent_setprop.copy(),
                "Guide.SetProp": self._last_sent_guide_setprop.copy() if self._last_sent_guide_setprop else {},
                }
            self._resend_attempts = 0
            self._pending_config_hash = self.compute_hash(combined_config)
            self._write_countdown = 2

            # 3. Finish edit
            print("[Controller] Waiting — for write confirm.")
            if hasattr(self.state_machine, "t_waiting_write_confirm"):
                self.state_machine.t_waiting_write_confirm()
            else:
                print("[Controller] Missing t_waiting_write_confirm")
            #if hasattr(self.state_machine, "t_finish_edit"):
            #    self.state_machine.t_finish_edit()
            #else:
            #    print("[Controller] Warning: finish_edit transition not available")

            # 4. Disable edit mode for group
            for widget_name, _ in bindings.items():
                widget = getattr(ui, widget_name, None)
                if widget:
                    widget.setEnabled(False)

            # 2. Enable all Edit buttons (across all groups)
            for suffix in ["Pos", "Vel", "Filter", "Guide"]:
                edit_btn = f"btn{suffix}Edit"
                if hasattr(ui, edit_btn):
                    getattr(ui, edit_btn).setEnabled(True)

            # 3. Disable all Write/Cancel buttons (across all groups)
            for suffix in ["Pos", "Vel", "Filter", "Guide"]:
                for kind in ["Write", "Cancel"]:
                    btn = f"btn{suffix}{kind}"
                    if hasattr(ui, btn):
                        getattr(ui, btn).setEnabled(False)

            if hasattr(ui, "cmbAxisName"):
                ui.cmbAxisName.setEnabled(True)

            if hasattr(ui, "btnEsReset"):
                ui.btnEsReset.setEnabled(True)

            #self._prev_state = self.state_machine.state
            #print(f"[Controller] Finished editing {group}.")

        except Exception as e:
            print(f"[Controller] Error during write for {group}: {e}")

    def _check_write_ack(self):
        if not self._pending_config_hash:
            return -1  # No pending write to confirm

        # Get current backend-confirmed state
        confirmed_frame = self.HW2GUI.read_confirmed()
        if confirmed_frame:
            self.Controler_Codec.unpack(confirmed_frame)
        confirmed = self.Controler_Codec.to_dict({})

        confirmed_setprop = confirmed.get("SetProp", {})
        confirmed_guide_setprop = confirmed.get("Guide", {}).get("SetProp", {})

        expected_setprop = self._last_sent_setprop or {}
        expected_guide_setprop = self._last_sent_guide_setprop or {}

        # Print comparison table
        print("\n[Controller] === Comparing SetProp ===")
        print("{:<24} | {:<24} | {:<24}".format("Key", "Sent", "Confirmed"))
        print("-" * 76)
        all_keys = sorted(set(expected_setprop.keys()).union(confirmed_setprop.keys()))
        for key in all_keys:
            sent = expected_setprop.get(key, "<missing>")
            conf = confirmed_setprop.get(key, "<missing>")
            print("{:<24} | {:<24} | {:<24}".format(key, str(sent), str(conf)))

        print("\n[Controller] === Comparing Guide.SetProp ===")
        print("{:<24} | {:<24} | {:<24}".format("Key", "Sent", "Confirmed"))
        print("-" * 76)
        guide_keys = sorted(set(expected_guide_setprop.keys()).union(confirmed_guide_setprop.keys()))
        for key in guide_keys:
            sent = expected_guide_setprop.get(key, "<missing>")
            conf = confirmed_guide_setprop.get(key, "<missing>")
            print("{:<24} | {:<24} | {:<24}".format(key, str(sent), str(conf)))
        print("-" * 76)

        # Combine for unified hash check
        combined_expected = {
            "SetProp": expected_setprop,
            "Guide.SetProp": expected_guide_setprop,
        }
        combined_confirmed = {
            "SetProp": confirmed_setprop,
            "Guide.SetProp": confirmed_guide_setprop,
        }

        expected_hash = self._pending_config_hash
        current_hash = self.compute_hash(combined_confirmed)

        print(f"[Controller] expected hash = {expected_hash}")
        print(f"[Controller] current hash  = {current_hash}")

        if current_hash == expected_hash:
            print("[Controller] Write confirmed by backend (SetProp + Guide.SetProp match).")
            self._pending_config_hash = None
            self.Controler_Codec.ActProp.Modus = "r"
            if hasattr(self.state_machine, "t_confirm_write"):
                self.state_machine.t_confirm_write()
                return 0
            else:
                print("[Controller] Missing t_confirm_write transition.")
                return -3
        else:
            print("[Controller] Waiting for write confirmation...")
            return -2
    
    def handle_click_EsReset(self):
        print("[Controller] EStop Reset button clicked.")
        self.Controler_Codec.ActProp.EStopReset = True
        self.set_props(self.Controler_Codec.to_dict({}))
        if hasattr(self.state_machine, 't_request_estop_clear'):
            self.state_machine.t_request_estop_clear()
        else:
            print("[Controller] State machine does not support t_request_estop_clear transition.")

    def handle_click_EStop(self):
        self.Controler_Codec.ActProp.EStopReset = False
        print("[Controller] EStop button clicked.")
        if hasattr(self.state_machine, 't_request_estop_engage'):
            self.state_machine.t_request_estop_engage()
        else:
            print("[Controller] State machine cannot transition to waiting_estop_engage")

    def handle_click_Recover(self):
        print("[Controller] Recover button clicked.")

    def handle_click_Resync(self):
        print("[Controller] Resync button clicked.")

    def handle_click_AxisReset(self):
        print("[Controller] Axis Reset button clicked.")

    def handle_click_GuideReset(self):
        print("[Controller] Guide Reset button clicked.")

    def handle_joystick_commands(self, raw_props):
        # Inject joystick values into raw_props and re-unpack
        self.input_manager.inject(raw_props)
        self.Controler_Codec.unpack(raw_props)

        # Joystick-driven tuning for AccMax and DccMax
        act = self.Controler_Codec.ActProp
        setp = self.Controler_Codec.SetProp

        # Don't read from ActProp — use the local shadow values
        acc = self._acc_tuned
        dcc = self._dcc_tuned

        acc_limit = float(getattr(setp, "AccMax", 0.0))
        dcc_limit = float(getattr(setp, "DccMax", 0.0))

        step = 0.01


        flags = raw_props.get("ActProp", {})
        #print(f"[JoystickCommands] Flags: {flags}")

        if flags.get("acc_inc"):
            acc = min(acc + step, acc_limit)
            #print(f"[JoystickCommands] Increasing AccMax: {acc} (limit: {acc_limit})")
        if flags.get("acc_dec"):
            acc = max(acc - step, 0.0)
            #print(f"[JoystickCommands] Decreasing AccMax: {acc} (limit: {acc_limit})")
        if flags.get("dcc_inc"):
            dcc = min(dcc + step, dcc_limit)
            #print(f"[JoystickCommands] Increasing DccMax: {dcc} (limit: {dcc_limit})")
        if flags.get("dcc_dec"):
            dcc = max(dcc - step, 0.0)
            #print(f"[JoystickCommands] Decreasing DccMax: {dcc} (limit: {dcc_limit})")

            # Save locally
        self._acc_tuned = acc
        self._dcc_tuned = dcc

        act.AccMax = acc
        act.DccMax = dcc

    def to_e_PosProps(self):
        """Transition to edit position properties state."""
        print("[Controller] Transitioning to edit_PosProps state.")
        ui = self.ui.ui
        try:
            # Enable editing fields
            for name in ["txtHardMax", "txtUserMax", "txtPosOffset", "txtUserMin", "txtHardMin", "txtPosWin"]:
                widget = getattr(ui, name, None)
                if widget:
                    widget.setEnabled(True)

            # Enable buttons
            for btn_name in ["btnPosWrite", "btnPosCancel"]:
                btn = getattr(ui, btn_name, None)
                if btn:
                    btn.setEnabled(True)

            # Disable reset button if it exists
            if hasattr(ui, 'btnEsReset'):
                ui.btnEsReset.setEnabled(False)
            # Disable edit buttons
            if hasattr(ui, 'btnPosEdit'):
                ui.btnPosEdit.setEnabled(False)
            if hasattr(ui, 'btnVelEdit'):
                ui.btnVelEdit.setEnabled(False)
            if hasattr(ui, 'btnGuideEdit'):
                ui.btnGuideEdit.setEnabled(False)   
            if hasattr(ui, 'btnFilterEdit'):
                ui.btnFilterEdit.setEnabled(False)
            # Disable axis selection combo box if it exists
            if hasattr(ui, 'cmbAxisName'):
                ui.cmbAxisName.setEnabled(False)
    
            # Store local copy of values in controller
            self._Pos_backup = {
                "HardMax": self.Controler_Codec.SetProp.HardMax,
                "UserMax": self.Controler_Codec.SetProp.UserMax,
                "PosOffset": self.Controler_Codec.SetProp.PosOffset,
                "UserMin": self.Controler_Codec.SetProp.UserMin,
                "HardMin": self.Controler_Codec.SetProp.HardMin,
                "PosWin": self.Controler_Codec.SetProp.PosWin,
            }

            # Only after UI and backup logic, trigger the state machine transition
            if hasattr(self.state_machine, 't_edit_PosProps'):
                print("[Controller] Now calling t_edit_PosProps to enter edit_PosProps state.")
                self.state_machine.t_edit_PosProps()
            else:
                print("[Controller] State machine does not support t_edit_PosProps transition.")

        except Exception as e:
            print(f"[Controller] Error in t_e_PosProps: {e}")
        # set Controls in Position edit mode

    def to_e_VelProps(self):
        """Transition to edit velocity properties state."""
        print("[Controller] Transitioning to edit_VelProps state.")
        ui = self.ui.ui
        try:
            # Enable editing fields
            for name in ["txtVelMax", "txtAccMax", "txtDccMax", "txtAccMove", "txtMaxAmp", "txtVelWin"]:
                widget = getattr(ui, name, None)
                if widget:
                    widget.setEnabled(True)

            # Enable buttons
            for btn_name in ["btnVelWrite", "btnVelCancel"]:
                btn = getattr(ui, btn_name, None)
                if btn:
                    btn.setEnabled(True)

            # Disable reset button if it exists
            if hasattr(ui, 'btnEsReset'):
                ui.btnEsReset.setEnabled(False)
            # Disable edit buttons
            if hasattr(ui, 'btnPosEdit'):
                ui.btnPosEdit.setEnabled(False)
            if hasattr(ui, 'btnVelEdit'):
                ui.btnVelEdit.setEnabled(False)
            if hasattr(ui, 'btnGuideEdit'):
                ui.btnGuideEdit.setEnabled(False)   
            if hasattr(ui, 'btnFilterEdit'):
                ui.btnFilterEdit.setEnabled(False)
            # Disable axis selection combo box if it exists
            if hasattr(ui, 'cmbAxisName'):
                ui.cmbAxisName.setEnabled(False)

            # Store local copy of values in controller
            self._Pos_backup = {
                "VelMax": self.Controler_Codec.SetProp.VelMax,
                "AccMax": self.Controler_Codec.SetProp.AccMax,
                "DccMax": self.Controler_Codec.SetProp.DccMax,
                "AccMove": self.Controler_Codec.SetProp.AccMove,
                "MaxAmp": self.Controler_Codec.SetProp.MaxAmp,
                "VelWin": self.Controler_Codec.SetProp.VelWin,
            }

            # Only after UI and backup logic, trigger the state machine transition
            if hasattr(self.state_machine, 't_edit_VelProps'):
                print("[Controller] Now calling t_edit_VelProps to enter edit_VelProps state.")
                self.state_machine.t_edit_VelProps()
            else:
                print("[Controller] State machine does not support t_edit_VelProps transition.")

        except Exception as e:
            print(f"[Controller] Error in t_e_VelProps: {e}")
        # set Controls in Velocity edit mode

    def to_e_FilterProps(self):
        """Transition to edit filter properties state."""
        print("[Controller] Transitioning to edit_FilterProps state.")
        # set Controls in Filter edit mode
        ui = self.ui.ui
        try:
            # Enable editing fields
            for name in ["txtFilterP", "txtFilterI", "txtFilterD", "txtFilterIL"]:
                widget = getattr(ui, name, None)
                if widget:
                    widget.setEnabled(True)

            # Enable buttons
            for btn_name in ["btnFilterWrite", "btnFilterCancel"]:
                btn = getattr(ui, btn_name, None)
                if btn:
                    btn.setEnabled(True)

            # Disable reset button if it exists
            if hasattr(ui, 'btnEsReset'):
                ui.btnEsReset.setEnabled(False)
            # Disable edit buttons
            if hasattr(ui, 'btnPosEdit'):
                ui.btnPosEdit.setEnabled(False)
            if hasattr(ui, 'btnVelEdit'):
                ui.btnVelEdit.setEnabled(False)
            if hasattr(ui, 'btnGuideEdit'):
                ui.btnGuideEdit.setEnabled(False)   
            if hasattr(ui, 'btnFilterEdit'):
                ui.btnFilterEdit.setEnabled(False)
            # Disable axis selection combo box if it exists
            if hasattr(ui, 'cmbAxisName'):
                ui.cmbAxisName.setEnabled(False)

            # Store local copy of values in controller
            self._filter_backup = {
                "FilterP": self.Controler_Codec.SetProp.FilterP,
                "FilterI": self.Controler_Codec.SetProp.FilterI,
                "FilterD": self.Controler_Codec.SetProp.FilterD,
                "FilterIL": self.Controler_Codec.SetProp.FilterIL,
            }

            # Only after UI and backup logic, trigger the state machine transition
            if hasattr(self.state_machine, 't_edit_FilterProps'):
                print("[Controller] Now calling t_edit_FilterProps to enter edit_FilterProps state.")
                self.state_machine.t_edit_FilterProps()
            else:
                print("[Controller] State machine does not support t_edit_FilterProps transition.")

        except Exception as e:
            print(f"[Controller] Error in t_e_FilterProps: {e}")

    def to_e_GuideProps(self):
        print("[Controller] Transitioning to edit_GuideProps state.")
        ui = self.ui.ui
        try:
            for name in ["txtGuidePitch", "txtGuidePosMax", "txtGuidePosMaxMax", "txtGuidePosMin"]:
                widget = getattr(ui, name, None)
                if widget:
                    widget.setEnabled(True)

            for btn_name in ["btnGuideWrite", "btnGuideCancel"]:
                btn = getattr(ui, btn_name, None)
                if btn:
                    btn.setEnabled(True)

            if hasattr(ui, 'btnEsReset'):
                ui.btnEsReset.setEnabled(False)
            for edit_btn in ["btnPosEdit", "btnVelEdit", "btnGuideEdit", "btnFilterEdit"]:
                btn = getattr(ui, edit_btn, None)
                if btn:
                    btn.setEnabled(False)
            if hasattr(ui, 'cmbAxisName'):
                ui.cmbAxisName.setEnabled(False)

            self._guide_backup = {
                "GuidePitch": self.Controler_Codec.Guide.SetProp.GuidePitch,
                "GuidePosMax": self.Controler_Codec.Guide.SetProp.GuidePosMax,
                "GuidePosMaxMax": self.Controler_Codec.Guide.SetProp.GuidePosMaxMax,
                "GuidePosMin": self.Controler_Codec.Guide.SetProp.GuidePosMin,
            }

            if hasattr(self.state_machine, 't_edit_GuideProps'):
                print("[Controller] Now calling t_edit_GuideProps to enter edit_GuideProps state.")
                self.state_machine.t_edit_GuideProps()

        except Exception as e:
            print(f"[Controller] Error in to_e_GuideProps: {e}")

    def restore_backup(self, backup_dict, target_obj):
        for key, value in backup_dict.items():
            if hasattr(target_obj, key):
                setattr(target_obj, key, value)
            else:
                print(f"[Controller] Warning: Cannot restore {key} on {target_obj}")

    def _handle_write_countdown(self):
        """
        Decrement and clear ActProp.Modus after a write commit ('w').
        Called during update before pushing props to backend.
        """
        if self._write_countdown > 0:
            self._write_countdown -= 1
            if self._write_countdown == 0:
                self.Controler_Codec.ActProp.Modus = "r"
                print("[Controller] Reset Modus to 'r' after write commit")

    def update_ui(self):
        """Push all bound data to the UI widgets."""
        for name, (widget_type, path, fmt) in self.ui._bindings.items():
            widget = self.ui.ui.findChild(self.ui.widget_classes[widget_type], name)
            if not widget:
                print(f"[UI] Missing widget: {name}")
                continue

            value = self.resolve_path(self.Controler_Codec, path)
            if widget_type in ("QLineEdit", "QLabel"):
                # Skip updating if user is currently editing this field (enabled during edit states)
                if widget_type == "QLineEdit" and widget.isEnabled():
                    continue

                if fmt:
                    try:
                        value_num = float(value)
                        widget.setText(fmt.format(value_num))
                    except (ValueError, TypeError):
                        widget.setText(str(value))
                else:
                    widget.setText(str(value))

            elif widget_type == "QRadioButton":
                widget.setChecked(bool(value))
            elif widget_type == "QSlider":
                widget.setValue(int(value))

            #if hasattr(widget, "txtTimeTick"):
            self.ui.ui.txtTimeTick.setText(f"{self.dt * 1000:.1f}")

        # Update all cbEs* checkboxes bound to EStop.*
        for name, (widget_type, path, fmt) in self.ui._bindings.items():
            if name.startswith('cbEs') and path.startswith('EStop.'):
                estop_attr = path.split('.')[-1]
                try:
                    cb = getattr(self.ui.ui, name)
                    value = getattr(self.Controler_Codec.EStop, estop_attr, False)
                    cb.setChecked(value)
                except AttributeError:
                    print(f"[UI] Missing cbEs widget or EStop attribute: {name} / {estop_attr}")

    def resolve_path(self, root, path):
        """Resolve dot-path like 'ActProp.PosIst' from the given root object."""
        for attr in path.split("."):
            root = getattr(root, attr)
        return root

    def trigger_estop_reset(self, value: bool):
        """
        Trigger an emergency stop reset or EStop action.
        """
        if not self.Controler_Codec:    
            return
        self.Controler_Codec.ActProp.EStopReset = value
        self.set_props(self.Controler_Codec.to_dict({}))

    def start_backend(self, axis_name: str):
        """Launch a new backend process for the specified axis."""
        import platform
        backend_path = os.path.join(os.path.dirname(__file__), "WWWinch_backend_udp.py")
        if not os.path.exists(backend_path):
            print(f"[Controller] Backend script not found: {backend_path}")
            return

        try:
            print(f"[Controller] Launching backend for axis '{axis_name}'...")

            if os.name == 'nt':
                # Windows: use CREATE_NEW_PROCESS_GROUP
                creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
                self.backend_proc = subprocess.Popen(
                    [sys.executable, backend_path, "--achse", axis_name],
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    stdin=subprocess.DEVNULL,
                    creationflags=creationflags
                )
            else:
                # POSIX (Linux/macOS): create new process group
                self.backend_proc = subprocess.Popen(
                    [sys.executable, backend_path, "--achse", axis_name],
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True
                )

            print(f"[Controller] Backend launched with PID {self.backend_proc.pid}")

        except Exception as e:
            print(f"[Controller] Failed to launch backend: {e}")
            self.backend_proc = None

    def stop_backend(self):
        if self.backend_proc and self.backend_proc.poll() is None:
            print(f"[Controller] Terminating backend with PID {self.backend_proc.pid}")
            try:
                if os.name == 'nt':
                    # Windows: use send_signal or terminate
                    self.backend_proc.send_signal(signal.CTRL_BREAK_EVENT)
                    self.backend_proc.wait(timeout=3)
                else:
                    # POSIX: use killpg
                    os.killpg(os.getpgid(self.backend_proc.pid), signal.SIGTERM)
                    self.backend_proc.wait(timeout=3)
            except Exception as e:
                print(f"[Controller] SIGTERM failed: {e}, trying SIGKILL or force kill...")
                try:
                    if os.name == 'nt':
                        self.backend_proc.kill()
                    else:
                        os.killpg(os.getpgid(self.backend_proc.pid), signal.SIGKILL)
                except Exception as e2:
                    print(f"[Controller] Force kill failed: {e2}")

    def restart_backend(self, axis_name: str):
        """
        Restart the backend process for the given axis name.
        """
        self.stop_backend()
        self.start_backend(axis_name)

    def clean_memory(self):
        shm_names = [MEM_NAME_GUI2HW, MEM_NAME_HW2GUI]
        for name in shm_names:
            try:
                shm = shared_memory.SharedMemory(name=name)
                shm.close()
                shm.unlink()
                print(f"[Main] Unlinked shared memory: {name}")
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"[Main] Error cleaning shared memory '{name}': {e}")

    def set_props(self, props: dict):
        props = {
            "SyncTag": 0xCAFEBABE,
            "Frame": self.frame_count,
            **self.Controler_Codec.to_dict({})
        }
        self.GUI2HW.write_pending(props)
        self.frame_count += 1

    def get_props(self) -> dict:
        frame = self.HW2GUI.read_confirmed()
        if frame is None:
            print("[Controller:backend-read] Frame is None")
            return None

        #frame_id = frame.get("Frame")
        #if frame_id == self._last_frame_id:
        #    self._repeat_count += 1
        #    if self._repeat_count in {6, 9, 12}:  # Only log at key thresholds
        #        print(f"[Guard:backend-read] Frame {frame_id} repeated {self._repeat_count} times — possible stall")
        #else:
        #    self._repeat_count = 0
        #    self._last_frame_id = frame_id

        return frame
        
    def shutdown(self):
        print("[Controller] shutdown() called — stopping backend and timer.")
        self.stop()
        self.stop_backend()
        self.clean_memory() 