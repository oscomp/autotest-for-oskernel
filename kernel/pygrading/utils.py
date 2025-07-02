"""
    Name: utils.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: A tool box contains many frequently used functions.
    Coding: UTF-8
"""

import os
import sys
import time
import shutil
import base64
import subprocess

from pygrading.html import img
from pygrading.exception import ExecError


class Exec(object):
    """Exec

    A Exec class instance contains all exec result.

    Attributes:
        cmd: Exec command.
        stdout: Standard output.
        stderr: Standard error.
        exec_time: Execute time.
        returncode: Return code.
    """

    def __init__(self, cmd: str, stdout: str, stderr: str, exec_time: int, returncode: int):
        self.cmd = cmd
        self.stdout = stdout
        self.stderr = stderr
        self.exec_time = exec_time
        self.returncode = returncode


def exec(cmd: str, input_str: str = "", time_out: int = None, queit: bool = True, env: dict = None) -> Exec:
    """Run a shell command with bash

    Args:
        cmd: A command string.
        input_str: Input resources for stdin.

    Returns:
        exec_result: A Exec instance.
    """
    begin = time.time()
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               encoding="utf8", env=env)
    out, err = process.communicate(input_str, timeout=time_out)
    end = time.time()
    exec_time = int((end - begin) * 1000)

    if process.returncode != 0 and not queit:
        raise ExecError(f"Error occurred when running command: {cmd}\n" + err)

    return Exec(cmd, out, err, exec_time, process.returncode)


def makedirs(path: str, exist_ok: bool = False):
    """ Make Dirs """
    os.makedirs(path, exist_ok=exist_ok)


def copyfile(src: str, dst: str):
    """Copy File"""
    shutil.copyfile(src, dst)


def copytree(src: str, dst: str):
    """Copy Tree"""
    shutil.copytree(src, dst)


def move(src: str, dst: str):
    """Move File"""
    shutil.move(src, dst)


def rmtree(src: str):
    """Remove Tree"""
    shutil.rmtree(src)


def rmfile(src: str):
    """Remove File"""
    os.remove(src)


def rename(old: str, new: str):
    """Rename File"""
    os.rename(old, new)


def writefile(src: str, lines: str, option: str = "w"):
    """ Write string to file """
    with open(src, option, encoding='utf-8') as f:
        f.write(lines)


def readfile(src: str) -> list:
    """
    Read file and return list.
    Auto remove blank line at the end of the file
    """
    with open(src, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].rstrip('\n')

        while "" == lines[-1]:
            lines.pop()

        return lines


def writefile_list(src: str, lines: list, option: str = "w"):
    """ Write string list to file """
    with open(src, option, encoding='utf-8') as f:
        f.writelines(lines)


def str2list(src: str) -> list:
    """Separate a string to a list by \n and ignore blank line at the end automatically."""
    ret = src.split("\n")
    while ret[-1] == "\n" or ret[-1] == "":
        ret.pop()
    return ret


def compare_str(str1: str, str2: str) -> bool:
    """Compare two string and ignore \n at the end of two strings."""
    return str1.rstrip() == str2.rstrip()


def compare_list(list1: list, list2: list) -> bool:
    """Compare two list and ignore \n at the end of two list."""
    while list1[-1] == "\n" or list1[-1] == "":
        list1.pop()
    while list2[-1] == "\n" or list2[-1] == "":
        list2.pop()
    return list1 == list2


def edit_distance(obj1, obj2) -> int:
    """Calculates the edit distance between obj1 and obj2"""
    edit = [[i + j for j in range(len(obj2) + 1)] for i in range(len(obj1) + 1)]

    for i in range(1, len(obj1) + 1):
        for j in range(1, len(obj2) + 1):
            if obj1[i - 1] == obj2[j - 1]:
                d = 0
            else:
                d = 1
            edit[i][j] = min(edit[i - 1][j] + 1, edit[i][j - 1] + 1, edit[i - 1][j - 1] + d)

    return edit[len(obj1)][len(obj2)]


def get_result_lines(stdout, tag) -> list:
    """ Get lines contains tag from stdout """
    return [raw for raw in stdout.split("\n") if tag in raw]


def get_result_dict(stdout, separater="=") -> list:
    """ Analyze stdout make it to a dict """
    lines, dic = [line for line in stdout.split("\n") if separater in line], {}

    for line in lines:
        key_val = line.split(separater)
        if len(key_val) != 2:
            continue
        else:
            dic[key_val[0].strip()] = key_val[1].strip()

    return dic


def img2base64(path):
    """ Transfore image to base64 string """
    image = "data:image/jpg;base64,"
    if os.path.exists(path):
        with open(path, "rb") as f:
            image += str(base64.b64encode(f.read()))[2:-1]

    return image


def get_image_element(path):
    """ Return a base64 image element """
    src = img2base64(path)
    return img(src=src, width="256")


def loge(message: str, config: dict = {}, key: str = "debug"):
    """ Print debug log to stdout """

    env = os.environ.get("PYGRADING_DEBUG")
    if env and env.lower() == "true":
        print(message, file=sys.stderr)
        return

    if key in config and config[key]:
        print(message, file=sys.stderr)
        return
