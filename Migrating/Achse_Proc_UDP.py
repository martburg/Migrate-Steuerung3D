from Migrating.WWWinch_properties import WWWinchProperties
from Migrating.WWWinch_codec import WWWinchCodec
from Migrating.WWWinch_achsmemory import Achsmemory
import time
import socket

MEM_NAME_GUI2HW = "achse_controler_to_hw"
MEM_NAME_HW2GUI = "achse_hw_to_controler"

ACHSEN     = {'Anton' : ("172.16.17.1", 15001,"172.16.17.5", 15001),
              'Burt'  : ("172.16.17.2", 15001,"172.16.17.5", 15002),
              'Cecil' : ("172.16.17.3", 15001,"172.16.17.5", 15003),
              'Debby' : ("172.16.17.4", 15001,"172.16.17.5", 15004),
              'Eugene': ("172.16.17.5", 15001,"172.16.17.5", 15005),
              'Fred'  : ("172.16.17.6", 15001,"172.16.17.5", 15006),
              'SIMUL' : ("127.0.0.1", 15001,"127.0.0.1", 15005)}


class Achse_Proc_UDP:
    """
    This class sends and receives properties of a axis.
    """
    
    def __init__(self, KontaktData='SIMUL'):

        shm_in  = Achsmemory(MEM_NAME_GUI2HW)
        shm_out = Achsmemory(MEM_NAME_HW2GUI)

        self.Host    = ACHSEN[KontaktData][0]
        self.Port    = ACHSEN[KontaktData][1]
        self.RecHost = ACHSEN[KontaktData][2]
        self.RecPort = ACHSEN[KontaktData][3] 
        
        self.recaddr = (self.RecHost,self.RecPort)
        self.timeOld = time.perf_counter()
        self.SpeedOld = 0.0

        self.Codec = WWWinchCodec()

        self._init_sockets()

        while True:
            try:
                controler_in_data = shm_in.read()

                Data = self.Codec.pack(controler_in_data)

                self.send(Data)

                controler_out_data = self.receive()

                shm_out.write(controler_out_data)

                time.sleep(0.01)
            except KeyboardInterrupt:
                break


    def _init_sockets(self):
        """
        Initializes the UDP sockets for sending and receiving data.
        """
        if self.Host != "127.0.0.1":
            self.sock       = None
            self.recUDPsock = None
            try:
                self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            except socket.error as e:
                raise Exception(f"Socket creation error: {e}")
            try:        
                #print 'init recsock'
                self.recUDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                self.recUDPSock.settimeout(0.25)
            except socket.error as e:
                raise Exception(f"Socket error: {e}")
            try:
                self.recUDPSock.bind(self.recaddr)
            except socket.error as e:
                if e.errno == 10048:
                    # Address already in use, likely another instance is running
                    pass
        else:
            # Simulated axis, no sockets needed
            self.sock       = None
            self.recUDPSock = None
            self.time       = time.perf_counter()
            self.IntervallR = time.perf_counter()-self.timeOld
            self.timeOld    = self.time
            self.Codec.simulate(self.IntervallR)
            try:
                self.recUDPSock.close()
                #print str(KontaktData) + '  UDP Close'
            except:
                pass            

    def send(self,Data):
        """
        Sends the properties of the axis.
        """
        if self.Host != "127.0.0.1":
            try:
                if self.ControlingPIDRx == '0' or str(self.OwnPID) == self.ControlingPIDRx or self.ControlingPIDRx == '0000':
                    self.sock.sendto(Data, (self.Host, self.Port)) 
            except:
                #print "Send Server error"
                pass
        else:
            self.time       = time.perf_counter()
            self.IntervallR = time.perf_counter()-self.timeOld
            self.timeOld    = self.time
            self.Codec.simulate(self.IntervallR)
    
    def receive(self):
        """
        Receives the properties.
        """
        if self.Host != "127.0.0.1":
            if self.ControlingPIDRx == '0' or self.OwnPID == self.ControlingPIDRx or self.ControlingPIDRx == '0000':
                #try:
                #    self.recUDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                #except:
                #    raise
                #try:
                #    self.recUDPSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                #    self.recUDPSock.bind(self.recaddr) 
                #except socket.error, (value,message):
                    #if value == 10048:
                     #   pass
                     #   dlg=wx.MessageDialog(None,'Another GUI has control','Error Another GUI',wx.OK|wx.ICON_EXCLAMATION)
                     #   result=dlg.ShowModal()
                     #   dlg.Destroy
                     #   sys.exit(1) 
                   # raise
                try:
                    self.received,addr = self.recUDPSock.recvfrom(601)
                    self.receivedBuff = self.received
                    #self.recUDPSock.close()
                except socket.timeout:
                    #print 'TimeOut'
                    self.received = self.receivedBuff
                else:
                    #print "Rec Server error"
                    self.received = self.receivedBuff
        else:
            self.received = self.receivedBuff


        self.Codec.unpack(self.received)
        if self.InitAchse == 1:            
            self.PosSoll = self.PosIst
            if self.Host != "127.0.0.1":
                try:
                    SendData=self.Codec.pack(self.Data)
                    self.sock.sendto(SendData, (self.Host, self.Port)) 
                except:
                    #print "Send Server error"
                    pass
            self.InitAchse = 0

        return self.received