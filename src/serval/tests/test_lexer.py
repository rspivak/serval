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

from serval import tokens


class LexerTestCase(unittest.TestCase):

    def _get_token(self, text):
        from serval.lexer import Lexer
        return Lexer(text).token()

    def test_skip_ws(self):
        token = self._get_token('  123')
        self.assertEquals(token.text, '123')

    def test_number(self):
        token = self._get_token('123\n')
        self.assertEquals(token.type, tokens.NUMBER)
        self.assertEquals(token.text, '123')

    def test_boolean_true(self):
        token = self._get_token('#t')
        self.assertEquals(token.type, tokens.BOOLEAN)
        self.assertEquals(token.text, '#t')

    def test_boolean_false(self):
        token = self._get_token('#f')
        self.assertEquals(token.type, tokens.BOOLEAN)
        self.assertEquals(token.text, '#f')

    def test_character(self):
        token = self._get_token('#\c')
        self.assertEquals(token.type, tokens.CHARACTER)
        self.assertEquals(token.text, '#\c')

    def test_character_newline(self):
        token = self._get_token(r'#\newline')
        self.assertEquals(token.type, tokens.CHARACTER)
        self.assertEquals(token.text, r'#\newline')

    def test_character_space(self):
        token = self._get_token(r'#\space')
        self.assertEquals(token.type, tokens.CHARACTER)
        self.assertEquals(token.text, r'#\space')

    def test_string(self):
        token = self._get_token(r'"hello\"world"')
        self.assertEquals(token.type, tokens.STRING)
        self.assertEquals(token.text, r'"hello\"world"')

    def test_lexer_iterator(self):
        from serval.lexer import Lexer
        lexer = Lexer(r'"hello\"world" #\c #t')
        it = iter(lexer)

        token = next(it)
        self.assertEquals(token.type, tokens.STRING)

        token = next(it)
        self.assertEquals(token.type, tokens.CHARACTER)

        token = next(it)
        self.assertEquals(token.type, tokens.BOOLEAN)

        token = next(it)
        self.assertEquals(token.type, tokens.EOF)

        self.assertRaises(StopIteration, lambda: next(it))

    def test_quote(self):
        token = self._get_token(" ' ")
        self.assertEquals(token.type, tokens.QUOTE)
        self.assertEquals(token.text, "'")

    def test_left_parenthesis(self):
        token = self._get_token('(')
        self.assertEquals(token.type, tokens.LPAREN)
        self.assertEquals(token.text, '(')

    def test_right_parenthesis(self):
        token = self._get_token(')')
        self.assertEquals(token.type, tokens.RPAREN)
        self.assertEquals(token.text, ')')

    def test_dot(self):
        token = self._get_token(' . ')
        self.assertEquals(token.type, tokens.DOT)
        self.assertEquals(token.text, '.')

    def test_id(self):
        token = self._get_token('quote')
        self.assertEquals(token.type, tokens.ID)
        self.assertEquals(token.text, 'quote')

    def test_id_eq(self):
        token = self._get_token('=')
        self.assertEquals(token.type, tokens.ID)
        self.assertEquals(token.text, '=')

    def test_id_lt(self):
        token = self._get_token('<')
        self.assertEquals(token.type, tokens.ID)
        self.assertEquals(token.text, '<')

    def test_id_gt(self):
        token = self._get_token('>')
        self.assertEquals(token.type, tokens.ID)
        self.assertEquals(token.text, '>')

    def test_id_le(self):
        token = self._get_token('<=')
        self.assertEquals(token.type, tokens.ID)
        self.assertEquals(token.text, '<=')

    def test_id_ge(self):
        token = self._get_token('>=')
        self.assertEquals(token.type, tokens.ID)
        self.assertEquals(token.text, '>=')

    def test_id_with_trailing_plus_sign(self):
        token = self._get_token('o+')
        self.assertEquals(token.type, tokens.ID)
        self.assertEquals(token.text, 'o+')

    def test_id_with_leading_plus_sign(self):
        token = self._get_token('+o')
        self.assertEquals(token.type, tokens.ID)
        self.assertEquals(token.text, '+o')

    def test_id_with_leading_digits(self):
        token = self._get_token('1st-sub-exp')
        self.assertEquals(token.type, tokens.ID)
        self.assertEquals(token.text, '1st-sub-exp')

    def test_id_with_leading_dot(self):
        token = self._get_token('.+')
        self.assertEquals(token.type, tokens.ID)
        self.assertEquals(token.text, '.+')

    def test_comment(self):
        token = self._get_token(
            """
            ; <
            >=
            """)
        self.assertEquals(token.type, tokens.ID)
        self.assertEquals(token.text, '>=')

