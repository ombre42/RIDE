#  Copyright 2008 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest
import sys
import os

from robot.utils.asserts import assert_equals, assert_true

from resources import DATAPATH
from robotide.spec.xmlreaders import init_from_spec

sys.path.append(os.path.join(DATAPATH, 'libs'))


class TestLibrarySpec(unittest.TestCase):

    def _spec(self, name):
        return init_from_spec(name)

    def test_reading_library_from_xml(self):
        kws = self._spec('LibSpecLibrary')
        assert_equals(len(kws), 3)
        exp_doc = 'This is kw documentation.\n\nThis is more docs.'
        self._assert_keyword(kws[0], 'Normal Keyword', exp_doc,
                             exp_doc.splitlines()[0], '[ foo ]')
        self._assert_keyword(kws[1], 'Attributeless Keyword')
        self._assert_keyword(kws[2], 'Multiarg Keyword',
                             args='[ arg1 | arg2=default value | *args ]')

    def test_reading_library_from_old_style_xml(self):
        kws = self._spec('OldStyleLibSpecLibrary')
        assert_equals(len(kws), 3)
        exp_doc = 'This is kw documentation.\n\nThis is more docs.'
        self._assert_keyword(kws[0], 'Normal Keyword', exp_doc,
                             exp_doc.splitlines()[0], '[ foo ]')
        self._assert_keyword(kws[1], 'Attributeless Keyword')
        self._assert_keyword(kws[2], 'Multiarg Keyword',
                             args='[ arg1 | arg2=default value | *args ]')

    def _assert_keyword(self, kw, name, doc='', shortdoc='', args='[  ]'):
        assert_equals(kw.name, name)
        assert_equals(kw.doc, doc, repr(kw.doc))
        assert_equals(kw.shortdoc, shortdoc)
        if args:
            assert_equals(kw.args, args)


if __name__ == '__main__':
    unittest.main()
