from __future__ import print_function
import sys, argparse

## windows readline support 
try:
  import readline
except ImportError:
  import pyreadline as readline

if not (sys.version_info.major == 3 and sys.version_info.minor >= 8):
    print("This tool requires python 3.8 or above.")
    sys.exit(0)

from lib.control import Control

def configure_tab_completion():
    if sys.platform == 'darwin':
        readline.parse_and_bind("bind -e")
        readline.parse_and_bind("bind '\t' rl_complete")
    else:
        readline.parse_and_bind('tab: complete')
        readline.set_completer_delims(' \t\n`~!@#$%^&*()-=+[{]}\\|;:\'",<>?')

def arguement_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("LHOST", help="Local address; type 0.0.0.0 if you're unsure.", type=str)
    parser.add_argument("LPORT", help="Local port for the Pontifex to listen on.", type=int)
    parser.add_argument("--testing", help="Toggle testing; devs only.")
    return parser.parse_args()

def pontifex(argslist):
    ptfx_control = Control(argslist.LHOST, argslist.LPORT)
    ptfx_control.start_multi_handler()

if __name__ == "__main__":
    try:
        configure_tab_completion()
        pontifex(arguement_parser())
    except (KeyboardInterrupt, SystemExit):
        pass


