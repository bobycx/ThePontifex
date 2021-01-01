from enum import Enum, auto

class PacketType(Enum):
    Command = auto()
    FileTransfer = auto()


