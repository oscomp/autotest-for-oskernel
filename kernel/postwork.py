import random
import time
from os.path import abspath

import os

from pygrading import Job, render_template
from verdict import Verdict
from datetime import datetime
import pytz


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
    # lmbench = [
    #     {
    #         "name": k,
    #         "res": v
    #     }
    #     for k, v in lmbench_results.items()
    # ]
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


def postwork_old(job: Job):
    job.add_log_detail(f"BEFORE_POSTWORK: {datetime.now()}", "time")
    summary = job.get_summary()[0]
    config = job.get_config()
    stage = config.get("stage", 1)
    # print(summary)
    job.detail(render_template("logs.html", logs=job.get_logs_detail()))
    comment = ""
    all_tests = 1
    passed_tests = 0
    ranks = None
    score = 0
    lmbench_results = None
    time_test = None
    if 'error' not in summary:
        if not config.get("final", False):
            test_results = summary['test_results']
            details = {}
        else:
            ranks = {}
            test_results = summary['lua_results']
            # lmbench_results = summary['scene_results']
            lmbench = generage_score(summary['lmbench_results'], summary['lmbench_baseline'])
            iozone = generage_score(summary['iozone_results'], summary['iozone_baseline'])
            iperf = generage_score(summary['iperf_results'], summary['iperf_baseline'])
            libcbench = generage_score(summary['libcbench_results'], summary['libcbench_baseline'])
            netperf = generage_score(summary['netperf_results'], summary['netperf_baseline'])
            unixbench = generage_score(summary['unixbench_results'], summary['unixbench_baseline'])
            cyclic = generage_score(summary['cyclictest_results'], summary['cyclictest_baseline'])
            time_test = summary['time-test']
            ltp_score = summary['ltp_result']['score']
            ltp = {'name': 'LTP', 'res': ltp_score, 'baseline': '-', 'score': min(ltp_score, 1000) }
            details = {
                "lmbench": lmbench,
                "iozone": iozone,
                "iperf": iperf,
                "libcbench": libcbench,
                "netperf": netperf,
                "unixbench": unixbench,
                "cyclictest": cyclic,
                "ltp": [ltp]
            }
            # if stage == 2:
            if stage == 1:
                # score += sum(item["score"] for item in lmbench)
                for k, v in details.items():
                    s = 0
                    for item in v:
                        s += item['score']
                        passed_tests += 1 if item['score'] > 0 else 0
                    score += s
                    ranks[k] = s
            for v in test_results:
                key = v['name'].split()[0]
                ranks[key] = ranks.get(key, 0) + v['passed']

        # test_results = [[dict(r, name=x['name']) for r in x['results']] for x in test_results]
        # test_results = sum(test_results, [])
        # test_results = [dict(r, arg0=r['arg'][0], arg1=r['arg'][1]) for r in test_results]
        all_tests = sum([x['all'] for x in test_results])
        if all_tests == 0:
            all_tests = 1
        passed_tests = sum([x['passed'] for x in test_results])
        for _, v in details.items():
            for s in v:
                if s['score'] > 0:
                    passed_tests += 1
                all_tests += 1

        # score += int(passed_tests / all_tests * 100 + 0.5)
        if stage == 1:
            score += sum([x['passed'] for x in test_results])  # 阶段1
        info = {
            "all": all_tests,
            "passed": passed_tests,
            "start_time": job.get_log("START TIME"),
            "end_time": str(datetime.now(tz=pytz.timezone("Asia/Shanghai"))),
            "device": job.get_config()['server_dev'],
            "score": score,
            "time_test": time_test
        }
        comment = render_template("comment.html",
                                  results=test_results,
                                  info=info,
                                  final=config.get("final", False),
                                  details=details,
                                  stage=stage
                                  )
        # verdicts = [x['res'] for x in test_results]
        verdict = Verdict.AC if all_tests == passed_tests else Verdict.WA
    else:
        verdict = Verdict.RuntimeError
    if 'verdict' in summary:
        verdict = summary['verdict']

    # job.add_log("END TIME" + str(datetime.now(tz=pytz.timezone("Asia/Shanghai"))))
    job.del_log("START TIME")
    comment += render_template("logs.html", logs=job.get_logs())
    # log_table = render_template("logs.html", logs=job.get_logs())
    job.comment(comment)

    job.verdict(verdict)
    if time_test and time_test['time-test'] == 0:
        score = 0
    job.score(int(score))
    if not ranks:
        ranks = {"rank": str(score)}
    else:
        ranks["rank"] = str(score)
    job.rank(ranks)
    job.add_log_detail(f"AFTER_POSTWORK: {datetime.now()}", "time")


allow_table_header = {'pass':0, 'all':1, 'result':2, 'baseline':3, 'score':4}
def get_headers(results):
    ans = set()
    for item in results:
        for k in item.keys():
            if k in allow_table_header:
                ans.add(k)
    return ans, {x['name']: x for x in results}


# summary: arch -> group -> List[result]
def build_table(group, arch_list, summary):
    data = {}
    headers = set()
    names = set()
    for arch in arch_list:
        h, d = get_headers(summary.get(arch, {}).get(group, []))
        headers.update(h)
        data[arch] = d
        names.update(set(d.keys()))
    names = sorted(names)
    headers = sorted(list(headers), key=lambda x: allow_table_header[x])
    result = []
    score = 0
    score_col = {'#TOTAL': 0}
    for name in names:
        r = [name]
        sc = 0
        for arch in arch_list:
            for h in headers:
                r.append(data[arch].get(name, {}).get(h, '-'))
            sc += data[arch].get(name, {}).get('score', 0)
            score_col[arch] = score_col.get(arch, 0) + data[arch].get(name, {}).get('score', 0)
        r.append(sc)
        result.append(r)
        score += sc
        score_col['#TOTAL'] = score_col.get('#TOTAL', 0) + sc
    r = ['总分']
    for arch in arch_list:
        for h in headers:
            r.append(score_col[arch] if h == 'score' else '')
    r.append(score_col['#TOTAL'])
    result.append(r)

    return score_col, render_template("table.html", group=group, result=result, headers=headers, arch_list=arch_list)

cnt = 100
def download(filename, name):
    global cnt
    cnt += 1
    if not os.path.exists(filename):
        return ""
    file = open(filename)
    ans = file.read(1024 * 1024)
    if len(ans) == 1024 * 1024:
        ans += "\n...超过1MB的部分被截断..."
    return render_template("download.html", id=cnt, name=name, content=ans)


def postwork(job):
    summary = job.get_summary()[0]
    config = job.get_config()
    test_arch = ['rv', 'la']
    test_groups = set()
    for arch in test_arch:
        for key in summary.get(arch, {}).keys():
            test_groups.add(key)
    test_groups = sorted(test_groups)
    comment = ""

    score = 0
    rank = {}
    rank_table = {}
    rank_cols = set()
    sum_col = {}
    for group in test_groups:
        s, c = build_table(group, test_arch, summary)
        comment += c + "<br/>"
        score += s['#TOTAL']
        del s['#TOTAL']
        if len(s) == 0:
            s = {k: 0 for k in test_arch}
        # arch, score
        for ar, sc in s.items():
            k = f"{group}-{ar}"
            point, tag = k.split('-', 1)
            if point not in rank_table:
                rank_table[point] = {}
            rank_cols.add(tag)
            rank_table[point][tag] = sc
            rank[k] = sc
            sum_col[tag] = sum_col.get(tag, 0) + sc
    rank_cols = sorted(rank_cols)
    rank_rows = sorted(rank_table.keys())
    sum_row = {k: sum(rank_table[k].values()) for k in rank_table.keys()}
    info = {
        "start_time": job.get_log("START TIME"),
        "end_time": str(datetime.now(tz=pytz.timezone("Asia/Shanghai"))),
        "score": score,
        "rank": rank,
        "rank_cols": rank_cols,
        "rank_rows": rank_rows,
        "rank_table": rank_table,
        "sum_row": sum_row,
        "sum_col": sum_col,
    }
    comment = render_template("general.html", info=info) + comment
    if 'out_file_rv' in summary:
        comment += download(summary['out_file_rv'], "Riscv输出")
    if 'out_file_la' in summary:
        comment += download(summary['out_file_la'], 'LoongArch输出')

    comment += "<br/><br/>" + render_template("logs.html", logs=job.get_logs())

    rank['rank'] = score
    job.score(int(score))
    job.rank(rank)
    job.comment(comment)
    job.detail(render_template("logs.html", logs=job.get_logs_detail()))
    job.verdict("Accpted")


if __name__ == "__main__":
    job = Job()
    job.set_config({
        'testcase_dir':abspath("judge")
    })
    result = {}
    config = job.get_config()
    from kernel.run import parse_serial_out_new
    result['rv'] = parse_serial_out_new(config, "../output1.txt")
    result['la'] = parse_serial_out_new(config, "../output1.txt")
    result['out_file_rv'] = "judge/all_output_rv.txt"
    result['out_file_la'] = "judge/all_output.txt"
    job.set_summary([result])
    job.add_log( str(datetime.now(tz=pytz.timezone("Asia/Shanghai"))), "START TIME")
    job.set_config({"server_dev": "dev0"})
    postwork(job)
    print(job._JobBase__rank)
    print(job._JobBase__score)
    with open("comment.html", "w", encoding="utf-8") as f:
        f.write(job._JobBase__comment)

