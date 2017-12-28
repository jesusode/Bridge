#Funciones de utilidad
import sys
import types
import copy
import string
import codecs
import io
import math
import time
import ctypes
import locale

HY_AVAILABLE=0 #Gestionar carga de Hy con una directiva -lisp (es lento y entorpece el arranque)
TK_AVAILABLE=0 #Uso de formbox

import imp
import md5
import platform
import inspect
import cProfile
import xml
if not 'java' in sys.platform:
    import json

#Soporte para subprocesos
import subprocess

#Revisar
import threading
import thread
import socket
#No hay multiprocessing en jython ni iPad/iPhone
if not 'java' in sys.platform and not'iPad' in platform.platform() and not 'iPhone' in platform.platform():
    import multiprocessing

#Soporte para async (parece que funciona bien en jython y iPad/iPhone)
import concurrent.futures

#Soporte ADO en win32---------------
if 'win32' in sys.platform:
    if platform.python_implementation() not in ["PyPy"]:
        import minimal_ado
        import win32com
#-----------------------------------

#Soporte Tkinter para usar formbox-------------
if '-tk' in sys.argv:
    if not 'java' in sys.platform and not'iPad' in platform.platform() and not 'iPhone' in platform.platform():
        import Tkinter
        import mini_tkbasic
        TK_AVAILABLE=1
    else:
        raise Exception("Error: Tkinter no esta disponible en esta plataforma")
#----------------------------------------------

#Ojo: esto peta si queremos un ejecutable con py2exe!!!----------------------------
# if '-math' in sys.argv:#??????????????
    # import sympy
#----------------------------------------------------------------------------------

if not 'os' in sys.modules:
     os=__import__('os')
else:
    os=sys.modules['os']
if not 'os.path' in sys.modules:
     os.path=__import__('os.path')
else:
     os.path=sys.modules['os.path']
if not 'inspect' in sys.modules:
     inspect=__import__('inspect')
else:
     inspect=sys.modules['inspect']
if not 'itertools' in sys.modules:
     itertools=__import__('itertools')
else:
     itertools=sys.modules['itertools']
if not 're' in sys.modules:
     re=__import__('re')
else:
     re=sys.modules['re']
if not 'glob' in sys.modules:
     glob=__import__('glob')
else:
     glob=sys.modules['glob']
if not 'fnmatch' in sys.modules:
     fnmatch=__import__('fnmatch') 
else:
     fnmatch=sys.modules['fnmatch']
import xml.dom.minidom as minidom
try:
    if not 'sqlite3' in sys.modules:
         sqlite3=__import__('sqlite3')
    else:
         sqlite3=sys.modules['sqlite3']
    SQLITE=1
except:
    SQLITE=0
if not 'prologpy' in sys.modules: 
     prologpy=__import__('prologpy')
else:
     prologpy=sys.modules['prologpy']
if not 'heapq' in sys.modules:
     heapq=__import__('heapq')
else:
     heapq=sys.modules['heapq']
if not 'urllib' in sys.modules:
    urllib=__import__('urllib')
else:
    urllib=sys.modules['urllib']
if not 'matrix' in sys.modules:
     matrix=__import__('matrix')
else:
     matrix=sys.modules['matrix']
if not 'pprint' in sys.modules:
     pprint=__import__('pprint')
else:
     pprint=sys.modules['pprint']
if not 'shutil' in sys.modules:
     shutil=__import__('shutil')
else:
     shutil=sys.modules['shutil']

if not 'inspect' in sys.modules:
    inspect=__import__('inspect')
else:
    inspect=sys.modules['inspect']

if not 'pickle' in sys.modules:
    pickle=__import__('pickle')
else:
    pickle=sys.modules['pickle']

if not 'lispy' in sys.modules:
    lispy=__import__('lispy')
else:
    lispy=sys.modules['lispy']

import cStringIO
#------------------------------------------------------------------------------
#Clase que envuelve un StringBuffer
#El contenido del buffer se obtiene con una llamada al mismo sin argumentos
#Para poner strings en el buffer se pude usar el operador +
# que admite un string o bien otro StringBuffer,
#o un llamada con tantos argumentos como se quieran meter en el buffer
#------------------------------------------------------------------------------ 
class StringBuffer:
    def __init__(self,*vals):
        self._sb= cStringIO.StringIO()
        self._encoding='utf-8'
        if vals!=(): 
            for item in vals:
                if type(item)==str:
                    self._sb.write(item)
                elif isinstance(item,StringBuffer):
                    self._sb.write(item._collect())
                else:
                    self._sb.write(str(item))
        self.__canCollect=True

    def getEncoding(self):
        return self._encoding

    def setEncoding(self,enc):
        self._encoding=enc

    def _canCollect(self):
        return self.__canCollect

    def __add__(self,astr):
        if self._canCollect():
            if type(astr) in [str,unicode]:
                self._sb.write(_tostring(astr,self._encoding))
            elif isinstance(astr,StringBuffer):
                self._sb.write(_tostring(astr._collect(),self._encoding))
            else:
                self._sb.write(str(astr))

    def __call__(self,*args):
        if args!=():
            for item in args:
                if type(item) in [str,unicode]:
                    self._sb.write(_tostring(item,self._encoding))
                elif isinstance(item,StringBuffer):
                    self._sb.write(_tostring(item._collect(),self._encoding))
                else:
                    self._sb.write(str(item))
            return ""
        else:
            return self._collect()

    def _collect(self):
        if self._canCollect():
            self.__canCollect=False
            return self._sb.getvalue()
        else:
            raise Exception("Error: This StringBuffer has been collected yet!")

#---------------------------------------------------------------------------------------------------


#codigo multiplataforma para getch()??-----------------
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            try:
                self.impl = _GetchUnix()
            except:
                self.impl=_GetchIOS()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchIOS:
    def __call__(self):
        return ""


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()
#-------------------------------------------------------------------------------


#Para usar BeautifulSoup--------------------------------------------------------------
from BeautifulSoup import BeautifulSoup # For processing HTML
from BeautifulSoup import BeautifulStoneSoup # For processing XML
from BSXPath import BSXPathEvaluator,XPathResult #Para poder usar expresiones XPATH
#-------------------------------------------------------------------------------------

#Para usar xpath con minidom (requiere py-dom-xpath)----------------------------------
if not 'xpath' in sys.modules:
     xpath=__import__('xpath')
else:
    xpath=sys.modules['xpath']
#-------------------------------------------------------------------------------------

#Para usar xmltodict----------------------------------
if not 'xmltodict' in sys.modules:
     xmltodict=__import__('xmltodict')
else:
    xmltodict=sys.modules['xmltodict']
#-------------------------------------------------------------------------------------

#Soporte para codigo C via TCC------------------------------------------------
if not 'iPad' in platform.platform() and not 'iPhone' in platform.platform():
    import minimal_cc
#-----------------------------------------------------------------------------

#Para servidor web.py-----------------------------------------------
if not 'web' in sys.modules:
     web=__import__('web')
else:
    web=sys.modules['web']
web.config.session_parameters.handler = 'file'
SESSION=None #objeto session global
#-------------------------------------------------------------------
class Application(web.application): 
  def run(self, port=8080, *middleware): 
      func = self.wsgifunc(*middleware) 
      return web.httpserver.runsimple(func, ('0.0.0.0', port)) 
#--------------------------------------------------------------------

#Contiene los nombres de las clases declaradas como final class...--------
__sealed__=[]
#-------------------------------------------------------------------------

#Base de las clases de minimal------------------------
class MiniMetaClass(type):
    #Necesario para permitir control de tipos en campos estaticos
    pyStaticTypeConstraints={}
    def __setattr2__(self, name, value):
        if MiniMetaClass.pyStaticTypeConstraints and name in MiniMetaClass.pyStaticTypeConstraints:
            if value and type(value)!=MiniMetaClass.pyStaticTypeConstraints[name]:
                raise Exception('Error de tipo: El campo estatico "%s" debe ser de tipo "%s" y se ha asignado un valor de tipo "%s"'%(name,MiniMetaClass.pyStaticTypeConstraints[name],type(value)))
        super(MiniMetaClass,self).__setattr__( name, value)
    def __setattr__(self, name, value):
        if MiniMetaClass.pyStaticTypeConstraints and name in MiniMetaClass.pyStaticTypeConstraints:
            #print 'COMPROBANDO TIPO DE CAMPO'
            prts=MiniMetaClass.pyStaticTypeConstraints[name]
            try:
                _checkType(value,*prts)
            except Exception:
                print 'Error asignando campo estatico "%s"'%name
                print(sys.exc_info()[1])
        super(MiniMetaClass,self).__setattr__( name, value)
    def __new__(meta, name, bases, dct):
        global __sealed__
        for base in bases:
           #print 'mirando base: %s' % base.__name__
           if base.__name__ in __sealed__:
               raise Exception('Error: la clase "%s" esta sellada y no se puede heredar de ella'%base.__name__)
        return super(MiniMetaClass, meta).__new__(meta, name, bases, dct)
    def __init__(cls, name, bases, dct):
        super(MiniMetaClass, cls).__init__(name, bases, dct)
#debe tener definidos todos los metodos magicos para operadores y accesores
#con la idea de permitir operadores en las clases
#tambien getattr y setattr y callable
class MiniObject(object):   
    __metaclass__ = MiniMetaClass
    def __init__(self,**kw):
        if not hasattr(self,"pyTypeConstraints"):
            self.pyTypeConstraints={}
        #self.init() #mejor aqui????
        for item in kw:
            setattr(self,item,kw[item])
            #Parche para inicializar campos private
            tmp="_" + self.__class__.__name__ + "__" + item
            if tmp in self.__dict__:
                setattr(self,tmp,kw[item])
            #fin parche   
        #Llamada al metodo que hace de falso constructor
        self.init()
        #Ponemos los tipos estaticos si estan definidos
        if self.pyTypeConstraints:
            MiniObject.__metaclass__.pyStaticTypeConstraints.update(self.pyTypeConstraints)
    def init(self):
        pass
    #Handles "missing" attributes
    def __getattr__(self,name): 
       return self.missing(name)
    def missing(self,name):
        raise Exception('Error: El campo "%s" no esta definido en la clase "%s"'%(name,self))
    #Type control if set
    def __setattr2__(self,name,value): 
        if not hasattr(self,'pyTypeConstraints'):
            self.__dict__['pyTypeConstraints']={}
        if self.pyTypeConstraints and name in self.pyTypeConstraints:
            if value and type(value)!= self.pyTypeConstraints[name]: #Si es None, no hacemos nada
                raise Exception('Error de tipo: El campo "%s" de la clase "%s" debe ser de tipo "%s" y se ha asignado un valor de tipo "%s"'%(name,type(self),self.pyTypeConstraints[name],type(value)))
        super(MiniObject,self).__setattr__(name, value)#.__dict__[name]=value
    #Type control if set
    def __setattr__(self,name,value): 
        if not hasattr(self,'pyTypeConstraints'):
            self.__dict__['pyTypeConstraints']={}
        if self.pyTypeConstraints and name in self.pyTypeConstraints:
            #print 'COMPROBANDO TIPO DE CAMPO'
            prts=self.pyTypeConstraints[name]
            try:
                _checkType(value,*prts)
            except Exception:
                print 'Error asignando campo "%s"'%name
                print(sys.exc_info()[1])
        super(MiniObject,self).__setattr__(name, value)#.__dict__[name]=value

def _checkType(item,_type,key=None,val=None):
    #print "TYPE ITEM: %s" %repr(type(item))
    #print "_TYPE: %s" %repr(_type)
    #print repr(type(item))==repr(_type)
    if type(item) not in [list,dict]:
        if _isclass(item) and isinstance(item,_type.__class__):#Mas seguro que issubclass()
            return item
        elif  type(item)==_type :
            return item
        else:
            raise Exception('Error de tipo: Se requiere que "%s" tenga como tipo "%s" y tiene "%s"'%(item,_type,type(item)))
    elif repr(type(item))==repr(type([])) and key!=None:
        for el in item:
            if type(el)!=key:
                raise Exception('Error de tipo: Se requiere que "%s" tenga como tipo "%s" y tiene "%s"'%(el,key,type(el)))
        return  item
    elif repr(type(item))==repr(type({}))  and key!=None and val!=None:
        #print "ITEMS: %s"%item.items()
        for el in item.items():
            k,v=el #;print "k: %s"%k;print "v: %s"%v
            if type(k)!=key:
                raise Exception('Error de tipo: Se requiere que "%s" tenga como tipo "%s" y tiene "%s"'%(k,key,type(k)))
            if type(v)!=val:
                raise Exception('Error de tipo: Se requiere que "%s" tenga como tipo "%s" y tiene "%s"'%(v,val,type(v)))
        return  item
    raise Exception('Error de tipo: Se requiere que "%s" tenga como tipo "%s" y tiene "%s"'%(item,_type,type(item)))

def ireduce(func, iterable, init=None): #??
    if init is None:
        iterable = iter(iterable)
        curr = iterable.next()
    else:
        curr = init
    for x in iterable:
        curr = func(curr, x)
        yield curr

def weave(*iterables):
    "Intersperse several iterables, until all are exhausted"
    iterables = map(iter, iterables)
    while iterables:
        for i, it in enumerate(iterables):
            try:
                yield it.next()
            except StopIteration:
                del iterables[i]

def tramp(gen, *args, **kwargs):
    g = gen(*args, **kwargs)
    while isinstance(g, types.GeneratorType):
        g=g.next()
    return g

def copy_func(f, name=None):
    return types.FunctionType(f.func_code, f.func_globals, name or f.func_name,f.func_defaults, f.func_closure)

def _check_py_bases(bases):
    for item in bases:
        if not inspect.isclass(item):
            raise Exception('Error: el tipo "%s" no se corresponde con una clase Python valida'%item)


def _get_files(patlist,srclist):
    all=[]
    filter=[]
    for item in srclist:
        if os.path.isfile(item):
            all.append(item)
        elif os.path.isdir(item):
            for root,dirs,files in os.walk(item):
                all+=[root + '/' + i for i in files]
        else:
            raise Exception('Error: debe ser un archivo o directorio')
    #filtrar ahora los que nos interesan
    for pat in patlist:
        filter+=fnmatch.filter(all,pat)
    return filter
     
    
def _get_directories(srclist):
    all=[]
    for item in srclist:
        if os.path.isdir(item):
            for root,dirs,files in os.walk(item):
                all.append(root)
                all+=dirs
        else:
            raise Exception('Error: debe ser un directorio')
    return all


def _itermix(*iters):
    return list(weave(*iters));

def _trampoline(gen,*args,**kwargs):
    return tramp(gen,*args,**kwargs);

class TailRecurseException:
  def __init__(self, args, kwargs):
    self.args = args
    self.kwargs = kwargs

def tail_call_optimized(g):
  """
  This function decorates a function with tail call
  optimization. It does this by throwing an exception
  if it is it's own grandparent, and catching such
  exceptions to fake the tail call optimization.
  
  This function fails if the decorated
  function recurses in a non-tail context.
  """
  def func(*args, **kwargs):
    f = sys._getframe()
    if f.f_back and f.f_back.f_back \
        and f.f_back.f_back.f_code == f.f_code:
      raise TailRecurseException(args, kwargs)
    else:
      while 1:
        try:
          return g(*args, **kwargs)
        except TailRecurseException, e:
          args = e.args
          kwargs = e.kwargs
  func.__doc__ = g.__doc__
  return func
  
class curry(object): #en js es .bind()
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs
        return self.fun(*(self.pending + args), **kw)


class closure(object): #??
    def __init__(self, fun, **kwargs):
        self.fun = fun
        self.kwargs = kwargs
        for item in kwargs:
           setattr(self,item,kwargs[item])

    def __setattr__(self,attr,value):
        object.__setattr__(self,attr,value)
        if hasattr(self,"kwargs") and attr!="kwargs":
            self.kwargs[attr]=value

    def __call__(self, **kwargs):
        #actualizar las variables pasadas
        kw=None
        for item in kwargs:
            if item in self.kwargs:
               self.kwargs[item]=kwargs[item]
               setattr(self,item,kwargs[item]) 
        kw=copy.deepcopy(self.kwargs)
        kw.update(kwargs)
        if kw!={}:
            return self.fun(**kw)
        else:
            return self.fun()



class compose(object):
    def __init__(self, funs):
        self.funs = list(funs)
        self.funs.reverse()
        
    def __call__(self, *args):
        t=args
        for f in self.funs:
            if type(t) in [list,tuple]:
                t=f(*t)
            else:
                t=f(t)
        return t
            

def _fcopy(f):
    if isinstance(f,(curry,compose,closure)):
        return copy.deepcopy(f)
    else:
        return copy_func(f)


def _decorate(f,**kwargs):
    for item in kwargs.keys():
        setattr(f, item , kwargs[item])
    return f


def _getSystem():
    #return sys.platform
    return platform.platform()

def _cmdline(start=2):
    return sys.argv[start:]

# def _print(x,encoding='ascii'):
    # if x==None:
        # print 'null'
    # elif x==True:
        # print 'true'
    # elif x==False:
        # print 'false'
    # elif x in [0,0L,0.0]:
        # print x
    # else:
        # #Si encoding es ascii, intentamos un toUnicode
        # print 'encoding en _print: %s' % encoding
        # print 'type en _print: %s' % type(x)
        # if encoding=='ascii':
            # print _toUnicode(x,encoding=encoding)
        # else:
            # print x.encode(encoding=encoding,errors='replace')


def _profilepy(code):
    return cProfile.run(code)

def _pause(ms):
    time.sleep(ms)


#Funciones para consola de windows

def _setWinConsoleCodePage(codepage):
    if os.name == 'nt':
        res=ctypes.windll.kernel32.SetConsoleCP(_toint(codepage))
        res=ctypes.windll.kernel32.SetConsoleOutputCP(_toint(codepage))


def _print(x,encoding='ascii',redirected=None):
    #print "type(x) en print: %s"%type(x) 
    if redirected!=None:
        print >> redirected , x
        return
    if x==None:
        print 'null'
    elif type(x)==bool:
        #print 'Imprimiendo un bool'
        if x==True:
            print 'true'
        else:
            print 'false'
    elif x in [0,0L,0.0]:
        print str(x)
    else:
        #print 'encoding en _print: %s' % encoding
        #print 'type en _print: %s' % type(x)
        if type(x)==type(''): #str
            try:
                print x.decode(encoding=encoding,errors='replace')
            except:
                print x
        elif type(x)==unicode:#unicode
            print x.encode(encoding=encoding,errors='replace')
        else: #io.TextIOWrapper
            #print 'type(x): %s' %repr(x)
            print x

def _input(x="",encoding='ascii',endline='\n'):
   #Todo lo entrado se convierte a unicode
   #esto no vale, sigue leyendo en el encoding por defecto
   #return raw_input(x).decode(encoding)
   #Hay que OBLIGAR a que lea en el encoding pasado
   #Y la consola debe tener un encoding adecuado
   old=sys.__stdin__
   reader=codecs.getreader(encoding)
   sys.__stdin__=reader(sys.__stdin__)
   read=""
   sys.stdout.write(x)
   while True:
        l=sys.__stdin__.read(1)
        read+=l
        if l==endline: break
   sys.__stdin__=old
   return read.strip()

#funciones para obtener stdin,stdout y stderr-----------------------------
def _getStdin():
    return sys.__stdin__

def _getStdout():
    return sys.__stdout__

def _getStderr():
    return sys.__stderr__
#--------------------------------------------------------------------------

#getchar multiplataforma(verlo: en Mac no funciona)
def _getchar():
    return getch()
   
def _eval(x):
   return eval(x)
   
def _exec(x):
   exec x
   return 1

def _del(x):
    del x
    return 1

def _type(x):
    return type(x)

def _toUnicode(s,encoding='ascii'): #Pruebas
    #Se pase lo que se pase, la salida TIENE que ser unicode
    U=""
    if type(s)==type(''):
        U=s.decode(encoding=encoding,errors='replace') #.encode(encoding=encoding,errors='replace')
    elif type(s)==type(u''):
        U=unicode(s.encode(encoding=encoding,errors='replace') ,encoding=encoding,errors='replace')
    else:
        U=str(s).decode(encoding=encoding,errors='replace')
    return U

def _tostring(x,encoding='ascii'):
    return _toUnicode(x,encoding)

#Version de format mas pobre que no usa la de Python(porque da problemas si en la cadena hay {})
#pero es mas homogenea con el resto de lenguajes(REVISAR)
def _format(cad,lst):
    n= cad
    #print "lst: %s" % lst
    #print "cad: " + cad
    for i in range(len(lst)):
       p='\{' + str(i) + '\}'
       #print 'VALOR DE P: %s' % p
       #n= re.sub(re.compile(p),str(lst[i]),n)
       n= re.sub(re.compile(p),_tostring(lst[i]),n)
       #print "valor de n: " + n
    return n
   
def _mod(x,y):
    return int(x%y)

def _divmod(x,y):
    return divmod(x,y)

def _floor(x):
    return math.floor(x)

def _ceil(x):
    return math.ceil(x)

def _fact(x):
    return math.factorial(x)

def _sqrt(x):
    return math.sqrt(x)

def _exp(x):
    return math.exp(x)

def _ln(x):
    return math.log(x,math.e)

def _log(x,base=None):
    if base!=None:
        return math.log(x,base)
    else:
        return math.log10(x)

def _sin(x):
    return math.sin(x)

def _asin(x):
    return math.asin(x)

def _cos(x):
    return math.cos(x)

def _acos(x):
    return math.acos(x)

def _tan(x):
    return math.tan(x)

def _atan(x):
    return math.atan(x)

def _append(x,y):
    y.append(x)

def _append2(x,y):
    y.append(x)
    return y

def _apply(f,*args):
    return f(args)

def _reverse(x):
    #x.reverse()
    return list(reversed(x))

def _cons(x,y):
    return [x]+y

def _car(x):
    return x[0]

def _last(x):
    return x[-1]

def _butlast(x):
    return x[0:-1]

def _cdr(x):
    return x[1:]

def _index(el,lst):
    return lst.index(el)

def _curry(f,*args,**kwargs):
    return curry(f,*args,**kwargs)

def _closure(f,*args,**kwargs):
    return closure(f,*args,**kwargs)
    
def _compose(*funs):
    return compose(funs)

#Alternativa con funciones para todas las formas funcionales del lenguaje--------
def _slice(s,b,e=None):
    if e:
        return s[b::e]
    else:
        return s[b::]

def _foreach(seq,fun):
    for i in range(len(seq)):
        seq[i]=func(seq[i])

#RESTO PENDIENTE!!!!!
#------------------------------------------------------------------------------------

def _sublist(s,b,e=None):
    if e:
        return s[b:e]
    else:
        return s[b:]

def _insert(lst,idx,obj):
    lst.insert(idx,obj)
    return lst

#Soporte para transacciones-----------------------------------------------------
def Memento(obj, deep=False):
   state = (copy.copy, copy.deepcopy)[bool(deep)](obj.__dict__)
   def Restore():
      obj.__dict__.clear()
      obj.__dict__.update(state)
   return Restore

class Transaction:
   """A transaction guard. This is realy just 
      syntactic suggar arount a memento closure.
   """
   deep = False
   def __init__(self, *targets):
      self.targets = targets
      self.Commit()
   def Commit(self):
      self.states = [Memento(target, self.deep) for target in self.targets]
   def Rollback(self):
      for state in self.states:
         state()

class transactional(object):
   """Adds transactional semantics to methods. Methods decorated 
      with @transactional will rollback to entry state upon exceptions.
   """
   def __init__(self, method):
      self.method = method
   def __get__(self, obj, T):
      def transaction(*args, **kwargs):
         state = Memento(obj)
         try:
            return self.method(obj, *args, **kwargs)
         except:
            state()
            raise
      return transaction

def _transaction(*objs):
    return Transaction(*objs)
def _rollback(*transactions):
    for t in transactions:
        t.Rollback()
    return 1
#-----------------------------------------------------------------------------------------

#Soporte para synchronized-----------------------------------------------------------------
#(decorador @synchronized)
def synchronized(func):
    func.__lock__ = threading.Lock()
    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)
    return synced_func
#-------------------------------------------------------------------------------------------

#Funciones Python imprescindibles
_list=list
_split=string.split
_strip=string.strip
_join=string.join
_size=len
_abs=abs
_toint=int #long??
_tofloat=float
_system=os.system
_copy=copy.deepcopy
_replace=string.replace #_replace(old,new[,max_replaces])
_find=string.find #find(str, beg=0, end=len(string))

def _strinsert(cad,new,start,end):
    cad[start:end]=new
    return cad

#Utilidades para diccionarios
def _keys(dic):
    return dic.keys()

def _values(dic):
    return dic.values()

def _pairs(dic):
    return [list(el) for el in dic.items()]


#Expresiones regulares
def _rematch(exp,cad,flags=0):
    return re.findall(exp,cad,flags)

def _rereplace(cad,old,new,flags=0):
    return re.sub(old,new,cad,flags)

def _resplit(cad,exp,flags=0):
    return re.split(exp,cad,flags)

def _regroups(exp,cad,n=-1,flags=0):
    if n==-1:
        return [[x.group(),x.start(),x.end()] for x in re.finditer(exp,cad,flags=0)]
    else:
        return [[x.group(n),x.start(n),x.end(n)] for x in re.finditer(exp,cad,flags=0)]



def _isclass(el):
    return type(el) not in [str,unicode,int,float,long,tuple,list,dict]

def _count(el,seq): 
    return seq.count(el)

def _histogram(seq):
    hist = {};
    def f(a):
        if a in hist:
            hist[a]+=1
        else:
            hist[a]=1
    map(f,seq)
    return hist;

def _indexof(el,seq): 
    return seq.index(el)

#Cambia el encoding por defecto
#Peligroso????
def _setencoding(encoding):
    reload(sys)
    sys.setdefaultencoding(encoding)
    return encoding

def _open(path,mode='r',encoding='ascii'):
    if not 'b' in mode:
        return io.open(path,mode,encoding=encoding)
    else:
        return open(path,mode)

def _close(fhandle):
    fhandle.close()

def _readf(f,encoding='ascii'): 
    #io.open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True)
    return io.open(f,'r',encoding=encoding).read()

def _readflines(f,encoding='ascii'): 
    return io.open(f,'r',encoding=encoding).readlines()

#Escritura en archivos de texto que acepta un encoding
def _writef(fl,_bytes,encoding='ascii',append=1): 
    f=None
    if append==0:
        f= io.open(fl,'w',encoding=encoding)
    else:
        f= io.open(fl,'a',encoding=encoding)
    b=_toUnicode(_bytes,encoding)
    f.write(b)
    f.close()
    return 1

def _writeflines(fl,lines,encoding='ascii',append=1): 
    f=None
    if append==0:
        f= io.open(fl,'w',encoding=encoding)
    else:
        f= io.open(fl,'a',encoding=encoding)
    for line in lines:
        f.write(line.encode(encoding).decode(encoding))
    f.close()
    return 1

def _writeflines_backup(fl,lines,encoding='ascii',append=1):
    f=None
    if append==0:
        if encoding=='ascii':
            f=open(fl,"w")
            for line in lines:
                f.write(line + '\n')
        else:
            f= io.open(fl,'w',encoding=encoding)
            for line in lines:
                f.write(unicode(line + '\n'))
    else:
        if encoding=='ascii':
            f=open(fl,"a")
            for line in lines:
                f.write(line + '\n')
        else:
            f= io.open(fl,'a',encoding=encoding)
            for line in lines:
                f.write(unicode(line + '\n'))

    f.close()
    return 1
#Funciones de utilidad del modulo itertools---------
_chain=itertools.chain
#_zip=itertools.izip
def _zip(*seqs):
    return [list(x) for x in itertools.izip(*seqs)]
def _enumerate(seq):
    return [list(x) for x in list(enumerate(seq))]
def _cartessian(*seqs):
    return [list(x) for x in list(itertools.product(*seqs))]
def _combinations(seq,n):
    return [list(x) for x in list(itertools.combinations(seq,n))]
def _combinations_with_r(seq,n):
    return [list(x) for x in list(itertools.combinations_with_replacement(seq,n))]
def _permutations(seq,n):
    return [list(x) for x in list(itertools.permutations(seq,n))]
def _starmap(f,seq):
    for item in seq:
        yield f(*item)
def _cycle(seq):
    i=0
    while i<len(seq)+1:
        if i==len(seq): i=0
        yield seq[i]
        i+=1

#xml-------------------------------------------------------------------
def _xmltod(xml):
    return xmltodict.parse(xml)

def _dtoxml(dict):
    return xmltodict.unparse(dict)

def _xmlstr(_xml):
    if _xml.nodeType == 4: #CDATA
        return _xml.data
    elif not isinstance(_xml,xml.dom.minidom.Attr) and hasattr(_xml,'toxml'):
        return _xml.toxml()
    elif hasattr(_xml,'value'):
        return _xml.value
    else:
        return ''
#Condicional porque no todos los sistemas tienen lxml
#Ojo: La transformacion DEBE producir xhtml VALIDO, o no funciona bien
try:
    import lxml.etree as ET

    def _applyXSLT(_xml,xsl):
        #dom = ET.parse(xml)
        #xslt = ET.parse(xsl)
        dom = ET.XML(_xml)
        xslt = ET.XML(xsl)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        return ET.tostring(newdom, pretty_print=True)
except:
    def _applyXSLT(xml,xsl):
        return xml
#----------------------------------------------------------------------

#Coger contenido de una url---------------------------------------------
def _geturl(url): 
    return getPathText(url)
#-----------------------------------------------------------------------

#Llamadas asincronas-----------------------------------------------------------
def asyncall(fn,callb,*args,**kwargs):#firma de callb: callb(future)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future=executor.submit(fn,*args,**kwargs)
        for future in concurrent.futures.as_completed([future]):
            data = future.result()
    retval=callb(data)
    return retval

def asynfun(fn,*args,**kwargs):
    executor=concurrent.futures.ThreadPoolExecutor(max_workers=3)
    future=executor.submit(fn,*args,**kwargs)
    return future
#-------------------------------------------------------------------------------

#----------------------------------------------------------------
#Funcion que evalua una S-expresion
def _scheme(sexpr):
   x=lispy.parse(sexpr.strip())
   if x is lispy.eof_object: return ''
   val=lispy.eval(x)
   return lispy.to_string(val) 

def _lisp(sexpr):
    if 'hy' in sys.modules:
        f=open('hytemp.hy','w')
        f.write(sexpr.strip())
        f.close()
        sys.modules['hy'].cmdline.run_file('hytemp.hy')
        return 1
    else:
        return 0


def _lispModule(mod_name,sexpr):
    #global HY_AVAILABLE
    #if HY_AVAILABLE==0: raise Exception('Error: el modulo Hy(lisp) no esta disponible en la plataforma "%s"'%sys.platform)
    if 'hy' in sys.modules:
        f=open(mod_name + '.hy','w')
        f.write(sexpr.strip())
        f.close()
        sys.modules[mod_name]=__import__ (mod_name)
        return 1
    else:
        return 0

#Ojo, retrasa la carga del programa(1M de codigo)
def _clojure(sexpr):
    if 'clojure' in sys.modules:
        f=open('cljtemp.clj','w')
        f.write(sexpr.strip())
        f.close()
        return sys.modules['clojure'].main.hack_for_minimal('cljtemp.clj') 
    return None


#Soporte para codigo C via TCC------------------------------------------
def _C(code,target,*dlls):
    dll=minimal_cc.C(code,target,*dlls)
    return dll

def _getC(dll,fun):
    return minimal_cc.getC(dll,fun)
#------------------------------------------------------------------------

#Soporte para gui Tk via formbox(a demanda)-----------
if TK_AVAILABLE==1:
    def _formbox(app_dict,label_list,label_types,data_dict,cancellable,noclose,menu_labels,menu_dict):
        return mini_tkbasic.formBox(app_dict,label_list,label_types,data_dict,cancellable,noclose,menu_labels,menu_dict)
    # def _message(title,message,type,icon):
       # return mini_tkbasic.messageBox(title,message,type,icon)
    # def _color(title):
       # return mini_tkbasic.getTkColor(title)
    # def _file(title,mode):
        # return mini_tkbasic.getTkFile(title,mode)
    # def _files(title):
        # return mini_tkbasic.getTkFiles(title)
    # def _dir(title):
        #return mini_tkbasic.getTkDir(title)
    def _getFormItemValue(form,item):
        return mini_tkbasic.getFormItemValue(form,item)
    def _setFormItemValue(form,item,value):
        return mini_tkbasic.setFormItemValue(form,item,value)
    def _getFormItem(form,item):
        return mini_tkbasic.getFormItem(form,item)
    def _callFormItem(form,item_name,func_name,args_list):
        return mini_tkbasic.callFormItem(form,item_name,func_name,args_list)
    def _setFormItemFont(form,item_name,font_descriptor):
        return mini_tkbasic.setFormItemFont(form,item_name,font_descriptor)
    def _tcl(code):
        tcl=Tkinter.Tcl()
        return tcl.eval(code)
else:
    def _formbox(*args):
        return {}
    # def _message(*args):
        # return 0
    # def _color(*args):
        # return 0
    # def _file(*args):
        # return 0
    # def _files(*args):
        # return 0
    # def _dir(*args):
        # return 0
    def _getFormItemValue(*args):
        return 0
    def _setFormItemValue(*args):
        return 0
    def _getFormItem(*args):
        return 0
    def _callFormItem(*args):
        return 0
    def _setFormItemFont(*args):
        return 0
    def _tcl(*args):
        return 0
#--------------------------------------------------------

#Soporte JSON--------------------------------------------
def _tojson(elem):
    return json.dumps(elem)

def _fromjson(cad):
    return json.loads(cad)
#-------------------------------------------------------

#Funciones de soporte para sockets TCP cliente y servidor
def _socket_server(host,port,thread_func,maxconns=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host,port))
    except:
        raise Exception("Socket error: Unable to connect to %s : %s"%(host,port))
    s.listen(maxconns)
    while 1:
        conn,addr=s.accept()
        thread.start_new_thread(thread_func ,(conn,))
    s.close()


def _socket_client(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host,port))
    except:
        raise Exception("Socket error: Unable to connect to %s : %s"%(host,port))
    return s


#Funciones para servidor web--------------------------------------------------------------------
_urlencode=urllib.quote_plus
_urldecode=urllib.unquote_plus

def _setHeader(name,value):
    web.header(name,value)
    return 1

def _webRedirect(url):
    web.redirect(url)
    return 1

def _getWebVar(name,multiple=0):
    if multiple==0:
        return getattr(web.input(),name)
    else:
        t=eval('web.input(' + name + '=[])')
        return eval('t.' + name)

def _getWebEnviron():
    return web.ctx.env

def _getWebPath():
    return web.ctx.path

def _getWebFile(name):
    _f=eval('web.input(' + name + '={})')
    return [eval('_f["' + name + '"].filename'),eval('_f["' + name + '"].value')]

def _killSession():
    global SESSION
    if SESSION!=None:
        SESSION.kill()
        SESSION=None

def _setSessionVar(name,value):
    global SESSION
    if SESSION!=None:
        SESSION[name]=value
        return value
    else:
        raise Exception("Error: la sesion no existe")

def _getSessionVar(name):
    global SESSION
    if SESSION!=None:
        return SESSION[name]
    else:
        raise Exception("Error: la sesion no existe")

def _setCookie(name,value,expires):
    web.setcookie(name,value,int(expires))
    return 1

def _getCookie(name):
    return web.cookies().get(name) or ''

#Funciones envoltorio sobre el modulo matrix-------------------------------------------------------
def _toMatrix(elem):
    if type(elem)==type({}):
        mtx=matrix.Matrix()
        mtx.loadFromDict(elem)
        return mtx
    elif type(elem)==type([]):
        return matrix.Matrix(elem)
    else:
        raise Exception("Error: solo las listas de listas y los diccionarios se pueden transformar en una Matrix")


def _getList(mtx):
    if not isinstance(mtx,matrix.Matrix): raise Exception("Error: '%s' no es una instancia de una Matrix"%mtx)
    return mtx.getList()

def _getRow(mtx,row):
    if not isinstance(mtx,matrix.Matrix): raise Exception("Error:  '%s' no es una instancia de una Matrix"%mtx)
    return mtx.getRow(row)

def _getCol(mtx,col):
    if not isinstance(mtx,matrix.Matrix): raise Exception("Error:  '%s' no es una instancia de una Matrix"%mtx)
    return mtx.getCol(col)

def _getDimensions(mtx):
    if not isinstance(mtx,matrix.Matrix): raise Exception("Error:  '%s' no es una instancia de una Matrix"%mtx)
    return mtx.getDimensions()

def _invert(mtx):
    if not isinstance(mtx,matrix.Matrix): raise Exception("Error:  '%s' no es una instancia de una Matrix"%mtx)
    return mtx.invert()

def _mcopy(mtx):
    if not isinstance(mtx,matrix.Matrix): raise Exception("Error:  '%s' no es una instancia de una Matrix"%mtx)
    return mtx.copy()

def _toDict(mtx,colnames=[]):
    if not isinstance(mtx,matrix.Matrix): raise Exception("Error:  '%s' no es una instancia de una Matrix"%mtx)
    return mtx.toDict(colnames)

def _appendRow(mtx,row):
    if not isinstance(mtx,matrix.Matrix): raise Exception("Error:  '%s' no es una instancia de una Matrix"%mtx)
    mtx.appendRow(row)
    return mtx

def _insertRow(mtx,row,pos):
    if not isinstance(mtx,matrix.Matrix): raise Exception("Error:  '%s' no es una instancia de una Matrix"%mtx)
    mtx.insertRow(row,pos)
    return mtx

def _appendCol(mtx,col):
    if not isinstance(mtx,matrix.Matrix): raise Exception("Error:  '%s' no es una instancia de una Matrix"%mtx)
    mtx.appendCol(col)
    return mtx

def _insertCol(mtx,col,pos):
    if not isinstance(mtx,matrix.Matrix): raise Exception("Error:  '%s' no es una instancia de una Matrix"%mtx)
    mtx.insertCol(col,pos)
    return mtx

def _queryADO(constr,query,encoding='latin-1'):
    if 'win32' in sys.platform:
        return minimal_ado.minimalQuery(constr,query,encoding)
    else:
        return []

def _getDBADOinfo(constr):#????????
    if 'win32' in sys.platform:
        info=[]
        catalog=minimal_ado.DbInfo()
        conn=win32com.client.Dispatch("ADODB.Connection")
        conn.Open(constr)
        catalog.setConnection(conn)
        return catalog.getDbTables()
        
    else:
        return []

def genRange(start,end,step=1):
    if type(step) in [type(0),type(0L)]:
        return range(start,end,step)
    else:
        resul=[]
        while start<end :
            resul.append(start)
            start+=step
        return resul


def doSort(x,func,reverse=0):
    try:
        # print 'al entrar: %s' % repr(list(x) )
        # print 'ordenada: %s' %sorted(list(x),key=func,reverse=reverse)
        # print sorted(x,key=func,reverse=reverse)
        return sorted(list(x),key=func,reverse=reverse)
    except:
        raise Exception('Error: "%s" no es una lista' %str(x))


# def doFormat(template,plist):
    # if type(template) in [type(''),type(u'')]:
        # #return template%tuple(plist)
        # if type(plist)==type({}):
            # return template.format(**plist)
        # else:
            # return template.format(*plist)
    # else:
        # raise Exception('Error: "%s" no es una cadena' %str(template))

def doFormat(template,plist):
    return _format(template,plist)

def doSerialize(id,dest=''):
    if dest: #and os.path.exists(dest) and os.path.isfile(dest):
        pickle.dump(id,open(dest,'wb'))
        return 1
    else:
        return pickle.dumps(id)


def doDeserialize(dest):
    if os.path.exists(dest) and os.path.isfile(dest):
        return pickle.load(open(dest,'rb'))
    else:
        return pickle.loads(dest)

def doAddition(elem1,elem2):
    '''El operador + esta sobrecargado, reglas:
       si los dos son numeros: sumarlos
       si los dos son cadenas, combinarlas
       numero+cadena: cad + str(num)
       lista+lista: combinarlas
       lista+ cualquiera o cualquiera + lista: meter cualquiera en lista
       dict + dict: combinarlos
       al principio o al final
    '''
    #print 'elem1:%s' %elem1,'elem2:%s' %elem2
    if type(elem1) in [type(0),type(0L),type(0.0)] and type(elem1) in [type(0),type(0L),type(0.0)]:
        return elem1 + elem2
    elif type(elem1) in [type(0),type(0L),type(0.0)] and type(elem2) in [type(''),type(u'')]:
        return str(elem1) + _toUnicode(elem2)
    elif type(elem2) in [type(0),type(0L),type(0.0)] and type(elem1) in [type(''),type(u'')]:
        return _toUnicode(elem1) + str(elem2)
    elif type(elem2) in [type(''),type(u'')] and type(elem1) in [type(''),type(u'')]:
        return _toUnicode(elem1) + _toUnicode(elem2)
    elif type(elem2)==type([]) and type(elem1)==type([]):
        return elem1 + elem2
    elif type(elem2)==type([]) and type(elem1)!=type([]):
        elem2.append(elem1)
        return elem2
    elif type(elem1)==type([]) and type(elem2)!=type([]):
        elem1.append(elem2)
        return elem1
    elif type(elem2)==type({}) and type(elem1)==type({}):
        elem1.update(elem2)
        return elem1
    else:#cualquier otra combinacion es un error, si no esta definido como operador de una clase
        try:
          return elem1 + elem2
        except:
            raise Exception("Error: El operador '+' no esta definido para estos dos tipos de operando:\n  '%s  de tipo: %s'\n y\n  '%s  de tipo: %s'\n"%(elem1,type(elem1),elem2,type(elem2)))


def doGroup(seqs,func):
    res={}
    for s in seqs:
        if func(s) in res:
            res[func(s)].append(s)
        else:
            res[func(s)]=[s]
    return res


def doCopy(files,dest,dirs=0):
    if type(files)==type([]):
        if dirs==0:
            for f in files:
                if os.path.exists(f) and os.path.isfile(f):
                    #dest aqui debe ser un directorio
                    shutil.copy2(f,dest + '/' + os.path.basename(f))
        else:
            for f in files:
                if os.path.exists(f) and os.path.isdir(f):
                    shutil.copytree(f,dest)
    else:
        if dirs==0:
            if os.path.exists(files) and os.path.isfile(files):
                #Crear dest si no existe
                if not os.path.exists(dest):
                    open(dest,'w').close()
                    shutil.copy2(files,dest)
                else:
                    shutil.copy2(files,dest + '/' + os.path.basename(files))
        else:
            if os.path.exists(files) and os.path.isdir(files):
                shutil.copytree(files,dest)


def doDelete(files,dirs=0):
    if type(files)==type([]):
        if dirs==0:
            for f in files:
                if os.path.exists(f) and os.path.isfile(f):
                    shutil.rmtree(f)
        else:
            for f in files:
                if os.path.exists(f) and os.path.isdir(f):
                    shutil.rmtree(f)
    else:
        if dirs==0:
            if os.path.exists(files) and os.path.isfile(files):
                shutil.rmtree(files)
        else:
            if os.path.exists(files) and os.path.isdir(files):
                shutil.rmtree(files)


#Funcion de utilidad que lee un archivo de texto o una url
#Si getlines es 1, se devuelve como lista de lineas
def getPathText(path,getlines=0):
    if path.lower().find('http://')==0:
        if getlines==0:
            #print 'Descargando url: %s' % path
            return urllib.urlopen(path).read()
        else:
            return urllib.urlopen(path).read().split('\r\n') 
    else:
        if getlines==0:
            if os.path.exists(path) and os.path.isfile(path):
                return open(path,'r').read()
            else:
                return path
        else:
            if os.path.exists(path) and os.path.isfile(path):
                return open(path,'r').readlines()
            else:
                return path


def getPathTextBinary(path):
    if path.lower().find('http://')==0:
        return urllib.urlopen(path).read()
    else:
        if os.path.exists(path) and os.path.isfile(path):
            return open(path,'rb').read()
        else:
            return path


def getBinaryChunk(path,start,end):
    if os.path.exists(path) and os.path.isfile(path):
        f=open(path,'rb')
        f.seek(start)
        if start!=0:
            return f.read(end-start)
        else:
            return f.read(start)
    else:
        return 0


def appendBinaryChunk(path,bytes):
    if os.path.exists(path) and os.path.isfile(path):
        f=open(path,'ab+')
        f.write(bytes)
        return len(bytes)



#Funciones de soporte para tipos-lista
def checkInstanceType(exp_list,template_list,kind):
    global __typedefs,__classes
    #print 'Comprobando tipos:'
    if type(template_list)==type([]):
        if kind==1: #choice of vals
            for el in template_list:
                #print 'Comnprobando: %s' %el
                if exp_list==el:
                    correct=1
                    break
        else:#tipo compuesto
            for i in range(len(exp_list)):
                #print 'Comprobando: %s' %exp_list[i]
                if type(exp_list[i]) in [type(0),type(0L),type(0.0)] and not template_list[i]=='numeric':
                    raise Exception('Error comprobando tipos: se esperaba "%s" para "%s"'%(template_list[i],exp_list[i]))
                elif  exp_list[i] in __typedefs + [i[0] for i in __classes]: #Comprobar que los tipos de los IDs coinciden exactamente
                    if template_list[i]!=TYPESTAB[exp_list[i]]:
                        raise Exception('Error comprobando tipos: se esperaba "%s" para "%s"'%(template_list[i],exp_list[i]))
                elif type(exp_list[i]) in [type(''),type(u'')]and not template_list[i]=='chain':
                    raise Exception('Error comprobando tipos: se esperaba "%s" para "%s"'%(template_list[i],exp_list[i]))
    elif type(template_list) in [type(''),type(u'')]:
        if len(exp_list)!=1:
            raise Exception('Error creando instancia de tipo: Un tipo basado en lista solo pude tener un parametro')
        exp_list=exp_list[0]
        correct=0
        if kind==2: #choice of types
            choices=template_list.split('|')
            for el in choices:
                #print 'Comnprobando: %s' %el
                if type(exp_list) in [type(0),type(0L),type(0.0)] and el=='numeric':
                    correct=1
                    break
                elif exp_list in TYPESTAB:
                    if el==TYPESTAB[exp_list]:
                        correct=1
                        break
                elif type(exp_list) in [type(''),type(u'')]and el=='chain':
                    correct=1
                    break
        if correct==0:
            raise Exception('Error: "%s" no se corresponde con ninguno de los tipos alternativos "%s"'%(exp_list,choices))




def listMatchType(lst,template,kind,__tdefs):
    #print 'Entrando a ListMatchType con:'
    #Valor para diferenciar el tipo de typedef:0:compuesto,1:choice of vals,2:choice of types,3:list(array) of type(???)
    #print repr(lst)
    #print template
    #print 'kind: %s' % kind
    if kind not in [1,2] and type(lst)!=type([]):
        raise Exception('Error: "%s" no es una lista y tiene que serlo'%lst)
    #print __tdefs
    #Proceder segun kind y template
    if kind==1: #Pertenencia a la lista del tipo (trivial)
        if type(lst) in [type(''),type(u'')]:
            #print 'por el if: %s'%(lst in template)
            if lst and lst in template:
                return 1
            else:
                #Cambio serio. Permitimos que t_string funcione tb como expresion regular!!!!--------
                for t in template.split(','):
                    #print 'probando en el if %s' % t
                    try:
                        if re.match(t.strip('"'),lst):
                            return 1
                    except:
                        return 0
                #Fin cambio--------------------------------------------------------------------------
                return 0
        else:
            #Si es una lista tienen que encajar todos!
            #print 'por el else'
            if type(template) in [type(''),type(u'')]: template=template.split(',')
            cont=0
            for el in lst:
                #print 'el: %s' %el
                if not el in template:
                    #Cambio serio. Permitimos que t_string funcione tb como expresion regular!!!!--------
                    for t in template:
                        #print 'probando %s con %s' % (t.strip('"'),el)
                        try:
                            #print re.match(t.strip('"'),el)
                            if not re.match(t.strip('"'),el):
                                #print 'continuamos...'
                                continue
                            else:
                                #print 'salimos...'
                                cont+=1
                                break
                        except:
                            #print 'error en regexp!!!'
                            return 0
                    #print 'me salgo del bucle!'
                    #return 0
                    #Fin cambio--------------------------------------------------------------------------  
                else:
                    return 1
            if cont==len(lst):
                return 1
            else:
                return 0
    elif kind==0: #tipo compuesto o alias
        #Asegurarse de que template es una lista
        if type(template)!=type([]): template=template.split(',')
        #print 'template modificado:%s' % template
        if len(lst)>len(template) or len(lst)==1: #Hay que encajar toda la lista
            #print 'probando lista entera: %s'%lst
            tipo=elems=None
            if template[0] not in ['numeric','string']: ##ESTO SE HA CAMBIADO PARA LA CREACION DE TIPOS-LISTA!!
                tipo,elems=__tdefs[template[0]]
            #print 'llamada recursiva!'
            #print 'probando "%s" con "%s"'%(lst,str(elems))
            if not listMatchType(lst,elems,tipo,__tdefs):
                #print 'No encaja con nada en el if de k0'
                return 0
            #print 'Encaja con %s en el if de k0'%str(elems)
            return 1
        else:
            for i in range(len(template)):
                #print 'probando elemento: %s'%lst[i]
                if type(lst[i]) in [type(0),type(0L),type(0.0)] and template[i]=='numeric':
                    #print '"%s" encaja en numeric en k0'%lst[i]
                    continue
                if type(lst[i]) in [type(''),type(u'')] and template[i]=='chain':
                    #print '"%s" encaja en chaing en k0'%lst[i]
                    continue
                if template[i] not in ['numeric','chain']:
                    tipo,elems=__tdefs[template[i]]
                    #print 'llamada recursiva!'
                    #print 'probando "%s" con "%s" en k0'%(lst[i],str(elems))
                    if not listMatchType(lst[i],elems,tipo,__tdefs):
                        #print 'No encaja con nada en k0'
                        return 0
                    #print 'Encaja con %s en k0'%str(elems)
                else:
                    #print 'no encaja, no en k0'
                    return 0
            return 1
    elif kind==2: #Uno de varios tipos posibles. Probar TODA la lista. Si alguno coincide, verdadero
        cont= 1 if template in ['numeric','chain'] else len(template)
        #print 'CONT: %s' % cont
        #print 'lst: %s' % lst
        if cont==1: #Template NO es una lista
            #Asegurarse de que es una lista 
            if type(lst)!=type([]): lst=[lst]
            #print 'probando elemento: %s con %s'%(lst[0],template)
            if len(lst)==1 and type(lst[0]) in [type(0),type(0L),type(0.0)] and template=='numeric':
                #print '"%s" encaja en numeric en k2'%lst[0]
                return 1
            if len(lst)==1 and type(lst[0]) in [type(''),type(u'')] and template=='chain':
                #print '"%s" encaja en chain en k2'%lst[0]
                return 1
        for i in range(cont):
            #print 'probando elemento: %s con %s'%(lst[i],template[i])
            if len(lst)==1 and type(lst[0]) in [type(0),type(0L),type(0.0)] and template[i]=='numeric':
                #print '"%s" encaja en t_numeric en k2'%lst[0]
                return 1
            if len(lst)==1 and type(lst[0]) in [type(''),type(u'')] and template[i]=='chain':
                #print '"%s" encaja en t_string en k2'%lst[0]
                return 1
            if template[i] not in ['numeric','chain']:
                #print 'llamada recursiva!'
                #print 'probando "%s" con "%s" y tipo "%s"'%(lst,[template[i]],0)
                if listMatchType(lst,[template[i]],0,__tdefs):
                    #print 'Encaja via or con %s en k2'%template[i]
                    #print 'saliendo'
                    return 1 
                    

    elif kind==3: #Array de un tipo. Probar que todos los elementos tienen el mismo tipo
        tipo=None
        #print 'template aqui: %s' % template
        #Asegurarse de que template es una lista
        if type(template)!=type([]): template=template.split(',')
        if template[0] not in ['numeric','chain']:
            tipo=__tdefs[template[0]][0]
        for i in range(len(lst)):
            #print 'probando elemento: %s con %s y kind 3'%(lst[i],template[0])
            #trivial: t_numeric
            if template[0]=='numeric' and not type(lst[i]) in [type(0),type(0L),type(0.0)]:
                return 0
            #trivial: t_string
            if template[0]=='chain' and not type(lst[i]) in [type(''),type(u'')]:
                return 0
            #recursivo:
            if template[0] not in ['numeric','chain']:
                it=lst[i]
                #print 'it: %s' % it
                #print type(lst[i])
                if type(lst[i])!=type([]):
                    it=lst
                #print 'it: %s' % it
                #print 'tipo: %s' % tipo
                #Ojo, cambio para si tipo del template es 1, pasar la lista de opciones
                tplt=__tdefs[template[0]][1:] if tipo==1 else [template[0]]
                if not listMatchType(it,tplt,tipo,__tdefs):
                   return 0
                #print 'ok por ahora!'
        return 1;
    return 0



#Clase que representa a un item de groupby
class GroupItem(object):
    def __init__(self):
        self.count=0
        self.value=0 #Ojo: antes esto era None
        self.items=[]
        self.max=-float('inf')
        self.min=float('inf')
    def __repr__(self):
        return '<GroupItem-> count: %s , value: %s , items: %s , max: %s , min: %s>'%(self.count,self.value,self.items,self.max,self.min)

#Funcion para construir una tabla de diccionarios para linq-like
def groupbyTable(master,_list,limit):
  #print type(master)
  if isinstance(master,GroupItem): #A REVISAR!!!!and limit==len(_list):
     limit=0
     return
  if len(master)==0 and limit==len(_list):
     limit=0
     return
  if len(master)==0:
     for item in _list[limit]:
        if _list[limit]==_list[-1]:
           master[item]=GroupItem()
        else:
           master[item]={}
     limit+=1
  for dic in master:
     groupbyTable(master[dic],_list,limit)


def processGroupbyRows(mtx,table,indexes,attrs_list):
    #global attrs_list
    #print 'indexes: %s' %indexes
    filas=mtx.getList()
    #print 'filas: %s' % filas
    #Buscar funcion de agregado si la hay y la posicion
    func=''
    fpos=-1
    for k in attrs_list:
        if k[2]!='':
            func=k[2]
            fpos=int(k[1])
            break
    #print 'valor de func: %s' %func
    for fila in filas:
        campos=[]
        for item in indexes:
            campos.append(fila[int(item[1])])
        #print 'Campos: %s' % campos
        actual={}
        last={}
        actual=table
        #Ir obteniendo el subdiccionario de cada campo
        #si falla, salimos
        #si se completa, sumar 1
        #print 'valor de actual: %s' % actual
        actindex=0
        for item in campos: #REVISAR!!!
            if type(actual)==type({}) and actual.has_key(item):
                #print 'actual:%s' %actual
                #print 'fila: %s' %fila
                last=actual
                actual=actual[item]
                #if type(actual) in [type(0),type(0L),type(0.0)]:
                if isinstance(actual,GroupItem):
                    if func in ['','count']:
                        last[item].count+=1
                    else:
                        if len(fila)< fpos:
                            last[item].count+=1
                            last[item].value+=fila[fpos]
                            #print 'last[item].value:%s' %last[item].value
                            #Esto solo se calcula si es necesario
                            if func in ['sum','avg','std','stdp','var','varp']:
                                last[item].items.append(fila[fpos])
                            if func=='max':
                                if fila[fpos]> last[item].max:
                                   last[item].max=fila[fpos]
                            if func=='min':
                                if fila[fpos]< last[item].min:
                                   last[item].min=fila[fpos]                                   
                        else:
                            last[item].count+=1
                            last[item].value+=fila[-1] if type(fila[-1]) in [type(0),type(0.0),type(0L)] else 0
                            #Esto solo se calcula si es necesario
                            if func in ['sum','avg','std','stdp','var','varp']:
                                last[item].items.append(fila[-1])
                            if func=='max':
                                if float(fila[-1])> float(last[item].max):
                                   last[item].max=fila[-1]
                            if func=='min':
                                if float(fila[-1])< float(last[item].min):
                                   last[item].min=fila[-1]                            
            actindex+=1


def groupbyToRows(table,out,row,group_list,attrs_list):
    #print 'Valor actual de table:%s' % table
    #global group_list
    #global attrs_list
    #print 'attrs_list:%s' % attrs_list
    if type(table)==type({}):
     for item in table:
        #print 'Recorriendo item: %s' % item
        #print 'con row: %s'%row
        row.append(item)
        #Guardar el valor de row, pq se modifica!!!
        row2=row[:]
        if type(table[item])==type({}):
            #print "llamada recursiva con row: %s\n"%row2
            for el in table[item]:
                row2.append(el)
                #print 'recorriendo subitem %s'%el
                #print 'row:%s'%row2
                groupbyToRows(table[item][el],out,row2,group_list,attrs_list)
                #print 'row despues de groupbyToRows: %s' % row2
                row2=row2[:-2]#[item]#Este cambio corrige un error en groupby cuando hay varios campos para agrupar
                #print 'row reconvertida: %s' % row2
                #print 'valor de ROW: %s\n' % row
            row=row[:-1]#;print 'cambiando row a: %s' % row
        else:
            #print "metiendo numero"
            row.append( table[item])
            #print 'row a meter:%s'%row           
            if row[-1]>0:
                functions=[]
                #Si se nos pide un agregado, poner el valor del agregado
                for j in attrs_list:
                    #print 'comprobando campo select aqui: %s' %j
                    if j[2]!='':
                        functions.append(j[1])
                #print 'functions222: %s' % functions
                #print 'len(row): %s' %len(row)
                if functions!=[]:
                    if functions[0]>=1:#len(row):
                        out.append(row)
                    else:
                        fval=row[-1]
                        row[functions[0]]=fval
                        #print 'metiendo row por functions: %s' % row
                        out.append(row[:-1])
                else:
                    #print 'metiendo row por functions en el else: %s' % row
                    out.append(row[:-1])
            row=row[:-2]
    else:
        row.append(table)
        #print 'ultima row a meter:%s'%row
        if row[-1]>0:
            functions=[]
            #Si se nos pide un agregado, poner el valor del agregado
            for j in attrs_list:
                #print 'comprobando campo select: %s' %j
                if j[2]!='':
                    functions.append(j[1])
            #print 'functions:%s' % functions
            #print 'row:%s' % row
            if functions!=[]:
                if functions[0]>=1:
                    out.append(row)
                else:
                    fval=row[-1]
                    #print 'fval:%s' % fval
                    row[functions[0]]=fval
                    out.append(row[:-1])
            else:
                out.append(row[:-1])
        #print 'metiendo row en el else:%s'%row
        row=[]        


def satisfyConditions(conds,item,at):
    #comprobar que cumple las condiciones si las hay
    condsOk=1
    at2=None#??
    #print 'conds:%s' % conds
    #print 'attrs_lists: %s' %attrs_list
    #print 'at: %s' %at
    if conds!=[]:
        for cond in conds:
            #Hay que permitir evaluar campos distintos del que se ha mandado(select texto where id...)
            #print 'evaluando item:%s' % item
            #print 'evaluando condicion:%s' % cond
            #print 'con valor de at: %s' %at
            atval=None            
            if isinstance(item,MiniObject):
                if at!=cond[0]:
                    at2=cond[0]
                    atval=getattr(item,at2)
                else:
                    atval=getattr(item,at)
                #print 'atval en objeto:%s' % atval
            elif type(item)==type({}):
                if at!=cond[0]:
                    at2=cond[0]
                    atval=item[int(at2)]
                else:
                    atval=item[at]
                #print 'atval en diccionario:%s' % atval
            elif type(item)==type([]):
                #print 'item:%s' % item
                #print 'at: %s' % at
                atval=item[int(at[1])]
                #print 'elemento para comprobar: %s' % atval
                at2=at[0] #antes era at aqui y abajo?
            if at2==cond[0]:
                if cond[1]=='=':
                    if atval!=cond[2]:
                        condsOk=0
                        break
                if cond[1] in ['!=','<>']:
                    if atval==cond[2]:
                        condsOk=0
                        break                                
                elif cond[1]=='>':
                    if atval<=cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='<':
                    if atval>=cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='>=':
                    if atval<cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='<=':
                    if atval>cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='contains':
                    if not cond[2] in atval:
                        condsOk=0
                        break
                elif cond[1]=='not contains':
                    if cond[2] in atval:
                        condsOk=0
                        break                     
                elif cond[1]=='in':
                    if atval not in cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='not in':
                    if atval in cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='like':
                    if not cond[2] in atval:
                        condsOk=0
                        break
                elif cond[1]=='not like':
                    if cond[2] in atval:
                        condsOk=0
                        break                     
                elif cond[1]=='between':                   
                    if not (atval>=cond[2] and atval<=cond[3]):
                        condsOk=0
                        break
                elif cond[1]=='not between':                     
                    if atval>=cond[2] and atval<=cond[3]:
                        condsOk=0
                        break
                #FALTA IMPLEMENTAR REGEX!!!!!!!!!!!!!
    return condsOk


def _linqlike(where_list,group_list,attrs_list,order_list,_list,order_type):
    linqresult_list=[]
    flds=[]
    conds=where_list
    seq=_list
    #print _list
    fpos=-1
    func=''
    #print 'where_list: %s' % where_list
    #print 'group_list: %s' % group_list
    #print 'attrs_list:%s'% attrs_list
    #print 'order_list:%s'% order_list
    #print 'type: %s'% order_type
    #Buscar func si la hay
    for item in attrs_list:
        if item[2]!='':
            func=item[2]
            break
    #Tratar de recuperar las expresiones si fuesen numericas(pasan como cadenas)
    for item in where_list:
        try:
           item[2]=int(item[2])
        except:
           pass
    #print 'lista de condiciones: %s' %where_list
    for item in seq:
        #print 'Recorriendo item: %s' % item
        if isinstance(item,MiniObject):
            condsOk=1
            for at in attrs_list:
                #print 'buscando campo: %s' % at
                if not hasattr(item,at[0]):
                    raise Exception('Error: El objeto no contiene la propiedad "%s"'%at[0])                                 
                condsOk=satisfyConditions(conds,item,at[0])
                #print 'Valor de condsOk: %s' % condsOk
                if condsOk==0: #optimizacion?
                    break                
                flds.append(getattr(item,int(at[0])))
            if flds!=[] and condsOk==1:
                linqresult_list.append(flds)
            flds=[]
        elif type(item)==type({}):
            for at in attrs_list:
                #print 'buscando campo: %s' % at
                #cambio para permitir claves de texto en diccionarios-----------
                if at[0][0]=='"': at[0]=at[0].strip('"')
                #fin cambio-----------------------------------------------------
                if at[0] not in item:
                   raise Exception('Error: El diccionario no contiene la clave "%s"'%at[0])
                condsOk=satisfyConditions(conds,item,at[0])
                #print 'Valor de condsOk: %s' % condsOk
                if condsOk==0: #optimizacion?
                    break 
                try: #??????????????????????????????                    
                    flds.append(item[int(at[0])])
                except:
                    flds.append(item[at[0]])
            if flds!=[] and condsOk==1:
                linqresult_list.append(flds)
            flds=[]
        elif type(item)==type([]):
            #print 'indices para las listas: %s' % attrs_list
            #print 'item: %s' % item
            #print 'attrs_list: %s' % attrs_list
            for at in attrs_list:
                #print 'probando at: %s' %at
                if int(at[1]) >=len(item):
                      raise Exception('Error: el indice "%s" esta fuera del rango de la lista'%at[1])
                condsOk=satisfyConditions(conds,item,at)
                #print 'Valor de condsOk: %s' % condsOk
                if condsOk==0: #optimizacion?
                    break                
                flds.append(item[int(at[1])])
            if flds!=[] and condsOk==1:
                linqresult_list.append(flds)
            flds=[]            
        else:
            raise Exception('Error: Las sentencias Linq-like solo se pueden aplicar a instancias de objetos, listas y diccionarios')
    #print 'resultados: %s' %linqresult_list
    #Comprobar si hay que agrupar los datos
    table={}
    mtx=matrix.Matrix(linqresult_list[:])
    if group_list!=[]:
        #Dar la vuelta a la lista
        #group_list.reverse() ???????????
        filt_values=[]
        #print 'group_list: %s' %group_list
        #print 'Hay que agrupar los resultados'
        #print mtx.toString()
        #Los campos del groupby deben ser menores o iguales a los atributos
        if len(group_list)>len(attrs_list):
            raise Exception('Error: El numero de campos en groupby debe ser igual o menor que el numero de campos seleccionados por el select')
        for el in group_list:
            if type(el[1]) not in [type(''),type(u''),type(0),type(0L),type(0.0)]:
                raise Exception('Error: no se puede usar groupby con elementos que no sean cadenas o numeros')
            if el[0] not in [e[0] for e in attrs_list]:
                raise Exception('Error: El campo "%s" no esta incluido en los campos de seleccion. Solo se puede usar groupby con campos incluidos en los campos de seleccion'%el[0])
            filt_values.append(list(set(mtx.getCol(int(el[1])))))
        #print 'filt_values: %s' % filt_values
        groupbyTable(table,filt_values,0)
        #print 'TABLE : %s' %table
        processGroupbyRows(mtx,table,group_list,attrs_list)
        #print 'TABLE DESPUES DE CONTAR: %s' %table
        m2=[]
        groupbyToRows(table,m2,[],group_list,attrs_list)
        #print 'RECONVERTIDO:'#Aqui esta el error
        #pprint.pprint(m2)
        #t0=m2
        #RESOLVER AQUI FUNCIONES NO COUNT!!!!!!!
        numfilas=len(m2)
        #print 'numero de filas obtenidas: %s' %numfilas
        #print 'funcion a aplicar: %s' %func
        #print 'posicion afectada en las filas: %s' %fpos
        if fpos>=0 and fpos >= len(m2[0]): fpos=len(m2[0])-1
        #proceder segun funcion(PERMITIMOS FUNCIONES AGRUPADAS: MAXMIN,SUMCOUNT,SUMAVG???)
        #estadisticos??
        s=v=sp=vp=m=max=min=count=recorr=None
        #Entrar en el for SOLO SI HAY ALGO (len!=0)
        #Cambio para que no coja las que tienen count a 0------------
        cont=0
        todelete=[]
        #print 'Valor de m2: %s' % m2
        #print 'Valor de fpos: %s' % fpos
        #-------------------------------------------------------------
        for it in m2:
            #print 'buscando funcion a aplicar...'
            #print 'func: %s' % func
            #print 'it[fpos]: %s'%it[fpos]
            if isinstance(it[fpos],GroupItem):
                if func=='count':
                    it[fpos]=it[fpos].count
                    if it[fpos]==0:#Cambio--------
                        todelete.append(m2[cont])#Cambio--------
                elif func=='sum':
                    #it[fpos]=it[fpos].value
                    it[fpos]=reduce(lambda x,y:float(x)+float(y),it[fpos].items)
                elif func=='avg':
                    #it[fpos]=(it[fpos].value)/(it[fpos].count)
                    it[fpos]=float(reduce(lambda x,y:float(x)+float(y),it[fpos].items))/len(it[fpos].items)
                elif func=='var':
                    sumx=float(reduce(lambda x,y:float(x)+float(y),it[fpos].items))
                    n=it[fpos].count
                    m=sumx/n                
                    sumx2=float(reduce(lambda x,y:float(x)+float(y),[(float(i)-float(m))**2 for i in it[fpos].items]))
                    if n>1:
                        it[fpos]=sumx2/(n-1)
                    else:
                        it[fpos]=sumx2/n
                elif func=='std':
                    sumx=float(reduce(lambda x,y:float(x)+float(y),it[fpos].items))
                    n=it[fpos].count
                    m=sumx/n                
                    sumx2=float(reduce(lambda x,y:float(x)+float(y),[(float(i)-float(m))**2 for i in it[fpos].items]))
                    if n>1:
                        it[fpos]=math.sqrt(sumx2/(n-1))
                    else:
                        it[fpos]=math.sqrt(sumx2/n)                    
                elif func=='varp':
                    sumx=float(reduce(lambda x,y:float(x)+float(y),it[fpos].items))
                    n=it[fpos].count
                    m=sumx/n              
                    sumx2=float(reduce(lambda x,y:float(x)+float(y),[(float(i)-float(m))**2 for i in it[fpos].items]))
                    it[fpos]=sumx2/n
                elif func=='stdp':
                    sumx=float(reduce(lambda x,y:float(x)+float(y),it[fpos].items))
                    n=it[fpos].count
                    m=sumx/n              
                    sumx2=float(reduce(lambda x,y:float(x)+float(y),[(float(i)-float(m))**2 for i in it[fpos].items]))
                    it[fpos]=math.sqrt(sumx2/n)               
                elif func=='max':
                    it[fpos]=it[fpos].max
                    #if func=='max':#Cambio--------
                    #    it[fpos]=it[fpos].max
                    if it[fpos]==-float('inf'):
                        todelete.append(m2[cont])#Cambio--------
                elif func=='min':
                    it[fpos]=it[fpos].min
                    #if func=='min':#Cambio--------
                    #    it[fpos]=it[fpos].max
                    #    if it[fpos]==float('inf'):
                    #        todelete.append(m2[cont])#Cambio--------
            #Cambiar el ultimo elemento si es un objeto por su campo count
            if isinstance(it[-1],GroupItem):
                it[-1]=it[-1].count
            cont+=1
        t0=m2
        #Cambio---------------------------
        if todelete:
            for item in todelete:
                #print 'deberiamos quitar %s'% item
                del m2[m2.index(item)]
        #Cambio-----------------------------------
    else:
        t0=linqresult_list[:]

    #Aplicar orderby si es preciso        
    #Crear un heap con el campo por el que se quiere ordenar (valido para mas de un campo??)
    #y recuperar la lista ordenada
    if order_list !=[]:
        heap=[]
        for el in t0:
            aux=[]
            for a in order_list:
                aux.append(el[int(a)])
            aux.append(el)
            heapq.heappush(heap,aux)
        t0=[heapq.heappop(heap)[-1] for i in range(len(heap))]
        #invertir si es preciso
        if order_type=='desc':
            t0.reverse()
    #-------------------------------------------------------
    #FIN DE PLANTILLA
    return t0

