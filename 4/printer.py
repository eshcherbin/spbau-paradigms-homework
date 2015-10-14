class PrettyPrinter:
    def __init__(self):
        self.indent_level = 0
        self.expr_is_statement = True

    def print_indent(self, string, end='\n'):
        print(' ' * self.indent_level, string, end=end, sep='')

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

        print(') {')

        self.indent_level += 4
        for expr in conditional.if_true:
            expr.accept(self)
        self.indent_level -= 4

        self.print_indent('} else {')

        self.indent_level += 4
        for expr in conditional.if_false:
            expr.accept(self)
        self.indent_level -= 4

        self.print_indent('};')

    def visitFunctionDefinition(self, fd):
        self.print_indent('def {}({}) {{'.format(
            fd.name,
            ', '.join(fd.function.args)
            ))

        self.indent_level += 4
        for statement in fd.function.body:
            statement.accept(self)
        self.indent_level -= 4

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

    def visitNumber(self, number):
        if self.expr_is_statement:
            self.handleArithmeticStatement(number)
        else:
            print('({})'.format(number.value), end='')

    def visitReference(self, reference):
        if self.expr_is_statement:
            self.handleArithmeticStatement(reference)
        else:
            print('({})'.format(reference.name), end='')

    def visitBinaryOperation(self, bin_op):
        if self.expr_is_statement:
            self.handleArithmeticStatement(bin_op)
        else:
            print('(', end='')
            bin_op.lhs.accept(self)
            print(' {} '.format(bin_op.op), end='')
            bin_op.rhs.accept(self)
            print(')', end='')

    def visitUnaryOperation(self, un_op):
        if self.expr_is_statement:
            self.handleArithmeticStatement(un_op)
        else:
            print('(', un_op.op, sep='', end='')
            un_op.expr.accept(self)
            print(')', end='')

    def visitFunctionCall(self, fc):
        if self.expr_is_statement:
            self.handleArithmeticStatement(fc)
        else:
            fc.fun_expr.accept(self)
            print('(', end='')
            if fc.args:
                fc.args[0].accept(self)
                for arg in fc.args[1:]:
                    print(', ', end='')
                    arg.accept(self)
            print(')', end='')
