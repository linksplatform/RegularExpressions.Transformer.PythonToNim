type MyClass = object  # please, create newMyClass function!
    test_var: int

proc newMyClass(test_var: int): MyClass =
    return MyClass(test_var: test_var)

proc init(self: MyClass): any =
        self.test_var = 0

var m = newMyClass(5)
