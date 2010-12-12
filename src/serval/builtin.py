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

import operator
import functools

from serval.model import Number, Boolean, Pair, EmptyList
from serval.expression.util import cdr


def _perform_arithmetic_function(func, *args):
    return Number(reduce(func, [int(arg.val) for arg in args]))

builtin_add = functools.partial(_perform_arithmetic_function, operator.add)
builtin_sub = functools.partial(_perform_arithmetic_function, operator.sub)
builtin_mul = functools.partial(_perform_arithmetic_function, operator.mul)
builtin_div = functools.partial(_perform_arithmetic_function, operator.div)

def _perform_comparison(func, *args):
    if len(args) == 1:
        return Boolean(True)

    prev, rest = args[0], args[1:]
    for arg in rest:
        if not func(prev, arg):
            return Boolean(False)
        prev = arg

    return Boolean(True)

builtin_eq = functools.partial(_perform_comparison, operator.eq)
builtin_lt = functools.partial(_perform_comparison, operator.lt)
builtin_le = functools.partial(_perform_comparison, operator.le)
builtin_gt = functools.partial(_perform_comparison, operator.gt)
builtin_ge = functools.partial(_perform_comparison, operator.ge)

def builtin_pair_p(*args):
    arg = args[0]
    return Boolean(isinstance(arg, Pair))

def builtin_null_p(*args):
    return Boolean(args[0] is EmptyList)

def builtin_cons(*args):
    first, second = args
    return Pair(first, second)

def builtin_car(*args):
    arg = args[0]
    return arg.head

def builtin_cdr(*args):
    arg = args[0]
    return arg.tail

def builtin_list(*args):
    def inner(args):
        if not args:
            return EmptyList
        return Pair(args[0], inner(args[1:]))

    return inner(args)

def builtin_abs(*args):
    return Number(abs(args[0].val))

def builtin_not(*args):
    return Boolean(not bool(args[0]))

def builtin_eq_p(*args):
    first, second = args
    return Boolean(first == second)

def builtin_zero_p(*args):
    return Boolean(args[0] == Number(0))

def builtin_number_p(*args):
    return Boolean(isinstance(args[0], Number))

def builtin_expt(*args):
    first, second = args
    return Number(first.val ** second.val)

def builtin_length(*args):
    alist = args[0]

    def inner(arg, count):
        if arg is EmptyList:
            return count
        return inner(cdr(arg), count + 1)

    return inner(alist, 0)

def builtin_even_p(*args):
    return Boolean(args[0].val % 2 == 0)

BUILTIN_PROCEDURES = [
    ('pair?', builtin_pair_p),
    ('eq?', builtin_eq_p),
    ('cons', builtin_cons),
    ('car', builtin_car),
    ('cdr', builtin_cdr),
    ('list', builtin_list),
    ('abs', builtin_abs),
    ('null?', builtin_null_p),
    ('not', builtin_not),
    ('zero?', builtin_zero_p),
    ('number?', builtin_number_p),
    ('expt', builtin_expt),
    ('length', builtin_length),
    ('even?', builtin_even_p),
    ('+', builtin_add),
    ('-', builtin_sub),
    ('*', builtin_mul),
    ('/', builtin_div),
    ('=', builtin_eq),
    ('<', builtin_lt),
    ('<=', builtin_le),
    ('>', builtin_gt),
    ('>=', builtin_ge),
    ]
