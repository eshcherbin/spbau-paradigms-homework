from model import (Number, Reference, Function,
                   FunctionDefinition, FunctionCall, BinaryOperation,
                   UnaryOperation, Conditional, Read, Print, Scope)


class EmptyScopeSingleton(Scope):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


class ConstantFolder:
    def __init__(self):
        self.is_root = True
        self.expr_stack = []

    def visit(self, tree):
        name = tree.__class__.__name__
        try:
            fn = getattr(self, 'visit' + name)
        except AttributeError:
            print('Method for {} not found!'.format(name))
            raise NotImplementedError
        if self.is_root:
            self.is_root = False
            fn(tree)
            self.is_root = True
            return self.expr_stack.pop()
        else:
            fn(tree)

    def visitNumber(self, number):
        self.expr_stack.append(Number(number.value))

    def visitFunction(self, function):
        current_func = Function(function.args, [])
        for expr in function.body:
            expr.accept(self)
            current_func.body.append(self.expr_stack.pop())
        self.expr_stack.append(current_func)

    def visitFunctionDefinition(self, fd):
        current_fd = FunctionDefinition(fd.name, None)
        fd.function.accept(self)
        current_fd.function = self.expr_stack.pop()
        self.expr_stack.append(current_fd)

    def visitConditional(self, conditional):
        current_cond = Conditional(None, [], None)
        conditional.condition.accept(self)
        current_cond.condition = self.expr_stack.pop()
        for expr in conditional.if_true:
            expr.accept(self)
            current_cond.if_true.append(self.expr_stack.pop())
        if conditional.if_false:
            current_cond.if_false = []
            for expr in conditional.if_false:
                expr.accept(self)
                current_cond.if_false.append(self.expr_stack.pop())
        self.expr_stack.append(current_cond)

    def visitPrint(self, print_expr):
        print_expr.expr.accept(self)
        self.expr_stack.append(Print(self.expr_stack.pop()))

    def visitRead(self, read_expr):
        self.expr_stack.append(Read(read_expr.name))

    def visitFunctionCall(self, fc):
        fc.fun_expr.accept(self)
        current_fc = FunctionCall(self.expr_stack.pop(), [])
        for expr in fc.args:
            expr.accept(self)
            current_fc.args.append(self.expr_stack.pop())
        self.expr_stack.append(current_fc)

    def visitReference(self, reference):
        self.expr_stack.append(Reference(reference.name))

    def visitBinaryOperation(self, bin_op):
        result = BinaryOperation(None, bin_op.op, None)
        bin_op.lhs.accept(self)
        result.lhs = self.expr_stack.pop()
        bin_op.rhs.accept(self)
        result.rhs = self.expr_stack.pop()
        if (isinstance(result.lhs, Number) and
                isinstance(result.rhs, Number)):
            empty_scope = EmptyScopeSingleton()
            result = result.evaluate(empty_scope)
        elif result.op == '*' and ((isinstance(result.lhs, Number) and
                                    result.lhs.value == 0) or
                                   (isinstance(result.rhs, Number) and
                                       result.rhs.value == 0)):
            result = Number(0)
        elif (result.op == '-' and
                isinstance(result.lhs, Reference) and
                isinstance(result.rhs, Reference) and
                result.lhs.name == result.lhs.name):
            result = Number(0)
        self.expr_stack.append(result)

    def visitUnaryOperation(self, un_op):
        un_op.expr.accept(self)
        result = UnaryOperation(un_op.op, self.expr_stack.pop())
        if isinstance(result.expr, Number):
            empty_scope = EmptyScopeSingleton()
            result = result.evaluate(empty_scope)
        self.expr_stack.append(result)
