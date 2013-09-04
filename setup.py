import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'nose'
]


setup(name='nose_xunitmp',
      version='0.2',
      description='Xunit output when running multiprocess tests using nose',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Software Development :: Testing",
      ],
      license='MIT',
      author='Ignas Mikalajunas',
      author_email='ignas@uber.com',
      url='',
      keywords='nosetest xunit multiprocessing',
      py_modules=['nose_xunitmp'],
      include_package_data=True,
      zip_safe=True,
      entry_points="""\
      [nose.plugins.0.10]
      xunitmp = nose_xunitmp:XunitMP
      """,
      install_requires=requires)
