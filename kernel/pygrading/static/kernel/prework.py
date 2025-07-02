import pygrading as gg

from pygrading import Job


def prework(job: Job):
    """任务预处理函数

    通常用于创建测试用例和创建配置信息

    参数:
        job: 传入的当前任务对象

    返回值:
        返回值为空，预处理内容需要更新到job对象中
    """

    # 创建测试用例和配置信息
    config = {"debug": False}

    testcases = gg.create_testcase(100)
    testcases.append(name="TestCase1", score=50, input_src="", output_src="")
    testcases.append(name="TestCase2", score=50, input_src="", output_src="")

    # 更新测试用例和配置信息到任务
    job.set_config(config)
    job.set_testcases(testcases)
