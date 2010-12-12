###############################################################################
#
# Copyright (c) 2010 Ruslan Spivak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'

import readline

from serval.lexer import Lexer
from serval.parser import Parser
from serval.model import Symbol, Boolean, EmptyList
from serval.scope import (
    setup_environment, define_variable,
    lookup_variable_value, extend_environment
    )
from serval.expression import (
    selfeval, quote, definition, variable,
    assignment, conditional, lambdaexpr,
    procedure, sequence, binding
    )
from serval.expression.util import cons, is_load, load


class Interpreter(object):
    """Serval interpreter.

    Closely follows Eval/Apply from SICP Ch. 4
    """

    def __init__(self):
        self.env = setup_environment()

    def interpret(self, expr):
        return self._eval(expr, self.env)

    def _eval(self, expr, env):
        if selfeval.is_self_evaluating(expr):
            return expr

        if quote.is_quoted(expr):
            return quote.text_of_quotation(expr)

        if definition.is_definition(expr):
            return self._eval_definition(expr, env)

        if sequence.is_begin(expr):
            return self._eval_sequence(sequence.begin_actions(expr), env)

        if binding.is_let_binding(expr):
            return self._eval_binding(expr, env)

        if variable.is_variable(expr):
            return lookup_variable_value(expr, env)

        if assignment.is_assignment(expr):
            return self._eval_assignment(expr, env)

        if conditional.is_if(expr):
            return self._eval_if(expr, env)

        if conditional.is_cond(expr):
            return self._eval(conditional.cond_to_if(expr), env)

        if conditional.is_and(expr):
            return self._eval_and(expr, env)

        if conditional.is_or(expr):
            return self._eval_or(expr, env)

        if lambdaexpr.is_lambda(expr):
            return procedure.make_procedure(
                lambdaexpr.lambda_parameters(expr),
                lambdaexpr.lambda_body(expr),
                env
                )

        if procedure.is_application(expr):
            return self._apply(
                self._eval(procedure.operator(expr), env),
                self._list_of_values(procedure.operands(expr), env)
                )

    def _eval_definition(self, expr, env):
        define_variable(
            definition.definition_variable(expr),
            self._eval(definition.definition_value(expr), env),
            env
            )
        return Symbol('ok')

    def _eval_assignment(self, expr, env):
        env.set_variable_value(
            assignment.assignment_variable(expr),
            self._eval(assignment.assignment_value(expr), env)
            )
        return Symbol('ok')

    def _eval_binding(self, expr, env):
        # return an application
        return self._eval(
            cons(lambdaexpr.make_lambda(binding.binding_variables(expr),
                                        binding.binding_body(expr)),
                 binding.binding_values(expr)),
            env)

    def _eval_if(self, expr, env):
        if self._eval(conditional.if_predicate(expr), env):
            return self._eval(conditional.if_consequent(expr), env)

        return self._eval(conditional.if_alternative(expr), env)

    def _eval_and(self, expr, env):
        if procedure.no_operands(procedure.operands(expr)):
            return Boolean(True)

        def inner(expr, env):
            if sequence.is_last_expr(expr):
                return self._eval(sequence.first_expr(expr), env)

            if not self._eval(sequence.first_expr(expr), env):
                return Boolean(False)

            return inner(sequence.rest_exprs(expr), env)

        return inner(sequence.rest_exprs(expr), env)

    def _eval_or(self, expr, env):
        if procedure.no_operands(procedure.operands(expr)):
            return Boolean(False)

        def inner(expr, env):
            if sequence.is_last_expr(expr):
                return self._eval(sequence.first_expr(expr), env)

            first_value = self._eval(sequence.first_expr(expr), env)
            if first_value:
                return first_value

            return inner(sequence.rest_exprs(expr), env)

        return inner(sequence.rest_exprs(expr), env)

    def _eval_sequence(self, expressions, env):
        if sequence.is_last_expr(expressions):
            return self._eval(sequence.first_expr(expressions), env)
        else:
            self._eval(sequence.first_expr(expressions), env)
            return self._eval_sequence(sequence.rest_exprs(expressions), env)

    def _list_of_values(self, expressions, env):
        if procedure.no_operands(expressions):
            return EmptyList
        else:
            return cons(
                self._eval(procedure.first_operand(expressions), env),
                self._list_of_values(procedure.rest_operands(expressions), env)
                )

    def _apply(self, proc, args):
        if procedure.is_primitive_procedure(proc):
            return procedure.apply_primitive_procedure(proc, args)
        elif procedure.is_compound_procedure(proc):
            return self._eval_sequence(
                procedure.procedure_body(proc),
                extend_environment(
                    procedure.procedure_parameters(proc),
                    args,
                    procedure.procedure_environment(proc)
                    )
                )


def main():
    interpreter = Interpreter()

    while True:
        try:
            buffer = raw_input('serval> ')
        except EOFError:
            print
            break
        lexer = Lexer(buffer)

        try:
            expressions = Parser(lexer).parse()
            if not expressions:
                continue
            expression = expressions[0]

            if is_load(expression):
                load(interpreter, expression)
                continue

            result_expr = interpreter.interpret(expression)
            if procedure.is_compound_procedure(result_expr):
                print procedure.get_procedure_repr(result_expr)
            else:
                print result_expr
        except Exception as e:
            print str(e)
            continue

