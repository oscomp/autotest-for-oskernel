import json
import shutil
import socket
import struct
import threading
import traceback

import serial
import time
import subprocess
import sys
import os

result = {}

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


def read_line(ss: serial.Serial):
    ans = bytearray()
    while True:
        c = ss.read()
        if len(c) == 0:
            break
        ans.append(c[0])
        if c[0] == ord('\r') or c[0] == ord('\n'):
            break
        if "Hit any key to stop autoboot".encode() in ans:
            break
    return bytes(ans)


def prepare_thread(ss, config):
    print("PREPARE")
    ss.write("\n\nprintenv\n".encode())
    time.sleep(5)
    if config['type'] == '2023_huashanpai':
        ss.write("mmc dev 1\n".encode())
        time.sleep(5)
    # ss.write("dhcp\n".encode())
    # time.sleep(2)
    ss.write("setenv serverip 192.168.100.1\n".encode())
    time.sleep(5)
    ss.write(f"setenv ipaddr {config['ip']}\n".encode())
    time.sleep(5)
    ss.write(f"mmc info\n".encode())
    time.sleep(5)
    if config['type'] == '2023_huashanpai':
        ss.write(f"bootp 0x80100000 sdcard.img\n".encode())
        time.sleep(30)
        ss.write(f"mmc write 0x80100000 0 8192\n".encode())
        time.sleep(30)
    else:
        ss.write(f"bootp 0x80300000 sdcard.img.gz\n".encode())
        time.sleep(30)
        ss.write(f"unzip 0x80300000 0x90000000 0x40000000\n".encode())
        time.sleep(30)
        ss.write(f"mmc write 0x90000000 0 8192\n".encode())
        time.sleep(30)
    if config['type'] == '2023_huashanpai' or config['type'] == '2023_starfive2':
        ss.write(f"ls mmc 1\n".encode())
    else:
        ss.write(f"ls mmc 0\n".encode())
    time.sleep(5)
    ss.write(f"bootp 0x80200000 {config['filename']}\n".encode())
    # time.sleep(5)
    # ss.write(f"bootp 0x80200000 {config['filename']}\n".encode())
    time.sleep(30)
    ss.write("go 0x80200000\n".encode())
    print("PREPARE FINISH")


def send_cmd(ss, num, cmd):
    ss.write(f"{num}{cmd}".encode())


def command(config, cmd):
    ss = serial.Serial(port=config['serial'], baudrate=115200)
    num = config['id']
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


config_list = {
    "s1": {
        "serial": "/dev/cg/star1port3",
        "type": "2023_starfive2",
        "filename": "s1.bin",
        "ip": "192.168.100.12"
    },
    "s2": {
        "serial": "/dev/cg/star1port1",
        "type": "2023_starfive2",
        "filename": "s2.bin",
        "ip": "192.168.100.13"
    },
    "s3": {
        "serial": "/dev/cg/star1port2",
        "type": "2023_starfive2",
        "filename": "s3.bin",
        "ip": "192.168.100.14"
    },
    "h1": {
        "serial": "/dev/cg/hsp1port3",
        "type": "2023_huashanpai",
        "filename": "h1.bin",
        "ip": "192.168.100.1"
    },
    "h2": {
        "serial": "/dev/cg/hsp1port1",
        "type": "2023_huashanpai",
        "filename": "h2.bin",
        "ip": "192.168.100.2"
    },
    "h3": {
        "serial": "/dev/cg/hsp1port2",
        "type": "2023_huashanpai",
        "filename": "h3.bin",
        "ip": "192.168.100.3"
    },
    "u1": {
        "serial": "/dev/cg/unmatched1",
        "type": "unmatched",
        "filename": "u1.bin",
        "ip": "192.168.100.50"
    },
    "u2": {
        "serial": "/dev/cg/unmatched2",
        "type": "unmatched",
        "filename": "u2.bin",
        "ip": "192.168.100.51"
    },
    "u3": {
        "serial": "/dev/cg/unmatched3",
        "type": "unmatched",
        "filename": "u3.bin",
        "ip": "192.168.100.52"
    },
}

def remote_switch(cmd):
    sk = socket.socket()
    sk.connect(("192.168.135.116", 9999))
    sk.send(cmd.encode())
    sk.close()


finish = False

def ssh_run(id):
    port_dir = arg.split('/')[-1]
    operator_config = config_list[id]
    config = config_list[id]
    on = lambda: remote_switch(id + "on")
    off = lambda: remote_switch(id + "off")

    off()

    os.system(f"mkdir -p /cg/{port_dir}")
    outf = open(f"/cg/{port_dir}/os_serial_out.txt", "w+", encoding='utf-8')

    # ---RUN---
    ss = serial.Serial(config['serial'], 115200,
                       timeout=40,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.EIGHTBITS)

    if not ss.isOpen():
        result['verdict'] = "SerialError"
        result['stderr'] = "OPEN Serial fail"
        result['return_code'] = 1
        return result

    # 准备启动文件
    tftp_dir = '/srv/tftp'
    target_path = os.path.join(tftp_dir, config_list[id]["filename"])
    print(f"copy os.bin to {target_path}", file=sys.stderr)
    shutil.copyfile(os.path.join("/cg/", id, "os.bin"), target_path)
    # 重启开发板
    time.sleep(5)
    on()

    start_time = time.time()

    in_prepare = True
    while not finish:
        if in_prepare:
            data = read_line(ss)
        else:
            data = ss.readline()
        try:
            data = data.decode()
        except UnicodeDecodeError:
            data = str(data)
        print(data, end='')
        sys.stdout.flush()
        if '!TEST FINISH!' in data:
            break
        if "### ERROR ### Please RESET the board ###" in data:
            break
        outf.write(str(data))
        outf.flush()

        if time.time() - start_time > 20 * 60:
            outf.write("\nTimeout.\n")
            outf.flush()
            break
        if in_prepare:
            if "Hit any key to stop autoboot" in data:
                ss.write("\n\n".encode())
                threading.Thread(target=prepare_thread, args=(ss, config)).start()
                in_prepare = False
            continue
        # #loge("[os autotest]"+str(use_time) + ' ss:',end =' ')
        # loge(str(data), end = '')

    outf.close()
    ss.close()
    off()

    return result

def timeout_watcher():
    start = time.time()
    while not finish:
        if time.time() - start > 20 * 60:
            sys.exit(0)
        time.sleep(1)


if __name__ == '__main__':
    arg = sys.argv[1]
    port = arg.split('/')[-1]

    threading.Thread(target=timeout_watcher).start()
    try:
        print(ssh_run(arg))
    except Exception as e:
        print(traceback.format_exc(), file=sys.stderr)
    finish = True
