#!Python

import sys
#Hack para la ultima version de ply(no funciona con jython)
if 'java' in sys.platform:
    import lex
else:
    from ply import lex

# List of token names.   This is always required
tokens = (
   'INSERTOREQ',
   'EXTRACTOREQ',
   'AMPERSANDEQ',
   'LPAREN',
   'RPAREN',
   'RBRACK',
   'LBRACK',
   'LCURLY',
   'RCURLY',
   'COLON',
   'TIMES',
   'PLUS',
   'MINUS',
   'STRING',
   'COMMA',
   'DIV',
   'EQ',
   'EQUAL',
   'BO',
   'GE',
   'GT',
   'LE',
   'LT',
   'NE',
   'NOT',
   'AND',
   'OR',
   'EXP',
   'SEMI',
   'INCR',
   'NUMBER',
   'ID',
   'IN',
   'WITH',
   'SETVAR',
   'IMPORTS',
   'DOT',
   'FUNCTION',
   'RETURN',
   'YIELD',
   'IF',
   'THEN',
   'ELSE',
   'COND',
   'CASE',
   'WHILE',
   'FOR',
   'FOREACH',
   'DO',
   'REPEAT',
   'UNTIL',
   'END',
   'AS',
   'QUESTION',
   'NULL',
   'PIPE',
   'FILTER',
   'BY',
   'NEW',
   'ARROW',
   'MAP',
   'REDUCE',
   'CREATE',
   'FILES',
   'DIRS',
   'WORDS',
   'TO',
   'BINARY',
   'FROM',
   'UPDATE',
   'CUT',
   'MATCH',
   'NATIVE',
   'XML',
   'PROLOG',
   'CONSULT',
   'DATABASE',
   'SELECT',
   'COPY',
   'DEL',
   'WEBSERVER',
   'WEBGET',
   'WEBPOST',
   'GLOBAL',
   'RESPONSE',
   'BREAK',
   'CONTINUE',
   'OBJECT',
   'TRY',
   'CATCH',
   'FINALLY',
   'RAISE',
   'ASSERT',
   'RUN',
   'GROUPBY',
   'ORDER',
   'LIKE',
   'BETWEEN',
   'COUNT',
   'CONTAINS',
   'ASC',
   'DESC',
   'WHERE',
   'LINES',
   'FORMAT',
   'REVERSE',
   'CLASS',
   'EXTENDS',
   'THIS',
   'PUBLIC',
   'PRIVATE',
   'STATIC',
   'TYPEDEF',
   'IS',
   'ARRAY',
   'NUMERIC',
   'CHAIN',
   'INSERTOR',
   'HTML',
   'SERIALIZE',
   'DESERIALIZE',
   'BEGIN',
   'ENDSEC',
   'ADD',
   'ENVIRON',
   'LET',
   #'NEXT',
   'LAZY',
   'PUT',
   'MACRO',
   'MACROID',
   'ARROBA',
   'AMPERSAND',
   'TRUE',
   'FALSE',
   'COMMENT',
   'CODEID',
   'TAKE',
   'OPERATOR',
   'THREAD',
   'JOIN',
   'ASYNC',
   'AWAIT',
   'GENERIC',
   'GET',
   'STRUCT',
   'INTERFACE',
   'SETFLAG',
   'UNSETFLAG',
   'ONFLAG',
   'ENUM',
   'DEFINE',
   'SETCVAR',
   'CFUNCTION',
   'CTYPEDEF',
   'EXTERN',
   'APPLY',
   'PTR',
   'DOTDOT',
   'EXTRACTOR',
   'PLUSEQ',
   'MINUSEQ',
   'TIMESEQ',
   'DIVEQ',
   'PTREQ',
   'DESTR',
   'IMPLEMENTS')



# Regular expression rules for simple tokens-------------
t_INCR=r'\+\+|--'
t_EXP=r'\*\*'
t_INSERTOREQ=r'<<='
t_EXTRACTOREQ=r'>>='
t_AMPERSANDEQ=r'&='
t_PTREQ=r'\^='
t_INSERTOR=r'<<'
t_EXTRACTOR=r'>>'
t_PLUSEQ=r'\+='
t_MINUSEQ=r'-='
t_TIMESEQ=r'\*='
t_DIVEQ=r'/='
t_DESTR=r'~'
#-----------------------
t_ARROW=r'->'
t_LPAREN=r'\('
t_RPAREN=r'\)'
t_LBRACK=r'\['
t_RBRACK=r'\]'
t_LCURLY=r'\{'
t_RCURLY=r'\}'
t_TIMES=r'\*'
t_PLUS=r'\+'
t_MINUS=r'-'
t_EQ=r'=='
t_COMMA=r','
t_DIV=r'/'
t_GE=r'>='
t_LE=r'<='
t_NE=r'!='
t_BO=r'<>'
t_GT=r'>'
t_EQUAL=r'='
t_LT=r'<'
t_SEMI=r';'
t_DOTDOT=r'\.\.'
t_DOT=r'\.'
t_QUESTION=r'\?'
t_PIPE=r'\|'
#t_COLON=r':'
t_AMPERSAND=r'\&'
t_PTR=r'\^'
#-------------------------------------------------------


reserved={
    'in':'IN',
    'with' : 'WITH',
    'setvar' : 'SETVAR',
    'imports' : 'IMPORTS',
    'function' : 'FUNCTION',
    'return' : 'RETURN',
    'yield' : 'YIELD',
    'if' : 'IF',
    'cond' : 'COND',
    'case' : 'CASE',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'foreach' : 'FOREACH',
    'for' : 'FOR',
    'do' : 'DO',
    'repeat' : 'REPEAT',
    'until' : 'UNTIL',
    'end' :  'END',
    'as' : 'AS',
    'not' : 'NOT',
    'and' : 'AND',
    'or' : 'OR',
    'filter' : 'FILTER',
    'by' : 'BY',
    'new' : 'NEW',
    'reduce' : 'REDUCE',
    'map' : 'MAP',
    'create' : 'CREATE',
    'files' : 'FILES',
    'dirs' : 'DIRS',
    'words' : 'WORDS',
    'to' : 'TO',
    'binary' : 'BINARY',
    'from' : 'FROM',
    'update' : 'UPDATE',
    'cut' : 'CUT',
    'match' : 'MATCH',
    'native' : 'NATIVE',
    'xml' : 'XML',
    'prolog' : 'PROLOG',
    'consult' : 'CONSULT',
    'database' : 'DATABASE',
    'select' : 'SELECT',
    'copy' : 'COPY',
    'del' : 'DEL',
    'webserver' : 'WEBSERVER',
    'webget' : 'WEBGET',
    'webpost' : 'WEBPOST',
    'global' : 'GLOBAL',
    'response' : 'RESPONSE',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'object' : 'OBJECT',
    'try' : 'TRY',
    'catch' : 'CATCH',
    'finally' : 'FINALLY',
    'raise' : 'RAISE',
    'assert' : 'ASSERT',
    'run' : 'RUN',
    'groupby' : 'GROUPBY',
    'order' : 'ORDER',
    'like' : 'LIKE',
    'between' : 'BETWEEN',
    'count' :'COUNT',
    'contains' : 'CONTAINS',
    'asc' : 'ASC',
    'desc' : 'DESC',
    'where' : 'WHERE',
    'lines' :'LINES',
    'format' : 'FORMAT',
    'reverse' : 'REVERSE',
    'class' : 'CLASS',
    'extends' : 'EXTENDS',
    'this' : 'THIS',
    'public' : 'PUBLIC',
    'private' :'PRIVATE',
    'static' : 'STATIC',
    'typedef' : 'TYPEDEF',
    'is' : 'IS',
    'array' : 'ARRAY',
    'numeric' : 'NUMERIC',
    'chain' : 'CHAIN',
    'html' : 'HTML',
    'serialize' : 'SERIALIZE',
    'deserialize' :'DESERIALIZE',
    'begin' : 'BEGIN',
    'endsec' : 'ENDSEC',
    'add' : 'ADD',    
    'environ' : 'ENVIRON',
    'let' : 'LET',
    #'next' : 'NEXT',
    'lazy' : 'LAZY',   
    'put' : 'PUT',
    'take' : 'TAKE',
    'macro' : 'MACRO',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'operator' : 'OPERATOR',
    'thread' : 'THREAD',
    'join' : 'JOIN',
    'async' : 'ASYNC',
    'await' : 'AWAIT',
    'generic' : 'GENERIC',
    'get' : 'GET',
    'struct' : 'STRUCT',
    'interface' : 'INTERFACE',
    'setflag' : 'SETFLAG',
    'unsetflag' : 'UNSETFLAG',
    'onflag' : 'ONFLAG',
    'enum' : 'ENUM',
    'define' : 'DEFINE',
    'setcvar' : 'SETCVAR',
    'cfunction' : 'CFUNCTION',
    'ctypedef' : 'CTYPEDEF',
    'extern' : 'EXTERN',
    'apply' : 'APPLY',
	'implements' : 'IMPLEMENTS'}


def t_STRING(t):
    r"[@|r|u]?\"\"\"[\s\S]*?\"\"\"|[@|r|u]?\"[^\"\\]*(?:\\.[^\"\\]*)*\""
    #r"(?:\'[^\'\\]*(?:\\.[^\'\\]*)*\') | (?:&[^/\\]*(?:\\.[^/'\\]*)*&)"
    #t.value=t.value.strip("'").strip("'") #Da problemas para distinguir en p_factor variables, objetos y strings!!!!
    #t.value=t.value.replace('\\',r'\\')
    #t.value=t.value.replace('\\n','\n') ##raw or not raw???
    #t.value=t.value.replace('\\r','\r')
    #t.value=t.value.replace('\\t','\t')
    return t
###-------------------------------------------------------------------------------------


#def t_ID(t): 
#    r'[a-zA-Z_][a-zA-Z_0-9]*|%[a-zA-Z_][a-zA-Z_0-9]*%' #Cambio para permitir palabras clave como id
   # t.type = reserved.get(t.value,'ID')    # Check for reserved words
   # return t
  


#cambio para permtir que los id se puedan sustituir por codigo en las macros???
def t_ID(t): 
    r'[a-zA-Z_][a-zA-Z_0-9]*|%[a-zA-Z_][a-zA-Z_0-9]*%|:[a-zA-Z_][a-zA-Z_0-9]*:' #Cambio para permitir palabras clave como id
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

t_COLON=r':' #Tiene que estar aqui para que se pruebe primero ID

def t_MACROID(t): 
    r'\$[a-zA-Z_][a-zA-Z_0-9]*'
    return t


def t_CODEID(t): 
    r'\@[a-zA-Z_][a-zA-Z_0-9]*'
    return t

t_ARROBA=r'@'

#Cambio gordo para que funcione el uminus.
#Los numeros se leen SIN signo
#def t_NUMBER(t):
#    r'[0-9]+[\.]?[0-9]*|0[\.][0-9]+e[\+|\-][0-9]+'
#    return t
def t_NUMBER(t):
    #r'[0-9]+[\.]?[0-9]*'
    r'0[bB][0-1]+|0[xX][0-9a-fA-F]+|[0-9]+L|[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
    return t

# Define a rule so we can track line numbers
def t_newline(t): #(Para win32 y Mac)
    r'(\r|\n)|\n'
    t.lexer.lineno += 1#len(t.value)
    #print 'AVANCE DE LINEA!!!!'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

#Esta regla da problemas con los \r!!!!!!!!!!
def t_COMMENT(t):
    r'\#[^\n]*[\n]?|\#[^\r\n]*[\r\n]|/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    t.lexer.lineno += 1
    #print 'Pillado comentario!!: %s'%t.value
    #No hay que devolver nada para que se ignore el token

# Error handling rule
def t_error(t):
    print "Caracter no permitido: '%s->%s'" % (t,repr(t.value[0]))
    raise Exception("Error del lexer")

# Build the lexer
lexer=lex.lex()


if __name__=='__main__':
    #print open('test_code/py_test1.txt').read()
    #tks=lexer.input(open('M/musica.txt').read())
    #tks=lexer.input(open(sys.argv[1]).read())
    #tks=lexer.input(open('test_code/grep.txt').read())#'a=grep("#.*",["./test_code/test48.txt","./test_code/test49.txt","./test_code/test50.txt","./test_code/test51.txt"]);')
    #tks=lexer.input('map |(x): _print(x)| in a;')
    # tks=lexer.input('234; 23e-5 ; -56E-128; 0.000007896; 0x0')
    # tks=lexer.input('''@(begin
      # function :template:():
          # _print("Hola");
          # :morecode:;
      # end
  # endsec;) as @codetemplate;);|(x):x|;''')
    tks=lexer.input('234; 23e-5 ; -56E-128; 0.000007896; 0x0; 0b1010101011110001; u"tralari";r"""bububtre""";@"fin del mundo";"tres";"""cuatro"""')
    while True:
         t=lexer.token()
         if not t: break
         print t
    