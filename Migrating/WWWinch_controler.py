from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox
from WWWinch_achsmemory import Achsmemory
from WWWinch_input_manager import InputManager
from WWWinch_state_machine import AxisStateMachine

import subprocess
import sys
import os
import signal



MEM_NAME_GUI2HW = "achse_controler_to_hw"
MEM_NAME_HW2GUI = "achse_hw_to_controler"


class Controller:
    def __init__(self, ui):
        self.ui = ui  # Reference to the UI widget (AchseWidget)

        self.shm_in  = Achsmemory(MEM_NAME_GUI2HW, create=True)
        self.shm_out = Achsmemory(MEM_NAME_HW2GUI, create=True)

        self.Controler_Codec = None  # Defer instantiation
        self.input_manager = InputManager()
        self.state_machine = AxisStateMachine()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.step_count = 0  # Used for simulated testing

        self.ui.axis_selected.connect(self.handle_axis_selection)
        self.ui.edit_setPosProps_requested.connect(self.handle_edit_PosProps)
        self.ui.edit_setVelProps_requested.connect(self.handle_edit_VelProps)
        self.ui.edit_setFilterProps_requested.connect(self.handle_edit_FilterProps)

        self._selected_axis_name = None
        self._prev_state = None

    def ensure_codec(self, axis_name):
        if axis_name == 'SIMUL':
            from WWWinch_sim_codec import SimCodec
            self.Controler_Codec = SimCodec()
        else:
            from WWWinch_codec import Codec
            self.Controler_Codec = Codec()

    def start(self, interval_ms=100):
        """Start the periodic update timer."""
        self.timer.start(interval_ms)

    def stop(self):
        self.timer.stop()

    def update(self):
        self.step_count += 1

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
        self.Controler_Codec.unpack(raw_props)

        # Step 3: Inject joystick input and re-unpack
        self.input_manager.inject(raw_props)
        self.Controler_Codec.unpack(raw_props)

        # Step 4: State machine update
        prev_state = getattr(self, '_prev_state', None)
        current_state = self.state_machine.update(
            self.Controler_Codec.ActProp,
            self.Controler_Codec.EStop,
            self.Controler_Codec.SetProp
        )

        # Step 5: Transition hook (trigger even on first-ever transition)
        if prev_state is None or prev_state != current_state:
            self._on_state_transition(current_state)

        # Always update stored state after transition check
        self._prev_state = current_state

        print(f"[Controller] Step {self.step_count}: AxisName={axis_name}, State={current_state}")

        # Step 6: Push updated properties to backend
        self.set_props(self.Controler_Codec.to_dict({}))

        # Step 7: Update UI
        self.update_ui()

    def _on_state_transition(self, state):
        match state:
            case "to_init":
                print("[Controller] Entering to_init: preparing for init...")
                self.ui_enable_edits()
            case "init":
                print("[Controller] Entering init: waiting for EStop clear...")
            case "to_idle":
                print("[Controller] Entering to_idle: preparing for idle...")
            case "idle":
                print("[Controller] Entering idle: updating EStop UI and enabling reset button...")
            case "moving":
                print("[Controller] Entering moving: update UI for movement...")
            case "fault":
                print("[Controller] Entering fault: show fault dialog or indicator...")
            case "offline":
                print("[Controller] Entering offline: disable controls...")
                if self.Controler_Codec:
                    print("[Controller] Destroying codec instance.")
                    self.Controler_Codec = None
            case "online_waiting":
                print("[Controller] Entering online_waiting: waiting for backend readiness...")
                self.Controler_Codec.ActProp.InitAchse = 1
                self.set_props(self.Controler_Codec.to_dict({}))
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
            case _:
                print(f"[Controller] Entering {state}: no specific handler.")

    def ui_enable_edits(self):
        """
        Update EStop checkboxes and enable btnEsReset when entering idle.
        """
        ui = self.ui.ui
        try:
            if hasattr(ui, 'btnEsReset'):
                ui.btnEsReset.setEnabled(True)
            if hasattr(ui, 'btnPosEdit'):
                ui.btnPosEdit.setEnabled(True)
            if hasattr(ui, 'btnVelEdit'):
                ui.btnVelEdit.setEnabled(True)
            if hasattr(ui, 'btnGuideEdit'):
                ui.btnGuideEdit.setEnabled(True)
            if hasattr(ui, 'btnFilterEdit'):
                ui.btnFilterEdit.setEnabled(True)           
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
        self.shm_out.write(self.Controler_Codec.to_dict({}))

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
            self.state_machine.t_edit_VelProps()
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

    def update_ui(self):
        """Push all bound data to the UI widgets."""
        for name, (widget_type, path, fmt) in self.ui._bindings.items():
            widget = self.ui.ui.findChild(self.ui.widget_classes[widget_type], name)
            if not widget:
                print(f"[UI] Missing widget: {name}")
                continue

            value = self.resolve_path(self.Controler_Codec, path)
            if widget_type in ("QLineEdit", "QLabel"):
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

    def start_backend(self, axis_name: str):
        """Launch a new backend process for the specified axis."""
        backend_path = os.path.join(os.path.dirname(__file__), "WWWinch_backend_udp.py")
        if not os.path.exists(backend_path):
            print(f"[Controller] Backend script not found: {backend_path}")
            return

        try:
            print(f"[Controller] Launching backend for axis '{axis_name}'...")
            self.backend_proc = subprocess.Popen(
                [sys.executable, backend_path, "--achse", axis_name],
                stdout=sys.stdout,
                stderr=sys.stderr,
                stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            print(f"[Controller] Backend launched with PID {self.backend_proc.pid}")
        except Exception as e:
            print(f"[Controller] Failed to launch backend: {e}")
            self.backend_proc = None

    def stop_backend(self):
        """Terminate any existing backend process."""
        if hasattr(self, "backend_proc") and self.backend_proc:
            print("[Controller] Stopping existing backend...")
            try:
                self.backend_proc.terminate()
                self.backend_proc.wait(timeout=2)
                print("[Controller] Backend stopped cleanly.")
            except subprocess.TimeoutExpired:
                print("[Controller] Backend did not exit in time — killing.")
                self.backend_proc.kill()
            except Exception as e:
                print(f"[Controller] Error stopping backend: {e}")
            finally:
                self.backend_proc = None

    def restart_backend(self, axis_name: str):
        """
        Restart the backend process for the given axis name.
        """
        self.stop_backend()
        self.start_backend(axis_name)

    def shutdown(self):
        """Gracefully shutdown the controller."""
        self.stop()
        self.shm_in.close()
        self.shm_out.close()
        self.shm_in.unlink()
        self.shm_out.unlink()
        print("[Controller] Shutdown complete.")

    def set_props(self, props: dict):
        self.shm_in.write(props)

    def get_props(self) -> dict:
        return self.shm_out.read()
