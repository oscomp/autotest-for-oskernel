import pygrading as gg

from prework import prework
from run import run
from postwork import postwork


if __name__ == '__main__':
    # 创建任务对象
    job = gg.Job(prework=prework, run=run, postwork=postwork)

    # 启动任务并配置最大线程数
    job.start(max_workers=1)

    # 输出结果JSON串
    job.print()
