from test_base import TestBase


class test3_test(TestBase):
    def __init__(self):
        super().__init__("test3", 2)

    def test(self, data):
        self.assert_in_str("parent process", data)
        self.assert_in_str("child process", data)
