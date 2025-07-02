#!/usr/bin/python3
import json
import sys

import serial


def send_cmd(ss, num, cmd):
    ss.write(f"{num}{cmd}".encode())


def main():
    config_file = sys.argv[1]
    config = json.load(open(config_file))
    ss = serial.Serial(port=config['serial'], baudrate=115200)
    num = config['id']
    cmd = sys.argv[2]
    if cmd == "power_on":
        send_cmd(ss, num, "P")
    elif cmd == "power_off":
        send_cmd(ss, num, "p")
    elif cmd == "reset_on":
        send_cmd(ss, num, "R")
    elif cmd == "reset_off":
        send_cmd(ss, num, "r")
    elif cmd == "sd_connect_board":
        send_cmd(ss, num, "S")
    elif cmd == "sd_connect_host":
        send_cmd(ss, num, "s")
    else:
        print(f"Unknown command {cmd}")


if __name__ == '__main__':
    main()

