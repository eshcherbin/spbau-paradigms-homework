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

    def accept(self, visitor):
        return visitor.visit(self)


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        result = None
        for expr in self.body:
            result = expr.evaluate(scope)
        return result

    def accept(self, visitor):
        return visitor.visit(self)


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def accept(self, visitor):
        return visitor.visit(self)


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

    def accept(self, visitor):
        return visitor.visit(self)


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        print(self.expr.evaluate(scope).value)

    def accept(self, visitor):
        return visitor.visit(self)


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))

    def accept(self, visitor):
        return visitor.visit(self)


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

    def accept(self, visitor):
        return visitor.visit(self)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visit(self)


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

    def accept(self, visitor):
        return visitor.visit(self)


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

    def accept(self, visitor):
        return visitor.visit(self)

if __name__ == '__main__':
    # GCD algo
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
    main = Function([],
                    [FunctionDefinition('gcd', gcd),
                     Read('a'),
                     Read('b'),
                     Print(FunctionCall(Reference('gcd'),
                                        [Reference('a'),
                                         Reference('b')]))])

    not_optimized = Function(['a'],
                             [Conditional(
                                 BinaryOperation(Number(0),
                                                 '*',
                                                 Reference('a')),
                                 [BinaryOperation(Reference('a'),
                                                  '-',
                                                  Reference('a'))],
                                 [Print(BinaryOperation(Number(117),
                                                        '+',
                                                        Number(225)))])])

    from printer import PrettyPrinter
    from folder import ConstantFolder

    def test_printer():
        print('Testing PrettyPrinter:')
        pretty_printer = PrettyPrinter()
        print('======== Test 1 ======')
        FunctionDefinition('main', main).accept(pretty_printer)
        print('======================\n')

    def test_folder():
        print('Testing ConstantFolder:')
        pretty_printer = PrettyPrinter()
        constant_folder = ConstantFolder()
        fd = FunctionDefinition('not_optimized', not_optimized)
        print('======== Test 1 ======')
        FunctionDefinition('main', main).accept(constant_folder)\
                                        .accept(pretty_printer)
        print('======== Test 2 ======')
        fd.accept(pretty_printer)
        print('----------------------')
        fd.accept(constant_folder).accept(pretty_printer)
        print('----------------------')
        fd.accept(pretty_printer)
        print('======================\n')

    test_printer()
    test_folder()
