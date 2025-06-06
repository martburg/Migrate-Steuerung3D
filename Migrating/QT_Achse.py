from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSlider, QRadioButton, QGridLayout, QComboBox, QSizePolicy, QFrame, QGroupBox
)
from PySide6.QtCore import QTimer, Qt
import sys


class YellowAxisWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yellow Axis UI (Qt)")
        self.resize(1100, 850)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # --- Axis Selection and State Readout ---
        top_group = QGroupBox("Axis State")
        top_bar = QHBoxLayout(top_group)

        self.cmb_axis_name = QComboBox()
        top_bar.addWidget(QLabel("Axis Name:"))
        top_bar.addWidget(self.cmb_axis_name)

        self.status_label = QLabel("Status: ---")
        top_bar.addWidget(self.status_label)

        self.txt_pos = QLineEdit(); self.txt_pos.setReadOnly(True)
        self.txt_vel = QLineEdit(); self.txt_vel.setReadOnly(True)
        self.txt_amp = QLineEdit(); self.txt_amp.setReadOnly(True)
        self.txt_temp = QLineEdit(); self.txt_temp.setReadOnly(True)

        for label, widget in [("Pos:", self.txt_pos), ("Vel:", self.txt_vel),
                              ("Amp:", self.txt_amp), ("Temp:", self.txt_temp)]:
            top_bar.addWidget(QLabel(label))
            top_bar.addWidget(widget)

        self.led_estop = QLabel("EStop")
        self.led_enable = QLabel("Enable")
        self.led_estop.setStyleSheet("background-color: red; color: white; padding: 3px;")
        self.led_enable.setStyleSheet("background-color: green; color: white; padding: 3px;")
        top_bar.addWidget(self.led_estop)
        top_bar.addWidget(self.led_enable)

        layout.addWidget(top_group)

        # --- Manual Control ---
        control_group = QGroupBox("Manual Control")
        mid_bar = QHBoxLayout(control_group)
        self.slider_vel = QSlider(Qt.Horizontal)
        self.slider_vel.setRange(-1000, 1000)
        self.slider_vel.setValue(0)
        self.slider_vel.setTickInterval(100)
        self.slider_vel.setTickPosition(QSlider.TicksBelow)
        mid_bar.addWidget(QLabel("Velocity:"))
        mid_bar.addWidget(self.slider_vel, 1)

        self.btn_zero = QPushButton("Zero")
        self.btn_ref = QPushButton("Ref")
        self.btn_enable = QPushButton("Enable")
        self.btn_disable = QPushButton("Disable")
        self.btn_estop_reset = QPushButton("Reset EStop")

        for btn in [self.btn_zero, self.btn_ref, self.btn_enable, self.btn_disable, self.btn_estop_reset]:
            mid_bar.addWidget(btn)

        layout.addWidget(control_group)

        # --- RampForm Selection ---
        ramp_box = QGroupBox("Ramp Form")
        ramp_layout = QHBoxLayout(ramp_box)
        self.radio_linear = QRadioButton("Linear")
        self.radio_scurve = QRadioButton("S-Curve")
        self.radio_linear.setChecked(True)
        ramp_layout.addWidget(self.radio_linear)
        ramp_layout.addWidget(self.radio_scurve)
        layout.addWidget(ramp_box)

        # --- Motion Limits and Position Config ---
        config_box = QGroupBox("Motion and Position Limits")
        grid = QGridLayout(config_box)

        self.txt_pos_hard_max = QLineEdit()
        self.txt_pos_user_max = QLineEdit()
        self.txt_pos_user_min = QLineEdit()
        self.txt_pos_hard_min = QLineEdit()
        self.txt_pos_win = QLineEdit()

        pos_labels = ["Pos Hard Max:", "Pos User Max:", "Pos User Min:", "Pos Hard Min:", "PosWin:"]
        pos_fields = [self.txt_pos_hard_max, self.txt_pos_user_max, self.txt_pos_user_min, self.txt_pos_hard_min, self.txt_pos_win]

        for row, (label, field) in enumerate(zip(pos_labels, pos_fields)):
            grid.addWidget(QLabel(label), row, 0)
            grid.addWidget(field, row, 1)

        self.txt_vel_max = QLineEdit()
        self.txt_acc_max = QLineEdit()
        self.txt_dcc_max = QLineEdit()
        self.txt_acc_tot = QLineEdit()
        self.txt_amp_max = QLineEdit()
        self.txt_vel_win = QLineEdit()

        vel_labels = ["Vel Max:", "Acc Max:", "Dcc Max:", "Acc Tot:", "Max Amp:", "Vel Win:"]
        vel_fields = [self.txt_vel_max, self.txt_acc_max, self.txt_dcc_max, self.txt_acc_tot, self.txt_amp_max, self.txt_vel_win]

        for row, (label, field) in enumerate(zip(vel_labels, vel_fields)):
            grid.addWidget(QLabel(label), row, 2)
            grid.addWidget(field, row, 3)

        layout.addWidget(config_box)

        # --- Filter and Rope Config ---
        misc_box = QGroupBox("Filter and Rope Setup")
        misc_grid = QGridLayout(misc_box)
        self.txt_filter_p = QLineEdit()
        self.txt_filter_i = QLineEdit()
        self.txt_filter_d = QLineEdit()
        self.txt_filter_il = QLineEdit()
        self.txt_rope_swll = QLineEdit()
        self.txt_rope_diam = QLineEdit()
        self.txt_rope_type = QLineEdit()
        self.txt_rope_number = QLineEdit()
        self.txt_rope_length = QLineEdit()

        misc_labels = ["Filter P:", "Filter I:", "Filter D:", "Filter IL:", "Rope SWLL:", "Rope Diam:",
                       "Rope Type:", "Rope Number:", "Rope Length:"]
        misc_fields = [self.txt_filter_p, self.txt_filter_i, self.txt_filter_d, self.txt_filter_il,
                       self.txt_rope_swll, self.txt_rope_diam, self.txt_rope_type, self.txt_rope_number,
                       self.txt_rope_length]

        for row, (label, field) in enumerate(zip(misc_labels, misc_fields)):
            misc_grid.addWidget(QLabel(label), row, 0)
            misc_grid.addWidget(field, row, 1)

        layout.addWidget(misc_box)

        # --- Guide Configuration ---
        guide_box = QGroupBox("Guide Setup")
        guide = QGridLayout(guide_box)
        self.txt_guide_pitch = QLineEdit()
        self.txt_guide_pos_max = QLineEdit()
        self.txt_guide_pos_min = QLineEdit()
        guide.addWidget(QLabel("Guide Pitch:"), 0, 0)
        guide.addWidget(self.txt_guide_pitch, 0, 1)
        guide.addWidget(QLabel("Guide Pos Max:"), 1, 0)
        guide.addWidget(self.txt_guide_pos_max, 1, 1)
        guide.addWidget(QLabel("Guide Pos Min:"), 2, 0)
        guide.addWidget(self.txt_guide_pos_min, 2, 1)
        layout.addWidget(guide_box)

        # --- Control Buttons ---
        btnrow = QHBoxLayout()
        self.btn_write_all = QPushButton("Write All")
        self.btn_cancel_all = QPushButton("Cancel")
        btnrow.addStretch(1)
        btnrow.addWidget(self.btn_write_all)
        btnrow.addWidget(self.btn_cancel_all)
        layout.addLayout(btnrow)

        # --- Timer Setup ---
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll)
        self.timer.start(100)

    def poll(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YellowAxisWindow()
    window.show()
    sys.exit(app.exec())
