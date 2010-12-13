Serval - Simple Scheme interpreter in Python
============================================

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

This is a current high-level overview of the interpreter:

          +----------------+
          |    Scheme      |
          |  source code   |
          |                |
          +-------+--------+
                  |
                  |
                 \|/
          +----------------+
          |  High-Level    |
          |  Interpreter   |
          |                |
          +-------+--------+
                  |
                  |
                 \|/

               Output


Session examples (REPL)
----------------------

1. Defining simple function

        serval> (define add1 (lambda (x) (+ x 1)))
        ok
        serval> (add1 9)
        10

2. Loading representation from a file

        serval> (load "/home/alienoid/scheme/the_little_schemer/ch10.ss")
        serval> (value '((lambda (x) (cons x x)) 5))
        (5 . 5)


Installation
------------

1. Using `buildout` (useful for local development and testing)

        $ cd serval
        $ python bootstrap.py
        $ bin/buildout

        Run the interpreter's REPL

        $ bin/serval

2. Using `pip` or `easy_install` (no need for sudo if using `virtualenv`)

        $ sudo pip install serval

        $ sudo easy_install serval

        Run the interpreter's REPL

        $ serval


Technical details
-----------------

**Serval** has a lexer which uses regular expressions to get a next token
and a recursive-descent parser implementation.

Some code parts are not *idiomatic* Python because I tried to follow SICP
implementation as close as possible for this interpeter.

There is no multiline editing support for the moment. If you need one,
you'd be better off by saving the code into a file and loading it with
`load` builtin function provided by REPL.

Development
-----------

Install 'enscript' utility (optional).
If you are on Ubuntu::

    $ sudo apt-get install enscript

Boostrap the buildout and run it:

    $ cd serval
    $ python bootstrap.py
    $ bin/buildout

Run tests, test coverage and produce coverage reports::

    $ bin/test
    $ bin/coverage-test
    $ bin/coveragereport

    Check ./var/report/serval.html out for coverage results.

Run pep8 and pylint to check code style and search for potential bugs:

    $ bin/pep8
    $ bin/pylint


Roadmap
-------

1. Scheme translator to high-level assembly language
2. Bytecode assembler
3. Register based bytecode interpretator (VM)