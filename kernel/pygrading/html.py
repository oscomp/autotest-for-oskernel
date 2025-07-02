"""
    Name: html.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: A module to generate html code.
    Coding: UTF-8
"""


def str2html(src: str) -> str:
    """Switch normal string to a html type"""
    if not src:
        return ""
    str_list = src.split("\n")
    while str_list and (str_list[-1] == "\n" or str_list[-1] == ""):
        str_list.pop()

    if not str_list:
        return "<br>"

    for i in range(len(str_list) - 1):
        str_list[i] += "<br>"

    return "".join(str_list)


class SingleTag(object):
    """Tag

    A super class of all single html tag class.

    Attributes:
        name: Tag name.
        attributes: Attributes of this tag.
    """

    def __init__(self, **attributes):
        self.name = "tag"
        self.attributes = attributes

    def __str__(self):
        ret = ["".join(["<", self.name])]
        for key, value in self.attributes.items():
            ret.append("".join([" ", key, "=", "'", value, "'"]))
        ret.append(">")

        return "".join(ret)

    def print(self):
        print(str(self))


class Tag(object):
    """Tag

    A super class of all pair html tag class.

    Attributes:
        text: Text content.
        name: Tag name.
        subtag: Sub tags.
        attributes: Attributes of this tag.
    """

    def __init__(self, *subtag, **attributes):
        self.text = ""
        self.name = "tag"

        for tag in subtag:
            if (not isinstance(tag, Tag)) and (not isinstance(tag, SingleTag)):
                raise ValueError(str(tag) + "is not a subtag.")

        self.subtag = []
        for tag in subtag:
            self.subtag.append(tag)

        self.attributes = attributes

    def __str__(self):
        ret = []

        pre = ["".join(["<", self.name])]
        for key, value in self.attributes.items():
            pre.append("".join([" ", key, "=", "'", value, "'"]))
        pre.append(">")
        ret.append("".join(pre))

        if self.text:
            ret.append(self.text)

        for s in self.subtag:
            ret.append(str(s))

        ret.append("".join(["</", self.name, ">"]))

        return "".join(ret)

    def __lshift__(self, other):
        if not isinstance(other, Tag):
            raise ValueError(str(other) + "is not a subtag.")
        self.subtag.append(other)
        return self

    def append(self, obj):
        if not isinstance(obj, Tag):
            raise ValueError(str(obj) + "is not a subtag.")
        self.subtag.append(obj)

    def pop(self, index=-1):
        self.subtag.pop(index)

    def insert(self, index, obj):
        if not isinstance(obj, Tag):
            raise ValueError(str(obj) + "is not a subtag.")
        self.subtag.insert(index, obj)

    def extend(self, seq):
        for obj in seq:
            if not isinstance(obj, Tag):
                raise ValueError(str(obj) + "is not a subtag.")
        self.subtag.extend(seq)

    def print(self):
        print(str(self))

    def set_text(self, src: str):
        self.text = src
        return self


class custom_single_tag(SingleTag):
    def __init__(self, tag_name, **attributes):
        super().__init__(**attributes)
        self.name = tag_name


class br(SingleTag):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = "br"


class img(SingleTag):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = "img"


class input_tag(SingleTag):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = "input"


class custom(Tag):
    def __init__(self, tag_name, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = tag_name


class a(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "a"


class body(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "body"


class div(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "div"


class font(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "font"


class form(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "form"


class h1(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "h1"


class h2(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "h2"


class h3(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "h3"


class h4(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "h4"


class h5(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "h5"


class h6(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "h6"


class head(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "head"


class html(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "html"


class p(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "p"


class table(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "table"


class th(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "th"


class title(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "title"


class tr(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "tr"


class td(Tag):
    def __init__(self, *subtag, **attributes):
        super().__init__(*subtag, **attributes)
        self.name = "td"
