import threading

import serial
import os


running = True


def read_line(ss: serial.Serial):
    ans = bytearray()
    while running:
        c = ss.read()
        if len(c) == 0:
            continue
        if c[0] == ord('\r') or c[0] == ord('\n'):
            break
        ans.append(c[0])
    return bytes(ans)


def read_serial(port):
    sock = serial.Serial(port, 115200, timeout=1)
    print(f"{port}:  open!")
    while running:
        line = read_line(sock).decode()
        if line == "":
            continue
        print(f"{port}:  {line}")
    print(f"{port}:  close!")
    sock.close()


def main():
    path = os.listdir("/dev/cg")
    for p in path:
        if "ctl" not in p:
            threading.Thread(target=read_serial, args=(os.path.join("/dev/cg/", p),)).start()


if __name__ == '__main__':
    main()
    input()
    running = False
