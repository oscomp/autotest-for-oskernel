from test_base import TestBase


class test4_test(TestBase):
    def __init__(self):
        super().__init__("test4", 2)

    def test(self, data):
        self.assert_equal(len(data), 1)
        self.assert_in("Write to pipe.", data[0])
