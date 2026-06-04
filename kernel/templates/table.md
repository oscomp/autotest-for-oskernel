### {{ group }}

| 测试点 | {% for item in arch_list %}{% for h in headers %}{{ item }}-{{ h }} | {% endfor %}{% endfor %}总分 |
|--------|{% for item in arch_list %}{% for h in headers %}----------|{% endfor %}{% endfor %}------|
{% for item in result %}| {% for x in item %}{{ x }} | {% endfor %}
{% endfor %}
