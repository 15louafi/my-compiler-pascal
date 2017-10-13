#!/usr/bin/env python
#
# $Id: asm.py 488 2014-10-08 14:08:07Z coelho $
#
# Code by 08servai, p08 rocks!
# C'etait mieux avant...
#
# Code published under GNU-GPL v3+
#

from __future__ import print_function

import sys
import re

# error messages and counting
errors = 0


def err(msg):
    print('## asm.py Error: ' + msg, file=sys.stderr)
    global errors
    errors += 1


# read all input
lines = sys.stdin.readlines()

# define re for names
IDENT = '[_@%a-zA-Z][_@%a-zA-Z0-9:]*'
something = re.compile(r'.*\w')
comment_re = re.compile(r'\s*;/')
label_re = re.compile('^' + IDENT + '\s+EQU')
var_re = re.compile('^' + IDENT + '\s+DS\s+\d+')

# define re for commands
push = re.compile(r'\s+PUSH\s+' + IDENT + '\s*')
pushInt = re.compile(r'\s+PUSH\s+\d*\s*')
begz = re.compile(r'\s+B[EG]Z\s+' + IDENT + '\s*')
command = re.compile(
    r'BGZ|BEZ|PUSH|LOAD|STORE|SWAP|ADD|SUB|MUL|DIV|AND|OR|NOT|STOP|GOTO|IN|OUT'
)
commandArg = re.compile(r'BGZ|BEZ|PUSH')

# constant or identifier
Arg = re.compile('^(\d+|' + IDENT + ')$')

# already defined names
dico = {}
# current line and memory extension...
line = 0
mem = 0

ln = 0
for l in lines:
    ln += 1
    if something.match(l) and not comment_re.match(l):
        l = l.split(';/')[0]  # drop inline comments
        tokens = l.split(None)
        if label_re.match(l):
            label = tokens[0]
            if label in dico:
                err('Duplicate key label %s at line %d' % (label, ln))
            else:
                dico[label] = line
        elif var_re.match(l):  # XXX DS 123
            var, size = tokens[0], tokens[2]
            if var in dico:
                err('Duplicate key var %s at line %d' % (var, ln))
            else:
                dico[var] = mem
                mem += int(size)
        elif command.match(tokens[0]):
            cmd = tokens[0]
            if commandArg.match(cmd):
                if len(tokens) < 2:
                    err('Missing %s argument at line %d' % (cmd, ln))
                elif not Arg.match(tokens[1]):
                    err('Bad argument for %s at line %d: %s' % (cmd, ln,
                                                                tokens[1]))
            elif len(tokens) > 1:
                err('Command %s does not except arguments (%s) at line %d' %
                    (cmd, tokens[1], ln))
            line += len(l.split(None))
        else:
            err('Unknown command "%s" at line %d' % (tokens[0], ln))

ln = 0
for l in lines:
    ln += 1
    l = l.split(';/')[0].strip('\n')
    tokens = l.split(None)
    if push.match(l):
        try:
            print('\tPUSH\t%s' % dico[tokens[1]])
        except KeyError:
            err('Undefined key %s at line %d' % (tokens[1], ln))
    elif pushInt.match(l):
        print('\tPUSH\t%s' % tokens[1])
    elif begz.match(l):
        try:
            print('\t%s\t%s' % (tokens[0], dico[tokens[1]]))
        except KeyError:
            err('Undefined key %s at line %d' % (tokens[1], ln))
    elif (something.match(l)
          and not (var_re.match(l)
                   or label_re.match(l)
                   or comment_re.match(l))):
        print(l)

if errors:  # show final error count
    err('%d errors' % errors)
    sys.exit(1)
