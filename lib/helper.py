import sys, os, traceback
import pyfiglet
from datetime import datetime
from termcolor import colored
from lib.debug import Debug
from prompt_toolkit.styles import Style

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

def _input():
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
        Debug.tprint("Connection with dmos {} has been broken".format(dmos.md5_hash))

def banner():

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
