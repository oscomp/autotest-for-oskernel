import time

import pytz

from pygrading import *
from exception import CG
from utils import loge, console_log
from datetime import datetime

import pygrading as gg
import os
import subprocess



@CG.catch
def prework(job: Job):
    with open("/mnt/cghook/cancel_purge", "w") as f:
        f.write("pkill qemu-system-riscv64\n")
        f.write("pkill qemu-system-loongarch64\n")
    job.add_log(str(datetime.now(tz=pytz.timezone("Asia/Shanghai"))), "START TIME")
    config = job.get_config()
    # need to be done when run in platform
    # config['submit_dir'] = os.path.join(config['submit_dir'], os.listdir(config['submit_dir'])[0])

#     check_result = subprocess.run("tar xavf /cg/STCheck.tar.gz -C /tmp", shell=True,
#                                     stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#     check_result = subprocess.run("/tmp/STCheck/RunTest.sh", shell=True,
#                                     cwd='/tmp/STCheck',
#                                     stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#
    if len(os.listdir(config['submit_dir'])) == 0:
        raise CG.CompileError("No submit file")

    forbidden_files = ["os_flash_out.txt", "os_serial_out.txt", "sdcard_write.txt", "sdcard_flash.txt", "os.bin"]
    for file in os.listdir(config['submit_dir']):
        if file in forbidden_files:
            raise CG.CompileError(f"You cannot submit a {file}")

    # start compile
    loge("\n[os autotest]: Compile Start\n")

    # execute make command
    loge("\n[os autotest]: call make to compile\n")
    os.system("mkdir -p /mnt/cghook")
    f = open("/mnt/cghook/console_log", "w")
    f.write("正在编译\n")
    f.flush()
    compile_result = subprocess.run("make all", shell=True,
                                    cwd=config['submit_dir'],
                                    stderr=f, stdout=f)
    f.close()
    job.add_log_detail(str(config), "CONFIG")
    job.add_log(open("/mnt/cghook/console_log", errors='ignore').read(), "编译输出")
    open("/mnt/cghook/console_log", "w").close()

    # has_sbi = os.path.exists(os.path.join(config['submit_dir'], 'sbi-rv'))

    config['sbi_file'] = 'default'

    if compile_result.returncode != 0:
        raise CG.CompileError("编译出错")

    console_log("编译完成")

    def logexec(cmd):
        # print("cmd" + cmd)
        job.add_log_detail(cmd, "cmd")
        loge("[os autotest]:" + cmd)
        start_time = time.time()
        res = gg.exec(cmd)
        job.add_log_detail(f"STDOUT:\n{res.stdout}\nSTDERR:{res.stderr}\nTIME:{datetime.now()}\nDURATION:{time.time() - start_time}", cmd)
        if res.returncode != 0:
            raise RuntimeError(f"run command error {cmd} \n{res.stdout}\n{res.stderr}")
        return res

    loge("[os autotest]: Compile Succeed")

    testcases = TestCases()
    testcases.append("TestCase 1", 100, "", "")
    job.set_testcases(testcases)
