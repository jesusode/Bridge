################ Scheme Interpreter in Python

## (c) Peter Norvig, 2010; See http://norvig.com/lispy2.html

################ Symbol, Procedure, classes

from __future__ import division
import re, sys, StringIO
import math, cmath, operator as op
import random


HAVE_SQLITE=0

#Cambio para version independiente-----------------------------
if not 'java' in sys.platform:
    import sqlite3
    HAVE_SQLITE=1
    #print 'importando sqlite'
#--------------------------------------------------------------

#Recuperar el eval de python
pyeval=eval

#Prompt
PROMPT='Minimal Scheme> '

class Symbol(str): pass

def Sym(s, symbol_table={}):
    "Find or create unique Symbol entry for str s in symbol table."
    if s not in symbol_table: symbol_table[s] = Symbol(s)
    return symbol_table[s]


def _gensym():
    return Symbol('G'+str(random.random()*100000))
    #return Symbol(x)

_quote, _if, _set, _define, _lambda, _begin, _definemacro, _cond, = map(Sym, "quote   if   set!  define   lambda   begin   define-macro cond".split())

_quasiquote, _unquote, _unquotesplicing = map(Sym,"quasiquote   unquote   unquote-splicing".split())

class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, exp, env):
        self.parms, self.exp, self.env = parms, exp, env
    def __call__(self, *args): 
        return eval(self.exp, Env(self.parms, args, self.env))

################ parse, read, and user interaction

def parse(inport):
    "Parse a program: read and expand/error-check it."
    # Backwards compatibility: given a str, convert it to an InPort
    if isinstance(inport, str): inport = InPort(StringIO.StringIO(inport))
    return expand(read(inport), toplevel=True)

eof_object = Symbol('#<eof-object>') # Note: uninterned; can't be read

class InPort(object):
    "An input port. Retains a line of chars."
    tokenizer = r"""\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)"""
    def __init__(self, file):
        self.file = file; self.line = ''
    def next_token(self):
        "Return the next token, reading new text into line buffer if needed."
        while True:
            if self.line == '': self.line = self.file.readline()
            if self.line == '': return eof_object
            token, self.line = re.match(InPort.tokenizer, self.line).groups()
            if token != '' and not token.startswith(';'):
                return token

def readchar(inport):
    "Read the next character from an input port."
    if inport.line != '':
        ch, inport.line = inport.line[0], inport.line[1:]
        return ch
    else:
        return inport.file.read(1) or eof_object

def read(inport):
    "Read a Scheme expression from an input port."
    def read_ahead(token):
        if '(' == token: 
            L = []
            while True:
                token = inport.next_token()
                if token == ')': return L
                else: L.append(read_ahead(token))
        elif ')' == token: raise SyntaxError('unexpected )')
        elif token in quotes: return [quotes[token], read(inport)]
        elif token is eof_object: raise SyntaxError('unexpected EOF in list')
        else: return atom(token)
    # body of read:
    token1 = inport.next_token()
    return eof_object if token1 is eof_object else read_ahead(token1)

quotes = {"'":_quote, "`":_quasiquote, ",":_unquote, ",@":_unquotesplicing}

def atom(token):
    'Numbers become numbers; #t and #f are booleans; "..." string; otherwise Symbol.'
    if token == '#t': return True
    elif token == '#f': return False
    elif token[0] == '"': return token[1:-1].decode('string_escape')
    #------------------------------------------------------------------------
    #Trampa para permitir variables mini: Empiezan con "!". Ej: !minivarname
    #elif token[0]=='!':return SYMTAB['@' + token[1:]]
    #Fin cambio para variables mini
    #------------------------------------------------------------------------
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            try: return complex(token.replace('i', 'j', 1))
            except ValueError:
                return Sym(token)

def to_string(x):
    "Convert a Python object back into a Lisp-readable string."
    if x is True: return "#t"
    elif x is False: return "#f"
    elif isa(x, Symbol): return x
    elif isa(x, str): return '"%s"' % x.encode('string_escape').replace('"',r'\"')
    elif isa(x, list): return '('+' '.join(map(to_string, x))+')'
    elif isa(x, complex): return str(x).replace('j', 'i')
    else: return str(x)

def load(filename):
    "Eval every expression from a file."
    repl(None, InPort(open(filename)), None)


def repl(prompt=PROMPT, inport=InPort(sys.stdin), out=sys.stdout):
    "A prompt-read-eval-print loop."
    #sys.stderr.write("Lispy version 2.0\n")
    while True:
        try:
            if prompt: sys.stderr.write(prompt)
            x = parse(inport)
            if x is eof_object: return
            val = eval(x)
            if val is not None and out: print >> out, to_string(val)
        except Exception,e:
            print '%s: %s' % (type(e).__name__, e)

################ Environment class

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        # Bind parm list to corresponding args, or single parm to list of args
        self.outer = outer
        if isa(parms, Symbol): 
            self.update({parms:list(args)})
        else: 
            if len(args) != len(parms):
                raise TypeError('expected %s, given %s, ' 
                                % (to_string(parms), to_string(args)))
            self.update(zip(parms,args))
    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self: return self
        elif self.outer is None: raise LookupError(var)
        else: return self.outer.find(var)

def is_pair(x): return x != [] and isa(x, list)
def cons(x, y): return [x]+y

def callcc(proc):
    "Call proc with current continuation; escape only"
    ball = RuntimeWarning("Sorry, can't continue this continuation any longer.")
    def throw(retval): ball.retval = retval; raise ball
    try:
        return proc(throw)
    except RuntimeWarning(w):
        if w is ball: return ball.retval
        else: raise w



def python(string):
    exec string
    return 1

def evalpython(string):
    return pyeval(string)

def callPythonFunc(fname,arglist):
    f=pyeval(fname)
    return f(*arglist)

def _sort(l):
    l.sort()
    return l

def _reverse(l):
    l.reverse()
    return l

def setcar(l,c):
    l[0]=c
    return True

def setcdr(l,c):
    l[1:]=c
    return True

def stringtolist(cad):
    return list(cad)

def stringappend(cad,strl):
    buff=StringIO.StringIO()
    buff.write(cad)
    for el in strl:
        buff.write(el)
    return buff.getvalue()

def newline():
    print

def pymap(f,l):
    ret=map(f,l)
    #cambiar None por False
    for i in range(len(ret)):
        if ret[i]==None:
            ret[1]=False
    return ret

def pyforeach(f,l):
    map(f,l)
    return []
    

def opensqlite(bd):
    if HAVE_SQLITE==0: raise Exception('Error: El manejo de bases de datos SQLite no esta disponible en plataformas Java')
    conn=sqlite3.connect(bd.strip('"'), isolation_level=None)
    return conn

def consultsqlite(bdconn,query,args):
    if HAVE_SQLITE==0: raise Exception('Error: El manejo de bases de datos SQLite no esta disponible en plataformas Java')    
    cursor=bdconn.cursor()
    query=query.strip('"')
    res=cursor.execute(query,args)
    data=[]
    if res:
      data=cursor.fetchall()
    data=[list(el) for el in data]
    bdconn.commit()
    cursor.close()
    #Asegurarse de que las cadenas van delimitadas por "
    for el in data:
        for i in range(len(el)):
            if type(el[i]) in [type(''),type(u'')]:
                el[i]='"' + el[i] + '"'
    return data

##-----------------------------------------------------------------------------------
def add_globals(self):
    "Add some Scheme standard procedures."
    #import math, cmath, operator as op
    self.update(vars(math))
    self.update(vars(cmath))
    self.update({
     '+':op.add,
     '-':op.sub,
     '*':op.mul,
     '/':op.div,
     'not':op.not_, 
     '>':op.gt,
     '<':op.lt,
     '>=':op.ge,
     '<=':op.le,
     '=':op.eq, 
     'equal?':op.eq,
     'eq?':op.is_,
     'length':len,
     'cons':cons,
     'car':lambda x:x[0],
     'cdr':lambda x:x[1:],
     'append':op.add,
     'list':lambda *x:list(x),
     'list?': lambda x:isa(x,list),
     #'null?':lambda x:x==[],
     'null?':lambda x:x in [False,[]],     
     'symbol?':lambda x: isa(x, Symbol),
     'boolean?':lambda x: isa(x, bool),
     'pair?':is_pair, 
     'port?': lambda x:isa(x,file),
     'apply':lambda proc,l: proc(*l),
     'map':pymap,
     'for-each': pyforeach,
     'eval':lambda x: eval(expand(x)),
     'load':lambda fn: load(fn),
     'call/cc':callcc,
     'open-input-file':open,
     'close-input-port':lambda p: p.file.close(), 
     'open-output-file':lambda f:open(f,'w'),
     'close-output-port':lambda p: p.close(),
     'eof-object?':lambda x:x is eof_object,
     'read-char':readchar,
     'read':read,
     'run-python' : python,
     'eval-python':evalpython,
     'call-python-func':callPythonFunc,
     'exit': sys.exit,
     #Versiones optimizadas de manejo de listas--------------
     'sort':_sort,
     'reverse':_reverse,
     'reduce': lambda f,l:reduce(f,l),
     'member': lambda o,l: True if o in l else False, #con equal?
     'list-item':lambda l,p:l[p],
     'list-tail':lambda l,p:l[p:],
     'list-slice':lambda l,b,e:l[b:e],     
     'set-car!':setcar,
     'set-cdr!':setcdr,
     #---------------------------------------------------------
     #Manejo de cadenas---------------------------------------
     'substring': lambda c,b,e: c[b:e],
     'string-ref': lambda c,p:cad[p],
     'list->string':lambda l,sep:sep.join(l),
     'split-string':lambda s,c:s.split(c),
     'string->list': stringtolist,
     'string-append':stringappend,
     #---------------------------------------------------------
     #SQLite-----------------------------------------------------
     'open-sqlite-db': opensqlite, #(open-sqlite-db name)->conn
     'consult-sqlite-db': consultsqlite, #(consult-sqlite-db conn query params)
     #-----------------------------------------------------------
     'write':lambda x,port=sys.stdout:port.write(to_string(x)),
     'display':lambda x,port=sys.stdout:port.write(x if isa(x,str) else to_string(x)),
     'newline':newline,
     'input': lambda x: raw_input(x),
     'system': lambda x: os.system(x), 
     'gensym' : _gensym,
     'make-hash' : lambda : {},
     'gethash': lambda h,k:h[k],
     'sethash': sethash
     })
    return self

def sethash(h,k,v):
  h[k]=v
  return v

isa = isinstance

global_env = add_globals(Env())

################ eval (tail recursive)

def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    while True:
        if isa(x, Symbol):       # variable reference
            return env.find(x)[x]
        elif not isa(x, list):   # constant literal
            return x
        elif x[0] is _quote:     # (quote exp)
            (_, exp) = x
            return exp
        elif x[0] is _if:        # (if test conseq alt)
            (_, test, conseq, alt) = x
            x = (conseq if eval(test, env) else alt)
        elif x[0] is _set:       # (set! var exp)
            (_, var, exp) = x
            env.find(var)[var] = eval(exp, env)
            return None
        elif x[0] is _define:    # (define var exp)
            (_, var, exp) = x
            env[var] = eval(exp, env)
            return None
        elif x[0] is _lambda:    # (lambda (var*) exp)
            (_, vars, exp) = x
            return Procedure(vars, exp, env)
        elif x[0] is _begin:     # (begin exp+)
            for exp in x[1:-1]:
                eval(exp, env)
            x = x[-1]
        elif x[0] == _cond:     # (cond (p1 e1) ... (pn en))
            for (p, e) in x[1:]:
                if eval(p, env): 
                    return eval(e, env)
        else:                    # (proc exp*)
            exps = [eval(exp, env) for exp in x]
            proc = exps.pop(0)
            if isa(proc, Procedure):
                x = proc.exp
                env = Env(proc.parms, exps, proc.env)
            else:
                return proc(*exps)

################ expand

def expand(x, toplevel=False):
    "Walk tree of x, making optimizations/fixes, and signaling SyntaxError."
    require(x, x!=[])                    # () => Error
    if not isa(x, list):                 # constant => unchanged
        return x
    elif x[0] is _quote:                 # (quote exp)
        require(x, len(x)==2)
        return x
    elif x[0] is _if:                    
        if len(x)==3: x = x + [None]     # (if t c) => (if t c None)
        require(x, len(x)==4)
        return map(expand, x)
    elif x[0] is _set:                   
        require(x, len(x)==3); 
        var = x[1]                       # (set! non-var exp) => Error
        require(x, isa(var, Symbol), "can set! only a symbol")
        return [_set, var, expand(x[2])]
    elif x[0] is _define or x[0] is _definemacro: 
        require(x, len(x)>=3)            
        _def, v, body = x[0], x[1], x[2:]
        if isa(v, list) and v:           # (define (f args) body)
            f, args = v[0], v[1:]        #  => (define f (lambda (args) body))
            return expand([_def, f, [_lambda, args]+body])
        else:
            require(x, len(x)==3)        # (define non-var/list exp) => Error
            require(x, isa(v, Symbol), "can define only a symbol")
            exp = expand(x[2])
            if _def is _definemacro:     
                require(x, toplevel, "define-macro only allowed at top level")
                proc = eval(exp)       
                require(x, callable(proc), "macro must be a procedure")
                macro_table[v] = proc    # (define-macro v proc)
                return None              #  => None; add v:proc to macro_table
            return [_define, v, exp]
    elif x[0] is _begin:
        if len(x)==1: return None        # (begin) => None
        else: return [expand(xi, toplevel) for xi in x]
    elif x[0] is _lambda:                # (lambda (x) e1 e2) 
        require(x, len(x)>=3)            #  => (lambda (x) (begin e1 e2))
        vars, body = x[1], x[2:]
        require(x, (isa(vars, list) and all(isa(v, Symbol) for v in vars))
                or isa(vars, Symbol), "illegal lambda argument list")
        exp = body[0] if len(body) == 1 else [_begin] + body
        return [_lambda, vars, expand(exp)]   
    elif x[0] is _quasiquote:            # `x => expand_quasiquote(x)
        require(x, len(x)==2)
        return expand_quasiquote(x[1])
    elif isa(x[0], Symbol) and x[0] in macro_table:
        return expand(macro_table[x[0]](*x[1:]), toplevel) # (m arg...) 
    else:                                #        => macroexpand if m isa macro
        return map(expand, x)            # (f arg...) => expand each

def require(x, predicate, msg="wrong length"):
    "Signal a syntax error if predicate is false."
    if not predicate: raise SyntaxError(to_string(x)+': '+msg)

_append, _cons, _let = map(Sym, "append cons let".split())

def expand_quasiquote(x):
    """Expand `x => 'x; `,x => x; `(,@x y) => (append x y) """
    if not is_pair(x):
        return [_quote, x]
    require(x, x[0] is not _unquotesplicing, "can't splice here")
    if x[0] is _unquote:
        require(x, len(x)==2)
        return x[1]
    elif is_pair(x[0]) and x[0][0] is _unquotesplicing:
        require(x[0], len(x[0])==2)
        return [_append, x[0][1], expand_quasiquote(x[1:])]
    else:
        return [_cons, expand_quasiquote(x[0]), expand_quasiquote(x[1:])]

def let(*args):
    args = list(args)
    x = cons(_let, args)
    require(x, len(args)>1)
    bindings, body = args[0], args[1:]
    require(x, all(isa(b, list) and len(b)==2 and isa(b[0], Symbol)
                   for b in bindings), "illegal binding list")
    vars, vals = zip(*bindings)
    return [[_lambda, list(vars)]+map(expand, body)] + map(expand, vals)

macro_table = {_let:let} ## More macros can go here

eval(parse("""(begin

(define-macro and (lambda args 
   (if (null? args) #t
       (if (= (length args) 1) (car args)
           `(if ,(car args) (and ,@(cdr args)) #f)))))

(define-macro when
    (lambda (test branch)
    (list 'if test
        (cons 'begin branch))))

(define-macro unless
(lambda (test branch)
    (list 'if
        (list 'not test)
        (cons 'begin branch))))
             
                 
;falla con '() por la forma en que se pasan los args recursivos!
(define-macro or (lambda args
   (display args)(display "reccall->\\n")
   (if (null? args) #f
        (if (not (null? (car args))) (car args)   
              `(or ,@(cdr args) ))))) 

;; More macros can also go here


(define (first x) 
  (car x))

(define (second x)
  (car (cdr x)))

(define (third x)
  (car (cdr (cdr x))))

(define (fourth x)
  (car (cdr (cdr (cdr x)))))

(define rest cdr)

(define (assoc key records)
  (cond ((null? records) false)
        ((equal? key (caar records)) (car records))
        (else (assoc key (cdr records)))))

(define (make-table)
  (let ((local-table (list '*table*)))
    (define (lookup key-1 key-2)
      (let ((subtable (assoc key-1 (cdr local-table))))
        (if subtable
            (let ((record (assoc key-2 (cdr subtable))))
              (if record
                  (cdr record)
                  false))
            false)))
    (define (insert! key-1 key-2 value)
      (let ((subtable (assoc key-1 (cdr local-table))))
        (if subtable
            (let ((record (assoc key-2 (cdr subtable))))
              (if record
                  (set-cdr! record value)
                  (set-cdr! subtable
                            (cons (cons key-2 value)
                                  (cdr subtable)))))
            (set-cdr! local-table
                      (cons (list key-1
                                  (cons key-2 value))
                            (cdr local-table)))))
      'ok)    
    (define (dispatch m)
      (cond ((eq? m 'lookup-proc) lookup)
            ((eq? m 'insert-proc!) insert!)
            (else (error "Unknown operation -- TABLE" m))))
    dispatch))

(define operation-table (make-table))
(define get (operation-table 'lookup-proc))
(define put (operation-table 'insert-proc!))
)"""))

if __name__ == '__main__':
    repl()

