from setuptools import setup, find_packages

classifiers = """\
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Software Development :: Interpreters
Operating System :: Unix
"""

long_description = """\
Overview
---------

**Serval** is a high-level Scheme interpreter written in Python.
It implements a subset of R5RS. The code closely follows
Scheme meta-circular evaluator implementation from Ch.4 of the SICP book.


The goal of the project
------------------------

1. Self-education (I've been always fascinated by language
   design and implementation, it was about time I started learning about
   interpreters and compilers by actually writing something).

2. To serve as a potential example for other people
   interested in interpreter implementation, particularly
   Scheme interpreter.

3. Not a goal per se, but I wanted the **Serval** to be able
   to run all examples from *"The Little Schemer"* book (that was
   my test target). The project has a test module *test_the_little_schemer.py*
   which runs simple meta-circular evaluator from Ch.10 of the book.
"""

setup(
    name='serval',
    version='0.1',
    url='http://github.com/rspivak/serval',
    license='MIT',
    description='Simple Scheme interpreter in Python',
    author='Ruslan Spivak',
    author_email='ruslan.spivak@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['setuptools'],
    zip_safe=False,
    entry_points="""\
    [console_scripts]
    serval = serval.interpreter:main
    """,
    classifiers=filter(None, classifiers.split('\n')),
    long_description=long_description
    )
