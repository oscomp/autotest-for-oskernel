from test_base import TestBase
import re


class test2_test(TestBase):
    def __init__(self):
        super().__init__("test2", 3)

    def test(self, data):
        self.assert_equal(len(data), 3)
        heap1 = int(re.findall(r"\[test3 ori]Before alloc,heap  pos: (\d+)", data[0])[0])
        heap2 = int(re.findall(r"\[test3 ori]After alloc,heap pos: (\d+)", data[1])[0])
        heap3 = int(re.findall(r"\[test3 ori]Alloc again,heap pos: (\d+)", data[2])[0])
        self.assert_equal(heap2, heap1 + 64)
        self.assert_equal(heap3, heap1 + 128)

