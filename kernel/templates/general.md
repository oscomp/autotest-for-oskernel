# 评测完成

**开始时间：** {{ info.start_time }}

**结束时间：** {{ info.end_time }}

**总分：** {{ info.score }}

## 得分详情

| 测试点 | {% for k in info.rank_cols %}{{ k }} | {% endfor %}总分 |
|--------|{% for k in info.rank_cols %}------|{% endfor %}------|
{% for row in info.rank_rows %}| {{ row }} | {% for col in info.rank_cols %}{% if row in info.rank_table %}{% if col in info.rank_table[row] %}{{ info.rank_table[row][col] }}{% else %}-{% endif %}{% else %}-{% endif %} | {% endfor %}{{ info.sum_row[row] }} |
{% endfor %}| **总分** | {% for col in info.rank_cols %}{{ info.sum_col[col] }} | {% endfor %}**{{ info.score }}** |

