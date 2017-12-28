#!Python

import sys
#Hack para la ultima version de ply(no funciona con jython)
if 'java' in sys.platform:
    import lex
else:
    from ply import lex

# List of token names.   This is always required
tokens = (
   'END',
   'STACK',
   'WINDOW',
   'FORM',
   'FOR',
   'WITH',
   'BIND',
   'TO',
   'FRAME',
   'PANEL',
   'BUTTON',
   'LABEL',
   'TEXTBOX',
   'TEXTAREA',
   'COMBOBOX',
   'LISTBOX',
   'TABLEBOX',
   'TREEBOX',
   'CHECKBOX',
   'NUMBER',
   'STRING',
   'ID',
   'COMMA',
   'SEMI',
   'COLON',
   'EQUAL',
   'COMMENT',
   'VERBATIM',
   'MENU',
   'TOPLEVEL',
   'VIEW',
   'CONTROLLER',
   'FONT',
   'IMPORT',
   'INCLUDE',
   'INIT',
   'DOT',
   'PIPE',
   'PLUS',
   'AID',
   'NOTHING',
   'LBRACK',
   'RBRACK',
   'USER',
   'MENUITEM',
   'TOPMENU',
   'KEY',
   'RADIO',
   'BRIDGE',
   'NOTEBOOK')



# Regular expression rules for simple tokens-------------
t_COMMA=r','
t_EQUAL=r'='
t_COLON=r':'
t_SEMI=r';'
t_DOT=r'.'
t_PIPE=r'\|'
t_PLUS=r'\+'
t_LBRACK=r'\['
t_RBRACK=r'\]'
#-------------------------------------------------------


reserved={
   'end' : 'END',
   'stack' : 'STACK',
   'window' : 'WINDOW',
   'form' : 'FORM',
   'for' : 'FOR',
   'with' : 'WITH',
   'bind' : 'BIND',
   'to' : 'TO',
   'frame' : 'FRAME',
   'panel' : 'PANEL',
   'button' : 'BUTTON',
   'label': 'LABEL',
   'textbox' : 'TEXTBOX',
   'textarea' : 'TEXTAREA',
   'combobox' : 'COMBOBOX',
   'listbox' : 'LISTBOX',
   'tablebox' : 'TABLEBOX',
   'treebox' : 'TREEBOX',
   'checkbox' : 'CHECKBOX',
   'menu' : 'MENU',
   'toplevel' : 'TOPLEVEL',
   'view' : 'VIEW',
   'controller' : 'CONTROLLER',
   'font' : 'FONT',
   'import' : 'IMPORT',
   'include' : 'INCLUDE',
   'init' : 'INIT',
   'nothing' : 'NOTHING',
   'user' : 'USER',
   'menuitem' : 'MENUITEM',
   'topmenu' : 'TOPMENU',
   'radio' : 'RADIO',
   'bridge' : 'BRIDGE',
   'notebook' : 'NOTEBOOK'
    }


def t_STRING(t):
    # "[^"\\]*(?:\\.[^"\\]*)*"
    r"\"\"\"[\s\S]*?\"\"\"|\"[^\"\\]*(?:\\.[^\"\\]*)*\"|\'[^\'\\]*(?:\\.[^\'\\]*)*\'"
    return t
###-------------------------------------------------------------------------------------

def t_VERBATIM(t):
    r"\{\{[\s\S]*?\}\}"
    return t

def t_ID(t): 
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_KEY(t): #Tiene que ir ANTES de AID o si no encuentra un AID!!!
    r'@[a-zA-Z_][a-zA-Z_0-9]*@'
    return t

def t_AID(t): 
    r'@[a-zA-Z_][a-zA-Z_0-9]*'
    #t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'[-]*[0-9]+[\.]?[0-9]*'
    return t


# Define a rule so we can track line numbers
def t_newline(t): #(Para win32 y Mac)
    r'(\r\n)+|\n+'
    t.lexer.lineno += len(t.value)
    #print 'AVANCE DE LINEA!!!!'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_COMMENT(t):
    r'\#[^\n]*[\n]?|\#[^\r\n]*[\r\n]|/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    t.lexer.lineno += 1

# Error handling rule
def t_error(t):
    print "Caracter no permitido: '%s->%s'" % (t,repr(t.value[0]))
    raise Exception("Error del lexer")

# Build the lexer
guilexer=lex.lex()


if __name__=='__main__':
   tks=guilexer.input("""\"\"\"<h2>Texto en <font color="red">HTML</b></h2>\"\"\"""")
   while True:
        t=guilexer.token()
        if not t: break
        print t
    
