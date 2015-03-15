import os
import unittest


class PassingTest(unittest.TestCase):
    def test_one(self):
        print 'pid: %d' % os.getpid()


class FailingTest(unittest.TestCase):
    def test_one(self):
        self.assertTrue(False)


class ErroringTest(unittest.TestCase):
    def test_one(self):
        raise Exception('error')


class SkippedTest(unittest.TestCase):
    @unittest.skip('skip reason')
    def test_one(self):
        pass
