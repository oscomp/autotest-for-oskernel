import os
import time

import serial

from exception import CG
from utils import loge

image_name = 'img.kfpkg'
usb_port = '/dev/ttyUSB0'
image_flash_output = 'sdcard_flash.txt'
image_sdcard_write_output = 'sdcard_write.txt'


def prepare_sdcard(config):
    loge("\n[k210 autotest sdcard flash]: start to flash sdcard use image["+image_name+"] \n")

    testcase_input_src = os.path.join(config["testcase_dir"], "input")
    image_path = os.path.join(testcase_input_src, image_name)
    flash_tool_path = os.path.join(testcase_input_src, "ktool.py")

    image_flash_output_path = os.path.join(config['submit_dir'], image_flash_output)
    image_sdcard_write_output_path = os.path.join(config['submit_dir'], image_sdcard_write_output)
    
    # flash_sdcard_cmd = "kflash -b 3000000 -B dan -p /dev/ttyUSB0 " + image_path + " > " + image_flash_output_path
    flash_sdcard_cmd = "python3.7 " + flash_tool_path+" -b 3000000 -B dan -p /dev/ttyUSB0 " + image_path + " > " + image_flash_output_path
    loge(flash_sdcard_cmd)

    outf = open(image_sdcard_write_output_path, "w+")

    flash_sdcard = gg.exec(flash_sdcard_cmd)
    loge("\n[k210 autotest sdcard flash]: Get Serial Out {usb_port}\n")

    ss = serial.Serial(usb_port, 115200,
                       timeout=5,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.EIGHTBITS)

    if not ss.isOpen():
        loge("OPEN Serial fail")
        raise CG.UnknownError("OPEN Serial Fail when Flash Sdcard")

    start_time = time.time()
    while (True):
        cur_time = time.time()
        use_time = cur_time - start_time
        if use_time > 20:
            loge("Flash time too long")
            outf.write("Flash time too long")
            raise CG.UnknownError("Flash time too long")
            break
        data = ss.readline()
        try:
            data = data.decode()
        except UnicodeDecodeError:
            data = str(data)
        outf.write(str(data))
        outf.flush()
        if 'FINISH' in data:
            loge("\n[k210 autotest sdcard flash]: sdcard flash succeed\n")
            break

    outf.close()
    ss.close()
