import sys
import json

# This is for reference only and is unused below.
# Note terminal control sequences (\x1b[...m) should be present in real output, which isn't shown here.
template = '''
RUN LTP CASE writev01
tst_tmpdir.c:316: TINFO: Using /tmp/LTP_wriRnYU84 as tmpdir (ext2/ext3/ext4 filesystem)
tst_test.c:1860: TINFO: LTP version: 20240930
tst_test.c:1864: TINFO: Tested kernel: 5.15.153.1-microsoft-standard-WSL2 #1 SMP Fri Mar 29 23:14:13 UTC 2024 x86_64
tst_test.c:1703: TINFO: Timeout per run is 0h 00m 30s
writev01.c:124: TPASS: invalid iov_len, expected: -1 (EINVAL), got: -1 (EINVAL)
writev01.c:124: TPASS: invalid fd, expected: -1 (EBADF), got: -1 (EBADF)
writev01.c:124: TPASS: invalid iovcnt, expected: -1 (EINVAL), got: -1 (EINVAL)
writev01.c:129: TPASS: zero iovcnt, expected: 0, got: 0
writev01.c:129: TPASS: NULL and zero length iovec, expected: 64, got: 64
writev01.c:124: TPASS: write to closed pipe, expected: -1 (EPIPE), got: -1 (EPIPE)

Summary:
passed   6
failed   0
broken   0
skipped  0
warnings 0
END LTP CASE writev01 : 0
RUN LTP CASE setegid02
tst_test.c:1860: TINFO: LTP version: 20240930
tst_test.c:1864: TINFO: Tested kernel: 5.15.153.1-microsoft-standard-WSL2 #1 SMP Fri Mar 29 23:14:13 UTC 2024 x86_64
tst_test.c:1703: TINFO: Timeout per run is 0h 00m 30s
setegid02.c:29: TPASS: setegid(65534) : EPERM (1)

Summary:
passed   1
failed   0
broken   0
skipped  0
warnings 0
END LTP CASE setegid02: 0
'''

def parse_ltp_log(content: str):
    lines = content.split('\n')
    result = {}
    testcase = None
    passed, failed, broken, skipped, warnings = 0, 0, 0, 0, 0
    for line in lines:
        line = line.strip()

        if line.startswith('RUN LTP CASE'):
            testcase = line.split()[-1]
            continue
        
        # Look at LTP logs (TPASS, TFAIL etc.) rather than summary.
        # Some LTP binaries don't produce summaries when run directly.
        if line.startswith("FAIL LTP CASE"):
            result[testcase] = {
                "success": passed,
                "failed": failed,
                "broken": broken,
                "skipped": skipped,
                "warnings": warnings,
                "all": passed + failed + broken + skipped + warnings
            }
            testcase = ""
            passed, failed, broken, skipped, warnings = 0, 0, 0, 0, 0
            continue

        if "\x1b[1;32mTPASS: \x1b[0m" in line:
            passed += 1
            continue
        if "\x1b[1;31mTFAIL: \x1b[0m" in line:
            failed += 1
            continue
        if "\x1b[1;31mTBROK: \x1b[0m" in line:
            broken += 1
            continue
        if "\x1b[1;33mTCONF: \x1b[0m" in line:
            skipped += 1
            continue
        if "\x1b[1;35mTWARN: \x1b[0m" in line:
            warnings += 1
            continue

    return result

# `sys.stdin.read()` will by default decode in UTF-8.
# However, it is possible that LTP produces some byte >= 0x80.
# To preserve it as-is, we decode with latin-1 instead.
read = sys.stdin.buffer.read().decode("latin-1")
result = parse_ltp_log(read)
result = [{
    "name": k,
    "pass": v["success"],
    "all": v["all"],
    "score": v["success"]
} for k, v in result.items()]

print(json.dumps(result))
