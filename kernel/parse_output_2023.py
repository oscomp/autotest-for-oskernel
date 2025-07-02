import re


def parse_iozone(output: str):
    ans = {}
    lines = output.split("\n")
    current_key = ""
    sub_key = ""
    for line in lines:
        if "iozone throughput write/read measurements" in line:
            current_key = "iozone write/read"
        elif "iozone throughput random-read measurements" in line:
            current_key = "iozone random-read"
        elif "iozone throughput read-backwards measurements" in line:
            current_key = "iozone read-backwards"
        elif "iozone throughput stride-read measurements" in line:
            current_key = "iozone stride-read"
        elif "iozone throughput fwrite/fread measurements" in line:
            current_key = "iozone fwrite/fread"
        elif "iozone throughput pwrite/pread measurements" in line:
            current_key = "iozone pwrite/pread"
        elif "iozone throughtput pwritev/preadv measurements" in line:
            current_key = "iozone pwritev/preadv"

        if "Children see throughput for" in line:
            sub_key = line.replace("Children see throughput for", "").strip()
            sub_key = sub_key.split("=")[0]
            sub_key = sub_key.strip()

        if "Max throughput per process" in line:
            key = f"{current_key} {sub_key} (kb/sec)"
            ans[key] = float(line.split("=")[1].split()[0])

    return ans


def parse_iperf(output):
    pat = re.compile(r"^\[\s*[5SUM]*].+[\d.]+ [MG]bits/sec.+receiver$")
    key = ""
    ans = {}
    for line in output.split("\n"):
        if "====== iperf BASIC_UDP begin ======" in line:
            key = "iperf BASIC_UDP"
        elif "====== iperf BASIC_TCP begin ======" in line:
            key = "iperf BASIC_TCP"
        elif "====== iperf PARALLEL_UDP begin ======" in line:
            key = "iperf PARALLEL_UDP"
        elif "====== iperf PARALLEL_TCP begin ======" in line:
            key = "iperf PARALLEL_TCP"
        elif "====== iperf REVERSE_UDP begin ======" in line:
            key = "iperf REVERSE_UDP"
        elif "====== iperf REVERSE_TCP begin ======" in line:
            key = "iperf REVERSE_TCP"
        res = pat.findall(line)
        if res:
            res = res[0].split()
            for i in range(0, len(res)):
                if res[i] == "Mbits/sec" or res[i] == "Gbits/sec":
                    val = float(res[i-1])
                    if res[i] == "Gbits/sec":
                        val = val * 1024
                    ans[key + " " + "(Mbits/sec)"] = val
                    break
    return ans


def parse_libcbench(output):
    ans = {}
    key = ""
    pat = re.compile(r"time: ([\d.]+)")
    for line in output.split("\n"):
        if not line:
            continue
        if line[0] == "b":
            key = line.strip()
        res = pat.findall(line)
        if res:
            ans[f"libc-bench {key} (seconds)"] = float(res[0])
    return ans


def is_int(s):
    try:
        int(s)
        return True
    except:
        return False

def parse_netperf(output):
    ans = {}
    key = ""
    for line in output.split('\n'):
        if "====== netperf UDP_STREAM begin ======" in line:
            key = "netperf UDP_STREAM"
        elif "====== netperf TCP_STREAM begin ======" in line:
            key = "netperf TCP_STREAM"
        elif "====== netperf UDP_RR begin ======" in line:
            key = "netperf UDP_RR"
        elif "====== netperf TCP_RR begin ======" in line:
            key = "netperf TCP_RR"
        elif "====== netperf TCP_CRR begin ======" in line:
            key = "netperf TCP_CRR"

        if not key:
            continue

        res = line.strip().split()
        if (len(res) == 5 or len(res) == 6) and is_int(res[0]):
            val = float(res[-1])
            if len(res) == 5:
                ans[key + " (Throughput 10^6bits/sec)"] = val
            else:
                ans[key + " (Trans. Rate/sec)"] = val
            key = ""
    return ans


def parse_time_test(output):
    pat = re.compile(r"time-test: time/iteration: ([\d.]+)ns total time: (\d+)ms")
    res = pat.findall(output)
    if not res:
        return {"time-test": 0}
    return {"time-test": float(res[0][1])}


def parse_unixbench(output):
    ans = {}
    for line in output.split("\n"):
        if line.startswith("Unixbench"):
            k, v = line.split(":")
            ans[k] = float(v.strip())
    return ans


def parse_libctest(output):
    ans = {}
    key = ""
    for line in output.split("\n"):
        if "START entry-static.exe" in line:
            key = "libctest static " + line.split(" ")[3]
        elif "START entry-dynamic.exe" in line:
            key = "libctest dynamic " + line.split(" ")[3]
        if line == "Pass!" and key != "":
            ans[key] = 1
    return ans


def parse_cyclictest(output):
    ans = {}
    key = ""
    vals = []
    pat = re.compile(r"T: .+ Min:\s+(\d+).+Max:\s+(\d+)")
    succ = False
    for line in output.split("\n"):
        if "cyclictest NO_STRESS_P1 begin" in line:
            key = "cyclictest NO_STRESS_P1"
        elif "cyclictest NO_STRESS_P8 begin" in line:
            key = "cyclictest NO_STRESS_P8"
        elif "cyclictest STRESS_P1 begin" in line:
            key = "cyclictest STRESS_P1"
        elif "cyclictest STRESS_P8 begin" in line:
            key = "cyclictest STRESS_P8"
        elif "end: success" in line:
            if len(vals) > 0:
                ans[key + " (microseconds)"] = sum(vals) / len(vals)
                vals = []
        elif "kill hackbench: success" in line:
            succ = True
        res = pat.findall(line)
        if res:
            minn = int(res[0][0])
            maxn = int(res[0][1])
            vals.append(max(maxn, minn))
    if not succ:
        return {}
    return ans


if __name__ == '__main__':
    # from baselines.iozone_baseline import iozone_baseline
    # print(parse_iozone(iozone_baseline))
    # from baselines.iperf_baseline import iperf_baseline
    # print(parse_iperf(iperf_baseline))
    # from baselines.libcbench_baseline import libcbench_baseline
    # print(parse_libcbench(libcbench_baseline))
    from baselines.netperf_baseline import netperf_baseline
    print(parse_netperf(netperf_baseline))
    time_test_baseline = "time-test: time/iteration: 0.057ns total time: 351ms"
    print(parse_time_test(time_test_baseline))
    # from baselines.unixbench_baseline import unixbench_baseline
    # print(parse_unixbench(unixbench_baseline))
    # from baselines.cyclictest_baseline import cyclictest_baseline
    # print(parse_cyclictest(cyclictest_baseline))
