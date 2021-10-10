#pragma once
#include "PacketType.h"
#include <Windows.h>
#include <string>

class Packet {

public:
	PacketType packetType;
	int packetSize;
	std::string message;
	char* packetHashID;

	char* returnPacket() {
		packetSize = message.size() + 1;
		int size = packetSize + 20;
		char* buf = new char[size];
		std::string _packetType = std::to_string(static_cast<int>(packetType));
		std::string zero(4 - std::to_string(packetSize).length(), '0');
		std::string _packetSize = zero + std::to_string(packetSize);
		memcpy(buf, "9999", 4);
		memcpy(buf + 4, "0000", 4); // TODO
		memcpy(buf + (4 * 2), packetHashID, 8);
		memcpy(buf + (4 * 2) + 8, _packetSize.c_str(), 4);
		memcpy(buf + (4 * 3) + 8, message.c_str() + '\0', packetSize);
		return buf;
	}
};


