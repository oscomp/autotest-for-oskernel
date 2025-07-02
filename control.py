#!/usr/bin/python3
import os
import socket
import sys

if __name__ == '__main__':
    dev_id = os.environ.get("BOARD_ID")
    if len(sys.argv) <= 1:
        if dev_id:
            print(f"tftp prefix is {dev_id}")
        print(f"Usage: {sys.argv[0]} [on|off]")
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd != "on" and cmd != "off":
        print(f"Usage: {sys.argv[0]} [on|off]")
        sys.exit(0)

    allow_ids = ["s4", "s5", "s6", "s7", "s8", "s9"]
    if dev_id not in allow_ids:
        print(f"Unknown BOARD_ID")
        sys.exit(0)

    sk = socket.socket()
    sk.connect(("192.168.135.116", 9999))
    sk.send((dev_id + cmd).encode())
    sk.close()

