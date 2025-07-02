import json
import re
import sys

libcbench_baseline = """
b_malloc_sparse (0)
  time: 0.384919462, virt: 39376, res: 5348, dirty: 5348

b_malloc_bubble (0)
  time: 0.360153490, virt: 39376, res: 6612, dirty: 6612

b_malloc_tiny1 (0)
  time: 0.014186324, virt: 628, res: 124, dirty: 124

b_malloc_tiny2 (0)
  time: 0.010810043, virt: 628, res: 628, dirty: 628

b_malloc_big1 (0)
  time: 0.118578071, virt: 80080, res: 2560, dirty: 2560

b_malloc_big2 (0)
  time: 0.107088632, virt: 80080, res: 14080, dirty: 14080

b_malloc_thread_stress (0)
  time: 0.096325490, virt: 32, res: 32, dirty: 32

b_malloc_thread_local (0)
  time: 0.096989785, virt: 56, res: 56, dirty: 56

b_string_strstr ("abcdefghijklmnopqrstuvwxyz")
  time: 0.011402239, virt: 4, res: 4, dirty: 4

b_string_strstr ("azbycxdwevfugthsirjqkplomn")
  time: 0.020868089, virt: 4, res: 4, dirty: 4

b_string_strstr ("aaaaaaaaaaaaaacccccccccccc")
  time: 0.011944437, virt: 4, res: 4, dirty: 4

b_string_strstr ("aaaaaaaaaaaaaaaaaaaaaaaaac")
  time: 0.011749838, virt: 4, res: 4, dirty: 4

b_string_strstr ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac")
  time: 0.013963025, virt: 4, res: 4, dirty: 4

b_string_memset (0)
  time: 0.025313365, virt: 4, res: 4, dirty: 4

b_string_strchr (0)
  time: 0.012811332, virt: 4, res: 4, dirty: 4

b_string_strlen (0)
  time: 0.013459429, virt: 4, res: 4, dirty: 4

b_pthread_createjoin_serial1 (0)
  time: 1.284791557, virt: 4, res: 4, dirty: 4

b_pthread_createjoin_serial2 (0)
  time: 1.006433722, virt: 4, res: 4, dirty: 4

b_pthread_create_serial1 (0)
  time: 0.892420718, virt: 50004, res: 10004, dirty: 10004

b_pthread_uselesslock (0)
  time: 0.080551368, virt: 4, res: 4, dirty: 4

b_utf8_bigbuf (0)
  time: 0.036977802, virt: 4, res: 4, dirty: 4

b_utf8_onebyone (0)
  time: 0.109599811, virt: 4, res: 4, dirty: 4

b_stdio_putcgetc (0)
  time: 0.767822967, virt: 4, res: 4, dirty: 4

b_stdio_putcgetc_unlocked (0)
  time: 0.765147171, virt: 4, res: 4, dirty: 4

b_regex_compile ("(a|b|c)*d*b")
  time: 0.088259223, virt: 20, res: 20, dirty: 20

b_regex_search ("(a|b|c)*d*b")
  time: 0.083251251, virt: 20, res: 20, dirty: 20

b_regex_search ("a{25}b")
  time: 0.286712251, virt: 20, res: 20, dirty: 20

"""

def generage_score(results, baseline):
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

serial_out = sys.stdin.read()
summary = {}
summary['libcbench_results'] = parse_libcbench(serial_out)
summary['libcbench_baseline'] = (parse_libcbench(libcbench_baseline))
libcbench = generage_score(summary['libcbench_results'], summary['libcbench_baseline'])
print(json.dumps(libcbench))