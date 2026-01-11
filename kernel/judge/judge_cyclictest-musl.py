import json
import re
import sys

cyclictest_baseline = """
====== cyclictest NO_STRESS_P1 begin ======
WARN: stat /dev/cpu_dma_latency failed: No such file or directory
T: 0 (  271) P:99 I:1000 C:    896 Min:    107 Act:  214 Avg:  563 Max:    1862
====== cyclictest NO_STRESS_P1 end: success ======
====== cyclictest NO_STRESS_P8 begin ======
WARN: stat /dev/cpu_dma_latency failed: No such file or directory
T: 0 (  273) P:99 I:1000 C:    995 Min:     97 Act:  186 Avg:  303 Max:    1917
T: 1 (  274) P:99 I:1500 C:    666 Min:    135 Act:  252 Avg:  325 Max:    2021
T: 2 (  275) P:99 I:2000 C:    498 Min:     90 Act:  165 Avg:  416 Max:    1274
T: 3 (  276) P:99 I:2500 C:    399 Min:    150 Act:  184 Avg:  350 Max:    1164
T: 4 (  277) P:99 I:3000 C:    333 Min:    108 Act:  618 Avg:  266 Max:    1539
T: 5 (  278) P:99 I:3500 C:    285 Min:    125 Act:  644 Avg:  373 Max:    1882
T: 6 (  279) P:99 I:4000 C:    249 Min:    102 Act:  247 Avg:  479 Max:    1362
T: 7 (  280) P:99 I:4500 C:    221 Min:    138 Act:  255 Avg:  405 Max:    1306
====== cyclictest NO_STRESS_P8 end: success ======
====== start hackbench ======
Running in process mode with 10 groups using 40 file descriptors each (== 400 tasks)
Each sender will pass 100000000 messages of 100 bytes
====== cyclictest STRESS_P1 begin ======
WARN: stat /dev/cpu_dma_latency failed: No such file or directory
T: 0 (  684) P:99 I:1000 C:    986 Min:     87 Act:  368 Avg:  389 Max:    1310
====== cyclictest STRESS_P1 end: success ======
====== cyclictest STRESS_P8 begin ======
WARN: stat /dev/cpu_dma_latency failed: No such file or directory
T: 0 (  687) P:99 I:1000 C:    971 Min:     51 Act:  150 Avg:  454 Max:    1950
T: 1 (  688) P:99 I:1500 C:    661 Min:    136 Act:  192 Avg:  473 Max:    1539
T: 2 (  689) P:99 I:2000 C:    495 Min:    152 Act:  242 Avg:  571 Max:    1515
T: 3 (  690) P:99 I:2500 C:    379 Min:    140 Act:  364 Avg:  434 Max:    1656
T: 4 (  691) P:99 I:3000 C:    317 Min:     97 Act:  320 Avg:  523 Max:    1375
T: 5 (  692) P:99 I:3500 C:    249 Min:    156 Act:  299 Avg:  484 Max:    1239
T: 6 (  693) P:99 I:4000 C:    225 Min:    153 Act:  266 Avg:  512 Max:    1468
T: 7 (  694) P:99 I:4500 C:     89 Min: 100000 Act:  213 Avg:  473 Max:    0
====== cyclictest STRESS_P8 end: success ======
Signal 2 caught, longjmp'ing out!
longjmp'ed out, reaping children
sending SIGTERM to all child processes
signaling 400 worker threads to terminate
Time: 9.813
====== kill hackbench: success ======

"""

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

serial_out = sys.stdin.read()
cyclictest_results = parse_cyclictest(serial_out)
cyclictest_baseline = parse_cyclictest(cyclictest_baseline)
def generate_score(results, baseline):
    lmbench_results = results
    lmbench_baseline = baseline
    lmbench = [
        {
            "name": name,
            "res": lmbench_results.get(name, 0),
            "baseline": baseline,
            "score": 0.0
        }
        for name, baseline in lmbench_baseline.items()
    ]
    for item in lmbench:
        if item["res"] > 0:
            if "microseconds" in item["name"] or "seconds" in item["name"]:
                item["score"] = item["baseline"] / item["res"]
            else:
                item["score"] = item["res"] / item["baseline"]

            if item['score'] >= 1:
                item['score'] = 2 - (1 / item['score'])
            else:
                item['score'] = 1.0
    return lmbench
print(json.dumps(generate_score(cyclictest_results, cyclictest_baseline)))