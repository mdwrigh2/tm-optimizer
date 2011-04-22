import yacc
import tmlex

from nodes import *

start = 'program'

memory = [0]

tokens = tmlex.tokens

def p_program(t):
    ''' program : data instrs'''
    print memory
    print t[1]
    print t[2]
    t[0] = [t[1], t[2]]

def p_data(t):
    ''' data : DOT DATA INT data'''
    data_node = Data(t[2], t[3])
    global memory
    memory.append(t[3])
    memory[0] += 1
    t[0] = [data_node] + t[4]

def p_data(t):
    ''' data : DOT SDATA STRING data '''
    data_node = Data(t[2], t[3])
    global memory
    for char in t[3]:
        memory.append(char)
        memory[0] += 1
    t[0] = [data_node] + t[4]

def p_data_empty(t):
    ''' data : empty '''
    t[0] = []

def p_instrs_halt(t):
    ''' instrs : HALT instrs '''
    t[0] = [HaltNode()] + t[2]

def p_instrs_in(t):
    ''' instrs : IN INT instrs '''
    t[0] = [InNode(t[2])] + t[3]

def p_instrs_out(t):
    ''' instrs : OUT INT instrs'''
    t[0] = [OutNode(t[2])] + t[3]
    
def p_instrs_inb(t):
    ''' instrs : INB INT instrs '''
    t[0] = [InBNode(t[2])] + t[3]

def p_instrs_outb(t):
    ''' instrs : OUTB INT instrs'''
    t[0] = [OutBNode(t[2])] + t[3]

def p_instrs_outc(t):
    ''' instrs : OUTC INT instrs'''
    t[0] = [OutCNode(t[2])] + t[3]

def p_instrs_outnl(t):
    ''' instrs : OUTNL instrs '''
    t[0] = [OutNLNode()] + t[2]

def p_instrs_add(t):
    ''' instrs : 
