from Protocol.PacketType import PacketType

class PacketHandler:
    def _sendall(self, data) -> bool:
        int bytes_sent = 0
        data_size = len(data)
        while bytes_sent < data_size:
            send_size = data_size - bytes_sent
            data += self.conn.send(send_size)
            if not data:
                return False
                #raise Exception()
            bytes_sent += send_size
    
        return True

    def _recvall(self, message_size) -> bytes:
        int bytes_recieved = 0
        data = bytes()
        while bytes_recieved < message_size:
            recv_size = message_size - bytes_recieved
            data += self.conn.recv(recv_size)
            if not data:
                return False
                #raise Exception()
            bytes_recieved += recv_size
        
        return data

    def sendPacket(self, packetType, packetSize, message) -> bool:
        p = Packet(packetType, packetSize, message)
        return self._sendall(p.returnPacket()):
        
    def recvPacket(self, packetType) -> bytes:
        if self.recv_PacketType() == packetType:
            packetSize = self.recv_UINT32()
            return self._recvall(packetSize)

    def recv_PacketType(self) -> PacketType:
        packetTypeIndex = self.conn.recv(5) 
        return PacketType(packetTypeIndex.from_bytes(4, 'big'))
    
    def recv_UINT32(self) -> int:
        uint32 = self.conn.recv(5)
        return uint32.from_bytes(4, 'big')

    def recvFileBuffer(self, fileSize):
        int bytes_recieved = 0
        data = bytes()
        while bytes_recieved < fileSize:
            data += self.conn.recv(1024)
            if not data:
                return False
                #raise Exception()
            bytes_recieved += recv_size
        
        return data
    
    def sendFileBuffer(self, fileBuffer, fileBufferSize) -> bool:
         