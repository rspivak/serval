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


class Number(object):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.val == other.val

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return isinstance(other, self.__class__) and self.val < other.val

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __nonzero__(self):
        return True


class Boolean(object):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return '#t' if self.val else '#f'

    def __nonzero__(self):
        return self.val

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.val == other.val


class Character(object):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return '#\\' + self.val

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.val == other.val

    def __nonzero__(self):
        return True


class String(object):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return '"%s"' % self.val

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.val == other.val

    def __nonzero__(self):
        return True


class Symbol(object):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Symbol) and self.name == other.name:
            return True

        return False

    def __nonzero__(self):
        return True


class EmptyList(object):

    def __str__(self):
        return '()'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __nonzero__(self):
        return True

EmptyList = EmptyList()


class Pair(object):

    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def __str__(self):
        return '(%s)' % self._write_pair(self)

    @staticmethod
    def _write_pair(pair):
        head, tail = pair.head, pair.tail

        output = str(head)

        if isinstance(tail, Pair):
            output += ' %s' % Pair._write_pair(tail)
            return output

        if tail is EmptyList:
            return output

        output += ' . %s' % str(tail)
        return output




















