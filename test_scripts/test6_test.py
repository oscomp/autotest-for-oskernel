from test_base import TestBase


class test6_test(TestBase):
    def __init__(self):
        super().__init__("test6", 2)

    def test(self, data):
        self.assert_equal(len(data), 1, "内容长度")
        self.assert_equal(data[0], "from fd 100")
        