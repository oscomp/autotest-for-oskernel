lmbench_baseline = r"""
"test_lua.sh" 9L, 190B written
root@debian:~/testsuits-for-oskernel/scripts/lua# chmod +x test_lua.sh 
root@debian:~/testsuits-for-oskernel/scripts/lua# ./test_lua.sh 
testcase lua date.lua success
testcase lua file_io.lua success
testcase lua max_min.lua fail 
testcase lua random.lua success
testcase lua remove.lua success
testcase lua round_num.lua fail
testcase lua sin30.lua success
testcase lua sort.lua success
testcase lua strings.lua success
  111 root      0:00 [ext4-rsv-conver]
  114 root      0:00 [kworker/u2:2-ex]
  144 root      0:01 /lib/systemd/systemd-journald
  158 root      0:00 /lib/systemd/systemd-udevd
  171 systemd-  0:00 /lib/systemd/systemd-timesyncd
  174 root      0:00 [hwrng]
  186 root      0:00 /usr/sbin/cron -f
  191 root      0:00 /usr/sbin/rsyslogd -n -iNONE
  214 root      0:00 [kworker/0:2-eve]
  217 root      0:00 /sbin/agetty -o -p -- \u --noclear tty1 linux
  218 root      0:00 /sbin/agetty -o -p -- \u --noclear tty2 linux
  219 root      0:00 /sbin/agetty -o -p -- \u --noclear tty3 linux
  220 root      0:00 /sbin/agetty -o -p -- \u --noclear tty4 linux
  221 root      0:00 /sbin/agetty -o -p -- \u --noclear tty5 linux
  222 root      0:00 /sbin/agetty -o -p -- \u --noclear tty6 linux
  223 root      0:00 /bin/login -p --
  224 root      0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
  251 root      0:01 -bash
  479 root      0:00 [kworker/u2:1-ex]

testcase busybox ash -c exit success
testcase busybox sh -c exit success
bbb
testcase busybox basename /aaa/bbb success
     June 2021
Su Mo Tu We Th Fr Sa
       1  2  3  4  5
 6  7  8  9 10 11 12
13 14 15 16 17 18 19
20 21 22 23 24 25 26
27 28 29 30

testcase busybox cal success
testcase busybox touch abc success
"hello world" > abc
testcase busybox echo "hello world" > abc success
echo "hello world" > abc
grep hello busybox_cmd.txt
testcase busybox grep hello busybox_cmd.txt success
testcase busybox cat abc success

testcase busybox clear success
testcase busybox cp busybox busybox_bak success
testcase busybox cut -c 3 abc success
0000000
testcase busybox od abc success
testcase busybox rm busybox_bak success
Mon Jun 21 02:28:58 UTC 2021
testcase busybox date success
Filesystem           1K-blocks      Used Available Use% Mounted on
udev                    443976         0    443976   0% /dev
tmpfs                    94468       188     94280   0% /run
/dev/vda1             10218644   1961304   7716676  20% /
tmpfs                   472336         0    472336   0% /dev/shm
tmpfs                     5120         0      5120   0% /run/lock
testcase busybox df success
/aaa
testcase busybox dirname /aaa/bbb success

testcase busybox dmesg success
1108	.
testcase busybox du success
"abc"
testcase busybox echo "abc" success
2
testcase busybox expr 1 + 1 success
testcase busybox false success
testcase busybox true success
testcase busybox find -name "busybox" success
              total        used        free      shared  buff/cache   available
Mem:         944672       42280      782572         188      119820      887144
Swap:             0           0           0
testcase busybox free success
testcase busybox head abc success
testcase busybox tail abc success
testcase busybox hexdump -C abc success
hwclock: can't open '/dev/misc/rtc': No such file or directory
testcase busybox hwclock fail
testcase busybox kill 10 success
abc                  busybox_cmd.txt      result.txt
busybox              busybox_testcode.sh
testcase busybox ls success
d41d8cd98f00b204e9800998ecf8427e  abc
testcase busybox md5sum abc success
testcase busybox mkdir test_dir success
testcase busybox mv test_dir test success
testcase busybox rmdir test success
"abcn"testcase busybox printf "abcn" success
PID   USER     TIME  COMMAND
    1 root      0:09 {systemd} /sbin/init noquiet
    2 root      0:00 [kthreadd]
    3 root      0:00 [rcu_gp]
  589 root      0:00 ./busybox ps
testcase busybox ps success
/root/testsuits-for-oskernel/scripts/busybox
testcase busybox pwd success
testcase busybox sleep 1 success
"aaaaaaa" >> abc
testcase busybox echo "aaaaaaa" >> abc success
"bbbbbbb" >> abc
testcase busybox echo "bbbbbbb" >> abc success
"ccccccc" >> abc
testcase busybox echo "ccccccc" >> abc success
"1111111" >> abc
testcase busybox echo "1111111" >> abc success
"2222222" >> abc
testcase busybox echo "2222222" >> abc success
sort: |: No such file or directory
testcase busybox sort abc | uniq fail
  File: abc
  Size: 0         	Blocks: 0          IO Block: 4096   regular empty file
Device: fe01h/65025d	Inode: 272553      Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2021-06-21 02:28:58.623019297 +0000
Modify: 2021-06-21 02:28:58.559019951 +0000
Change: 2021-06-21 02:28:58.559019951 +0000
testcase busybox stat abc success
testcase busybox strings abc success
Linux
testcase busybox uname success
 02:29:00 up 26 min,  0 users,  load average: 0.00, 0.00, 0.00
testcase busybox uptime success
        0         0         0 abc
testcase busybox wc abc success
/bin/ls
testcase busybox which ls success
testcase busybox [ -f abc ] success
testcase busybox more abc success
testcase busybox rm abc success
If the CMD runs incorrectly, return value will put in result.txt
Else nothing will put in result.txt

TEST START
return: 1, cmd: hwclock
return: 2, cmd: sort abc | uniq
TEST END


latency measurements
Simple syscall: 9.25013 microseconds
Simple read: 16.8192 microseconds
Simple write: 16.87553 microseconds
mkdir: cannot create directory ‘/var/tmp’: File exists
Simple stat: 425.2565 microseconds
Simple fstat: 29.54674 microseconds
Simple open/close: 501.2352 microseconds
Select on 100 fd's: 56.05561 microseconds
Signal handler installation: 18.84948 microseconds
Signal handler overhead: 25.89064 microseconds
Pipe latency: 141.9106 microseconds
Process fork+exit: 4409.188 microseconds
Process fork+execve: 2004.3333 microseconds
Process fork+/bin/sh -c: 920010.2 microseconds
File /var/tmp/XXX write bandwidth:5617 KB/sec
Pagefaults on /var/tmp/XXX: 978.2374643 microseconds
0.524288 4109
file system latency
0k      30      24573    30703
1k      19      15130    255558
4k      18      13265    126595
10k     14      11723    23688
Bandwidth measurements
Pipe bandwidth: 127.244 MB/sec
0.524288 71703.7
0.524288 2637.494
0.524288 1037.403
0.524288 187.0208
context switch overhead
"size=32k ovr=32.98
2 41.24
4 41.58071
8 41.04231
16 40.77077
24 43.86385
32 47.74923
64 8703.026
96 2952.14
"""
import re
import sys
import json
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

summary = {}
serial_out = sys.stdin.read()
summary['lmbench_results'] = parse_lmbench(serial_out)
summary['lmbench_baseline'] = parse_lmbench(lmbench_baseline)

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

lmbench = generate_score(summary['lmbench_results'], summary['lmbench_baseline'])
print(json.dumps(lmbench))
