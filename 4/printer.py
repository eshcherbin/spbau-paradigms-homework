def handle_ariphm(visit_method):
    def handler(self, expr):
        if self.expr_is_statement:
            self.handleArithmeticStatement(expr)
        else:
            visit_method(self, expr)
    return handler


class PrettyPrinter:
    def __init__(self, indent_width=4):
        self.indent_level = 0
        self.expr_is_statement = True
        self.indent_width = indent_width

    def print_indent(self, string, end='\n'):
        print(' ' * self.indent_level, string, end=end, sep='')

    def scope_enter(self):
        self.indent_level += self.indent_width
        print('{')

    def scope_exit(self):
        self.indent_level -= self.indent_width
        self.print_indent('}', end='')

    def visit(self, tree):
        name = tree.__class__.__name__
        try:
            fn = getattr(self, 'visit' + name)
        except AttributeError:
            print('Method for {} not found!'.format(name))
            raise NotImplementedError
        return fn(tree)

    def visitConditional(self, conditional):
        self.print_indent('if (', end='')

        self.expr_is_statement = False
        conditional.condition.accept(self)
        self.expr_is_statement = True

        print(') ', end='')

        self.scope_enter()
        for expr in conditional.if_true:
            expr.accept(self)
        self.scope_exit()

        if conditional.if_false:
            print(' else ', end='')
            self.scope_enter()
            for expr in conditional.if_false:
                expr.accept(self)
            self.scope_exit()

        print(';')

    def visitFunctionDefinition(self, fd):
        self.print_indent('def {}({}) '.format(
            fd.name,
            ', '.join(fd.function.args)
            ), end='')

        self.scope_enter()
        for statement in fd.function.body:
            statement.accept(self)
        self.scope_exit()

        self.print_indent('};')

    def visitPrint(self, print_stat):
        self.print_indent('print ', end='')
        self.expr_is_statement = False
        print_stat.expr.accept(self)
        self.expr_is_statement = True
        print(';')

    def visitRead(self, read_stat):
        self.print_indent('read {};'.format(read_stat.name))

    def handleArithmeticStatement(self, ar_stat):
        self.print_indent('', end='')
        self.expr_is_statement = False
        ar_stat.accept(self)
        self.expr_is_statement = True
        print(';')

    @handle_ariphm
    def visitNumber(self, number):
        print('({})'.format(number.value), end='')

    @handle_ariphm
    def visitReference(self, reference):
        print(reference.name, end='')

    @handle_ariphm
    def visitBinaryOperation(self, bin_op):
        print('(', end='')
        bin_op.lhs.accept(self)
        print(' {} '.format(bin_op.op), end='')
        bin_op.rhs.accept(self)
        print(')', end='')

    @handle_ariphm
    def visitUnaryOperation(self, un_op):
        print('(', un_op.op, sep='', end='')
        un_op.expr.accept(self)
        print(')', end='')

    @handle_ariphm
    def visitFunctionCall(self, fc):
        fc.fun_expr.accept(self)
        print('(', end='')
        if fc.args:
            fc.args[0].accept(self)
            for arg in fc.args[1:]:
                print(', ', end='')
                arg.accept(self)
        print(')', end='')
