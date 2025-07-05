# sim_codec.py
from WWWinch_codec import Codec
import math, time

class SimCodec(Codec):
    def __init__(self):
        super().__init__()
        self.receivedBuff = None
        self.timeOld = None

        self.SetProp.Name = "SIMUL"
        self.SetProp.GearToUI = float("13.0") 
        self.SetProp.HardMax = float("299")
        self.SetProp.UserMax = float("298")
        self.SetProp.PosOffset = float("0.0")
        self.SetProp.UserMin = float("-298")
        self.SetProp.HardMin = float("-299")
        self.SetProp.PosWin = float("0.01")
        self.SetProp.VelMaxMot = float("10.5")
        self.SetProp.VelMax = float("10.5")
        self.SetProp.AccMax = float("5.5")
        self.SetProp.DccMax = float("5.4")
        self.SetProp.AccMove = float("5.5")
        self.SetProp.MaxAmp = float("150")
        self.SetProp.VelWin = float("0.01")
        self.SetProp.FilterP = float("1.0")
        self.SetProp.FilterI = float("1.0")
        self.SetProp.FilterD = float("1.0")
        self.SetProp.FilterIL = float("1.0")
        self.SetProp.RopeSWLL = float("2500.0")
        self.SetProp.RopeDiameter = float("5.0")
        self.SetProp.RopeType = "SIMUL"
        self.SetProp.RopeNumber = "SIMUL"
        self.SetProp.RopeLength = float("200")
        self.SetProp.SpeedMaxForUI = float("16.25")
        self.SetProp.PosDiffForUI = "SIMUL"
        self.SetProp.AccTot = float("5.00")
        self.SetProp.Rampform = "SIMUL"

        self.PosIst = float("0.0")  # Current position
        self.SpeedIstUI = float("0.0")  # Current speed for UI display 
        self.SpeedSoll = float("0.0" ) # Desired speed
        self.PosUserMax = float("298.0")  # User-defined maximum position
        self.PosUserMin = float("-298.0")  # User-defined minimum position
        self.DccMax = float("5.4")  # Maximum deceleration
        self.AccMax = float("5.5")  # Maximum acceleration
        self.SpeedMax = float("10.5")  # Maximum speed



    def simulate(self, IntervallR):
        fa = "%3.2f"
        self.ControlingPIDRx = "1234"

        time_now = time.perf_counter()
        if self.timeOld is not None:
                dt = (time_now - self.timeOld) * 1000.0  # Convert to milliseconds
        else:
            dt = 0.0
        self.timeOld = time_now

        # Automatically clear/reset EsMaster based on reset flag
        if self.ActProp.EStopReset:
            # Simulate successful reset: all safety inputs become healthy
            for attr in dir(self.EStop):
                if attr.startswith("Es") and isinstance(getattr(self.EStop, attr), bool):
                    setattr(self.EStop, attr, True)

            self.EStop.EsReady = True  # explicitly ensure readiness
            self.EStop.EsMaster = True
            self.EStop.GUINotHalt = False
            self.ActProp.EStopStatus = 2048  # Reset status to indicate no emergency

        else:
            # Simulate emergency state
            for attr in dir(self.EStop):
                if attr.startswith("Es") and isinstance(getattr(self.EStop, attr), bool):
                    setattr(self.EStop, attr, False)

            self.EStop.EsReady = False
            self.EStop.EsMaster = False
            self.EStop.EsNetwork = False  # backend still reachable
            self.EStop.GUINotHalt = True
            self.ActProp.EStopStatus = 4096  # Set status to indicate emergency

        estop_triggered = any(bool(getattr(self.EStop, attr)) for attr in dir(self.EStop) if attr.startswith("Es"))


        if self.ActProp.Enable and not estop_triggered:
            # Fetch limits from SetProp
            pos_max = float(self.SetProp.UserMax)
            pos_min = float(self.SetProp.UserMin)
            acc_max = float(self.ActProp.AccMax)
            dcc_max = float(self.SetProp.DccMax)
            speed_max = float(self.SetProp.VelMax)

            # Fetch current values from ActProp
            pos = float(self.ActProp.PosIst)
            speed_ist = float(self.ActProp.SpeedIstUI)
            speed_soll = float(self.ActProp.SpeedSoll)

            # Clamp desired speed to within velocity limits
            speed_soll = max(min(speed_soll, speed_max), -speed_max)

            # Enforce positional stopping zones near the limits
            if speed_soll > 0:
                dist_to_max = pos_max - pos
                if dist_to_max <= 0:
                    speed_soll = 0.0
                else:
                    stop_speed = math.sqrt(dcc_max * dist_to_max)
                    speed_soll = min(speed_soll, stop_speed)
            elif speed_soll < 0:
                dist_to_min = pos - pos_min
                if dist_to_min <= 0:
                    speed_soll = 0.0
                else:
                    stop_speed = math.sqrt(dcc_max * dist_to_min)
                    speed_soll = max(speed_soll, -stop_speed)

            # Integrate acceleration
            if speed_soll > speed_ist:
                speed_ist += acc_max * IntervallR
                speed_ist = min(speed_ist, speed_soll)
            elif speed_soll < speed_ist:
                speed_ist -= dcc_max * IntervallR
                speed_ist = max(speed_ist, speed_soll)

            # Integrate position
            pos += speed_ist * IntervallR

            # Write back to ActProp
            self.ActProp.PosIst = pos
            self.ActProp.SpeedIstUI = speed_ist

            #print(f"[SimCodec] Simulated PosIst={pos:.2f}, SpeedIstUI={speed_ist:.2f}, SpeedSoll={speed_soll:.2f}")

        else:
            self.ActProp.SpeedIstUI = 0.0
        
        # Update ActProp with simulated values

        self.ActProp.LTOld               = dt                         # from 1
        self.ActProp.OwnPID                = 0
        self.ActProp.ControlingPIDTx       = 0                        # from 0
        self.ActProp.ControlingPIDRx       = 1234                     # Simulated PID Tx value

        self.ActProp.LagError            = 12 #           
        self.ActProp.MasterMomentUI      = 250.0                        # from 6
        self.ActProp.MotAuslastUI        = 1230.0                        # legacy
        self.ActProp.ActCurUI            = 2340.0                        # from 32
        self.ActProp.CabTemperature      = 22.2

        self.ActProp.EStopStatus          = 0                         # from 37
        self.ActProp.EStopCutTime        = 0.0                        # from 39
        self.ActProp.EStopCutPos         = 0.0                        # from 40
        self.ActProp.EStopCutVel         = 0.0                        # from 41
        self.ActProp.EStopPosDiff        = 0.0               
        #self.ActProp.EStopReset       : bool    = False              # from UI
        #self.ActProp.InitAchse        : int     = 0                  # from UI    

        self.Guide.Control             = "GuideControl"
        self.Guide.SpeedSoll           = 0.0
        self.Guide.SpeedIstUI          = 0.0 
        self.Guide.GuidePosIstUI       = 0.0                      # from 30
        self.Guide.GuidePitch          = -6.3                     # from 27
        self.Guide.GuidePosMax         = 0.9                      # from 28
        self.Guide.GuidePosMaxMax      = 0.9                      # from 45
        self.Guide.GuidePosMin         = 0.0                      # from 29
        
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

