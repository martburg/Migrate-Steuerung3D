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
        self.SpeedMaxForUI = "16.25"
        self.PosDiffForUI = "SIMUL"
        self.Name = "SIMUL"
        self.GearToUI = "13.0"
        self.PosHardMax = "299"
        self.PosUserMax = "298"
        self.PosUserMin = "-298"
        self.PosHardMin = "-299"
        self.SpeedMax = "10.5"
        self.AccMax = "5.5"
        self.DccMax = "5.4"
        self.MaxAmp = "150"
        self.FilterP = "1.0"
        self.FilterI = "1.0"
        self.FilterD = "1.0"
        self.FilterIL = "1.0"
        self.RopeSWLL = "2500.0"
        self.RopeDiameter = "5.0"
        self.RopeType = "SIMUL"
        self.RopeNumber = "SIMUL"
        self.RopeLength = "200"
        self.GuidePitch = "-6.3"
        self.GuidePosMax = "0.97"
        self.GuidePosMaxMax = "0.97"
        self.GuidePosMin = "0.01"
        self.PosWin = "0.01"
        self.VelWin = "0.01"
        self.AccTot = "5.00"
        self.EStopStatus = 2048
        self.EsNetwork = True
        self.EsTaster = True
        self.EStopTime = 0
        self.EStopCutPos = 0
        self.EStopCutVel = 0
        self.EsEStop2 = False

    def step_sim(self):
        time_now = time.perf_counter()
        if self.timeOld is None:
            self.timeOld = time_now
        IntervallR = time_now - self.timeOld
        self.timeOld = time_now
        self.simulate(IntervallR)
        self.receivedBuff = self.pack(self.__dict__)
        return self.receivedBuff
