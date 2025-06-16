# sim_codec.py
from WWWinch_codec import Codec
import math, time

class SimCodec(Codec):
    def __init__(self):
        super().__init__()
        self.receivedBuff = None
        self.timeOld = None

        self.SetProp.Name = "SIMUL"
        self.SetProp.GearToUI = "13.0" 
        self.SetProp.HardMax = "299"
        self.SetProp.UserMax = "298"
        self.SetProp.PosOffset = "0.0"
        self.SetProp.UserMin = "-298"
        self.SetProp.HardMin = "-299"
        self.SetProp.PosWin = "0.01"
        self.SetProp.VelMaxMot = "10.5"
        self.SetProp.VelMax = "10.5"
        self.SetProp.AccMax = "5.5"
        self.SetProp.DccMax = "5.4"
        self.SetProp.AccMove = "5.5"
        self.SetProp.MaxAmp = "150"
        self.SetProp.VelWin = "0.01"
        self.SetProp.FilterP = "1.0"
        self.SetProp.FilterI = "1.0"
        self.SetProp.FilterD = "1.0"
        self.SetProp.FilterIL = "1.0"
        self.SetProp.RopeSWLL = "2500.0"
        self.SetProp.RopeDiameter = "5.0"
        self.SetProp.RopeType = "SIMUL"
        self.SetProp.RopeNumber = "SIMUL"
        self.SetProp.RopeLength = "200"
        self.SetProp.SpeedMaxForUI = "16.25"
        self.SetProp.PosDiffForUI = "SIMUL"
        self.SetProp.AccTot = "5.00"
        self.SetProp.Rampform = "SIMUL"

        self.GuidePitch = "-6.3"
        self.GuidePosMax = "0.97"
        self.GuidePosMaxMax = "0.97"
        self.GuidePosMin = "0.01"


    def simulate(self, IntervallR):
        fa = "%3.2f"
        self.ControlingPIDRx = "1234"

        time_now = time.perf_counter()
        if self.timeOld is not None:
                dt = (time_now - self.timeOld) * 1000.0  # Convert to milliseconds
        else:
            dt = 0.0
        self.timeOld = time_now
        self.ActProp.LTOld = dt

        # Automatically clear/reset EsMaster based on reset flag
        if self.ActProp.EStopReset:
            # Simulate successful reset: all safety inputs become healthy
            for attr in dir(self.EStop):
                if attr.startswith("Es") and isinstance(getattr(self.EStop, attr), bool):
                    setattr(self.EStop, attr, True)

            self.EStop.EsReady = True  # explicitly ensure readiness
            self.EStop.EsMaster = True
            self.EStop.GUINotHalt = False

        else:
            # Simulate emergency state
            for attr in dir(self.EStop):
                if attr.startswith("Es") and isinstance(getattr(self.EStop, attr), bool):
                    setattr(self.EStop, attr, False)

            self.EStop.EsReady = False
            self.EStop.EsMaster = False
            self.EStop.EsNetwork = True  # backend still reachable
            self.EStop.GUINotHalt = True

        self.Status = "SIMUL"
        self.GuideStatus = "SIMUL"
        self.Enable = 0

        if self.Enable == 1:
            SpeedIstIntern = float(self.SpeedIstUI)
            SpeedSollIntern = max(min(float(self.SpeedSoll), float(self.SpeedMax)), -float(self.SpeedMax))

            PosDiffG = float(self.PosUserMax) - float(self.PosIst)
            if PosDiffG > 0:
                SpeedMaxG = math.sqrt(float(self.DccMax) * PosDiffG)
                SpeedSollIntern = min(SpeedSollIntern, SpeedMaxG)
            elif SpeedSollIntern > 0:
                SpeedSollIntern = 0.0

            PosDiffG = float(self.PosIst) - float(self.PosUserMin)
            if PosDiffG > 0:
                SpeedMaxG = math.sqrt(float(self.DccMax) * PosDiffG)
                SpeedSollIntern = max(SpeedSollIntern, -SpeedMaxG)
            elif SpeedSollIntern < 0:
                SpeedSollIntern = 0.0

            if SpeedSollIntern > SpeedIstIntern:
                SpeedIstIntern += float(self.AccMax) * IntervallR
                SpeedIstIntern = min(SpeedIstIntern, SpeedSollIntern)
            elif SpeedSollIntern < SpeedIstIntern:
                SpeedIstIntern -= float(self.DccMax) * IntervallR
                SpeedIstIntern = max(SpeedIstIntern, SpeedSollIntern)

            self.PosIst = str(float(self.PosIst) + SpeedIstIntern * IntervallR)
            self.SpeedIstUI = str(SpeedIstIntern)
        else:
            self.SpeedIstUI = "0.0"

        self.MasterMomentUI = "0.0"
        self.CabTemperature = "22.2"
        self.GuidePosIstUI = "0.0"
        self.GuideIstSpeedUI = "0.0"

        self.EStopStatus = 2048
        self.EsNetwork = True
        self.EsTaster = True
        self.EStopTime = 0
        self.EStopCutPos = 0
        self.EStopCutVel = 0
        self.EsEStop2 = False

    def step_sim(self):
        """
        Simulate one backend cycle. Responds to GUI commands via ActProp.Modus.
        """

        time_now = time.perf_counter()
        if self.timeOld is None:
            self.timeOld = time_now
        IntervallR = time_now - self.timeOld
        self.timeOld = time_now
        self.simulate(IntervallR)

        mode = getattr(self.ActProp, "Modus", "r").lower()

        if mode == "w":
            self.apply_config_from_setprop()

        self.sperre = False if mode == "e" else True

        # Construct reply using updated ActProp
        self.receivedBuff = self.pack(self.to_dict({}))
        return self.receivedBuff
    
    def apply_config_from_setprop(self):
        """
        Apply SetProp to ActProp, and Guide.SetProp to Guide.ActProp,
        while respecting legacy field structure and avoiding overwrite
        of simulation-controlled fields like AccMax and DccMax.
        """
        pass


    def unpack(self, props: dict):
        """
        Load incoming values (e.g. from shared memory) into internal state.
        """
        if not props:
            return

        for key in ['SetProp', 'ActProp', 'EStop']:
            if key in props:
                source = props[key]
                target = getattr(self, key, None)
                if target:
                    for k, v in source.items():
                        if hasattr(target, k):
                            setattr(target, k, v)

        # Handle nested Guide separately
        if "Guide" in props:
            guide_props = props["Guide"]
            for subkey in ["SetProp", "ActProp"]:
                if subkey in guide_props:
                    source = guide_props[subkey]
                    target = getattr(self.Guide, subkey, None)
                    if target:
                        for k, v in source.items():
                            if hasattr(target, k):
                                setattr(target, k, v)

    def to_dict(self, data=None):
        """
        Convert internal codec state into a dictionary for shared memory push.
        Mirrors the structure used in Controller <-> Backend communication.
        """
        def obj_to_dict(obj):
            return {k: getattr(obj, k) for k in dir(obj)
                    if not k.startswith("_") and not callable(getattr(obj, k))}

        return {
            "ActProp": obj_to_dict(self.ActProp),
            "SetProp": obj_to_dict(self.SetProp),
            "EStop":   obj_to_dict(self.EStop),
            "Guide": {
                "ActProp": obj_to_dict(self.Guide.ActProp),
                "SetProp": obj_to_dict(self.Guide.SetProp),
            }
        }

