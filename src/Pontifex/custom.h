#pragma once
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#define _CRT_DEPRECATED_NO_WARNINGS

#pragma comment(lib, "ws2_32.lib")

#include <Winsock2.h>
#include <Windows.h>
#include <iostream>
#include <tchar.h>
#include <string>
#include <lmcons.h>
#include <iphlpapi.h>
#include <WS2tcpip.h>
#include <regex>
#include "x2struct/x2struct.hpp"
#include <stdio.h>
#include <stdlib.h>
#include "direct.h"
#include <fstream>
#include <nlohmann/json.hpp>
#include <sstream>
#include <io.h>
#include "PacketHandler.h"
#include "config.h"
#include <locationapi.h>