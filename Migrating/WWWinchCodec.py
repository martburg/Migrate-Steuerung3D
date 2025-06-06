from WWWinchProperties import WWWinchProperties

class WWWinchCodec:
    """
    This class handles the packing and unpacking and decoding of the wiredworks Winch properties.
    It is used to convert the properties to a format suitable for transmission and vice versa.
    """
    
    def __init__(self):
        self.ActProp = WWWinchProperties.AxisProp.ActProp()
        self.SetProp = WWWinchProperties.AxisProp.SetProp()
        self.Guide   = WWWinchProperties.AxisProp.GuideProp()
        self.EStop   = WWWinchProperties.AxisProp.EStopProp()
    
    def pack(self,data):
        """
        Encodes the properties into a byte array.
        """
        # Implement packing logic here
        pass
    
    def unpack(self,data):
        """
        Decodes the byte array into properties.
        
        :param data: The byte array to decode.
        :return: A tuple containing the unpacked properties.
        """
        # Implement unpacking logic here
        pass

    def decode(self, data):
        """
        Decodes the error codes.
        
        :param data: The byte array to decode.
        """
        # Implement decoding logic here
        pass

    def simulate(self):
        """
        Simulates the Position and Velocities for testing purposes.
        """
        fa="%3.2f"
        self.ControlingPIDRx              = str(self.OwnPID)            #[0] Controling PID
        self.LTold                        = 1                                     
        self.Status                       = "SIMUL"
        self.GuideStatus                  = "SIMUL"
        
               
        if self.Enable == 1:
        #self.SpeedIstUI 
            SpeedIstIntern = float(self.SpeedIstUI)
            SpeedSollIntern = min(float(self.SpeedSoll),float(self.SpeedMax))
            SpeedSollIntern = max(float(self.SpeedSoll),-float(self.SpeedMax))

            PosDiffG = float(self.PosUserMax) - float(self.PosIst)
            if PosDiffG > 0 :
                SpeedMaxG = math.sqrt(float(self.DccMax)*PosDiffG)
                SpeedSollIntern = min(SpeedSollIntern,SpeedMaxG)
                #print " Ausserer Anschlag"
            else:
                if SpeedSollIntern > 0:
                    SpeedSollIntern = 0.0
                    #print "auserhalb Ausserer Anschlag"

            PosDiffG = float(self.PosIst) - float(self.PosUserMin)
            if PosDiffG > 0:
                SpeedMaxG = math.sqrt(float(self.DccMax)*PosDiffG);
                SpeedSollIntern = max(SpeedSollIntern,-SpeedMaxG)
                #print " Innerer Anschlag"
            else:
                if SpeedSollIntern < 0:
                    SpeedSollIntern= 0.0
                   #print "auserhalb innerenr Anschlag"

           #print "SpeedSoll "+str(fa%(float(self.SpeedSoll)))+
           #     "  Speed SollIntern "+str(fa%(float(SpeedSollIntern)))+
           #     "   SpeedIstIntern "+ str(fa%(float(SpeedIstIntern)))+
           #     "   PosIst "+fa%(float(self.PosIst))

            
            if (SpeedSollIntern > 0 and SpeedSollIntern >= SpeedIstIntern):
                SpeedIstIntern = (SpeedIstIntern+float(self.AccMax)*self.IntervallR)
                #print "werden Schneller in Plus Richtung"
                if SpeedIstIntern > SpeedSollIntern:
                    SpeedIstIntern = SpeedSollIntern
                    #print "Soll Gesch erreicht von Unten Richtung Plus"
            elif (SpeedSollIntern >= 0 and SpeedSollIntern < SpeedIstIntern):
                SpeedIstIntern = (SpeedIstIntern-float(self.DccMax)*self.IntervallR)
               #print "werden langsamer in Plus Richtung"
                if SpeedIstIntern < SpeedSollIntern:
                    SpeedIstIntern = SpeedSollIntern
                    #print "Soll Gesch erreicht von Oben Richtung Plus"
            elif (SpeedSollIntern <= 0 and SpeedSollIntern < SpeedIstIntern):
                SpeedIstIntern = (SpeedIstIntern-float(self.AccMax)*self.IntervallR)
                #print "werden Schneller in Minus Richtung"
                if SpeedIstIntern < SpeedSollIntern :
                    SpeedIstIntern = SpeedSollIntern
                    #print "Soll Gesch erreicht von Oben Richtung Minus"
            elif (SpeedSollIntern <= 0 and SpeedSollIntern >= SpeedIstIntern):
                SpeedIstIntern = (SpeedIstIntern+float(self.DccMax)*self.IntervallR)
                #print "werden Langsamer in Minus Richtung"
                if SpeedIstIntern > SpeedSollIntern:
                    SpeedIstIntern = SpeedSollIntern
                    #print "Soll Gesch erreicht von Unten Richtung Minus"

        #self.PosIst
            self.PosIst = str(float(self.PosIst)+SpeedIstIntern*self.IntervallR)
            self.SpeedIstUI = str(SpeedIstIntern)
        else:
            self.SpeedIstUI = "0.0"


        self.MasterMomentUI               = "0.0"                         #[6] AxisAmp
        self.CabTemperature               = "22.2"                        #[7] AxisTemp        
        self.GuidePosIstUI                = "0.0"                         #zu rechnen
        self.GuideIstSpeedUI              = "0.0"                         #zu rechnen
        self.SpeedMaxForUI                = "16.25"                       #[37]VelMaxMot
        self.PosDiffForUI                 = "SIMUL"                       #zu rechnen
        self.Name                         = "SIMUL"                       #[8]  Name
        self.GearToUI                     = "13.0"                        #[9]  Gear
        self.PosHardMax                   = self.PosHardMax               #[10] PosHardMax
        self.PosUserMax                   = self.PosUserMax               #[11] PosUserMax
        self.PosUserMin                   = self.PosUserMin               #[12] PosUserMin
        self.PosHardMin                   = self.PosHardMin               #[13] PosHardMin
        self.SpeedMax                     = self.SpeedMax                 #[14] VelMax
        self.AccMax                       = self.AccMax                   #[15] AccMax
        self.DccMax                       = self.DccMax                   #[16] DccMax
        self.MaxAmp                       = "150"                         #[17] AmpMax
        self.FilterP                      = "1.0"                         #[18] FilterP
        self.FilterI                      = "1.0"                         #[19] FilterI
        self.FilterD                      = "1.0"                         #[20] FilterD
        self.FilterIL                     = "1.0"                         #[21] FilterIL
        self.RopeSWLL                     = "2500.0"                      #[22] SWLL
        self.RopeDiameter                 = "5.0"                         #[23] Rope Diam    
        self.RopeType                     = "SIMUL"                       #[24] Rope Type 
        self.RopeNumber                   = "SIMUL"                       #[25] Rope Number     
        self.RopeLength                   = "200"                         #[26] Rope Length   
        self.GuidePitch                   = "-6.3"                        #[27] Pitch       
        self.GuidePosMax                  = "0.97"                        #[28] Guide Pos Max
        self.GuidePosMaxMax               = "0.97"                        #[41] Guide Pos MaxMax 
        self.GuidePosMin                  = "0.01"                        #[29] Guide Pos Min
        self.PosWin                       = "0.01"                        #[38] PosWin
        self.VelWin                       = "0.01"                        #[39] VelWin
        self.AccTot                       = "5.00"                        #[40] AccTot
        self.EStopStatus                  = 2048
        self.EsNetwork                    = True
        self.EsTaster                     = True
        self.EStopTime                    = 0
        self.EStopCutPos                  = 0
        self.EStopCutVel                  = 0
        self.EsEStop2                     = False
    pass