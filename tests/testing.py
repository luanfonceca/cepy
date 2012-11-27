from __future__ import print_function
import os
import sys
import unittest


def save_and_restore_environ(class_):
    def empty(self):
        pass
    orig_setup = getattr(class_, 'setUp', empty)
    orig_teardown = getattr(class_, 'tearDown', empty)
    def setup(self):
        self._preserved_environ = os.environ.copy()
        orig_setup(self)
    def teardown(self):
        orig_teardown(self)
        os.environ.clear()
        os.environ.update(self._preserved_environ)
    class_.setUp = setup
    class_.tearDown = teardown
    return class_

#  Patch unittest.TestCase as necessary
if (sys.version_info[0], sys.version_info[1]) < (2, 7):
    class TestCase(unittest.TestCase):
        def setUp(self):
            pass
        def tearDown(self):
            pass
        def assertIsNotNone(self, obj, msg=None):
            self.failIf(obj is None, msg or 'value should not be None')
        def assertIsNone(self, obj, msg=None):
            self.failIf(obj is not None, msg or 'value should be None')
else:
    class TestCase(unittest.TestCase):
        def setUp(self):
            pass
        def tearDown(self):
            pass

#  If we cannot import mock, then cause any tests using patching to fail
#  somewhat gracefully.
try:
    import mock
    patch = mock.patch
except:
    def ignore_this(*patch_args):
        def wrapped(test):
            print('*** ignoring %s.%s' %(test.__module__, test.__name__))
        return wrapped
    patch = ignore_this

