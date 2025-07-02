from pygrading.html import *
from verdict import Verdict

# data = {
#     'name': '4位全加器',
#     'score': 100,
#     'detail': [
#         {'name': 'TestCase1', 'time': 750, 'stdout': "balabala", 'answer': "hahahahha", 'score': "14", 'verdict': 'Accept'},
#         {'name': 'TestCase1', 'time': 750, 'stdout': "balabala", 'answer': "hahahahha", 'score': "14", 'verdict': 'Accept'},
#     ]
# }
#
# title   = ['name', 'score']  # 输出报告标头内容
# summary = ['name', 'time', 'score', 'verdict']  # 摘要内容
# details = ['input', 'stdout', 'answer']  # 细节内容


def make_table(data, summary):
    ans = table(border="1")
    # 创建表头
    thead = tr()
    for key in summary:
        thead << th().set_text(key)
    ans << thead

    # 创建表主体
    for test in data:
        # print(data)
        row = tr()
        for key in summary:
            row << td().set_text(str2html(str(test[key])))
        ans << row

    return str(ans)


def make_log_table(logs):
    ans = table(border='1')
    if "error" in logs:
        ans << (tr() << td().set_text("<div style=\"color: red;\">error</div>"))
        ans << (tr() << td().set_text(f"<div style=\"color: red;\">{str2html(logs['error'])}</div>"))
    for k, v in logs.items():
        ans << (tr() << td().set_text("<b>" + str2html(k) + "</b>"))
        ans << (tr() << td().set_text(str2html(v)))
    return str(ans)


def make_one_line_table(data, header):
    tab = table(border="1")
    tab << tr(th(colspan=str(len(header))).set_text(data['name']))
    thead = tr()
    for key in header:
        thead << th().set_text(key)
    tab << thead

    # 创建表主体
    row = tr()
    for key in header:
        row << td().set_text(str2html(str(data[key])))
    tab << row
    return str(tab)


# verdicts = ['Accept', 'Accept', 'Wrong Answer']
def make_verdict(verdicts: list):
    for x in verdicts:
        if x != Verdict.Accept:
            return x
    return Verdict.Accept
