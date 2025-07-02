import datetime
import json
import re
import os
import subprocess
import sys
import threading
import time
import pdb

import pygrading as gg
from parse_output_2023 import parse_iozone, parse_iperf, parse_libcbench, parse_netperf, parse_time_test, \
    parse_unixbench, parse_libctest, parse_cyclictest
import postwork
from pygrading.job import Job

from utils import loge, console_log

server_run = False

from run_qemu import run_qemu, run_qemu_loong


def pe(e: exec):
    loge(f"CMD: {e.cmd}\nOUT:\n{e.stdout}\nERR:\n{e.stderr}\nRETCODE:{e.returncode}")


def is_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False

def to_int(x):
    try:
        return int(x)
    except ValueError:
        return -1

def parse_lmbench(output):
    result = {}
    units = ("microseconds", "KB/sec", "MB/sec")
    lst = ["lat_mmap:(microseconds)", "bw_file_rd io_only", "bw_file_rd open2close", "bw_mmap_rd mmap_only", "bw_mmap_rd open2close"]
    lst_cnt = 0
    ctx = (2, 4, 8, 16, 24, 32, 64, 96)
    stat = 0
    for line in output.split("\n"):
        sep = line.strip().split()
        if not sep:
            continue
        if "latency measurements" in line:
            stat = 1
        if stat < 1 or stat > 15:
            continue
        if "context switch overhead" in line:
            stat = 2
        if stat >= 2:
            stat += 1
        if len(sep) >= 3 and sep[-1] in units and is_float(sep[-2]):
            result[' '.join(sep[:-2]) + f"({sep[-1]})"] = float(sep[-2])
        if len(sep) == 4 and sep[0][-1] == 'k':
            result[f"fs latency {sep[0]} create"] = to_int(sep[2])
            result[f"fs latency {sep[0]} remove"] = to_int(sep[3])
        if len(sep) == 2 and is_float(sep[0]) and is_float(sep[1]):
            if float(sep[0]) in ctx:
                result[f"context switch {sep[0]}:(microseconds)"] = float(sep[1])
            else:
                if lst_cnt < len(lst):
                    result[lst[lst_cnt]] = float(sep[1])
                lst_cnt += 1
    ans = {}
    for k, v in result.items():
        ans["lmbench " + k] = v
    return ans


def check_n(line, n):
    lst = line.split(' ')
    if len(lst) == n:
        try:
            for i in range(n):
                float(lst[i])
        except ValueError:
            return False
        return True
    return False


def parse_scene(output):
    state = 0
    keys = (
        "bw_file_rd_io_only",
        "bw_file_rd_open2close",
        "lat_proc_fork",
        "lat_proc_exec",
        "bw_pipe",
        "lat_pipe",
        "lat_pagefault",
        "lat_mmap",
        "lat_ctx"
    )
    result_keys = (
        "bw_file_rd_io_only",
        "bw_file_rd_open2close",
        "lat_proc_fork",
        "lat_proc_exec",
        "bw_pipe",
        "lat_pipe",
        "lat_pagefault",
        "lat_mmap",
        "lat_ctx_2",
        "lat_ctx_4",
        "lat_ctx_8",
        "lat_ctx_16",
        "lat_ctx_24",
        "lat_ctx_32"
    )
    result = {}
    key = ""
    for line in output.split("\n"):
        if state == 0:
            if line[:5] == "START":
                if line[6:] in keys:
                    key = line[6:]
                    state = 1
        elif state == 1:
            if line[:3] == "END":
                state = 0
                if line.split(' ')[-1] != "0":
                    result[key] = "0"
            elif line[:5] == "START":
                if line[6:] in keys:
                    result[key] = "0"
                    key = line[6:]
                    state = 1
            elif key in ("bw_file_rd_io_only", "bw_file_rd_open2close", "lat_mmap"):
                if check_n(line, 2):
                    result[key] = line.split(' ')[1]
            elif key in ("lat_proc_fork", "lat_proc_exec", "bw_pipe", "lat_pipe"):
                lst = line.split(' ')
                if len(lst) == 4:
                    try:
                        result[key] = str(float(lst[2]))
                    except ValueError:
                        pass
            elif key == "lat_ctx":
                if check_n(line, 2):
                    lst = line.split(' ')
                    if lst[0] in ("2", "4", "8", "16", "24", "32"):
                        result[key + "_" + lst[0]] = lst[1]
            elif key == "lat_pagefault":
                lst = line.split(' ')
                if len(lst) == 5:
                    try:
                        result[key] = str(float(lst[3]))
                    except ValueError:
                        pass
    for k in result_keys:
        if k not in result.keys():
            result[k] = "0"
    for k in result.keys():
        if k[:2] == "bw" and float(result[k]) != 0:
            result[k] = str(1 / float(result[k]))
    return result


def run(job: gg.Job, testcase: gg.TestCases.SingleTestCase):
    job.add_log_detail(f"BEFORE_RUN: {datetime.datetime.now()}", "time")
    config = job.get_config()
    result = {'name': testcase.name, 'score': 0}
    # -- check bin file ---

    loge("\n[os autotest]: Flash Start:\n")


    def logexec(cmd):
        job.add_log_detail(cmd, "cmd")
        loge("[os autotest]:" + cmd)
        start_time = time.time()
        res = gg.exec(cmd)
        job.add_log_detail(f"STDOUT:\n{res.stdout}\nSTDERR:{res.stderr}\nTIME:{datetime.datetime.now()}\nDURATION:{time.time() - start_time}", cmd)
        if res.returncode != 0:
            raise RuntimeError(f"run command error {cmd} \n{res.stdout}\n{res.stderr}")
        return res

    os.chdir(config['submit_dir'])
    logexec(f"cp {config['testcase_dir']}/sdcard-rv.img.gz sdcard-rv.img.gz")
    trv = threading.Thread(target=run_qemu, args=(job, config["sbi_file"], "kernel-rv", "sdcard-rv.img", "os_serial_out_rv.txt"))

    logexec(f"cp {config['testcase_dir']}/sdcard-la.img.gz sdcard-la.img.gz")
    tla = threading.Thread(target=run_qemu_loong, args=(job, config["sbi_file"], "kernel-la", "sdcard-la.img", "os_serial_out_la.txt"))

    trv.start()
    tla.start()
    trv.join()
    tla.join()

    result['out_file_rv'] = "os_serial_out_rv.txt"
    result['out_file_la'] = "os_serial_out_la.txt"
    result['rv'] = parse_serial_out_new(config, "os_serial_out_rv.txt")
    result['la'] = parse_serial_out_new(config, "os_serial_out_la.txt")

    job.add_log_detail(f"AFTER_RUN: {datetime.datetime.now()}", "time")
    return result


def _get_name(x: str):
    x = x.removeprefix("judge_")
    if '.' in x:
        x = x[:x.rindex('.')]
    return x

def _get_exec(x: str):
    if x.endswith(".py"):
        return [sys.executable, x]
    if x.endswith(".sh"):
        return ["/bin/bash", x]
    return [x]

def parse_serial_out_new(config, filename):
    ans = {}
    file = open(filename, "r", encoding='utf-8', errors='ignore')
    judge_path = config["testcase_dir"]
    judge = None
    group = None
    called_group = set()
    start = re.compile(r"#### OS COMP TEST GROUP START ([a-zA-Z0-9-]+) ####")
    end = '#### OS COMP TEST GROUP END'
    judges = [x for x in os.listdir(judge_path) if x.startswith("judge_")]
    judges = {_get_name(x): _get_exec(os.path.join(judge_path, x)) for x in judges}
    for line in file:
        is_start = start.findall(line)
        if end in line or len(is_start) > 0:
            if judge:
                try:
                    judge.stdin.close()
                    x = judge.stdout.read().decode()
                    ans[group] = json.loads(x)
                    judge.wait(5)
                    judge = None
                    group = None
                except Exception as e:
                    print(f"评测 {filename} : {group} 发生错误：{e}")
                    raise e
        elif judge is not None:
            judge.stdin.write(line.encode())
        if is_start:
            group = is_start[0]
            # group = line.replace(start, '').replace('#', '').strip()
            if group in judges:
                console_log(f"正在评测：{filename} : {group}")
                judge = subprocess.Popen(judges[group], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                called_group.add(group)
    if judge:
        try:
            judge.stdin.close()
            x = judge.stdout.read().decode()
            ans[group] = json.loads(x)
            judge.wait(5)
            judge = None
            group = None
        except Exception as e:
            print(f"评测 {filename} : {group} 发生错误：{e}")
            raise e
    for g, j in judges.items():
        if g not in called_group:
            console_log(f"正在评测：{filename} : {g}")
            try:
                judge = subprocess.Popen(judges[g], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                judge.stdin.close()
                x = judge.stdout.read().decode()
                ans[g] = json.loads(x)
            except Exception as e:
                print(f"评测 {filename} : {g} 发生错误：{e}")
                raise e
    # print(ans)
    return ans


def parse_serial_out_new_new(filename):
    ans = {}
    file = open(filename, "r", encoding='utf-8', errors='ignore')
    judge_path = "judge"
    judge = None
    group = None
    called_group = set()
    start = re.compile(r"#### OS COMP TEST GROUP START ([a-zA-Z0-9-]+) ####")
    end = '#### OS COMP TEST GROUP END'
    judges = [x for x in os.listdir(judge_path) if x.startswith("judge_")]
    judges = {_get_name(x): _get_exec(os.path.join(judge_path, x)) for x in judges}
    for line in file:
        is_start = start.findall(line)
        if end in line or len(is_start) > 0:
            if judge:
                try:
                    judge.stdin.close()
                    x = judge.stdout.read().decode()
                    ans[group] = json.loads(x)
                    judge.wait(5)
                    judge = None
                    group = None
                except Exception as e:
                    print(f"评测 {filename} : {group} 发生错误：{e}")
                    raise e
        elif judge is not None:
            judge.stdin.write(line.encode())
        if is_start:
            group = is_start[0]
            # group = line.replace(start, '').replace('#', '').strip()
            if group in judges:
                console_log(f"正在评测：{filename} : {group}")
                judge = subprocess.Popen(judges[group], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                called_group.add(group)
    if judge:
        try:
            judge.stdin.close()
            x = judge.stdout.read().decode()
            ans[group] = json.loads(x)
            judge.wait(5)
            judge = None
            group = None
        except Exception as e:
            print(f"评测 {filename} : {group} 发生错误：{e}")
            raise e
    for g, j in judges.items():
        if g not in called_group:
            console_log(f"正在评测：{filename} : {g}")
            try:
                judge = subprocess.Popen(judges[g], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                judge.stdin.close()
                x = judge.stdout.read().decode()
                ans[g] = json.loads(x)
            except Exception as e:
                print(f"评测 {filename} : {g} 发生错误：{e}")
                raise e
    # print(ans)
    return ans



def parse_serial_out(serial_out, job):
    result = {}
    pattern = re.compile(r"testcase (.+) (\bsuccess\b|\bfail\b)")
    results = pattern.findall(serial_out)
    results = {x[0].strip(): x[1] == 'success' for x in results}

    # names = set(x["name"] for x in results)

    def append_miss(name, prefix):
        config = job.get_config()
        with open(f"{config['testcase_dir']}/{name}") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if f"{prefix} {line}" not in results.keys():
                    results[f"{prefix} {line}"] = False
                    # results.append({"name": f"{prefix} {line}", "passed": 0, "all": 1})

    #append_miss("luas.txt", "lua")
    #append_miss("busybox_cmd.txt", "busybox")

    job.add_log_detail(str(results), "RESULTS??")

    from baselines.libctest_baseline import libctest_baseline
    libctest_baseline_out = parse_libctest(libctest_baseline)
    libctest_output = parse_libctest(serial_out)
    for k in libctest_baseline_out.keys():
        if k not in libctest_output:
            libctest_output[k] = 0

    results = [{
        "name": k,
        "passed": 1 if v else 0,
        "all": 1
    }
        for k, v in results.items()
    ]
    for k, v in libctest_output.items():
        results.append({
            "name": k,
            "passed": v,
            "all": 1
        })
    results = sorted(results, key=lambda x: x["name"])
    result['lua_results'] = results
    from baselines import baseline_output
    result['lmbench_results'] = parse_lmbench(serial_out)
    result['lmbench_baseline'] = parse_lmbench(baseline_output.serial_out)
    from baselines.iozone_baseline import iozone_baseline
    result['iozone_results'] = parse_iozone(serial_out)
    result['iozone_baseline'] = parse_iozone(iozone_baseline)
    from baselines.iperf_baseline import iperf_baseline
    result['iperf_results'] = parse_iperf(serial_out)
    result['iperf_baseline'] = (parse_iperf(iperf_baseline))
    from baselines.libcbench_baseline import libcbench_baseline
    result['libcbench_results'] = parse_libcbench(serial_out)
    result['libcbench_baseline'] = (parse_libcbench(libcbench_baseline))
    from baselines.netperf_baseline import netperf_baseline
    result['netperf_results'] = parse_netperf(serial_out)
    result['netperf_baseline'] = (parse_netperf(netperf_baseline))
    from baselines.unixbench_baseline import unixbench_baseline
    result['unixbench_results'] = parse_unixbench(serial_out)
    result['unixbench_baseline'] = (parse_unixbench(unixbench_baseline))
    from baselines.cyclictest_baseline import cyclictest_baseline
    result['cyclictest_results'] = parse_cyclictest(serial_out)
    result['cyclictest_baseline'] = parse_cyclictest(cyclictest_baseline)
    result['ltp_result'] = parse_ltp(serial_out)
    result['time-test'] = parse_time_test(serial_out)
    return result


def parse_ltp(out):
    out = out.replace("\033", "")
    pat = re.compile(r"(.+): (?:\[1;32m)?pass.*")
    ans1 = pat.findall(out)
    s = set()
    pat = re.compile(r"(.+): (?:\[1;32m)?success.*")
    ans2 =pat.findall(out)
    for x in ans1 + ans2:
        if isinstance(x, str):
            if ' ' not in x:
                s.add(x)
        else:
            if ' ' not in x[0]:
                s.add(x[0])
    return {"score": len(s)}


if __name__ == '__main__':
    # out = open("ltp-result.txt").read() + open("all_out.txt").read()
    # print(parse_ltp(out))
    # exit(0)
    result = {}
    job = Job()
    pdb.set_trace()
    result['rv'] = parse_serial_out_new_new("os_serial_out_rv.txt")
    

