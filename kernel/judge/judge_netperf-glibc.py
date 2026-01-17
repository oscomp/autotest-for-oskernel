import re
import sys
import json

netperf_baseline = """
====== netperf UDP_STREAM begin ======
Starting netserver with host '127.0.0.1' port '12865' and family AF_UNSPEC
MIGRATED UDP STREAM TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to 127.0.0.1 (127.0.0) port 0 AF_INET
Socket  Message  Elapsed      Messages                
Size    Size     Time         Okay Errors   Throughput
bytes   bytes    secs            #      #   10^6bits/sec

 212992    1000   1.00         3442      0      27.50
 32000           1.00         3428             27.39

====== netperf UDP_STREAM end: success ======
====== netperf TCP_STREAM begin ======
MIGRATED TCP STREAM TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to 127.0.0.1 (127.0.0) port 0 AF_INET
Recv   Send    Send                          
Socket Socket  Message  Elapsed              
Size   Size    Size     Time     Throughput  
bytes  bytes   bytes    secs.    10^6bits/sec  

 32000  32000   1000    1.00       79.75   
====== netperf TCP_STREAM end: success ======
====== netperf UDP_RR begin ======
MIGRATED UDP REQUEST/RESPONSE TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to 127.0.0.1 (127.0.0) port 0 AF_INET : first burst 0
Local /Remote
Socket Size   Request  Resp.   Elapsed  Trans.
Send   Recv   Size     Size    Time     Rate         
bytes  Bytes  bytes    bytes   secs.    per sec   

32000  32000  64       64      1.00     2070.62   
32000  32000 
====== netperf UDP_RR end: success ======
====== netperf TCP_RR begin ======
MIGRATED TCP REQUEST/RESPONSE TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to 127.0.0.1 (127.0.0) port 0 AF_INET : first burst 0
Local /Remote
Socket Size   Request  Resp.   Elapsed  Trans.
Send   Recv   Size     Size    Time     Rate         
bytes  Bytes  bytes    bytes   secs.    per sec   

32000  32000  64       64      1.00     2017.98   
32000  32000 
====== netperf TCP_RR end: success ======
====== netperf TCP_CRR begin ======
MIGRATED TCP Connect/Request/Response TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to 127.0.0.1 (127.0.0) port 0 AF_INET
Local /Remote
Socket Size   Request  Resp.   Elapsed  Trans.
Send   Recv   Size     Size    Time     Rate         
bytes  Bytes  bytes    bytes   secs.    per sec   

32000  32000  64       64      1.00      390.53   
32000  32000 
====== netperf TCP_CRR end: success ======
"""

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

serial_out = sys.stdin.read()
summary = {}
summary['netperf_results'] = parse_netperf(serial_out)
summary['netperf_baseline'] = (parse_netperf(netperf_baseline))
netperf = generate_score(summary['netperf_results'], summary['netperf_baseline'])
print(json.dumps(netperf))
