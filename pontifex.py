from __future__ import print_function
import sys, argparse,  threading, time

if not (sys.version_info.major == 3 and sys.version_info.minor >= 8):
    print("This tool requires python 3.8 or above.")
    sys.exit(0)

from lib.control import Control

def arguement_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("LHOST", help="Local address; type 0.0.0.0 if you're unsure.", type=str)
    parser.add_argument("LPORT", help="Local port for the Pontifex to listen on.", type=int)
    parser.add_argument("--travis", help="Toggle testing; devs only.")
    return parser.parse_args()

def pontifex(argslist):
    try:
        ptfx_control = Control(argslist.LHOST, argslist.LPORT)
        ptfx_control.start_multi_handler()
    except Exception as e:
        print(e)
        ptfx_control.terminate_server()


if __name__ == "__main__":
    #configure_tab_completion()
    pontifex(arguement_parser())
    
        


