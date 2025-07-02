import socket
import threading


def print_thread(s):
    while True:
        print(s.recv().decode(), end='')


def main():
    s = socket.socket()
    s.connect(("192.168.0.103", 2000))
    t = threading.Thread(target=print_thread, args=(s,))
    t.start()
    while True:
        text = input()
        s.send(text.encode())


if __name__ == '__main__':
    main()
