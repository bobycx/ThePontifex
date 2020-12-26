import builtins
import sys
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Colours:
    RED             = '\x1b[38;2;255;0;0m'
    CYAN            = '\x1b[38;2;0;255;251m'
    GREEN           = '\x1b[38;2;0;255;0m'
    BLUE            = '\x1b[38;2;36;114;200m'
    YELLOW_DIM      = '\x1b[38;2;220;220;220m'
    RESET           = '\x1b[0m'

palette = Colours()

class Debug():
    @staticmethod
    def prompt_input(*objs):
        return input("{}{}{}".format(palette.CYAN, *objs, palette.RESET)).rstrip(' ')

    @staticmethod
    def _print(text):
        sys.stdout.write(text)
        sys.stdout.flush()

    @staticmethod
    def tprint(*objs, thread=False):
        prefix = "[{0}] ".format(str(datetime.now().time())[:8])
        __ = lambda _: "\n" if _==1 else ""
        Debug._print(__(thread) + palette.YELLOW_DIM + prefix + palette.RESET + " {}{}{}\n".format(palette.BLUE, *objs, palette.RESET))

    @staticmethod
    def eprint(*objs):
        prefix = "[-]"
        Debug._print("{}{} {}{}\n".format(palette.RED, prefix, *objs, palette.RESET))

    @staticmethod
    def sprint(*objs, ANODE, APORT, thread=False):
        # server print
        prefix = palette.YELLOW_DIM + "[{0}] ".format(str(datetime.now().time())[:8]) + palette.RESET + palette.YELLOW_DIM + f" <tcp://{ANODE}:{APORT}>"
        __ = lambda _: "\n" if _==1 else ""
        Debug._print(__(thread) + prefix + Colours.RESET + " {}{}\n".format(palette.BLUE, *objs))
