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

from serval.model import Symbol, Pair, EmptyList
from serval.expression.util import (
    is_tagged_list, pair_to_list, car, cdr, cons, cadr, caddr, cadddr)
from serval.builtin import BUILTIN_PROCEDURES


#################################
# Procedure application
#################################
def is_application(expr):
    return isinstance(expr, Pair)

def operator(expr):
    return car(expr)

def operands(expr):
    return cdr(expr)

def no_operands(ops):
    return ops is EmptyList

def first_operand(ops):
    return car(ops)

def rest_operands(ops):
    return cdr(ops)

#################################
# Compound procedures
#################################
def make_procedure(params, body, env):
    """Create a list"""
    return cons(Symbol('procedure'),
                cons(params, cons(body, cons(env, EmptyList))))

def is_compound_procedure(expr):
    return is_tagged_list(expr, Symbol('procedure'))

def procedure_parameters(expr):
    return cadr(expr)

def procedure_body(expr):
    return caddr(expr)

def procedure_environment(expr):
    return cadddr(expr)

def get_procedure_repr(expr):
    return '#<procedure %s %s <procedure-env>' % (
        procedure_parameters(expr), procedure_body(expr))

#################################
# Primitive procedures
#################################
def is_primitive_procedure(expr):
    return is_tagged_list(expr, Symbol('primitive'))

def primitive_implementation(expr):
    return cadr(expr)

def primitive_procedure_names():
    return [name for name, _ in BUILTIN_PROCEDURES]

def primitive_procedure_values():
    return [Pair(Symbol('primitive'), Pair(proc, EmptyList))
            for _, proc in BUILTIN_PROCEDURES]

def apply_primitive_procedure(proc, args):
    func = primitive_implementation(proc)
    return func(*pair_to_list(args))
