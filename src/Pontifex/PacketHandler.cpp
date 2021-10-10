#include "PacketHandler.h"
#include <iostream>

bool PacketHandler::_sendall(SOCKET sock, std::string data) {
	int bytes_sent = 0;
	int data_size = data.length() + 1;
	std::cout << data_size << std::endl;
	while (bytes_sent < data_size) {
		int retCode = send(sock, data.c_str(), data_size - bytes_sent, 0);
		if (retCode == SOCKET_ERROR) {
			return false;
		}
		bytes_sent += retCode;
	}

	return true;
}

bool PacketHandler::_recvall(SOCKET sock, int message_size, char* dataBuf) {
	int bytes_recieved = 0;
	while (bytes_recieved < message_size) {
		int retCode = recv(sock, dataBuf, message_size - bytes_recieved, 0);
		if (retCode == SOCKET_ERROR) {
			return false;
		}
		bytes_recieved += retCode;
	}

	return true;
}

bool PacketHandler::sendPacket(SOCKET sock, PacketType packetType, json message, char* packetHashID) {
	Packet pkt;
	pkt.packetType = packetType;
	pkt.packetHashID = packetHashID;
	//pkt.packetSize = packetSize;
	pkt.message = message.dump();
	std::cout << message.dump().size() << std::endl;
	std::string result = pkt.returnPacket();
	std::cout << result << std::endl;
	std::cout << result.length() << std::endl;
	std::cout << sizeof(result) << std::endl;
	return _sendall(sock, pkt.returnPacket());
}

bool PacketHandler::recvPacket(SOCKET sock, char* dataBuf) {
	int payloadSize;
	if (recv_INT(sock, payloadSize)) {
		_recvall(sock, payloadSize, dataBuf);
	}

	return true;
}

bool PacketHandler::recv_INT(SOCKET sock, int &INT) {
	char charBuf[4];
	int retCode = recv(sock, charBuf, sizeof(charBuf), 0);
	if (retCode == SOCKET_ERROR) {
		return false;
	}
	//std::cout << charBuf << std::endl;
	INT = atoi(charBuf);

	ZeroMemory(charBuf, 4);
	return true;
}

bool PacketHandler::recv_PacketType(SOCKET sock, PacketType& packetType) {
	int magicNum;
	int packetTypeINT;
	if (recv_INT(sock, magicNum)) {
		if (magicNum == 9999) {
			if (recv_INT(sock, packetTypeINT)) {
				packetType = static_cast<PacketType>(packetTypeINT - 1); // minus 1 because python enum index starts at 1 not 0 (big gae)
			}
			
		}
		else {
			return false;
		}
		
	} 

	return true;
}


bool PacketHandler::recvFileBuffer(SOCKET sock, uint32_t fileSize,  FILE* fileHandle) {
	int bytes_recieved = 0;
	char fileBuffer[1024] = { 0 };
	while (bytes_recieved < fileSize) {
		int retCode = recv(sock, fileBuffer, 1024, 0);
		if (retCode == SOCKET_ERROR) {
			return false;
		}
		fwrite(fileBuffer, sizeof(char), sizeof(fileBuffer), fileHandle);
		ZeroMemory(fileBuffer, sizeof(fileBuffer));
		bytes_recieved += retCode;
	}

	return true;
}

bool PacketHandler::sendFileBuffer(SOCKET sock, FILE* fileHandle) {
	char buffer[1024] = { 0 };   //Buffer
	int nCount;
	while ((nCount = fread(buffer, 1, 1024, fileHandle)) > 0) {
		send(sock, buffer, nCount, 0);
	}

	return true;
}
