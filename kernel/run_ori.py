import traceback

import serial

from utils import loge
from verdict import Verdict


def run(job, testcase):
    try:
        return _run(job,testcase)
    except Exception as e:
        print(traceback.format_exc())
        raise e

def _run(job: gg.Job, testcase: gg.TestCases.SingleTestCase):
    config = job.get_config()
    result = {'name': testcase.name, 'score': 0}
    usb_port = config['usb_port']

    # ---FLASH---
    # input_str = gg.utils.readfile(str(testcase.input_src))
    loge("\n[k210 autotest]: Flash Start:\n")
    
    flash_cmd = f"kflash -b 3000000 -B dan {config['submit_dir']}/target/k210.bin -p {usb_port} > {config['submit_dir']}/k210_flash_out.txt"

    loge("\n[k210 autotest]:"+flash_cmd+"\n")
    outf = open(config['submit_dir'] + "/k210_serial_out.txt","w+")
    
    run_result = gg.utils.exec(flash_cmd)
    
    if run_result.returncode != config['return_code']:
        loge("FLASH ERROR")
        loge(run_result.stderr)
        result['verdict'] = Verdict.RuntimeError
        result['stderr'] = run_result.stderr
        result['return_code'] = run_result.returncode
        return result

    loge("\n[k210 autotest]: Flash Succeed:\n")
    
    loge("\n[k210 autotest]: Get Serial Out {usb_port}\n")
    # time.sleep(10)
    
    # ---RUN---
    # open serial
    ss = serial.Serial(usb_port, 115200, 
                    timeout=3, 
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS)
    if not ss.isOpen():
        loge("OPEN Serial fail")
        result['verdict'] = Verdict.UnknownError
        result['stderr'] = "OPEN Serial fail"
        result['return_code'] = 1
        return result
    loge("\n[k210 autotest]:"+str(ss)+"\n")

    loge("\n[k210 autotest]: Rebooting\n")

    # # read from serial
    loge("\n[k210 autotest]: Read from serial\n")
    # time_start  = time.time()
    ss.setDTR(False)
    ss.setRTS(True)
    ss.setRTS(False)
    # time.sleep(0.1)
    while(True):
        # cur_time = time.time()
        # use_time = cur_time - time_start
        data = ss.readline()
        try:
            data = data.decode()
        except UnicodeDecodeError:
            data = str(data)
        # loge("[k210 autotest]"+str(use_time) + ' ss:',end =' ')
        # loge(str(data), end = '')
        if len(data) == 0:
            break
        outf.write(str(data))
        outf.flush()
    outf.close()
    ss.close()

    result['output'] = run_result.stdout
    result['time'] = run_result.exec_time

    answer = gg.utils.readfile(str(testcase.output_src))
    result['answer'] = str(testcase.output_src)
    outp = gg.utils.readfile(config['submit_dir'] + "/k210_serial_out.txt")

    if gg.utils.compare_str(answer, outp):
        result['verdict'] = Verdict.Accept
        result['score'] = testcase.score
    else:
        result['verdict'] = Verdict.WrongAnswer
    return result
