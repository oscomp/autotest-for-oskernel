"""
    Name: testcase.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: A module to generate testcase instance.
    Coding: UTF-8
"""

import os


class TestCases(object):
    """TestCases

    A TestCases class instance is a container of all test cases,
    each test case will be send to a run() function.

    Attributes:
        __count: An integer count of test cases loaded.
        __cases: An list of test cases.
        __total_score: The total score of all test cases.
    """

    class SingleTestCase(object):
        """SingleTestCase

        A SingleTestCase instance contains whole information of a test case.

        Attributes:
            name: The name of the test case.
            score: The score of the test case.
            input_src: The input content of the test case.
            output_src: The output content of the test case.
            extension: (Optional)The extension content of the test case which is customizable.
        """

        def __init__(self, name: str, score: int, input_src=None, output_src=None, extension=None):
            self.name = str(name)
            self.score = int(score)
            self.input_src = input_src
            self.output_src = output_src
            self.extension = extension

        def __str__(self):
            """Overview single cases."""
            ret = ["{}:\n".format(self.name),
                   "\tscore: {}\n".format(self.score),
                   "\tinput_src: {}\n".format(str(self.input_src)),
                   "\toutput_src: {}\n".format(str(self.output_src)),
                   "\textension: {}\n".format(str(self.extension))]
            return ''.join(ret)

    def __init__(self, count: int = 0, total_score: int = 100):
        """Init TestCases with empty values"""
        self.__count = count
        self.__cases = []
        self.__total_score = total_score

    def __str__(self):
        """Overview test cases."""
        ret = ["Cases Count: {}\n".format(self.__count), "Total Scare: {}\n".format(self.__total_score)]
        for case in self.__cases:
            ret.append("{}:\n".format(case.name))
            ret.append("\tscore: {}\n".format(case.score))
            ret.append("\tinput_src: {}\n".format(str(case.input_src)))
            ret.append("\toutput_src: {}\n".format(str(case.output_src)))
            ret.append("\textension: {}\n".format(str(case.extension)))
        return ''.join(ret)

    def get_count(self):
        return self.__count

    def get_total_score(self):
        return self.__total_score

    def get_testcases(self):
        return self.__cases

    def set_total_score(self, total_score: int):
        self.__total_score = total_score

    def isempty(self):
        return self.__count == 0

    def append(self, name: str, score: int, input_src=None, output_src=None, extension=None):
        """Add test case to list of test cases."""
        single_case = self.SingleTestCase(name, score, input_src, output_src, extension)
        self.__cases.append(single_case)
        self.__count += 1


def create_testcase(total_score: int = 100):
    """
    Create a empty TestCases instance

    Args:
        total_score: The total score of all test cases.

    Returns:
        test_cases: A instance of TestCases.
    """
    return TestCases(total_score=total_score)


def create_std_testcase(testcase_dir: str, testcase_num: int):
    """
    Create test cases in a recommended way.
    For example:
        testdata
        ├── input
        │   ├── input1.txt
        │   ├── input2.txt
        │   └── input3.txt
        └── output
            ├── output1.txt
            ├── output2.txt
            └── output3.txt

    Returns:
        test_cases: A instance of TestCases.

    Raises:
        IOError: A error occurred when missing file.
    """
    test_cases = TestCases()

    # Fix typing error
    testcase_num = int(testcase_num)

    for i in range(1, testcase_num + 1):

        input_scr = os.path.join(testcase_dir, "input", "input{}.txt".format(i))
        output_src = os.path.join(testcase_dir, "output", "output{}.txt".format(i))

        if not os.path.exists(input_scr):
            raise IOError("".join(["Missing file ", input_scr]))

        if not os.path.exists(output_src):
            raise IOError("".join(["Missing file ", output_src]))

        test_cases.append(
            name="TestCase{}".format(i),
            score=(test_cases.get_total_score() / testcase_num),
            input_src=input_scr,
            output_src=output_src
        )

    return test_cases
