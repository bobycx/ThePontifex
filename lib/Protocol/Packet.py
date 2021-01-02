from .PacketType import PacketType
#from socket import htonl

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
    def __init__(self, packetType: PacketType, packetSize: int, message: bytes):
        self._packetType = packetType
        self._packetSize = packetSize
        self._message    = message
    
    def returnPacket(self) -> bytes: 
        buf = bytes()
        buf += self._packetType.value.to_bytes(4, 'big')
        buf += self._packetSize.to_bytes(4, 'big')
        buf += self._message
        return buf


