def add1():
    x = 1
    return lambda y: x+y

a = add1()
b = add1()

print a(9)
print b(99)

def makebold(fn):
    def wrapped():
        return "<b>" + fn() + "</b>"

    return wrapped

def hello():
    return "hello"

hello = makebold(hello)

print(hello())

