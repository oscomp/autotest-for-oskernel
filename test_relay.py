import socket
import struct
import sys

import time


GatewayAddr = ("192.168.100.210", 2000)
# GatewayAddr = ("10.1.1.200", 2000)


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


class ModbusRelay:
    def __init__(self, bus_addr=1):
        sk = socket.socket()
        sk.connect(GatewayAddr)
        self.port = sk
        self.bus_addr = bus_addr

    def _generate_command(self, cmd, reg, data):
        origin = struct.pack(">BBHH", self.bus_addr, cmd, reg, data)
        crc = calc_crc(origin)
        return origin + crc.to_bytes(2, byteorder='little')

    def _send_recv(self, cmd, reg, data):
        cmd = self._generate_command(cmd, reg, data)
        self.port.send(cmd)
        response = self.port.recv(12)
        return response

    def on(self, relay):
        return self._send_recv(0x05, relay, 0xFF00)

    def off(self, relay):
        return self._send_recv(0x05, relay, 0x0000)

    def get(self, relay):
        return self._send_recv(0x01, relay, 0x0001)

    # 闪烁，单位为100ms
    def blink(self, relay, period):
        self.on(relay)
        time.sleep(period * 0.1)
        return self.off(relay)

    def flip(self, relay):
        return self._send_recv(0x05, relay, 0x5500)


if __name__ == '__main__':
    relay_num = int(sys.argv[1])
    bus_num = 1 if len(sys.argv) <= 2 else int(sys.argv[2])
    relay = ModbusRelay(bus_addr=bus_num)
    op = "blink" if len(sys.argv) <= 3 else sys.argv[3]

    if op == "on":
        relay.on(relay_num)
    elif op == "off":
        relay.off(relay_num)
    else:
        relay.blink(relay_num, 1)
