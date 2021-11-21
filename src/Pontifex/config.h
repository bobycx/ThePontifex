#pragma once
#ifndef CONFIG_H
#define CONFIG_H

#include <string>

class Config {
public:
	static std::string szHost;
	static int szPort;

	static std::string selfPath;
	static bool hasPersistence;
	static bool isAdmin;

};


#endif