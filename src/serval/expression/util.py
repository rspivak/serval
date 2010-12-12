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

from serval.lexer import Lexer
from serval.parser import Parser
from serval.model import Pair, Symbol, EmptyList


def is_tagged_list(expr, tag):
    if isinstance(expr, Pair) and car(expr) == tag:
        return True

    return False

def is_symbol(expr):
    return isinstance(expr, Symbol)

def cons(head, tail):
    return Pair(head, tail)

def car(pair):
    return pair.head

def cdr(pair):
    return pair.tail

def tolist(*expressions):
    def inner(args):
        if not args:
            return EmptyList
        return cons(args[0], inner(args[1:]))

    return inner(expressions)

caar = lambda pair: car(car(pair))
cadr = lambda pair: car(cdr(pair))
caddr = lambda pair: car(cdr(cdr(pair)))
cadar = lambda pair: car(cdr(car(pair)))
cdddr = lambda pair: cdr(cdr(cdr(pair)))
cadddr = lambda pair: car(cdr(cdr(cdr(pair))))
caadr = lambda pair: car(car(cdr(pair)))
cdadr = lambda pair: cdr(car(cdr(pair)))
cddr = lambda pair: cdr(cdr(pair))

def pair_to_list(pair):
    result = []
    if pair is EmptyList:
        return result

    head, tail = pair.head, pair.tail
    result.append(head)
    while tail is not EmptyList:
        head, tail = tail.head, tail.tail
        result.append(head)

    return result

def is_load(expr):
    return is_tagged_list(expr, Symbol('load'))

def load(interpreter, expression):
    """Read expression and definitions from the file.

    After reading the procedure evaluates expressions
    and definitions  sequentially.
    """
    filepath = cadr(expression).val
    data = open(os.path.abspath(filepath)).read()
    parser = Parser(Lexer(data))

    for expr in parser.parse():
        interpreter.interpret(expr)

