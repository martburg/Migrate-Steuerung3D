# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Achse_Linux.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_StatusForm(object):
    def setupUi(self, StatusForm):
        if not StatusForm.objectName():
            StatusForm.setObjectName(u"StatusForm")
        StatusForm.resize(856, 433)
        StatusForm.setStyleSheet(u"QGroupBox {\n"
"    background-color: #909090;\n"
"}\n"
"")
        self.mainLayout = QVBoxLayout(StatusForm)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.gbEngine = QGroupBox(StatusForm)
        self.gbEngine.setObjectName(u"gbEngine")
        self.engineLayout = QHBoxLayout(self.gbEngine)
        self.engineLayout.setSpacing(9)
        self.engineLayout.setObjectName(u"engineLayout")
        self.engineLayout.setContentsMargins(9, 0, 9, 9)
        self.cmbAxisName = QComboBox(self.gbEngine)
        self.cmbAxisName.addItem("")
        self.cmbAxisName.addItem("")
        self.cmbAxisName.addItem("")
        self.cmbAxisName.addItem("")
        self.cmbAxisName.addItem("")
        self.cmbAxisName.addItem("")
        self.cmbAxisName.setObjectName(u"cmbAxisName")
        self.cmbAxisName.setPlaceholderText(u"")

        self.engineLayout.addWidget(self.cmbAxisName)

        self.txtPosIst = QLineEdit(self.gbEngine)
        self.txtPosIst.setObjectName(u"txtPosIst")
        self.txtPosIst.setEnabled(False)
        self.txtPosIst.setMaximumSize(QSize(64, 16777215))

        self.engineLayout.addWidget(self.txtPosIst)

        self.txtSpeedIstUI = QLineEdit(self.gbEngine)
        self.txtSpeedIstUI.setObjectName(u"txtSpeedIstUI")
        self.txtSpeedIstUI.setEnabled(False)
        self.txtSpeedIstUI.setMaximumSize(QSize(64, 16777215))

        self.engineLayout.addWidget(self.txtSpeedIstUI)

        self.txtActCurUI = QLineEdit(self.gbEngine)
        self.txtActCurUI.setObjectName(u"txtActCurUI")
        self.txtActCurUI.setEnabled(False)
        self.txtActCurUI.setMaximumSize(QSize(64, 16777215))

        self.engineLayout.addWidget(self.txtActCurUI)

        self.sldAxisVel = QSlider(self.gbEngine)
        self.sldAxisVel.setObjectName(u"sldAxisVel")
        self.sldAxisVel.setMinimum(-32767)
        self.sldAxisVel.setMaximum(32767)
        self.sldAxisVel.setOrientation(QSlider.Horizontal)

        self.engineLayout.addWidget(self.sldAxisVel)

        self.txtStatus = QLineEdit(self.gbEngine)
        self.txtStatus.setObjectName(u"txtStatus")
        self.txtStatus.setEnabled(False)
        self.txtStatus.setMaximumSize(QSize(120, 16777215))

        self.engineLayout.addWidget(self.txtStatus)

        self.btnAxisReset = QPushButton(self.gbEngine)
        self.btnAxisReset.setObjectName(u"btnAxisReset")
        self.btnAxisReset.setEnabled(False)

        self.engineLayout.addWidget(self.btnAxisReset)

        self.txtCabTemperature = QLineEdit(self.gbEngine)
        self.txtCabTemperature.setObjectName(u"txtCabTemperature")
        self.txtCabTemperature.setEnabled(False)
        self.txtCabTemperature.setMaximumSize(QSize(40, 16777215))

        self.engineLayout.addWidget(self.txtCabTemperature)

        self.txtTimeTick = QLineEdit(self.gbEngine)
        self.txtTimeTick.setObjectName(u"txtTimeTick")
        self.txtTimeTick.setEnabled(False)
        self.txtTimeTick.setMaximumSize(QSize(30, 16777215))

        self.engineLayout.addWidget(self.txtTimeTick)


        self.mainLayout.addWidget(self.gbEngine)

        self.groupBox = QGroupBox(StatusForm)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 9, 0, 9)
        self.horizontalSpacer_12 = QSpacerItem(44, 13, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_12)

        self.txtSelected1 = QLineEdit(self.groupBox)
        self.txtSelected1.setObjectName(u"txtSelected1")
        self.txtSelected1.setEnabled(False)
        self.txtSelected1.setMaximumSize(QSize(16777215, 20))
        self.txtSelected1.setEchoMode(QLineEdit.Normal)
        self.txtSelected1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.txtSelected1)

        self.horizontalSpacer_11 = QSpacerItem(45, 13, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_11)

        self.cbFBT = QCheckBox(self.groupBox)
        self.cbFBT.setObjectName(u"cbFBT")

        self.horizontalLayout.addWidget(self.cbFBT)

        self.horizontalSpacer_15 = QSpacerItem(44, 13, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_15)

        self.cbReady = QCheckBox(self.groupBox)
        self.cbReady.setObjectName(u"cbReady")

        self.horizontalLayout.addWidget(self.cbReady)

        self.horizontalSpacer_13 = QSpacerItem(44, 13, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_13)

        self.cbOnline = QCheckBox(self.groupBox)
        self.cbOnline.setObjectName(u"cbOnline")

        self.horizontalLayout.addWidget(self.cbOnline)

        self.horizontalSpacer_16 = QSpacerItem(43, 13, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_16)

        self.cbBrake1 = QCheckBox(self.groupBox)
        self.cbBrake1.setObjectName(u"cbBrake1")

        self.horizontalLayout.addWidget(self.cbBrake1)

        self.horizontalSpacer_10 = QSpacerItem(44, 13, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_10)

        self.cbBrake2 = QCheckBox(self.groupBox)
        self.cbBrake2.setObjectName(u"cbBrake2")

        self.horizontalLayout.addWidget(self.cbBrake2)

        self.horizontalSpacer_14 = QSpacerItem(45, 13, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_14)

        self.txtSelected2 = QLineEdit(self.groupBox)
        self.txtSelected2.setObjectName(u"txtSelected2")
        self.txtSelected2.setEnabled(False)
        self.txtSelected2.setMaximumSize(QSize(16777215, 20))
        self.txtSelected2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.txtSelected2)

        self.horizontalSpacer_9 = QSpacerItem(44, 13, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_9)


        self.mainLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(StatusForm)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gbPositions = QGroupBox(self.groupBox_2)
        self.gbPositions.setObjectName(u"gbPositions")
        self.gbPositions.setStyleSheet(u"QGroupBox {\n"
"    background-color: #d0d0d0;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(self.gbPositions)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_3 = QGroupBox(self.gbPositions)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMaximumSize(QSize(16777215, 30))
        self.groupBox_3.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_44 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.horizontalLayout_44.setContentsMargins(-1, 5, -1, 0)
        self.btnPosEdit = QPushButton(self.groupBox_3)
        self.btnPosEdit.setObjectName(u"btnPosEdit")
        self.btnPosEdit.setEnabled(False)
        self.btnPosEdit.setMinimumSize(QSize(0, 20))
        self.btnPosEdit.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_44.addWidget(self.btnPosEdit)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_11)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.groupBox_18 = QGroupBox(self.gbPositions)
        self.groupBox_18.setObjectName(u"groupBox_18")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_18.sizePolicy().hasHeightForWidth())
        self.groupBox_18.setSizePolicy(sizePolicy)
        self.groupBox_18.setMaximumSize(QSize(16777215, 30))
        self.groupBox_18.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_11 = QHBoxLayout(self.groupBox_18)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, 0)
        self.label_9 = QLabel(self.groupBox_18)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_11.addWidget(self.label_9)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_17)

        self.txtHardMax = QLineEdit(self.groupBox_18)
        self.txtHardMax.setObjectName(u"txtHardMax")
        self.txtHardMax.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.txtHardMax.sizePolicy().hasHeightForWidth())
        self.txtHardMax.setSizePolicy(sizePolicy1)
        self.txtHardMax.setMinimumSize(QSize(64, 20))
        self.txtHardMax.setMaximumSize(QSize(70, 20))
        self.txtHardMax.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.txtHardMax)


        self.verticalLayout.addWidget(self.groupBox_18)

        self.groupBox_17 = QGroupBox(self.gbPositions)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.groupBox_17.setMaximumSize(QSize(16777215, 30))
        self.groupBox_17.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_10 = QHBoxLayout(self.groupBox_17)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, 0)
        self.label_8 = QLabel(self.groupBox_17)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_10.addWidget(self.label_8)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_8)

        self.txtUserMax = QLineEdit(self.groupBox_17)
        self.txtUserMax.setObjectName(u"txtUserMax")
        self.txtUserMax.setEnabled(False)
        self.txtUserMax.setMinimumSize(QSize(64, 0))
        self.txtUserMax.setMaximumSize(QSize(64, 20))
        self.txtUserMax.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.txtUserMax)


        self.verticalLayout.addWidget(self.groupBox_17)

        self.groupBox_16 = QGroupBox(self.gbPositions)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.groupBox_16.setMaximumSize(QSize(16777215, 30))
        self.groupBox_16.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_9 = QHBoxLayout(self.groupBox_16)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, 0)
        self.label_7 = QLabel(self.groupBox_16)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_9.addWidget(self.label_7)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_7)

        self.txtPosOffset = QLineEdit(self.groupBox_16)
        self.txtPosOffset.setObjectName(u"txtPosOffset")
        self.txtPosOffset.setEnabled(False)
        self.txtPosOffset.setMinimumSize(QSize(64, 0))
        self.txtPosOffset.setMaximumSize(QSize(64, 20))
        self.txtPosOffset.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.txtPosOffset)


        self.verticalLayout.addWidget(self.groupBox_16)

        self.groupBox_15 = QGroupBox(self.gbPositions)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setMaximumSize(QSize(16777215, 30))
        self.groupBox_15.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_8 = QHBoxLayout(self.groupBox_15)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.label_6 = QLabel(self.groupBox_15)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_8.addWidget(self.label_6)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.txtUserMin = QLineEdit(self.groupBox_15)
        self.txtUserMin.setObjectName(u"txtUserMin")
        self.txtUserMin.setEnabled(False)
        self.txtUserMin.setMinimumSize(QSize(64, 0))
        self.txtUserMin.setMaximumSize(QSize(64, 20))
        self.txtUserMin.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.txtUserMin)


        self.verticalLayout.addWidget(self.groupBox_15)

        self.groupBox_10 = QGroupBox(self.gbPositions)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setMaximumSize(QSize(16777215, 30))
        self.groupBox_10.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.label = QLabel(self.groupBox_10)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_3.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.txtHardMin = QLineEdit(self.groupBox_10)
        self.txtHardMin.setObjectName(u"txtHardMin")
        self.txtHardMin.setEnabled(False)
        self.txtHardMin.setMinimumSize(QSize(64, 0))
        self.txtHardMin.setMaximumSize(QSize(64, 20))
        self.txtHardMin.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.txtHardMin)


        self.verticalLayout.addWidget(self.groupBox_10)

        self.groupBox_14 = QGroupBox(self.gbPositions)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setMaximumSize(QSize(16777215, 30))
        self.groupBox_14.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_14)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.label_5 = QLabel(self.groupBox_14)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_7.addWidget(self.label_5)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.txtPosWin = QLineEdit(self.groupBox_14)
        self.txtPosWin.setObjectName(u"txtPosWin")
        self.txtPosWin.setEnabled(False)
        self.txtPosWin.setMinimumSize(QSize(64, 0))
        self.txtPosWin.setMaximumSize(QSize(64, 20))
        self.txtPosWin.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.txtPosWin)


        self.verticalLayout.addWidget(self.groupBox_14)

        self.groupBox_19 = QGroupBox(self.gbPositions)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.groupBox_19.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_12 = QHBoxLayout(self.groupBox_19)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 5, -1, 5)
        self.btnPosWrite = QPushButton(self.groupBox_19)
        self.btnPosWrite.setObjectName(u"btnPosWrite")
        self.btnPosWrite.setEnabled(False)
        self.btnPosWrite.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_12.addWidget(self.btnPosWrite)

        self.horizontalSpacer_35 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_35)

        self.btnPosCancel = QPushButton(self.groupBox_19)
        self.btnPosCancel.setObjectName(u"btnPosCancel")
        self.btnPosCancel.setEnabled(False)
        self.btnPosCancel.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_12.addWidget(self.btnPosCancel)


        self.verticalLayout.addWidget(self.groupBox_19)


        self.horizontalLayout_2.addWidget(self.gbPositions)

        self.gbVel = QGroupBox(self.groupBox_2)
        self.gbVel.setObjectName(u"gbVel")
        self.gbVel.setStyleSheet(u"QGroupBox {\n"
"    background-color: #d0d0d0;\n"
"}\n"
"")
        self.verticalLayout_2 = QVBoxLayout(self.gbVel)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBox_4 = QGroupBox(self.gbVel)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMaximumSize(QSize(16777215, 30))
        self.groupBox_4.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_45 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.horizontalLayout_45.setContentsMargins(-1, 5, -1, 0)
        self.btnVelEdit = QPushButton(self.groupBox_4)
        self.btnVelEdit.setObjectName(u"btnVelEdit")
        self.btnVelEdit.setEnabled(False)
        self.btnVelEdit.setMinimumSize(QSize(0, 20))
        self.btnVelEdit.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_45.addWidget(self.btnVelEdit)


        self.verticalLayout_2.addWidget(self.groupBox_4)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_6)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.groupBox_25 = QGroupBox(self.gbVel)
        self.groupBox_25.setObjectName(u"groupBox_25")
        self.groupBox_25.setMaximumSize(QSize(16777215, 30))
        self.groupBox_25.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_18 = QHBoxLayout(self.groupBox_25)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(-1, 0, -1, 0)
        self.label_15 = QLabel(self.groupBox_25)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_18.addWidget(self.label_15)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_23)

        self.txtVelMaxMot = QLineEdit(self.groupBox_25)
        self.txtVelMaxMot.setObjectName(u"txtVelMaxMot")
        self.txtVelMaxMot.setEnabled(False)
        self.txtVelMaxMot.setMinimumSize(QSize(64, 0))
        self.txtVelMaxMot.setMaximumSize(QSize(64, 20))
        self.txtVelMaxMot.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_18.addWidget(self.txtVelMaxMot)


        self.verticalLayout_2.addWidget(self.groupBox_25)

        self.groupBox_24 = QGroupBox(self.gbVel)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.groupBox_24.setMaximumSize(QSize(16777215, 30))
        self.groupBox_24.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_17 = QHBoxLayout(self.groupBox_24)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(-1, 0, -1, 0)
        self.label_14 = QLabel(self.groupBox_24)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_17.addWidget(self.label_14)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_22)

        self.txtVelMax = QLineEdit(self.groupBox_24)
        self.txtVelMax.setObjectName(u"txtVelMax")
        self.txtVelMax.setEnabled(False)
        self.txtVelMax.setMinimumSize(QSize(64, 0))
        self.txtVelMax.setMaximumSize(QSize(64, 20))
        self.txtVelMax.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_17.addWidget(self.txtVelMax)


        self.verticalLayout_2.addWidget(self.groupBox_24)

        self.groupBox_23 = QGroupBox(self.gbVel)
        self.groupBox_23.setObjectName(u"groupBox_23")
        self.groupBox_23.setMaximumSize(QSize(16777215, 30))
        self.groupBox_23.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_16 = QHBoxLayout(self.groupBox_23)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(-1, 0, -1, 0)
        self.label_13 = QLabel(self.groupBox_23)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_16.addWidget(self.label_13)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_21)

        self.txtAccMax = QLineEdit(self.groupBox_23)
        self.txtAccMax.setObjectName(u"txtAccMax")
        self.txtAccMax.setEnabled(False)
        self.txtAccMax.setMinimumSize(QSize(64, 0))
        self.txtAccMax.setMaximumSize(QSize(64, 20))
        self.txtAccMax.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_16.addWidget(self.txtAccMax)


        self.verticalLayout_2.addWidget(self.groupBox_23)

        self.groupBox_26 = QGroupBox(self.gbVel)
        self.groupBox_26.setObjectName(u"groupBox_26")
        self.groupBox_26.setMaximumSize(QSize(16777215, 30))
        self.groupBox_26.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_19 = QHBoxLayout(self.groupBox_26)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(-1, 0, -1, 0)
        self.label_16 = QLabel(self.groupBox_26)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_19.addWidget(self.label_16)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_24)

        self.txtDccMax = QLineEdit(self.groupBox_26)
        self.txtDccMax.setObjectName(u"txtDccMax")
        self.txtDccMax.setEnabled(False)
        self.txtDccMax.setMinimumSize(QSize(64, 0))
        self.txtDccMax.setMaximumSize(QSize(64, 20))
        self.txtDccMax.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_19.addWidget(self.txtDccMax)


        self.verticalLayout_2.addWidget(self.groupBox_26)

        self.groupBox_22 = QGroupBox(self.gbVel)
        self.groupBox_22.setObjectName(u"groupBox_22")
        self.groupBox_22.setMaximumSize(QSize(16777215, 30))
        self.groupBox_22.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_15 = QHBoxLayout(self.groupBox_22)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(-1, 0, -1, 0)
        self.label_12 = QLabel(self.groupBox_22)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_15.addWidget(self.label_12)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_20)

        self.txtAccMove = QLineEdit(self.groupBox_22)
        self.txtAccMove.setObjectName(u"txtAccMove")
        self.txtAccMove.setEnabled(False)
        self.txtAccMove.setMinimumSize(QSize(64, 0))
        self.txtAccMove.setMaximumSize(QSize(64, 20))
        self.txtAccMove.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.txtAccMove)


        self.verticalLayout_2.addWidget(self.groupBox_22)

        self.groupBox_20 = QGroupBox(self.gbVel)
        self.groupBox_20.setObjectName(u"groupBox_20")
        self.groupBox_20.setMaximumSize(QSize(16777215, 30))
        self.groupBox_20.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_13 = QHBoxLayout(self.groupBox_20)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 0, -1, 0)
        self.label_10 = QLabel(self.groupBox_20)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_13.addWidget(self.label_10)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_18)

        self.txtMaxAmp = QLineEdit(self.groupBox_20)
        self.txtMaxAmp.setObjectName(u"txtMaxAmp")
        self.txtMaxAmp.setEnabled(False)
        self.txtMaxAmp.setMinimumSize(QSize(64, 0))
        self.txtMaxAmp.setMaximumSize(QSize(64, 20))
        self.txtMaxAmp.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.txtMaxAmp)


        self.verticalLayout_2.addWidget(self.groupBox_20)

        self.groupBox_21 = QGroupBox(self.gbVel)
        self.groupBox_21.setObjectName(u"groupBox_21")
        self.groupBox_21.setMaximumSize(QSize(16777215, 30))
        self.groupBox_21.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_14 = QHBoxLayout(self.groupBox_21)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, 0, -1, 0)
        self.label_11 = QLabel(self.groupBox_21)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_14.addWidget(self.label_11)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_19)

        self.txtVelWin = QLineEdit(self.groupBox_21)
        self.txtVelWin.setObjectName(u"txtVelWin")
        self.txtVelWin.setEnabled(False)
        self.txtVelWin.setMinimumSize(QSize(64, 0))
        self.txtVelWin.setMaximumSize(QSize(64, 20))
        self.txtVelWin.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_14.addWidget(self.txtVelWin)


        self.verticalLayout_2.addWidget(self.groupBox_21)

        self.groupBox_27 = QGroupBox(self.gbVel)
        self.groupBox_27.setObjectName(u"groupBox_27")
        self.groupBox_27.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_20 = QHBoxLayout(self.groupBox_27)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(-1, 5, -1, 5)
        self.btnVelWrite = QPushButton(self.groupBox_27)
        self.btnVelWrite.setObjectName(u"btnVelWrite")
        self.btnVelWrite.setEnabled(False)
        self.btnVelWrite.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_20.addWidget(self.btnVelWrite)

        self.horizontalSpacer_36 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_36)

        self.btnVelCancel = QPushButton(self.groupBox_27)
        self.btnVelCancel.setObjectName(u"btnVelCancel")
        self.btnVelCancel.setEnabled(False)
        self.btnVelCancel.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_20.addWidget(self.btnVelCancel)


        self.verticalLayout_2.addWidget(self.groupBox_27)


        self.horizontalLayout_2.addWidget(self.gbVel)

        self.gbGuider = QGroupBox(self.groupBox_2)
        self.gbGuider.setObjectName(u"gbGuider")
        self.verticalLayout_14 = QVBoxLayout(self.gbGuider)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.groupBox_54 = QGroupBox(self.gbGuider)
        self.groupBox_54.setObjectName(u"groupBox_54")
        self.groupBox_54.setMaximumSize(QSize(16777215, 30))
        self.groupBox_54.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_36 = QHBoxLayout(self.groupBox_54)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(-1, 0, -1, 0)
        self.txtGuidePosIstUI = QLineEdit(self.groupBox_54)
        self.txtGuidePosIstUI.setObjectName(u"txtGuidePosIstUI")
        self.txtGuidePosIstUI.setEnabled(False)
        self.txtGuidePosIstUI.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_36.addWidget(self.txtGuidePosIstUI)

        self.btnGuideEngaged = QPushButton(self.groupBox_54)
        self.btnGuideEngaged.setObjectName(u"btnGuideEngaged")
        self.btnGuideEngaged.setEnabled(False)
        self.btnGuideEngaged.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_36.addWidget(self.btnGuideEngaged)

        self.txtGuideIstSpeedUI = QLineEdit(self.groupBox_54)
        self.txtGuideIstSpeedUI.setObjectName(u"txtGuideIstSpeedUI")
        self.txtGuideIstSpeedUI.setEnabled(False)
        self.txtGuideIstSpeedUI.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_36.addWidget(self.txtGuideIstSpeedUI)


        self.verticalLayout_14.addWidget(self.groupBox_54)

        self.groupBox_53 = QGroupBox(self.gbGuider)
        self.groupBox_53.setObjectName(u"groupBox_53")
        self.groupBox_53.setMaximumSize(QSize(16777215, 30))
        self.groupBox_53.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_37 = QHBoxLayout(self.groupBox_53)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(-1, 0, -1, 0)
        self.txtGuideStatus = QLineEdit(self.groupBox_53)
        self.txtGuideStatus.setObjectName(u"txtGuideStatus")
        self.txtGuideStatus.setEnabled(False)
        self.txtGuideStatus.setMaximumSize(QSize(80, 20))

        self.horizontalLayout_37.addWidget(self.txtGuideStatus)

        self.horizontalSpacer_41 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_41)

        self.btnGuideReset = QPushButton(self.groupBox_53)
        self.btnGuideReset.setObjectName(u"btnGuideReset")
        self.btnGuideReset.setEnabled(False)
        self.btnGuideReset.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_37.addWidget(self.btnGuideReset)


        self.verticalLayout_14.addWidget(self.groupBox_53)

        self.groupBox_50 = QGroupBox(self.gbGuider)
        self.groupBox_50.setObjectName(u"groupBox_50")
        self.groupBox_50.setMaximumSize(QSize(16777215, 30))
        self.groupBox_50.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_38 = QHBoxLayout(self.groupBox_50)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(-1, 0, -1, 0)
        self.horizontalSpacer_39 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_38.addItem(self.horizontalSpacer_39)

        self.cbGuideReady = QCheckBox(self.groupBox_50)
        self.cbGuideReady.setObjectName(u"cbGuideReady")
        self.cbGuideReady.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_38.addWidget(self.cbGuideReady)

        self.cbGuideOnline = QCheckBox(self.groupBox_50)
        self.cbGuideOnline.setObjectName(u"cbGuideOnline")
        self.cbGuideOnline.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_38.addWidget(self.cbGuideOnline)

        self.horizontalSpacer_40 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_38.addItem(self.horizontalSpacer_40)


        self.verticalLayout_14.addWidget(self.groupBox_50)

        self.groupBox_51 = QGroupBox(self.gbGuider)
        self.groupBox_51.setObjectName(u"groupBox_51")
        self.groupBox_51.setMaximumSize(QSize(16777215, 30))
        self.groupBox_51.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_39 = QHBoxLayout(self.groupBox_51)
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.horizontalLayout_39.setContentsMargins(-1, 0, -1, 0)
        self.sldGuideSpeed = QSlider(self.groupBox_51)
        self.sldGuideSpeed.setObjectName(u"sldGuideSpeed")
        self.sldGuideSpeed.setMaximumSize(QSize(16777215, 20))
        self.sldGuideSpeed.setMinimum(-32767)
        self.sldGuideSpeed.setMaximum(32767)
        self.sldGuideSpeed.setOrientation(QSlider.Horizontal)

        self.horizontalLayout_39.addWidget(self.sldGuideSpeed)


        self.verticalLayout_14.addWidget(self.groupBox_51)

        self.groupBox_52 = QGroupBox(self.gbGuider)
        self.groupBox_52.setObjectName(u"groupBox_52")
        self.groupBox_52.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.verticalLayout_15 = QVBoxLayout(self.groupBox_52)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(-1, 0, -1, 0)
        self.groupBox_7 = QGroupBox(self.groupBox_52)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_48 = QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_48.setSpacing(0)
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.horizontalLayout_48.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_34 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_48.addItem(self.horizontalSpacer_34)

        self.btnGuideEdit = QPushButton(self.groupBox_7)
        self.btnGuideEdit.setObjectName(u"btnGuideEdit")
        self.btnGuideEdit.setEnabled(False)
        self.btnGuideEdit.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_48.addWidget(self.btnGuideEdit)

        self.horizontalSpacer_2 = QSpacerItem(64, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_48.addItem(self.horizontalSpacer_2)


        self.verticalLayout_15.addWidget(self.groupBox_7)

        self.groupBox_55 = QGroupBox(self.groupBox_52)
        self.groupBox_55.setObjectName(u"groupBox_55")
        self.groupBox_55.setMaximumSize(QSize(16777215, 30))
        self.groupBox_55.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_42 = QHBoxLayout(self.groupBox_55)
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.horizontalLayout_42.setContentsMargins(-1, 0, 12, 0)
        self.label_28 = QLabel(self.groupBox_55)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_42.addWidget(self.label_28)

        self.txtGuidePitch = QLineEdit(self.groupBox_55)
        self.txtGuidePitch.setObjectName(u"txtGuidePitch")
        self.txtGuidePitch.setEnabled(False)
        self.txtGuidePitch.setMinimumSize(QSize(64, 0))
        self.txtGuidePitch.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_42.addWidget(self.txtGuidePitch)

        self.btnGuideWrite = QPushButton(self.groupBox_55)
        self.btnGuideWrite.setObjectName(u"btnGuideWrite")
        self.btnGuideWrite.setEnabled(False)
        self.btnGuideWrite.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_42.addWidget(self.btnGuideWrite)


        self.verticalLayout_15.addWidget(self.groupBox_55)

        self.groupBox_57 = QGroupBox(self.groupBox_52)
        self.groupBox_57.setObjectName(u"groupBox_57")
        self.groupBox_57.setMaximumSize(QSize(16777215, 30))
        self.groupBox_57.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_41 = QHBoxLayout(self.groupBox_57)
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.horizontalLayout_41.setContentsMargins(-1, 0, 12, 0)
        self.label_29 = QLabel(self.groupBox_57)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_41.addWidget(self.label_29)

        self.txtGuidePosMax = QLineEdit(self.groupBox_57)
        self.txtGuidePosMax.setObjectName(u"txtGuidePosMax")
        self.txtGuidePosMax.setEnabled(False)
        self.txtGuidePosMax.setMinimumSize(QSize(64, 0))
        self.txtGuidePosMax.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_41.addWidget(self.txtGuidePosMax)

        self.txtGuidePosMaxMax = QLineEdit(self.groupBox_57)
        self.txtGuidePosMaxMax.setObjectName(u"txtGuidePosMaxMax")
        self.txtGuidePosMaxMax.setEnabled(False)
        self.txtGuidePosMaxMax.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_41.addWidget(self.txtGuidePosMaxMax)


        self.verticalLayout_15.addWidget(self.groupBox_57)

        self.groupBox_56 = QGroupBox(self.groupBox_52)
        self.groupBox_56.setObjectName(u"groupBox_56")
        self.groupBox_56.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_43 = QHBoxLayout(self.groupBox_56)
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_43.setContentsMargins(-1, 0, 12, 0)
        self.label_30 = QLabel(self.groupBox_56)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_43.addWidget(self.label_30)

        self.txtGuidePosMin = QLineEdit(self.groupBox_56)
        self.txtGuidePosMin.setObjectName(u"txtGuidePosMin")
        self.txtGuidePosMin.setEnabled(False)
        self.txtGuidePosMin.setMinimumSize(QSize(64, 0))
        self.txtGuidePosMin.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_43.addWidget(self.txtGuidePosMin)

        self.btnGuideCancel = QPushButton(self.groupBox_56)
        self.btnGuideCancel.setObjectName(u"btnGuideCancel")
        self.btnGuideCancel.setEnabled(False)
        self.btnGuideCancel.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_43.addWidget(self.btnGuideCancel)


        self.verticalLayout_15.addWidget(self.groupBox_56)


        self.verticalLayout_14.addWidget(self.groupBox_52)


        self.horizontalLayout_2.addWidget(self.gbGuider)

        self.gbFilter = QGroupBox(self.groupBox_2)
        self.gbFilter.setObjectName(u"gbFilter")
        self.gbFilter.setStyleSheet(u"QGroupBox {\n"
"    background-color: #d0d0d0;\n"
"}\n"
"")
        self.verticalLayout_3 = QVBoxLayout(self.gbFilter)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.groupBox_5 = QGroupBox(self.gbFilter)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMaximumSize(QSize(16777215, 30))
        self.groupBox_5.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_46 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.horizontalLayout_46.setContentsMargins(-1, 5, -1, 0)
        self.btnFilterEdit = QPushButton(self.groupBox_5)
        self.btnFilterEdit.setObjectName(u"btnFilterEdit")
        self.btnFilterEdit.setEnabled(False)
        self.btnFilterEdit.setMinimumSize(QSize(0, 20))
        self.btnFilterEdit.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_46.addWidget(self.btnFilterEdit)


        self.verticalLayout_3.addWidget(self.groupBox_5)

        self.groupBox_12 = QGroupBox(self.gbFilter)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setMaximumSize(QSize(16777215, 30))
        self.groupBox_12.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_12)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.label_3 = QLabel(self.groupBox_12)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_5.addWidget(self.label_3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.txtLagError = QLineEdit(self.groupBox_12)
        self.txtLagError.setObjectName(u"txtLagError")
        self.txtLagError.setEnabled(False)
        self.txtLagError.setMinimumSize(QSize(64, 0))
        self.txtLagError.setMaximumSize(QSize(64, 20))
        self.txtLagError.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.txtLagError)


        self.verticalLayout_3.addWidget(self.groupBox_12)

        self.groupBox_28 = QGroupBox(self.gbFilter)
        self.groupBox_28.setObjectName(u"groupBox_28")
        self.groupBox_28.setMaximumSize(QSize(16777215, 30))
        self.groupBox_28.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_21 = QHBoxLayout(self.groupBox_28)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(-1, 0, -1, 0)
        self.label_17 = QLabel(self.groupBox_28)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_21.addWidget(self.label_17)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_25)

        self.txtFilterP = QLineEdit(self.groupBox_28)
        self.txtFilterP.setObjectName(u"txtFilterP")
        self.txtFilterP.setEnabled(False)
        self.txtFilterP.setMinimumSize(QSize(64, 0))
        self.txtFilterP.setMaximumSize(QSize(64, 20))
        self.txtFilterP.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_21.addWidget(self.txtFilterP)


        self.verticalLayout_3.addWidget(self.groupBox_28)

        self.groupBox_30 = QGroupBox(self.gbFilter)
        self.groupBox_30.setObjectName(u"groupBox_30")
        self.groupBox_30.setMaximumSize(QSize(16777215, 30))
        self.groupBox_30.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_23 = QHBoxLayout(self.groupBox_30)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(-1, 0, -1, 0)
        self.label_19 = QLabel(self.groupBox_30)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_23.addWidget(self.label_19)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_27)

        self.txtFilterI = QLineEdit(self.groupBox_30)
        self.txtFilterI.setObjectName(u"txtFilterI")
        self.txtFilterI.setEnabled(False)
        self.txtFilterI.setMinimumSize(QSize(64, 0))
        self.txtFilterI.setMaximumSize(QSize(64, 20))
        self.txtFilterI.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_23.addWidget(self.txtFilterI)


        self.verticalLayout_3.addWidget(self.groupBox_30)

        self.groupBox_29 = QGroupBox(self.gbFilter)
        self.groupBox_29.setObjectName(u"groupBox_29")
        self.groupBox_29.setMaximumSize(QSize(16777215, 30))
        self.groupBox_29.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_22 = QHBoxLayout(self.groupBox_29)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, 0, -1, 0)
        self.label_18 = QLabel(self.groupBox_29)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_22.addWidget(self.label_18)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_26)

        self.txtFilterD = QLineEdit(self.groupBox_29)
        self.txtFilterD.setObjectName(u"txtFilterD")
        self.txtFilterD.setEnabled(False)
        self.txtFilterD.setMinimumSize(QSize(64, 0))
        self.txtFilterD.setMaximumSize(QSize(64, 20))
        self.txtFilterD.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_22.addWidget(self.txtFilterD)


        self.verticalLayout_3.addWidget(self.groupBox_29)

        self.groupBox_32 = QGroupBox(self.gbFilter)
        self.groupBox_32.setObjectName(u"groupBox_32")
        self.groupBox_32.setMaximumSize(QSize(16777215, 30))
        self.groupBox_32.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_25 = QHBoxLayout(self.groupBox_32)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(-1, 0, -1, 0)
        self.label_21 = QLabel(self.groupBox_32)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_25.addWidget(self.label_21)

        self.horizontalSpacer_29 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_29)

        self.txtFilterIL = QLineEdit(self.groupBox_32)
        self.txtFilterIL.setObjectName(u"txtFilterIL")
        self.txtFilterIL.setEnabled(False)
        self.txtFilterIL.setMinimumSize(QSize(64, 0))
        self.txtFilterIL.setMaximumSize(QSize(64, 20))
        self.txtFilterIL.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_25.addWidget(self.txtFilterIL)


        self.verticalLayout_3.addWidget(self.groupBox_32)

        self.groupBox_31 = QGroupBox(self.gbFilter)
        self.groupBox_31.setObjectName(u"groupBox_31")
        self.groupBox_31.setMaximumSize(QSize(16777215, 30))
        self.groupBox_31.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_24 = QHBoxLayout(self.groupBox_31)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, 0, -1, 0)
        self.label_20 = QLabel(self.groupBox_31)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_24.addWidget(self.label_20)

        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_28)

        self.txtRampform = QLineEdit(self.groupBox_31)
        self.txtRampform.setObjectName(u"txtRampform")
        self.txtRampform.setEnabled(False)
        self.txtRampform.setMinimumSize(QSize(64, 0))
        self.txtRampform.setMaximumSize(QSize(64, 20))
        self.txtRampform.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_24.addWidget(self.txtRampform)


        self.verticalLayout_3.addWidget(self.groupBox_31)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_7)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_13)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.groupBox_33 = QGroupBox(self.gbFilter)
        self.groupBox_33.setObjectName(u"groupBox_33")
        self.groupBox_33.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_26 = QHBoxLayout(self.groupBox_33)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(-1, 5, -1, 5)
        self.btnFilterWrite = QPushButton(self.groupBox_33)
        self.btnFilterWrite.setObjectName(u"btnFilterWrite")
        self.btnFilterWrite.setEnabled(False)
        self.btnFilterWrite.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_26.addWidget(self.btnFilterWrite)

        self.horizontalSpacer_37 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_37)

        self.btnFilterCancel = QPushButton(self.groupBox_33)
        self.btnFilterCancel.setObjectName(u"btnFilterCancel")
        self.btnFilterCancel.setEnabled(False)
        self.btnFilterCancel.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_26.addWidget(self.btnFilterCancel)


        self.verticalLayout_3.addWidget(self.groupBox_33)


        self.horizontalLayout_2.addWidget(self.gbFilter)

        self.gbRope = QGroupBox(self.groupBox_2)
        self.gbRope.setObjectName(u"gbRope")
        self.gbRope.setStyleSheet(u"QGroupBox {\n"
"    background-color: #d0d0d0;\n"
"}\n"
"")
        self.verticalLayout_4 = QVBoxLayout(self.gbRope)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.groupBox_6 = QGroupBox(self.gbRope)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMaximumSize(QSize(16777215, 30))
        self.groupBox_6.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_47 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_47.setSpacing(0)
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.horizontalLayout_47.setContentsMargins(-1, 5, -1, 0)
        self.btnRopeEdit = QPushButton(self.groupBox_6)
        self.btnRopeEdit.setObjectName(u"btnRopeEdit")
        self.btnRopeEdit.setEnabled(False)
        self.btnRopeEdit.setMinimumSize(QSize(0, 20))
        self.btnRopeEdit.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_47.addWidget(self.btnRopeEdit)


        self.verticalLayout_4.addWidget(self.groupBox_6)

        self.groupBox_13 = QGroupBox(self.gbRope)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setMaximumSize(QSize(16777215, 30))
        self.groupBox_13.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_13)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, 0)
        self.label_4 = QLabel(self.groupBox_13)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_6.addWidget(self.label_4)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.txtRopeSWLL = QLineEdit(self.groupBox_13)
        self.txtRopeSWLL.setObjectName(u"txtRopeSWLL")
        self.txtRopeSWLL.setEnabled(False)
        self.txtRopeSWLL.setMinimumSize(QSize(64, 0))
        self.txtRopeSWLL.setMaximumSize(QSize(64, 20))
        self.txtRopeSWLL.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.txtRopeSWLL)


        self.verticalLayout_4.addWidget(self.groupBox_13)

        self.groupBox_36 = QGroupBox(self.gbRope)
        self.groupBox_36.setObjectName(u"groupBox_36")
        self.groupBox_36.setMaximumSize(QSize(16777215, 30))
        self.groupBox_36.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_29 = QHBoxLayout(self.groupBox_36)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(-1, 0, -1, 0)
        self.label_23 = QLabel(self.groupBox_36)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_29.addWidget(self.label_23)

        self.horizontalSpacer_31 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_31)

        self.txtRopeDiameter = QLineEdit(self.groupBox_36)
        self.txtRopeDiameter.setObjectName(u"txtRopeDiameter")
        self.txtRopeDiameter.setEnabled(False)
        self.txtRopeDiameter.setMinimumSize(QSize(64, 0))
        self.txtRopeDiameter.setMaximumSize(QSize(64, 20))
        self.txtRopeDiameter.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_29.addWidget(self.txtRopeDiameter)


        self.verticalLayout_4.addWidget(self.groupBox_36)

        self.groupBox_35 = QGroupBox(self.gbRope)
        self.groupBox_35.setObjectName(u"groupBox_35")
        self.groupBox_35.setMaximumSize(QSize(16777215, 30))
        self.groupBox_35.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_28 = QHBoxLayout(self.groupBox_35)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(-1, 0, -1, 0)
        self.label_22 = QLabel(self.groupBox_35)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_28.addWidget(self.label_22)

        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_30)

        self.txtRopeType = QLineEdit(self.groupBox_35)
        self.txtRopeType.setObjectName(u"txtRopeType")
        self.txtRopeType.setEnabled(False)
        self.txtRopeType.setMinimumSize(QSize(64, 0))
        self.txtRopeType.setMaximumSize(QSize(64, 20))
        self.txtRopeType.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_28.addWidget(self.txtRopeType)


        self.verticalLayout_4.addWidget(self.groupBox_35)

        self.groupBox_37 = QGroupBox(self.gbRope)
        self.groupBox_37.setObjectName(u"groupBox_37")
        self.groupBox_37.setMaximumSize(QSize(16777215, 30))
        self.groupBox_37.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_30 = QHBoxLayout(self.groupBox_37)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(-1, 0, -1, 0)
        self.label_24 = QLabel(self.groupBox_37)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_30.addWidget(self.label_24)

        self.horizontalSpacer_32 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_32)

        self.txtRopeNumber = QLineEdit(self.groupBox_37)
        self.txtRopeNumber.setObjectName(u"txtRopeNumber")
        self.txtRopeNumber.setEnabled(False)
        self.txtRopeNumber.setMinimumSize(QSize(64, 0))
        self.txtRopeNumber.setMaximumSize(QSize(64, 20))
        self.txtRopeNumber.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_30.addWidget(self.txtRopeNumber)


        self.verticalLayout_4.addWidget(self.groupBox_37)

        self.groupBox_38 = QGroupBox(self.gbRope)
        self.groupBox_38.setObjectName(u"groupBox_38")
        self.groupBox_38.setMaximumSize(QSize(16777215, 30))
        self.groupBox_38.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_31 = QHBoxLayout(self.groupBox_38)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(-1, 0, -1, 0)
        self.label_25 = QLabel(self.groupBox_38)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_31.addWidget(self.label_25)

        self.horizontalSpacer_33 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_33)

        self.txtRopeLength = QLineEdit(self.groupBox_38)
        self.txtRopeLength.setObjectName(u"txtRopeLength")
        self.txtRopeLength.setEnabled(False)
        self.txtRopeLength.setMinimumSize(QSize(64, 0))
        self.txtRopeLength.setMaximumSize(QSize(64, 20))
        self.txtRopeLength.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_31.addWidget(self.txtRopeLength)


        self.verticalLayout_4.addWidget(self.groupBox_38)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_15)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_8)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_14)

        self.groupBox_34 = QGroupBox(self.gbRope)
        self.groupBox_34.setObjectName(u"groupBox_34")
        self.groupBox_34.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.horizontalLayout_27 = QHBoxLayout(self.groupBox_34)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, 5, -1, 5)
        self.btnRopeWrite = QPushButton(self.groupBox_34)
        self.btnRopeWrite.setObjectName(u"btnRopeWrite")
        self.btnRopeWrite.setEnabled(False)
        self.btnRopeWrite.setMinimumSize(QSize(0, 20))
        self.btnRopeWrite.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_27.addWidget(self.btnRopeWrite)

        self.horizontalSpacer_38 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_38)

        self.btnRopeCancel = QPushButton(self.groupBox_34)
        self.btnRopeCancel.setObjectName(u"btnRopeCancel")
        self.btnRopeCancel.setEnabled(False)
        self.btnRopeCancel.setMinimumSize(QSize(0, 20))
        self.btnRopeCancel.setMaximumSize(QSize(64, 20))

        self.horizontalLayout_27.addWidget(self.btnRopeCancel)


        self.verticalLayout_4.addWidget(self.groupBox_34)


        self.horizontalLayout_2.addWidget(self.gbRope)


        self.mainLayout.addWidget(self.groupBox_2)

        self.gbRecover = QGroupBox(StatusForm)
        self.gbRecover.setObjectName(u"gbRecover")
        self.gbRecover.setStyleSheet(u"")
        self.horizontalLayout_4 = QHBoxLayout(self.gbRecover)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(9, 0, 9, 9)
        self.label_2 = QLabel(self.gbRecover)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.horizontalSpacer_44 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_44)

        self.txtEStopCutPos = QLineEdit(self.gbRecover)
        self.txtEStopCutPos.setObjectName(u"txtEStopCutPos")
        self.txtEStopCutPos.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.txtEStopCutPos.sizePolicy().hasHeightForWidth())
        self.txtEStopCutPos.setSizePolicy(sizePolicy1)
        self.txtEStopCutPos.setMinimumSize(QSize(64, 0))
        self.txtEStopCutPos.setMaximumSize(QSize(64, 16777215))

        self.horizontalLayout_4.addWidget(self.txtEStopCutPos)

        self.label_26 = QLabel(self.gbRecover)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_4.addWidget(self.label_26)

        self.txtEStopCutVel = QLineEdit(self.gbRecover)
        self.txtEStopCutVel.setObjectName(u"txtEStopCutVel")
        self.txtEStopCutVel.setEnabled(False)
        self.txtEStopCutVel.setMinimumSize(QSize(64, 0))
        self.txtEStopCutVel.setMaximumSize(QSize(64, 16777215))

        self.horizontalLayout_4.addWidget(self.txtEStopCutVel)

        self.horizontalSpacer_46 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_46)

        self.horizontalSpacer_42 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_42)

        self.txtEStopCutTime = QLineEdit(self.gbRecover)
        self.txtEStopCutTime.setObjectName(u"txtEStopCutTime")
        self.txtEStopCutTime.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.txtEStopCutTime.sizePolicy().hasHeightForWidth())
        self.txtEStopCutTime.setSizePolicy(sizePolicy1)
        self.txtEStopCutTime.setMinimumSize(QSize(170, 0))
        self.txtEStopCutTime.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.txtEStopCutTime)

        self.horizontalSpacer_43 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_43)

        self.label_27 = QLabel(self.gbRecover)
        self.label_27.setObjectName(u"label_27")

        self.horizontalLayout_4.addWidget(self.label_27)

        self.txtEStopPosDiff = QLineEdit(self.gbRecover)
        self.txtEStopPosDiff.setObjectName(u"txtEStopPosDiff")
        self.txtEStopPosDiff.setEnabled(False)
        self.txtEStopPosDiff.setMinimumSize(QSize(64, 0))
        self.txtEStopPosDiff.setMaximumSize(QSize(64, 16777215))

        self.horizontalLayout_4.addWidget(self.txtEStopPosDiff)

        self.btnRecover = QPushButton(self.gbRecover)
        self.btnRecover.setObjectName(u"btnRecover")
        self.btnRecover.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.btnRecover)

        self.btnResync = QPushButton(self.gbRecover)
        self.btnResync.setObjectName(u"btnResync")
        self.btnResync.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.btnResync)


        self.mainLayout.addWidget(self.gbRecover)

        self.gbEStop = QGroupBox(StatusForm)
        self.gbEStop.setObjectName(u"gbEStop")
        self.gbEStop.setStyleSheet(u"QGroupBox {\n"
"    background-color:rgb(245, 194, 17);\n"
"}")
        self.horizontalLayout_32 = QHBoxLayout(self.gbEStop)
        self.horizontalLayout_32.setSpacing(10)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.groupBox_11 = QGroupBox(self.gbEStop)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(15, 0, 0, 0)
        self.cbEsMaster = QCheckBox(self.groupBox_11)
        self.cbEsMaster.setObjectName(u"cbEsMaster")

        self.verticalLayout_5.addWidget(self.cbEsMaster)

        self.cbEsGuider = QCheckBox(self.groupBox_11)
        self.cbEsGuider.setObjectName(u"cbEsGuider")

        self.verticalLayout_5.addWidget(self.cbEsGuider)

        self.cbEsNetwork = QCheckBox(self.groupBox_11)
        self.cbEsNetwork.setObjectName(u"cbEsNetwork")

        self.verticalLayout_5.addWidget(self.cbEsNetwork)


        self.horizontalLayout_32.addWidget(self.groupBox_11)

        self.btnEsReset = QPushButton(self.gbEStop)
        self.btnEsReset.setObjectName(u"btnEsReset")
        self.btnEsReset.setEnabled(False)

        self.horizontalLayout_32.addWidget(self.btnEsReset)

        self.groupBox_39 = QGroupBox(self.gbEStop)
        self.groupBox_39.setObjectName(u"groupBox_39")
        self.horizontalLayout_33 = QHBoxLayout(self.groupBox_39)
        self.horizontalLayout_33.setSpacing(0)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.groupBox_42 = QGroupBox(self.groupBox_39)
        self.groupBox_42.setObjectName(u"groupBox_42")
        self.groupBox_42.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_42)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.cbEsEStop1 = QCheckBox(self.groupBox_42)
        self.cbEsEStop1.setObjectName(u"cbEsEStop1")
        self.cbEsEStop1.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")

        self.verticalLayout_6.addWidget(self.cbEsEStop1)

        self.cbEsEStop2 = QCheckBox(self.groupBox_42)
        self.cbEsEStop2.setObjectName(u"cbEsEStop2")

        self.verticalLayout_6.addWidget(self.cbEsEStop2)

        self.verticalSpacer_9 = QSpacerItem(20, 19, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_9)


        self.horizontalLayout_33.addWidget(self.groupBox_42)

        self.groupBox_44 = QGroupBox(self.groupBox_39)
        self.groupBox_44.setObjectName(u"groupBox_44")
        self.groupBox_44.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_44)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.cbEs30kW = QCheckBox(self.groupBox_44)
        self.cbEs30kW.setObjectName(u"cbEs30kW")

        self.verticalLayout_7.addWidget(self.cbEs30kW)

        self.cbEs05kW = QCheckBox(self.groupBox_44)
        self.cbEs05kW.setObjectName(u"cbEs05kW")

        self.verticalLayout_7.addWidget(self.cbEs05kW)

        self.verticalSpacer_10 = QSpacerItem(20, 19, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_10)


        self.horizontalLayout_33.addWidget(self.groupBox_44)

        self.groupBox_43 = QGroupBox(self.groupBox_39)
        self.groupBox_43.setObjectName(u"groupBox_43")
        self.groupBox_43.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_43)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.cbEsBRK1OK = QCheckBox(self.groupBox_43)
        self.cbEsBRK1OK.setObjectName(u"cbEsBRK1OK")

        self.verticalLayout_8.addWidget(self.cbEsBRK1OK)

        self.cbEsBRK2OK = QCheckBox(self.groupBox_43)
        self.cbEsBRK2OK.setObjectName(u"cbEsBRK2OK")

        self.verticalLayout_8.addWidget(self.cbEsBRK2OK)

        self.cbEsBRK2KB = QCheckBox(self.groupBox_43)
        self.cbEsBRK2KB.setObjectName(u"cbEsBRK2KB")

        self.verticalLayout_8.addWidget(self.cbEsBRK2KB)


        self.horizontalLayout_33.addWidget(self.groupBox_43)


        self.horizontalLayout_32.addWidget(self.groupBox_39)

        self.groupBox_40 = QGroupBox(self.gbEStop)
        self.groupBox_40.setObjectName(u"groupBox_40")
        self.horizontalLayout_34 = QHBoxLayout(self.groupBox_40)
        self.horizontalLayout_34.setSpacing(0)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.gbSps = QGroupBox(self.groupBox_40)
        self.gbSps.setObjectName(u"gbSps")
        self.gbSps.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.verticalLayout_9 = QVBoxLayout(self.gbSps)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.cbEsSPS = QCheckBox(self.gbSps)
        self.cbEsSPS.setObjectName(u"cbEsSPS")

        self.verticalLayout_9.addWidget(self.cbEsSPS)

        self.cbEsRED = QCheckBox(self.gbSps)
        self.cbEsRED.setObjectName(u"cbEsRED")

        self.verticalLayout_9.addWidget(self.cbEsRED)

        self.cbEsENC = QCheckBox(self.gbSps)
        self.cbEsENC.setObjectName(u"cbEsENC")

        self.verticalLayout_9.addWidget(self.cbEsENC)


        self.horizontalLayout_34.addWidget(self.gbSps)

        self.gbPos = QGroupBox(self.groupBox_40)
        self.gbPos.setObjectName(u"gbPos")
        self.gbPos.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.verticalLayout_10 = QVBoxLayout(self.gbPos)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.cbEsPosWin = QCheckBox(self.gbPos)
        self.cbEsPosWin.setObjectName(u"cbEsPosWin")

        self.verticalLayout_10.addWidget(self.cbEsPosWin)

        self.cbEsVelWin = QCheckBox(self.gbPos)
        self.cbEsVelWin.setObjectName(u"cbEsVelWin")

        self.verticalLayout_10.addWidget(self.cbEsVelWin)

        self.cbEsEndlage = QCheckBox(self.gbPos)
        self.cbEsEndlage.setObjectName(u"cbEsEndlage")
        self.cbEsEndlage.setCheckable(True)
        self.cbEsEndlage.setChecked(False)

        self.verticalLayout_10.addWidget(self.cbEsEndlage)


        self.horizontalLayout_34.addWidget(self.gbPos)


        self.horizontalLayout_32.addWidget(self.groupBox_40)

        self.gbGs = QGroupBox(self.gbEStop)
        self.gbGs.setObjectName(u"gbGs")
        self.horizontalLayout_35 = QHBoxLayout(self.gbGs)
        self.horizontalLayout_35.setSpacing(0)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.gbG1 = QGroupBox(self.gbGs)
        self.gbG1.setObjectName(u"gbG1")
        self.gbG1.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.verticalLayout_13 = QVBoxLayout(self.gbG1)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.cbEsG1COM = QCheckBox(self.gbG1)
        self.cbEsG1COM.setObjectName(u"cbEsG1COM")

        self.verticalLayout_13.addWidget(self.cbEsG1COM)

        self.cbEsG1OUT = QCheckBox(self.gbG1)
        self.cbEsG1OUT.setObjectName(u"cbEsG1OUT")

        self.verticalLayout_13.addWidget(self.cbEsG1OUT)

        self.cbEsG1FB = QCheckBox(self.gbG1)
        self.cbEsG1FB.setObjectName(u"cbEsG1FB")

        self.verticalLayout_13.addWidget(self.cbEsG1FB)


        self.horizontalLayout_35.addWidget(self.gbG1)

        self.gbG2 = QGroupBox(self.gbGs)
        self.gbG2.setObjectName(u"gbG2")
        self.gbG2.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.verticalLayout_12 = QVBoxLayout(self.gbG2)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.cbEsG2COM = QCheckBox(self.gbG2)
        self.cbEsG2COM.setObjectName(u"cbEsG2COM")

        self.verticalLayout_12.addWidget(self.cbEsG2COM)

        self.cbEsG2OUT = QCheckBox(self.gbG2)
        self.cbEsG2OUT.setObjectName(u"cbEsG2OUT")

        self.verticalLayout_12.addWidget(self.cbEsG2OUT)

        self.cbEsG2FB = QCheckBox(self.gbG2)
        self.cbEsG2FB.setObjectName(u"cbEsG2FB")

        self.verticalLayout_12.addWidget(self.cbEsG2FB)


        self.horizontalLayout_35.addWidget(self.gbG2)

        self.gbG3 = QGroupBox(self.gbGs)
        self.gbG3.setObjectName(u"gbG3")
        self.gbG3.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"    margin-top: 0px;\n"
"}\n"
"")
        self.verticalLayout_11 = QVBoxLayout(self.gbG3)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.cbEsG3COM = QCheckBox(self.gbG3)
        self.cbEsG3COM.setObjectName(u"cbEsG3COM")
        self.cbEsG3COM.setEnabled(True)
        self.cbEsG3COM.setCheckable(True)
        self.cbEsG3COM.setChecked(False)

        self.verticalLayout_11.addWidget(self.cbEsG3COM)

        self.cbEsG3OUT = QCheckBox(self.gbG3)
        self.cbEsG3OUT.setObjectName(u"cbEsG3OUT")

        self.verticalLayout_11.addWidget(self.cbEsG3OUT)

        self.cbEsG3FB = QCheckBox(self.gbG3)
        self.cbEsG3FB.setObjectName(u"cbEsG3FB")

        self.verticalLayout_11.addWidget(self.cbEsG3FB)


        self.horizontalLayout_35.addWidget(self.gbG3)


        self.horizontalLayout_32.addWidget(self.gbGs)


        self.mainLayout.addWidget(self.gbEStop)


        self.retranslateUi(StatusForm)

        QMetaObject.connectSlotsByName(StatusForm)
    # setupUi

    def retranslateUi(self, StatusForm):
        StatusForm.setWindowTitle(QCoreApplication.translate("StatusForm", u"Status Panel", None))
        self.gbEngine.setTitle(QCoreApplication.translate("StatusForm", u"Engine", None))
        self.cmbAxisName.setItemText(0, "")
        self.cmbAxisName.setItemText(1, QCoreApplication.translate("StatusForm", u"Anton", None))
        self.cmbAxisName.setItemText(2, QCoreApplication.translate("StatusForm", u"Burt", None))
        self.cmbAxisName.setItemText(3, QCoreApplication.translate("StatusForm", u"Cecil", None))
        self.cmbAxisName.setItemText(4, QCoreApplication.translate("StatusForm", u"Debby", None))
        self.cmbAxisName.setItemText(5, QCoreApplication.translate("StatusForm", u"SIMUL", None))

        self.cmbAxisName.setCurrentText("")
        self.txtPosIst.setText(QCoreApplication.translate("StatusForm", u"0 m", None))
        self.txtSpeedIstUI.setText(QCoreApplication.translate("StatusForm", u"0 m/s", None))
        self.txtActCurUI.setText(QCoreApplication.translate("StatusForm", u"0 A", None))
        self.txtStatus.setText(QCoreApplication.translate("StatusForm", u"F 999/99", None))
        self.btnAxisReset.setText(QCoreApplication.translate("StatusForm", u"Reset", None))
        self.txtCabTemperature.setText(QCoreApplication.translate("StatusForm", u"0\u00b0C", None))
        self.txtTimeTick.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox.setTitle("")
        self.txtSelected1.setText(QCoreApplication.translate("StatusForm", u"Selected", None))
        self.cbFBT.setText(QCoreApplication.translate("StatusForm", u"FBT", None))
        self.cbReady.setText(QCoreApplication.translate("StatusForm", u"Ready", None))
        self.cbOnline.setText(QCoreApplication.translate("StatusForm", u"Online", None))
        self.cbBrake1.setText(QCoreApplication.translate("StatusForm", u"Brake 1", None))
        self.cbBrake2.setText(QCoreApplication.translate("StatusForm", u"Brake 2", None))
        self.txtSelected2.setText(QCoreApplication.translate("StatusForm", u"Selected", None))
        self.groupBox_2.setTitle("")
        self.gbPositions.setTitle(QCoreApplication.translate("StatusForm", u"Positions", None))
        self.groupBox_3.setTitle("")
        self.btnPosEdit.setText(QCoreApplication.translate("StatusForm", u"Edit", None))
        self.groupBox_18.setTitle("")
        self.label_9.setText(QCoreApplication.translate("StatusForm", u"Hard Max", None))
        self.txtHardMax.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_17.setTitle("")
        self.label_8.setText(QCoreApplication.translate("StatusForm", u"User Max", None))
        self.txtUserMax.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_16.setTitle("")
        self.label_7.setText(QCoreApplication.translate("StatusForm", u"Offset", None))
        self.txtPosOffset.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_15.setTitle("")
        self.label_6.setText(QCoreApplication.translate("StatusForm", u"User Min", None))
        self.txtUserMin.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_10.setTitle("")
        self.label.setText(QCoreApplication.translate("StatusForm", u"Hard Min", None))
        self.txtHardMin.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_14.setTitle("")
        self.label_5.setText(QCoreApplication.translate("StatusForm", u"Pos Win", None))
        self.txtPosWin.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_19.setTitle("")
        self.btnPosWrite.setText(QCoreApplication.translate("StatusForm", u"Write", None))
        self.btnPosCancel.setText(QCoreApplication.translate("StatusForm", u"Cancel", None))
        self.gbVel.setTitle(QCoreApplication.translate("StatusForm", u"Vel/Acc/Amp", None))
        self.groupBox_4.setTitle("")
        self.btnVelEdit.setText(QCoreApplication.translate("StatusForm", u"Edit", None))
        self.groupBox_25.setTitle("")
        self.label_15.setText(QCoreApplication.translate("StatusForm", u"VelMaxMot", None))
        self.txtVelMaxMot.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_24.setTitle("")
        self.label_14.setText(QCoreApplication.translate("StatusForm", u"Vel Max", None))
        self.txtVelMax.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_23.setTitle("")
        self.label_13.setText(QCoreApplication.translate("StatusForm", u"Acc Max", None))
        self.txtAccMax.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_26.setTitle("")
        self.label_16.setText(QCoreApplication.translate("StatusForm", u"Dcc Max", None))
        self.txtDccMax.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_22.setTitle("")
        self.label_12.setText(QCoreApplication.translate("StatusForm", u"Acc Move", None))
        self.txtAccMove.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_20.setTitle("")
        self.label_10.setText(QCoreApplication.translate("StatusForm", u"Max Amp", None))
        self.txtMaxAmp.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_21.setTitle("")
        self.label_11.setText(QCoreApplication.translate("StatusForm", u"Vel Win", None))
        self.txtVelWin.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_27.setTitle("")
        self.btnVelWrite.setText(QCoreApplication.translate("StatusForm", u"Write", None))
        self.btnVelCancel.setText(QCoreApplication.translate("StatusForm", u"Cancel", None))
        self.gbGuider.setTitle(QCoreApplication.translate("StatusForm", u"Guider", None))
        self.groupBox_54.setTitle("")
        self.txtGuidePosIstUI.setText(QCoreApplication.translate("StatusForm", u"9.99", None))
        self.btnGuideEngaged.setText(QCoreApplication.translate("StatusForm", u"engaged", None))
        self.txtGuideIstSpeedUI.setText(QCoreApplication.translate("StatusForm", u"999", None))
        self.groupBox_53.setTitle("")
        self.txtGuideStatus.setText(QCoreApplication.translate("StatusForm", u"F 999/99", None))
        self.btnGuideReset.setText(QCoreApplication.translate("StatusForm", u"Reset", None))
        self.groupBox_50.setTitle("")
        self.cbGuideReady.setText(QCoreApplication.translate("StatusForm", u"Ready", None))
        self.cbGuideOnline.setText(QCoreApplication.translate("StatusForm", u"Online", None))
        self.groupBox_51.setTitle("")
        self.groupBox_52.setTitle("")
        self.groupBox_7.setTitle("")
        self.btnGuideEdit.setText(QCoreApplication.translate("StatusForm", u"Edit", None))
        self.groupBox_55.setTitle("")
        self.label_28.setText(QCoreApplication.translate("StatusForm", u"Pitch", None))
        self.txtGuidePitch.setText(QCoreApplication.translate("StatusForm", u"6.3", None))
        self.btnGuideWrite.setText(QCoreApplication.translate("StatusForm", u"Write", None))
        self.groupBox_57.setTitle("")
        self.label_29.setText(QCoreApplication.translate("StatusForm", u"Pos Max", None))
        self.txtGuidePosMax.setText(QCoreApplication.translate("StatusForm", u"1.25", None))
        self.txtGuidePosMaxMax.setText(QCoreApplication.translate("StatusForm", u"1.00", None))
        self.groupBox_56.setTitle("")
        self.label_30.setText(QCoreApplication.translate("StatusForm", u"Pos MIn", None))
        self.txtGuidePosMin.setText(QCoreApplication.translate("StatusForm", u"0.00", None))
        self.btnGuideCancel.setText(QCoreApplication.translate("StatusForm", u"Cancel", None))
        self.gbFilter.setTitle(QCoreApplication.translate("StatusForm", u"Filter", None))
        self.groupBox_5.setTitle("")
        self.btnFilterEdit.setText(QCoreApplication.translate("StatusForm", u"Edit", None))
        self.groupBox_12.setTitle("")
        self.label_3.setText(QCoreApplication.translate("StatusForm", u"Lag Error", None))
        self.txtLagError.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_28.setTitle("")
        self.label_17.setText(QCoreApplication.translate("StatusForm", u"Prop", None))
        self.txtFilterP.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_30.setTitle("")
        self.label_19.setText(QCoreApplication.translate("StatusForm", u"Integral", None))
        self.txtFilterI.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_29.setTitle("")
        self.label_18.setText(QCoreApplication.translate("StatusForm", u"Derivate", None))
        self.txtFilterD.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_32.setTitle("")
        self.label_21.setText(QCoreApplication.translate("StatusForm", u"Int.Lim.", None))
        self.txtFilterIL.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_31.setTitle("")
        self.label_20.setText(QCoreApplication.translate("StatusForm", u"Rampform", None))
        self.txtRampform.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_33.setTitle("")
        self.btnFilterWrite.setText(QCoreApplication.translate("StatusForm", u"Write", None))
        self.btnFilterCancel.setText(QCoreApplication.translate("StatusForm", u"Cancel", None))
        self.gbRope.setTitle(QCoreApplication.translate("StatusForm", u"Rope", None))
        self.groupBox_6.setTitle("")
        self.btnRopeEdit.setText(QCoreApplication.translate("StatusForm", u"Info Only", None))
        self.groupBox_13.setTitle("")
        self.label_4.setText(QCoreApplication.translate("StatusForm", u"SWLL", None))
        self.txtRopeSWLL.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_36.setTitle("")
        self.label_23.setText(QCoreApplication.translate("StatusForm", u"Diameter", None))
        self.txtRopeDiameter.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_35.setTitle("")
        self.label_22.setText(QCoreApplication.translate("StatusForm", u"Type", None))
        self.txtRopeType.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_37.setTitle("")
        self.label_24.setText(QCoreApplication.translate("StatusForm", u"Number", None))
        self.txtRopeNumber.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_38.setTitle("")
        self.label_25.setText(QCoreApplication.translate("StatusForm", u"Length", None))
        self.txtRopeLength.setText(QCoreApplication.translate("StatusForm", u"0", None))
        self.groupBox_34.setTitle("")
        self.btnRopeWrite.setText(QCoreApplication.translate("StatusForm", u"Write", None))
        self.btnRopeCancel.setText(QCoreApplication.translate("StatusForm", u"Cancel", None))
        self.gbRecover.setTitle(QCoreApplication.translate("StatusForm", u"Recover", None))
        self.label_2.setText(QCoreApplication.translate("StatusForm", u"Cut Pos", None))
        self.txtEStopCutPos.setText(QCoreApplication.translate("StatusForm", u"0 m", None))
        self.label_26.setText(QCoreApplication.translate("StatusForm", u"Cut Vel", None))
        self.txtEStopCutVel.setText(QCoreApplication.translate("StatusForm", u"0 m/s", None))
        self.txtEStopCutTime.setText(QCoreApplication.translate("StatusForm", u"06-06-2025 16:01:00 123 ms", None))
        self.label_27.setText(QCoreApplication.translate("StatusForm", u"Pos Dif", None))
        self.txtEStopPosDiff.setText(QCoreApplication.translate("StatusForm", u"0 m", None))
        self.btnRecover.setText(QCoreApplication.translate("StatusForm", u"Recover", None))
        self.btnResync.setText(QCoreApplication.translate("StatusForm", u"ReSync", None))
        self.gbEStop.setTitle("")
        self.groupBox_11.setTitle("")
        self.cbEsMaster.setText(QCoreApplication.translate("StatusForm", u"Master", None))
        self.cbEsGuider.setText(QCoreApplication.translate("StatusForm", u"Guider", None))
        self.cbEsNetwork.setText(QCoreApplication.translate("StatusForm", u"Network", None))
        self.btnEsReset.setText(QCoreApplication.translate("StatusForm", u"Reset", None))
        self.groupBox_39.setTitle("")
        self.groupBox_42.setTitle("")
        self.cbEsEStop1.setText(QCoreApplication.translate("StatusForm", u"E-Stop 1", None))
        self.cbEsEStop2.setText(QCoreApplication.translate("StatusForm", u"E-Stop 2", None))
        self.groupBox_44.setTitle("")
        self.cbEs30kW.setText(QCoreApplication.translate("StatusForm", u"30kW OK", None))
        self.cbEs05kW.setText(QCoreApplication.translate("StatusForm", u"0.5kW OK", None))
        self.groupBox_43.setTitle("")
        self.cbEsBRK1OK.setText(QCoreApplication.translate("StatusForm", u"BRK 1 OK", None))
        self.cbEsBRK2OK.setText(QCoreApplication.translate("StatusForm", u"BRK 2 OK", None))
        self.cbEsBRK2KB.setText(QCoreApplication.translate("StatusForm", u"BRK 2 KB", None))
        self.groupBox_40.setTitle("")
        self.gbSps.setTitle("")
        self.cbEsSPS.setText(QCoreApplication.translate("StatusForm", u"SPS OK", None))
        self.cbEsRED.setText(QCoreApplication.translate("StatusForm", u"RED OK", None))
        self.cbEsENC.setText(QCoreApplication.translate("StatusForm", u"ENC OK", None))
        self.gbPos.setTitle("")
        self.cbEsPosWin.setText(QCoreApplication.translate("StatusForm", u"PosWin", None))
        self.cbEsVelWin.setText(QCoreApplication.translate("StatusForm", u"VelWin", None))
        self.cbEsEndlage.setText(QCoreApplication.translate("StatusForm", u"Endlage", None))
        self.gbGs.setTitle("")
        self.gbG1.setTitle("")
        self.cbEsG1COM.setText(QCoreApplication.translate("StatusForm", u"G1 COM", None))
        self.cbEsG1OUT.setText(QCoreApplication.translate("StatusForm", u"G1 OUT", None))
        self.cbEsG1FB.setText(QCoreApplication.translate("StatusForm", u"G1 FB", None))
        self.gbG2.setTitle("")
        self.cbEsG2COM.setText(QCoreApplication.translate("StatusForm", u"G2 COM", None))
        self.cbEsG2OUT.setText(QCoreApplication.translate("StatusForm", u"G2 OUT", None))
        self.cbEsG2FB.setText(QCoreApplication.translate("StatusForm", u"G2 FB", None))
        self.gbG3.setTitle("")
        self.cbEsG3COM.setText(QCoreApplication.translate("StatusForm", u"G3 COM", None))
        self.cbEsG3OUT.setText(QCoreApplication.translate("StatusForm", u"G3 OUT", None))
        self.cbEsG3FB.setText(QCoreApplication.translate("StatusForm", u"G3 FB", None))
    # retranslateUi

