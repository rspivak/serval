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

from serval.expression.procedure import (primitive_procedure_names,
                                         primitive_procedure_values)
from serval.expression.util import pair_to_list


class Environment(object):

    def __init__(self, parent=None, bindings=None):
        self.parent = parent
        self.bindings = dict() if bindings is None else bindings

    def define_variable(self, symbol, val):
        self.bindings[symbol.name] = val

    def set_variable_value(self, symbol, val):
        name = symbol.name
        if name in self.bindings:
            self.bindings[name] = val

        elif self.parent is not None:
            self.parent.set_variable_value(symbol, val)

        else:
            raise NameError('Unbound variable - SET! %s' % name)

    def load(self, symbol):
        name = symbol.name
        if name in self.bindings:
            return self.bindings[name]

        if self.parent is not None:
            return self.parent.load(symbol)

        return None


def setup_environment():
    bindings = dict(
        zip(primitive_procedure_names(), primitive_procedure_values())
        )

    return Environment(bindings=bindings)

def define_variable(var, val, env):
    env.define_variable(var, val)

def lookup_variable_value(var, env):
    val = env.load(var)
    if val is None:
        raise NameError('Unbound variable: %s' % var)
    return val

def extend_environment(variables, values, env):
    bindings = dict(zip([var.name for var in pair_to_list(variables)],
                        pair_to_list(values)))

    env = Environment(parent=env, bindings=bindings)
    return env
