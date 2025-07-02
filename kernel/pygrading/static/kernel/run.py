import pygrading as gg

from pygrading import Job, TestCases


def run(job: Job, case: TestCases.SingleTestCase) -> dict:
    """任务执行函数

    用于执行测试用例

    参数:
        job: 传入的当前任务对象
        case: 单独的测试用例对象

    返回值:
        result: 测试用例执行结果字典，该结果会被汇总到job对象的summary对象中
    """

    # 创建一个结果对象
    result = {"name": case.name, "score": 0}

    # 执行评测任务命令
    exec_result = gg.exec("echo success")

    if gg.utils.compare_str(exec_result.stdout, "success"):
        result["score"] = case.score

    return result
