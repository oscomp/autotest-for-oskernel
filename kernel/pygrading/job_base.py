"""
    Name: job_base.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: The main process of a grading.
    Coding: UTF-8
"""

import json
import types

from pygrading.testcase import TestCases
from pygrading.exception import FunctionsTypeError, FieldMissingError, DataTypeError


class JobBase(object):
    """ A Job is a work flow, using run() function to handle each testcase. """

    def __init__(
        self,
        prework: types.FunctionType = None,
        run: types.FunctionType = None,
        postwork: types.FunctionType = None,
        testcases: TestCases = TestCases(),
        config: dict = {"debug": False}
    ):
        """Init Job instance"""
        self.set_prework(prework)
        self.set_run(run)
        self.set_postwork(postwork)

        self.__testcases = testcases
        self.__config = config
        self.is_terminate = False

        self.__verdict = "Unknown"
        self.__score = 0
        self.__rank = {"rank": "-1.0"}
        self.__comment = ""
        self.__detail = ""
        self.__secret = ""
        self.__HTML = "enable"

        self.__json = {}
        self.__summary = []

        self.__log = {}
        self.__log_detail = {}

    def set_prework(self, prework: types.FunctionType):
        """ Set prework function for job """

        if not prework:
            self.prework = None
            return

        if not callable(prework):
            raise FunctionsTypeError("The prework object passed in is not of function type!")

        self.prework = prework

    def set_run(self, run: types.FunctionType):
        """ Set run function for job """

        if not run:
            self.run = None
            return

        if not callable(run):
            raise FunctionsTypeError("The run object passed in is not of function type!")

        self.run = run

    def set_postwork(self, postwork: types.FunctionType):
        """ Set postwork function for job """

        if not postwork:
            self.postwork = None
            return

        if not callable(postwork):
            raise FunctionsTypeError("The postwork object passed in is not of function type!")

        self.postwork = postwork

    def verdict(self, src: str):
        self.__verdict = src
        self.update_json()

    def score(self, src: int):
        self.__score = src
        self.update_json()

    def rank(self, src: dict):
        self.__rank = src
        self.update_json()

    def comment(self, src: str):
        self.__comment = src
        self.update_json()

    def detail(self, src: str):
        self.__detail = src
        self.update_json()

    def secret(self, src: str):
        self.__secret = src
        self.update_json()

    def HTML(self, src: str):
        self.__HTML = src
        self.update_json()

    def set_summary(self, summary: list):
        self.__summary = summary

    def get_summary(self):
        return self.__summary

    def set_config(self, config):
        self.__config = config

    def get_config(self):
        return self.__config

    def set_testcases(self, testcases):
        self.__testcases = testcases

    def get_testcases(self):
        return self.__testcases.get_testcases()

    def get_total_score(self):
        ret = 0
        for i in self.__summary:
            if type(i) == dict and "score" in i:
                ret += int(i["score"])
        return ret

    def update_json(self):
        self.__json["verdict"] = str(self.__verdict)

        try:
            self.__score = int(self.__score)
        except ValueError:
            raise DataTypeError("Score field must be integer!")

        self.__json["score"] = str(self.__score)

        if "rank" not in self.__rank:
            raise FieldMissingError("No 'rank' detected in super 'rank' field!")

        for k, v in self.__rank.items():
            try:
                num = float(v)
                self.__rank[k] = str(num)
            except ValueError:
                raise DataTypeError("Fields in 'rank' must be single-float!")

        self.__json["rank"] = self.__rank
        self.__json["HTML"] = str(self.__HTML)

        if self.__comment:
            self.__json["comment"] = str(self.__comment)
        elif "comment" in self.__json:
            del self.__json["comment"]

        if self.__detail:
            self.__json["detail"] = str(self.__detail)
        elif "detail" in self.__json:
            del self.__json["detail"]

        if self.__secret:
            self.__json["secret"] = str(self.__secret)
        elif "secret" in self.__json:
            del self.__json["secret"]

    def get_json(self):
        self.update_json()
        return self.__json

    def print(self, return_str=False):
        """ Print result json to stdout or return a json string """

        self.update_json()
        str_json = json.dumps(self.__json)

        if return_str is True:
            return str_json

        print(str_json)

    def add_log(self, content, key="log"):
        if key not in self.__log:
            self.__log[key] = ''
        self.__log[key] += content + "\n"

    def get_logs(self):
        return self.__log

    def get_log(self, key):
        return self.__log[key]

    def del_log(self, key):
        del self.__log[key]

    def add_log_detail(self, content, key="log"):
        if key not in self.__log_detail:
            self.__log_detail[key] = ''
        self.__log_detail[key] += content + "\n"

    def get_logs_detail(self):
        return self.__log_detail

