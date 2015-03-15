# encoding: utf-8

import os
import unittest
import tempfile
import xml.etree.ElementTree as ET

import nose.plugins

from nose_xunitmp import XunitMP


_here = os.path.dirname(__file__)


class TestProducesOutput(nose.plugins.PluginTester, unittest.TestCase):
    activate = '--with-xunitmp'
    plugins = [XunitMP(), nose.plugins.multiprocess.MultiProcess()]
    suitepath = os.path.join(_here, 'support.py')
    args = ['--processes=2']

    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix='.xml')
        os.close(fd)
        self.args += ['--xunitmp-file=%s' % self.path]
        # Due to the way PluginTester works, the plugins in self.plugins are
        # not automatically loaded in the test processes. If we add them to
        # _instantiate_plugins, then the multiprocessing plugin will load them.
        nose.plugins.multiprocess._instantiate_plugins = [p.__class__ for p in
                                                          self.plugins]
        # PluginTester's setUp() does the actual test run
        super(TestProducesOutput, self).setUp()
        self.xml = ET.parse(self.path)
        self.root = self.xml.getroot()

    def tearDown(self):
        os.remove(self.path)

    def test_stats(self):
        """Stats should be included on the <testsuite> element."""
        self.assertEqual(self.root.attrib['tests'], '4')
        self.assertEqual(self.root.attrib['errors'], '1')
        self.assertEqual(self.root.attrib['failures'], '1')
        self.assertEqual(self.root.attrib['skip'], '1')

    def test_number_of_testcase_elements(self):
        """The number of <testcase> elements should match the number of tests."""
        testcases = self.root.findall('testcase')
        self.assertEqual(len(testcases), 4)

    def test_skip(self):
        """Skipped tests should appear in the output."""
        testcase = self.root.find('./testcase[@classname="support.SkippedTest"]')
        self.assertNotEqual(testcase, None)

    def test_passing(self):
        """Passing tests should appear in the output."""
        testcase = self.root.find('./testcase[@classname="support.PassingTest"]')
        self.assertNotEqual(testcase, None)

    def test_failing(self):
        """Failing tests should appear in the output."""
        testcase = self.root.find('./testcase[@classname="support.FailingTest"]')
        self.assertNotEqual(testcase, None)

    def test_errored(self):
        """Errored tests should appear in the output."""
        testcase = self.root.find('./testcase[@classname="support.ErroringTest"]')
        self.assertNotEqual(testcase, None)

    def test_different_pid(self):
        """Check that the tests ran in a different process.

        We can't force them to all run in different processes, but we can check
        that they've run in a different process to these tests, which should
        be sufficient to catch most errors.
        """
        testcase = self.root.find('./testcase[@classname="support.PassingTest"]')
        systemout = testcase.find('system-out')
        test_pid = systemout.text.replace('pid: ', '').replace('\n', '')
        self.assertNotEqual(str(os.getpid()), test_pid)
