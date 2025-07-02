import json
import sys
import os
import re
import importlib

file_path = os.path.split(os.path.realpath(__file__))[0]

test_file_pattern = re.compile(r"(.+)_test\.py")

tests = []

for name in os.listdir(file_path):
    t = test_file_pattern.findall(name)
    if not t:
        continue
    t = t[0]
    tests.append(getattr(importlib.import_module(f"{t}_test"), t + "_test")())

runner = {x.name: x for x in tests}
print(runner.keys(), file=sys.stderr)


def generate_result(name, data):
    res = len(data) == 1 and data[0].strip() == 'Pass!'
    result = [{
            "rep": "=",
            "res": res,
            "arg": data,
            "msg": ""
        }]
    return {
        "name": name,
        "results": result,
        "all": 1,
        "passed": len([x for x in result if x['res']])
    }


def get_runner(name):
    # return runner.get(name, runner.get("test_"+name, runner[name+"_test"]))
    return runner.get(name, None)


# print(runner)


if __name__ == '__main__':
    file_name = sys.argv[1]
    try:
        serial_out = open(file_name, encoding='utf-8').read()
    except UnicodeDecodeError:
        serial_out = open(file_name, 'rb').read().decode(errors='ignore')
    serial_out = serial_out.split('\n')

    test_name = None
    state = 0
    data = []
    result_map = {}
    for line in serial_out:
        if line in ('', '\n'):
            continue
        if state == 0:
            # 寻找测试样例开头
            if "========== START " in line:
                test_name = line.replace("=", '').replace(" ", "").replace("START", "")
                if data:
                    # 只找到了开头没找到结尾，说明某个样例内部使用assert提前退出
                    r = get_runner(test_name)
                    if r:
                        r.start(data)
                    else:
                        result_map[test_name] = generate_result(test_name, data)
                data = []
                state = 1
        elif state == 1:
            if "========== END " in line:
                # 测试样例结尾
                r = get_runner(test_name)
                if r:
                    r.start(data)
                else:
                    result_map[test_name] = generate_result(test_name, data)
                state = 0
                data = []
                continue
            elif "========== START " in line:
                data = []
                test_name = line.replace("=", '').replace(" ", "").replace("START", "")
                continue
            # 测试样例中间
            data.append(line)

    all_tests = [''.join(x.split()[2:]) for x in open(os.path.join(file_path, "run-static.sh")).readlines()]
    all_tests += [''.join(x.split()[2:]) for x in open(os.path.join(file_path, "run-dynamic.sh")).readlines()]
    miss_tests = [x for x in all_tests if x not in result_map]
    for key in result_map.keys():
        if key not in all_tests:
            result_map[key]['passed'] = 0
    for miss in miss_tests:
        result_map[miss] = generate_result(miss, "")
    test_results = [x.get_result() for x in tests] + [x for x in result_map.values()]
    for x in test_results:
        x['name'] = x['name'].replace('.exe', ' ')
    test_results = sorted(test_results, key=lambda x: x['name'])
    print(json.dumps(test_results))
