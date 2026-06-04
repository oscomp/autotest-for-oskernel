**开始评测时间：** {{ info.start_time }}

**结束评测时间：** {{ info.end_time }}

**得分：** {{ info.score }}

**时间测试：** {{ info.time_test['time-test'] }}ms

{% if info.time_test['time-test'] == 0 %}
⚠️ **时间测试失败，此次提交成绩无效！**
{% endif %}

{% if stage == 1 %}
### 测试结果

| 测试样例名 | 通过测试点 | 全部测试点 |
|-----------|-----------|-----------|
{% for item in results %}| {{ item.name }} | {{ item.passed }} | {{ item.all }} |
{% endfor %}

{% endif %}

{% if final %}
{% for k, v in details.items() %}
### {{ k }}

| 测试点 | 运行结果 | 基准 | 得分 |
|-------|---------|------|------|
{% for item in v %}| {{ item.name }} | {{ item.res }} | {{ item.baseline }} | {{ item.score }} |
{% endfor %}

{% endfor %}
{% endif %}
