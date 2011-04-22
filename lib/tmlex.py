import lex
import sys

reserved = (
    'DATA',
    'SDATA',

    'HALT',

    'IN',
    'OUT',
    'INB',
    'OUTB',
    'OUTC',
    'OUTNL',

    'ADD',
    'SUB',
    'MUL',
    'DIV',

    'LDC',
    'LDA',
    'LD',

    'ST',

    'JLT',
    'JLE',
    'JEQ',
    'JNE',
    'JGE',
    'JGT'
)

tokens = reserved + (
    'LPAREN',
    'RPAREN',
    'COMMA',
    'STRING',
    'INT',
    'STAR',
    'DOT',
    'COLON'
)


reserved_words = { }

for word in reserved:
    reserved_words[word.lower()] = word


# ----------------------------------------
# How to identify tokens
# ----------------------------------------

t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COMMA     = r','
t_STAR      = r'\*'
t_DOT       = r'\.'
t_COLON     = r':'

# ----------------------------------------
# Handle the more complex tokens
# ----------------------------------------

def t_ID(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    if reserved_words.has_key(t.value.lower()):
        t.type = reserved_words[t.value.lower()]
    return t

def t_INT(t):
    r'[-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'("[^"\n]*")|(\'[^\'\n]*\')' # match either double or single quoted string literals
    return t

# ----------------------------------------
# Handle ignored (whitespace) tokens 
# ----------------------------------------
def t_WHITESPACE(t):
    r'[ \t\r\v\f\n]+'
    t.lexer.lineno += t.value.count("\n")

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# I need to check this, because this may be eating too many new lines
# I think it should be okay though
# another worry is that the new lines aren't being counted properly.
# I'll have to test this in my program output
def t_COMMENT(t):
    r'\*[^\n]*\n'
    t.lexer.lineno += t.value.count("\n")


# ----------------------------------------
# Handle Errors
# ----------------------------------------

def t_error(t):
    print "On line %d: " % (t.lineno,) + "",
    if t.value[0] == '"' or t.value[0] == "'":
        print "unterminated string"
    else:
        print "parse error near %s" % t.value
    sys.exit(1)

def test_lex():
    import sys
    prog = sys.stdin.read()
    lex.input(prog)
    while True:
        token = lex.token()
        if not token: break
        print "(%s, '%s', %d)" % (token.type, token.value, token.lineno)

lex.lex()

if __name__ == '__main__':
    test_lex()
