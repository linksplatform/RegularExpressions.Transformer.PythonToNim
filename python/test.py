# -*- coding: utf-8 -*-
# authors: Ethosa

from py2nim import PythonToNim

if __name__ == "__main__":
    test = PythonToNim(useRegex=True)

    code = """
# author: Ethosa

# -----=== Varibales ===-----
# Integer
int_variable = 10
# Float
float_variable = 10.0
# Boolean
bool_variable = True
# Strings
string_variable = "Hello"
string_variable3 = '''Hello'''
string_variable2 = \"\"\"Hello\"\"\"

string_variable1 = 'Hello'
s = "Hello world"
s = "1"
s = ""

    """

    print(test.Transform(code))
