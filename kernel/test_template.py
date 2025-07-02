from pygrading.render import Render, render_template

data = [
    {
        "name": f"name{a}",
        "arg0": f"arg0{a}",
        "rep": f"rep{a}",
        "arg1": f"arg1{a}",
        "res": f"res{a}",
        "msg": f"msg{a}",
    }
    for a in range(10)
]

logs = [
    {
        "name": f"name{a}",
        "content": f"contenta{a}"
    }
    for a in range(20)
]

r = render_template("comment.html", results=data, logs=logs)
with open("test.html", "w", encoding='utf-8') as f:
    f.write(r)
