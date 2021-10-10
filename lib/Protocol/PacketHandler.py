from lib.Protocol.PacketType import PacketType
from lib.Protocol.Packet import Packet
from lib.debug import log
from lib.helper import ConnectionBroken, safe_socket
from secrets import token_hex 


class PacketHandler:
    def __init__(self, conn):
        self.conn = conn
        self.magicNum = 9999
    
    def _send(self, data):
        try:
            return self.conn.send(data)
        except:
            raise ConnectionBroken

    def _recv(self, size):
        try:
            return self.conn.recv(size)
        except:
            raise ConnectionBroken

    def _sendall(self, data) -> bool:
        bytes_sent = 0
        data_size = len(data)
        while bytes_sent < data_size:
            bytes_sent += self._send(data)
    
        return True

    def _recvall(self, message_size) -> bytes:
        bytes_recieved = 0
        data = bytes()
        while bytes_recieved < message_size:
            recv_size = message_size - bytes_recieved
            data += self._recv(recv_size)
            if not data:
                return False
                #raise Exception()
            bytes_recieved += recv_size
        
        return data

    @safe_socket
    def sendPacket(self, packetType, message):
        packetHashID = token_hex(nbytes=4)
        pBuf = Packet(packetType, message, packetHashID).returnPacket()
        #log.debug(pBuf)
        if self._sendall(pBuf):
            return packetHashID
        
    
    @safe_socket
    def recvPacket(self, packetType, packetHashID) -> bytes:
        if self.recv_PacketType() == packetType:
            hash = self._recv(8).decode()
            if hash == packetHashID:
                packetSize = self.recv_INT() + 1
                return self._recvall(packetSize)

    def recv_PacketType(self) -> PacketType:
        if int(self._recv(4)) == 9999:
            packetTypeIndex = int(self._recv(4).decode()[0]) + 1
            return PacketType(packetTypeIndex)
    
    def recv_INT(self) -> int:
        dataSize = int(self._recv(4))
        return dataSize

    def recvFileBuffer(self, fileSize):
        bytes_recieved = 0
        data = bytes()
        while bytes_recieved < fileSize:
            data += self._recv(1024)
            if not data:
                return False
                #raise Exception()
            bytes_recieved += 1024
        
        return data
    
    def sendFileBuffer(self, fileBuffer, fileBufferSize) -> bool:
        pass