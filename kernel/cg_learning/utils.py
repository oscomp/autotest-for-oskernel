import types

import requests
import urllib.parse


def get_file_sha256(file_path):
    """ 计算文件的 Sha256"""
    with open(file_path, "rb") as f:
        import hashlib
        sha256obj = hashlib.sha256()
        sha256obj.update(f.read())
        hash_value = sha256obj.hexdigest()
        return hash_value


def exec_function_with_timing(func: types.FunctionType, *args, **kargs):
    """ 计算函数调用时长 """
    import time
    begin = time.time()
    ret = func(*args, **kargs)
    end = time.time()
    total_time = int((end - begin) * 1000)
    return ret, total_time


def url_join_args(endpoint, api, params: dict=None, **kwargs):
    """拼接请求参数
    :param endpoint: 服务地址
    :param api: 接口，可带?或不带
    :param params: 请求参数
    :param kwargs: 未出现的参数，将组合成字典
    :return: 拼接好的url
    """
    result = endpoint + api
    if not result.endswith('?') and (params or kwargs):
        result = result + '?'
    if params:
        result = result + urllib.parse.urlencode(params)
    if kwargs:
        if params:
            result = result + '&' + urllib.parse.urlencode(kwargs)
        else:
            result = result + urllib.parse.urlencode(kwargs)
    return result


def post_request(endpoint, api, params: dict = None, upload_files: dict=None,
                 content_key: str="statements", content_data=None, headers: dict = None):
    """发起一个POST请求
    :param endpoint: 服务地址
    :param api: 接口，可带?或不带
    :param params: 请求参数
    :param upload_files: 要上传的文件{"key1": {"path": str}, "key2": {"path": str}....}
    :param content_key: content的表单键
    :param content_data: 要上传的非文件对象
    :param headers: 请求头
    :return: 拼接好的url
    """
    url = url_join_args(endpoint, api, params)
    import json
    files = {content_key: json.dumps(content_data)}
    if upload_files is not None:
        for key in upload_files.keys():
            file_info = upload_files[key]
            files[key] = open(file_info["path"], 'rb')

    res = requests.post(url, files=files, headers=headers)
    from cg_learning.tracker import debug
    debug(str(res.request.body))
    debug(str(res.content))
    return res.json
