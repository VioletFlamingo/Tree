
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " +
                        self.__class__.__name__)

    @addToClass(AST.BinExpr)
    def printTree(self, l):
        print(l * "| " + self.op)
        self.left.printTree(l + 1)
        self.right.printTree(l + 1)

    @addToClass(AST.Program)
    def printTree(self, l):
        self.declarations.printTree(l)
        self.fundefs_opt.printTree(l)
        self.instructions_opt.printTree(l)

    @addToClass(AST.Const)
    def printTree(self, l):
        print(l * "| " + self.value)

    @addToClass(AST.Labeled_instr)
    def printTree(self, l):
        print(l * "| " + "LABELED_INSTR")
        print((l + 1) * "| " + self.name)
        self.instruction.printTree(l + 1)

    @addToClass(AST.Assignment)
    def printTree(self, l):
        print(l * "| " + "=")
        print((l + 1) * "| " + self.variable)
        if (isinstance(self.expression, str)):
            print((l+1)* "| " + self.expression)
        else:
            self.expression.printTree(l + 1)

    @addToClass(AST.Return)
    def printTree(self, l):
        print(l * "| " + "RETURN")
        if (isinstance(self.expression, str)):
            print((l+1)* "| " + self.expression)
        else:
            self.expression.printTree(l + 1)

    @addToClass(AST.KeyWord)
    def printTree(self, l):
        print(l * "| " + self.name)

    @addToClass(AST.Condition)
    def printTree(self, l):
        self.expression.printTree(l)

    @addToClass(AST.Function)
    def printTree(self, l):
        print(l * "| " + "FUNDEF")
        print((l + 1) * "| " + self.funname)
        print((l + 1) * "| " + "RET " + self.rettype)
        self.arg_list.printTree(l+1)
        self.instructions.printTree(l + 1)

    @addToClass(AST.Init)
    def printTree(self, l):
        print(l * "| " + "=")
        print((l + 1) * "| " + self.name)
        self.value.printTree(l+1)

    @addToClass(AST.DeclarationList)
    def printTree(self, l):
        if (len(self.dec_list) > 0):
            print(l * "| " +"DECL")
            for dec in self.dec_list:
                dec.printTree(l+1)

    @addToClass(AST.Declaration)
    def printTree(self, l):
        self.inits.printTree(l)

    @addToClass(AST.InitList)
    def printTree(self, l):
        for init in self.init_list:
            init.printTree(l)

    @addToClass(AST.InstructionList)
    def printTree(self, l):
        for instr in self.instr_list:
            instr.printTree(l)

    # to check
    @addToClass(AST.Arg)
    def printTree(self, l):
        print(l*"| " + "ARG " + self.argname)

    @addToClass(AST.ArgsList)
    def printTree(self, l):
        for arg in self.args_list:
            arg.printTree(l)

    @addToClass(AST.FunctionList)
    def printTree(self, l):
        for fun in self.fun_list:
            fun.printTree(l)

    @addToClass(AST.ExprList)
    def printTree(self, l):
        for expr in self.expr_list:
            if (isinstance(expr, str)):
                print(l * "| " + expr)
            else:
                expr.printTree(l)

    @addToClass(AST.PrintInstr)
    def printTree(self, l):
        print(l * "| " + "PRINT")
        self.expr_list.printTree(l + 1)

    @addToClass(AST.ChoiceInstr)
    def printTree(self, l):
        print(l * "| " + "IF")
        self.condition.printTree(l + 1)
        self.instruction.printTree(l + 1)
        if(self.else_instruction):
            print(l * "| " + "ELSE")
            self.else_instruction.printTree(l + 1)

    @addToClass(AST.WhileInstr)
    def printTree(self, l):
        print(l * "| " + self.instr_type)
        self.condition.printTree(l+1)
        self.instruction.printTree(l+1)

    @addToClass(AST.ExpressionIdWithList)
    def printTree(self, l):
        print(l * "| " + "FUNCALL")
        print((l+1) * "| " + self.name)
        self.expr_list.printTree(l+1)

    @addToClass(AST.Compound_instr)
    def printTree(self, l):
        self.declarations.printTree(l)
        self.instructions.printTree(l)

    @addToClass(AST.Id)
    def printTree(self, l):
        print(l*("| ") + self.name)