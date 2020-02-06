# -*- coding: utf-8 -*-
# authors: Ethosa

from py2nim import PythonToNim


test = PythonToNim(useRegex=True)

code = """
class MyClass(object):
    test_var: int
    def __init__(self):
        self.test_var = 0

m = MyClass()
"""
print(test.Transform(code))


# class A:
#     a: int
#     b: str
#     def __init__(self):
#         self.a = 5

# a = A()
# print(a)
