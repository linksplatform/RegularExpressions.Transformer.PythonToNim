# -*- coding: utf-8 -*-
# authors: Ethosa
from retranslator import Translator


class PythonToNim(Translator):
    def __init__(self, code="", rules=[],
                 useRegex=False, debug=False):
        rules.extend(PythonToNim.RULES)
        Translator.__init__(self, code, rules, useRegex, debug)

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

        ((r""),
         (r""),
         None, 0),
    ]
