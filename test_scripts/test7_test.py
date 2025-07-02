from test_base import TestBase


class test7_test(TestBase):
    def __init__(self):
        super().__init__("test7", 1)

    def test(self, data):
        self.assert_great(len(data), 1)
