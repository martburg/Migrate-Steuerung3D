from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QLineEdit, QLabel, QRadioButton, QSlider, QCheckBox


import os,re


class Widget(QWidget):
    """Widget for displaying and controlling axis properties in the WWWinch application."""

    axis_selected                 = Signal(str)  # Emit selected axis name
    edit_setPosProps_requested    = Signal()  # Signal for edit Pos state
    edit_setVelProps_requested    = Signal()  # Signal for edit Vel state
    edit_setFilterProps_requested = Signal()  # Signal for edit Filter state
    edit_setGuideProps_requested  = Signal()   # Signal for edit Guide state
    edit_cancel_requested         = Signal(str)  # Signal will carry group name: "Pos", "Vel", "Filter", "Guide"
    edit_commit_requested         = Signal(str)  # Signal to commit changes, will carry group name: "Pos", "Vel", "Filter", "Guide"
    click_EsReset_requested       = Signal()
    click_EStop_requested         = Signal()
    click_Recover_requested       = Signal()
    click_ReSync_requested        = Signal()
    click_AxisReset_requested     = Signal()
    click_GuideReset_requested    = Signal()

    def __init__(self):
        super().__init__()

        self.widget_classes = {
            "QLineEdit": QLineEdit,
            "QLabel": QLabel,
            "QRadioButton": QRadioButton,
            "QSlider": QSlider,
            "QCheckBox": QCheckBox,
        }

        self._load_ui()

        self.Controller = None  # Will be set by Controller class

        self._bindings = {
            # --- SetProp ---
            "txtAccMax":          ("QLineEdit", "SetProp.AccMax", "{:.2f}"),
            "txtAccMove":         ("QLineEdit", "SetProp.AccMove", "{:.2f}"),
            "txtDccMax":          ("QLineEdit", "SetProp.DccMax", "{:.2f}"),
            "txtFilterD":         ("QLineEdit", "SetProp.FilterD", "{:.2f}"),
            "txtFilterI":         ("QLineEdit", "SetProp.FilterI", "{:.2f}"),
            "txtFilterIL":        ("QLineEdit", "SetProp.FilterIL", "{:.2f}"),
            "txtFilterP":         ("QLineEdit", "SetProp.FilterP", "{:.2f}"),
            "txtHardMax":         ("QLineEdit", "SetProp.HardMax", "{:.2f}"),
            "txtHardMin":         ("QLineEdit", "SetProp.HardMin", "{:.2f}"),
            "txtMaxAmp":          ("QLineEdit", "SetProp.MaxAmp", "{:.2f}"),
            "txtPosWin":          ("QLineEdit", "SetProp.PosWin", "{:.2f}"),
            "txtRampform":        ("QLineEdit", "SetProp.Rampform", None),
            "txtRopeDiameter":    ("QLineEdit", "SetProp.RopeDiameter", "{:.2f}"),
            "txtRopeLength":      ("QLineEdit", "SetProp.RopeLength", "{:.2f}"),
            "txtRopeNumber":      ("QLineEdit", "SetProp.RopeNumber", None),
            "txtRopeSWLL":        ("QLineEdit", "SetProp.RopeSWLL", "{:.2f}"),
            "txtRopeType":        ("QLineEdit", "SetProp.RopeType", None),
            "txtUserMax":         ("QLineEdit", "SetProp.UserMax", "{:.2f}"),
            "txtUserMin":         ("QLineEdit", "SetProp.UserMin", "{:.2f}"),
            "txtVelMax":          ("QLineEdit", "SetProp.VelMax", "{:.2f}"),
            "txtVelWin":          ("QLineEdit", "SetProp.VelWin", "{:.2f}"),

            # --- ActProp ---
            "txtActCurUI":        ("QLineEdit", "ActProp.ActCurUI", "{:.2f}"),
            "txtCabTemperature":  ("QLineEdit", "ActProp.CabTemperature", "{:.2f}"),
            "txtEStopCutPos":     ("QLineEdit", "ActProp.EStopCutPos", "{:.2f}"),
            "txtEStopCutTime":    ("QLineEdit", "ActProp.EStopCutTime", "{:.2f}"),
            "txtEStopCutVel":     ("QLineEdit", "ActProp.EStopCutVel", "{:.2f}"),
            "txtEStopPosDiff":    ("QLineEdit", "ActProp.EStopPosDiff", "{:.2f}"),
            "txtPosIst":          ("QLineEdit", "ActProp.PosIst", "{:.2f}"),
            "txtSpeedIstUI":      ("QLineEdit", "ActProp.SpeedIstUI", "{:.2f}"),
            "txtStatus":          ("QLineEdit", "ActProp.Status", None),
            "txtTimeTick":        ("QLineEdit", "ActProp.LTOld", "{:.0f}"),
            "txtAcc":             ("QLineEdit", "ActProp.AccMax", "{:.2f}"),
            "txtDcc":             ("QLineEdit", "ActProp.DccMax", "{:.2f}"),

            # --- Guide.SetProp ---
            "txtGuidePitch":      ("QLineEdit", "Guide.SetProp.GuidePitch", "{:.2f}"),
            "txtGuidePosMax":     ("QLineEdit", "Guide.SetProp.GuidePosMax", "{:.2f}"),
            "txtGuidePosMaxMax":  ("QLineEdit", "Guide.SetProp.GuidePosMaxMax", "{:.2f}"),
            "txtGuidePosMin":     ("QLineEdit", "Guide.SetProp.GuidePosMin", "{:.2f}"),

            # --- Guide.ActProp ---
            "txtGuideIstSpeedUI": ("QLineEdit", "Guide.ActProp.GuideIstSpeedUI", "{:.2f}"),
            "txtGuidePosIstUI":   ("QLineEdit", "Guide.ActProp.GuidePosIstUI", "{:.2f}"),
            "txtGuideStatus":     ("QLineEdit", "Guide.ActProp.GuideStatus", None),

            # --- EStop ---
            # 🟨 These will be enabled later, leave as-is
            #"cbFBT":              ("QCheckBox", "EStop.EsFBT", None),
            #"cbBrake1":           ("QCheckBox", "EStop.EsBrake1", None),
            #"cbBrake2":           ("QCheckBox", "EStop.EsBrake2", None),
            "cbBrake1":           ("QCheckBox", "EStop.EsBRK1OK", None),
            "cbBrake2":           ("QCheckBox", "EStop.EsBRK2OK", None),
            "cbEs05kW":           ("QCheckBox", "EStop.Es05kWOK", None),
            "cbEs30kW":           ("QCheckBox", "EStop.Es30kWOK", None),
            "cbEsBRK1OK":         ("QCheckBox", "EStop.EsBRK1OK", None),
            "cbEsBRK2KB":         ("QCheckBox", "EStop.EsBRK2KB", None),
            "cbEsBRK2OK":         ("QCheckBox", "EStop.EsBRK2OK", None),
            "cbEsENC":            ("QCheckBox", "EStop.EsENC", None),
            "cbEsEndlage":        ("QCheckBox", "EStop.EsEndlage", None),
            "cbEsEStop1":         ("QCheckBox", "EStop.EsEStop1", None),
            "cbEsEStop2":         ("QCheckBox", "EStop.EsEStop2", None),
            "cbEsG1COM":          ("QCheckBox", "EStop.EsG1COM", None),
            "cbEsG1FB":           ("QCheckBox", "EStop.EsG1FB", None),
            "cbEsG1OUT":          ("QCheckBox", "EStop.EsG1OUT", None),
            "cbEsG2COM":          ("QCheckBox", "EStop.EsG2COM", None),
            "cbEsG2FB":           ("QCheckBox", "EStop.EsG2FB", None),
            "cbEsG2OUT":          ("QCheckBox", "EStop.EsG2OUT", None),
            "cbEsG3COM":          ("QCheckBox", "EStop.EsG3COM", None),
            "cbEsG3FB":           ("QCheckBox", "EStop.EsG3FB", None),
            "cbEsG3OUT":          ("QCheckBox", "EStop.EsG3OUT", None),
            "cbEsGuider":         ("QCheckBox", "EStop.EsGuider", None),
            "cbEsMaster":         ("QCheckBox", "EStop.EsMaster", None),
            "cbEsNetwork":        ("QCheckBox", "EStop.EsNetwork", None),
            "cbEsPosWin":         ("QCheckBox", "EStop.EsPosWin", None),
            "cbEsRED":            ("QCheckBox", "EStop.EsSteuerwort", None),
            "cbEsSPS":            ("QCheckBox", "EStop.EsSPSOK", None),
            "cbEsVelWin":         ("QCheckBox", "EStop.EsVelWin", None),
            "cbReady":            ("QCheckBox", "EStop.EsReady", None),

            # --- Other Checkboxes ---
            "cbGuideOnline":      ("QCheckBox", "Guide.ActProp.GuideStatus", None),
            "cbGuideReady":       ("QCheckBox", "Guide.ActProp.GuideStatus", None),
            "cbOnline":           ("QCheckBox", "ActProp.Enable", None),

            # --- Sliders ---
            "sldAxisVel":         ("QSlider", "ActProp.SpeedSoll", None),
            "sldGuideSpeed":      ("QSlider", "Guide.ActProp.GuideIstSpeedUI", None),

            # --- 🟨 Legacy/Commented for future activation ---
            #"txtSelected1":       ("QLineEdit", "ActProp.ControlingPIDTx", None),
            #"txtSelected2":       ("QLineEdit", "ActProp.ControlingPIDRx", None),
        }

        
        # Bind signals to slots
        self.ui.cmbAxisName.currentIndexChanged.connect(self._on_axis_select)
        self.ui.btnPosEdit.clicked.connect(self._on_click_PosEdit)
        self.ui.btnVelEdit.clicked.connect(self._on_click_VelEdit)
        self.ui.btnFilterEdit.clicked.connect(self._on_click_FilterEdit)
        self.ui.btnGuideEdit.clicked.connect(self.edit_setGuideProps_requested.emit)
        self.ui.btnPosCancel.clicked.connect(lambda: self.edit_cancel_requested.emit("Pos"))
        self.ui.btnVelCancel.clicked.connect(lambda: self.edit_cancel_requested.emit("Vel"))
        self.ui.btnFilterCancel.clicked.connect(lambda: self.edit_cancel_requested.emit("Filter"))
        self.ui.btnGuideCancel.clicked.connect(lambda: self.edit_cancel_requested.emit("Guide"))
        self.ui.btnPosWrite.clicked.connect(lambda: self.edit_commit_requested.emit("Pos"))
        self.ui.btnVelWrite.clicked.connect(lambda: self.edit_commit_requested.emit("Vel"))
        self.ui.btnFilterWrite.clicked.connect(lambda: self.edit_commit_requested.emit("Filter"))
        self.ui.btnGuideWrite.clicked.connect(lambda: self.edit_commit_requested.emit("Guide"))
        self.ui.btnEsReset.clicked.connect(self._on_click_EsReset)
        self.ui.btnEStop.clicked.connect(self._on_click_EStop)
        self.ui.btnRecover.clicked.connect(self._on_click_Recover)
        self.ui.btnReSync.clicked.connect(self._on_click_ReSync)
        self.ui.btnAxisReset.clicked.connect(self._on_click_AxisReset)
        self.ui.btnGuideReset.clicked.connect(self._on_click_GuideReset)
            

    def _load_ui(self):
        loader = QUiLoader()
        ui_path = os.path.join(os.path.dirname(__file__), "Achse_Linux.ui")
        ui_file = QFile(ui_path)

        if not ui_file.exists():
            raise FileNotFoundError(f"UI file not found: {ui_path}")
        if not ui_file.open(QFile.ReadOnly):
            raise IOError(f"Cannot open UI file: {ui_path}")

        self.ui = loader.load(ui_file, self)
        ui_file.close()

        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)

        self.setFixedSize(self.ui.size())

    def _on_click_PosEdit(self):
        self.edit_setPosProps_requested.emit() 

    def _on_click_VelEdit(self):
        self.edit_setVelProps_requested.emit()

    def _on_click_FilterEdit(self):
        self.edit_setFilterProps_requested.emit()

    def _on_click_GuideEdit(self):
        self.edit_setGuideProps_requested.emit()

    def _on_axis_select(self, index):
        axis_name = self.ui.cmbAxisName.itemText(index)
        self.axis_selected.emit(axis_name)

    def _on_click_EsReset(self):
        self.click_EsReset_requested.emit()

    def _on_click_EStop(self):
        self.click_EStop_requested.emit()

    def _on_click_Recover(self):
        self.click_Recover_requested.emit()

    def _on_click_ReSync(self):
        self.click_ReSync_requested.emit()

    def _on_click_AxisReset(self):
        self.click_AxisReset_requested.emit()

    def _on_click_GuideReset(self):
        self.click_GuideReset_requested.emit()



    def get_properties(self):
        """Collects all properties from the UI widgets and returns them as a dictionary."""
        props = {}
        for name, (widget_type, path, fmt) in self._bindings.items():
            widget = getattr(self.ui, name, None)
            if not widget:
                continue

            if widget_type in ("QLineEdit", "QLabel"):
                value = widget.text()
                if fmt:
                    value_clean = re.sub(r"[^\d.\-]+", "", value)
                    try:
                        value = fmt.format(float(value_clean)) if value_clean else None
                    except ValueError:
                        value = None
                    

            elif widget_type == "QRadioButton":
                value = widget.isChecked()
            elif widget_type == "QSlider":
                value = widget.value()
            elif widget_type == "QCheckBox":
                value = widget.isChecked()
            else:
                continue

            # Resolve the path to the property
            parts = path.split(".")
            current = props
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = value

        return props
    
    def closeEvent(self, event):
        if self.controller:
            print("[Widget] Window close requested. Calling controller.shutdown()...")
            self.controller.shutdown()
        else:
            print("[Widget] Window close requested, but no controller linked.")
        super().closeEvent(event)

