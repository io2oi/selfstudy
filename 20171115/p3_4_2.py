strings=['foo','foobar','baz','qux','python','Guido Van rossum','scari'] * 100000

def method1(strings):
    [x for x in strings if x.startswith('foo')]
def method2(strings):
    [x for x in strings if x[:3]=='foo']
