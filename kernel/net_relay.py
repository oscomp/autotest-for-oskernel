import os
import socket
import struct
import threading
import time
import binascii


GatewayAddr = ("192.168.101.70", 2000)


def calc_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

class ModbusRelay:
    def __init__(self, port, bus_addr=1):
        self.port = port
        self.bus_addr = bus_addr

    def _generate_command(self, cmd, reg, data):
        origin = struct.pack(">BBHH", self.bus_addr, cmd, reg, data)
        # crc = crc16xmodem(origin, 0xFFFF)
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


class FileLock:
    def __init__(self):
        self.path = "lock.pid"
        self.f = None

    def _lock(self, file):
        if os.name == 'nt':
            import win32con, win32file, pywintypes
            __overlapped = pywintypes.OVERLAPPED()
            hfile = win32file._get_osfhandle(file.fileno())
            win32file.LockFileEx(hfile, win32con.LOCKFILE_EXCLUSIVE_LOCK, 0, 0xffff0000, __overlapped)
        elif os.name == 'posix':
            import fcntl
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        else:
            raise RuntimeError("Unknown os")

    def _unlock(self, file):
        if os.name == 'nt':
            import win32con, win32file, pywintypes
            __overlapped = pywintypes.OVERLAPPED()
            hfile = win32file._get_osfhandle(file.fileno())
            win32file.UnlockFileEx(hfile, 0, 0xffff0000, __overlapped)
        elif os.name == 'posix':
            import fcntl
            fcntl.flock(file.fileno(), fcntl.LOCK_UN)
        else:
            raise RuntimeError("Unknown os")


    def lock(self):
        if not self.f:
            self.f = open(self.path, "w")
        self._lock(self.f)
        self.f.write(str(os.getpid()))

    def unlock(self):
        self._unlock(self.f)
        # self.f.close()
        # self.f = None


def test_thread():
    mutex = threading.Lock()
    def worker(w):
        sk = socket.socket()
        sk.connect(GatewayAddr)
        relay = ModbusRelay(sk)
        locker = FileLock()
        for i in range(100):
            locker.lock()
            relay.on(w)
            time.sleep(0.1)
            relay.off(w)
            locker.unlock()
            time.sleep(1)
        sk.close()

    threads = [threading.Thread(target=worker, args=(i, )) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def main():
    sk = socket.socket()
    sk.connect(GatewayAddr)
    relays = ModbusRelay(sk)
    for _ in range(100):
        for i in range(8):
            relays.on(i)
            time.sleep(1)
        for i in range(8):
            relays.off(i)
            time.sleep(1)

    sk.close()
    # print(binascii.hexlify(relays.on(2)))
    # print(binascii.hexlify(relays.off(2)))
    # print(binascii.hexlify(relays.get(2)))
    # print(binascii.hexlify(relays.blink(1, 20)))
    # print(binascii.hexlify(relays.flip(2)))


if __name__ == '__main__':
    test_thread()
