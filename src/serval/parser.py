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

import itertools

from serval import tokens
from serval.model import (
    Number, Boolean, Character, String, Symbol, Pair, EmptyList)

# datum: simple_datum | compound_datum
# simple_datum: boolean | number | character | string | symbol
# symbol: identifier
# compound_datum: list
# list: ( datum *) | ( datum + . datum ) | abbreviation
# abbreviation: abbrev_prefix datum
# abbrev_prefix: '

class ParserException(Exception):
    pass


class Parser(object):
    """Parser for a Scheme subset.

    Partially implements grammar definition from R5RS
    """

    def __init__(self, lexer):
        self.lexer = lexer
        self.marks = []
        self.lookahead = []
        self.pos = 0
        self._sync(1)

    def parse(self):
        """Main entry method.

        Returns a list of parsed expressions.
        """
        result = []
        while self._lookahead_type(0) != tokens.EOF:
            result.append(self._datum())
        return result

    def _datum(self):

        if self._lookahead_type(0) in (tokens.LPAREN, tokens.QUOTE):
            return self._list()

        return self._simple_datum()

    def _simple_datum(self):
        token = self._lookahead_token(0)

        if token.type == tokens.NUMBER:
            expr = Number(int(token.text))

        elif token.type == tokens.BOOLEAN:
            expr = Boolean(True if token.text == '#t' else False)

        elif token.type == tokens.CHARACTER:
            expr = Character(token.text[2:])

        elif token.type == tokens.STRING:
            expr = String(token.text.strip('"'))

        elif token.type == tokens.ID:
            expr = Symbol(token.text)

        else:
            raise ParserException('No viable alternative')

        self._match(token.type)
        return expr

    def _abbreviation(self):
        self._match(tokens.QUOTE)

        if self._lookahead_type(0) == tokens.LPAREN:
            expr = self._list()
        else:
            expr = self._simple_datum()

        return Pair(Symbol('quote'), Pair(expr, EmptyList))

    def _list(self):
        result = []

        if self._lookahead_type(0) == tokens.QUOTE:
            return self._abbreviation()

        self._match(tokens.LPAREN)

        # empty list
        if self._lookahead_type(0) == tokens.RPAREN:
            self._match(tokens.RPAREN)
            return EmptyList

        index, dot_index = 0, -1

        while self._lookahead_type(0) != tokens.RPAREN:
            head = self._datum()

            if self._lookahead_type(0) == tokens.DOT:
                self._match(tokens.DOT)
                tail = self._datum()
                result.append(Pair(head, tail))
                dot_index = index
                break
            else:
                result.append(head)

            index += 1

        self._match(tokens.RPAREN)

        if dot_index > 0:
            dot_index = len(result) - dot_index - 1

        tail = EmptyList
        for index, expr in enumerate(reversed(result)):
            if index == dot_index:
                tail = expr
            else:
                tail = Pair(expr, tail)

        return tail

    ##########################################################
    # Parser helper methods
    ##########################################################
    def _sync(self, index):
        if index + self.pos > len(self.lookahead):
            number = index + self.pos - len(self.lookahead)
            self._fill(number)

    def _fill(self, number):
        self.lookahead.extend(itertools.islice(self.lexer, 0, number))

    def _lookahead_type(self, number):
        return self._lookahead_token(number).type

    def _lookahead_token(self, number):
        self._sync(number)
        return self.lookahead[self.pos + number]

    def _match(self, token_type):
        if self._lookahead_type(0) == token_type:
            self._consume()
        else:
            raise ParserException(
                'Expecting %s; found %s' % (
                    token_type, self._lookahead_token(0))
                )

    def _consume(self):
        self.pos += 1
        if self.pos == len(self.lookahead) and not self._is_speculating():
            self.lookahead = []
            self.pos = 0

        self._sync(1)

    def _is_speculating(self):
        return bool(self.marks)

    def _mark(self):
        self.marks.append(self.pos)

    def _release(self):
        self._seek(self.marks.pop())

    def _index(self):
        return self.pos

    def _seek(self, index):
        self.pos = index

