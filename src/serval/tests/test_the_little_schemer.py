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

import unittest


class LittleSchemerEvaluatorTestCase(unittest.TestCase):

    TEXT = """
    (define atom?
     (lambda (x)
        (and (not (pair? x)) (not (null? x)))))

    (define build
      (lambda (s1 s2)
        (cons s1 (cons s2 (quote ())))))

    (define new-entry build)

    (define first
      (lambda (p)
        (car p)))

    (define second
      (lambda (p)
        (car (cdr p))))

    (define third
      (lambda (l)
        (car (cdr (cdr l)))))

    (define lookup-in-entry
      (lambda (name entry entry-f)
        (lookup-in-entry-help name
          (first entry)
          (second entry)
          entry-f)))

    (define lookup-in-entry-help
      (lambda (name names values entry-f)
        (cond
          ((null? names) (entry-f name))
          ((eq? (car names) name)
           (car values))
          (else (lookup-in-entry-help
                  name
                  (cdr names)
                  (cdr values)
                  entry-f)))))

    ; A table (an environment in SICP) is a list of pairs
    ;
    (define extend-table cons)

    (define lookup-in-table
      (lambda (name table table-f)
        (cond
          ((null? table) (table-f name))
          (else (lookup-in-entry name
                  (car table)
                  (lambda (name)
                    (lookup-in-table name
                      (cdr table)
                      table-f)))))))

    (define expression-to-action
      (lambda (e)
        (cond
          ((atom? e) (atom-to-action e))
          (else
            (list-to-action e)))))

    (define atom-to-action
      (lambda (e)
        (cond
          ((number? e) *const)
          ((eq? e #t) *const)
          ((eq? e #f) *const)
          ((eq? e (quote cons)) *const)
          ((eq? e (quote car)) *const)
          ((eq? e (quote cdr)) *const)
          ((eq? e (quote null?)) *const)
          ((eq? e (quote eq?)) *const)
          ((eq? e (quote atom?)) *const)
          ((eq? e (quote zero?)) *const)
          ((eq? e (quote add1)) *const)
          ((eq? e (quote sub1)) *const)
          ((eq? e (quote number?)) *const)
          (else *identifier))))

    (define list-to-action
      (lambda (e)
        (cond
          ((atom? (car e))
           (cond
             ((eq? (car e) (quote quote))
              *quote)
             ((eq? (car e) (quote lambda))
              *lambda)
             ((eq? (car e) (quote cond))
              *cond)
             (else *application)))
          (else *application))))

    ; EVAL
    ;
    (define value
      (lambda (e)
        (meaning e (quote ()))))

    (define meaning
      (lambda (e table)
        ((expression-to-action e) e table)))

    (define *const
      (lambda (e table)
        (cond
          ((number? e) e)
          ((eq? e #t) #t)
          ((eq? e #f) #f)
          (else
            (build (quote primitive) e)))))

    (define *quote
      (lambda (e table)
        (text-of e)))

    (define text-of second)

    (define *identifier
      (lambda (e table)
        (lookup-in-table e table initial-table)))

    (define initial-table
      (lambda (name)
        (car (quote ()))))

    (define *lambda
      (lambda (e table)
        (build (quote non-primitive)
               (cons table (cdr e)))))

    (define table-of first)
    (define formals-of second)
    (define body-of third)

    (define evcon
      (lambda (lines table)
        (cond
          ((else? (question-of (car lines)))
           (meaning (answer-of (car lines)) table))
          ((meaning (question-of (car lines)) table)
           (meaning (answer-of (car lines)) table))
          (else
            (evcon (cdr lines) table)))))


    (define else?
      (lambda (x)
        (cond
          ((atom? x) (eq? x (quote else)))
          (else #f))))

    (define question-of first)
    (define answer-of second)

    (define *cond
      (lambda (e table)
        (evcon (cond-lines-of e) table)))

    (define cond-lines-of cdr)

    (define evlis
      (lambda (args table)
        (cond
          ((null? args) (quote ()))
          (else
            (cons (meaning (car args) table)
                  (evlis (cdr args) table))))))

    (define *application
      (lambda (e table)
        (applyf
          (meaning (function-of e) table)
          (evlis (arguments-of e) table))))

    (define function-of car)
    (define arguments-of cdr)

    (define primitive?
      (lambda (l)
        (eq? (first l) (quote primitive))))

    (define non-primitive?
      (lambda (l)
        (eq? (first l) (quote non-primitive))))

    ; APPLY
    ;
    (define applyf
      (lambda (fun vals)
        (cond
          ((primitive? fun)
           (apply-primitive (second fun) vals))
          ((non-primitive? fun)
           (apply-closure (second fun) vals)))))

    ; APPLY PRIMITIVE + EXAMPLE OF QUOTE USAGE: '
    ;
    (define apply-primitive
      (lambda (name vals)
        (cond
          ((eq? name 'cons)
           (cons (first vals) (second vals)))
          ((eq? name 'car)
           (car (first vals)))
          ((eq? name 'cdr)
           (cdr (first vals)))
          ((eq? name 'null?)
           (null? (first vals)))
          ((eq? name 'eq?)
           (eq? (first vals) (second vals)))
          ((eq? name 'atom?)
           (:atom? (first vals)))
          ((eq? name 'zero?)
           (zero? (first vals)))
          ((eq? name 'add1)
           (+ 1 (first vals)))
          ((eq? name 'sub1)
           (- 1 (first vals)))
          ((eq? name 'number?)
           (number? (first vals))))))

    (define :atom?
      (lambda (x)
        (cond
          ((atom? x) #t)
          ((null? x) #f)
          ((eq? (car x) (quote primitive))
           #t)
          ((eq? (car x) (quote non-primitive))
           #t)
          (else #f))))

    (define apply-closure
      (lambda (closure vals)
        (meaning (body-of closure)
          (extend-table (new-entry
                          (formals-of closure)
                          vals)
                        (table-of closure)))))
    """

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

    def _get_interpreter(self):
        from serval.interpreter import Interpreter

        interpreter = Interpreter()
        self._interpret(self.TEXT, interpreter=interpreter)

        return interpreter

    def test_value_add1(self):
        interpreter = self._get_interpreter()

        result = self._interpret("(value '(add1 6))", interpreter=interpreter)
        self.assertEquals(result, '7')

    def test_value_quote(self):
        interpreter = self._get_interpreter()

        result = self._interpret(
            "(value '(quote (a b c)))", interpreter=interpreter)
        self.assertEquals(result, '(a b c)')

    def test_value_car(self):
        interpreter = self._get_interpreter()

        result = self._interpret(
            "(value '(car (quote (a b c))))", interpreter=interpreter)
        self.assertEquals(result, 'a')

    def test_value_cdr(self):
        interpreter = self._get_interpreter()

        result = self._interpret(
            "(value '(cdr (quote (a b c))))", interpreter=interpreter)
        self.assertEquals(result, '(b c)')

    def test_value_lambda(self):
        interpreter = self._get_interpreter()

        result = self._interpret(
            """
            (value
              '((lambda (x)
                (cond
                  (x (cons x 'true))
                  (else
                    (cons x 'false))))
                #f))
            """,
            interpreter=interpreter)
        self.assertEquals(result, '(#f . false)')
