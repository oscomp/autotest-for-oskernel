from test_base import TestBase
import re


class test5_test(TestBase):
    def __init__(self):
        super().__init__("test5", 3)

    def test(self, data):
        self.assert_equal(len(data), 1, "内容长度")
        new_fd = re.findall(r"new fd is (\d+)", data[0])
        self.assert_equal(len(new_fd), 1, "存在新文件描述符")
        self.assert_great(int(new_fd[0]), 3, "新文件描述符值")
