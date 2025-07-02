"""
    Name: configuration.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: A module to load config file.
    Coding: UTF-8
"""

import json
from typing import Dict


def load_config(source: str) -> Dict:
    """Load Configuration File

    Reads the configuration file and returns it as a dictionary.

    Args:
        source: Configuration file path.

    Returns:
        A dict of config information.

        For example:
        {'testcase_num': '3',
        'testcase_dir': 'example/testdata',
        'submit_path': 'example/submit/*',
        'exec_path': 'example/exec/student.exec'}

    Raises:
        IOError: A error occurred when missing config file.
    """
    f = open(source, encoding='utf-8')
    return json.load(f)
