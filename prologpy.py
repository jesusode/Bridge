#!/usr/bin/env python
#
#   p r o l o g 3 . p y
#   Hacked from Python-for-Fun-by-Chris-Meyers
#
import sys, copy, re,os,cStringIO,cPickle
import random
import re
import urllib
##Copia del eval de Python----------
pyeval=eval
##----------------------------------

#Cambio para version independiente-----------------------------
if not 'java' in sys.platform:
    import sqlite3
    #print 'importando sqlite'
#--------------------------------------------------------------    

uppercase= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rules    = []
trace    = 0
#Cambios para mini2: toplevel es 1 cuando se ejecuta el interprete
toplevel=0
prolog_prompt='Minimal prolog>'
#----------------------------------------------------------------
goalId   = 100
indent   = ""

#Para DCGs------------------
dcgn='0'
rest='Rest'
#---------------------------

#Lista de predicados especiales------------------------------------------------------------------
SPECIAL_PREDS=['*is*', 'cut','fail','true','<','>','=>','=<','/==','==','=..','=','write','writeln',
               'read','assert','assertz','consult','retract','save','system','python','tostring',
               'exit','fopen','fread','fclose','fwrite','consultstring',
               'saveList','loadList','createTable','deleteTable','saveTable','loadTable','setTableEntry',
               'getTableEntry','getTableEntries','getTableValues','setPythonVar','getPythonVar',
               'callPythonFunc','evalPython','operator','split','join','divmod',
               'int','float','abs','bin','hex','char','ord','strip','pow','random',
               'strcat','strlen','substr','strfind','rematch','resplit','rereplace',
               'geturl','urlencode','urldecode']#Implementar 

PROLOG_TABLES={}

PROLOG_PYTHON_SHARED_NAMESPACE={} #Tabla compartida con Python

if not 'java' in sys.platform: #solo es predicado especial donde se puede tener sqlite3
    SPECIAL_PREDS+=['sqlite']

#-------------------------------------------------------------------------------------------------    
#numero de reglas activas-----------
def numrules():
    global rules
    return len(rules)
#------------------------------------

#Reduce reglas multilinea a reglas de una sola linea
def flatprolog(cad):
    #print 'cad: %s' % cad
    compressed=''
    rule=''
    for line in cad.split('\n'):
        #print 'analizando: %s' % line
        if line and line.strip()!='' and line.strip()[0]=='#': continue #Saltarse comentarios
        if line and line.strip()!='' and line.strip()[-1]not in ['.','?']:
            rule+=line.strip()
        if line and line.strip()!='' and line.strip()[-1]in ['.','?']:
            rule+=line.strip()
            compressed+='\n' + rule
            rule=''
        #print 'rule: %s' % rule
    return compressed.strip() + '\n'


def protectStrings(s):
    #Proteger codigo dentro de strings
    #print 's sin proteger: %s' % s
    regx=re.compile('\"[\s\S]*?\"')
    scont=0
    strings={}
    #print regx.findall(s)
    strs=regx.findall(s)
    for el in strs:
        s=s.replace(el,'%%%%'+str(scont)+'%%%%')
        #print 's al sustituir: %s' % s
        strings['%%%%'+str(scont)+'%%%%']=el
        scont+=1
    #print 's protegido: %s' %s
    return (s,strings,scont)


def recoverStrings(s,strings):
    #Recuperar el contenido de las strings-------------------------------------------------------
    numsusts=0
    #print 'probando string: %s' % s
    #print 'strings: %s' % strings
    s2=s
    for item in strings:
        s2=s2.replace(item,strings[item])
        if s!=s2:
            numsusts+=1
    #print 's reconstruido: %s'%s2
    return (s2,numsusts)
    #--------------------------------------------------------------------------------------------



def fatal (mesg) :
    sys.stdout.write ("Fatal error: %s\n" % mesg)
    sys.exit(1)

def split (l, sep, All=1) :
    "Split l by sep but honoring () and []"
    #print 'llamada a split. sep: %s,l: %s'%(sep,l)
    nest = 0
    #print type(sep)
    sep=str(sep)#!!!!!sep puede ser un termino
    lsep = len(sep)
    if l == "" : return []
    for i in range(len(l)) :
        c = l[i]
        if nest <= 0 and l[i:i+lsep] == sep :
            if All : return [l[:i]]+split(l[i+lsep:],sep)
            else   : return [l[:i],l[i+lsep:]]
        if c in ['[','('] : nest = nest+1
        if c in [']',')'] : nest = nest-1
    return [l]

def isVariable(term) : return term.args == [] and     term.pred[0:1] in uppercase
def isConstant(term) : return term.args == [] and not term.pred[0:1] in uppercase

infixOps = ["*is*","/==","==","=<","=>","=..","=","<",">","+","-","*","/",]
def splitInfix(s) :
    global infixOps
    for op in infixOps :
        #Trampa para arreglar el fallo con los numeros negativos--------
        # if op=='-' and not op in s[1:]:
            # print 'xvbfrty????'
            # break
        #---------------------------------------------------------------
        p = split(s,op,All=0)
        #print "p: %s"%p
        if len(p) > 1 :
            return (op,p)
    return None

def processDCG(cad):#?????Incompleto
    parts=cad.split('-->')
    print "parts:%s"%parts
    #Q&D: reconstruir el termino
    return parts[0] + '(' + ','.join(parts[1:]) + ')'


class Term :
    def __init__ (self, s, args=None) :
        #print 'construyendo termino con %s y %s'%(s,args)
        #print 'En Term: s:%s,args:%s'%(s,args)
        self.args=[] #Cambio para mini
        parts=None
        
        #if not args : parts = splitInfix(s)# a recuperar
        if not args and s and s[0]!='"': #Construir a partir de un string
            #print 'llamando a splitInfix'
            parts = splitInfix(s)
            
        if args :            # Predicate and args seperately
            self.pred = s
            self.args = args
        elif parts :
            #self.args = map(Term,parts[1])
            #parts[1],fldlist,numsusts=protectStrings(parts[1])
            #print 'valor de parts: %s' % str(parts)
            for el in parts[1]:
                #print 'elx:%s' % el
                #t,flag=recoverStrings(el,fldlist)
                #print 'tx: %s' % el                
                self.args.append(Term(el))
            self.pred = parts[0]
        elif s and s[-1] == ']' :  # Build list "term"
            flds = split(s[1:-1],",")#AQUI
            #print 'flds en list: %s' % flds
            fld2 = split(s[1:-1],"|")
            if len(fld2) > 1 :
                self.args = map(Term,fld2)
                self.pred = '.'
            else :
                flds.reverse()
                l = Term('.',[])
                for fld in flds : l = Term('.',[Term(fld),l])
                self.pred = l.pred; self.args = l.args
        elif s and s[-1] == ')' :               # Compile from "pred(a,b,c)" string
            flds = split(s,'(',All=0)
            if len(flds) != 2 : fatal("Syntax error in term: %s" % [s])
            #self.args = map(Term,split(flds[1][:-1],','))#Y AQUI
            flds[1],fldlist,numsusts=protectStrings(flds[1])
            for el in split(flds[1][:-1],','):
                #print 'el:%s' % el
                t,flag=recoverStrings(el,fldlist)
                #print 't: %s' % t
                self.args.append(Term(t))
            self.pred = flds[0]
        else : 
            self.pred = s           # Simple constant or variable
            self.args = []

    def __repr__ (self) :
        if self.pred == '.' :
            if len(self.args) == 0 : return "[]"
            nxt = self.args[1]
            if nxt.pred == '.' and nxt.args == [] :
                return "[%s]" % str(self.args[0])
            elif nxt.pred == '.' :
                return "[%s,%s]" % (str(self.args[0]),str(self.args[1])[1:-1])
            else :
                return "[%s|%s]" % (str(self.args[0]),str(self.args[1]))
        elif self.args :
            return "%s(%s)" % (self.pred, ",".join(map(str,self.args)))
        else : return self.pred

class Rule :
    def __init__ (self, s) :   # expect "term:-term,term,..."
        #print 'construyendo Regla con %s' % s
        flds = s.split(":-")
        #print "flds: %s" % flds
        self.head = Term(flds[0])
        self.goals = []
        if len(flds) == 2 :
            #print 'flds en rule: %s' %flds
            flds[1],fldlist,numsusts=protectStrings(flds[1])
            flds = split(flds[1],",")
            #print 'flds ahora en rule: %s' % flds
            #print fldlist
            for i in  range(len(flds)):
                t,flag=recoverStrings(flds[i],fldlist)
                flds[i]=t
            #print 'flds en rule ahora valen: %s' % flds
            for fld in flds : self.goals.append(Term(fld))

    def __repr__ (self) :
        rep = str(self.head)
        sep = " :- "
        for goal in self.goals :
            rep += sep + str(goal)
            sep = ","
        return rep
        
class Goal :
    def __init__ (self, rule, parent=None, env={}) :
        global goalId
        goalId += 1
        self.id = goalId
        self.rule = rule
        self.parent = parent
        self.env = copy.deepcopy(env)
        self.inx = 0      # start search with 1st subgoal

    def __repr__ (self) :
        return "Goal %d rule=%s inx=%d env=%s" % (self.id,self.rule,self.inx,self.env)

def main () :
    global toplevel
    toplevel=1
    #print sys.argv
    for file in sys.argv[1:] :
        if file == '.' : return    # early out. no user interaction
        f=cStringIO.StringIO(flatprolog(open(file).read()))
        #print 'Archivo processado: %s' % f.getvalue()
        procFile(f,'')    # file on the command line
    procFile (sys.stdin,prolog_prompt)      # let the user have her say

def procString (f) :
    global rules, trace,toplevel
    f=flatprolog(f)
    env = []
    for sent in f.split('\n') :
        #print 'leido: %s' % sent
        if sent == "" : continue
        s = re.sub("#.*","",sent[:-1]) # clip comments and newline
        s = re.sub(" is ","*is*",s)    # protect "is" operator
        s = re.sub("\\\\n","\n",s)    # saltos de linea??
        #Mas cambios para mini2--------------------------------------------------
        s=s.strip()
        #print 'valor de s: %s' % s
        
        #Hay que proteger las cadenas antes de quitar el espacio sobrante!!!!!!!
        #print 's antes: %s'%s
        s,strings,numsus=protectStrings(s)
        s = re.sub(" ", "" ,s)           # remove spaces ????????????????????                  
        s,flag=recoverStrings(s,strings)
        #print 's despues: %s'%s
        #------------------------------------------------------------------------- 

        if s == "" : continue

        if s[-1] in '?.' : punc=s[-1]; s=s[:-1]
        else             : punc='.'

        if punc == '?' :
            #print 'llamada a search con s=%s'%s
            search(Term(s))
        elif '-->' in s:
            print "Detectado DCG!!"
            s=processDCG(s)
            rules.append(Rule(s))
        else             :
            #print 'Construyendo regla con %s' %s
            rules.append(Rule(s))
    #print 'rules: %s ' %rules

def procFile (f, prompt) :
    global rules, trace,toplevel
    env = []
    while 1 :
        if prompt :
            sys.stdout.write(prompt)
            sys.stdout.flush()
        sent = f.readline()
        #print 'leido: %s' % sent
        if sent == "" : break
        s = re.sub("#.*","",sent[:-1]) # clip comments and newline
        s = re.sub(" is ","*is*",s)    # protect "is" operator
        s = re.sub("\\\\n","\n",s)    # saltos de linea??
        #Mas cambios para mini2--------------------------------------------------
        s=s.strip()
        #print 'valor de s: %s' % s
        
        #Hay que proteger las cadenas antes de quitar el espacio sobrante!!!!!!!
        #print 's antes: %s'%s
        s,strings,numsus=protectStrings(s)
        s = re.sub(" ", "" ,s)           # remove spaces ????????????????????                  
        s,flag=recoverStrings(s,strings)
        #print 's despues: %s'%s
        #------------------------------------------------------------------------- 

        if s == "" : continue

        if s[-1] in '?.' : punc=s[-1]; s=s[:-1]
        else             : punc='.'
        if   s == 'trace=0' : trace = 0
        elif s == 'trace=1' : trace = 1

        #Cambios para mini2------------------
        elif s == 'toplevel=0' : toplevel = 0
        elif s == 'toplevel=1' : toplevel = 1
        #-------------------------------------

        elif s == 'quit'    : sys.exit(0)
        elif s == 'listing'  :
            for rule in rules : print rule
        elif punc == '?' :
            #print 'llamada a search'
            search(Term(s))
        elif '-->' in s:
            #print "Detectado DCG!!"
            s=processDCG(s)
            #print s
            #sys.exit(0)
            rules.append(Rule(s))
        else             :
            #print 'Construyendo regla con %s' %s
            rules.append(Rule(s))

# A Goal is a rule in at a certain point in its computation. 
# env contains definitions (so far), inx indexes the current term
# being satisfied, parent is another Goal which spawned this one
# and which we will unify back to when this Goal is complete.
#

def unify (src, srcEnv, dest, destEnv) :
    "update dest env from src. return true if unification succeeds"
    global trace, indent
    if trace : print indent, "Unify", src, srcEnv, "to", dest, destEnv
    indent = indent+"  "
    if src.pred == '_' or dest.pred == '_' : return sts(1,"Wildcard")

    if isVariable(src) :
        srcVal = eval(src, srcEnv)
        if not srcVal : return sts(1,"Src unset")
        else : return sts(unify(srcVal,srcEnv,dest,destEnv), "Unify to Src Value")

    if isVariable(dest) :
        destVal = eval(dest, destEnv)           # evaluate destination
        if destVal : return sts(unify(src,srcEnv,destVal,destEnv),"Unify to Dest value")
        else :
            destEnv[dest.pred] = eval(src,srcEnv)
            return sts(1,"Dest updated 1")      # unifies. destination updated

    elif src.pred      != dest.pred      : return sts(0,"Diff predicates")
    elif len(src.args) != len(dest.args) : return sts(0,"Diff # args")
    else :
        dde = copy.deepcopy(destEnv)
        for i in range(len(src.args)) :
            if not unify(src.args[i],srcEnv,dest.args[i],dde) :
                return sts(0,"Arg doesn't unify")
        destEnv.update(dde)
        return sts(1,"All args unify")

def sts(ok, why) :
    global trace, indent
    indent = indent[:-2]
    if trace: print indent, ["No","Yes"][ok], why
    return ok

def search (term) :
    global trace,toplevel,rules,infixOps
    all_solutions=[]
    #print 'en search: %s' %repr(term)#term
    #print 'partial_solutions: %s' % partial_solutions
    # pop will take item from end, insert(0,val) will push item onto queue
    goal = Goal(Rule("all(done):-x(y)"))      # Anything- just get a rule object
    goal.rule.goals = [term]                  # target is the single goal
    queue = [goal]# Start our search
    while queue :
        #print 'Queue en el while: %s' % str(queue)
        #trace=1 #Solo para pruebas!!!!!!
        c = queue.pop()                       # Next goal to consider
        #print 'Objetivo: %s' % c
        if trace : print "Deque", c
        if c.inx >= len(c.rule.goals) :       # Is this one finished?
            if c.parent == None :            # Yes. Our original goal?
                if c.env :
                    if toplevel==1: print  c.env             # Yes. tell user we
                    all_solutions.append(c.env)
                else     :
                    if toplevel==1: print "Yes" # have a solution
                    #print 'metiendo un YES'
                    all_solutions.append('Yes') #
                #print 'all_solutions por ahora: %s'%all_solutions
                continue
            parent = copy.deepcopy(c.parent)  # Otherwise resume parent goal
            unify (c.rule.head,    c.env,
                   parent.rule.goals[parent.inx],parent.env)
            parent.inx = parent.inx+1         # advance to next goal in body
            queue.insert(0,parent)            # let it wait its turn
            if trace : print "Queue", parent
            continue

        # No. more to do with this goal.
        term = c.rule.goals[c.inx]            # What we want to solve
        #print 'Evaluando termino: %s' % term
        pred = term.pred  # Special term?
        #print 'Evaluando termino: %s' % pred
        if pred in SPECIAL_PREDS:
            #print 'predicado especial!!: %s'%pred
            if pred == '*is*' :
                ques = eval(term.args[0],c.env)
                ans  = eval(term.args[1],c.env)
                if ques == None :
                    c.env[term.args[0].pred] = ans  # Set variable
                elif ques.pred != ans.pred :
                    continue                # Mismatch, fail
            elif pred == '=' : 
                #print 'En =!!!'
                ques = eval(term.args[0],c.env)
                ans  = eval(term.args[1],c.env)
                if ques == None :
                    c.env[term.args[0].pred] = ans  # Set variable
                elif ques.pred != ans.pred :
                    continue                # Mismatch, fail
            elif pred == 'read':
                c.env[term.args[0].pred] = Term(raw_input()) #Leer variable
            elif pred == 'int':
                strnum=str(eval(term.args[0],c.env)).strip('"')
                c.env[term.args[1].pred] = Term(str(int(strnum)))
            elif pred == 'float':
                strnum=str(eval(term.args[0],c.env)).strip('"')
                c.env[term.args[1].pred] = Term(str(float(strnum)))
            elif pred == 'divmod':
                strnum=int(str(eval(term.args[0],c.env)).strip('"'))
                strnum2=int(str(eval(term.args[1],c.env)).strip('"'))
                c.env[term.args[2].pred] = Term(str(list(divmod(strnum,strnum2))))
            elif pred == 'abs':
                strnum=float(str(eval(term.args[0],c.env)).strip('"'))
                c.env[term.args[1].pred] = Term(str(abs(strnum)))
            elif pred == 'bin':
                strnum=int(str(eval(term.args[0],c.env)).strip('"'))
                c.env[term.args[1].pred] = Term(str(bin(strnum)[2:]))
            elif pred == 'hex':
                strnum=str(eval(term.args[0],c.env)).strip('"')
                c.env[term.args[1].pred] = Term(str(hex(int(strnum))[2:]))
            elif pred == 'char':
                strnum=str(eval(term.args[0],c.env)).strip('"')
                c.env[term.args[1].pred] = Term(str(chr(int(strnum))))
            elif pred == 'ord':
                strnum=str(eval(term.args[1],c.env)).strip('"')
                c.env[term.args[0].pred] = Term(str(ord(strnum)))
            elif pred == 'strip':
                cad=str(eval(term.args[1],c.env)).strip('"')
                sub=str(eval(term.args[0],c.env)).strip('"')
                c.env[term.args[2].pred] = Term(cad.strip(sub))
            elif pred == 'strcat':
                s1=str(eval(term.args[0],c.env)).strip('"')
                s2=str(eval(term.args[1],c.env)).strip('"')
                c.env[term.args[2].pred] = Term(s1+s2)
            elif pred == 'substr':
                s1=str(eval(term.args[0],c.env)).strip('"')
                beg=int(str(eval(term.args[1],c.env)).strip('"'))
                end=int(str(eval(term.args[2],c.env)).strip('"'))
                c.env[term.args[2].pred] = Term(s1[beg:end])
            elif pred == 'strfind':
                s1=str(eval(term.args[0],c.env)).strip('"')
                s2=str(eval(term.args[1],c.env)).strip('"')
                pos=s1.find(s2)
                if pos >0:
                    c.env[term.args[2].pred] = Term(str(pos))
                else:
                    continue
            elif pred == 'strlen':
                cad=str(eval(term.args[0],c.env)).strip('"')
                c.env[term.args[1].pred] = Term(str(len(cad)))
            elif pred == 'rematch':
                regex=str(eval(term.args[0],c.env)).strip('"')
                cad=str(eval(term.args[1],c.env)).strip('"')
                r=re.compile(regex)
                l=r.findall(cad)
                c.env[term.args[2].pred] = Term(str(l))
            elif pred == 'resplit':
                regex=str(eval(term.args[0],c.env)).strip('"')
                cad=str(eval(term.args[1],c.env)).strip('"')
                r=re.compile(regex)
                l=r.split(cad)
                c.env[term.args[2].pred] = Term(str(l))
            elif pred == 'rereplace':
                regex=str(eval(term.args[0],c.env)).strip('"')
                cad=str(eval(term.args[1],c.env)).strip('"')
                rep=str(eval(term.args[2],c.env)).strip('"')
                r=re.compile(regex)
                l=r.sub(rep,cad)
                c.env[term.args[3].pred] = Term(l)
            elif pred == 'pow':
                base=float(str(eval(term.args[0],c.env)).strip('"'))
                exp=float(str(eval(term.args[1],c.env)).strip('"'))
                c.env[term.args[2].pred] = Term(str(base**exp))
            elif pred == 'random':
                c.env[term.args[0].pred] = Term(str(random.random()))
            elif pred == 'geturl':#Hace cosas raras al montar el Term con el resultado!!!!
                path=str(eval(term.args[0],c.env)).strip('"')
                cont=urllib.urlopen(path).read()
                #print cont
                c.env[term.args[1].pred] = Term('"' + cont + '"')
            elif pred == 'urlencode':
                cad=str(eval(term.args[0],c.env)).strip('"')
                #print urllib.quote_plus(cad)
                c.env[term.args[1].pred] = Term('"' + urllib.quote_plus(cad) + '"')
            elif pred == 'urldecode':
                cad=str(eval(term.args[0],c.env)).strip('"')
                c.env[term.args[1].pred] = Term('"' + urllib.unquote_plus(cad) + '"')
            elif pred == 'cut' :
                  #print 'queue antes del corte:%s'%queue
                  queue = [] # Zap the competition
                  #print 'Aplicando corte!'
                  #print 'queue despues del corte:%s'%queue
            elif pred == 'fail':
                 #print 'Aplicando FAIL!'
                 #print 'all_solutions in fail: %s' %all_solutions
                 #En fail hay que quitar los posibles 'Yes' de all_solutions
                 all_solutions=[x for x in all_solutions if x!='Yes']
                 #print 'all_solutions al salir de fail: %s' %all_solutions
                 continue   # Dont succeed
            elif pred=='true': #No hacer nada
                 pass
            elif pred == 'exit': sys.exit(0)  
            elif pred=='operator':#op(Precedence,Type,Name)=>Aqui solo operator(name). Todos infijos
                infixOps.append(term.args[0])
                #print infixOps
            elif pred=='=..': #Predicado Univ: reversible: X =.. [a,b,c]=>X=a(b,c) || X=..a(b,c)=>X=[a,b,c]. Solo acepta atomos en la posicion 0 de la lista.
                a=isVariable(term.args[0])
                b=isVariable(term.args[1])
                #print term.args[0].pred
                #print term.args[1].pred
                if a==b: raise Exception("Error: en el predicado Univ(=..) no pueden ser variables los dos argumentos")
                if a and str(term.args[1].pred)=='.': #Revisar esto!!!!
                    items=(str(term.args[1])[1:-1]).split(',')
                    #print 'items: %s' % items
                    cad=items[0] + '(' + ','.join(items[1:]) + ')'
                    #print cad
                    c.env[term.args[0].pred]=Term(cad)
                elif a and str(term.args[1].pred)!='.':
                    f=str(term.args[1].pred)
                    items=term.args[1].args
                    c.env[term.args[0].pred]=Term('['+f+','+ ','.join(map(str,items)) + ']')
                elif b and str(term.args[0].pred)=='.': #Revisar esto!!!!
                    items=(str(term.args[0])[1:-1]).split(',')
                    #print 'items: %s' % items
                    cad=items[0] + '(' + ','.join(items[1:]) + ')'
                    #print cad
                    c.env[term.args[1].pred]=Term(cad)
                elif b and str(term.args[0].pred)!='.':
                    f=str(term.args[0].pred)
                    items=term.args[0].args
                    c.env[term.args[1].pred]=Term('['+f+','+ ','.join(map(str,items)) + ']')
            elif pred=='write':
                res=eval(term.args[0],c.env)#Revisar esto!!!
                #print 'en write con res:%s'%res
                if type(str(res)) in [type(''),type(u'')]:
                    sys.stdout.write(str(res).strip().strip('"').strip("'"))
                    sys.stdout.flush()
                else:
                    sys.stdout.write(str(res))
                    sys.stdout.flush()
            elif pred=='writeln':
                res=eval(term.args[0],c.env)#Revisar esto!!!
                #print 'en write con res:%s'%res
                if type(str(res)) in [type(''),type(u'')]:
                    print str(res).strip().strip('"').strip("'")
                else:
                    print str(res)                    
            elif pred=='system':
                cmd=str(eval(term.args[0],c.env))#Revisar esto!!!
                os.system(cmd)
            elif pred=='split':#split(cad,sep,L)
                cad=str(eval(term.args[0],c.env)).strip('"')
                sep=str(eval(term.args[1],c.env)).strip('"')
                c.env[term.args[2].pred]=Term(str(cad.split(sep)))  
            elif pred=='join':#join(lst,sep,Cad)
                lst=eval(term.args[0],c.env)
                sep=str(eval(term.args[1],c.env)).strip('"')
                c.env[term.args[2].pred]=Term(sep.join(pyeval(repr(lst))))
            elif pred=='fopen':#Revisar esto. fopen(path,mode,Handle)
                c.env[term.args[2].pred]=open(str(eval(term.args[0],c.env))[1:-1],str(eval(term.args[1],c.env))[1:-1])
            elif pred=='fwrite':#fwrite(Handle,Material)
                c.env[term.args[0].pred].write(str(eval(term.args[1],c.env)).strip('"'))
            elif pred=='fread':#fread(Handle,Dest)
                c.env[term.args[1].pred]=Term('"' + c.env[term.args[0].pred].read() + '"')              
            elif pred=='fclose':#fclose(Handle)
                c.env[term.args[0].pred].close()
            elif pred=='python':#python(code)
                #print 'en python'
                cmd=str(eval(term.args[0],c.env))#Revisar esto!!!
                #print cmd
                exec cmd.strip('"')
                #eval(cmd)
            elif pred=='callPythonFunc': #callPythonFunc(fname,arglist,Resul)
                #Excepcion si no existe la funcion y si el segundo argumento no es una lista!!!!!
                f=str(eval(term.args[0],c.env)).strip('"')#Revisar esto!!!
                _args=eval(term.args[1],c.env)
                _args='[%s,%s]'% (str(_args.args[0]),str(_args.args[1])[1:-1])
                #El resultado TIENE que obtenerse como una cadena (?)
                _args='"' + str(pyeval(f)(*pyeval(_args))) + '"'
                c.env[term.args[2].pred]=Term(_args)
            elif pred=='evalPython': #evalPython(evalstring,Resul)
                evalstr=str(eval(term.args[0],c.env)).strip('"')#Revisar esto!!!
                #El resultado TIENE que obtenerse como una cadena (?)
                _res='"' + str(pyeval(evalstr)) + '"'
                c.env[term.args[1].pred]=Term(_res) 
                
            elif pred=='saveList': #saveList(fname,List)
                #Excepcion si no existe la funcion y si el segundo argumento no es una lista!!!!!
                fname=eval(term.args[0],c.env).pred.strip('"')
                lst=eval(term.args[1],c.env)
                cPickle.dump(lst,open(fname,'w'))
            elif pred=='loadList': #loadList(fname,List)
                #Excepcion si no existe la funcion y si el segundo argumento no es una lista!!!!!
                fname=eval(term.args[0],c.env).pred.strip('"')
                c.env[term.args[1].pred]=cPickle.load(open(fname,'r'))
            elif pred=='createTable': #createTable(tablename)
                #Excepcion si no existe la funcion y si el segundo argumento no es una lista!!!!!
                PROLOG_TABLES[eval(term.args[0],c.env).pred.strip('"')]={}
                print PROLOG_TABLES
            elif pred=='deleteTable': #deleteTable(tablename)
                #Excepcion si no existe la funcion y si el segundo argumento no es una lista!!!!!
                name=eval(term.args[0],c.env).pred.strip('"')
                if name in PROLOG_TABLES:
                    del PROLOG_TABLES[name]
                #print PROLOG_TABLES
            elif pred=='saveTable': #saveList(fname,tname)
                #
                fname=eval(term.args[0],c.env).pred.strip('"')
                tbl=eval(term.args[1],c.env).pred.strip('"')
                if tbl in PROLOG_TABLES:
                    cPickle.dump(PROLOG_TABLES[tbl],open(fname,'w'))
                #print PROLOG_TABLES
            elif pred=='loadTable': #loadTable(fname,tname)
                #
                fname=eval(term.args[0],c.env).pred.strip('"')
                if term.args[1].pred.strip('"')[0] in uppercase: #Es una variable que hay que evaluar
                    PROLOG_TABLES[c.env[term.args[1].pred.strip('"')]]=cPickle.load(open(fname,'r'))
                else:
                    PROLOG_TABLES[term.args[1].pred.strip('"')]=cPickle.load(open(fname,'r'))
                #print PROLOG_TABLES
            elif pred=='setTableEntry': #setTableEntry(tname,key,value)
                #
                tname=eval(term.args[0],c.env).pred.strip('"')
                key=eval(term.args[1],c.env).pred.strip('"')
                val=eval(term.args[2],c.env).pred
                #if type(val) in [type(''),type(u'')]:
                #    val=val.strip('"')
                if tname in PROLOG_TABLES:
                   PROLOG_TABLES[tname][key]=val
                #print PROLOG_TABLES
                
            elif pred=='getTableEntry': #getTableEntry(tname,key,Val)
                #
                tname=eval(term.args[0],c.env).pred.strip('"')
                key=eval(term.args[1],c.env).pred.strip('"')
                val=eval(term.args[2],c.env)
                if val:
                    val=val.pred
                else:#No existe. Crearla??????
                    val=Term(term.args[2].pred)
                if tname in PROLOG_TABLES and val and val.pred[0] in uppercase:
                   c.env[val.pred]=Term('"' + str(PROLOG_TABLES[tname][key]) + '"')

            elif pred=='getTableEntries': #getTableEntries(tname,Val)
                #
                tname=eval(term.args[0],c.env).pred.strip('"')
                val=term.args[1]
                if tname in PROLOG_TABLES and val and val.pred[0] in uppercase:
                   _args=  '"' +  str(PROLOG_TABLES[tname].keys()) + '"'
                   c.env[term.args[1].pred]=Term(_args)

            elif pred=='getTableValues': #getTableValues(tname,Val)
                #
                tname=eval(term.args[0],c.env).pred.strip('"')
                val=term.args[1]
                if tname in PROLOG_TABLES and val and val.pred[0] in uppercase:
                   _args=  '"' +  str(PROLOG_TABLES[tname].values()) + '"'
                   c.env[term.args[1].pred]=Term(_args)

            elif pred=='getPythonVar': #getPythonVar(varname,Val)
                #
                vname=eval(term.args[0],c.env).pred.strip('"')
                val=term.args[1]
                if vname in PROLOG_PYTHON_SHARED_NAMESPACE and val and val.pred[0] in uppercase:
                   _args=  '"' +  str(PROLOG_PYTHON_SHARED_NAMESPACE[vname]) + '"'
                   c.env[term.args[1].pred]=Term(_args)

            elif pred=='setPythonVar': #setPythonVar(varname,Val)
                #
                vname=eval(term.args[0],c.env).pred.strip('"')
                val=eval(term.args[1],c.env).pred.strip('"')
                PROLOG_PYTHON_SHARED_NAMESPACE[vname]=val
                #print PROLOG_PYTHON_SHARED_NAMESPACE
                
            elif pred=='sqlite': #sqlite(db,query,arglist,Resul)
                conn=sqlite3.connect(str(eval(term.args[0],c.env)).strip('"'), isolation_level=None)
                cursor=conn.cursor()
                query=eval(term.args[1],c.env).pred.strip('"')
                #print query
                _args=eval(term.args[2],c.env)
                if len(_args.args)==0:
                    _args='[]'
                else:
                    _args='[%s,%s]'% (str(_args.args[0]),str(_args.args[1])[1:-1])
                #El resultado TIENE que obtenerse como una cadena (?)
                a=pyeval(_args)
                #res=cursor.executemany(query,a)#Esto hay que hacerlo con transacciones!!!!!!!!
                res=cursor.execute(query,a)
                data=[]
                if res:
                  data=cursor.fetchall()
                data=[list(el) for el in data]
                conn.commit()
                cursor.close()
                _args='"' + str(data) + '"'
                c.env[term.args[3].pred]=Term(_args)                
            elif pred=='assert': 
                #print 'en assert!'
                s=eval(term.args[0],c.env)#Revisar esto!!!
                s = re.sub(" is ","*is*",str(s))    # protect "is" operator
                rules.append(Rule(s))
            elif pred=='assertz': 
                #print 'en assertz!'
                s=eval(term.args[0],c.env)#Revisar esto!!!
                s = re.sub(" is ","*is*",str(s))    # protect "is" operator
                rules=[Rule(s)] + rules                
            elif pred=='consult': #
                #print 'en consult'
                ff=str(eval(term.args[0],c.env)).strip('"')#Revisar esto!!!
                if os.path.exists(ff) and os.path.isfile(ff):
                    f=cStringIO.StringIO(flatprolog(open(ff).read()))
                    procFile(f,'')
            elif pred=='consultstring': #
                #print 'en consult'
                f=cStringIO.StringIO(flatprolog(str(eval(term.args[0],c.env)).strip('"')))
                procFile(f,'')                    
            elif pred=='retract': #Hay que controlar los argumentos tambien (Ej: retract(name(X,value)) )
                #print 'en retract!'
                todel=str(eval(term.args[0],c.env)).strip('"')
                temprules=[]
                for rule in rules:
                    if '(' in str(rule.head):
                        if todel != str(rule.head).split('(')[0]:
                            temprules.append(rule)
                        else:
                            if toplevel==1: print 'Retracting rule: %s' %rule
                    else:
                        if todel != str(rule.head):
                            temprules.append(rule)
                        else:
                            if toplevel==1: print 'Retracting rule: %s' %rule
                rules=temprules[:]

            elif pred=='getrules': #getrules(functor,Var)Obtiene todas las reglas que coincidan con functor como lista en Var
                pass

            elif pred=='save': #save(path)
                #print 'en save!'
                path=str(eval(term.args[0],c.env)).strip('"')
                f=open(path,'w')
                for rule in rules:
                    f.write(str(rule) + '.\n')
                f.close()
            elif pred=='tostring': #tostring(Str)
                #print 'en tostring!'
                _str='"'
                for rule in rules:
                    _str+=str(rule) + '.'
                _str+='"'
                #print _str
                c.env[term.args[0].pred]=Term(_str)
            elif not eval(term,c.env) :
                continue # Fail if not true
            c.inx = c.inx + 1               # Succeed. resume self.
            queue.insert(0,c)
            continue
        
        elif pred=='call':#Revisar esto!!!
            #print 'evaluando un call!!!!'
            #print term
            #print 'nuevo termino a evaluar: %s,%s' %(term.args[0],term.args[0].__class__)
            #print c.env
            p=search(eval(term.args[0],c.env))  #,all_solutions)#Cuidadin!!!
            #p=search(term.args[0])  #,all_solutions)#Cuidadin!!!
            #print 'all_solutions despues de call: %s' % p
            if len(p)>=1: #Si hay soluciones es verdadero.
                c.inx = c.inx + 1  
                queue.insert(0,c)
                all_solutions.extend(p)#Ojito con esto
            continue

        elif pred in ['findall','bagof']:#Revisar esto!!!
            a=isVariable(term.args[0])
            b=isVariable(term.args[2])
            if a!=b: raise Exception("Error: en el predicado findall: el primer y el tercer argumento deben ser variables")
            #print 'evaluando un findall!!!!'
            #print term.args
            p=search(term.args[1]) 
            #print 'all_solutions despues de findall: %s' % p
            if len(p)>=1: #Si hay soluciones es verdadero.
                c.inx = c.inx + 1  
                queue.insert(0,c)
                if pred=='findall':
                    c.env[term.args[2].pred] = Term(str([x[term.args[0].pred] for x in p]))
                else: #bagof
                    c.env[term.args[2].pred] =Term(str(list(set( [str(x[term.args[0].pred]) for x in p]))))
                #print 'c.env en findall: %s' % c.env
            continue
        
        
        #print 'Entrando al for'
        for rule in rules :   # Not special. Walk rule database
            #print 'probando regla: %s con %s' % (rule,term)
            if rule.head.pred      != term.pred      : continue
            if len(rule.head.args) != len(term.args) : continue
            child = Goal(rule, c)               # A possible subgoal
            ans = unify (term, c.env, rule.head, child.env)
            if ans : # if unifies, queue it up
                #print 'unificacion con %s' % rule
                queue.insert(0,child)
                if trace : print "Queue", child
        #print 'queue al salir del for: %s'%queue
    #print 'Saliendo de search!!'
    return all_solutions


#def add (a,b) : return Term(str(int(a.pred)+int(b.pred)),[])
#Revisar operadores para que funcionen tambien con strings
def add (a,b):
    print 'a: %s,b: %s' %(a,b)
    #if str(a.pred)[0]=='"': #string: concatenamos
    #       return Term(str((a.pred).strip('"'))+ str((b.pred).strip('"')),[])
    if '.' in str(a.pred):
        return Term(str(float(a.pred)+float(b.pred)),[])
    else:
        return Term(str(int(a.pred)+int(b.pred)),[])
    
def sub (a,b) :
    #print 'en sub con (%s,%s)'%(a,b)
    if a is None:
        return Term(str(-int(b.pred)),[])
    else:
        if '.' in str(a) or '.' in str(b): # algun float
           return Term(str(float(a.pred)-float(b.pred)),[])
        else:
            return Term(str(int(a.pred)-int(b.pred)),[])        
    
def mul (a,b) : return Term(str(float(a.pred)*float(b.pred)),[])

def div (a,b): return Term(str(float(a.pred)/float(b.pred)),[])

def lt  (a,b) : return str(a.pred) <  str(b.pred)
def eq  (a,b) : 
    #print 'en equal: %s,%s'%(repr(a.pred),repr(b.pred))
    #print 'en equal: %s,%s'%(type(str(a.pred)),type(str(b.pred)))
    #print 'resultado:%s' %(str(a.pred) == str(b.pred))
    return str(a.pred) == str(b.pred)
def neq  (a,b) : return str(a.pred) != str(b.pred)
#Nuevas-------------------------------------------
def gt  (a,b) : return str(a.pred) >  str(b.pred)
def ge  (a,b) : return str(a.pred) >=  str(b.pred)
def le  (a,b) : return str(a.pred) <=  str(b.pred)
#-------------------------------------------------

operators = {'+': add, '-':sub, '*':mul, '<':lt,'>':gt,'>=':ge,'=<':le,'/==':neq,'==':eq,'/':div}

def eval (term, env) :      # eval all variables within a term to constants
    #print 'En eval con %s y %s'%(term,env)
    #print type(term)
    #if hasattr(term,'pred'): print 'term.pred: %s' %term.pred
    special = operators.get(term.pred)
    if special :
        #print 'por is special: %s' %eval(term.args[0],env),eval(term.args[1],env)
        return special(eval(term.args[0],env),eval(term.args[1],env))
    if isConstant(term) :
        #print 'por isConstant'
        return term
    if isVariable(term) :#if o elif???
        #print 'por isVariable'
        ans = env.get(term.pred)
        #print 'term.pred: %s'%term.pred
        if not ans : return None
        else       : return eval(ans,env)
    args = []
    for arg in term.args : 
        a = eval(arg,env)
        if not a : return None
        args.append(a)
    return Term(term.pred, args)

if __name__ == "__main__" : main()
