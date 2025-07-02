import shutil
import socket
import struct
import traceback

import serial
import time
import sys
import os
import filecmp


tftp_dir = '/srv/tftp'
sd_card_file = f"{tftp_dir}/sdcard.img.gz"
GatewayAddr = ("192.168.100.210", 2000)
lock_file = '/cg/lock.pid'

debug = False

class FileLock:
    def __init__(self):
        self.path = lock_file
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

lock = FileLock()

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
    def __init__(self):
        sk = socket.socket()
        sk.connect(GatewayAddr)
        self.port = sk

    def _generate_command(self, cmd, bus, reg, data):
        origin = struct.pack(">BBHH", bus, cmd, reg, data)
        crc = calc_crc(origin)
        return origin + crc.to_bytes(2, byteorder='little')

    def _send_recv(self, cmd, bus, reg, data):
        lock.lock()
        cmd = self._generate_command(cmd, bus, reg, data)
        # print("send ", cmd)
        self.port.send(cmd)
        response = self.port.recv(12)
        lock.unlock()
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




class Board:
    def __init__(self, usb_port, relay_number):
        self.usb_port = usb_port
        self.relay_number = relay_number


class PXE:
    def __init__(self, mac_addr, ip_addr, filename):
        self.mac_addr = mac_addr
        self.ip_addr = ip_addr
        self.filename = filename


board_list = {
    "0": Board("/dev/board_serial_0", 0),
    "1": Board("/dev/board_serial_1", 1),
    "2": Board("/dev/board_serial_2", 2),
    "3": Board("/dev/board_serial_3", 3),
    "4": Board("/dev/board_serial_4", 4),
}

dhcp_list = {
    "70:b3:d5:92:f6:d3": PXE("70:b3:d5:92:f6:d3", "10.1.1.15", "os_1.bin"),
    "70:b3:d5:92:fa:27": PXE("70:b3:d5:92:fa:27", "10.1.1.19", "os_5.bin"),
    "70:b3:d5:92:fa:14": PXE("70:b3:d5:92:fa:14", "10.1.1.18", "os_4.bin"),
    "70:b3:d5:92:fa:2b": PXE("70:b3:d5:92:fa:2b", "10.1.1.17", "os_3.bin"),
    "70:b3:d5:92:f6:d9": PXE("70:b3:d5:92:f6:d9", "10.1.1.16", "os_2.bin"),
}


def try_get_mac(ss):
    # 查找MAC这块开发板的MAC地址
    t = time.time()
    while True:
        data = ss.readline()
        if time.time() - t > 10:
            return ""
        try:
            data = data.decode()
        except UnicodeDecodeError:
            data = str(data)
        if "Ethernet MAC address" in data:
            # Ethernet MAC address: 70:b3:d5:92:fa:27
            return data[data.find(':') + 2:].strip()


def ssh_run(dev_number):
    port_dir = f"/cg/{dev_number}"
    board = board_list[dev_number]
    result = {}

    # 打开串口
    print(f"open {board.usb_port}", file=sys.stderr)
    ss = serial.Serial(board.usb_port, 115200,
                       timeout=40,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.EIGHTBITS)
    if not ss.isOpen():
        result['verdict'] = "SerialError"
        result['stderr'] = "OPEN Serial fail"
        result['return_code'] = 1
        return result
    relay_controller = ModbusRelay()

    relay_controller.blink(2, board.relay_number, 40)
    time.sleep(2)
    relay_controller.blink(2, board.relay_number, 10)

    # 复位开发板
    # lock.lock()
    # relay_controller.blink(board.relay_number, 1)
    # lock.unlock()

    mac = try_get_mac(ss)
    if not mac:
        relay_controller.blink(2, board.relay_number, 10)
        mac = try_get_mac(ss)
    if not mac:
        print("reset fail, try to power up", file=sys.stderr)
        result['verdict'] = "BoardError"
        result['stderr'] = f"cannot get address of board {dev_number}"
        result['return_code'] = 1
        return result
    print(f"get Mac address: {mac}", file=sys.stderr)
    dhcp = dhcp_list[mac]
    target_path = os.path.join(tftp_dir, dhcp.filename)
    print(f"copy os.bin to {target_path}", file=sys.stderr)
    shutil.copyfile(os.path.join(port_dir, "os.bin"), target_path)

    # 复位开发板
    relay_controller.blink(1, board.relay_number, 1)

    outf = open(f"/cg/{dev_number}/os_serial_out.txt", "w+", encoding='utf-8')
    start_time = time.time()
    while True:
        # cur_time = time.time()
        # use_time = cur_time - time_start
        data = ss.readline(1024)
        try:
            data = data.decode()
        except UnicodeDecodeError:
            data = str(data)
        # #loge("[k210 autotest]"+str(use_time) + ' ss:',end =' ')
        # loge(str(data), end = '')
        # if len(data) == 0:
        #     break
        if '!TEST FINISH!' in data:
            break
        if debug:
            print(str(data), file=sys.stderr, end='')
        outf.write(str(data))
        outf.flush()
        if time.time() - start_time > 1 * 60:
            outf.write("\nTimeout.\n")
            outf.flush()
            break
    outf.close()
    ss.close()

    if debug:
        print("quit reading", file=sys.stderr)

    # power off after run.
    relay_controller.blink(2, board.relay_number, 40)
    return result


if __name__ == '__main__':
    arg = sys.argv[1]
    if len(sys.argv) == 3:
        debug = True
    try:
        print(ssh_run(arg))
    except Exception as e:
        print(traceback.format_exc(), file=sys.stderr)
