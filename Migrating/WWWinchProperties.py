from dataclasses import dataclass, field

class WWWinchProperties:
    """
    This class holds the properties of a wiredworks Winch.
    It is used to store the properties of the wiredworks Winch in a structured way.
    """
    def __init__(self):
        self.Axis = AxisProp()
@dataclass
class GuidActProp:
    GuidePosIstUI    : float = 0.0               # from 30
    GuideIstSpeedUI  : float = 0.0               # from 31
    GuideSpeedSoll   : float = 0.0               # from UI
    GuideStatus      : str   = "GuideStatus"     # from 3

@dataclass
class GuideSetProp:
    Control          : str     = "GuideControl"
    SpeedSoll        : float   = 0.0
    GuidePitch       : float   = -6.3            # from 27
    GuidePosMax      : float   = 0.9             # from 28
    GuidePosMaxMax   : float   = 0.9             # from 45
    GuidePosMin      : float   = 0.0             # from 29

@dataclass
class GuideProp:
    ActProp          : GuidActProp = field(default_factory=GuidActProp)
    SetProp          : GuideSetProp = field(default_factory=GuideSetProp)

@dataclass
class AxisActProp:
    LTOld            : float   = 0                # from 1
    Status           : str     = "Status"         # from 2
    Modus            : str     = "Modus"
    OwnPID           : int     = 0
    ControlingPIDTx  : int     = 0                # from 0
    ControlingPIDRx  : int     = 0
    Intent           : str     = "False"
    Enable           : bool    = False   
    PosIst           : float   = 0.0              # from 4
    SpeedIstUI       : float   = 0.0              # from 5
    MasterMomentUI   : float   = 0.0              # from 6
    MotAuslastUI     : float   = 0.0              # legacy
    ActCurUI         : float   = 0.0              # from 32
    CabTemperature   : float   = 0.0              # from 7
    PosSoll          : float   = 0.0              # from UI
    SpeedSoll        : float   = 0.0              # from UI
    AccMax           : float   = 0.0              # from UI modified
    DccMax           : float   = 0.0              # from UI modified
    ReSync           : bool    = False            # from UI
    EStopStatus      : int     = 0                # from 37
    EStopCutTime     : float   = 0.0              # from 39
    EStopCutPos      : float   = 0.0              # from 40
    EStopCutVel      : float   = 0.0              # from 41
    EStopReset       : bool    = False            # from UI
    InitAchse        : int     = 1                # from UI       

@dataclass
class AxisSetProp:
    Name             : str     = "AxisName"       # from 8
    GearToUI         : float   = 1.0              # from 9
    PosHardMax       : float   = 300.0            # from 10
    PosUserMax       : float   = 300.0            # from 11
    PosUserMin       : float   = -300.0           # from 12
    PosHardMin       : float   = -300.0           # from 13
    PosWin           : float   = 0.5              # from 42
    SpeedMax         : float   = 5.0              # from 14
    AccMax           : float   = 10.0             # from 15 
    DccMax           : float   = 10.0             # from 16
    MaxAmp           : float   = 150              # from 17
    VelWin           : float   = 0.5              # from 43
    FilterP          : float   = 1.0              # from 18
    FilterI          : float   = 1.0              # from 19
    FilterD          : float   = 1.0              # from 20
    FilterIL         : float   = 1.0              # from 21
    RopeSWLL         : float   = 0.0              # from 22
    RopeDiameter     : float   = 0.0              # from 23
    RopeType         : str     = "RopeType"       # from 24
    RopeNumber       : int     = 0                # from 25
    RopeLength       : float   = 0.0              # from 26
    SpeedMaxForUI    : float   = 5.0              # from 34
    PosDiffForUI     : float   = 0.5              # from 35
    AccTot           : float   = 10.0             # from 44
    Rampform         : str     = "Rampform"       # from 36 

@dataclass
class EStopProp:
    Es30kWOK         : bool    = False
    EsG3OUT          : bool    = False
    EsG3COM          : bool    = False
    EsG3FB           : bool    = False
    EsG2OUT          : bool    = False
    EsG2COM          : bool    = False
    EsG2FB           : bool    = False
    EsG1OUT          : bool    = False
    EsG1COM          : bool    = False
    EsG1FB           : bool    = False
    EsSlave          : bool    = False
    EsNetwork        : bool    = False
    EsMaster         : bool    = False
    EsResetAble      : bool    = False
    EsEStop1         : bool    = False
    EsEstop2         : bool    = False
    EsSteuerwort     : bool    = False
    Es05kWOK         : bool    = False
    EsB1OK           : bool    = False
    EsB2OK           : bool    = False
    EsDCSOK          : bool    = False
    EsSPSOK          : bool    = False
    EsBRK2KB         : bool    = False
    EsFTBOK          : bool    = False
    EsPosWin           : bool    = False
    EsVelWin         : bool    = False
    EsEndlage        : bool    = False
    EsSchluessel1    : bool    = False
    EsSchluessel2    : bool    = False
    EsTaster         : bool    = False
    EsSchuetz        : bool    = False
    EsReady          : bool    = False
    EsOneMore        : bool    = False
    GUINotHalt       : bool    = False

@dataclass
class AxisProp:
    ActProp          : AxisActProp  = field(default_factory = AxisActProp)
    SetProp          : AxisSetProp  = field(default_factory = AxisSetProp)
    Guide            : GuideProp    = field(default_factory = GuideProp)
    EStop            : EStopProp    = field(default_factory = EStopProp)            

