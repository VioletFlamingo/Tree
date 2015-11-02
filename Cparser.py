#!/usr/bin/python

from scanner import Scanner
from AST import *
import TreePrinter


def printError(line_no):
    print("Error in line {0}".format(line_no))


class Cparser(object):

    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(
                p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : declarations fundefs_opt instructions_opt"""
        p[0] = Program(p[1], p[2], p[3])


# declarations

    def p_declarations(self, p):
        """declarations : declarations declaration"""
        p[0] = DeclarationList(p[1].dec_list + [p[2]])

    def p_no_declarations(self, p):
        """declarations : """
        p[0] = DeclarationList([])

# END declarations


# declaration

    def p_declaration(self, p):
        """declaration : TYPE inits ';'"""
        p[0] = Declaration(p[1], p[2])

    def p_error_declaration(self, p):
        """declaration : error ';'"""
        # DRUKUJ BLAD

# END declaration

# inits

    def p_inits(self, p):
        """inits : inits ',' init"""

        p[0] = InitList(p[1].init_list + [p[3]])

    def p_single_init(self, p):
        """inits : init """
        p[0] = InitList([p[1]])

# END inits


    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = Init(p[1], p[3])


# instructions_opt

    def p_instructions_opt(self, p):
        """instructions_opt : instructions"""
        p[0] = p[1]

    def p_empty_instructions_opt(self, p):
        """instructions_opt : """
        p[0] = InstructionList([])

# END instructions_opt

# instructions

    def p_instructions(self, p):
        """instructions : instructions instruction"""
        p[0] = InstructionList(p[1].instr_list + [p[2]])

    def p_sinle_instruction(self, p):
        """instructions : instruction """
        p[0] = InstructionList([p[1]])

# END instructions

    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """
        p[0] = p[1]



# print_instr

    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'"""
        p[0] = PrintInstr(p[2])

    def p_print_instr_err(self, p):
        """print_instr : PRINT error ';' """
        # DRUKUJ BLAD

# END print_instr


    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = Labeled_instr(p[1], p[3])


    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = Assignment(p[1], p[3])


# choice_instr

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX """
        p[0] = ChoiceInstr(p[3], p[5])

    def p_choice_instr_with_else(self, p):
        """choice_instr : IF '(' condition ')' instruction ELSE instruction """
        p[0] = ChoiceInstr(p[3], p[5], p[7])

    def p_error_choice_instr(self, p):
        """choice_instr : IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        # DRUKUJ BLAD

# END choice)instr


# while_instr

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction """
        p[0] = WhileInstr("While", p[3], p[5])

    def p_error_while_instr(self, p):
        """while_instr : WHILE '(' error ')' instruction """
        # DRUKUJ BLAD

# END while_instr


    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = WhileInstr("Repeat", p[4], p[2])

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = Return(p[2])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = KeyWord("continue")

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = KeyWord("break")


    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions_opt '}' """
        p[0] = Compound_instr(p[2], p[3])


    def p_condition(self, p):
        """condition : expression"""
        p[0] = Condition(p[1])


    def p_const_I(self, p):
        """const : INTEGER"""
        p[0] = Integer(p[1])

    def p_const_F(self, p):
        """const : FLOAT"""
        p[0] = Float(p[1])

    def p_const_S(self, p):
        """const : STRING"""
        p[0] = String(p[1])
# expression

    def p_expression(self, p):
        """expression : ID '(' expr_list_or_empty ')' """
        p[0] = ExpressionIdWithList(p[1], p[3])

    def p_expression_const(self, p):
        """expression : const """
        p[0] = p[1]

    def p_expression_id(self, p):
        """expression : ID """
        p[0] = Id(p[1])

    def p_expression_with_par(self, p):
        """expression : '(' expression ')' """
        p[0] = p[2]

    def p_expression_two_exprs(self, p):
        """expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression """
        p[0] = BinExpr(p[2], p[1], p[3])

    def p_expression_err(self, p):
        """expression : ID '(' error ')'
                      | '(' error ')'"""
        # DRUKUJ BLAD

# END expression


# expr_list_or_empty

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list"""
        p[0] = p[1]

    def p_empty_expr_list(self, p):
        """expr_list_or_empty : """
        p[0] = ExprList([])

# END expr_list_or_empty


# expr_list

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression"""
        p[0] = ExprList(p[1].expr_list + [p[3]])

    def p_single_expr(self, p):
        """expr_list : expression """
        p[0] = ExprList([p[1]])

# END expr_list


# fundefs_opt

    def p_fundefs_opt(self, p):
        """fundefs_opt : fundefs"""
        p[0] = p[1]

    def p_empty_fundefs_opt(self, p):
        """fundefs_opt : """
        p[0] = FunctionList([])

# END fundefs_opt


# fundefs

    def p_fundefs(self, p):
        """fundefs : fundefs fundef"""
        p[0] = FunctionList(p[1].fun_list + [p[2]])

    def p_single_fundef(self, p):
        """fundefs : fundef """
        p[0] = FunctionList([p[1]])

# END fundefs

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = Function(p[1], p[2], p[4], p[6])


# args_list_or_empty

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list"""
        p[0] = p[1]

    def p_empty_args_list(self, p):
        """args_list_or_empty : """
        p[0] = ArgsList([])

# END args_list_or_empty


# args_list

    def p_args_list(self, p):
        """args_list : args_list ',' arg"""
        p[0] = ArgsList(p[1].args_list + [p[3]])

    def p_single_arg_list(self, p):
        """args_list : arg """
        p[0] = ArgsList([p[1]])

# END args_list

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = Arg(p[1], p[2])
