"""
    Name: job_run.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: Job running process.
    Coding: UTF-8
"""

import inspect

from concurrent.futures import ThreadPoolExecutor

from pygrading.job_base import JobBase
from pygrading.exception import FunctionArgsError


class Job(JobBase):
    """ Running a job and support multi-threading """

    # @learning_tracker_grading
    def start(self, max_workers: int = 1):
        """ start a job """

        # run prework
        if self.prework:
            prework_inspect = inspect.getfullargspec(self.prework)

            if not prework_inspect.args:
                self.prework()
            elif len(prework_inspect.args) == 1:
                self.prework(self)
            else:
                raise FunctionArgsError("Prework function supports\n\t1. prework()\n\t2. prework(job: Job)")

        if self.is_terminate:
            return self.print(return_str=True)

        # get testcases and bind with job obj
        testcases = [(self, case) for case in self.get_testcases()]

        # create a thradd pool
        #@learning_tracker_test_case
        def outer_run(args):
            """
            support these four situations:
            1. run(job, testcase)
            2. run(testcase)
            3. run(job)
            4. run()
            """
            run_inspect = inspect.getfullargspec(self.run)

            if not run_inspect.args:
                return self.run()
            elif len(run_inspect.args) == 2:
                return self.run(*args)
            elif len(run_inspect.args) == 1:
                if run_inspect.args[0] == "job":
                    return self.run(args[0])
                elif run_inspect.args[0] == "case":
                    return self.run(args[1])
            else:
                raise FunctionArgsError(
                    "Run function supports\n\t" +
                    "1. run()\n\t" +
                    "2. run(job: Job)\n\t" +
                    "3. run(case: TestCases.SingleTestCase)\n\t" +
                    "4. run(job: Job, case: TestCases.SingleTestCase)\n\t"
                )

        if self.run:
            with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="job_") as pool:
                self.set_summary([result for result in pool.map(outer_run, testcases)])

        # run postwork
        if self.postwork:
            postwork_inspect = inspect.getfullargspec(self.postwork)

            if not postwork_inspect.args:
                self.postwork()
            elif len(postwork_inspect.args) == 1:
                self.postwork(self)
            else:
                raise FunctionArgsError("Postwork function supports\n\t1. prework()\n\t2. prework(job: Job)")

        return self.print(return_str=True)
