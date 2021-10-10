import sys, os, traceback
from lib.debug import Debug, log, palette
from datetime import datetime



SUCCESS_CODE    = "SUCCESS"
ERROR_CODE      = "ERROR"
WINDOWS         = sys.platform.startswith('win')
CMD_CLEAR       = "cls" if WINDOWS else "clear"

def getTime(file=False):
    dtCurrentTime = datetime.now()
    if file == False:
        return dtCurrentTime.strftime("%Y/%m/%d %H:%M:%S")
    else:
        return dtCurrentTime.strftime("%Y-%m-%d at %H.%M.%S")

def safe_exec(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            Debug.eprint(f"<{func.__name__}> {e}")
            traceback.print_exc()
    return inner_function

def safe_socket(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionBroken:
            raise ConnectionBroken
    return inner_function

def banner():
    print(r"""
 _______ _           ______                 _    ___
(_______) |         (_____ \            _  (_)  / __)
    _   | |__  _____ _____) )__  ____ _| |_ _ _| |__ _____ _   _
   | |  |  _ \| ___ |  ____/ _ \|  _ (_   _) (_   __) ___ ( \ / )
   | |  | | | | ____| |   | |_| | | | || |_| | | |  | ____|) X (
   |_|  |_| |_|_____)_|    \___/|_| |_| \__)_| |_|  |_____|_/ \_) {}v1.0 

             λ Cross-platform RAT created by {}@kryptosr {}λ
    
    """.format("\033[1m", "\033[31m", "\033[37m"))

def banner_old():
    
    print(r"""
                _|_             Welcome to the Cathedral
                 |          [   {2}The Pontifex version 0.1.3{1}                                                                ]
                / \    *    [   {0}Disclaimer{1}: this project has no religious intent, if you know the reference, you know ;)  ]
                | |         [   {0}Creator{1}: Kryptosr                                                                         ]
        *      //_\\        [   {0}Hobby{1}: Making secc width doritos                                                          ]
              //(_)\\
               |/^\|      *
            *  ||_||
    *          // \\
              //   \\         *
             // === \\  *
        *   // =-=-= \\
           //   ===   \\   *
    *     //|         |\\
            |         |
            |  __ __  |   *
        *   | |  |  | |
            | | -|- | |        *
            |_|__|__|_|
*          /`  =======`\
        /`    =======    `\
                """.format('\033[31m', '\033[00m', '\033[93m'))

class ConnectionBroken(Exception):
    pass