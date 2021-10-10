from .PacketType import PacketType
from socket import htonl, ntohl
import json

class Packet:
    """
    Packet struct//
    first 4 bytes = packetType: PacketType
    next 4 bytes = packetSize: int
    remaining bytes = message: str

    Example usage//
        pkt = Packet(PacketType.Message, 1024, b'hello')
        sock.send(pkt.returnPacket())

    """
    def __init__(self, packetType: PacketType, message: dict, hash: str):
        self._packetType = packetType
        self._message    = json.dumps(message).encode()
        self._packetSize = len(self._message) + 1 # add terminating string character: '\0'
        self._hash       = hash.encode()
        
    
    def returnPacket(self) -> bytes: 
        buf = bytes()
        buf += str(9999).encode()
        buf += b'0' * (4 - len(str(self._packetType.value))) + str(self._packetType.value).encode()
        buf += self._hash + b'\0'
        buf += b'0' * (4 - len(str(self._packetSize))) + str(self._packetSize).encode()
        buf += self._message + b'\0'
        return buf


