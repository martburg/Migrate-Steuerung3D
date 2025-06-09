class YellowAxisUI(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,(225,40), (742, 428),
                          style =wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_NO_TASKBAR)
        self.res = xrc.XmlResource("AchsSteuerungAxisSelectState1.xrc")
        ##self.res = xrc.XmlResource("AchsSteuerungRecover.xrc")        
        self.RootPanel = self.res.LoadPanel(self,'RootPanel')
        
        self.AxisSelected=False
        self.ControlingPIDRx=0
        self.Modus = 'rE' # initialisieren im read Edit Mode
        self.ClutchStatus = 1        
        self.init_Mainframe()
        self.init_MainframeEvents()
        self.DisableControls()        
        self.EStopReset =0
        self.Decode = Decode()
        self.ReSync = 0
        self.Recover = 0
        self.Modus = 0
        self.refreshSelect = "Blue"

        self.EnableOld = 0
        self.VX = 0
        self.Pos0 = 0
        self.T1Old  = time.clock()
        self.EStopMode = 'EStop'

    def init_Mainframe(self):
        self.ControlsEnabeled = False
        self.StatusPanelColour = "RedBrown"        
        '''Initialisiert die Objekte des Mainframes'''      
        self.StatusPanel        = xrc.XRCCTRL(self.RootPanel,'StatusPanel')
        self.SetupPanel         = xrc.XRCCTRL(self.RootPanel,'SetupPanel')
        self.SliderPanel        = xrc.XRCCTRL(self.RootPanel,'SliderPanel')
        self.SetupPositionPanel = xrc.XRCCTRL(self.RootPanel,'SetupPosition')
        self.SetupVelPanel      = xrc.XRCCTRL(self.RootPanel,'SetupVel')
        self.SetupGuidePanel    = xrc.XRCCTRL(self.RootPanel,'SetupGuide')
        self.SetupFilterPanel   = xrc.XRCCTRL(self.RootPanel,'SetupFilter')
        self.SetupRopePanel     = xrc.XRCCTRL(self.RootPanel,'SetupRope')
        self.EStopPanel         = xrc.XRCCTRL(self.RootPanel,'EStopPanel')
        self.BitPanel           = xrc.XRCCTRL(self.RootPanel,'BitPanel')
        self.RecoverPanel       = xrc.XRCCTRL(self.RootPanel,'RecoverPanel')

        # Kinder vom StatusPanel
        self.cmbAxisName       = xrc.XRCCTRL(self.StatusPanel,'cmbAxisName')
        self.cmbAxisName.SetEditable( False )
        self.Achsen=ACHSEN.keys()
        for a in range(len(ACHSEN.keys())):
            self.cmbAxisName.SetString(a,ACHSEN.keys()[a])
       
        self.txtAxisPos        = xrc.XRCCTRL(self.StatusPanel,'txtAxisPos')
        self.txtAxisPos.SetEditable( False )

        self.txtAxisVel        = xrc.XRCCTRL(self.StatusPanel,'txtAxisVel')
        self.txtAxisVel.SetEditable( False )

        self.txtAxisAmp        = xrc.XRCCTRL(self.StatusPanel,'txtAxisAmp')
        self.txtAxisAmp.SetEditable( False )
        self.sldAxisVel        = xrc.XRCCTRL(self.StatusPanel,'sldAxisVel')
        self.sldAxisVel.Enable(False)
        self.txtAxisError      = xrc.XRCCTRL(self.StatusPanel,'txtAxisError')
        self.txtAxisError.SetEditable( False )
        self.btnAxisReset      = xrc.XRCCTRL(self.StatusPanel,'btnAxisReset')    
        self.txtAxisTemp       = xrc.XRCCTRL(self.StatusPanel,'txtAxisTemp')
        self.txtAxisTemp.SetEditable( False )

        self.txtTimeTick       = xrc.XRCCTRL(self.StatusPanel,'txtTimeTick')
        self.txtTimeTick.SetEditable( False )
        
        self.rFBT              = xrc.XRCCTRL(self.BitPanel,'rFBT')
        self.rbReady           = xrc.XRCCTRL(self.BitPanel,'rbReady')
        self.rbPowered         = xrc.XRCCTRL(self.BitPanel,'rbPowered')
        self.rbBrake1          = xrc.XRCCTRL(self.BitPanel,'rbBrake1')
        self.rbBrake2          = xrc.XRCCTRL(self.BitPanel,'rbBrake2')
        self.txtSelected1       = xrc.XRCCTRL(self.BitPanel,'txtSelected1')
        self.txtSelected2       = xrc.XRCCTRL(self.BitPanel,'txtSelected2')

        self.txtCutPos         = xrc.XRCCTRL(self.RecoverPanel,'txtEStopCutPosition')
        self.txtCutVel         = xrc.XRCCTRL(self.RecoverPanel,'txtEStopCutVel')
        self.txtCutTime        = xrc.XRCCTRL(self.RecoverPanel,'txtEStopCutTime')
        self.txtPosDiff        = xrc.XRCCTRL(self.RecoverPanel,'txtEStopPosDiff')
        self.txtPosDiff.SetValue('0')
        self.btnRecover        = xrc.XRCCTRL(self.RecoverPanel,'btnRecover')
        self.btnReSync         = xrc.XRCCTRL(self.RecoverPanel,'btnReSync')
        
        # Kinder vom SetupPositionPanel
        self.btnAxisSetupPosEdit    = xrc.XRCCTRL(self.SetupPositionPanel,'btnAxisSetupPosEdit')
        
        self.txtAxisSetupPosHardMax = xrc.XRCCTRL(self.SetupPositionPanel,'txtAxisSetupPosHardMax')
        self.txtAxisSetupPosHardMax.SetValidator(NumValidator("digit"))
        self.txtAxisSetupPosHardMax.SetEditable( False )
        self.txtAxisSetupPosHardMax.SetValue('300.0')
        
        self.txtAxisSetupPosUserMax = xrc.XRCCTRL(self.SetupPositionPanel,'txtAxisSetupPosUserMax')
        self.txtAxisSetupPosUserMax.SetValidator(NumValidator("digit"))
        self.txtAxisSetupPosUserMax.SetEditable( False )
        self.txtAxisSetupPosUserMax.SetValue('300.0')
        
        self.txtAxisSetupPosIst     = xrc.XRCCTRL(self.SetupPositionPanel,'txtAxisSetupPosIst')
        self.txtAxisSetupPosIst.SetEditable( False )
        self.txtAxisSetupPosUserMin = xrc.XRCCTRL(self.SetupPositionPanel,'txtAxisSetupPosUserMin')
        self.txtAxisSetupPosUserMin.SetValidator(NumValidator("digit"))
        self.txtAxisSetupPosUserMin.SetEditable( False )
        self.txtAxisSetupPosUserMin.SetValue('-300.0')
        
        self.txtAxisSetupPosHardMin = xrc.XRCCTRL(self.SetupPositionPanel,'txtAxisSetupPosHardMin')
        self.txtAxisSetupPosHardMin.SetValidator(NumValidator("digit"))
        self.txtAxisSetupPosHardMin.SetEditable( False )
        self.txtAxisSetupPosHardMin.SetValue('-300.0')
        
        self.txtAxisSetupPosPosWin = xrc.XRCCTRL(self.SetupPositionPanel,'txtAxisSetupPosPosWin')
        self.txtAxisSetupPosPosWin.SetValidator(NumValidator("digit"))
        self.txtAxisSetupPosPosWin.SetEditable( False )
        self.txtAxisSetupPosPosWin.SetValue('1.50')
        
        self.btnAxisSetupPosWrite    = xrc.XRCCTRL(self.SetupPositionPanel,'btnAxisSetupPosWrite')
        self.btnAxisSetupPosCancel    = xrc.XRCCTRL(self.SetupPositionPanel,'btnAxisSetupPosCancel')
        
        # Kinder vom SetupVelPanel
        
        self.btnAxisSetupVelEdit = xrc.XRCCTRL(self.SetupVelPanel,'btnAxisSetupVelEdit')
        
        self.txtAxisSetupVelMaxMot  = xrc.XRCCTRL(self.SetupVelPanel,'txtAxisSetupVelMaxMot')
        self.txtAxisSetupVelMaxMot.SetEditable( False )
        
        self.txtAxisSetupVelMax  = xrc.XRCCTRL(self.SetupVelPanel,'txtAxisSetupVelMax')
        self.txtAxisSetupVelMax.SetValidator(NumValidator("positivdigit"))
        self.txtAxisSetupVelMax.SetEditable( False )
        self.txtAxisSetupVelMax.SetValue('8.0')
        
        self.txtAxisSetupAccMax  = xrc.XRCCTRL(self.SetupVelPanel,'txtAxisSetupAccMax')
        self.txtAxisSetupAccMax.SetValidator(NumValidator("positivdigit"))
        self.txtAxisSetupAccMax.SetEditable( False )
        self.txtAxisSetupAccMax.SetValue('5.5')
        
        self.txtAxisSetupDccMax  = xrc.XRCCTRL(self.SetupVelPanel,'txtAxisSetupDccMax')
        self.txtAxisSetupDccMax.SetValidator(NumValidator("positivdigit"))
        self.txtAxisSetupDccMax.SetEditable( False )
        self.txtAxisSetupDccMax.SetValue('5.5')
        
        self.txtAxisSetupAccTot = xrc.XRCCTRL(self.SetupVelPanel,'txtAxisSetupAccTot')
        self.txtAxisSetupAccTot.SetValidator(NumValidator("positivdigit"))
        self.txtAxisSetupAccTot.SetEditable( False )
        self.txtAxisSetupAccTot.SetValue('5.5')
        
        self.txtAxisSetupMaxAmp  = xrc.XRCCTRL(self.SetupVelPanel,'txtAxisSetupMaxAmp')
        self.txtAxisSetupMaxAmp.SetValidator(NumValidator("positivdigit"))
        self.txtAxisSetupMaxAmp.SetEditable( False )
        self.txtAxisSetupMaxAmp.SetValue('150')
        
        self.txtAxisSetupVelWin  = xrc.XRCCTRL(self.SetupVelPanel,'txtAxisSetupVelWin')
        self.txtAxisSetupMaxAmp.SetValidator(NumValidator("positivdigit"))
        self.txtAxisSetupVelWin.SetEditable( False )
        self.txtAxisSetupVelWin.SetValue('1.5')
        
        self.btnAxisSetupVelWrite    = xrc.XRCCTRL(self.SetupVelPanel,'btnAxisSetupVelWrite')
        self.btnAxisSetupVelCancel    = xrc.XRCCTRL(self.SetupVelPanel,'btnAxisSetupVelCancel')

        # Kinder vom SetupGuidePanel
        
        self.txtAxisSetupGuidePos = xrc.XRCCTRL(self.SetupGuidePanel, 'txtAxisSetupGuidePos')
        self.txtAxisSetupGuidePos.SetEditable( False )
        
        self.txtAxisSetupGuideVel = xrc.XRCCTRL(self.SetupGuidePanel, 'txtAxisSetupGuideVel')
        self.txtAxisSetupGuideVel.SetEditable( False )
        
        self.sldAxisSetupGuideVel        = xrc.XRCCTRL(self.SetupGuidePanel,'sldAxisSetupGuideVel')
        self.sldAxisSetupGuideVel.Enable(False)
        
        self.btnAxisSetupGuideSetup  = xrc.XRCCTRL(self.SetupGuidePanel,'btnAxisSetupGuideSetup')
        
        self.txtAxisSetupGuideError  = xrc.XRCCTRL(self.SetupGuidePanel,'txtAxisSetupGuideError')
        self.txtAxisSetupGuideError.SetEditable( False )
        
        self.btnAxisSetupGuideReset  = xrc.XRCCTRL(self.SetupGuidePanel,'btnAxisSetupGuideReset')
        self.btnAxisSetupGuideReset.Enable(False)
        
        self.txtAxisSetupGuidePitch  = xrc.XRCCTRL(self.SetupGuidePanel,'txtAxisSetupGuidePitch')
        self.txtAxisSetupGuidePitch.SetValidator(NumValidator("digit"))
        self.txtAxisSetupGuidePitch.SetEditable( False )
        
        self.btnAxisSetupGuideWrite    = xrc.XRCCTRL(self.SetupGuidePanel,'btnAxisSetupGuideWrite')
        
        self.txtAxisSetupGuidePosMax = xrc.XRCCTRL(self.SetupGuidePanel,'txtAxisSetupGuidePosMax')
        self.txtAxisSetupGuidePosMax.SetValidator(NumValidator("digit"))
        self.txtAxisSetupGuidePosMax.SetEditable( False )
        
        self.txtAxisSetupGuidePosMaxMax = xrc.XRCCTRL(self.SetupGuidePanel,'txtAxisSetupGuidePosMaxMax')
        self.txtAxisSetupGuidePosMaxMax.SetEditable( False )        
        
        self.txtAxisSetupGuidePosMin = xrc.XRCCTRL(self.SetupGuidePanel,'txtAxisSetupGuidePosMin')
        self.txtAxisSetupGuidePosMin.SetValidator(NumValidator("digit"))
        self.txtAxisSetupGuidePosMin.SetEditable( False )
        self.txtAxisSetupGuidePosMin.SetValue('0.0')
        
        self.btnAxisSetupGuideCancel    = xrc.XRCCTRL(self.SetupGuidePanel,'btnAxisSetupGuideCancel')
        
        self.btnAxisSetupGuideClutch    = xrc.XRCCTRL(self.SetupGuidePanel,'btnAxisSetupGuideClutch')
        self.btnAxisSetupGuideClutch.SetValue(True)
        
        self.btnAxisSetupGuideMoveLeft  = xrc.XRCCTRL(self.SetupGuidePanel,'btnAxisSetupGuideMoveLeft')
        self.btnAxisSetupGuideMoveStop  = xrc.XRCCTRL(self.SetupGuidePanel,'btnAxisSetupGuideMoveStop')
        self.btnAxisSetupGuideMoveRight = xrc.XRCCTRL(self.SetupGuidePanel,'btnAxisSetupGuideMoveRight')
        
        self.rbSReady           = xrc.XRCCTRL(self.SetupGuidePanel,'rbSReady')
        self.rbSPowered         = xrc.XRCCTRL(self.SetupGuidePanel,'rbSPowered')
        


        # Kinder vom SetupFilterPanel
        self.btnAxisSetupFilterEdit = xrc.XRCCTRL(self.SetupFilterPanel,'btnAxisSetupFilterEdit')
        self.txtAxisSetupFilterLagError    = xrc.XRCCTRL(self.SetupFilterPanel,'txtAxisSetupFilterLagError')
        self.txtAxisSetupFilterLagError.SetEditable( False )
        self.txtAxisSetupFilterP    = xrc.XRCCTRL(self.SetupFilterPanel,'txtAxisSetupFilterP')
        self.txtAxisSetupFilterP.SetValidator(NumValidator("positivdigit"))
        self.txtAxisSetupFilterP.SetEditable( False )
        self.txtAxisSetupFilterI    = xrc.XRCCTRL(self.SetupFilterPanel,'txtAxisSetupFilterI')
        self.txtAxisSetupFilterI.SetValidator(NumValidator("positivdigit"))
        self.txtAxisSetupFilterI.SetEditable( False )
        self.txtAxisSetupFilterD    = xrc.XRCCTRL(self.SetupFilterPanel,'txtAxisSetupFilterD')
        self.txtAxisSetupFilterD.SetValidator(NumValidator("positivdigit"))
        self.txtAxisSetupFilterD.SetEditable( False )
        self.txtAxisSetupFilterIL    = xrc.XRCCTRL(self.SetupFilterPanel,'txtAxisSetupFilterIL')
        self.txtAxisSetupFilterIL.SetValidator(NumValidator("positivdigit"))
        self.txtAxisSetupFilterIL.SetEditable( False )
        self.txtAxisSetupFilterRampform = xrc.XRCCTRL(self.SetupFilterPanel,'txtAxisSetupFilterRampform')
        self.txtAxisSetupFilterRampform.SetEditable( False )
        self.btnAxisSetupFilterWrite    = xrc.XRCCTRL(self.SetupFilterPanel,'btnAxisSetupFilterWrite')
        self.btnAxisSetupFilterCancel    = xrc.XRCCTRL(self.SetupFilterPanel,'btnAxisSetupFilterCancel')

        # Kinder vom SetupRopePanel
        
        self.btnAxisSetupRopeEdit     = xrc.XRCCTRL(self.SetupRopePanel,'btnAxisSetupRopeEdit')
        self.btnAxisSetupRopeEdit.Enable(False)
        self.txtAxisSetupRopeSWLL     = xrc.XRCCTRL(self.SetupRopePanel,'txtAxisSetupRopeSWLL')
        self.txtAxisSetupRopeSWLL.SetEditable( False )
        self.txtAxisSetupRopeDiameter = xrc.XRCCTRL(self.SetupRopePanel,'txtAxisSetupRopeDiameter')
        self.txtAxisSetupRopeDiameter.SetEditable( False )
        self.txtAxisSetupRopeType     = xrc.XRCCTRL(self.SetupRopePanel,'txtAxisSetupRopeType')
        self.txtAxisSetupRopeType.SetEditable( False )
        self.txtAxisSetupRopeNumber   = xrc.XRCCTRL(self.SetupRopePanel,'txtAxisSetupRopeNumber')
        self.txtAxisSetupRopeNumber.SetEditable( False )
        self.txtAxisSetupRopeLength   = xrc.XRCCTRL(self.SetupRopePanel,'txtAxisSetupRopeLength')
        self.txtAxisSetupRopeLength.SetEditable( False )
        self.btnAxisSetupRopeWrite    = xrc.XRCCTRL(self.SetupRopePanel,'btnAxisSetupRopeWrite')
        self.btnAxisSetupRopeCancel    = xrc.XRCCTRL(self.SetupRopePanel,'btnAxisSetupRopeCancel')
        
        # Kinder vom EStopPanel
        
        self.rMaster          = xrc.XRCCTRL(self.EStopPanel,'rMaster')
        self.rMaster.SetValue(True)
         
        self.rSlave           = xrc.XRCCTRL(self.EStopPanel,'rSlave')
        self.rSlave.SetValue(True)
        
        self.rNetwork         = xrc.XRCCTRL(self.EStopPanel,'rNetwork')
        self.rNetwork.SetValue(True)
        
        self.btnEReset        = xrc.XRCCTRL(self.EStopPanel,'btnEReset')
        
        self.rEStop1          = xrc.XRCCTRL(self.EStopPanel,'rEStop1')
        self.rEStop1.SetValue(True)
        
        self.rEStop2          = xrc.XRCCTRL(self.EStopPanel,'rEStop2')
        self.rEStop2.SetValue(True)
        
        self.rSteuerwort       = xrc.XRCCTRL(self.EStopPanel,'rSteuerwort')
        self.rSteuerwort.SetValue(True)
        
        self.r30kWOK          = xrc.XRCCTRL(self.EStopPanel,'r30kWOK')
        self.r30kWOK.SetValue(True)
        
        self.r05kWOK          = xrc.XRCCTRL(self.EStopPanel,'r05kWOK')
        self.r05kWOK.SetValue(True)
        
        self.rB1OK            = xrc.XRCCTRL(self.EStopPanel,'rB1OK')
        self.rB1OK.SetValue(True)
        
        self.rB2OK            = xrc.XRCCTRL(self.EStopPanel,'rB2OK')
        self.rB2OK.SetValue(True)
        
        self.rDSC             = xrc.XRCCTRL(self.EStopPanel,'rDCS')
        self.rDSC.SetValue(True)
        
        self.rSPSOK          = xrc.XRCCTRL(self.EStopPanel,'rSPSOK')
        self.rSPSOK.SetValue(True)
        
        self.rBRK2KB         = xrc.XRCCTRL(self.EStopPanel,'rBRK2KB')
        self.rBRK2KB.SetValue(True)
        
        self.rPosWin          = xrc.XRCCTRL(self.EStopPanel,'rPosWin')
        self.rPosWin.SetValue(True)
        
        self.rVelWin          = xrc.XRCCTRL(self.EStopPanel,'rVelWin')
        self.rVelWin.SetValue(True)
        
        self.rEndlage         = xrc.XRCCTRL(self.EStopPanel,'rEndlage')
        self.rEndlage.SetValue(True)
        
        self.rG1COM           = xrc.XRCCTRL(self.EStopPanel,'rG1COM')
        self.rG1COM.SetValue(True)
        
        self.rG1OUT           = xrc.XRCCTRL(self.EStopPanel,'rG1OUT')
        self.rG1OUT.SetValue(True)
        
        self.rG1FB            = xrc.XRCCTRL(self.EStopPanel,'rG1FB')
        self.rG1FB.SetValue(True)
        
        self.rG2COM           = xrc.XRCCTRL(self.EStopPanel,'rG2COM')
        self.rG2COM.SetValue(True)
        
        self.rG2OUT           = xrc.XRCCTRL(self.EStopPanel,'rG2OUT')
        self.rG2OUT.SetValue(True)
        
        self.rG2FB            = xrc.XRCCTRL(self.EStopPanel,'rG2FB')
        self.rG2FB.SetValue(True)
        
        self.rG3COM           = xrc.XRCCTRL(self.EStopPanel,'rG3COM')
        self.rG3COM.SetValue(True)
        
        self.rG3OUT           = xrc.XRCCTRL(self.EStopPanel,'rG3OUT')
        self.rG3OUT.SetValue(True)
       
        self.rG3FB            = xrc.XRCCTRL(self.EStopPanel,'rG3FB')
        self.rG3FB.SetValue(True)      

    def init_MainframeEvents(self):
        self.Command = 0
        self.EnableStatus = 0
        self.Controlle = False
        self.Online    = False
        self.Bind(wx.EVT_COMBOBOX, self.OnAxisSelect, id=xrc.XRCID('cmbAxisName'))
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnAxisReset, id=xrc.XRCID('btnAxisReset'))

        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupPosEdit, id=xrc.XRCID('btnAxisSetupPosEdit'))
        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupPosWrite, id=xrc.XRCID('btnAxisSetupPosWrite'))
        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupPosCancel, id=xrc.XRCID('btnAxisSetupPosCancel'))

        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupVelEdit, id=xrc.XRCID('btnAxisSetupVelEdit'))
        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupVelWrite, id=xrc.XRCID('btnAxisSetupVelWrite'))
        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupVelCancel, id=xrc.XRCID('btnAxisSetupVelCancel'))

        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupGuideSetup, id=xrc.XRCID('btnAxisSetupGuideSetup'))
        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupGuideWrite, id=xrc.XRCID('btnAxisSetupGuideWrite'))
        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupGuideCancel, id=xrc.XRCID('btnAxisSetupGuideCancel'))
        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupGuideReset,  id=xrc.XRCID('btnAxisSetupGuideReset'))

        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnAxisSetupGuideClutch, id=xrc.XRCID('btnAxisSetupGuideClutch'))

        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupFilterEdit, id=xrc.XRCID('btnAxisSetupFilterEdit'))        
        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupFilterWrite, id=xrc.XRCID('btnAxisSetupFilterWrite'))
        self.Bind(wx.EVT_BUTTON, self.OnAxisSetupFilterCancel, id=xrc.XRCID('btnAxisSetupFilterCancel'))
        
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnEReset, id=xrc.XRCID('btnEReset'))
        self.Bind(wx.EVT_BUTTON, self.OnReSync, id = xrc.XRCID('btnReSync'))
        
        self.txtAxisError.Bind(wx.EVT_LEFT_DOWN, self.OnAxisErrorClick, id=xrc.XRCID('txtAxisError'))
        self.txtAxisSetupGuideError.Bind(wx.EVT_LEFT_DOWN, self.OnAxisGuideErrorClick, id=xrc.XRCID('txtAxisSetupGuideError'))
        
        self.Bind(wx.EVT_BUTTON, self.OnRecoverClick, id=xrc.XRCID('btnRecover'))

    def OnRecoverClick(self,evt):        
        if self.btnRecover.GetLabel() != 'Running':
            self.btnRecover.SetLabel('Running')    
            self.Modus ='recover'
        else:
            self.btnRecover.SetLabel('Recover')
            self.Modus = 'r'
        evt.Skip()

    def OnReSync(self,evt):
        #print 'ReSync'
        App.Yellow.ReSync = 1
        for i in range(10):
            App.Yellow.comunicateServer()
        App.Yellow.ReSync = 0
        
    def OnAxisErrorClick(self,evt):
        
        ##rect = self.GetRect()
        ##x1, y1 = rect.GetTopLeft() 
        ##a=self.Decode.Decode(self.Achse.Status)                                                    #[2] Axis Status  
        ##self.test = wx.TipWindow(self, str(a[0]))
        ##self.test.SetBoundingRect(wx.Rect(x1+480,y1+20,x1+580,y1+100))
        
        try:
            App.Yellow
            App.Green
            App.Cyan
            App.Magenta
            AchsenInitialisiert=True
        except:
            AchsenInitialisiert=False
        if AchsenInitialisiert:
            rect = self.GetRect()
            x1, y1 = rect.GetTopLeft() 
            a=self.Decode.Decode(App.Yellow.Status)                                                    #[2] Axis Status  
            self.test = wx.TipWindow(self, str(a[0]))
            self.test.SetBoundingRect(wx.Rect(x1+400,y1,x1+580,y1+200))
    
    def OnAxisGuideErrorClick(self,evt):
        
        ##rect = self.GetRect()
        ##x1, y1 = rect.GetTopLeft() 
        ##a=self.Decode.Decode(self.Achse.GuideStatus)                                                    #[2] Axis Status  
        ##self.test = wx.TipWindow(self, str(a[0]))
        ##self.test.SetBoundingRect(wx.Rect(x1+285,y1+20,x1+580,y1+100))
        
        try:
            App.Yellow
            App.Green
            App.Cyan
            App.Magenta
            AchsenInitialisiert=True
        except:
            AchsenInitialisiert=False
        if AchsenInitialisiert:
            rect = self.GetRect()
            x1, y1 = rect.GetTopLeft() 
            a=self.Decode.Decode(App.Yellow.GuideStatus)                                                    #[2] Axis Status  
            self.test = wx.TipWindow(self, str(a[0]))
            self.test.SetBoundingRect(wx.Rect(x1+285,y1,x1+580,y1+200))
            
    def OnAxisReset(self, evt):
        
        if self.btnAxisReset.GetValue():
            self.btnAxisReset.SetLabel("reseting")
        else:        
            self.btnAxisReset.SetLabel("Reset")
    def OnAxisEnable(self,evt):

        if self.btnAxisReset.GetValue():
            self.EnableStatus = 64
        else:
            if self.Modus == 'JoyEnabeled' or self.Modus == 'recover' :
                self.cmbAxisName.Enable(False)
                self.EnableStatus = 1
            else:
                self.EnableStatus = 0
                self.Modus = 'r'
               
        if (evt & 32):
            if self.StatusPanelColour != "Green":
                self.StatusPanel.SetBackgroundColour((0,150,0))
                self.StatusPanel.Refresh()
                self.sldAxisVel.Refresh
                self.StatusPanelColour = "Green"
        else:
            if self.StatusPanelColour != "RedBrown":             
                self.StatusPanel.SetBackgroundColour((128,128,128))
                self.StatusPanel.Refresh()
                self.sldAxisVel.Refresh
                self.StatusPanelColour = "RedBrown"                
            #Clutch
                


    #--------------------------------------------------------------- 
    def OnAxisSetupPosEdit(self, evt):
        #print "AxisSetupPosEdit"
        self.DisableControls()
        self.Modus = 'E' # Setup Pos Edit
        self.btnAxisSetupPosWrite.Enable(True)
        self.btnAxisSetupPosCancel.Enable(True)

        self.PosHardMax     = self.txtAxisSetupPosHardMax.GetValue()
        self.PosUserMax     = self.txtAxisSetupPosUserMax.GetValue()
        self.PosUserMin     = self.txtAxisSetupPosUserMin.GetValue()
        self.PosHardMin     = self.txtAxisSetupPosHardMin.GetValue()
        self.PosWin         = self.txtAxisSetupPosPosWin.GetValue()

        self.txtAxisSetupPosHardMax.SetEditable( True )
        self.txtAxisSetupPosUserMax.SetEditable( True )
        self.txtAxisSetupPosUserMin.SetEditable( True )
        self.txtAxisSetupPosHardMin.SetEditable( True )
        self.txtAxisSetupPosPosWin.SetEditable( True )
        self.txtAxisSetupPosHardMax.SetBackgroundColour(wx.Colour(255,255,255))
        self.txtAxisSetupPosUserMax.SetBackgroundColour(wx.Colour(255,255,255))
        #self.txtAxisSetupPosIst.SetBackgroundColour(wx.Colour(255,255,255))
        self.txtAxisSetupPosUserMin.SetBackgroundColour(wx.Colour(255,255,255))
        self.txtAxisSetupPosHardMin.SetBackgroundColour(wx.Colour(255,255,255))
        self.txtAxisSetupPosPosWin.SetBackgroundColour(wx.Colour(255,255,255))

    def OnAxisSetupPosWrite(self, evt):
        #print "AxisSetupPosWrite"  
        self.EnableControls()
        self.btnAxisSetupPosWrite.Enable(False)
        self.btnAxisSetupPosCancel.Enable(False)
        
        
        if not((float(self.txtAxisSetupPosHardMax.GetValue()) >= float(self.txtAxisSetupPosUserMax.GetValue())) and
               (float(self.txtAxisSetupPosUserMax.GetValue()) >  float(self.txtAxisSetupPosUserMin.GetValue())) and
               (float(self.txtAxisSetupPosUserMin.GetValue()) >= float(self.txtAxisSetupPosHardMin.GetValue()))):
            dlg=wx.MessageDialog(None,'Limits not monotone! Values uncanged','Error User Limit',wx.OK|wx.ICON_EXCLAMATION)
            result=dlg.ShowModal()
            dlg.Destroy
            self.txtAxisSetupPosHardMax.SetValue(str(self.PosHardMax))
            self.txtAxisSetupPosUserMax.SetValue(str(self.PosUserMax))
            self.txtAxisSetupPosUserMin.SetValue(str(self.PosUserMin))
            self.txtAxisSetupPosHardMin.SetValue(str(self.PosHardMin))
            self.txtAxisSetupPosHardMax.Refresh()
            self.txtAxisSetupPosUserMax.Refresh()
            self.txtAxisSetupPosUserMin.Refresh()
            self.txtAxisSetupPosHardMin.Refresh()

        #PosWin            
        if ((float(self.txtAxisSetupPosPosWin.GetValue()) > 1.5 ) or
            float(self.txtAxisSetupPosPosWin.GetValue()) < 0.01):
            dlg=wx.MessageDialog(None,'0.01 m < PosWin < 1.5 m ; Reset to Last Value','Error Wrong Input',wx.OK|wx.ICON_EXCLAMATION)
            result=dlg.ShowModal()
            dlg.Destroy        
            self.txtAxisSetupPosPosWin.SetValue(self.PosWin)
            self.txtAxisSetupPosPosWin.Refresh()
        else:             
            self.PosPosWin    = float(self.txtAxisSetupPosPosWin.GetValue()) 



        self.Modus = 'w'

        self.txtAxisSetupPosHardMax.SetEditable( False )
        self.txtAxisSetupPosUserMax.SetEditable( False )
        self.txtAxisSetupPosUserMin.SetEditable( False )
        self.txtAxisSetupPosHardMin.SetEditable( False )
        self.txtAxisSetupPosPosWin.SetEditable( False )
        self.txtAxisSetupPosHardMax.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupPosUserMax.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupPosIst.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupPosUserMin.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupPosHardMin.SetBackgroundColour(wx.Colour(187,187,187)) 
        self.txtAxisSetupPosPosWin.SetBackgroundColour(wx.Colour(187,187,187))

    def OnAxisSetupPosCancel(self, evt):
        #print "AxisSetupPosCancel" 
        self.EnableControls()
        self.Modus = 'r'#setup Pos Cancel
        self.btnAxisSetupPosWrite.Enable(False)
        self.btnAxisSetupPosCancel.Enable(False)

        self.txtAxisSetupPosHardMax.SetValue(self.PosHardMax)
        self.txtAxisSetupPosUserMax.SetValue(self.PosUserMax)
        self.txtAxisSetupPosUserMin.SetValue(self.PosUserMin)
        self.txtAxisSetupPosHardMin.SetValue(self.PosHardMin)
        self.txtAxisSetupPosPosWin.SetValue(self.PosWin)

        self.txtAxisSetupPosHardMax.SetEditable( False )
        self.txtAxisSetupPosUserMax.SetEditable( False )
        self.txtAxisSetupPosUserMin.SetEditable( False )
        self.txtAxisSetupPosHardMin.SetEditable( False )
        self.txtAxisSetupPosPosWin.SetEditable( False )
        self.txtAxisSetupPosHardMax.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupPosUserMax.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupPosIst.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupPosUserMin.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupPosHardMin.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupPosPosWin.SetBackgroundColour(wx.Colour(187,187,187))

    #---------------------------------------------------------------
    def OnAxisSetupVelEdit(self, evt):
        #print "AxisSetupVelEdit"  
        self.DisableControls()
        self.Modus = 'E'#setup Vel Edit
        self.btnAxisSetupVelWrite.Enable(True)
        self.btnAxisSetupVelCancel.Enable(True)

        self.VelMax     = abs(float(self.txtAxisSetupVelMax.GetValue()))           
        self.AccMax     = abs(float(self.txtAxisSetupAccMax.GetValue()))
        self.DccMax     = abs(float(self.txtAxisSetupDccMax.GetValue()))
        self.AccTot     = abs(float(self.txtAxisSetupAccTot.GetValue()))
        self.MaxAmp     = abs(float(self.txtAxisSetupMaxAmp.GetValue()))
        self.VelWin     = abs(float(self.txtAxisSetupVelWin.GetValue()))        

        self.txtAxisSetupVelMax.SetEditable( True )
        self.txtAxisSetupAccMax.SetEditable( True )
        self.txtAxisSetupDccMax.SetEditable( True )
        self.txtAxisSetupAccTot.SetEditable( True )
        self.txtAxisSetupMaxAmp.SetEditable( True )
        self.txtAxisSetupVelWin.SetEditable( True )
        self.txtAxisSetupVelMax.SetBackgroundColour(wx.Colour(255,255,255))        
        self.txtAxisSetupAccMax.SetBackgroundColour(wx.Colour(255,255,255))
        self.txtAxisSetupDccMax.SetBackgroundColour(wx.Colour(255,255,255))       
        self.txtAxisSetupAccTot.SetBackgroundColour(wx.Colour(255,255,255))        
        self.txtAxisSetupMaxAmp.SetBackgroundColour(wx.Colour(255,255,255))
        self.txtAxisSetupVelWin.SetBackgroundColour(wx.Colour(255,255,255))

    def OnAxisSetupVelWrite(self, evt):
        #print "AxisSetupVelWrite" 
        self.EnableControls()
        #self.btnAxisSetupVelWrite.Enable(False)
        #self.btnAxisSetupVelCancel.Enable(False)
        #MaxVel
        if (abs(float(self.txtAxisSetupVelMax.GetValue())) > 
            abs(float(self.txtAxisSetupVelMaxMot.GetValue()))):
            dlg=wx.MessageDialog(None,'MaxVel larger than MaxVel Motor; Value uncanged','Error User Limit',wx.OK|wx.ICON_EXCLAMATION)
            result=dlg.ShowModal()
            dlg.Destroy
            modifyMaxVel = False
        else:
            modifyMaxVel = True       
        #MaxAmp
        if (float(self.txtAxisSetupMaxAmp.GetValue()) > 150.0 or 
            float(self.txtAxisSetupMaxAmp.GetValue()) < 50 ):
            dlg=wx.MessageDialog(None,'50% < MaxAmp < 150% ; Reset to Last Value','Error Wrong Input',wx.OK|wx.ICON_EXCLAMATION)
            result=dlg.ShowModal()
            dlg.Destroy        
            modifyMaxAmp = False
        else:             
            modifyMaxAmp = True           
        #VelWin       
        if (float(self.txtAxisSetupVelWin.GetValue()) > 1.5 or 
            float(self.txtAxisSetupVelWin.GetValue()) < 0.01):
            dlg=wx.MessageDialog(None,'0.01 m/s < VelWin < 1.5 m/s; Reset to Last Value','Error Wrong Input',wx.OK|wx.ICON_EXCLAMATION)
            result=dlg.ShowModal()
            dlg.Destroy        
            modifyVelWin = False
        else:             
            modifyVelWin = True
            #AccMove        
        if (float(self.txtAxisSetupAccTot.GetValue()) > 10.0 or 
            float(self.txtAxisSetupAccTot.GetValue()) < 1.5 ):
            dlg=wx.MessageDialog(None,'1.5 m/ss< Acc Move < 10 m/ss; Value uncanged','Error Wrong Input',wx.OK|wx.ICON_EXCLAMATION)
            result=dlg.ShowModal()
            dlg.Destroy        
            modifyAccMove = False
        else:
            modifyAccMove = True         
        #AccMax    
        if (abs(float(self.txtAxisSetupAccMax.GetValue())) > abs(float(self.txtAxisSetupAccTot.GetValue())) or
            abs(float(self.txtAxisSetupDccMax.GetValue())) > abs(float(self.txtAxisSetupAccTot.GetValue()))):
            dlg=wx.MessageDialog(None,'Acc/Dcc/AccMove Mismatch; Values unchanged','Error AccMax',wx.OK|wx.ICON_EXCLAMATION)
            result=dlg.ShowModal()
            dlg.Destroy
            modifyAccDccAccMove = False
        else:
            modifyAccDccAccMove = True
               
        
        if modifyMaxVel and modifyMaxAmp and modifyVelWin and modifyAccDccAccMove and modifyAccMove :
            self.VelMax     = abs(float(self.txtAxisSetupVelMax.GetValue()))
            self.MaxAmp     = float(self.txtAxisSetupMaxAmp.GetValue())
            self.VelWin     = float(self.txtAxisSetupVelWin.GetValue()) 
            self.AccMax     = abs(float(self.txtAxisSetupAccMax.GetValue()))
            self.DccMax     = abs(float(self.txtAxisSetupDccMax.GetValue()))
            self.AccTot     = abs(float(self.txtAxisSetupAccTot.GetValue()))
            self.btnAxisSetupVelWrite.Enable(False)
            self.btnAxisSetupVelCancel.Enable(False)            
        else:
            self.txtAxisSetupVelMax.SetValue(str(self.VelMax))
            self.txtAxisSetupMaxAmp.SetValue(str(self.MaxAmp))
            self.txtAxisSetupVelWin.SetValue(str(self.VelWin))            
            self.txtAxisSetupAccMax.SetValue(str(abs(self.AccMax)))     
            self.txtAxisSetupDccMax.SetValue(str(abs(self.DccMax)))     
            self.txtAxisSetupAccTot.SetValue(str(abs(self.AccTot)))
            self.btnAxisSetupVelWrite.Enable(True)
            self.btnAxisSetupVelCancel.Enable(True)            
            

        self.Modus = 'w'

        self.txtAxisSetupVelMax.SetEditable( False )
        self.txtAxisSetupAccMax.SetEditable( False )
        self.txtAxisSetupDccMax.SetEditable( False )
        self.txtAxisSetupAccTot.SetEditable( False )
        self.txtAxisSetupMaxAmp.SetEditable( False )
        self.txtAxisSetupVelWin.SetEditable( False )
        self.txtAxisSetupVelMax.SetBackgroundColour(wx.Colour(187,187,187))        
        self.txtAxisSetupAccMax.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupDccMax.SetBackgroundColour(wx.Colour(187,187,187))       
        self.txtAxisSetupAccTot.SetBackgroundColour(wx.Colour(187,187,187))        
        self.txtAxisSetupMaxAmp.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupVelWin.SetBackgroundColour(wx.Colour(187,187,187))


    def OnAxisSetupVelCancel(self, evt):
        #print "AxisSetupVelCancel" 
        self.EnableControls()
        self.Modus = 'r'#setup Vel Cancel
        self.btnAxisSetupVelWrite.Enable(False)
        self.btnAxisSetupVelCancel.Enable(False)

        self.txtAxisSetupVelMax.SetValue(str(self.VelMax))
        self.txtAxisSetupAccMax.SetValue(str(self.AccMax))
        self.txtAxisSetupDccMax.SetValue(str(self.DccMax))
        self.txtAxisSetupAccTot.SetValue(str(self.AccTot))
        self.txtAxisSetupMaxAmp.SetValue(str(self.MaxAmp))
        self.txtAxisSetupVelWin.SetValue(str(self.VelWin))
        

        self.txtAxisSetupVelMax.SetEditable( False )
        self.txtAxisSetupAccMax.SetEditable( False )
        self.txtAxisSetupDccMax.SetEditable( False )
        self.txtAxisSetupAccTot.SetEditable( False )
        self.txtAxisSetupMaxAmp.SetEditable( False )
        self.txtAxisSetupVelWin.SetEditable( False )
        self.txtAxisSetupVelMax.SetBackgroundColour(wx.Colour(187,187,187))        
        self.txtAxisSetupAccMax.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupDccMax.SetBackgroundColour(wx.Colour(187,187,187))       
        self.txtAxisSetupAccTot.SetBackgroundColour(wx.Colour(187,187,187))        
        self.txtAxisSetupMaxAmp.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupVelWin.SetBackgroundColour(wx.Colour(187,187,187)) 

#----------------------------------------------------------------
    def OnAxisSetupGuideSetup(self, evt):
        #print "AxisSetupGuideSetup"
        self.DisableControls()
        self.Modus = 'E' # Setup Pos Edit

        self.btnAxisSetupGuideReset.Enable(False)
        self.btnAxisSetupGuideWrite.Enable(True)
        self.btnAxisSetupGuideCancel.Enable(True)


        self.GuidePitch     = self.txtAxisSetupGuidePitch.GetValue()
        self.GuidePosMax    = self.txtAxisSetupGuidePosMax.GetValue()
        self.GuidePosMin    = self.txtAxisSetupGuidePosMin.GetValue()

        self.txtAxisSetupGuidePitch.SetEditable( True )
        self.txtAxisSetupGuidePosMax.SetEditable( True )
        #self.txtAxisSetupGuidePosMin.SetEditable( True ) # Muss erst in SPS implementiert werden
        self.txtAxisSetupGuidePitch.SetBackgroundColour(wx.Colour(255,255,255))
        self.txtAxisSetupGuidePosMax.SetBackgroundColour(wx.Colour(255,255,255))
        #self.txtAxisSetupGuidePosMin.SetBackgroundColour(wx.Colour(255,255,255)) # Muss erst in SPS implementiert werden

    def OnAxisSetupGuideWrite(self, evt):
        #print "AxisSetupGuideWrite"
        self.EnableControls()
        self.btnAxisSetupGuideReset.Enable(True)

        self.btnAxisSetupGuideWrite.Enable(False)
        self.btnAxisSetupGuideCancel.Enable(False)
        
        if (abs(float(self.txtAxisSetupGuidePitch.GetValue())) > 15 ):
            dlg=wx.MessageDialog(None,'Guide Pitch > 15mm; Value uncanged','Error Pitch',wx.OK|wx.ICON_EXCLAMATION)
            result=dlg.ShowModal()
            dlg.Destroy
            self.txtAxisSetupGuidePitch.SetValue(str(self.GuidePitch))
            self.txtAxisSetupGuidePitch.Refresh() 
            
        if ((float(self.txtAxisSetupGuidePosMax.GetValue())) < 0.05 or
            (float(self.txtAxisSetupGuidePosMax.GetValue())) > (float(self.txtAxisSetupGuidePosMaxMax.GetValue())) ):
            dlg=wx.MessageDialog(None,'Pos Max Guider out of bounds; Value unchanged','Error Pos Max',wx.OK|wx.ICON_EXCLAMATION)
            result=dlg.ShowModal()
            dlg.Destroy
            self.txtAxisSetupGuidePosMax.SetValue(str(self.GuidePosMax))
            self.txtAxisSetupGuidePosMax.Refresh()
            
        self.GuidePitch     = self.txtAxisSetupGuidePitch.GetValue()
        self.GuidePosMax    = self.txtAxisSetupGuidePosMax.GetValue()
        self.GuidePosMin    = self.txtAxisSetupGuidePosMin.GetValue()

        self.Modus = 'w'

        self.txtAxisSetupGuidePitch.SetEditable( False )
        self.txtAxisSetupGuidePosMax.SetEditable( False )
        self.txtAxisSetupGuidePosMin.SetEditable( False )
        self.txtAxisSetupGuidePitch.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupGuidePosMax.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupGuidePosMin.SetBackgroundColour(wx.Colour(187,187,187)) 

    def OnAxisSetupGuideCancel(self, evt):
        #print "AxisSetupGuideCancel" 
        self.EnableControls()
        
        self.Modus ='r'

        self.btnAxisSetupGuideReset.Enable(True)
        self.btnAxisSetupGuideWrite.Enable(False)
        self.btnAxisSetupGuideCancel.Enable(False)

        self.txtAxisSetupGuidePitch.SetValue(self.GuidePitch )
        self.txtAxisSetupGuidePosMax.SetValue(self.GuidePosMax)
        self.txtAxisSetupGuidePosMin.SetValue(self.GuidePosMin)

        self.txtAxisSetupGuidePitch.SetEditable( False )
        self.txtAxisSetupGuidePosMax.SetEditable( False )
        self.txtAxisSetupGuidePosMin.SetEditable( False )
        self.txtAxisSetupGuidePitch.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupGuidePosMax.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupGuidePosMin.SetBackgroundColour(wx.Colour(187,187,187)) 


    def OnAxisSetupGuideReset(self, evt):
        #print "AxisSetupGuideReset"
        self.btnAxisSetupGuideClutch.SetLabel('reseting')
        dlg=wx.MessageDialog(None,'Pls Cycle DeadMan Switch after closing this Dialog and wait for the reset to complete','Slave reset',wx.OK|wx.ICON_EXCLAMATION)
        result=dlg.ShowModal()
        dlg.Destroy         
        
    def OnAxisSetupGuideClutch(self, evt):
        #print "AxisSetupGuideClutch"        
        if self.btnAxisSetupGuideClutch.GetValue():
            #print "  engage Clutch"
            self.ClutchStatus = 1
            self.GuideControl = 5
            self.DisableGuideControls() 
            self.btnAxisSetupGuideClutch.SetLabel('engaged')
        else:

            #print "  Dis-engage Clutch"
            self.ClutchStatus = 0
            self.GuideControl = 2
            self.EnableGuideControls()
            self.btnAxisSetupGuideClutch.SetLabel('dis-engaged')

    
#----------------------------------------------------------------
    def OnAxisSetupFilterEdit(self, evt):
        #print "AxisSetupFilterEdit" 
        self.DisableControls()
        self.Modus = 'E'#setup Filter Edit
        self.btnAxisSetupFilterWrite.Enable(True)
        self.btnAxisSetupFilterCancel.Enable(True)

        self.P      = self.txtAxisSetupFilterP.GetValue()
        self.I      = self.txtAxisSetupFilterI.GetValue()
        self.D     = self.txtAxisSetupFilterD.GetValue()
        self.IL     = self.txtAxisSetupFilterIL.GetValue()

        self.txtAxisSetupFilterP.SetEditable( True )
        self.txtAxisSetupFilterI.SetEditable( True )
        self.txtAxisSetupFilterD.SetEditable( True )
        self.txtAxisSetupFilterIL.SetEditable( True )
        self.txtAxisSetupFilterP.SetBackgroundColour(wx.Colour(255,255,255))        
        self.txtAxisSetupFilterI.SetBackgroundColour(wx.Colour(255,255,255))        
        self.txtAxisSetupFilterD.SetBackgroundColour(wx.Colour(255,255,255))
        self.txtAxisSetupFilterIL.SetBackgroundColour(wx.Colour(255,255,255))

    def OnAxisSetupFilterWrite(self, evt):
        #print "AxisSetupFilterWrite"
        self.EnableControls()
        self.btnAxisSetupFilterWrite.Enable(False)
        self.btnAxisSetupFilterCancel.Enable(False)

        self.P     = self.txtAxisSetupFilterP.GetValue()
        self.I      = self.txtAxisSetupFilterI.GetValue()
        self.D     = self.txtAxisSetupFilterD.GetValue()
        self.IL    = self.txtAxisSetupFilterIL.GetValue()

        self.Modus = 'w'

        self.txtAxisSetupFilterP.SetEditable( False )
        self.txtAxisSetupFilterI.SetEditable( False )
        self.txtAxisSetupFilterD.SetEditable( False )
        self.txtAxisSetupFilterIL.SetEditable( False )
        self.txtAxisSetupFilterP.SetBackgroundColour(wx.Colour(187,187,187))        
        self.txtAxisSetupFilterI.SetBackgroundColour(wx.Colour(187,187,187))        
        self.txtAxisSetupFilterD.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupFilterIL.SetBackgroundColour(wx.Colour(187,187,187)) 

    def OnAxisSetupFilterCancel(self, evt):
        #print "AxisSetupFilterCancel" 
        self.EnableControls()
        self.Modus = 'r'#setup Filter Cancel
        self.btnAxisSetupFilterWrite.Enable(False)
        self.btnAxisSetupFilterCancel.Enable(False)

        self.txtAxisSetupFilterP.SetValue(self.P)
        self.txtAxisSetupFilterI.SetValue(self.I)
        self.txtAxisSetupFilterD.SetValue(self.D)
        self.txtAxisSetupFilterIL.SetValue(self.IL)

        self.txtAxisSetupFilterP.SetEditable( False )
        self.txtAxisSetupFilterI.SetEditable( False )
        self.txtAxisSetupFilterD.SetEditable( False )
        self.txtAxisSetupFilterIL.SetEditable( False )
        self.txtAxisSetupFilterP.SetBackgroundColour(wx.Colour(187,187,187))        
        self.txtAxisSetupFilterI.SetBackgroundColour(wx.Colour(187,187,187))        
        self.txtAxisSetupFilterD.SetBackgroundColour(wx.Colour(187,187,187))
        self.txtAxisSetupFilterIL.SetBackgroundColour(wx.Colour(187,187,187)) 

#-------------------------------------------------------------------------------
    def OnEReset(self,evt):
        if self.btnEReset.GetValue():
            App.Yellow.PosSoll = App.Yellow.PosIst
            App.Yellow.EStopReset = 1
            for i in range(10):
                App.Yellow.comunicateServer()
            App.Yellow.EStopReset = 0
            if abs(float(self.txtPosDiff.GetValue())) < 0.01:
                self.OnReSync(1)
            self.btnEReset.SetValue(False)

            
    def EnableGuideControls(self):
        #print "Enabel Guide Controls" 
        self.btnAxisSetupGuideReset.Enable(True) 

    def DisableGuideControls(self):
        #print "Disabel Guide Controls" 

        self.btnAxisSetupGuideReset.Enable(False)

#----------------------------------------------------------------    
    def GoOnline(self):
        # Pruefe ob anderer Client das Commando hat
        if self.Online == False: 
            #print " Going Online" 
            App.Yellow.Intent  = 'False'
            self.EnableControls()
            self.Modus = 'r'#setup Rope Cancel
            self.txtTimeTick.SetBackgroundColour(wx.Colour(0 ,150,0))
            self.cmbAxisName.SetBackgroundColour(wx.Colour(0 ,150,0))
            self.txtTimeTick.Refresh()
            self.cmbAxisName.Refresh()
            self.Online = True


    def GoOffline(self):
        #if self.Online == True:
        #print " Going Offline" 
        self.Online = False
        self.DisableControls()
        self.Modus = 'rE'#setup Rope Cancel
        self.txtTimeTick.SetBackgroundColour(wx.Colour(255,255,255))
        self.cmbAxisName.SetBackgroundColour(wx.Colour(255,255,255))
        self.txtTimeTick.Refresh()
        self.cmbAxisName.Refresh()
        return

    def PermitOnline(self):
        if self.Controlle == False:
            #print "Online Permission"
            App.Yellow.Intent  = 'True'
            self.Controlle = True


    def DenyOnline(self):
        if self.Controlle == True:
            #print "Online forbidden"  
            App.Yellow.Intent = 'False'
            self.Controlle = False

    def DisableControls(self):
        if self.ControlsEnabeled:
            #print 'Disabeling Controls'
            self.btnAxisReset.Enable(False)
            self.btnAxisSetupPosEdit.Enable(False)
            self.btnAxisSetupPosWrite.Enable(False)
            self.btnAxisSetupPosCancel.Enable(False)
            self.txtAxisSetupPosHardMax.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupPosUserMax.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupPosIst.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupPosUserMin.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupPosHardMin.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupPosPosWin.SetBackgroundColour(wx.Colour(187,187,187)) 
            self.btnAxisSetupVelEdit.Enable(False)
            self.btnAxisSetupVelWrite.Enable(False)
            self.btnAxisSetupVelCancel.Enable(False)
            self.txtAxisSetupVelMaxMot.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupVelMaxMot.SetForegroundColour(wx.Colour(255,0,0))
            self.txtAxisSetupVelMax.SetBackgroundColour(wx.Colour(187,187,187))        
            self.txtAxisSetupAccMax.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupDccMax.SetBackgroundColour(wx.Colour(187,187,187))       
            self.txtAxisSetupAccTot.SetBackgroundColour(wx.Colour(187,187,187))        
            self.txtAxisSetupMaxAmp.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupVelWin.SetBackgroundColour(wx.Colour(187,187,187))
            self.btnAxisSetupGuideSetup.Enable(False)
            self.btnAxisSetupGuideWrite.Enable(False)
            self.btnAxisSetupGuideCancel.Enable(False)
            self.btnAxisSetupGuideReset.Enable(False)              
            self.btnAxisSetupGuideClutch.Enable(False)
    
            self.txtAxisSetupGuidePitch.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupGuidePosMax.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupGuidePosMin.SetBackgroundColour(wx.Colour(187,187,187))        
            self.btnAxisSetupFilterEdit.Enable(False)        
            self.btnAxisSetupFilterWrite.Enable(False)
            self.btnAxisSetupFilterCancel.Enable(False)
            self.txtAxisSetupFilterLagError.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupFilterP.SetBackgroundColour(wx.Colour(187,187,187))        
            self.txtAxisSetupFilterI.SetBackgroundColour(wx.Colour(187,187,187))        
            self.txtAxisSetupFilterD.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupFilterIL.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupFilterRampform.SetBackgroundColour(wx.Colour(187,187,187))
            self.btnAxisSetupRopeEdit.Enable(False)
            self.btnAxisSetupRopeWrite.Enable(False)
            self.btnAxisSetupRopeCancel.Enable(False)
            self.txtAxisSetupRopeSWLL.SetBackgroundColour(wx.Colour(187,187,187))        
            self.txtAxisSetupRopeDiameter.SetBackgroundColour(wx.Colour(187,187,187))        
            self.txtAxisSetupRopeType.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupRopeNumber.SetBackgroundColour(wx.Colour(187,187,187))
            self.txtAxisSetupRopeLength.SetBackgroundColour(wx.Colour(187,187,187))
            self.ControlsEnabeled = False
            self.btnRecover.Enable(False)
            self.btnReSync.Enable(False)
    def EnableControls(self):
        if not(self.ControlsEnabeled):
            #print 'Enabeling Controls'
            self.btnAxisReset.Enable(True)
            self.btnAxisSetupPosEdit.Enable(True)
            self.btnAxisSetupVelEdit.Enable(True)
            self.btnAxisSetupGuideSetup.Enable(True)
            self.btnAxisSetupGuideReset.Enable(True)              
            self.btnAxisSetupGuideClutch.Enable(True)
            self.btnAxisSetupFilterEdit.Enable(True)        
            #self.btnAxisSetupRopeEdit.Enable(True)
            #self.btnRecover.Enable(True)
            self.ControlsEnabeled = True
            
    def OnAxisSelect(self,evt):
        try:
            App.Yellow            
            item = evt.GetSelection()
            if App.Yellow.Name <> self.Achsen[item]:

                dlg = wx.MessageDialog(None, 'Are you sure you want to reassign Yellow Axis ?','Question', wx.OK | wx.CANCEL | wx.NO_DEFAULT | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                dlg.Destroy()
                if result == wx.ID_OK:
                    try:
                        Temp = Achse(self.Achsen[item]) # Achse item laesst sich assignen
                    except: # wenn anderes GUI kontrolle dann auf SIMUL
                        dlg = wx.MessageDialog(None, 'Yellow Axis set to SIMUL !','Reset to SIMUL', wx.OK | wx.ICON_EXCLAMATION)
                        result = dlg.ShowModal()
                        dlg.Destroy()                        
                        del App.Yellow
                        App.Yellow = Achse('SIMUL')
                        App.Yellow.OwnPID= '0'#str(os.getpid())
                        #print 'Axis '+self.Achsen[item]+ ' as Yellow selected'
                        App.Yellow.comunicateServer()
                        taskMgr.add(self.AxisTask,'YellowAxisTask')
                    else:
                        #print 'Gelb lsst sich auf ' + str(self.Achsen[item]) + ' assignen'
                        try:
                            del Temp
                        except:
                            pass
                        
                        self.ResetAxis()
                else:
                    #print ' Accessing App.Yellow '
                    self.ReadDatafromAchse()
        except: # Noch kein Achsobjekt
            self.ResetAxis()

    def AxisReadJoystick(self):
        self.initJoystick()
        self.keepGoing                       = True
        self.LTold                           = 0
        self.ControlingPIDTx                 = 0
        self.ControlingPIDRx                 = 0
        self.Progression                     = 0.0001
        self.WriteZaehler = 0
        self.T1Old = 0
        self.VX = 0
        self.Pos0 = 0
        self.EnableOld = 0
        self.PoweredOld = 0
        self.Decode  = Decode()
        self.InitAxis = 1
        self.FahrbefehlOld = 1
        self.refreshEstopPanel = "Yellow"
        self.refreshBitPanel = "RedBrown"
        self.refreshRecoverPanel = "RedBrown"
        self.refreshSelect = "Blue"
        self.GuideControlOld = 2
        self.ValueSLDMain = 0
        self.ValueSLDSlave = 0
        self.SetupVelMax = 0

        taskMgr.add(self.AxisTask,'YellowAxisTask')
        
    def LoadFromFileQuit(self):

        taskMgr.remove("YellowAxisTask")
        
    def ResetAxis(self):
        
        self.initJoystick()
        self.keepGoing                       = True
        self.LTold                           = 0
        self.ControlingPIDTx                 = 0
        self.ControlingPIDRx                 = 0
        self.Progression                     = 0.0001
        self.WriteZaehler = 0
        self.T1Old = 0
        self.VX = 0
        self.Pos0 = 0
        self.EnableOld = 0
        self.PoweredOld = 0
        self.Decode  = Decode()
        self.InitAxis = 1
        self.FahrbefehlOld = 1
        self.refreshEstopPanel = "Yellow"
        self.refreshBitPanel = "RedBrown"
        self.refreshRecoverPanel = "RedBrown"
        self.refreshSelect = "Blue"
        self.GuideControlOld = 2
        self.ValueSLDMain = 0
        self.ValueSLDSlave = 0
        self.SetupVelMax = 0

        self.Modus = 'rE' # initialisieren im read Edit Mode
        self.Command=False
        self.DisableControls()
        try:
            App.Yellow
            AxisExists = True
            #print 'Gelb existiert'
        except: # Noch kein Achsobjekt
            AxisExists = False
            #print 'Gelb non exist'
            
        if not(AxisExists): # noch kein Achsobjekt -> neues instanzieren
            #print 'bauen neues Gelb'
            item=self.cmbAxisName.GetCurrentSelection()
            App.Yellow = Achse(self.Achsen[item])
            App.Yellow.OwnPID= str(os.getpid())
            #print 'Axis '+self.Achsen[item]+ ' as Yellow selected'
            App.Yellow.comunicateServer()
        else:
            del App.Yellow
            #print 'del Yellow'
            item=self.cmbAxisName.GetCurrentSelection()
            App.Yellow = Achse(self.Achsen[item])
            App.Yellow.OwnPID= '0'#str(os.getpid())
            #print 'Neues Neues Gelb'
            #print 'Axis '+self.Achsen[item]+ ' as Yellow selected'
            App.Yellow.comunicateServer()            
            
        taskMgr.add(self.AxisTask,'YellowAxisTask') 
        
        return True
        
    def Loadfromfile(self,item):
        
        self.initJoystick()
        self.keepGoing                       = True
        self.LTold                           = 0
        self.ControlingPIDTx                 = 0
        self.ControlingPIDRx                 = 0
        self.Progression                     = 0.0001
        self.WriteZaehler = 0
        self.T1Old = 0
        self.VX = 0
        self.Pos0 = 0
        self.EnableOld = 0
        self.PoweredOld = 0
        self.Decode  = Decode()
        self.InitAxis = 1
        self.FahrbefehlOld = 1
        self.refreshEstopPanel = "Yellow"
        self.refreshBitPanel = "RedBrown"
        self.refreshRecoverPanel = "RedBrown"
        self.refreshSelect = "Blue"
        self.GuideControlOld = 2
        self.ValueSLDMain = 0
        self.ValueSLDSlave = 0
        self.SetupVelMax = 0
        
        self.Modus = 'rE' # initialisieren im read Edit Mode
        self.Command=False
        self.DisableControls()
        
        
        try:
            App.Yellow
            YellowExists = True
        except:
            YellowExists = False
        if not(YellowExists):
            App.Yellow = Achse(item.rstrip('\n'))
            App.Yellow.OwnPID= str(os.getpid())
            #print 'Axis '+item.rstrip('\n')+ ' as Yellow selected'
        else:
            taskMgr.remove('YellowAxisTask')
            del App.Yellow
            App.Yellow = Achse(item.rstrip('\n'))
            App.Yellow.OwnPID= str(os.getpid())
            
        App.Yellow.comunicateServer()

        taskMgr.add(self.AxisTask,'YellowAxisTask')        


    def AxisTask(self,task):
        
        self.refresh()
        return task.cont
    
    
    def refresh(self):
        
        self.readJoystick()
        self.readDataFromGUI()
        self.RampGenerator()        
        self.comunicateServer()
        self.writeDataToGUI()
        self.CheckStatus()
        
    def readDataFromGUI(self):

        App.Yellow.ControlingPIDTx = 0
        App.Yellow.Intent          = self.Command
        App.Yellow.Enable          = self.EnableStatus
        ##App.Yellow.EStopReset      = str(self.EStopReset)
        
        if App.Yellow.EStopReset == '1':
            self.Pos0 = App.Yellow.PosIst
        if self.btnAxisSetupGuideClutch.GetLabel() == "reseting":
            App.Yellow.GuideControl   = 5
            b=self.Decode.Decode(App.Yellow.GuideStatus)
            if b[1][0][2] == "Save Stop" or b[1][0][2] == "Not Enabled" or b[1][0][2] == "Ready":
                self.btnAxisSetupGuideClutch.SetLabel("Reset")
                if self.btnAxisSetupGuideClutch.GetValue():
                    self.btnAxisSetupGuideClutch.SetLabel("engaged")
                else:
                    self.btnAxisSetupGuideClutch.SetLabel("dis-engaged")
        else:
            if self.ClutchStatus == 1:
                App.Yellow.GuideControl   = 5
            else:
                if self.buttons & 128:
                    App.Yellow.GuideControl   = 17
                else:
                    App.Yellow.GuideControl   = 2 
                    
        if self.btnAxisReset.GetLabel() == "reseting":
            b=self.Decode.Decode(App.Yellow.Status)
            if b[1][0][2] == "Save Stop" or b[1][0][2] == "Not Enabled" or b[1][0][2] == "Ready":
                self.btnAxisReset.SetLabel("Reset") 
                self.btnAxisReset.SetValue(0)
        try:
            App.Yellow.Modus         = self.Modus
            App.Yellow.SpeedSoll     = self.VX
            App.Yellow.GuideSpeedSoll= self.sldAxisSetupGuideVel.GetValue()*20
            if not (self.txtAxisSetupPosHardMax.GetValue() == "-" or self.txtAxisSetupPosHardMax.GetValue() ==""):
                App.Yellow.PosHardMax    = float(self.txtAxisSetupPosHardMax.GetValue())
            if not (self.txtAxisSetupPosUserMax.GetValue() == "-" or self.txtAxisSetupPosUserMax.GetValue() == "") :
                App.Yellow.PosUserMax    = float(self.txtAxisSetupPosUserMax.GetValue())
            if not (self.txtAxisSetupPosUserMin.GetValue() == "-"  or self.txtAxisSetupPosUserMin.GetValue() == ""):
                App.Yellow.PosUserMin    = float(self.txtAxisSetupPosUserMin.GetValue())
            if not (self.txtAxisSetupPosHardMin.GetValue() == "-" or self.txtAxisSetupPosHardMin.GetValue() == "" ):
                App.Yellow.PosHardMin    = float(self.txtAxisSetupPosHardMin.GetValue())
            if not (self.txtAxisSetupPosPosWin.GetValue() == "-"  or self.txtAxisSetupPosPosWin.GetValue() == ""):
                App.Yellow.PosWin           = abs(float(self.txtAxisSetupPosPosWin.GetValue()))
            if not (self.txtAxisSetupVelMax.GetValue() == "-" or self.txtAxisSetupVelMax.GetValue() == ""):
                App.Yellow.SpeedMax         = abs(float(self.txtAxisSetupVelMax.GetValue()))
            if not (self.txtAxisSetupAccMax.GetValue() == "-" or self.txtAxisSetupAccMax.GetValue() == ""):
                App.Yellow.AccMax           = abs(float(self.txtAxisSetupAccMax.GetValue()))
            if not (self.txtAxisSetupDccMax.GetValue() == "-" or self.txtAxisSetupDccMax.GetValue() == ""):
                App.Yellow.DccMax           = abs(float(self.txtAxisSetupDccMax.GetValue()))
            if not (self.txtAxisSetupAccTot.GetValue() == "-" or self.txtAxisSetupAccTot.GetValue() == ""):
                App.Yellow.AccTot           = abs(float(self.txtAxisSetupAccTot.GetValue()))
            if not (self.txtAxisSetupMaxAmp.GetValue() == "-" or self.txtAxisSetupMaxAmp.GetValue() == ""):
                App.Yellow.MaxAmp           = abs(float(self.txtAxisSetupMaxAmp.GetValue()))
            if not (self.txtAxisSetupVelWin.GetValue() == "-" or self.txtAxisSetupVelWin.GetValue() == ""):
                App.Yellow.VelWin           = abs(float(self.txtAxisSetupVelWin.GetValue()))
            if not (self.txtAxisSetupFilterP.GetValue() == "-" or self.txtAxisSetupFilterP.GetValue() == ""):
                App.Yellow.FilterP          = abs(float(self.txtAxisSetupFilterP.GetValue()))
            if not (self.txtAxisSetupFilterI.GetValue() == "-" or self.txtAxisSetupFilterI.GetValue() == ""):
                App.Yellow.FilterI          = abs(float(self.txtAxisSetupFilterI.GetValue()))
            if not (self.txtAxisSetupFilterD.GetValue() == "-" or self.txtAxisSetupFilterD.GetValue() == ""):
                App.Yellow.FilterD          = abs(float(self.txtAxisSetupFilterD.GetValue()))
            if not (self.txtAxisSetupFilterIL.GetValue() == "-" or self.txtAxisSetupFilterIL.GetValue() == ""):
                App.Yellow.FilterIL         = abs(float(self.txtAxisSetupFilterIL.GetValue()))
            if not (self.txtAxisSetupRopeSWLL.GetValue() == "-" or self.txtAxisSetupRopeSWLL.GetValue() == ""):
                App.Yellow.RopeSWLL         = abs(float(self.txtAxisSetupRopeSWLL.GetValue()))
            if not (self.txtAxisSetupRopeDiameter.GetValue() == "-" or self.txtAxisSetupRopeDiameter.GetValue() == ""):
                App.Yellow.RopeDiameter     = abs(float(self.txtAxisSetupRopeDiameter.GetValue()))
            App.Yellow.RopeType         = self.txtAxisSetupRopeType.GetValue()
            App.Yellow.RopeNumber       = self.txtAxisSetupRopeNumber.GetValue()
            if not (self.txtAxisSetupRopeLength.GetValue() == "-" or self.txtAxisSetupRopeLength.GetValue() == ""):
                App.Yellow.RopeLength       = abs(float(self.txtAxisSetupRopeLength.GetValue()))
            if not (self.txtAxisSetupGuidePitch.GetValue() == "-" or self.txtAxisSetupGuidePitch.GetValue() == "-"):
                App.Yellow.GuidePitch       = float(self.txtAxisSetupGuidePitch.GetValue())
            if not (self.txtAxisSetupGuidePosMax.GetValue() == "-" or self.txtAxisSetupGuidePosMax.GetValue() == ""):
                App.Yellow.GuidePosMax      = abs(float(self.txtAxisSetupGuidePosMax.GetValue()))
            App.Yellow.GuidePosMaxMax   = float(self.txtAxisSetupGuidePosMaxMax.GetValue())
            if not (self.txtAxisSetupGuidePosMin.GetValue() == "-" or self.txtAxisSetupGuidePosMin.GetValue() == ""):
                App.Yellow.GuidePosMin      = float(self.txtAxisSetupGuidePosMin.GetValue())
        except ValueError:
            dlg=wx.MessageDialog(None,'Please use just numbers, minus and . as comma. Like 123.45  Use <Backspace> to correct the error!','Syntax ERROR',wx.OK|wx.ICON_EXCLAMATION)
            result=dlg.ShowModal()
            dlg.Destroy
            self.txtAxisSetupPosHardMax.SetValue(str(App.Yellow.PosHardMax))
            self.txtAxisSetupPosUserMax.SetValue(str(App.Yellow.PosUserMax))
            self.txtAxisSetupPosUserMin.SetValue(str(App.Yellow.PosUserMin))
            self.txtAxisSetupPosHardMin.SetValue(str(App.Yellow.PosHardMin))
            self.txtAxisSetupPosPosWin.SetValue(str(App.Yellow.PosWin))
            self.txtAxisSetupVelMax.SetValue(str(App.Yellow.SpeedMax))
            self.txtAxisSetupAccMax.SetValue(str(App.Yellow.AccMax))
            self.txtAxisSetupDccMax.SetValue(str(App.Yellow.DccMax))
            self.txtAxisSetupAccTot.SetValue(str(App.Yellow.AccTot))
            self.txtAxisSetupMaxAmp.SetValue(str(App.Yellow.MaxAmp))
            self.txtAxisSetupVelWin.SetValue(str(App.Yellow.VelWin))
            self.txtAxisSetupFilterP.SetValue(str(App.Yellow.FilterP))
            self.txtAxisSetupFilterI.SetValue(str(App.Yellow.FilterI))
            self.txtAxisSetupFilterD.SetValue(str(App.Yellow.FilterD))
            self.txtAxisSetupFilterIL.SetValue(str(App.Yellow.FilterIL))
            self.txtAxisSetupRopeSWLL.SetValue(str(App.Yellow.RopeSWLL))
            self.txtAxisSetupRopeDiameter.SetValue(str(App.Yellow.RopeDiameter))
            self.txtAxisSetupRopeType.SetValue(str(App.Yellow.RopeType))
            self.txtAxisSetupRopeNumber.SetValue(str(App.Yellow.RopeNumber))
            self.txtAxisSetupRopeLength.SetValue(str(App.Yellow.RopeLength))
            self.txtAxisSetupGuidePitch.SetValue(str(App.Yellow.GuidePitch))
            self.txtAxisSetupGuidePosMax.SetValue(str(App.Yellow.GuidePosMax))
            self.txtAxisSetupGuidePosMaxMax.SetValue(str(App.Yellow.GuidePosMaxMax))
            self.txtAxisSetupGuidePosMin.SetValue(str(App.Yellow.GuidePosMin))
            self.readDataFromGUI()

    def ReadDatafromAchse(self):
        
        self.Command          = App.Yellow.Intent           
        self.Enable           = App.Yellow.Enable
        if App.Yellow.GuideControl   == 5:
            self.btnAxisSetupGuideClutch.SetValue(True)    # Noch nicht passend        
        elif App.Yellow.GuideControl   == 17:              # Noch nicht passend  
            self.btnAxisSetupGuideEnable.SetValue(True)    # Noch nicht passend                 
        else:                                              # Noch nicht passend  
            self.btnAxisSetupGuideClutch.SetValue(True)    # Noch nicht passend  
            self.btnAxisSetupGuideEnable.SetValue(True)    # Noch nicht passend 
        self.Modus = App.Yellow.Modus 
        
        self.cmbAxisName.SetSelection(self.cmbAxisName.GetItems().index(unicode(App.Yellow.Name)))
        
        self.sldAxisVel.SetValue(500)    # Noch nicht passend 
        self.sldAxisSetupGuideVel.SetValue(50)
        self.txtAxisPos.SetValue(App.Yellow.PosIst)
        self.txtAxisSetupPosIst.SetValue(App.Yellow.PosIst)
        self.txtAxisSetupPosHardMax.SetValue(str(App.Yellow.PosHardMax)) 
        self.txtAxisSetupPosUserMax.SetValue(str(App.Yellow.PosUserMax))
        self.txtAxisSetupPosUserMin.SetValue(str(App.Yellow.PosUserMin))
        self.txtAxisSetupPosHardMin.SetValue(str(App.Yellow.PosHardMin))
        self.txtAxisSetupVelMax.SetValue(str(App.Yellow.SpeedMax))
        self.txtAxisSetupAccMax.SetValue(str(App.Yellow.AccMax))
        self.txtAxisSetupDccMax.SetValue(str(App.Yellow.DccMax))
        if App.Yellow.MaxAmp == 0.0:
            self.txtAxisSetupMaxAmp.SetValue("SIMUL")                
        else:
            self.txtAxisSetupMaxAmp.SetValue(str(App.Yellow.MaxAmp))
        self.txtAxisSetupFilterP.SetValue(App.Yellow.FilterP)
        self.txtAxisSetupFilterI.SetValue(App.Yellow.FilterI)
        self.txtAxisSetupFilterD.SetValue(App.Yellow.FilterD)
        self.txtAxisSetupFilterIL.SetValue(App.Yellow.FilterIL)
        self.txtAxisSetupGuidePitch.SetValue(App.Yellow.GuidePitch)
        self.txtAxisSetupGuidePosMax.SetValue(App.Yellow.GuidePosMax)
        self.txtAxisSetupGuidePosMin.SetValue(App.Yellow.GuidePosMin)
        


    def comunicateServer(self):
        App.Yellow.comunicateServer()

    def RampGenerator(self):
        if self.InitAxis == 1:
            self.Pos0 = App.Yellow.PosIst
            self.InitAxis = 0
        self.Pos0=App.Yellow.PosSoll        
        T1     = time.clock()
        self.DiffT= T1-self.T1Old
        self.T1Old  = T1
        # Fahrbefehlstaster gedrueckt Programm reagiert normal auf Joystick
        if App.Yellow.EsTaster:
            if self.FahrbefehlOld == 1:
                self.Pos0 = App.Yellow.PosIst
                self.FahrbefehlOld = 0
                
            d=self.Decode.Decode(App.Yellow.Status) #schauen ob Verstaerker in TechOpt ist
            if d[1][0][1] == "10"and (self.buttons & 32 and self.buttons & 1):
                if self.Modus != 'recover':
                    #self.SetupVelMax = float(self.txtAxisSetupVelMax.GetValue())
                    self.SetupVelMax = max((float(self.txtAxisSetupVelMax.GetValue()))/10,1.0) #3D Aktivieren
                else:
                    self.SetupVelMax = max((float(self.txtAxisSetupVelMax.GetValue()))/10,1.0)
                x = (self.sldAxisVel.GetValue() - 500) * 2 *self.SetupVelMax/1000  # 20 = 1000mm / 50 fuer Prozent
            else:
                x=0
            #VelX
            if self.VX < x:
                self.VX = self.VX + float(App.Yellow.AccMax)*(self.DiffT)
                if self.VX >= x:
                    self.VX = x
            elif self.VX > x:
                self.VX = self.VX - float(App.Yellow.DccMax)*(self.DiffT)
                if self.VX <= x:
                        self.VX = x  
        # Abfangen der Endpositionen *)
        #Bei Fahrt Richtung oberes Ende Beginn
            PosDiffG = float(App.Yellow.PosUserMax) - float(App.Yellow.PosIst)
            if PosDiffG > 0 :
                SpeedMaxG = math.sqrt(float(App.Yellow.DccMax)*0.8*PosDiffG)
                self.VX = min(self.VX,SpeedMaxG);
            else:
                if self.VX > 0:
                    self.VX = 0.0;
            #Bei Fahrt Richtung oberes Ende End
            #Bei Fahrt Richtung unteres Ende Beginn
            PosDiffG = float(App.Yellow.PosIst) - float(App.Yellow.PosUserMin)
            if PosDiffG > 0 :
                SpeedMaxG = math.sqrt(float(App.Yellow.DccMax)*0.8*PosDiffG)
                self.VX = max(self.VX,-SpeedMaxG);
            else:
                if self.VX < 0 :
                    self.VX = 0.0
            #Bei Fahrt Richtung unteres Ende End
# Fahrbefehlstaster offen Programm steuert Motor mit AccTot zum Stillstand
        else:
            x = 0.0
            if self.VX < x:
                self.VX = self.VX + float(App.Yellow.AccTot)*(self.DiffT)
                if self.VX >= x:
                    self.VX = x
            elif self.VX > x:
                self.VX = self.VX - float(App.Yellow.AccTot)*(self.DiffT)
                if self.VX <= x:
                        self.VX = x 
            self.FahrbefehlOld = 1
            
        App.Yellow.PosSoll= str(float(self.Pos0)+self.VX*(self.DiffT))        

    
    
    def writeDataToGUI(self):        
        a=self.Decode.Decode(App.Yellow.Status)                         
        b=self.Decode.Decode(App.Yellow.GuideStatus)
        if App.Yellow.EsTaster:
            self.DisableControls()
            self.btnAxisSetupGuideClutch.Enable(False)
            self.btnAxisSetupGuideReset.Enable(False)            
            self.cmbAxisName.Enable(False)
        else:
            if self.Modus != 'E':
                self.EnableControls()
                self.cmbAxisName.Enable(True)
                self.btnAxisSetupGuideClutch.Enable(True)
                #if self.ClutchStatus == 0:
                self.btnAxisSetupGuideReset.Enable(True)
            
        if App.Yellow.EsResetAble:
            self.btnEReset.Enable(False)
        else:
            self.btnEReset.Enable(True)
            
        self.SliderPanel.Update()

        if not(abs(float(self.txtPosDiff.GetValue())) < 0.01):
            if self.refreshRecoverPanel != 'Yellow':
                self.RecoverPanel.SetBackgroundColour((250,198,12))
                self.RecoverPanel.Refresh()
                self.refreshRecoverPanel = 'Yellow'               
        else:
            if self.refreshRecoverPanel != 'Green':
                self.RecoverPanel.SetBackgroundColour((0,150,0))
                self.RecoverPanel.Refresh()
                self.refreshRecoverPanel = 'Green'
                
        if not(App.Yellow.EsNetwork) :            
            if self.refreshEstopPanel != "Yellow":
                self.EStopPanel.SetBackgroundColour((250,198,12))
                self.EStopPanel.Refresh()
                self.refreshEstopPanel = "Yellow"
        else:
            if self.refreshEstopPanel != "Green":
                self.EStopPanel.SetBackgroundColour((0,150,0))
                self.EStopPanel.Refresh()
                self.refreshEstopPanel = "Green" 
                
        if App.Yellow.Modus !='E':
            if not(App.Yellow.EsNetwork) : 
                self.btnRecover.Enable(False)
                self.btnReSync.Enable(False)
            else:
                if (abs(float(self.txtPosDiff.GetValue())) < 0.01):
                    self.btnRecover.Enable(False)
                else:
                    self.btnRecover.Enable(True)
                if (App.Yellow.EsTaster or abs(float(self.txtPosDiff.GetValue())) < 0.01 or
                    self.btnRecover.GetLabel() == 'Running'):
                    self.btnReSync.Enable(False)
                else:     
                    self.btnReSync.Enable(True) 
        else:
            self.btnRecover.Enable(False)
            self.btnReSync.Enable(False)
            
        if (not(App.Yellow.EsNetwork)):          #Gelb
            if self.refreshBitPanel != "Yellow":
                self.BitPanel.SetBackgroundColour((250,198,12)) 
                self.BitPanel.Refresh()
                self.refreshBitPanel = "Yellow"
        else:
            if ((App.Yellow.EsReady and abs(float(self.txtPosDiff.GetValue())) >= 0.01) or
                ((App.Yellow.EsReady and abs(float(self.txtPosDiff.GetValue())) < 0.01))):
                if self.refreshBitPanel != "LightGreen":
                    self.BitPanel.SetBackgroundColour((0,150,0))
                    self.BitPanel.Refresh()
                    self.refreshBitPanel = "LightGreen"
            else:
                if (not(App.Yellow.EsReady) and abs(float(self.txtPosDiff.GetValue())) > 0.01) :
                    if self.refreshBitPanel != "Yellow":
                        self.BitPanel.SetBackgroundColour((250,198,12)) 
                        self.BitPanel.Refresh()
                        self.refreshBitPanel = "Yellow"
                else:
                    if self.refreshBitPanel != "RedBrown":
                        self.BitPanel.SetBackgroundColour((128,128,128)) 
                        self.BitPanel.Refresh()
                        self.refreshBitPanel = "RedBrown"

        if (App.Yellow.Modus == 'r' or 
            App.Yellow.Modus == 'rE' or 
            App.Yellow.Modus == 'JoyEnabeled' or
            App.Yellow.Modus == 'recover'):
            fa="%3.2f"
            fb="%2.3f"
            fc="%2.0f"
            fd="%3.1f"
            fe="%1.4f"
            self.ControlingPIDRx = App.Yellow.ControlingPIDRx                                         #[0] Controling PID
            self.txtTimeTick.SetValue(str(App.Yellow.LTold-self.LTold))
            #self.txtTimeTick.SetValue(str(self.Achse.GetLTold()-self.LTold))
            self.LTold =int(App.Yellow.LTold)                                        
            self.txtAxisError.SetValue(a[1][0][2])
            self.txtAxisError.SetBackgroundColour(a[1][0][3])
            #self.txtAxisError.SetToolTipString(str(a[0]))
                                                              #[3] Guide Status
            self.txtAxisSetupGuideError.SetValue(b[1][0][2])
            self.txtAxisSetupGuideError.SetBackgroundColour(b[1][0][3])
            #self.txtAxisSetupGuideError.SetToolTipString(str(b[0]))
            self.txtAxisPos.SetValue(str(fa%(float(App.Yellow.PosIst)) +' m'))                              #[4] AxisPos
            self.txtAxisSetupPosIst.SetValue(str(fa%(float(App.Yellow.PosIst))))
            self.txtAxisVel.SetValue(str(fa%(float(App.Yellow.SpeedIstUI)) +' m/s'))                        #[5] AxisVel
            self.txtAxisAmp.SetValue(str(fa%(float(App.Yellow.MasterMomentUI )/1000*60)+' A'))  #[6] AxisAmp
            self.txtAxisTemp.SetValue(str(App.Yellow.CabTemperature +' C'))                     #[7] AxisTemp        
            self.txtAxisSetupGuidePos.SetValue(str(App.Yellow.GuidePosIstUI))                   #[30]GuidePos
            self.txtAxisSetupGuideVel.SetValue(str(App.Yellow.GuideIstSpeedUI))                 #[31]GuideVel
            self.txtAxisSetupVelMaxMot.SetValue(str(abs(float(App.Yellow.SpeedMaxForUI))))                  #[37]VelMaxMot
            self.txtAxisSetupFilterLagError.SetValue(str(App.Yellow.PosDiffForUI ))             #[38]Lag Error
            self.cmbAxisName.SetValue(str(App.Yellow.Name))                                     #[8]  Name
            self.txtAxisSetupPosHardMax.SetValue(str(App.Yellow.PosHardMax))                    #[10] PosHardMax
            self.txtAxisSetupPosUserMax.SetValue(str(App.Yellow.PosUserMax))                    #[11] PosUserMax
            self.txtAxisSetupPosUserMin.SetValue(str(App.Yellow.PosUserMin))                    #[12] PosUserMin
            self.txtAxisSetupPosHardMin.SetValue(str(App.Yellow.PosHardMin))                    #[13] PosHardMin
            self.txtAxisSetupPosPosWin.SetValue(str(App.Yellow.PosWin))                            #[38] PosWin
            self.txtAxisSetupVelMax.SetValue(str(App.Yellow.SpeedMax))                          #[14] VelMax
            self.txtAxisSetupAccMax.SetValue(str(App.Yellow.AccMax))                            #[15] AccMax
            self.txtAxisSetupDccMax.SetValue(str(App.Yellow.DccMax))                            #[16] DccMax
            self.txtAxisSetupAccTot.SetValue(str(App.Yellow.AccTot))                            #[40] AccTot
            self.txtAxisSetupMaxAmp.SetValue(str(App.Yellow.MaxAmp))                            #[17] AmpMax
            self.txtAxisSetupVelWin.SetValue(str(App.Yellow.VelWin))                            #[39] VelWin
            self.txtAxisSetupFilterP.SetValue(str(App.Yellow.FilterP))                          #[18] FilterP
            self.txtAxisSetupFilterI.SetValue(str(App.Yellow.FilterI))                          #[19] FilterI
            self.txtAxisSetupFilterD.SetValue(str(App.Yellow.FilterD))                          #[20] FilterD
            self.txtAxisSetupFilterIL.SetValue(str(App.Yellow.FilterIL))                        #[21] FilterIL
            self.txtAxisSetupFilterRampform.SetValue(str(App.Yellow.Rampform))                  #[36] Rampform
            self.txtAxisSetupRopeSWLL.SetValue(str(App.Yellow.RopeSWLL))                        #[22] SWLL
            self.txtAxisSetupRopeDiameter.SetValue(str(App.Yellow.RopeDiameter))                #[23] Rope Diam    
            self.txtAxisSetupRopeType.SetValue(str(App.Yellow.RopeType))                        #[24] Rope Type 
            self.txtAxisSetupRopeNumber.SetValue(str(App.Yellow.RopeNumber))                    #[25] Rope Number     
            self.txtAxisSetupRopeLength.SetValue(str(App.Yellow.RopeLength))                    #[26] Rope Length   
            self.txtAxisSetupGuidePitch.SetValue(str(App.Yellow.GuidePitch))                    #[27] Pitch       
            self.txtAxisSetupGuidePosMax.SetValue(str(App.Yellow.GuidePosMax))                  #[28] Guide Pos Max
            self.txtAxisSetupGuidePosMaxMax.SetValue(str(App.Yellow.GuidePosMaxMax))            #[41] Guide Pos MaxMax
            self.txtAxisSetupGuidePosMin.SetValue(str(App.Yellow.GuidePosMin))                  #[29] Guide Pos Min
            self.txtCutPos.SetValue(str(fa%(float(App.Yellow.EStopCutPos))))
            self.txtCutVel.SetValue(str(fa%(float(App.Yellow.EStopCutVel))))
            self.txtPosDiff.SetValue(str(fa%(float(App.Yellow.EStopCutPos)-float(App.Yellow.PosIst))))
            self.txtCutTime.SetValue(str(App.Yellow.EStopCutTime))

        
        self.rMaster.SetValue(App.Yellow.EsMaster)
        self.rSlave.SetValue(App.Yellow.EsSlave)
        self.rNetwork.SetValue(App.Yellow.EsNetwork)            
        self.rEStop1.SetValue(App.Yellow.EsEStop1)
        self.rEStop2.SetValue(App.Yellow.EsEStop2)
        self.rSteuerwort.SetValue(App.Yellow.EsSteuerwort)
        self.r30kWOK.SetValue(App.Yellow.Es30kWOK )
        self.r05kWOK.SetValue(App.Yellow.Es05kWOK)
        self.rB1OK.SetValue(not(App.Yellow.EsB1OK ^ App.Yellow.EsTaster))
        self.rB2OK.SetValue(not (App.Yellow.EsB2OK ^ App.Yellow.EsTaster))
        #self.rB1OK.SetValue(App.Yellow.EsB1OK )
        #self.rB2OK.SetValue(App.Yellow.EsB2OK )        
        self.rDSC.SetValue(App.Yellow.EsDCSOK)    
        self.rSPSOK.SetValue(App.Yellow.EsSPSOK)
        self.rBRK2KB.SetValue(App.Yellow.EsBRK2KB)
        self.rPosWin.SetValue(App.Yellow.EsPosWin)
        self.rVelWin.SetValue(App.Yellow.EsVelWin)
        self.rEndlage.SetValue(App.Yellow.EsEndlage) 
        
        self.rG1COM.SetValue(App.Yellow.EsG1COM)
        self.rG1FB.SetValue(App.Yellow.EsG1FB)
        self.rG1OUT.SetValue(App.Yellow.EsG1OUT)
        self.rG2COM.SetValue(App.Yellow.EsG2COM)
        self.rG2FB.SetValue(App.Yellow.EsG2FB)
        self.rG2OUT.SetValue(App.Yellow.EsG2OUT)
        self.rG3COM.SetValue(App.Yellow.EsG3COM)
        self.rG3FB.SetValue(App.Yellow.EsG3FB)
        self.rG3OUT.SetValue(App.Yellow.EsG3OUT)
        
        if App.Yellow.EsSchluessel1:                      # Nur Master          
            font = wx.Font(8,wx.DEFAULT,wx.NORMAL,wx.BOLD)
            if App.Yellow.EsTaster:
                self.btnAxisSetupGuideClutch.Enable(False)
                self.btnAxisSetupGuideSetup.Enable(False)
            else:
                self.btnAxisSetupGuideClutch.Enable(True)
                self.btnAxisSetupGuideSetup.Enable(True)
            self.rMaster.SetFont(font)
            self.rEStop1.SetFont(font)
            self.rEStop2.SetFont(font)
            self.rSteuerwort.SetFont(font)
            self.r30kWOK.SetFont(font)
            self.rB1OK.SetFont(font)
            self.rSPSOK.SetFont(font)
            self.rBRK2KB.SetFont(font)
            self.rPosWin.SetFont(font)
            self.rVelWin.SetFont(font)
            self.rEndlage.SetFont(font)            
            font = wx.Font(8,wx.DEFAULT,wx.NORMAL,wx.LIGHT)
            self.rSlave.SetFont(font)
            self.rNetwork.SetFont(font)            
            self.r05kWOK.SetFont(font)
            self.rB2OK.SetFont(font)
            self.rDSC.SetFont(font)            
            self.rG1COM.SetFont(font) 
            self.rG1FB.SetFont(font) 
            self.rG1OUT.SetFont(font) 
            self.rG2COM.SetFont(font) 
            self.rG2FB.SetFont(font) 
            self.rG2OUT.SetFont(font) 
            self.rG3COM.SetFont(font) 
            self.rG3FB.SetFont(font) 
            self.rG3OUT.SetFont(font)            
        elif App.Yellow.EsSchluessel2:
            font = wx.Font(8,wx.DEFAULT,wx.NORMAL,wx.BOLD)          # Master und Slave
            self.btnAxisSetupGuideClutch.Enable(False)
            self.btnAxisSetupGuideSetup.Enable(False)
            self.rMaster.SetFont(font)
            self.rSlave.SetFont(font)
            self.rEStop1.SetFont(font)
            self.rEStop2.SetFont(font)
            self.rSteuerwort.SetFont(font)
            self.r30kWOK.SetFont(font)
            self.rB1OK.SetFont(font)
            self.rSPSOK.SetFont(font)
            self.rBRK2KB.SetFont(font)
            self.rPosWin.SetFont(font)
            self.rVelWin.SetFont(font)
            self.rEndlage.SetFont(font) 
            font = wx.Font(8,wx.DEFAULT,wx.NORMAL,wx.LIGHT)
            self.rNetwork.SetFont(font)            
            self.rG1COM.SetFont(font) 
            self.rG1FB.SetFont(font) 
            self.rG1OUT.SetFont(font) 
            self.rG2COM.SetFont(font) 
            self.rG2FB.SetFont(font) 
            self.rG2OUT.SetFont(font) 
            self.rG3COM.SetFont(font) 
            self.rG3FB.SetFont(font) 
            self.rG3OUT.SetFont(font) 
        else:
            font = wx.Font(8,wx.DEFAULT,wx.NORMAL,wx.BOLD)              # Master Slave und Netzwerk
            self.btnAxisSetupGuideClutch.Enable(False)
            self.btnAxisSetupGuideSetup.Enable(False)
            self.rMaster.SetFont(font)
            self.rSlave.SetFont(font)
            self.rEStop1.SetFont(font)
            self.rEStop2.SetFont(font)
            self.rSteuerwort.SetFont(font)
            self.r30kWOK.SetFont(font)
            self.rB1OK.SetFont(font)
            self.rSPSOK.SetFont(font)
            self.rBRK2KB.SetFont(font)
            self.rPosWin.SetFont(font)
            self.rVelWin.SetFont(font)
            self.rEndlage.SetFont(font) 
            self.rNetwork.SetFont(font)            
            self.r05kWOK.SetFont(font)
            self.rB2OK.SetFont(font)
            self.rDSC.SetFont(font)            
            self.rG1COM.SetFont(font) 
            self.rG1FB.SetFont(font) 
            self.rG1OUT.SetFont(font) 
            self.rG2COM.SetFont(font) 
            self.rG2FB.SetFont(font) 
            self.rG2OUT.SetFont(font) 
            self.rG3COM.SetFont(font) 
            self.rG3FB.SetFont(font) 
            self.rG3OUT.SetFont(font)
        
        if(self.rG1COM.GetValue() and
           self.rG1FB.GetValue() and
           self.rG1OUT.GetValue() and
           self.rG2COM.GetValue() and
           self.rG2FB.GetValue() and
           self.rG2OUT.GetValue() and
           self.rG3COM.GetValue() and
           self.rG3FB.GetValue() and
           self.rG3OUT.GetValue()):
            pass
            self.EStopReset =0              

        self.rbReady.SetValue(a[1][2])
        self.rbPowered.SetValue(a[1][1])
        self.rbBrake1.SetValue(App.Yellow.EsB1OK)
        self.rbBrake2.SetValue(App.Yellow.EsB2OK)
        self.rFBT.SetValue(not(App.Yellow.EsFTBOK))
        
        self.rbSReady.SetValue(b[1][2])
        self.rbSPowered.SetValue(b[1][1])
            

        if self.Modus =='w':
            self.WriteZaehler = self.WriteZaehler+1
            self.readDataFromGUI()
            App.Yellow.comunicateServer()
            if self.WriteZaehler > 4:   # Das ist naemlich so. Wenn die Werte runter geschrieben werden, braucht's eine Zeit bis sie auch
                                        # entsprechend aktualisiert wieder zurueckkommen. So etwa 5 Zyklen.
                                        # Wenn also Modus-w eintritt warten wir einige Zyklen bevor wir die Ueberpruefung beginnen.

                if (self.cmbAxisName.GetValue()                            == App.Yellow.Name          and               
                    "%.2f"%float(self.txtAxisSetupPosHardMax.GetValue())   == App.Yellow.PosHardMax    and
                    "%.2f"%float(self.txtAxisSetupPosUserMax.GetValue())   == App.Yellow.PosUserMax    and
                    "%.2f"%float(self.txtAxisSetupPosUserMin.GetValue())   == App.Yellow.PosUserMin    and
                    "%.2f"%float(self.txtAxisSetupPosHardMin.GetValue())   == App.Yellow.PosHardMin    and
                    "%.4f"%float(self.txtAxisSetupPosPosWin.GetValue())    == App.Yellow.PosWin        and
                    "%.2f"%float(self.txtAxisSetupVelMax.GetValue())       == App.Yellow.SpeedMax      and
                    "%.2f"%float(self.txtAxisSetupAccMax.GetValue())       == App.Yellow.AccMax        and
                    "%.2f"%float(self.txtAxisSetupDccMax.GetValue())       == App.Yellow.DccMax        and
                    "%.2f"%float(self.txtAxisSetupAccTot.GetValue())       == App.Yellow.AccTot        and
                    "%.2f"%float(self.txtAxisSetupMaxAmp.GetValue())       == App.Yellow.MaxAmp        and
                    "%.4f"%float(self.txtAxisSetupVelWin.GetValue())       == App.Yellow.VelWin        and
                    "%.3f"%float(self.txtAxisSetupFilterP.GetValue())      == App.Yellow.FilterP       and
                    "%.3f"%float(self.txtAxisSetupFilterI.GetValue())      == App.Yellow.FilterI       and
                    "%.3f"%float(self.txtAxisSetupFilterD.GetValue())      == App.Yellow.FilterD       and
                    "%.1f"%float(self.txtAxisSetupFilterIL.GetValue())     == App.Yellow.FilterIL      and
                    "%.3f"%float(self.txtAxisSetupGuidePitch.GetValue())   == App.Yellow.GuidePitch): # and        
                    #"%.3f"%float(self.txtAxisSetupGuidePosMax.GetValue())  == self.Achse.GuidePosMax)   and        
                    #"%.4f"%float(self.txtAxisSetupGuidePosMin.GetValue())  == self.Achse.GuidePosMin):
                    pass
                    #print 'Daten transfer OK'
                else:
                    #print 'Data transfer recheck'
                    dlg=wx.MessageDialog(None,'Data transfer: Pls Check Data','Data transfer',wx.OK|wx.ICON_EXCLAMATION)
                    result=dlg.ShowModal()
                    dlg.Destroy                                  
                self.Modus = 'rE'
                self.WriteZaehler = 0
    def readJoystick(self):

        if not((self.Modus ==  'E') or (self.Modus ==  'w')):
            self.buttons=self.stick.GetButtonState()
            a=self.stick.GetPosition().y
            d=self.stick.GetPosition().x
            b=a/32767.0-1
            e=d/32767.0-1
            # Achse
            if b>0:            
                c=b*(1-self.Progression)+b*b*self.Progression
            else:
                c=b*(1-self.Progression)-b*b*self.Progression
            self.ValueSLDMain = int(c*500.0+500)
            # Slider
            if e>0:            
                f=e*(1-self.Progression)+e*e*self.Progression
            else:
                f=e*(1-self.Progression)-e*e*self.Progression
            self.ValueSLDSlave = int(f*1000)

            if self.buttons & 1 :
                if self.refreshSelect != "Blue":
                    self.txtSelected1.SetBackgroundColour((0,200,0))
                    self.txtSelected2.SetBackgroundColour((0,200,0))
                    self.txtSelected1.SetLabel('Selected')
                    self.txtSelected2.SetLabel('Selected') 
                    self.txtSelected1.Refresh()
                    self.txtSelected2.Refresh()
                    self.refreshSelect = "Blue"
            else:
                if self.refreshSelect != "White":
                    self.txtSelected1.SetBackgroundColour((255,240,0))
                    self.txtSelected2.SetBackgroundColour((255,240,0))
                    self.txtSelected1.SetLabel('De-Selected')
                    self.txtSelected2.SetLabel('De-Selected')                     
                    self.txtSelected1.Refresh()
                    self.txtSelected2.Refresh()
                    self.refreshSelect = "White"    

            if self.Modus != "recover":
                if self.buttons & 32 and self.buttons & 1:
                    self.Modus ='JoyEnabeled'
                    if abs(float(self.txtPosDiff.GetValue())) > 0.01:
                        self.ValueSLDMain = 500
                    self.OnAxisEnable(self.buttons)
                elif not(self.buttons & 32):
                    self.Modus ='JoyDisabeled'
                    self.OnAxisEnable(self.buttons)
            else:
                if abs(float(self.txtPosDiff.GetValue())) < 0.01:
                    self.btnRecover.SetLabel('Recover')
                    self.OnReSync(1)
                    self.Modus ='r'
                    self.OnAxisEnable(self.buttons)
                self.OnAxisEnable(self.buttons)
                di= float(self.txtPosDiff.GetValue())
                PVel =  math.atan(di)/(math.pi/2)*500
                Vel = 500+PVel
                b=self.Decode.Decode(App.Yellow.GuideStatus)
                if b[1][0][1] == "10":
                    self.ValueSLDMain = Vel
                else:
                    self.ValueSLDMain = 500
      
            self.sldAxisVel.SetValue(self.ValueSLDMain)
            #self.sldAxisVel.Refresh()
            #self.SliderPanel.Refresh()
            self.sldAxisSetupGuideVel.SetValue(self.ValueSLDSlave)
            #self.sldAxisVel.Refresh()
            #self.SliderPanel.Refresh()

    def initJoystick(self):                
        #Joystick auslesen und Umrechnungen vorbereiten
        self.stick = wx.Joystick()
        self.min0 = self.stick.GetXMin()
        self.max0 = self.stick.GetXMax()
        self.diff0 = float((self.max0-self.min0)/2)
        self.min1 = self.stick.GetYMin()
        self.max1 = self.stick.GetYMax()
        self.diff1 = float((self.max1-self.min1)/2)
        self.min2 = self.stick.GetRudderMin()
        self.max2 = self.stick.GetRudderMax()
        self.diff2 = float((self.max2-self.min2)/2)
        self.min3 = self.stick.GetZMin()
        self.max3 = self.stick.GetZMax()
        self.diff3 = float((self.max3-self.min3)/2)
        if self.diff0 == 0.0 or self.diff1 == 0.0 or self.diff2 == 0.0 or self.diff3 == 0.0:
            dlg = wx.MessageDialog(self.frame, ' Joystick configuration error',' Joystick configuration error!', wx.OK|wx.ICON_EXCLAMATION)
            self.logger.debug('No Joystick')
            if dlge.ShowModal() == wx.ID_OK:
                dlge.Destroy() 
        #print       self.min0
        #print       self.max0
        #print       self.diff0
        #print       self.min1
        #print       self.max1
        #print       self.diff1
        #print       self.min2
        #print       self.max2
        #print       self.diff2
        #print       self.min3
        #print       self.max3
        #print       self.diff3
        
        
        
        
    def CheckStatus(self):
        ##if self.ControlingPIDRx == "0"   or self.ControlingPIDRx == str(App.Yellow.OwnPID) :
        if (self.ControlingPIDRx == "0" or self.ControlingPIDRx == str(App.Yellow.OwnPID) or self.ControlingPIDRx == '0000' ):     # If the system is available
            self.PermitOnline()
        else:
            self.DenyOnline()

        if (self.ControlingPIDRx == str(App.Yellow.OwnPID)) :       # If we are connected
        ##if (self.ControlingPIDRx == str(self.frame.Achse.OwnPID)) :       # If we are connected
            self.GoOnline()
        else:
            self.GoOffline()


    def OnClose(self,evt):

        try:
            App.Yellow.LTold              = 0
            App.Yellow.Modus              = 0
            App.Yellow.OwnPID             = 0
            App.Yellow.ControlingPIDTx    = 0
            App.Yellow.Intent             = 0
            App.Yellow.Enable             = 0
            App.Yellow.GuideControl       = 5
            App.Yellow.SpeedSoll          = 0
            App.Yellow.GuideSpeedSoll     = 0
            #print "Clean Exit"                  
            App.Yellow.comunicateServer()
            ##self.keepGoing = False
            taskMgr.remove("YellowAxisTask")
        except:
            ##self.keepGoing = False
            taskMgr.remove("YellowAxisTask")
            #print "Exit"
 