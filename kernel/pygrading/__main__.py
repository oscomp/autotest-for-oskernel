"""
    Name: __main__.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: Main funcution for console application
    Coding: UTF-8
"""

import fire
import pygrading as gg

from pygrading.init_project import init


def version():
    print(gg.__version__)


if __name__ == "__main__":
    fire.Fire({
        "-v": version,
        "version": version,
        "init": init
    })
