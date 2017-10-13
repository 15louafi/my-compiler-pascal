#!/usr/bin/env python
#
# $Id: mach.py 504 2017-09-22 08:25:09Z coelho $
#
# python version of a little stack machine
# because python ints are big ints, the machine uses big ints.

from __future__ import print_function

import sys
import re

# all available instructions
ONEARG = 'BGZ|BEZ|PUSH'
NOARG = 'LOAD|STORE|SWAP|ADD|SUB|MUL|DIV|AND|OR|NOT|STOP|GOTO|IN|OUT'

onearg = re.compile('^(' + ONEARG + ')$')
noarg = re.compile('^(' + NOARG + ')$')
integer = re.compile('^-?\d+$')
split = re.compile('[ \n\t\r]+')
empty = re.compile('^[ \t\r]+\n$')

# build instruction translation
i2n = {}
n2i = []
ni = 0
for ins in re.split('\|', ONEARG + '|' + NOARG):
    i2n[ins] = ni
    n2i.append(ins)
    ni += 1

program = []


class Machine:
    def __init__(self, program):
        self.program = program
        self.pc, self.data, self.stack = 0, [], []
        self.check_code()

    def check_code(self):
        # get and check code
        nline = 0
        for line in open(sys.argv[1], 'r').readlines():
            nline += 1
            if empty.match(line):
                continue
            cmds = split.split(line.upper().lstrip(' \t').rstrip(' \n\t\r'))
            # check command & argument
            if len(cmds) == 0 or (len(cmds) == 1 and cmds[0] == ''):
                continue
            elif onearg.match(cmds[0]):
                assert len(cmds) == 2
                if not integer.match(cmds[1]):
                    self.err('expecting integer, got %s on line %d' %
                             (cmds[1], nline))
            elif noarg.match(cmds[0]):
                assert len(cmds) == 1
            else:
                self.err('unexpected command %s on line %d' % (cmds[0], nline))
            # store program as binary instructions
            program.append(i2n[cmds[0]])
            if len(cmds) == 2:
                program.append(int(cmds[1]))

    def err(self, msg):
        # status on error
        print('program length %d, pc=%d' %
              (len(self.program), self.pc), file=sys.stderr)
        print('stack length %d' % len(self.stack), file=sys.stderr)
        print('data length %d' % len(self.data), file=sys.stderr)
        # message & exit
        sys.stderr.write(msg + '\n')
        sys.exit(1)

    # all instructions as methods
    def stop(self):
        print('program length %d, pc=%d' % (len(self.program), self.pc))
        print('stack length %d' % len(self.stack))
        print('data length %d' % len(self.data))
        sys.exit(0)

    def push(self):
        self.stack.append(self.program[self.pc])
        self.pc += 1

    def swap(self):
        stack = self.stack
        stack[-2], stack[-1] = stack[-1], stack[-2]

    def store(self):
        val, adr = self.stack.pop(), self.stack.pop()
        if adr < 0 or adr > 1000000:
            self.err('unexpected STORE data address: %d', adr)
        if adr >= len(self.data):  # expand memory?
            self.data += [0] * (adr - len(self.data) + 1)
        assert adr < len(self.data)
        self.data[adr] = val

    def load(self):
        adr = self.stack.pop()
        if adr < 0 or adr > 1000000:
            self.err('unexpected LOAD data address: %d', adr)
        if adr < len(self.data):
            self.stack.append(self.data[adr])
        else:
            # set zero if out of bound...
            sys.stderr.write('out of bounds memory load: data[%d]\n' % adr)
            self.stack.append(0)

    def add(self):
        stack = self.stack
        stack.append(stack.pop() + stack.pop())

    def mul(self):
        stack = self.stack
        stack.append(stack.pop() * stack.pop())

    def _and(self):
        stack = self.stack
        stack.append(stack.pop() & stack.pop())

    def _or(self):
        stack = self.stack
        stack.append(stack.pop() | stack.pop())

    def sub(self):
        stack = self.stack
        i, j = stack.pop(), stack.pop()
        stack.append(j - i)

    def div(self):
        stack = self.stack
        i, j = stack.pop(), stack.pop()
        stack.append(j // i)

    def _not(self):
        stack = self.stack
        # binary inversion, not logical!
        stack.append(~stack.pop())

    def out(self):
        print('output: %d' % self.stack.pop())

    def _in(self):
        sys.stdout.write('input: ')
        sys.stdout.flush()
        self.stack.append(int(sys.stdin.readline()))

    def goto(self):
        self.pc = self.stack.pop()

    def bgz(self):
        self.pc = self.program[
            self.pc] if self.stack.pop() > 0 else self.pc + 1

    def bez(self):
        self.pc = self.program[
            self.pc] if self.stack.pop() == 0 else self.pc + 1

    EXEC = {
        'STOP': stop,
        'PUSH': push,
        'SWAP': swap,
        'STORE': store,
        'LOAD': load,
        'ADD': add,
        'SUB': sub,
        'MUL': mul,
        'DIV': div,
        'AND': _and,
        'OR': _or,
        'NOT': _not,
        'OUT': out,
        'IN': _in,
        'GOTO': goto,
        'BGZ': bgz,
        'BEZ': bez
    }

    def run(self):
        while True:
            # sandboxing:-)
            if self.pc >= len(self.program) or self.pc < 0:
                self.err('pc is out of program: %d' % self.pc)
            cur = n2i[self.program[self.pc]]
            self.pc += 1
            assert cur in self.EXEC, "invalid instruction %s" % cur
            self.EXEC[cur](self)


Machine(program).run()
