from colorama import Fore, Back, Style
import builtins
import sys
from datetime import datetime

class Debug():
    @staticmethod
    def _print(text):
        sys.stdout.write(text)
        sys.stdout.flush()

    @staticmethod
    def tprint(*objs, thread=False):
        prefix = "[{0}] ".format(str(datetime.now().time())[:8])
        __ = lambda _: "\n" if _==1 else ""
        Debug._print(__(thread) + Style.DIM + Fore.YELLOW + prefix + Style.RESET_ALL + " {}{}\n".format(Fore.BLUE, *objs))

    @staticmethod
    def eprint(*objs):
        prefix = "[⚠]"
        Debug._print("{}{}{} {}{}\n".format(Style.BRIGHT, Fore.RED, prefix, *objs, Style.RESET_ALL))

    @staticmethod
    def sprint(*objs, ANODE, APORT, thread=False):
        # server print
        prefix = Style.DIM + Fore.YELLOW + "[{0}] ".format(str(datetime.now().time())[:8]) + Style.RESET_ALL + Fore.YELLOW + f" <tcp://{ANODE}:{APORT}>"
        __ = lambda _: "\n" if _==1 else ""
        Debug._print(__(thread) + prefix + Style.RESET_ALL + " {}{}\n".format(Fore.BLUE, *objs))
