# sim_codec.py
from WWWinch_codec import Codec
import math, time

class SimCodec(Codec):
    def __init__(self):
        super().__init__()
        self.receivedBuff = None
        self.timeOld = None


    def simulate(self, IntervallR):
        fa = "%3.2f"
        self.ControlingPIDRx = "1234"
        self.LTold = 1
        self.Status = "SIMUL"
        self.GuideStatus = "SIMUL"
        self.Enable = 0
        ''''
        # --- Ensure simulated EStop is ready ---
        try:
            if hasattr(self, 'EStop') and hasattr(self.EStop, 'EsReady'):
                self.EStop.EsReady = True
        except AttributeError:
            print("EStop attribute not found, skipping EsReady assignment.")    

        # --- Persist InitAchse if set externally (e.g. by controller) ---
        if hasattr(self, 'ActProp') and hasattr(self.ActProp, 'InitAchse'):
            if getattr(self.ActProp, 'InitAchse', 0) == 1:
                if not hasattr(self, '_persisted_initachse'):
                    self._persisted_initachse = 1
            elif hasattr(self, '_persisted_initachse'):
                # Only clear if explicitly set to 0 externally
                if getattr(self.ActProp, 'InitAchse', 0) == 0:
                    self._persisted_initachse = 0
        # Always use persisted value if present
        if hasattr(self, '_persisted_initachse'):
            self.ActProp.InitAchse = self._persisted_initachse

    '''
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

        
        self.GuidePitch = "-6.3"
        self.GuidePosMax = "0.97"
        self.GuidePosMaxMax = "0.97"
        self.GuidePosMin = "0.01"

        self.EStopStatus = 2048
        self.EsNetwork = True
        self.EsTaster = True
        self.EStopTime = 0
        self.EStopCutPos = 0
        self.EStopCutVel = 0
        self.EsEStop2 = False

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


        # Set all cbEs... bits to True for simulation
        #for attr in dir(self.EStop):
        #    if attr.startswith('Es') and isinstance(getattr(self.EStop, attr), bool):
        #        setattr(self.EStop, attr, True)

    def step_sim(self):
        time_now = time.perf_counter()
        if self.timeOld is None:
            self.timeOld = time_now
        IntervallR = time_now - self.timeOld
        self.timeOld = time_now
        self.simulate(IntervallR)
        self.receivedBuff = self.pack(self.__dict__)
        return self.receivedBuff

    #def unpack(self, data):
        # Always persist SetProp.Name across cycles
        #super().unpack(data)
        #if hasattr(self, 'SetProp') and hasattr(self.SetProp, 'Name'):
         #   if self.SetProp.Name:
        #        self._last_axis_name = self.SetProp.Name
        #    elif self._last_axis_name:
        #        self.SetProp.Name = self._last_axis_name
        #print(f"[SimCodec] unpack: SetProp.Name={getattr(self.SetProp, 'Name', None)} _last_axis_name={getattr(self, '_last_axis_name', None)}")
        #return data
