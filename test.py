#!/usr/bin/env python

# INSTRUCTIONS
# ============
#
# This is a test suite for TM optimizers.
#
# This program must be run from the directory where "tests" is. Your optimizer
# will be run like this: (change as necessary)
COMPILER_EXE = './ice9'

# Your optimizer should:
# - Read the input program from standard input.
# - Write the output program to a file; the filename is given in the first
#   argument.

# TEST FILE FORMAT
# ================
#
# Each program in tests/ has comments like this:
#   *:run [17], [1351]
# This means that both the original program and the optimized version should be
# run with input 17; 1351 will be put in memory address 1, possibly overwriting
# a .DATA statement. The two versions should have the same output, and the
# optimized version should finish in fewer instructions.

from subprocess import Popen, PIPE, STDOUT
from json import loads as load_json
import tempfile
import re

class TM(object):
    HALT, IN, INB, OUT, OUTB, OUTC, OUTNL, ADD, SUB, MUL, DIV, LD, ST, LDA, LDC, JLT, JLE, JGT, JGE, JEQ, JNE = range(21)
    opcode_table = {'HALT':HALT, 'IN':IN, 'INB':INB, 'OUT':OUT, 'OUTB':OUTB, 'OUTC':OUTC, 'OUTNL':OUTNL, 'ADD':ADD, 'SUB':SUB, 'MUL':MUL, 'DIV':DIV, 'LD':LD, 'ST':ST, 'LDA':LDA, 'LDC':LDC, 'JLT':JLT, 'JLE':JLE, 'JGT':JGT, 'JGE':JGE, 'JEQ':JEQ, 'JNE':JNE}
    insn_re = re.compile(r'\s*(\d+)\s*:\s*([A-Za-z]+)\s*(\d+)\s*,\s*(-?\d+)\s*[,(]\s*(\d+)')
    def __init__(self, asm):
        self.im = [(self.HALT,0,0,0)]*10000
        self.dm_orig = [0]*10000
        self.dm_orig[0] = len(self.dm_orig) - 1
        di = 1
        for line in asm.split('\n'):
            line = line.strip()
            if line.startswith('*'):
                continue
            elif line.startswith('.SDATA'):
                i = line.index('"') + 1
                j = line.index('"', i)
                self.dm_orig[di:di + j - i] = [ord(c) for c in line[i:j]]
                di += j - i
            elif line.startswith('.DATA'):
                self.dm_orig[di] = int(line[5:].strip().split()[0])
                di += 1
            elif not line:
                continue
            else:
                pos, op, r, s, t = self.insn_re.match(line).groups()
                pos = int(pos)
                r = int(r)
                s = int(s)
                t = int(t)
                op = self.opcode_table[op.upper()]
                self.im[pos] = (op, r, s, t)

    def run(self, inp, dm):
        inp = list(reversed(inp)) # so we can use pop()
        output = ''
        dm = [len(self.dm_orig) - 1] + dm + self.dm_orig[len(dm)+1:]
        R = [0]*8
        steps = 0
        while True:
            o, r, s, t = self.im[R[7]]
            R[7] += 1
            steps += 1
            if o == self.HALT:
                break
            elif o == self.IN:
                R[r] = inp.pop()
            elif o == self.INB:
                assert False
            elif o == self.OUT:
                output += str(R[r]) + ' '
            elif o == self.OUTC:
                output += chr(R[r])
            elif o == self.OUTNL:
                output += '\n'
            elif o == self.ADD:
                R[r] = R[s] + R[t]
            elif o == self.SUB:
                R[r] = R[s] - R[t]
            elif o == self.MUL:
                R[r] = R[s] * R[t]
            elif o == self.DIV:
                x, y = R[s], R[t]
                if y < 0:
                    x, y = -x, -y
                if x < 0:
                    x += y - 1
                R[r] = x // y
            elif o == self.LD:
                a = s + R[t]
                assert a >= 0
                R[r] = dm[a]
            elif o == self.ST:
                a = s + R[t]
                assert a >= 0
                dm[a] = R[r]
            elif o == self.LDA:
                R[r] = s + R[t]
            elif o == self.LDC:
                R[r] = s
            elif o == self.JLT:
                if R[r] < 0:
                    R[7] = s + R[t]
            elif o == self.JLE:
                if R[r] <= 0:
                    R[7] = s + R[t]
            elif o == self.JEQ:
                if R[r] == 0:
                    R[7] = s + R[t]
            elif o == self.JNE:
                if R[r] != 0:
                    R[7] = s + R[t]
            elif o == self.JGE:
                if R[r] >= 0:
                    R[7] = s + R[t]
            elif o == self.JGT:
                if R[r] > 0:
                    R[7] = s + R[t]
            else:
                assert False
        assert not inp
        return output, steps

slower = set()
notfaster = set()

class ICE9Test(object):
    def __init__(self, fn, outfn):
        self.fn = fn
        self.outfn = outfn

    def runTest(self):
        outfn = self.outfn
        with open(self.fn, 'rb') as f:
            compiler = Popen([COMPILER_EXE, outfn], stdin = f, stdout = PIPE, stderr = STDOUT)
            output = compiler.communicate()[0]
            if compiler.returncode == -11: # SIGSEGV
                self.fail('Optimizer segfaulted')
            elif compiler.returncode != 0:
                self.fail('Optimizer terminated with signal %d'%(compiler.returncode))

            f.seek(0)
            origtm = TM(f.read().decode('latin-1'))
            with open(outfn, 'rb') as outf:
                optitm = TM(outf.read().decode('latin-1'))
            f.seek(0)
            for line in f:
                line = line.decode('latin-1')
                if not line.startswith('*:run'):
                    continue
                inp, dm = load_json('['+line[5:].strip()+']')
                origout, origtime = origtm.run(inp, dm)
                optiout, optitime = optitm.run(inp, dm)
                if origout != optiout:
                    print('FAIL: with input ' + str(inp) + ' and data ' + str(dm) + ', original program outputs ' + str(origout) + ' but optimized version outputs ' + str(optiout))
                if optitime > origtime:
                    slower.add((self.fn, tuple(inp), tuple(dm)))
                elif optitime == origtime:
                    notfaster.add((self.fn, tuple(inp), tuple(dm)))

    def __str__(self):
        return self.fn

if __name__ == '__main__':
    import os
    outfn = tempfile.mktemp()
    for fn in sorted(os.listdir('tests')):
        if fn.endswith('.tm') and not fn.startswith('.'):
            print('- ' + fn)
            ICE9Test('tests/'+fn, outfn).runTest()
    print('Same speed after optimization: ')
    for fn, inp, dm in sorted(list(notfaster)):
        fn = fn + ' '*(20-len(fn))
        print('- ' + fn + ' (input ' + str(inp) + ', data ' + str(dm) + ')')
    for fn, inp, dm in slower:
        print('- ' + fn + ' is SLOWER after optimization! (input ' + str(inp) + ', data ' + str(dm) + ')')
