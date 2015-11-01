
class Node(object):

    def __str__(self):
        return self.printTree()


class BinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Program(Node):

    def __init__(self, declarations, fundefs_opt, instructions_opt):
        self.declarations = declarations
        self.fundefs_opt = fundefs_opt
        self.instructions_opt = instructions_opt

class Const(Node):
    
    def __init__(self, value):
        self.value = value

class Integer(Const):
    pass
    #...


class Float(Const):
    pass
    #...


class String(Const):
    pass
    #...


class Variable(Node):
    pass
    #...




# ...

class Labeled_instr(Node):

    def __init__(self, name, instruction):
        self.name = name
        self.instruction = instruction


class Assignment(Node):

    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression


class Return(Node):

    def __init__(self, expression):
        self.expression = expression


class KeyWord(Node):

    def __init__(self, name):
        self.name = name


class Condition(Node):

    def __init__(self, expression):
        self.expression = expression


class Function(Node):

    def __init__(self, rettype, funname, arg_list, instructions):
        self.rettype = rettype
        self.funname = funname
        self.arg_list = arg_list
        self.instructions = instructions


class Init(Node):

    def __init__(self, name, value):
        self.name = name
        self.value = value

class DeclarationList(Node):

    def __init__(self, dec_list):
        self.dec_list = dec_list

class Declaration(Node):

    def __init__(self, type, inits):
        self.type = type
        self.inits = inits

class InitList(Node):

    def __init__(self, init_list):
        self.init_list = init_list

class InstructionList(Node):

    def __init__(self, instr_list):
        self.instr_list = instr_list

class Arg(Node):

    def __init__(self, argtype, argname):
        self.type = argtype
        self.name = argname

class ArgsList(Node):

    def __init__(self, args_list):
        self.args_list = args_list

class FunctionList(Node):

    def __init__(self, fun_list):
        self.fun_list = fun_list

class ExprList(Node):

    def __init__(self, expr_list):
        self.expr_list = expr_list

class PrintInstr(Node):

    def __init__(self, expr_list):
        self.expr_list = expr_list

class ChoiceInstr(Node):

    def __init__(self, condition, instruction, else_instruction):
        self.condition = condition
        self.instruction = instruction
        self.else_instruction = else_instruction

class WhileInstr(Node):

    def __init__(self, instr_type, condition, instruction):
        self.instr_type = instr_type
        self.condition = condition
        self.instruction = instruction 

class ExpressionIdWithList(Node):

    def __init__(self, name, expr_list):
        self.name = name
        self.expr_list = expr_list
