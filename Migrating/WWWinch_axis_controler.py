from PySide6.QtCore import QTimer
from WWWinch_codec import Codec
from Achsmemory import Achsmemory
from WWWinch_input_manager import InputManager

MEM_NAME_GUI2HW = "achse_controler_to_hw"
MEM_NAME_HW2GUI = "achse_hw_to_controler"

class AxisMode:
    READONLY = "read"
    EDIT     = "edit"
    WRITE    = "write"
    RECOVER  = "recover"
    ONLINE   = "online"
    OFFLINE  = "offline"

class Controller:
    def __init__(self, ui):
        self.ui = ui  # Reference to the UI widget (AchseWidget)

        self.shm_in  = Achsmemory(MEM_NAME_GUI2HW, create=True)
        self.shm_out = Achsmemory(MEM_NAME_HW2GUI, create=True)

        self.Codec = Codec()

        self.input_manager = InputManager()

        self.mode = AxisMode.READONLY

        # Future: add controller submodules
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        self.step_count = 0  # Used for simulated testing

    def start(self, interval_ms=100):
        """Start the periodic update timer."""
        self.timer.start(interval_ms)

    def stop(self):
        self.timer.stop()

    def update(self):
        """This method runs periodically."""
        self.step_count += 1

        # write properties to shared memory
        self.set_props(self.ui.get_properties())	

    # Read from backend and rehydrate
        raw_props = self.get_props()
        self.Codec.unpack(raw_props)

        print(f"[Controller] Step {self.step_count}: Read properties SpeedSoll: {self.Codec.ActProp.SpeedSoll}, PosIst: {self.Codec.ActProp.PosIst}")

        self.input_manager.inject(raw_props)  # optionally inject again
        
        # Push updated data to the UI
        self.update_ui()

        # TODO: handle Joystick ramp, online status, button states, etc.

    def update_ui(self):
        """Push all bound data to the UI widgets."""
        for name, (widget_type, path, fmt) in self.ui._bindings.items():
            widget = self.ui.ui.findChild(self.ui.widget_classes[widget_type], name)
            if not widget:
                print(f"[UI] Missing widget: {name}")
                continue

            value = self.resolve_path(self.Codec, path)
            if widget_type in ("QLineEdit", "QLabel"):
                widget.setText(fmt.format(value) if fmt else str(value))
            elif widget_type == "QRadioButton":
                widget.setChecked(bool(value))
            elif widget_type == "QSlider":
                widget.setValue(int(value))

    def resolve_path(self, root, path):
        """Resolve dot-path like 'ActProp.PosIst' from the given root object."""
        for attr in path.split("."):
            root = getattr(root, attr)
        return root

    def set_mode(self, mode: str):
        """Switch between modes like edit/write/recover."""
        print(f"[Controller] Switching mode to: {mode}")
        self.mode = mode
        # TODO: trigger UI state changes accordingly

    def set_props(self, props: dict):
        self.shm_in.write(props)

    def get_props(self) -> dict:
        return self.shm_out.read()
