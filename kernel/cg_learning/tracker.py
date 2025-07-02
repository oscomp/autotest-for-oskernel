import copy
import os
import threading
from functools import wraps

import jwt as jwt
from Cython.Utils import OrderedSet

from cg_learning.models import Statement, Verb, Actor, Activity
from cg_learning.utils import exec_function_with_timing, get_file_sha256
from pygrading.exception import ExecError
from pygrading.utils import copyfile, makedirs

track_grading_enable_config_key = "track_grading_enable"
track_testcase_enable_config_key = "track_testcase_enable"
track_lrs_endpoint_config_key = "track_lrs_endpoint"
track_auth_jwt_secret_config_key = "track_jwt_secret"
track_auth_jwt_config_key = "track_jwt"
track_debug_config_key = "track_debug_enable"
track_http_enable_config_key = "track_http_enable"
track_file_back_up_dir_config_key = "track_file_dir"

track_auth_jwt_env_key = "track_jwt_token"
track_root_statement_env_key = "track_root_statement"
track_root_activity_env_key = "track_root_activity"
track_depend_env_key = [track_auth_jwt_env_key, track_root_statement_env_key,
                        track_root_activity_env_key]

default_concept_domain = 'http://learning.educg.net'
default_grading_verb = Verb(f"{default_concept_domain}/verb?word=通用评测", meaning_zh="通用评测")
default_grading_actor = Actor(Actor.Account(default_concept_domain, 'Python Grading Kernel'))
default_grading_activity = Activity(f'{default_concept_domain}/activity?type=PythonGrading',
                                    name='program_project',
                                    activity_type=f'{default_concept_domain}/activity?type=EngineeringPractice',
                                    description={'en': 'A program project written by a student or a study team',
                                                 'zh': '一个学生或者一个学习小组编写的工程项目'})
default_file_back_up_dir = "/var/tmp/cg_learning"

local_statements = threading.local()
grading_statement = None
statements_queue = OrderedSet()
track_config = {}
file_hash_map = {}


def load_config(job_config):
    """根据测评配置更新采集配置(该方法不应在本模块外调用)"""
    if job_config is None:
        return
    track_config.update(job_config)


def load_env():
    """根据环境变量更新采集配置(该方法不应在本模块外调用)"""
    for key in track_depend_env_key:
        value = os.environ.get(key, None)
        if value:
            track_config[key] = value


def build_the_verb(verb, domain: str=default_concept_domain):
    """构建一个动词"""
    return Verb(f'{domain}/verb#{verb}')


def get_grading_statement():
    """获取测评Statement"""
    return grading_statement


def debug(info: str, condition: bool = True, error: bool = False):
    """当track_debug_config_key对应的配置值为True时打印调试信息
    :param info: 要打印的信息
    :param condition: 条件
    :param error: 是否使用error输出
    """
    if track_config.get(track_debug_config_key, False) and condition:
        import logging
        import sys
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)
        try:
            logging.error(info) if error else logging.debug(info)
        finally:
            logger.removeHandler(stream_handler)


def set_current_statement(statement: Statement):
    """设置当前正在采集的Statement(该方法不应在本模块外调用)"""
    if not hasattr(local_statements, 's') or local_statements.s is None:
        local_statements.s = []
    debug(f'set current statement {statement.statement_id} in thread {threading.current_thread().name}')
    local_statements.s.append(statement)


def get_current_statement():
    """获取当前正在采集的Statement"""
    if not hasattr(local_statements, 's') or local_statements.s is None or len(local_statements.s) == 0:
        debug(f'retrieve fail in thread {threading.current_thread().name}')
        return None
    return local_statements.s[-1]


def submit_statement(statement: Statement):
    """提交一个Statement到待发送队列中(该方法不建议在本模块外调用)"""
    statements_queue.add(statement)


def get_statements_queue():
    """获取当前待发送的Statement队列"""
    return copy.deepcopy(statements_queue)


def clear_statements_queue():
    """清空Statement队列(该方法不建议在本模块外调用)"""
    global statements_queue
    statements_queue = OrderedSet()


def new_statement_instance(actor: Actor=default_grading_actor, verb: Verb=default_grading_verb,
                           auto_submit: bool = True):
    """创建一个新的Statement实例
    :param actor: 执行人
    :param verb: 执行的动作
    :param auto_submit 是否提交到发送队列
    :return 新的Statement实例
    """
    statement = Statement(actor=actor, verb=verb)
    if auto_submit:
        submit_statement(statement)
    return statement


def pop_current_statement():
    """跳入正确的采集语句(该方法不应在本模块外调用)"""
    if local_statements.s is None or len(local_statements.s) == 0:
        debug(f'pop fail in thread {threading.current_thread().name}')
        return None
    return local_statements.s.pop()


def add_attachment(statement: Statement, file_path: str, ignore_if_not_exists: bool = False,
                   usage_type: str = None, description: dict = None):
    """采集一个文件
    :param statement: 该文件关联的Statement
    :param file_path: 文件路径
    :param ignore_if_not_exists: 文件不存在时是否忽略
    :param usage_type: 文件的用途IRI,如"http://learning.educg.net/attachments/type/mips"
    :param description: 文件描述 {"zh":"编译测评中间生成的mips文件"}
    """
    if not os.path.exists(file_path):
        if not ignore_if_not_exists:
            raise ExecError(f"{file_path} not exists")
        return
    if os.path.isdir(file_path):
        raise ExecError(f"{file_path} is a dir")
    sha_code = get_file_sha256(file_path)
    file_dir_path, file_name = os.path.split(file_path)
    backup_dir = track_config.get(track_file_back_up_dir_config_key, default_file_back_up_dir) + os.path.sep + sha_code
    makedirs(backup_dir, True)
    target_path = backup_dir + os.path.sep + file_name
    statement.add_attachment(sha_code, target_path, usage_type=usage_type, description=description)
    if not os.path.exists(target_path):
        copyfile(file_path, target_path)


def learning_tracker_grading(job_start_func):
    """通用测评装饰器，该装饰器仅能用于Job.start方法"""
    @wraps(job_start_func)
    def _wrapper(*args, **kargs):
        job = args[0]
        if not job.get_config().get(track_grading_enable_config_key, False):
            return job_start_func(*args, **kargs)
        load_env()
        load_config(job.get_config())
        statement = new_statement_instance()
        set_current_statement(statement)
        global grading_statement
        grading_statement = statement
        statement.context_statement_id = track_config.get(track_root_statement_env_key, None)
        debug("root statement is None", statement.context_statement_id is None)
        root_activity_id = track_config.get(track_root_activity_env_key, None)
        activity = Activity(root_activity_id) if root_activity_id is not None else default_grading_activity
        statement.object_activity = activity
        debug("using default activity as root activity", root_activity_id is None, error=True)
        statement.context_extensions = copy.deepcopy(job.get_config())
        # remove jwt secret
        if statement.context_extensions and track_auth_jwt_secret_config_key in statement.context_extensions:
            del statement.context_extensions[track_auth_jwt_secret_config_key]
        # remove jwt
        if statement.context_extensions and track_auth_jwt_config_key in statement.context_extensions:
            del statement.context_extensions[track_auth_jwt_config_key]
        total_time = 0
        try:
            # job_start_func(*args, **kargs)
            ret, total_time = exec_function_with_timing(job_start_func, *args, **kargs)
            # set result_completion=True when not set and not raise an exception
            if statement.result_completion is None:
                statement.result_completion = True
            return ret
        except Exception as ex:
            statement.add_result_extension("exception", str(ex))
            raise ex
        finally:
            if statement.result_score_min is None:
                statement.result_score_min = 0
            if statement.result_score_max is None:
                statement.result_score_max = 0
                for case in job.get_testcases():
                    statement.result_score_max += case.score
            statement.result_duration = total_time
            # get the result from get_json function instead of ret
            statement.update_result_extensions(job.get_json(), True)
            pop_current_statement()
            upload_statements(job.get_config())

    return _wrapper


def learning_tracker_test_case(run_func):
    """用例测评装饰器，该装饰器仅能用于Job.start.outer_run方法"""
    @wraps(run_func)
    def _wrapper(*args, **kargs):
        job, test_case = args[0]
        if not job.get_config().get(track_grading_enable_config_key, False) or \
                not job.get_config().get(track_testcase_enable_config_key, True):
            return run_func(*args, **kargs)
        load_config(job.get_config())
        statement = new_statement_instance()
        set_current_statement(statement)
        statement.context_statement_id = str(grading_statement.statement_id)
        statement.add_context_activity(Statement.ContextActivityType.Parent,
                                       grading_statement.object_activity.activity_id)
        activity = Activity(f"{default_concept_domain}/activity?type=testcase&name={test_case.name}")
        activity.type = f"{default_concept_domain}/type#testcase"
        statement.object_activity = activity
        statement.result_score_max = test_case.score
        statement.result_score_min = 0
        ret = None
        total_time = 0
        try:
            ret, total_time = exec_function_with_timing(run_func, *args, **kargs)
            # set result_completion=True when not set and not throw an exception
            if statement.result_completion is None:
                statement.result_completion = True
            return ret
        except Exception as ex:
            statement.add_result_extension("exception", str(ex))
            raise ex
        finally:
            statement.result_duration = total_time
            result = ret
            if type(ret) == int or type(ret) == float:
                result = {"score": result}
            elif type(ret) != dict:
                result = {"case_result": result}
            statement.update_result_extensions(result, True)
            pop_current_statement()

    return _wrapper


def generate_authorization_header(config):
    """根据Job配置生成用于验证的Token"""
    auth_token = os.environ.get(track_auth_jwt_env_key, None)
    if auth_token:
        return auth_token
    auth_token = config.get(track_auth_jwt_config_key, None)
    if auth_token:
        return auth_token
    secret = config.get(track_auth_jwt_secret_config_key, None)
    if secret is None:
        return None
    token_dict = {"iss": default_grading_actor.account.home_page,
                  "name": default_grading_actor.account.name}
    return jwt.encode(token_dict, secret)


def upload_statements(config):
    """向LRS服务器发送所有待发送的Statement(该方法不应在本模块外调用)"""
    if track_config.get(track_debug_config_key, False):
        if not statements_queue:
            debug('empty statement queue')
        for statement in statements_queue:
            debug(f'statement in queue: {statement}')
    lrs_endpoint = config.get(track_lrs_endpoint_config_key)
    if lrs_endpoint is None:
        debug('missing endpoint info', error=True)
        return
    token = generate_authorization_header(config)
    headers = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    else:
        debug("missing access token", error=True)
        return
    if track_config.get(track_http_enable_config_key, True):
        files = {}
        statements = []
        for statement in statements_queue:
            statements.append(statement.to_dict())
            attachment = statement.get_attachments()
            if attachment:
                files.update(attachment)
        try:
            from cg_learning.utils import post_request
            post_request(lrs_endpoint, '/xAPI/statements', None,
                         content_data=statements, upload_files=files, headers=headers)
        except Exception as ex:
                debug(str(ex), error=True)
    else:
        debug('disable http request')
