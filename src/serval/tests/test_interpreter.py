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

import os
import shutil
import unittest

THIS_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseTestCase(unittest.TestCase):

    def _interpret(self, text, interpreter=None):
        from serval.lexer import Lexer
        from serval.parser import Parser
        from serval.interpreter import Interpreter
        from serval.expression.procedure import (
            is_compound_procedure, get_procedure_repr)

        if interpreter is None:
            interpreter = Interpreter()

        expressions = Parser(Lexer(text)).parse()
        for expr in expressions:
            result_expr = interpreter.interpret(expr)
            if is_compound_procedure(result_expr):
                result = get_procedure_repr(result_expr)
            else:
                result = str(result_expr)

        return result


class InterpreterRepresentationTestCase(BaseTestCase):

    def test_constant_boolean_true_repr(self):
        result = self._interpret('#t')
        self.assertEquals(result, '#t')

    def test_constant_boolean_false_repr(self):
        result = self._interpret('#f')
        self.assertEquals(result, '#f')

    def test_constant_character_repr(self):
        result = self._interpret(r'#\a')
        self.assertEquals(result, r'#\a')

    def test_constant_character_newline_repr(self):
        result = self._interpret(r'#\newline')
        self.assertEquals(result, r'#\newline')

    def test_quoted_list_repr(self):
        result = self._interpret("'(1 2 3)")
        self.assertEquals(result, '(1 2 3)')

    def test_quoted_list_quote_repr(self):
        result = self._interpret('(quote (1 2 3))')
        self.assertEquals(result, '(1 2 3)')

    def test_quoted_list_repr_quote(self):
        result = self._interpret('(quote (1 2 3))')
        self.assertEquals(result, '(1 2 3)')

    def test_improper_list_repr(self):
        result = self._interpret("'(1 2 . 3)")
        self.assertEquals(result, '(1 2 . 3)')

    def test_proper_list_with_pair_repr(self):
        result = self._interpret("'(1 (2 . 3))")
        self.assertEquals(result, '(1 (2 . 3))')

    def test_nested_pairs_repr(self):
        result = self._interpret("'(1 . (2 . 3))")
        self.assertEquals(result, '(1 2 . 3)')

    def test_pair_with_empty_list_repr(self):
        result = self._interpret("'(1 . (2 . (3 . ())))")
        self.assertEquals(result, '(1 2 3)')

    def test_list_of_lists_repr(self):
        result = self._interpret("'((1 2) (3 4))")
        self.assertEquals(result, '((1 2) (3 4))')

    def test_empty_list_repr(self):
        result = self._interpret("'()")
        self.assertEquals(result, '()')

    def test_list_with_cdr_as_empty_list_repr(self):
        result = self._interpret("'(1 ())")
        self.assertEquals(result, '(1 ())')

    def test_pair_with_cdr_as_empty_list_repr(self):
        result = self._interpret("'(1 . ())")
        self.assertEquals(result, '(1)')

    def test_pair_with_car_as_empty_list_repr(self):
        result = self._interpret("'(() . 1)")
        self.assertEquals(result, '(() . 1)')

    def test_quoted_list_with_car_as_empty_list_repr(self):
        result = self._interpret('(quote (() 1))')
        self.assertEquals(result, '(() 1)')


class IFSpecialFormTestCase(BaseTestCase):

    def test_if_positive_number(self):
        result = self._interpret(
            """
            (define a 5)
            (if a
              '(1 2 3 4 5)
              '(0))
            """)
        self.assertEquals(result, '(1 2 3 4 5)')

    def test_if_zero_number(self):
        result = self._interpret(
            """
            (define a 0)
            (if a
              '(1 2 3 4 5)
              '(0))
            """)
        self.assertEquals(result, '(1 2 3 4 5)')

    def test_if_true_boolean(self):
        result = self._interpret(
            """
            (define a #t)
            (if a
              '(1 2 3 4 5)
              '(0))
            """)
        self.assertEquals(result, '(1 2 3 4 5)')

    def test_if_false_boolean(self):
        result = self._interpret(
            """
            (define a #f)
            (if a
              '(1 2 3 4 5)
              '(0))
            """)
        self.assertEquals(result, '(0)')


class CONDDerivedFormTestCase(BaseTestCase):

    def test_cond(self):
        result = self._interpret(
            """
            (let ((x -1))
              (cond
                ((< x 0) (list 'minus (abs x)))
                ((> x 0) (list 'plus x))
                (else (list 'zero x))))
            """)
        self.assertEquals(result, '(minus 1)')

    def test_cond_else_clause_with_multiple_expressions(self):
        result = self._interpret(
            """
            (let ((x 0))
              (cond
                ((< x 0) (list 'minus (abs x)))
                ((> x 0) (list 'plus x))
                (else (cons x x) (list 'zero x))))
            """)
        self.assertEquals(result, '(zero 0)')


class ANDSpecialFormTestCase(BaseTestCase):

    def test_and_conditional(self):
        self.assertEquals(self._interpret('(and 1 2 3)'), '3')

    def test_and_conditional_no_expressions(self):
        self.assertEquals(self._interpret('(and)'), '#t')

    def test_and_conditional_zero_number(self):
        self.assertEquals(self._interpret('(and 1 0 3)'), '3')

    def test_and_conditional_false(self):
        self.assertEquals(self._interpret('(and 1 #f 3)'), '#f')

    def test_and_conditional_true(self):
        self.assertEquals(self._interpret('(and 1 2 #t)'), '#t')

    def test_and_conditional_true_nested_expressions(self):
        self.assertEquals(self._interpret('(and (< 1 2) (> 3 1))'), '#t')

    def test_and_conditional_false_nested_expressions(self):
        self.assertEquals(self._interpret('(and (>= 1 2) (> 3 1))'), '#f')


class ORSpecialFormTestCase(BaseTestCase):

    def test_or_conditional(self):
        self.assertEquals(self._interpret('(or #f 1 2)'), '1')

    def test_or_conditional_no_expressions(self):
        self.assertEquals(self._interpret('(or)'), '#f')

    def test_or_conditional_zero_number(self):
        self.assertEquals(self._interpret('(or 0 1 2)'), '0')

    def test_or_conditional_true(self):
        self.assertEquals(self._interpret('(or (< 1 2) (> 4 3))'), '#t')

    def test_or_conditional_return_expr(self):
        self.assertEquals(self._interpret("(or #f '(1 2) '(3 4))"), '(1 2)')

    def test_or_conditional_false(self):
        self.assertEquals(self._interpret('(or #f (> 3 4))'), '#f')


class AssignmentTestCase(BaseTestCase):

    def test_assignment(self):
        result = self._interpret(
            """
            (define a 5)
            (set! a 7)

            a
            """)
        self.assertEquals(result, '7')

    def test_assignment_outer_scope(self):
        result = self._interpret(
            """
            ((lambda (x)
               (define y x)
               ((lambda (z)
                  (set! y z))
                 3)
               y)
             10)
            """)
        self.assertEquals(result, '3')

    def test_assignment_exception(self):
        self.assertRaises(NameError, self._interpret, '(set! a 5)')


class BindingTestCase(BaseTestCase):

    def test_binding_let_selfeval_expressions(self):
        result = self._interpret(
            """
            (let ((x 1) (y 2))
              (+ x y))
            """)
        self.assertEquals(result, '3')

    def test_binding_let_builtin_procedures_as_expressions(self):
        result = self._interpret(
            """
            (let ((x (* 3 3)) (y (+ 1 10)))
              (+ x y))
            """)
        self.assertEquals(result, '20')

    def test_binding_let_quoted_expressions(self):
        result = self._interpret(
            """
            (let ((x 'a) (y '(b c)))
              (cons x y))
            """)
        self.assertEquals(result, '(a b c)')


class SequencingTestCase(BaseTestCase):

    def test_begin(self):
        result = self._interpret(
            """
            (define x 3)
            (begin
              (set! x (+ x 1))
              (+ x x))
            """)
        self.assertEquals(result, '8')

    def test_begin_with_definitions(self):
        result = self._interpret(
            """
            (let ()
              (begin (define x 3) (define y 4))
              (+ x y))
            """)
        self.assertEquals(result, '7')


class DefinitionTestCase(BaseTestCase):

    def test_define(self):
        result = self._interpret('(define a 5)')
        self.assertEquals(result, 'ok')

    def test_define_procedure(self):
        result = self._interpret(
            """
            (define (simple p1 p2)
              (cons p1 p2))

            simple
            """)
        self.assertEquals(
            result, '#<procedure (p1 p2) ((cons p1 p2)) <procedure-env>')


class EnvironmentLookupTestCase(BaseTestCase):

    def test_lookup_variable_number_value(self):
        result = self._interpret(
            """
            (define a 5)

            a
            """)
        self.assertEquals(result, '5')

    def test_lookup_variable_list_value(self):
        result = self._interpret(
            """
            (define b (quote (1 . (2 . ()))))

            b
            """)
        self.assertEquals(result, '(1 2)')

    def test_lookup_variable_value_exception(self):
        self.assertRaises(NameError, self._interpret, 'a')


class ProcedureApplicationTestCase(BaseTestCase):

    def test_apply_compound_procedure(self):
        result = self._interpret(
            """
            (define (simple p1 p2)
              (cons p1 p2))

            (simple 1 3)
            """)
        self.assertEquals(result, '(1 . 3)')

    def test_apply_nested_compound_procedure(self):
        result = self._interpret(
            """
            (define b 20)

            (define (simple p1 p2)
              (define (nested a)
                (+ a b 10))
              (cons (nested 5) (cons p1 p2)))

            (simple 1 3)
            """)
        self.assertEquals(result, '(35 1 . 3)')

    def test_apply_recursive_compound_procedure(self):
        result = self._interpret(
            """
            (define (factorial num)
              (if (= num 0)
                1
                (* num (factorial (- num 1)))))

            (factorial 5)
            """)
        self.assertEquals(result, '120')

    def test_apply_procedure_without_parameters(self):
        result = self._interpret(
            """
            (define (sum)
              '(1 2 3))

            (sum)
            """)
        self.assertEquals(result, '(1 2 3)')

    def test_apply_compound_procedure_defined_with_lambda(self):
        result = self._interpret(
            """
            (define add1
              (lambda (n) (+ n 1)))

            (define sub1
              (lambda (n) (- n 1)))

            (define o+
              (lambda (n m)
                (cond
                  ((zero? m) n)
                  (else (add1 (o+ n (sub1 m)))))))

            (o+ 46 12)
            """)
        self.assertEquals(result, '58')


class BuiltinTestCase(BaseTestCase):

    def test_number_builtin_add(self):
        result = self._interpret('(+ 1 2 3 4)')
        self.assertEquals(result, '10')

    def test_number_builtin_sub(self):
        result = self._interpret('(- 10 2 11)')
        self.assertEquals(result, '-3')

    def test_number_builtin_mul(self):
        result = self._interpret('(* 3 2 5)')
        self.assertEquals(result, '30')

    def test_number_builtin_div(self):
        result = self._interpret('(/ 30 2 5)')
        self.assertEquals(result, '3')

    def test_number_builtin_eq_predicate_false(self):
        result = self._interpret('(= 1 2)')
        self.assertEquals(result, '#f')

    def test_number_builtin_eq_predicate_true(self):
        result = self._interpret('(= 3 3 3)')
        self.assertEquals(result, '#t')

    def test_number_builtin_lt_predicate_false(self):
        result = self._interpret('(< 2 1)')
        self.assertEquals(result, '#f')

    def test_number_builtin_lt_predicate_true(self):
        result = self._interpret('(< 1 2 3)')
        self.assertEquals(result, '#t')

    def test_number_builtin_le_predicate_true(self):
        result = self._interpret('(<= 1 2 3 3)')
        self.assertEquals(result, '#t')

    def test_number_builtin_le_predicate_false(self):
        result = self._interpret('(<= 1 2 3 1)')
        self.assertEquals(result, '#f')

    def test_number_builtin_gt_predicate_true(self):
        result = self._interpret('(> 3 2 1)')
        self.assertEquals(result, '#t')

    def test_number_builtin_gt_predicate_false(self):
        result = self._interpret('(> 1 2)')
        self.assertEquals(result, '#f')

    def test_number_builtin_ge_predicate_true(self):
        result = self._interpret('(>= 3 3 1)')
        self.assertEquals(result, '#t')

    def test_number_builtin_ge_predicate_false(self):
        result = self._interpret('(>= 2 2 3)')
        self.assertEquals(result, '#f')

    def test_number_builtin_comparison_with_one_argument(self):
        for op in ('<', '>', '=', '<=', '>='):
            self.assertEquals(self._interpret('(%s 7)' % op), '#t')

    def test_number_builtin_abs_positive_argument(self):
        result = self._interpret('(abs 3)')
        self.assertEquals(result, '3')

    def test_number_builtin_abs_negative_argument(self):
        result = self._interpret('(abs -3)')
        self.assertEquals(result, '3')

    def test_pair_builtin_car(self):
        result = self._interpret("(car '(1 2 3))")
        self.assertEquals(result, '1')

    def test_pair_builtin_list(self):
        result = self._interpret(
            """
            (define x -4)
            (list 'minus (abs x))
            """)
        self.assertEquals(result, '(minus 4)')

    def test_improper_list_builtin_pair_p(self):
        result = self._interpret("(pair? '(1 . 2))")
        self.assertEquals(result, '#t')

    def test_proper_list_builtin_pair_p(self):
        result = self._interpret("(pair? '(1 2))")
        self.assertEquals(result, '#t')

    def test_empty_list_builtin_pair_p(self):
        result = self._interpret("(pair? '())")
        self.assertEquals(result, '#f')

    def test_empty_list_builtin_null_p(self):
        result = self._interpret("(null? '())")
        self.assertEquals(result, '#t')

    def test_symbol__builtin_null_p(self):
        result = self._interpret("(null? 'abc)")
        self.assertEquals(result, '#f')

    def test_builtin_not_false_as_argument(self):
        self.assertEquals(self._interpret('(not #f)'), '#t')

    def test_builtin_not_true_as_argument(self):
        self.assertEquals(self._interpret('(not #t)'), '#f')

    def test_builtin_not_empty_list_as_argument(self):
        self.assertEquals(self._interpret("(not '())"), '#f')

    def test_builtin_not_expression_as_argument(self):
        self.assertEquals(self._interpret('(not (< 4 5))'), '#f')

    def test_builtin_eq_p_true_true(self):
        self.assertEquals(self._interpret('(eq? #t #t)'), '#t')

    def test_builtin_eq_p_false_true(self):
        self.assertEquals(self._interpret('(eq? #f #t)'), '#f')

    def test_builtin_eq_p_symbol_symbol(self):
        self.assertEquals(self._interpret("(eq? 'a 'a)"), '#t')

    def test_builtin_zero_p_zero(self):
        self.assertEquals(self._interpret("(zero? 0)"), '#t')

    def test_builtin_zero_p_one(self):
        self.assertEquals(self._interpret("(zero? 1)"), '#f')

    def test_builtin_number_p_true(self):
        self.assertEquals(self._interpret("(number? 1)"), '#t')

    def test_builtin_number_p_false(self):
        self.assertEquals(self._interpret("(number? 'abc)"), '#f')

    def test_builtin_number_expt(self):
        self.assertEquals(self._interpret("(expt 2 10)"), '1024')

    def test_builtin_list_empty_list(self):
        self.assertEquals(self._interpret("(length '())"), '0')

    def test_builtin_list(self):
        self.assertEquals(self._interpret("(length '(1 2 3 7))"), '4')

    def test_builtin_even_p_true(self):
        self.assertEquals(self._interpret('(even? 0)'), '#t')

    def test_builtin_even_p_false(self):
        self.assertEquals(self._interpret('(even? 1)'), '#f')


class InterpreterLoadProcedureTestCase(unittest.TestCase):

    def setUp(self):
        datadir = os.path.join(THIS_MODULE_DIR, 'data')
        os.mkdir(os.path.join(datadir))
        with open(os.path.join(datadir, 'test.ss'), 'w') as fout:
            fout.write("""\
            (define a 10)

            (define c '(1 2 3))
            """)

    def tearDown(self):
        shutil.rmtree(os.path.join(THIS_MODULE_DIR, 'data'))

    def test_load_procedure(self):
        from serval.lexer import Lexer
        from serval.parser import Parser
        from serval.interpreter import Interpreter
        from serval.expression.util import load

        interp = Interpreter()
        filepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data', 'test.ss')
        expr = Parser(Lexer('(load "%s")' % filepath)).parse()[0]
        load(interp, expr)

        expr = Parser(Lexer('c')).parse()[0]
        result = interp.interpret(expr)
        self.assertEquals(str(result), '(1 2 3)')


