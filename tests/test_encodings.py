# Copyright (c) 2019 Dmitry Marakasov <amdmi3@amdmi3.ru>
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

import unittest

from .common import runJS


class TestJsonSlicerEncodings(unittest.TestCase):
    def test_encodings_bytes_unicode_default(self):
        self.assertEqual(
            runJS(b'{"foo":"bar"}', ('foo',)),
            ['bar']
        )

    def test_encodings_bytes_unicode_unicode(self):
        self.assertEqual(
            runJS(b'{"foo":"bar"}', ('foo',), encoding='utf-8'),
            ['bar']
        )

    def test_encodings_bytes_unicode_binary(self):
        self.assertEqual(
            runJS(b'{"foo":"bar"}', (b'foo',), binary=True),
            [b'bar']
        )

    def test_encodings_unicode_unicode_default(self):
        self.assertEqual(
            runJS('{"foo":"bar"}', ('foo',)),
            ['bar']
        )

    def test_encodings_unicode_unicode_unicode(self):
        self.assertEqual(
            runJS('{"foo":"bar"}', ('foo',), encoding='utf-8'),
            ['bar']
        )

    def test_encodings_unicode_unicode_binary(self):
        self.assertEqual(
            runJS('{"foo":"bar"}', (b'foo',), binary=True),
            [b'bar']
        )

    def test_encodings_bytes_bytes_default(self):
        self.assertEqual(
            runJS(b'{"foo":"bar"}', ('foo',)),
            ['bar']
        )

    def test_encodings_bytes_bytes_unicode(self):
        self.assertEqual(
            runJS(b'{"foo":"bar"}', ('foo',), encoding='utf-8'),
            ['bar']
        )

    def test_encodings_bytes_bytes_binary(self):
        self.assertEqual(
            runJS(b'{"foo":"bar"}', (b'foo',), binary=True),
            [b'bar']
        )

    def test_encodings_unicode_bytes_default(self):
        self.assertEqual(
            runJS('{"foo":"bar"}', ('foo',)),
            ['bar']
        )

    def test_encodings_unicode_bytes_unicode(self):
        self.assertEqual(
            runJS('{"foo":"bar"}', ('foo',), encoding='utf-8'),
            ['bar']
        )

    def test_encodings_unicode_bytes_binary(self):
        self.assertEqual(
            runJS('{"foo":"bar"}', (b'foo',), binary=True),
            [b'bar']
        )


if __name__ == '__main__':
    unittest.main()
