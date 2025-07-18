iperf_baseline = """
====== iperf BASIC_UDP begin ======
Connecting to host 127.0.0.1, port 5001
[  5] local 127.0.0.1 port 36728 connected to 127.0.0.1 port 5001
[ ID] Interval           Transfer     Bitrate         Total Datagrams
[  5]   0.00-2.00   sec  93.8 MBytes   393 Mbits/sec  3003
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Jitter    Lost/Total Datagrams
[  5]   0.00-2.00   sec  93.8 MBytes   393 Mbits/sec  0.000 ms  0/3003 (0%)  sender
[  5]   0.00-2.00   sec  93.8 MBytes   393 Mbits/sec  0.057 ms  0/3003 (0%)  receiver

iperf Done.
====== iperf BASIC_UDP end: success ======

====== iperf BASIC_TCP begin ======
Connecting to host 127.0.0.1, port 5001
[  5] local 127.0.0.1 port 40284 connected to 127.0.0.1 port 5001
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-2.00   sec   199 MBytes   832 Mbits/sec    0   1.31 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-2.00   sec   199 MBytes   832 Mbits/sec    0             sender
[  5]   0.00-2.01   sec   191 MBytes   796 Mbits/sec                  receiver

iperf Done.
====== iperf BASIC_TCP end: success ======

====== iperf PARALLEL_UDP begin ======
Connecting to host 127.0.0.1, port 5001
[  5] local 127.0.0.1 port 49353 connected to 127.0.0.1 port 5001
[  7] local 127.0.0.1 port 55324 connected to 127.0.0.1 port 5001
[  9] local 127.0.0.1 port 46409 connected to 127.0.0.1 port 5001
[ 11] local 127.0.0.1 port 34383 connected to 127.0.0.1 port 5001
[ 13] local 127.0.0.1 port 44302 connected to 127.0.0.1 port 5001
[ ID] Interval           Transfer     Bitrate         Total Datagrams
[  5]   0.00-2.00   sec  21.2 MBytes  88.7 Mbits/sec  678
[  7]   0.00-2.00   sec  21.2 MBytes  88.7 Mbits/sec  678
[  9]   0.00-2.00   sec  21.2 MBytes  88.7 Mbits/sec  678
[ 11]   0.00-2.00   sec  21.2 MBytes  88.7 Mbits/sec  678
[ 13]   0.00-2.00   sec  21.2 MBytes  88.7 Mbits/sec  678
[SUM]   0.00-2.00   sec   106 MBytes   444 Mbits/sec  3390
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Jitter    Lost/Total Datagrams
[  5]   0.00-2.00   sec  21.2 MBytes  88.7 Mbits/sec  0.000 ms  0/678 (0%)  sender
[  5]   0.00-2.00   sec  21.2 MBytes  88.5 Mbits/sec  0.386 ms  1/678 (0.15%)  receiver
[  7]   0.00-2.00   sec  21.2 MBytes  88.7 Mbits/sec  0.000 ms  0/678 (0%)  sender
[  7]   0.00-2.00   sec  21.2 MBytes  88.7 Mbits/sec  0.362 ms  0/678 (0%)  receiver
[  9]   0.00-2.00   sec  21.2 MBytes  88.7 Mbits/sec  0.000 ms  0/678 (0%)  sender
[  9]   0.00-2.00   sec  21.1 MBytes  88.4 Mbits/sec  0.376 ms  2/678 (0.29%)  receiver
[ 11]   0.00-2.00   sec  21.2 MBytes  88.7 Mbits/sec  0.000 ms  0/678 (0%)  sender
[ 11]   0.00-2.00   sec  21.0 MBytes  87.9 Mbits/sec  0.389 ms  6/678 (0.88%)  receiver
[ 13]   0.00-2.00   sec  21.2 MBytes  88.7 Mbits/sec  0.000 ms  0/678 (0%)  sender
[ 13]   0.00-2.00   sec  21.0 MBytes  88.0 Mbits/sec  0.465 ms  5/678 (0.74%)  receiver
[SUM]   0.00-2.00   sec   106 MBytes   444 Mbits/sec  0.000 ms  0/3390 (0%)  sender
[SUM]   0.00-2.00   sec   106 MBytes   442 Mbits/sec  0.396 ms  14/3390 (0.41%)  receiver

iperf Done.
====== iperf PARALLEL_UDP end: success ======

====== iperf PARALLEL_TCP begin ======
Connecting to host 127.0.0.1, port 5001
[  5] local 127.0.0.1 port 40290 connected to 127.0.0.1 port 5001
[  7] local 127.0.0.1 port 40292 connected to 127.0.0.1 port 5001
[  9] local 127.0.0.1 port 40294 connected to 127.0.0.1 port 5001
[ 11] local 127.0.0.1 port 40296 connected to 127.0.0.1 port 5001
[ 13] local 127.0.0.1 port 40298 connected to 127.0.0.1 port 5001
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-2.03   sec  62.5 MBytes   258 Mbits/sec    0   1023 KBytes
[  7]   0.00-2.03   sec  62.5 MBytes   258 Mbits/sec    0   1.06 MBytes
[  9]   0.00-2.03   sec  62.5 MBytes   258 Mbits/sec    0   1.62 MBytes
[ 11]   0.00-2.03   sec  62.5 MBytes   258 Mbits/sec    0   1.56 MBytes
[ 13]   0.00-2.03   sec  62.5 MBytes   258 Mbits/sec    0   1.06 MBytes
[SUM]   0.00-2.03   sec   312 MBytes  1.29 Gbits/sec    0
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-2.03   sec  62.5 MBytes   258 Mbits/sec    0             sender
[  5]   0.00-2.04   sec  62.5 MBytes   257 Mbits/sec                  receiver
[  7]   0.00-2.03   sec  62.5 MBytes   258 Mbits/sec    0             sender
[  7]   0.00-2.04   sec  62.4 MBytes   257 Mbits/sec                  receiver
[  9]   0.00-2.03   sec  62.5 MBytes   258 Mbits/sec    0             sender
[  9]   0.00-2.04   sec  62.4 MBytes   257 Mbits/sec                  receiver
[ 11]   0.00-2.03   sec  62.5 MBytes   258 Mbits/sec    0             sender
[ 11]   0.00-2.04   sec  62.4 MBytes   257 Mbits/sec                  receiver
[ 13]   0.00-2.03   sec  62.5 MBytes   258 Mbits/sec    0             sender
[ 13]   0.00-2.04   sec  62.4 MBytes   257 Mbits/sec                  receiver
[SUM]   0.00-2.03   sec   312 MBytes  1.29 Gbits/sec    0             sender
[SUM]   0.00-2.04   sec   312 MBytes  1.28 Gbits/sec                  receiver

iperf Done.
====== iperf PARALLEL_TCP end: success ======

====== iperf REVERSE_UDP begin ======
Connecting to host 127.0.0.1, port 5001
Reverse mode, remote host 127.0.0.1 is sending
[  5] local 127.0.0.1 port 43873 connected to 127.0.0.1 port 5001
[ ID] Interval           Transfer     Bitrate         Jitter    Lost/Total Datagrams
[  5]   0.00-2.00   sec  90.8 MBytes   381 Mbits/sec  0.058 ms  9/2914 (0.31%)
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Jitter    Lost/Total Datagrams
[  5]   0.00-2.01   sec  91.1 MBytes   380 Mbits/sec  0.000 ms  0/2914 (0%)  sender
[  5]   0.00-2.00   sec  90.8 MBytes   381 Mbits/sec  0.058 ms  9/2914 (0.31%)  receiver

iperf Done.
====== iperf REVERSE_UDP end: success ======

====== iperf REVERSE_TCP begin ======
Connecting to host 127.0.0.1, port 5001
Reverse mode, remote host 127.0.0.1 is sending
[  5] local 127.0.0.1 port 40304 connected to 127.0.0.1 port 5001
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-2.00   sec   189 MBytes   792 Mbits/sec
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-2.02   sec   198 MBytes   822 Mbits/sec    0             sender
[  5]   0.00-2.00   sec   189 MBytes   792 Mbits/sec                  receiver

iperf Done.
====== iperf REVERSE_TCP end: success ======
"""