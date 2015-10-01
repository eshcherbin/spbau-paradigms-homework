class Scope(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.data = dict()

    def __getitem__(self, key):
        current_scope = self
        while current_scope:
            if key in current_scope.data:
                return current_scope.data[key]
            current_scope = current_scope.parent
        raise KeyError

    def __setitem__(self, key, value):
        self.data[key] = value


class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        result = None
        for expr in self.body:
            result = expr.evaluate(scope)
        return result


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        branch = self.if_false if self.condition.evaluate(scope).value == 0 \
            else self.if_true
        if not branch:
            return None
        result = None
        for expr in branch:
            result = expr.evaluate(scope)
        return result


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        print(self.expr.evaluate(scope).value)


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for arg_name, arg_value in zip(function.args,
                                       map(lambda expr: expr.evaluate(scope),
                                           self.args)):
            call_scope[arg_name] = arg_value
        return function.evaluate(call_scope)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        a = self.lhs.evaluate(scope).value
        b = self.rhs.evaluate(scope).value
        op = self.op
        if op == '+':
            return Number(a + b)
        elif op == '-':
            return Number(a - b)
        elif op == '*':
            return Number(a * b)
        elif op == '/':
            return Number(a // b)
        elif op == '%':
            return Number(a % b)
        elif op == '==':
            return Number(1 if a == b else 0)
        elif op == '!=':
            return Number(0 if a == b else 1)
        elif op == '<':
            return Number(1 if a < b else 0)
        elif op == '>':
            return Number(1 if a > b else 0)
        elif op == '<=':
            return Number(1 if a <= b else 0)
        elif op == '>=':
            return Number(1 if a >= b else 0)
        elif op == '&&':
            return Number(a and b)
        elif op == '||':
            return Number(a or b)


class UnaryOperation:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        a = self.expr.evaluate(scope).value
        op = self.op
        if op == '!':
            return Number(1 if not a else 0)
        elif op == '-':
            return Number(-a)


if __name__ == '__main__':
    parent = Scope()
    parent['foo'] = Function(['a', 'b'], [Number(117)])
    parent['bar'] = Number(10)
    scope = Scope(parent)
    scope['a'] = Number(0)
    assert isinstance(scope['a'], Number) and scope['a'].value == 0
    assert isinstance(scope['bar'], Number) and scope['bar'].value == 10
    assert isinstance(scope['foo'], Function) and scope['foo'].args == ['a', 'b'] and\
        isinstance(scope['foo'].body, list) and len(scope['foo'].body) == 1 and\
        isinstance(scope['foo'].body[0], Number) and\
        scope['foo'].body[0].value == 117
    try:
        scope['zoo']
    except KeyError:
        pass
    else:
        assert False

    # GCD algo
    # tested on
    # http://informatics.msk.ru/mod/statements/view3.php?id=268&chapterid=199#1
    # passed all tests there (input was a little bit different)
    scope = Scope()
    Read('a').evaluate(scope)
    Read('b').evaluate(scope)
    gcd = Function(['a', 'b'],
                   [Conditional(
                    UnaryOperation('!',
                                   BinaryOperation(Reference('a'),
                                                   '&&',
                                                   Reference('b'))),
                    [Conditional(Reference('a'),
                                 [Reference('a')],
                                 [Reference('b')])],
                    [Conditional(BinaryOperation(Reference('a'),
                                                 '>=',
                                                 Reference('b')),
                                 [FunctionCall(Reference('gcd'),
                                               [BinaryOperation(
                                                Reference('a'),
                                                '%',
                                                Reference('b')),
                                                Reference('b')])],
                                 [FunctionCall(Reference('gcd'),
                                               [Reference('a'),
                                                BinaryOperation(
                                                Reference('b'),
                                                '%',
                                                Reference('a'))])])])])
    Print(FunctionCall(FunctionDefinition('gcd', gcd),
                       [Reference('a'), Reference('b')])).evaluate(scope)
