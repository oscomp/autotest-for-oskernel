import socket
import struct
import threading  # 导入线程模块
import time

import serial

lock = threading.Lock()
GatewayAddr = ("192.168.100.210", 2000)


def calc_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc


relay_lock = threading.Lock()
class ModbusRelay:
    def __init__(self):
        sk = socket.socket()
        sk.connect(GatewayAddr)
        self.port = sk

    def _generate_command(self, cmd, bus, reg, data):
        origin = struct.pack(">BBHH", bus, cmd, reg, data)
        crc = calc_crc(origin)
        return origin + crc.to_bytes(2, byteorder='little')

    def _send_recv(self, cmd, bus, reg, data):
        relay_lock.acquire()
        cmd = self._generate_command(cmd, bus, reg, data)
        # print("send ", cmd)
        self.port.send(cmd)
        response = self.port.recv(12)
        relay_lock.release()
        return response

    def on(self, bus, relay):
        return self._send_recv(0x05, bus, relay, 0xFF00)

    def off(self, bus, relay):
        return self._send_recv(0x05, bus, relay, 0x0000)

    def get(self, bus, relay):
        return self._send_recv(0x01, bus, relay, 0x0001)

    # 闪烁，单位为100ms
    def blink(self, bus, relay, period):
        self.on(bus, relay)
        time.sleep(period * 0.1)
        return self.off(bus, relay)

    def flip(self, bus, relay):
        return self._send_recv(0x05, bus, relay, 0x5500)

def send_serial(port, cmd):
    lock.acquire()
    try:
        ss = serial.Serial(port="/dev/cg/" + port, baudrate=115200)
        ss.write((cmd + "\n").encode())
        ans = ss.readline()
        print(f"send {cmd} to /dev/cg/{port}, ans {ans}")
        ss.close()
    except Exception as e:
        raise e
    finally:
        lock.release()


def link_handler(link: socket, client):
    """
    该函数为线程需要执行的函数，负责具体的服务器和客户端之间的通信工作
    :param link: 当前线程处理的连接
    :param client: 客户端ip和端口信息，一个二元元组
    :return: None
    """
    print("服务器开始接收来自[%s:%s]的请求...." % (client[0], client[1]))
    running = True
    while running:  # 利用一个死循环，保持和客户端的通信状态
        client_data = link.recv(1024).decode()
        cmds = client_data.split("\n")
        for cmd in cmds:
            cmd = cmd.strip()
            if cmd == "":
                continue
            if cmd == "exit":
                running = False
                break
            elif cmd == "s1on":
                send_serial("star1ctl", "1p")
            elif cmd == "s1off":
                send_serial("star1ctl", "1P")
            elif cmd == "s2on":
                send_serial("star1ctl", "2p")
            elif cmd == "s2off":
                send_serial("star1ctl", "2P")
            elif cmd == "s3on":
                send_serial("star1ctl", "3p")
            elif cmd == "s3off":
                send_serial("star1ctl", "3P")
            elif cmd == "s4on":
                send_serial("star2ctl", "1p")
            elif cmd == "s4off":
                send_serial("star2ctl", "1P")
            elif cmd == "s5on":
                send_serial("star2ctl", "2p")
            elif cmd == "s5off":
                send_serial("star2ctl", "2P")
            elif cmd == "s6on":
                send_serial("star2ctl", "3p")
            elif cmd == "s6off":
                send_serial("star2ctl", "3P")
            elif cmd == "s7on":
                send_serial("star3ctl", "1p")
            elif cmd == "s7off":
                send_serial("star3ctl", "1P")
            elif cmd == "s8on":
                send_serial("star3ctl", "2p")
            elif cmd == "s8off":
                send_serial("star3ctl", "2P")
            elif cmd == "s9on":
                send_serial("star3ctl", "3p")
            elif cmd == "s9off":
                send_serial("star3ctl", "3P")
            elif cmd == "h1on":
                send_serial("hsp1ctl", "1p")
            elif cmd == "h1off":
                send_serial("hsp1ctl", "1P")
            elif cmd == "h2on":
                send_serial("hsp1ctl", "2p")
            elif cmd == "h2off":
                send_serial("hsp1ctl", "2P")
            elif cmd == "h3on":
                send_serial("hsp1ctl", "3p")
            elif cmd == "h3off":
                send_serial("hsp1ctl", "3P")
            elif cmd == "u1on":
                ModbusRelay().blink(2, 0, 4)
                ModbusRelay().blink(2, 0, 1)
            elif cmd == "u1off":
                ModbusRelay().blink(2, 0, 4)
            elif cmd == "u2on":
                ModbusRelay().blink(2, 1, 4)
                ModbusRelay().blink(2, 1, 1)
            elif cmd == "u2off":
                ModbusRelay().blink(2, 1, 4)
            elif cmd == "u3on":
                ModbusRelay().blink(2, 2, 4)
                ModbusRelay().blink(2, 2, 1)
            elif cmd == "u3off":
                ModbusRelay().blink(2, 2, 4)

    print("结束与[%s:%s]的通信..." % (client[0], client[1]))
    link.close()


ip_port = ('0.0.0.0', 9999)
sk = socket.socket()  # 创建套接字
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk.bind(ip_port)  # 绑定服务地址
sk.listen(20)  # 监听连接请求

print('启动socket服务，等待客户端连接...')

while True:  # 一个死循环，不断的接受客户端发来的连接请求
    conn, address = sk.accept()  # 等待连接，此处自动阻塞
    # 每当有新的连接过来，自动创建一个新的线程，
    # 并将连接对象和访问者的ip信息作为参数传递给线程的执行函数
    t = threading.Thread(target=link_handler, args=(conn, address))
    t.start()
