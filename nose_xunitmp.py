"""This plugin provides test results in the standard XUnit XML format."""
import multiprocessing
import codecs

from nose.plugins.base import Plugin
from nose.plugins.xunit import Xunit
from nose.pyversion import force_unicode


class XunitMP(Xunit):
    """This plugin provides test results in the standard XUnit XML format."""

    name = 'xunitmp'
    score = 2000
    error_report_filename = None
    error_report_file = None
    xunit_prefix_class = None

    def options(self, parser, env):
        """Sets additional command line options."""
        Plugin.options(self, parser, env)
        parser.add_option(
            '--xunitmp-file', action='store',
            dest='xunitmp_file', metavar="FILE",
            default=env.get('NOSE_XUNITMP_FILE', 'nosetests.xml'),
            help=("Path to xml file to store the xunit report in. "
                  "Default is nosetests.xml in the working directory "
                  "[NOSE_XUNIT_FILE]"))

    def configure(self, options, config):
        """Configures the xunit plugin."""
        Plugin.configure(self, options, config)
        self.config = config
        if self.enabled:
            # Each subprocess gets a new instance of this plugin. We need to be
            # sure that each of these instances shares the same errorlist/stats
            # Placing them on self.config achieves this, as nose pickles it and
            # passes it to each subprocess.
            # Doing it here (rather than at the module level) means that they
            # will be shared on Windows too.
            if not hasattr(self.config, '_nose_xunitmp_state'):
                manager = multiprocessing.Manager()
                self.errorlist = manager.list()
                self.stats = manager.dict(**{
                    'errors': 0,
                    'failures': 0,
                    'passes': 0,
                    'skipped': 0
                })
                self.config._nose_xunitmp_state = self.errorlist, self.stats
            else:
                self.errorlist, self.stats = self.config._nose_xunitmp_state
            self.error_report_filename = options.xunitmp_file

    def report(self, stream):
        """Writes an Xunit-formatted XML file

        The file includes a report of test errors and failures.

        """
        self.error_report_file = codecs.open(self.error_report_filename, 'w',
                                             self.encoding, 'replace')
        self.stats['encoding'] = self.encoding
        self.stats['total'] = (self.stats['errors'] + self.stats['failures']
                               + self.stats['passes'] + self.stats['skipped'])
        self.error_report_file.write(
            u'<?xml version="1.0" encoding="%(encoding)s"?>'
            u'<testsuite name="nosetests" tests="%(total)d" '
            u'errors="%(errors)d" failures="%(failures)d" '
            u'skip="%(skipped)d">' % self.stats)
        self.error_report_file.write(u''.join([
            force_unicode(error)
            for error
            in self.errorlist
        ]))

        self.error_report_file.write(u'</testsuite>')
        self.error_report_file.close()
        if self.config.verbosity > 1:
            stream.writeln("-" * 70)
            stream.writeln("XML: %s" % self.error_report_file.name)
