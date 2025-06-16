from WWWinch_codec import Codec
from WWWinch_sim_codec import SimCodec
from WWWinch_achsmemory import Achsmemory
import time
import socket
import argparse
from multiprocessing import shared_memory
import sys ,signal

MEM_NAME_GUI2HW = "achse_controler_to_hw"
MEM_NAME_HW2GUI = "achse_hw_to_controler"

should_exit = False

def handle_sigterm(signum, frame):
    global should_exit
    print("[Backend] Caught SIGTERM, setting exit flag.")
    should_exit = True

signal.signal(signal.SIGTERM, handle_sigterm)

ACHSEN     = {'Anton' : ("172.16.17.1", 15001,"172.16.17.5", 15001),
              'Burt'  : ("172.16.17.2", 15001,"172.16.17.5", 15002),
              'Cecil' : ("172.16.17.3", 15001,"172.16.17.5", 15003),
              'Debby' : ("172.16.17.4", 15001,"172.16.17.5", 15004),
              'Eugene': ("172.16.17.5", 15001,"172.16.17.5", 15005),
              'Fred'  : ("172.16.17.6", 15001,"172.16.17.5", 15006),
              'SIMUL' : ("127.0.0.1", 15001,"127.0.0.1", 15005)}


class backend_udp:
    """
    This class sends and receives properties of a axis.
    """

    def __init__(self, KontaktData='SIMUL'):

        self.GUI2HW  = Achsmemory(MEM_NAME_GUI2HW, wait=True)
        self.HW2GUI = Achsmemory(MEM_NAME_HW2GUI, wait=True)


        self.Host    = ACHSEN[KontaktData][0]
        self.Port    = ACHSEN[KontaktData][1]
        self.RecHost = ACHSEN[KontaktData][2]
        self.RecPort = ACHSEN[KontaktData][3] 

        self.recaddr = (self.RecHost,self.RecPort)

        self.receivedBuff = b"" 
        self.frame_count = 0

        if KontaktData == 'SIMUL':
            self.Backend_Codec = SimCodec()
            print(f"[Backend] Using SimCodec")
        else:
            self.Backend_Codec = Codec()        
            print(f"[Backend] Using Codec")
        
        self.Backend_Codec.SetProp.Name = KontaktData

        self._init_sockets()

        self.run()

    def run(self):
        global should_exit
        while not should_exit:
            try:
                #controler_in_data = self.GUI2HW.read()
                controler_in_data = self.GUI2HW.read_pending()

                self.Backend_Codec.unpack(controler_in_data)
                Data = self.Backend_Codec.pack(controler_in_data)
                #print(f"[Backend] Sending data: {Data}")

                self.send(Data)

                controler_out_data = self.receive()
                #print(f"[Backend] Received data: {controler_out_data}")

                frame_out = {
                    "SyncTag": 0xCAFEBABE,
                    "Frame": self.frame_count,
                    "Timestamp": time.time(),
                    **self.Backend_Codec.to_dict(controler_out_data)
                }
                # --- Perform write ---

                self.HW2GUI.write_confirmed(frame_out)
                self.frame_count += 1

                self.GUI2HW._mark_confirmed()

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
                self.recUDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                self.recUDPSock.settimeout(0.25)
            except socket.error as e:
                raise Exception(f"Socket error: {e}")
            try:
                self.recUDPSock.bind(self.recaddr)
            except socket.error as e:
                if e.errno == 10048:
                    pass
        else:
            self.sock       = None
            self.recUDPsock = None

    def send(self,Data):
        """
        Sends the properties of the axis.
        """
        if self.Host != "127.0.0.1":
            try:
                self.sock.sendto(Data, (self.Host, self.Port)) 
            except:
                pass
        else:
            # In simulation mode, store the last sent data for loopback
            self._sim_last_data = Data

    def receive(self):
        """
        Receives the properties.
        """
        if self.Host != "127.0.0.1":
            try:
                self.received,addr = self.recUDPSock.recvfrom(601)
                self.receivedBuff = self.received
            except socket.timeout:
                self.received = getattr(self, 'receivedBuff', None)
                if not self.received:
                    print("[Backend] Warning: No previous UDP data received — skipping this cycle.")
                    return None  # ← KEY CHANGE
            else:
                self.received = self.receivedBuff

            self.Backend_Codec.unpack(self.received)
        else:
            # In simulation mode, step the simulation and return the result
            if hasattr(self.Backend_Codec, 'step_sim'):
                self.received = self.Backend_Codec.step_sim()
            else:
                self.received = getattr(self, '_sim_last_data', None)

        return self.received


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--achse", type=str, default="SIMUL", help="Name of axis to control")
    args = parser.parse_args()

    backend_udp(KontaktData=args.achse)
