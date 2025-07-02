import pygrading as gg

from pygrading import Job


def postwork(job: Job) -> dict:
    """任务后处理函数

    用于汇总测试执行结果

    参数:
        job: 传入的当前任务对象

    返回值:
        返回值为空，后处理内容需要更新到job对象中
    """

    # 获取执行结果总分
    total_score = job.get_total_score()

    # 更新结果输出字段
    job.verdict("Accepted" if total_score == 100 else "Wrong Answer")
    job.score(total_score)
    job.comment("Mission Complete")

    # 渲染 HTML 模板页面（可选）
    # 被渲染的页面应位于 kernel/templates/html 目录下
    job.detail(gg.render_template("index.html", author="Charles Zhang"))
