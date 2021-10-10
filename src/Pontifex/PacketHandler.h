#pragma once
#pragma once
#ifndef PACKETHANDLER_H
#define PACKETHANDLER_H

#include <Windows.h>
#include <string>
#include "PacketType.h"
#include "Packet.h"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class PacketHandler {
public:
	static bool _sendall(SOCKET sock, std::string data);
	static bool _recvall(SOCKET sock, int message_size, char* dataBuf);
	static bool sendPacket(SOCKET sock, PacketType packetType, json message, char* packetHashID);
	static bool recvPacket(SOCKET sock, char* dataBuf);
	static bool recv_INT(SOCKET sock, int& INT);
	static bool recv_PacketType(SOCKET sock, PacketType& packetType);
	static bool recvFileBuffer(SOCKET sock, uint32_t fileSize, FILE* fileHandle);
	static bool sendFileBuffer(SOCKET sock, FILE* fileHandle);
};



#endif