import subprocess
import threading
import os
import time

import select

import pygrading as gg
from utils import console_log

error = None
process = None


def run_qemu_thread(job, sbi, os_file, fs, out):
    global error
    global process
    gg.exec(f"cp {fs} initrd.img")
    cmd = f"qemu-system-riscv64 -machine virt -kernel {os_file} -m 128M -nographic -smp 2 -bios {sbi} -drive file={fs},if=none,format=raw,id=x0 -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 -serial file:{out} -initrd initrd.img"
    job.add_log(cmd, "QEMU CMD")
    # cmd = f"qemu-system-riscv64 -machine virt -bios {os} -m 8M -nographic -smp 2 -drive file={fs},if=none,format=raw,id=x0 -serial file:{out}"
    try:
        process = gg.exec(cmd)
        # process = subprocess.Popen(args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # process.wait(120)
    except subprocess.TimeoutExpired as e:
        error = e
    except subprocess.CalledProcessError as e:
        error = e


def run_qemu1(job, sbi, os_file, fs, out):
    subprocess.check_output("gzip -d sdcard.img.gz", shell=True)
    thread = threading.Thread(target=run_qemu_thread, args=(job, sbi, os_file, fs, out))
    thread.start()
    time.sleep(3)
    if not os.path.exists(out):
        with open(out, "w") as f:
            f.write("FAIL to run QEMU")
            return
    last_change_time = time.time()
    last_size = os.path.getsize(out)
    global error
    while error is None:
        cur_time = time.time()
        cur_size = os.path.getsize(out)
        if cur_size != last_size:
            last_change_time = cur_time
            last_size = cur_size
        else:
            if cur_time - last_change_time > 10:
                break
    return error, process


def run_qemu(job, sbi, os_file, fs, out):
    subprocess.check_output("gzip -d sdcard-rv.img.gz", shell=True)
    config = job.get_config()
    smp = config.get('smp', 1)
    mem = config.get('mem', '1G')
    timeout = config.get('qemu.timeout', 60)
    cmd = (f"qemu-system-riscv64 -machine virt -kernel {os_file} -m {mem} -nographic -smp {smp} -bios default -drive file={fs},if=none,format=raw,id=x0  "
           f"-device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 -no-reboot -device virtio-net-device,netdev=net -netdev user,id=net  "
           f"-rtc base=utc")
    cmd = (f"qemu-system-riscv64 -machine virt -kernel {os_file} -m {mem} -nographic -smp {smp} -bios default -drive file={fs},if=none,format=raw,id=x0 "
            "-device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 -no-reboot -device virtio-net-device,netdev=net -netdev user,id=net "
            "-rtc base=utc ")
    if os.path.exists(os.path.join(os.getcwd(), "disk.img")):
        os.system("cp disk.img disk-rv.img")
        cmd += " -drive file=disk-rv.img,if=none,format=raw,id=x1 -device virtio-blk-device,drive=x1,bus=virtio-mmio-bus.1"
    job.add_log(cmd, "QEMU CMD")
    console_log("运行：" + cmd)

    with open(out, "w", errors='ignore', buffering=1) as f, \
         open("/mnt/cghook/console_log", "a", errors='ignore', buffering=1) as hook_f:
        f.write(cmd)
        f.write("\n")
        f.flush()
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            shell=True,
            text=True,
            bufsize=1,
        )

        # Thread to read stdout in real-time
        timeout_occurred = threading.Event()

        def read_output():
            try:
                for line in p.stdout:
                    if timeout_occurred.is_set():
                        break
                    f.write(line)
                    f.flush()
                    hook_f.write("qemu-system-riscv:" + line)
                    hook_f.flush()
            except:
                pass

        reader_thread = threading.Thread(target=read_output)
        reader_thread.daemon = True
        reader_thread.start()

        try:
            p.stdin.write("\n")
            p.stdin.flush()
            p.stdin.close()
            p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timeout_occurred.set()
            p.kill()
            p.wait()

        # Wait for reader thread to finish (with a short timeout)
        reader_thread.join(timeout=1)

    return error, process


def run_qemu_loong(job, sbi, os_file, fs, out):
    config = job.get_config()
    subprocess.run("gzip -df sdcard-la.img.gz", shell=True)
    smp = config.get('qemu.smp', 1)
    mem = config.get('qemu.mem', '1G')
    timeout = config.get('qemu.timeout', 60)
    cmd = (f"qemu-system-loongarch64 -kernel {os_file} -m {mem} -nographic -smp {smp} -drive file={fs},if=none,format=raw,id=x0 "
                "-device virtio-blk-pci,drive=x0 -no-reboot -device virtio-net-pci,netdev=net0 "
                "-netdev user,id=net0 -rtc base=utc ")
    if os.path.exists(os.path.join(os.getcwd(), "disk-la.img")):
        cmd += " -drive file=disk-la.img,if=none,format=raw,id=x1 -device virtio-blk-pci,drive=x1"
    job.add_log(cmd, "QEMU CMD")
    console_log("运行：" + cmd)
    with open(out, "w", errors='ignore', buffering=1) as f, \
         open("/mnt/cghook/console_log", "a", errors='ignore', buffering=1) as hook_f:
        f.write(cmd)
        f.write("\n")
        f.flush()
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            shell=True,
            text=True,
            bufsize=1,
        )

        # Thread to read stdout in real-time
        timeout_occurred = threading.Event()

        def read_output():
            try:
                for line in p.stdout:
                    if timeout_occurred.is_set():
                        break
                    f.write(line)
                    f.flush()
                    hook_f.write("qemu-system-loong:" + line)
                    hook_f.flush()
            except:
                pass

        reader_thread = threading.Thread(target=read_output)
        reader_thread.daemon = True
        reader_thread.start()

        try:
            p.stdin.write("\n")
            p.stdin.flush()
            p.stdin.close()
            p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timeout_occurred.set()
            p.kill()
            p.wait()

        # Wait for reader thread to finish (with a short timeout)
        reader_thread.join(timeout=1)

    return error, process

"""
dd if=/dev/zero of=2kfs.img bs=100M count=1
mkfs.vfat 2kfs.img
mkdir -p mnt2
fusefat 2kfs.img mnt2 -o rw+
cp kernel.bin /mnt2
fusermount -u mnt2
"""
