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

from serval.model import Symbol, Boolean, EmptyList
from serval.expression.sequence import sequence_exp
from serval.expression.util import (
    is_tagged_list, car, cdr, cadr, caddr, cdddr, cadddr, tolist)


def is_if(expr):
    return is_tagged_list(expr, Symbol('if'))

def if_predicate(expr):
    return cadr(expr)

def if_consequent(expr):
    return caddr(expr)

def if_alternative(expr):
    if cdddr(expr) is not EmptyList:
        return cadddr(expr)

    return False

def make_if(predicate, consequent, alternative):
    return tolist(Symbol('if'), predicate, consequent, alternative)

def is_and(expr):
    return is_tagged_list(expr, Symbol('and'))

def is_or(expr):
    return is_tagged_list(expr, Symbol('or'))

def is_cond(expr):
    return is_tagged_list(expr, Symbol('cond'))

def cond_clauses(expr):
    return cdr(expr)

def is_cond_else_clause(clause):
    return cond_predicate(clause) == Symbol('else')

def cond_predicate(clause):
    return car(clause)

def cond_actions(clause):
    return cdr(clause)

def cond_to_if(expr):
    return expand_clauses(cond_clauses(expr))

def expand_clauses(clauses):
    if clauses is EmptyList:
        return Boolean(False)

    first = car(clauses)
    rest = cdr(clauses)

    if is_cond_else_clause(first):
        if rest is EmptyList:
            return sequence_exp(cond_actions(first))
        else:
            raise ValueError("ELSE clause isn't last: %s" % clauses)
    else:
        return make_if(cond_predicate(first),
                       sequence_exp(cond_actions(first)), expand_clauses(rest))

