# import pygrading.general_test as gg
from pygrading.utils import exec
import os
import sys
import json
import time

only_run = ['rCore-Tutorial']
# only_run = ['xv6-k210']

#os/PQpwGe^Q]T
def test(image, usb_port):
    serial_out = "test/rCore-Tutorial/submit/k210_serial_out.txt"
    exec("rm "+ serial_out)
    start_time = time.time()
    test_src = os.path.join(os.getcwd(), 'test')
    print(test_src)
    if not os.path.exists(test_src):
        print("No test cases")
        exit(1)

    # test_result_src = os.path.join(os.getcwd(), "test_result")
    # os.makedirs(test_result_src, exist_ok=True)
    cmds = []
    # lst = [int(x) for x in os.listdir(test_src)]
    # lst = sorted(lst)
    # lst = [str(x) for x in lst]
    lst = os.listdir(test_src)
    statistic = {}
    for test in lst:
        # print(test)
        if only_run and test not in only_run:
            continue
        print('##run:::'+test)
        testcase = os.path.join(test_src, test)
        if not os.path.isdir(testcase):
            continue
        local_submit = os.path.join(testcase, "submit")
        local_testcase = os.path.join(testcase, "testdata")
        local_config = os.path.join(os.getcwd(), 'config.json')
        print(local_config)
        if not os.path.exists(local_config):
            print("No config file")
            exit(1)
        
        print('--------------------------------Enter docker--------------------------------')
        
        # docker_submit = '/mnt/cgsubmit'
        cmd = f"docker run --rm -i " \
              f"-e CONFIG_SRC=/mnt/config.json " \
              f"--mount type=bind,source=\"{local_config}\",target=\"/mnt/config.json\" " \
              f"--mount type=bind,source=\"{local_testcase}\",target=\"/coursegrader/testdata\" " \
              f"--mount type=bind,source=\"{local_submit}\",target=\"/coursegrader/submit\" " \
              f"--mount type=bind,source=\"{os.getcwd()}\",target=\"/home/cguser\" " \
              f"--device={usb_port} " \
              f"-u root {image} python3.7 /home/cguser/kernel.zip"
        # print(cmd)
        cmds.append(cmd)
        res = exec(cmd)
        print('--------------------------------Exit docker--------------------------------')
        print("\nStdout:\n")
        print(res.stdout)
        print("\nError:\n")
        print(res.stderr)
        try:
            res_json = json.loads(res.stdout)
        except:
            res_json = {"verdict": "Not Json", "score": 0}
            # os.system(cmd)
        print(f"test: {test} result: {res_json['verdict']} score: {res_json['score']}")

        if not res_json['verdict'] in statistic:
            statistic[res_json['verdict']] = []
        statistic[res_json['verdict']].append(test)

        result_src = os.path.join(testcase, f"result")
        os.makedirs(result_src, exist_ok=True)
        with open(os.path.join(result_src, 'result.json'), 'w') as f:
            f.write(res.stdout)
        with open(os.path.join(result_src, 'stderr.txt'), 'w') as f:
            f.write(res.stderr)
        with open(os.path.join(result_src, "result.html"), 'w') as f:
            f.write(str(res_json.get('comment', "No COMMENT</br>")))
            f.write(str(res_json.get('detail', "No DETAIL</br>")))

    for cmd in cmds:
        print(cmd)
    for k, v in statistic.items():
        if k == 'Accept':
            print(f"{k}: {len(v)}")
        else:
            print(f"{k}: {v}")
    end_time = time.time()
    time_use = end_time - start_time
    cur_time = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(end_time))

    record = open("record.txt","a+")
    out_path = "test/"+only_run[0]+"/submit/"
    if os.path.exists(out_path + "k210_serial_out.txt"):
        with open(out_path + "k210_serial_out.txt","r") as serial_output:
            count = len(serial_output.readlines())
    else :
        print("Run error, serial out file not exist, should record\n")
        count = 0
    if(count >= 90):
        record.write('['+cur_time + '] use:' + str(time_use) + "s Success\n")
    else:
        record.write('['+cur_time + '] use:' + str(time_use) + "s Failed\n")
        exec("cp"+ out_path + "k210_flash_out.txt record_output/k210_flash_out_"+cur_time+".txt")
        exec("cp"+ out_path + "sdcard_write.txt record_output/sdcard_write_"+cur_time+".txt")
        exec("cp"+ out_path + "k210_compile_out.txt record_output/k210_compile_out_"+cur_time+".txt")
        exec("cp"+ out_path + "k210_serial_out.txt record_output/k210_serial_out_"+cur_time+".txt")
        exec("cp"+ out_path + "sdcard_flash.txt record_output/sdcard_flash_"+cur_time+".txt")
    record.close()


if __name__ == '__main__':
    test(sys.argv[1],'/dev/ttyUSB0')
