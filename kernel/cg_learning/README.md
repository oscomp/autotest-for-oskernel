<h1>
    CG Learning Tracker
</h1>

针对PyGrading测评框架的测评数据采集工具，既支持对整个测评流程和每个测试用例的数据自动采集，也支持添加自定义采集数据

## 采集配置

采集配置来源于Job配置和环境变量，现支持配置项如下：

| 配置项  | 来源| 含义| 是否可缺省| 缺省值|
| ---------- | -----------| -----------| -----------| -----------|
| track_grading_enable   | Job   | 是否自动采集整体测评数据,该项为False时自动禁用测试用例的数据采集| 是| False|
| track_testcase_enable   | Job   | 是否自动采集每个测试用例的测评数据| 是| True|
| track_lrs_endpoint   | Job   | 接收采集数据的LRS服务地址| 否| -|
| track_jwt_secret   | Job   | 用于JWT签名的密钥| 是| -|
| track_jwt   | Job   | 用于验证的JWT| 是| -|
| track_debug_enable   | Job   | 是否打印调试信息| 是| False|
| track_http_enable   | Job   | 是否将采集的数据自动发送至LRS| 是| True|
| track_file_dir   | Job   | 附件本地保存目录| 是| /var/tmp/cg_learning|
| track_jwt_token   | 环境变量   | 用于验证的JWT| 是| -|
| track_root_statement   | 环境变量   | 本次测评的来源Statement| 是| -|
| track_root_activity   | 环境变量   | 本次测评的Activity| 是| http://learning.educg.net/activity#program_project|


## 可自动采集的数据

整体测评：

1. 测评配置数据(即job.get_config())
2. 测评消耗的时间
3. 测评的结果
4. 测评的错误信息(即在pre_work、run或post_work中抛出的异常)

用例测评：

1. 测评消耗的时间
2. 测评的结果
3. 测评的错误信息


## Q&A

### 1.如何在整体测评或用例测评中添加自定义的采集数据？

采集工具会自动采集整体或用例的测评结果，因此在`run`中直接返回需要采集的数据即可

或者可先通过`get_current_statement()`方法获取当前采集Statement，使用`add_result_extension`方法添加结果数据、使用`add_attachment`方法添加附件、使用`add_context_extensions`方法添加上下文信息

具体样例可参考测试文件中的`test_with_custom_statistics`测试用例

### 2.如何添加自定义的采集事件？

可先通过`new_statement_instance`方法生成新的Statement，然后设置上下文、填写采集数据即可

具体样例可参考测试文件中的`test_with_custom_event`测试用例

