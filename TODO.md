### Todo

- proper README, change-log, and license
- package final product, version release
- tab-completion
- argparse
- sigterm handler
- detect os

- secure with AES w/ RSA
- registry persistence, maybe a small bat/vbs script too
- harvest credentials/token grabber
- updater
- uninstall

- status commands

- add exceptions class, safe_exec is gay
- send_command function

- remove stupid libraries

- help command

- use discord bot/webhooks as C2???

- use stager instead of a dropper

1. banner
2. prompt with colour and tab-completion
3. clean up helper.py
4. help command
5. replace all dmos.conn.send to dmos.send_packet

Anatomy:
1. Victim opens the stager (command line on unix systems and simple c++ binary on windows)
2. stager connects to C2 --> C2 sends stage --> stager writes and executes recieved stage --> stager self deletes


Commands:
- process list
- process migration
- screenshot 
- dl and execute powershell scripts
- gps