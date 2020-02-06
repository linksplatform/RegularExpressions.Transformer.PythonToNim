# -*- coding: utf-8 -*-
# authors: Ethosa
from retranslator import Translator


class PythonToNim(Translator):
    def __init__(self, code="", rules=[],
                 useRegex=False, debug=False):
        rules.extend(PythonToNim.RULES)
        Translator.__init__(self, code, rules, useRegex, debug)

    MAX_COUNT = 1_000

    RULES = [
        # '' => ""
        ((r"'"),
         (r'"'),
         None, 0),

        # s = ...
        # var s = ...
        ((r"(?P<enter>[\r\n]+[ ]*)(?P<var>[a-zA-Z_][a-zA-Z0-9_]*)"
          r"[ ]*=[ ]*(?P<val>[^\r\n]+)"
          r"(?P<other>[\s\S]*(?P=var)\b[ ]*)*"),
         (r"\g<enter>var \g<var> = \g<val>"
          r"\g<other>"),
         None, 110),

        # str -> string
        ((r"(?P<enter>[\r\n]+[ ]*[^\"\r\n]*)\bstr\b"),
         (r"\g<enter>string"),
         None, 0),

        # var s = ...
        # ...
        # var s = ...
        # -----------
        # var s = ...
        # ...
        # s = ...
        ((r"(?P<enter>[\r\n]+[ ]*)var (?P<var>[a-zA-Z_][a-zA-Z0-9_]*)[ ]*=[ ]*"
          r"(?P<other>[\s\S]*)var (?P=var)\b"),
         (r"\g<enter>var \g<var> = \g<other>\g<var>"),
         None, 110),

        # range(10)
        # 0..<10
        ((r"\brange[ ]*\((?P<val>[\S]+?)[ ]*\)"),
         (r"0..<\g<val>"),
         None, 0),

        # range(1, 10)
        # countup(1, 10 - 1, 1)
        ((r"\brange[ ]*\((?P<one>[\S]+?)[ ]*,"
          r"[ ]*(?P<two>[\S]+?)[ ]*\)"),
         (r"countup(\g<one>, \g<two> - 1, 1)"),
         None, 0),

        # range(1, 10, 1)
        # countdown(1, 10 - 1, 1)
        ((r"\brange[ ]*\((?P<one>[\S]+?)[ ]*,"
          r"[ ]*(?P<two>[\S]+?)[ ]*,"
          r"[ ]*-(?P<three>[\S]+?)[ ]*\)"),
         (r"countdown(\g<one>, \g<two>-1, \g<three>)"),
         None, 0),

        # range(1, 10, 1)
        # countup(1, 10 - 1, 1)
        ((r"\brange[ ]*\((?P<one>[\S]+?)[ ]*,"
          r"[ ]*(?P<two>[\S]+?)[ ]*,"
          r"[ ]*(?P<three>[\S]+?)[ ]*\)"),
         (r"countup(\g<one>, \g<two>-1, \g<three>)"),
         None, 0),

        # item not in array -> not (item in array)
        ((r"[ ]+(?P<item>[\w]+)[ ]+not[ ]+in"
          r"[ ]+(?P<array>\[?[\w]+([ ]*,[ ]*[\w]+)*\]?)"),
         (r" not (\g<item> in \g<array>)"),
         None, 0),

        # dictionary = {...}
        # dictionary = %*{...}
        ((r"(?P<enter>[\r\n]+[ ]*)(?P<assign>var )?"
          r"(?P<var>[a-zA-Z_][a-zA-Z0-9_]*)[ ]*=[ ]*"
          r"(?P<val>\{[\s\S]*?\})"),
         (r"\g<enter>\g<assign>\g<var> = %*\g<val>"),
         None, 0),

        # import json
        ((r"\A(?P<enter>[\S\s]+?)(?P<assign>var )?"
          r"(?P<var>[a-zA-Z_][a-zA-Z0-9_]*)[ ]*=[ ]*%\*"),
         (r"import json\n\g<enter>\g<assign>\g<var> = %*"),
         None, 0),

        # pass -> discard
        ((r"(?P<enter>[\r\n]+[ ]*[^\"\r\n]*)pass"),
         (r"\g<enter>discard"),
         None, 0),

        # [...] -> @[...]
        ((r"(?P<enter>[\r\n]+[ ]*[^\"\r\n]*)"
          r"(?P<array>\[[\w]+([ ]*,[ ]*[\w]+)*\])"),
         (r"\g<enter>@\g<array>"),
         None, 0),

        # print -> echo
        ((r"(?P<enter>[\r\n]+[ ]*[^\"\r\n]*)\bprint\b"),
         (r"\g<enter>echo"),
         None, 0),

        # with open(...) as f: ...
        # with_as = open(...)
        # f = with_as_f.enter()
        # try:
        #     ...
        # finally:
        # with_as_f.exit()
        ((r"(?P<enter>[\r\n]+)(?P<bindent>[ ]*)(?P<enter1>[^\"\r\n]*)"
          r"with[ ]+(?P<call>[\S ]+?)[ ]+as[ ]+(?P<var>\w+):(?P<body>[\r\n]+"
          r"(?P<indent>(?P=bindent)[ ]+)[^\r\n]+([\r\n]+(?P=indent)[^\r\n]+)*)"),
         (r"\g<enter>\g<bindent>\g<enter1>var\n\g<indent>with_as_\g<var> = \g<call>\n"
          r"\g<indent>\g<var> = with_as_\g<var>.enter()"
          r"\n\g<bindent>try:\g<body>\n\g<bindent>finally:\n\g<indent>"
          r"with_as_\g<var>.exit()"),
         None, MAX_COUNT),

        # class A:
        # type A = object
        ((r"(?P<enter>[\r\n]+[ ]*[^\"\r\n]*)"
          r"class[ ]+(?P<name>[\w]+):"),
         (r"\g<enter>type \g<name> = object  "
          r"# please, create new\g<name> function!"),
         None, 0),

        # class A(SuperClass):
        # type A = SuperClass
        ((r"(?P<enter>[\r\n]+[ ]*[^\"\r\n]*)"
          r"class[ ]+(?P<name>[\w]+)[ ]*\([ ]*"
          r"(?P<super>[\w]+)[ ]*\)[ ]*:"),
         (r"\g<enter>type \g<name> = \g<super>  "
          r"# please, create new\g<name> function!"),
         None, 0),

        # __init__ -> init
        ((r"\b_+(\S+(?<!_))_+\b"),
         (r"\1"),
         None, 0),

        # type A = object
        # a = A() -> a = newA()
        ((r"(?P<enter>[\r\n]+[ ]*[^\"\r\n]*)"
          r"type[ ]+(?P<name>[\w]+)[ ]*=[ ]*object"
          r"(?P<other>[\S\s]+?)\b(?P=name)[ ]*\((?P<args>[^\)]*)\)"),
         (r"\g<enter>type \g<name> = object\g<other>"
          r"new\g<name>(\g<args>)"),
         None, 0),

        # def smth(self, a, b, x):
        # proc smth(self: CLASSNAME, a, b, x: any): any =
        ((r"(?P<enter>[\r\n]+)(?P<bindent>[ ]*)(?P<enter1>[^\"\r\n]*)"
          r"type[ ]+(?P<name>[\w]+)[ ]*=[ ]*object"
          r"(?P<other>[\S\s]+?)(?P<indent>(?P=bindent)[ ]+)def[ ]+"
          r"(?P<method>[\w]+)[ ]*\([ ]*self[ ]*,[ ]*"
          r"(?P<args>[^\)]+)\)[ ]*:"),
         (r"\g<enter>\g<bindent>\g<enter1>type \g<name> = object"
          r"\g<other>\g<bindent>proc \g<method>(self: \g<name>, "
          r"\g<args>: any): any ="),
         None, MAX_COUNT),

        # def smth(self):
        # proc smth(self: CLASSNAME): any =
        ((r"(?P<enter>[\r\n]+)(?P<bindent>[ ]*)(?P<enter1>[^\"\r\n]*)"
          r"type[ ]+(?P<name>[\w]+)[ ]*=[ ]*object"
          r"(?P<other>[\S\s]+?)(?P<indent>(?P=bindent)[ ]+)def[ ]+"
          r"(?P<method>[\w]+)[ ]*\([ ]*self[ ]*\)[ ]*:"),
         (r"\g<enter>\g<bindent>\g<enter1>type \g<name> = object"
          r"\g<other>\g<bindent>proc \g<method>(self: \g<name>"
          r"): any ="),
         None, MAX_COUNT),

        # def smth(a, b, x):
        # proc smth(a, b, x: any): any =
        ((r"(?P<enter>[\r\n]+[ ]*[^\"\r\n]*)"
          r"def[ ]+(?P<name>[\w]+)[ ]*\("
          r"(?P<args>[^\)]+)\)[ ]*:"),
         (r"\g<enter>proc \g<name>(\g<args>: any): any ="),
         None, 0),

        # def smth():
        # proc smth(): any =
        ((r"(?P<enter>[\r\n]+[ ]*[^\"\r\n]*)"
          r"def[ ]+(?P<name>[\w]+)[ ]*\([ ]*\)[ ]*:"),
         (r"\g<enter>proc \g<name>(): any ="),
         None, 0),

        # from random import randint -> from random import rand, randomize; randomize()
        ((r"from[ ]+random[ ]+import[ ]+randint"),
         (r"from random import rand, randomize\nrandomize()"),
         None, 0),

        # import random -> import random; randomize()
        ((r"import[ ]+random"),
         (r"import random\nrandomize()"),
         None, 0),

        # random.randint(0, 100) -> rand
        ((r"(random[ ]*.[ ]*)?randint[ ]*\((?P<min>[^,]+),[ ]*(?P<max>[^\)]+)\)"),
         (r"rand(\g<max> - \g<min>) + \g<min>"),
         None, 0),

        ((r""),
         (r""),
         None, 0),
    ]
