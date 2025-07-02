import multiprocessing

import requests
import os
import shutil
# from concurrent.futures import ThreadPoolExecutor

from multiprocessing.dummy import Pool as ThreadPool, freeze_support

# groups = {
#     1998: "初赛",
#     2334: "决赛阶段1",
#     2388: "决赛阶段2",
#     2394: "现场赛"
# }

groups = {
4667: "k210",
4670: "unmatched"
}

pool = ThreadPool(16)
# freeze_support()

k210 = """
https://gitlab.eduxiji.net/educg-group-12100-765609/1911570-1951
https://gitlab.eduxiji.net/educg-group-12100-765609/2022os-test
https://gitlab.eduxiji.net/educg-group-12100-765609/20201947-44
https://gitlab.eduxiji.net/educg-group-12100-765609/853476998-820
https://gitlab.eduxiji.net/educg-group-12100-765609/910191774-1509
https://gitlab.eduxiji.net/educg-group-12100-765609/2019301887-2665
https://gitlab.eduxiji.net/educg-group-12100-765609/13119492637-1032
https://gitlab.eduxiji.net/educg-group-12100-765609/_404_-411
https://gitlab.eduxiji.net/educg-group-12100-765609/oskernel2022-byte-os
https://gitlab.eduxiji.net/educg-group-12100-765609/Augustus-2265
https://gitlab.eduxiji.net/educg-group-12100-765609/CG2019011412-3869
https://gitlab.eduxiji.net/educg-group-12100-765609/charon-2913
https://gitlab.eduxiji.net/educg-group-12100-765609/deng19992008-98
https://gitlab.eduxiji.net/educg-group-12100-765609/eulerfan-1843
https://gitlab.eduxiji.net/educg-group-12100-765609/Gxm-405
https://gitlab.eduxiji.net/educg-group-12100-765609/hu_jing-4036
https://gitlab.eduxiji.net/educg-group-12100-765609/jarvis-1146
https://gitlab.eduxiji.net/educg-group-12100-765609/LihuaSong02-1453
https://gitlab.eduxiji.net/educg-group-12100-765609/LiuJiLan-2638
https://gitlab.eduxiji.net/educg-group-12100-765609/PB20111623-22
https://gitlab.eduxiji.net/educg-group-12100-765609/Phil-1372
https://gitlab.eduxiji.net/educg-group-12100-765609/piper-3298
https://gitlab.eduxiji.net/educg-group-12100-765609/PTRNULL-694
https://gitlab.eduxiji.net/educg-group-12100-765609/qianpinyi-858
https://gitlab.eduxiji.net/educg-group-12100-765609/qpr-1946
https://gitlab.eduxiji.net/educg-group-12100-765609/sad-3353
https://gitlab.eduxiji.net/educg-group-12100-765609/Shiroko-2338
https://gitlab.eduxiji.net/educg-group-12100-765609/useg-151
https://gitlab.eduxiji.net/educg-group-12100-765609/USTB_NO1-3638
https://gitlab.eduxiji.net/educg-group-12100-765609/wangzhen-1279
https://gitlab.eduxiji.net/educg-group-12100-765609/waoa-2482
https://gitlab.eduxiji.net/educg-group-12100-765609/weihuan_tang-3790
https://gitlab.eduxiji.net/educg-group-12100-765609/yhwu_is-994
https://gitlab.eduxiji.net/educg-group-12100-765609/yyz-2267
https://gitlab.eduxiji.net/educg-group-12100-765609/youdaoli-team
https://gitlab.eduxiji.net/educg-group-12100-765609/Zhohfut-2930
https://gitlab.eduxiji.net/educg-group-12100-765609/oskernel2022-oops
https://gitlab.eduxiji.net/educg-group-12100-765609/oskernel2022-segmentfault
https://gitlab.eduxiji.net/educg-group-12100-765609/oskernel2022-lotusos
https://gitlab.eduxiji.net/educg-group-12100-765609/2022os-c-core
https://gitlab.eduxiji.net/educg-group-12100-765609/oskernel2022-toyos
https://gitlab.eduxiji.net/educg-group-12100-765609/oscomp2022_core
https://gitlab.eduxiji.net/educg-group-12100-765609/oskernel2021-neuos
https://gitlab.eduxiji.net/educg-group-12100-765609/ucore-smp
https://gitlab.eduxiji.net/educg-group-13484-858191/2022OS
https://gitlab.eduxiji.net/educg-group-12100-765609/oskernel2022-los
https://gitlab.eduxiji.net/educg-group-12100-765609/gl-os
https://gitlab.eduxiji.net/educg-group-12100-765609/os
""".split()


# def clone(item):
#     path = os.path.join(os.getcwd(), "repos", group_name, item['name'])
#     if os.path.exists(path):
#         shutil.rmtree(path)
#     os.makedirs(path, exist_ok=True)
#     git_url = item['http_url_to_repo']
#     print(f"cloning {git_url} to {path}")
#     os.system(f"git clone {git_url} '{path}'")
#     return path


def clone(item):
    url = item
    name = item.split('/')[-1]
    path = os.path.join(os.getcwd(), "repos", 'k210', item)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)
    # git_url = item['http_url_to_repo']
    # print(f"cloning {git_url} to {path}")
    os.system(f"git clone {item} '{name}'")
    return path

for key, group_name in groups.items():
    # get_proj_url = f"https://gitlab.eduxiji.net/api/v4/groups/{key}/projects"
    # result = requests.get(get_proj_url).json()
    p = multiprocessing.Pool(processes=15)
    _ = [p.apply_async(func=clone, args=(i,)) for i in k210]
    p.close()
    p.join()

# find repos/ -name Cargo.toml | sed 's/^repos\///g' | sed 's/Cargo.toml//g' | xargs -I {} mkdir -p cargo.toml/{}
# find repos/ -name Cargo.toml | sed 's/^repos\///g' | xargs -I cp repos/{} cargo.toml/{}
