"""
    Name: init_project.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: Initialize a pygrading project
    Coding: UTF-8
"""


import os
import pkgutil
from pygrading.utils import makedirs, writefile


def copy_file(pkg_path, target_path, name):
    data = pkgutil.get_data(__package__, pkg_path).decode()
    writefile(os.path.join(target_path, name), str(data))
    print(f"copy {pkg_path} done.")


def init(path=os.getcwd(), name="cg-kernel"):
    """ Initialize a pygrading project """

    print("Create project folder", end="")
    new_project_path = os.path.join(path, name)
    new_project_kernel_path = os.path.join(new_project_path, "kernel")
    new_project_template_path = os.path.join(new_project_kernel_path, "templates")

    html_template_path = os.path.join(new_project_template_path, "html")

    makedirs(new_project_template_path, exist_ok=True)
    makedirs(html_template_path, exist_ok=True)
    print("Create project folder success")

    print("Copy files start ===")
    copy_file("static/README.md", new_project_path, "README.md")
    copy_file("static/Makefile", new_project_path, "Makefile")
    copy_file("static/.gitignore", new_project_path, ".gitignore")
    copy_file("static/kernel/__init__.py", new_project_kernel_path, "__init__.py")
    copy_file("static/kernel/__main__.py", new_project_kernel_path, "__main__.py")
    copy_file("static/kernel/prework.py", new_project_kernel_path, "prework.py")
    copy_file("static/kernel/run.py", new_project_kernel_path, "run.py")
    copy_file("static/kernel/postwork.py", new_project_kernel_path, "postwork.py")
    copy_file("static/kernel/templates/__init__.py", new_project_template_path, "__init__.py")
    copy_file("static/kernel/templates/html/base.jinja", html_template_path, "base.jinja")
    copy_file("static/kernel/templates/html/index.html", html_template_path, "index.html")
    print("Copy files success")

    print("Initialization Completed!")
