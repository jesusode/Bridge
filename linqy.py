from __future__ import division
import sys
sys.path.append('.')#Para py2exe
sys.path.append('./modules')#Para py2exe
sys.path.append('library.zip')#Para py2exe
#Para evitar el error de desbordamiento que da el parser actual con jython
if not 'java' in sys.platform:
    if not 'minimal_py' in sys.modules:
         minimal_py=__import__('minimal_py')
    else:
         minimal_py=sys.modules['minimal_py']
if not 'python_runtime' in sys.modules:
     python_runtime=__import__('python_runtime')
else:
     python_runtime=sys.modules['python_runtime']
from python_runtime import *
if not 'itertools' in sys.modules:
     itertools=__import__('itertools')
else:
     itertools=sys.modules['itertools']
if not 'shutil' in sys.modules:
     shutil=__import__('shutil')
else:
     shutil=sys.modules['shutil']
if not 'prologpy' in sys.modules: 
     prologpy=__import__('prologpy')
else:
     prologpy=sys.modules['prologpy']
if not 'os' in sys.modules:
     os=__import__('os')
else:
     os=sys.modules['os']
if not 'os.path' in sys.modules:
     os.path=__import__('os.path')
else:
     os.path=sys.modules['os.path']
import xml.dom.minidom as minidom
#Esto tiene que estar asi para que sea procesado por pyinstaller-----------------------------------
try:
   import sqlite3
except:
   pass
import shutil
import BeautifulSoup
import BSXPath
import sgmllib
import cgi, Cookie, pprint, urlparse, urllib
import xpath
import web
import SimpleHTTPServer
from python_runtime import _print,_input,_exec,_eval,_getSystem,_mod,_check_py_bases,_type,_tostring,_append,_car,_cdr,_cons,_last,_butlast,_curry,_closure,_compose,_fcopy,_decorate,_itermix,_trampoline
from python_runtime import _getWebVar,_getWebEnviron,_getWebPath,SESSION,_killSession,_setSessionVar,_getSessionVar,_getCookie,_setCookie,_getWebFile,_setHeader,_webRedirect
from python_runtime import _toMatrix,_invert,_toDict,_mcopy,_appendRow,_getList,_insertRow,_appendCol,_insertCol,_getCol,_getRow,_getDimensions,_size,_toint,_tofloat,_abs,_strip,_count,_indexof,_histogram
from python_runtime import _chain,_zip,_cartessian, _combinations,_combinations_with_r, _permutations,_enumerate, _starmap, _list,_cycle,_split,_join,_readf,_readflines,_system,_lisp,_scheme,_lispModule,_clojure
from python_runtime import _xmltod,_dtoxml,_transaction,_rollback,_isclass,_cmdline,_toUnicode,_slice,_checkType,_xmlstr,_applyXSLT,_geturl,_open,_C,_getC,_copy
from python_runtime import _urlencode,_urldecode,_linqlike,_append2,_reverse,_queryADO,_getDBADOinfo,_sublist,_insert,_rematch,_resplit,_rereplace,_fromjson,_tojson
from python_runtime import _formbox,_getFormItemValue,_setFormItemValue,_getFormItem,_callFormItem,_setFormItemFont,_tcl,_keys,_values,_pairs, _socket_server,_socket_client,_apply,_del,_format,_replace,_getchar
from python_runtime import _find,_strinsert,_regroups,_writef,_writeflines
#---------------------------------------------------------------------------------------------------------------



class EnumMetaClass(type):
    def __setattr__(self, name, value):
        raise Exception('Error: You cannot set an enum value. Enum values are inmutable')

class Enum:
    __metaclass__= EnumMetaClass

__typedefs={'numeric':[],'chain':[]}
__type_instances={}
__basecons={}
__pyBases=[]

python_runtime._check_py_bases([])
class enumerable(MiniObject):
 def __init__(self,*k,**kw):
  self.iterable=None
  self.orderitem=None
  MiniObject.__init__(self,*k,**kw)
 
 def select ( self, callable):
         return enumerable(iterable=(list(itertools.imap(callable,list(itertools.chain(self.iterable))))),orderitem=0)
         
         
 
 def selectMany ( self, callable):
      t = enumerable(iterable=(list(itertools.imap(callable,list(itertools.chain(self.iterable))))),orderitem=0)
      
      
      resul = []
      
      
      for item in t.iterable: 
           
           if _type(item) == _type([]) : 
                for el in flatten(item): 
                     python_runtime._append2(el,resul)
                     
                     
                
                
                
           else:
                python_runtime._append2(item,resul)
                
                
           
           
           
           
           
      
      
      return enumerable(iterable=resul,orderitem=1)
      
      
      
      
 
 def foreach ( self, callable):
      for item in self.iterable: 
           callable(item)
           
           
      
      
      return enumerable(iterable=self.iterable,orderitem=0)
      
      
 
 def where ( self, pred):
      return enumerable(iterable=(filter(pred,list(itertools.chain(self.iterable)))),orderitem=0)
      
      
 
 def orderBy ( self, callable):
      return enumerable(orderitem=1,iterable=(python_runtime.doSort(itertools.chain(self.iterable),callable)))
      
      
 
 def thenBy ( self, callable):
      
      if self.orderitem == 0 : 
           raise Exception("Error: Solo se permite thenBy despues de un orderBy,orderByDescending u otro thenBy o thenByDescending")
           
           
           
      
      
      
      
      return enumerable(iterable=(python_runtime.doSort(itertools.chain(self.iterable),callable)),orderitem=1)
      
      
      
 
 def orderByDescending ( self, callable):
      return enumerable(iterable=(python_runtime.doSort(itertools.chain(self.iterable),callable,1)),orderitem=1)
      
      
 
 def thenByDescending ( self, callable):
      
      if self.orderitem == 0 : 
           raise Exception("Error: Solo se permite thenByDescending despues de un orderBy,orderByDescending u otro thenBy o thenByDescending")
           
           
           
      
      
      
      
      return enumerable(iterable=(python_runtime.doSort(itertools.chain(self.iterable),callable)),orderitem=1)
      
      
      
 
 def any ( self, pred):
      for item in self.iterable: 
           
           if pred(item) : 
                return True
                
                
           
           
           
           
           
      
      
      return False
      
      
 
 def first ( self, pred):
      for item in self.iterable: 
           
           if pred(item) : 
                return item
                
                
           
           
           
           
           
      
      
      return None
      
      
 
 def last ( self, pred):
      last = None
      
      
      for item in self.iterable: 
           
           if pred(item) : 
                last = item
                
                
                
           
           
           
           
           
      
      
      return last
      
      
      
 
 def single ( self, pred):
      cont = 0
      
      
      target = None
      
      
      for item in self.iterable: 
           
           if pred(item) : 
                cont+=1
                
                target = item
                
                
                
                
           
           
           
           
           
      
      
      return target if cont == 1 else None
      
      
      
      
      
 
 def groupBy ( self, callable):
      return (python_runtime.doGroup(self.iterable,callable))
      
      
 
 def take ( self, n):
      return enumerable(iterable=(list(itertools.chain(self.iterable))[ 0: n]
      ),orderitem=0)
      
      
 
 def takeWhile ( self, pred):
      resul = []
      
      
      for item in self.iterable: 
           
           if pred(item) : 
                python_runtime._append2(item,resul)
                
                
           else:
                return enumerable(iterable=resul,orderitem=0)
                
                
           
           
           
           
           
      
      
      return enumerable(iterable=resul,orderitem=0)
      
      
      
 
 def skip ( self, n):
      return enumerable(iterable=(list(itertools.chain(self.iterable))[ n: None]
      ),orderitem=0)
      
      
 
 def skipWhile ( self, pred):
      cont = 0
      
      
      
      while cont < _size(self.iterable) : 
           
           if pred(self.iterable[cont]) : 
                cont+=1
                
                continue
                
                
                
           else:
                break
                
                
           
           
           
           
           
      
      
      
      __it__ = enumerable(iterable=(list(itertools.chain(self.iterable))[ cont: None]
      ),orderitem=0)
      
      
      return __it__
      
      
      
      
      
 
 def all ( self, pred):
      resul = []
      
      
      for item in self.iterable: 
           
           if pred(item) : 
                python_runtime._append2(item,resul)
                
                
           
           
           
           
           
      
      
      return enumerable(iterable=resul,orderitem=0)
      
      
      
 
 def join ( self, seq2, fncond1, fncond2, mapfun):
      resul = []
      
      
      cont = 0
      
      
      elems = self.iterable
      
      
      elems2 = seq2.iterable
      
      
      i = 0
      while i < _size(elems2) :
           
           if fncond2(elems2[i]) == fncond1(elems[i]) : 
                python_runtime._append2(mapfun(elems[i],elems2[i]),resul)
                
                
           
           
           
           
           
           i+=1
      
      
      return enumerable(iterable=resul,orderitem=0)
      
      
      
      
      
      
      
 
 def groupJoin ( self, seq, fnkey1, fnkey2, mapfun):
      resul = []
      
      
      grouped = self.groupBy(fnkey1)
      
      
      grouped2 = seq.groupBy(fnkey2)
      
      
      for item in grouped: 
           python_runtime._append2(mapfun(grouped[item][0],grouped2[item]),resul)
           
           
      
      
      return enumerable(iterable=resul,orderitem=0)
      
      
      
      
      
 
 def reverse ( self):
      return enumerable(iterable=_reverse(self.iterable),orderitem=0)
      
      
 
 def intersect ( self, seq):
      resul = []
      
      
      for item in self.iterable: 
           
           if item in seq.iterable : 
                python_runtime._append2(item,resul)
                
                
           
           
           
           
           
      
      
      return enumerable(iterable=resul,orderitem=0)
      
      
      
 
 def union ( self, seq):
      resul = self.iterable
      
      
      for item in seq.iterable: 
           
           if item not in resul : 
                python_runtime._append2(item,resul)
                
                
           
           
           
           
           
      
      
      return enumerable(iterable=resul,orderitem=0)
      
      
      
 
 def distinct ( self):
      resul = []
      
      
      for item in self.iterable: 
           
           if not item in resul : 
                python_runtime._append2(item,resul)
                
                
           
           
           
           
           
      
      
      return enumerable(iterable=resul,orderitem=0)
      
      
      
 
 def except_ ( self, seq):
      resul = []
      
      
      for item in self.iterable: 
           
           if item not in seq.iterable : 
                python_runtime._append2(item,resul)
                
                
           
           
           
           
           
      
      
      return enumerable(iterable=resul,orderitem=0)
      
      
      
 
 def zip ( self, seq2, fun):
      resul = []
      
      
      elems1 = self.iterable
      
      
      elems2 = seq2.iterable
      
      
      i = 0
      while i < _size(elems1) :
           python_runtime._append2(fun(elems1[i],elems2[i]),resul)
           
           
           i+=1
      
      
      return enumerable(iterable=resul,orderitem=0)
      
      
      
      
      
      
 
 def contains ( self, elem):
      
      if elem in self.iterable : 
           return True
           
           
      else:
           return False
           
           
      
      
      
      
      
 
 def concat ( self, seq):
      return enumerable(iterable=python_runtime.doAddition(self.iterable,seq.iterable),orderitem=0)
      
      
 
 def count ( self):
      return _size(self.iterable)
      
      
 
 def aggregate ( self, reducefun, initval=None):
      
      if initval == None : 
           return reduce(reducefun,itertools.chain(self.iterable))
           
           
      else:
           return reduce(reducefun,itertools.chain(self.iterable),initval)
           
           
      
      
      
      
      
 
 def defaultIfEmpty ( self, default_value):
      
      if self.iterable == [] : 
           return enumerable(iterable=[default_value],orderitem=0)
           
           
      else:
           return enumerable(iterable=self.iterable,orderitem=0)
           
           
      
      
      
      
      
 
 def elementAt ( self, pos):
      
      if pos < _size(self.iterable) : 
           return self.iterable[pos]
           
           
      else:
           return None
           
           
      
      
      
      
      
 
 def __repr__ ( self):
      return _tostring(self.iterable)
      
      
 
 def sequenceEqual ( self, seq):
      return self.iterable == seq.iterable
      
      
 
 def ofType ( self, elem):
      return enumerable(iterable=(filter(lambda x: _type(x) == _type(elem),list(itertools.chain(self.iterable)))),orderitem=0)
      
      
 
 def toList ( self):
      return self.iterable
      
      
 
 def toDictionary ( self, fun):
      return python_runtime.doGroup(self.iterable,fun)
      
      
 
 def toLookup ( self, keysfun, valuesfun):
      lookup = {}
      
      
      for item in self.iterable: 
           
           if not keysfun(item) in lookup : 
                lookup[keysfun(item)] = [valuesfun(item)]
                
                
                
           else:
                python_runtime._append2(valuesfun(item),lookup[keysfun(item)])
                
                
           
           
           
           
           
      
      
      return lookup
      
      
      
 
 def sum ( self):
      return reduce(lambda x,y: python_runtime.doAddition(x,y),itertools.chain(self.iterable))
      
      
 
 def average ( self):
      return (reduce(lambda x,y: python_runtime.doAddition(x,y),itertools.chain(self.iterable)))/_size(self.iterable)
      
      
 
 def max ( self):
      max = self.iterable[0]
      
      
      
      i = 1
      while i < _size(self.iterable) :
           
           if self.iterable[i] > max : 
                max = self.iterable[i]
                
                
                
           
           
           
           
           
           i+=1
      
      
      return max
      
      
      
      
 
 def min ( self):
      min = self.iterable[0]
      
      
      
      i = 1
      while i < _size(self.iterable) :
           
           if self.iterable[i] < min : 
                min = self.iterable[i]
                
                
                
           
           
           
           
           
           i+=1
      
      
      return min
      
      
      
      
 



def linq ( iter):
     return enumerable(iterable=iter)
     
     

def flatten ( list):
     flat = []
     
     
     for item in list: 
          
          if _type(item) == _type([]) : 
               for el in flatten(item): 
                    python_runtime._append2(el,flat)
                    
                    
               
               
               
          else:
               python_runtime._append2(item,flat)
               
               
          
          
          
          
          
     
     
     return flat
     
     
     

def range ( start, howmany):
     return linq(python_runtime.genRange(start,python_runtime.doAddition(python_runtime.doAddition(start,howmany),1)))
     
     

def empty ( ):
     return linq([])
     
     

def repeat ( elem, times):
     resul = []
     
     
     cont = 0
     
     
     
     while cont < times : 
          python_runtime._append2(elem,resul)
          
          cont+=1
          
          
          
     
     
     
     return resul
     
     
     
     
     






python_runtime._check_py_bases([])
class Stack(MiniObject):
 def __init__(self,*k,**kw):
  self.__stack=None
  MiniObject.__init__(self,*k,**kw)
 
 def init ( self):
      
      if self.__stack == None : 
           self.__stack = []
           
           
           
      
      
      
      
      
 
 def push ( self, elem):
      python_runtime._append2(elem,self.__stack)
      
      
 
 def pop ( self):
      ret = self.__stack[-1]
      
      
      
      if _size(self.__stack) > 0 : 
           self.__stack = list(itertools.chain(self.__stack))[ None: -1]
           
           
           
           
      
      
      
      
      return ret
      
      
      
      
 
 def peek ( self):
      
      if _size(self.__stack) > 0 : 
           return self.__stack[-1]
           
           
      else:
           return None
           
           
      
      
      
      
      
 
 def size ( self):
      return _size(self.__stack)
      
      
 
 def isEmpty ( self):
      
      if _size(self.__stack) > 0 : 
           return True
           
           
      else:
           return False
           
           
      
      
      
      
      
 
 def empty ( self):
      self.__stack = []
      
      
      
 
 def getList ( self):
      return self.__stack
      
      
 
 def toString ( self):
      return _tostring(self.__stack)
      
      
 






import re


python_runtime._check_py_bases([])
class token(MiniObject):
 def __init__(self,*k,**kw):
  self.id=None
  self.type=None
  self.value=None
  self.lin=None
  self.col=None
  MiniObject.__init__(self,*k,**kw)
 
 def init ( self):
      
      if self.id == None : 
           self.id = ""
           
           
           
      
      
      
      
      
      if self.type == None : 
           self.type = "notype"
           
           
           
      
      
      
      
      
      if self.value == None : 
           self.value = None
           
           
           
      
      
      
      
      
      if self.lin == None : 
           self.lin = 0
           
           
           
      
      
      
      
      
      if self.col == None : 
           self.col = 0
           
           
           
      
      
      
      
      
      
      
      
      
 
 def toString ( self):
      return python_runtime.doFormat("<Token -> Type: {0},Value: {1}>",[self.type,self.value])
      
      
 
 def __repr__ ( self):
      return self.toString()
      
      
 
class symbol(MiniObject):
 def __init__(self,*k,**kw):
  self.__name=None
  self.__category=None
  self.__type=None
  MiniObject.__init__(self,*k,**kw)
 
 def init ( self):
      
      if self.name == None : 
           self.name = ""
           
           
           
      
      
      
      
      
      if self.category == None : 
           self.category = ""
           
           
           
      
      
      
      
      
      if self.type == None : 
           self.type = ""
           
           
           
      
      
      
      
      
      
      
 
 def getName ( self):
      return self.__name
      
      
 
 def setName ( self, val):
      self.__name = val
      
      
      
 
 def getCategory ( self):
      return self.__category
      
      
 
 def setCategory ( self, val):
      self.__category = val
      
      
      
 
 def getType ( self):
      return self.__type
      
      
 
 def setType ( self, val):
      self.__type = val
      
      
      
 
class lexer(MiniObject):
 def __init__(self,*k,**kw):
  self.__current=None
  self.__input=None
  self.__index=None
  self.__table=None
  self.__strict=None
  self.__whitespace=None
  self.toklist=None
  self.__curline=None
  self.__curpos=None
  self.__toignore=None
  MiniObject.__init__(self,*k,**kw)
 
 def init ( self):
      
      if self.toklist == None : 
           self.toklist = []
           
           
           
      
      
      
      
      
      if self.__current == None : 
           self.__current = None
           
           
           
      
      
      
      
      
      if self.__input == None : 
           self.__input = ""
           
           
           
      
      
      
      
      
      if self.__index == None : 
           self.__index = 0
           
           
           
      
      
      
      
      
      if self.__whitespace == None : 
           self.__whitespace = False
           
           
           
      
      
      
      
      
      if self.__table == None : 
           self.__table = {}
           
           
           
      
      
      
      
      
      if self.__curline == None : 
           self.__curline = 0
           
           
           
      
      
      
      
      
      if self.__curpos == None : 
           self.__curpos = 0
           
           
           
      
      
      
      
      
      if self.__toignore == None : 
           self.__toignore = []
           
           
           
      
      
      
      
      
      
      
      
      
      
      
      
      
 
 def setInput ( self, inp):
      self.__input = inp
      
      
      self.__index = 0
      
      
      
      
 
 def getInput ( self):
      return self.__input
      
      
 
 def setIgnore ( self, ign_lst):
      self.__toignore = ign_lst
      
      
      
 
 def getIgnore ( self):
      return self.__toignore
      
      
 
 def getRest ( self):
      return _sublist(self.__input,self.__index)
      
      
 
 def isEOF ( self):
      
      if self.__index > _size(self.__input) : 
           return True
           
           
      else:
           return False
           
           
      
      
      
      
      
 
 def setIndex ( self, idx):
      self.__index = idx
      
      
      
 
 def getIndex ( self):
      return self.__index
      
      
 
 def ignoreWhitespace ( self, tf):
      if not tf in [True,False]:
       raise Exception("""assertion error: 'tf in [True,False]' is false""")
      
      self.__whitespace = tf
      
      
      
 
 def setTable ( self, table):
      self.__table = table
      
      
      for item in self.__table: 
           
           if item[3] == True : 
                python_runtime._append2(item[1],self.__toignore)
                
                
           
           
           
           
           
      
      
      
      
 
 def nextToken ( self, expected=None):
      self.__current = self.__next(expected)
      
      
      return self.__current
      
      
      
 
 def __next ( self, expected=None):
      if not self.__table != []:
       raise Exception("""assertion error: 'self.__table != []' is false""")
      
      fn = None
      
      
      
      
      if self.__input == "" or self.__index == _size(self.__input) : 
           t = token(type="EOF",value="END OF INPUT")
           
           
           
           if expected != None and t.type != expected : 
                raise Exception(python_runtime.doFormat("Error: Se esperaba un token de tipo {0} y se ha encontrado {1}",[expected,t.type]))
                
                
                
           
           
           
           
           return t
           
           
           
           
      
      
      
      
      
      if self.__whitespace == True : 
           self.__input = self.__input.strip()
           
           
           
      
      
      
      
      for item in self.__table: 
           kind = item[1]
           
           
           fn = item[2]
           
           
           
           if self.__whitespace == True : 
                self.__input = self.__input.strip()
                
                
                
           
           
           
           
           rest = _sublist(self.__input,self.__index)
           
           
           
           if rest == "" : 
                return None
                
                
           
           
           
           
           m = re.search(item[0],rest,re.MULTILINE)
           
           
           
           if m and m.start() == 0 : 
                val = _sublist(rest,m.start(),m.end())
                
                
                self.__index = python_runtime.doAddition(self.__index,m.end())
                
                
                t = token(type=kind,value=val)
                
                
                
                if t.type in self.__toignore : 
                     continue
                     
                     
                
                
                
                
                
                if expected != None and t.type != expected : 
                     raise Exception(python_runtime.doFormat("Error: Se esperaba un token de tipo {0} y se ha encontrado {1}",[expected,t.type]))
                     
                     
                     
                
                
                
                
                python_runtime._append2(t,self.toklist)
                
                
                if fn != None : 
                     fn(val)
                     
                     
                
                
                
                
                return t
                
                
                
                
                
                
                
                
                
           
           
           
           
           
           
           
           
           
           
           
      
      
      raise Exception("Invalid input value: no token match.")
      
      
      
      
      
      
 
 def lookahead2 ( self, n):
      old = self.__input
      
      
      toks_seen = []
      
      
      i = 0
      while i < n :
           python_runtime._append2(self.nextToken(),toks_seen)
           
           
           i+=1
      
      
      self.__input = old
      
      
      return toks_seen
      
      
      
      
      
      
 
 def lookahead ( self, n):
      old = self.__index
      
      
      toks_seen = []
      
      
      
      try : 
           i = 0
           while i < n :
                nxt = self.nextToken()
                
                
                
                if nxt != None : 
                     python_runtime._append2(nxt,toks_seen)
                     
                     
                
                
                
                
                
                
                i+=1
           
           
           
      
      
      
      except Exception as exception: 
           toks_seen = []
           
           
           
      
      
      
      
      self.__index = old
      
      
      return toks_seen
      
      
      
      
      
      
 
class AST(MiniObject):
 def __init__(self,*k,**kw):
  self.parent=None
  self.token=None
  self.children=None
  self.scope=None
  self.annots=None
  MiniObject.__init__(self,*k,**kw)
 
 def init ( self):
      
      if self.children == None : 
           self.children = []
           
           
           
      
      
      
      
      
      if self.annots == None : 
           self.annots = {}
           
           
           
      
      
      
      
      
      
 
 def isRoot ( self):
      return self.parent == None
      
      
 
 def isLeaf ( self):
      return _size(self.children) == 0
      
      
 
 def getParent ( self):
      return self.parent
      
      
 
 def getChildren ( self):
      return self.children
      
      
 
 def addChild ( self, child):
      python_runtime._append2(child,self.children)
      
      
 
 def getNodeType ( self):
      return self.token.type if self.token != None else None
      
      
      
 
 def isNil ( self):
      return self.token == None
      
      
 
 def getScope ( self):
      return self.scope
      
      
 
 def toString ( self):
      return self.token.toString() if self.token != None else "nil"
      
      
      
 
 def toStringTree ( self):
      buff = ""
      
      
      
      
      if self.children == None or _size(self.children) == 0 : 
           return self.toString()
           
           
      
      
      
      
      
      if not self.isNil() : 
           buff = python_runtime.doAddition(buff,"(")
           
           
           buff = python_runtime.doAddition(buff,self.toString())
           
           
           buff = python_runtime.doAddition(buff," ")
           
           
           
           
           
      
      
      
      
      for child in self.children: 
           buff = python_runtime.doAddition(buff," ")
           
           
           buff = python_runtime.doAddition(buff,child.toStringTree())
           
           
           
           
      
      
      
      if not self.isNil() : 
           buff = python_runtime.doAddition(buff,")")
           
           
           
      
      
      
      
      return buff
      
      
      
      
      
      
 






def visit ( ast, fun):
     if not _type(ast) == AST:
      raise Exception("""assertion error: '_type(ast) == AST' is false""")
     
     fun(ast.token)
     
     for node in ast.getChildren(): 
          visit(node,fun)
          
          
     
     
     
     









def clear_memos ( ):
     global memos
     
     memos = {}
     
     
     
     

def _alreadyParsed ( memo, pos):
     
     if pos in _keys(memo) : 
          return memo[pos]
          
          
     else:
          return None
          
          
     
     
     
     
     

def _memoize ( memo, start, stop):
     global memos
     
     _print(python_runtime.doAddition("Memos antes de _memoize: ",_tostring(memos)))
     
     memo[start] = stop
     
     
     _print(python_runtime.doAddition("Memos despues de _memoize: ",_tostring(memos)))
     
     
     
     
     


memos = {}




















lexx = lexer()



_AST = None



_stack = Stack()



table = [["\s+","WHITESPACE",None,False],["\->","ARROW",None,False],["\#[^\#]*[\#]","COMMENT",None,False],["\+|\-","PLUSMIN",None,False],["\*|/","TIMESDIV",None,False],["\^","EXP",None,False],["\?","QUESTION",None,False],["\(","LPAREN",None,False],["\)","RPAREN",None,False],["\[","LBRACK",None,False],["\]","RBRACK",None,False],["\{","LCURLY",None,False],["\}","RCURLY",None,False],["[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?","NUMBER",None,False],[",","COMMA",None,False],[":","COLON",None,False],[";","SEMI",None,False],["\|","PIPE",None,False],["\.","DOT",None,False],["file\s","FILE",None,False],["show\s","SHOW",None,False],["as\s","AS",None,False],["to\s","TO",None,False],["if\s","IF",None,False],["then\s","THEN",None,False],["while\s","WHILE",None,False],["do\s","DO",None,False],["set\s","SET",None,False],["toplevel\s","TOPLEVEL",None,False],["csv\s","CSV",None,False],["select\s","SELECT",None,False],["selectMany\s","SELECTMANY",None,False],["where\s","WHERE",None,False],["orderBy\s","ORDERBY",None,False],["orderByDescending\s","ORDERBYDESCENDING",None,False],["thenBy\s","THENBY",None,False],["thenByDescending\s","THENBYDESCENDING",None,False],["any\s","ANY",None,False],["first\s","FIRST",None,False],["last\s","LAST",None,False],["single\s","SINGLE",None,False],["groupBy\s","GROUPBY",None,False],["take\s","TAKE",None,False],["takeWhile\s","TAKEWHILE",None,False],["skip\s","SKIP",None,False],["skipWhile\s","SKIPWHILE",None,False],["all\s","ALL",None,False],["join\s","JOIN",None,False],["groupJoin\s","GROUPJOIN",None,False],["reverse\s","REVERSE",None,False],["intersect\s","INTERSECT",None,False],["union\s","UNION",None,False],["distinct\s","DISTINCT",None,False],["except\s","EXCEPT",None,False],["zip\s","ZIP",None,False],["concat\s","CONCAT",None,False],["contains\s","CONTAINS",None,False],["count\s","COUNT",None,False],["aggregate\s","AGGREGATE",None,False],["defaultIfEmpty\s","DEFAULTIFEMPTY",None,False],["sequenceEqual\s","SEQUENCEEQUAL",None,False],["toList\s","TOLIST",None,False],["toDictionary\s","TODICTIONARY",None,False],["toLookup\s","TOLOOKUP",None,False],["foreach\s","FOREACH",None,False],["sum\s","SUM",None,False],["average\s","AVERAGE",None,False],["max\s","MAX",None,False],["min\s","MIN",None,False],["ofType\s","OFTYPE",None,False],["elementAt\s","ELEMENTAT",None,False],["float\s","FLOAT",None,False],["integer\s","INTEGER",None,False],["text\s","TEXT",None,False],["call\s","CALL",None,False],["get\s","GET",None,False],["use\s","USE",None,False],["function\s","FUNCTION",None,False],["end\s*","END",None,False],["and\s","AND",None,False],["or\s","OR",None,False],["not\s","NOT",None,False],["<=|>=|>|<|==|!=","BOOLOP",None,False],["=","EQUAL",None,False],["[a-zA-Z_][a-zA-Z_0-9]*","ID",None,False],["\"[^\"]*\"","STRING",None,False]]



lexx.setTable(table)

ignore_list = ["WHITESPACE"]



lexx.setIgnore(ignore_list)

defined_ids = []



linq_operators = ["select","where","orderBy","any","first","last","single","groupBy","take","skip","all","join","reverse","intersect","union","distinct","except","zip","concat","contains","count","aggregate","elementAt","sum","average","max","min","ofType","foreach","selectMany","takeWhile","skipWhile","thenBy","orderByDescending","thenByDescending","groupJoin","defaultIfEmpty","sequenceEqual","toList","toDictionary","toLookup"]




def openfile ( path, csv=""):
     
     if csv == "" : 
          return _readflines(path)
          
          
     else:
          lns = list(itertools.imap(lambda x: _split(x,csv),list(itertools.chain(_readflines(path)))))
          
          
          return lns
          
          
          
     
     
     
     
     

def toFileId ( id, _file):
     open(_file,"w").close()
     
     
     
     if _type(id) in [_type(""),_type(unicode("")),_type(34),_type(90.67)] : 
          _writef(_file,id)
          
          
     else:
          _writeflines(_file,id.iterable)
          
          
     
     
     
     
     
     



def linqy ( ):
     linqy_values = []
     
     
     
     linqy_val = ""
     
     
     python_runtime._append2(linq_st(),linqy_values)
     
     lexx.nextToken("SEMI")
     
     
     while lexx.lookahead(1) and lexx.lookahead(1)[0].type != "EOF" : 
          python_runtime._append2(linq_st(),linqy_values)
          
          lexx.nextToken("SEMI")
          
          
          
     
     
     
     linqy_val = python_runtime.doAddition(_join((filter(lambda x: x != "",list(itertools.chain(linqy_values)))),";"),";")
     
     
     linqy_val = _rereplace(linqy_val,";;",";")
     
     
     return linqy_val
     
     
     
     
     
     
     
     
     

def linq_st ( ):
     linq_st_values = []
     
     
     
     linq_st_val = ""
     
     
     global defined_ids
     
     
     if lexx.lookahead(1)[0].type == "TOPLEVEL" : 
          lexx.nextToken("TOPLEVEL")
          
          python_runtime._append2(idlist(),linq_st_values)
          
          linq_st_val = python_runtime.doAddition("global ",linq_st_values[0])
          
          
          
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "USE" : 
               lexx.nextToken("USE")
               
               python_runtime._append2(boolexp(),linq_st_values)
               
               linq_st_val = python_runtime.doAddition("native ",linq_st_values[0])
               
               
               
               
               
          else:
               
               if lexx.lookahead(1)[0].type == "SHOW" : 
                    lexx.nextToken("SHOW")
                    
                    python_runtime._append2(lexx.nextToken("ID"),linq_st_values)
                    
                    linq_st_val = python_runtime.doAddition(python_runtime.doAddition("_print(",linq_st_values[0].value),")")
                    
                    
                    
                    
                    
               else:
                    
                    if lexx.lookahead(1)[0].type == "TO" : 
                         lexx.nextToken("TO")
                         
                         lexx.nextToken("FILE")
                         
                         python_runtime._append2(lexx.nextToken("STRING"),linq_st_values)
                         
                         python_runtime._append2(lexx.nextToken("ID"),linq_st_values)
                         
                         linq_st_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("toFileId(",linq_st_values[1].value),","),linq_st_values[0].value),")")
                         
                         
                         
                         
                         
                         
                         
                    else:
                         
                         if lexx.lookahead(1)[0].type == "COMMENT" : 
                              python_runtime._append2(lexx.nextToken("COMMENT"),linq_st_values)
                              
                              linq_st_val = ""
                              
                              
                              
                              
                         else:
                              
                              if lexx.lookahead(1)[0].type == "FUNCTION" : 
                                   python_runtime._append2(lexx.nextToken("FUNCTION"),linq_st_values)
                                   
                                   python_runtime._append2(lexx.nextToken("ID"),linq_st_values)
                                   
                                   lexx.nextToken("LPAREN")
                                   
                                   python_runtime._append2(idlist(),linq_st_values)
                                   
                                   lexx.nextToken("RPAREN")
                                   
                                   python_runtime._append2(linq_st(),linq_st_values)
                                   
                                   
                                   while lexx.lookahead(1)[0].type != "END" : 
                                        python_runtime._append2(linq_st(),linq_st_values)
                                        
                                        
                                   
                                   
                                   
                                   python_runtime._append2(lexx.nextToken("END"),linq_st_values)
                                   
                                   linq_st_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("begin ",linq_st_values[0].value)," "),linq_st_values[1].value),"("),linq_st_values[2]),"): ")
                                   
                                   
                                   cont = 3
                                   
                                   
                                   i = 3
                                   while i < _size(linq_st_values) :
                                        
                                        if _type(linq_st_values[i]) == _type(token()) : 
                                             linq_st_val = python_runtime.doAddition(linq_st_val,linq_st_values[i].value)
                                             
                                             
                                             
                                        else:
                                             
                                             if cont == _size(linq_st_values)-2 : 
                                                  linq_st_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(linq_st_val,"return "),linq_st_values[i]),";")
                                                  
                                                  
                                                  
                                             else:
                                                  linq_st_val = python_runtime.doAddition(python_runtime.doAddition(linq_st_val,linq_st_values[i]),";")
                                                  
                                                  
                                                  
                                             
                                             
                                             
                                             
                                             
                                        
                                        
                                        
                                        
                                        cont+=1
                                        
                                        
                                        
                                        i+=1
                                   
                                   
                                   linq_st_val = python_runtime.doAddition(linq_st_val," endsec; ")
                                   
                                   
                                   linq_st_val = _rereplace(linq_st_val,"setvar\s+[a-zA-Z_][a-zA-Z_0-9]*\s*;","")
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                              else:
                                   
                                   if lexx.lookahead(1)[0].type == "IF" : 
                                        python_runtime._append2(lexx.nextToken("IF"),linq_st_values)
                                        
                                        python_runtime._append2(boolexp(),linq_st_values)
                                        
                                        python_runtime._append2(lexx.nextToken("THEN"),linq_st_values)
                                        
                                        python_runtime._append2(linq_st(),linq_st_values)
                                        
                                        
                                        while lexx.lookahead(1)[0].type != "END" : 
                                             python_runtime._append2(linq_st(),linq_st_values)
                                             
                                             
                                        
                                        
                                        
                                        python_runtime._append2(lexx.nextToken("END"),linq_st_values)
                                        
                                        linq_st_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(linq_st_values[0].value," "),linq_st_values[1])," "),linq_st_values[2].value)," ")
                                        
                                        
                                        i = 3
                                        while i < _size(linq_st_values) :
                                             
                                             if _type(linq_st_values[i]) == _type(token()) : 
                                                  linq_st_val = python_runtime.doAddition(linq_st_val,linq_st_values[i].value)
                                                  
                                                  
                                                  
                                             else:
                                                  linq_st_val = python_runtime.doAddition(python_runtime.doAddition(linq_st_val,linq_st_values[i]),";")
                                                  
                                                  
                                                  
                                             
                                             
                                             
                                             
                                             
                                             i+=1
                                        
                                        
                                        linq_st_val = python_runtime.doAddition(linq_st_val,";")
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                   else:
                                        
                                        if lexx.lookahead(1)[0].type == "WHILE" : 
                                             python_runtime._append2(lexx.nextToken("WHILE"),linq_st_values)
                                             
                                             python_runtime._append2(boolexp(),linq_st_values)
                                             
                                             python_runtime._append2(lexx.nextToken("DO"),linq_st_values)
                                             
                                             python_runtime._append2(linq_st(),linq_st_values)
                                             
                                             
                                             while lexx.lookahead(1)[0].type != "END" : 
                                                  python_runtime._append2(linq_st(),linq_st_values)
                                                  
                                                  
                                             
                                             
                                             
                                             python_runtime._append2(lexx.nextToken("END"),linq_st_values)
                                             
                                             linq_st_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(linq_st_values[0].value," "),linq_st_values[1])," "),linq_st_values[2].value)," ")
                                             
                                             
                                             i = 3
                                             while i < _size(linq_st_values) :
                                                  
                                                  if _type(linq_st_values[i]) == _type(token()) : 
                                                       linq_st_val = python_runtime.doAddition(linq_st_val,linq_st_values[i].value)
                                                       
                                                       
                                                       
                                                  else:
                                                       linq_st_val = python_runtime.doAddition(python_runtime.doAddition(linq_st_val,linq_st_values[i]),";")
                                                       
                                                       
                                                       
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  i+=1
                                             
                                             
                                             linq_st_val = python_runtime.doAddition(linq_st_val,";")
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                        else:
                                             
                                             if lexx.lookahead(1)[0].type == "SET" : 
                                                  lexx.nextToken("SET")
                                                  
                                                  python_runtime._append2(lexx.nextToken("ID"),linq_st_values)
                                                  
                                                  lexx.nextToken("EQUAL")
                                                  
                                                  python_runtime._append2(source(),linq_st_values)
                                                  
                                                  
                                                  if linq_st_values[0].value not in defined_ids : 
                                                       linq_st_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(linq_st_val,"setvar "),linq_st_values[0].value),";")
                                                       
                                                       
                                                       python_runtime._append2((linq_st_values[0].value),defined_ids)
                                                       
                                                       
                                                       
                                                  
                                                  
                                                  
                                                  
                                                  linq_st_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(linq_st_val,linq_st_values[0].value),"="),linq_st_values[1])
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                             else:
                                                  python_runtime._append2(boolexp(),linq_st_values)
                                                  
                                                  linq_st_val = linq_st_values[0]
                                                  
                                                  
                                                  
                                                  
                                             
                                             
                                             
                                             
                                             
                                        
                                        
                                        
                                        
                                        
                                   
                                   
                                   
                                   
                                   
                              
                              
                              
                              
                              
                         
                         
                         
                         
                         
                    
                    
                    
                    
                    
               
               
               
               
               
          
          
          
          
          
     
     
     
     
     return linq_st_val
     
     
     
     
     
     

def source ( ):
     source_values = []
     
     
     
     global linq_operators
     
     source_val = ""
     
     
     
     if lexx.lookahead(1)[0].type == "FILE" : 
          lexx.nextToken("FILE")
          
          python_runtime._append2(lexx.nextToken("STRING"),source_values)
          
          
          if lexx.lookahead(1)[0].type == "AS" : 
               lexx.nextToken("AS")
               
               python_runtime._append2(lexx.nextToken("CSV"),source_values)
               
               python_runtime._append2(lexx.nextToken("STRING"),source_values)
               
               _print("as csv!!")
               
               
               
               
               
          
          
          
          
          
          if _size(source_values) == 1 : 
               source_val = python_runtime.doAddition(python_runtime.doAddition("linq(openfile(",source_values[0].value),"))")
               
               
               
          else:
               source_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("linq(openfile(",source_values[0].value),","),source_values[2].value),"))")
               
               
               
          
          
          
          
          
          
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "ARROW" : 
               lexx.nextToken("ARROW")
               
               python_runtime._append2(lexx.nextToken("ID"),source_values)
               
               python_runtime._append2(linqoperator(),source_values)
               
               python_runtime._append2(source_item(),source_values)
               
               
               while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "ARROW" : 
                    lexx.nextToken("ARROW")
                    
                    python_runtime._append2(linqoperator(),source_values)
                    
                    python_runtime._append2(source_item(),source_values)
                    
                    
                    
                    
               
               
               
               source_val = source_values[0].value
               
               
               for item in (list(itertools.chain(source_values))[ 1: None]
               ): 
                    
                    if _strip(item,"%") in linq_operators : 
                         source_val = python_runtime.doAddition(python_runtime.doAddition(source_val,"."),item)
                         
                         
                         
                    else:
                         
                         if _strip(item,"%") == "." : 
                              source_val = python_runtime.doAddition(source_val,"()")
                              
                              
                              
                         else:
                              source_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(source_val,"("),item),")")
                              
                              
                              
                         
                         
                         
                         
                         
                    
                    
                    
                    
                    
               
               
               
               
               
               
               
               
               
          else:
               python_runtime._append2(boolexp(),source_values)
               
               source_val = source_values[0]
               
               
               
               
          
          
          
          
          
     
     
     
     
     return source_val
     
     
     
     
     
     

def source_item ( ):
     source_item_values = []
     
     
     
     source_item_val = ""
     
     
     
     if lexx.lookahead(1)[0].type == "DOT" : 
          python_runtime._append2(lexx.nextToken("DOT"),source_item_values)
          
          source_item_val = "."
          
          
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "INTEGER" : 
               python_runtime._append2(lexx.nextToken("INTEGER"),source_item_values)
               
               source_item_val = "33333333"
               
               
               
               
          else:
               
               if lexx.lookahead(1)[0].type == "FLOAT" : 
                    python_runtime._append2(lexx.nextToken("FLOAT"),source_item_values)
                    
                    source_item_val = "458970.55555555"
                    
                    
                    
                    
               else:
                    
                    if lexx.lookahead(1)[0].type == "TEXT" : 
                         python_runtime._append2(lexx.nextToken("TEXT"),source_item_values)
                         
                         source_item_val = "\"xyz\""
                         
                         
                         
                         
                    else:
                         python_runtime._append2(boolexp(),source_item_values)
                         
                         
                         while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "COMMA" : 
                              lexx.nextToken("COMMA")
                              
                              python_runtime._append2(boolexp(),source_item_values)
                              
                              
                              
                         
                         
                         
                         source_item_val = _join(source_item_values,",")
                         
                         
                         
                         
                         
                    
                    
                    
                    
                    
               
               
               
               
               
          
          
          
          
          
     
     
     
     
     return source_item_val
     
     
     
     
     

def idlist ( ):
     idlist_values = []
     
     
     
     idlist_val = ""
     
     
     python_runtime._append2(lexx.nextToken("ID"),idlist_values)
     
     
     while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "COMMA" : 
          lexx.nextToken("COMMA")
          
          python_runtime._append2(lexx.nextToken("ID"),idlist_values)
          
          
          
     
     
     
     
     if _size(idlist_values) == 1 : 
          idlist_val = idlist_values[0].value
          
          
          
     else:
          idlist_val = reduce(lambda x,y: python_runtime.doAddition(python_runtime.doAddition(x.value,","),y.value),itertools.chain(idlist_values))
          
          
          
     
     
     
     
     return idlist_val
     
     
     
     
     
     
     

def linqoperator ( ):
     linqoperator_values = []
     
     
     
     linqoperator_val = ""
     
     
     
     if lexx.lookahead(1)[0].type == "SELECT" : 
          python_runtime._append2(lexx.nextToken("SELECT"),linqoperator_values)
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "SELECTMANY" : 
               python_runtime._append2(lexx.nextToken("SELECTMANY"),linqoperator_values)
               
               
          else:
               
               if lexx.lookahead(1)[0].type == "WHERE" : 
                    python_runtime._append2(lexx.nextToken("WHERE"),linqoperator_values)
                    
                    
               else:
                    
                    if lexx.lookahead(1)[0].type == "ORDERBY" : 
                         python_runtime._append2(lexx.nextToken("ORDERBY"),linqoperator_values)
                         
                         
                    else:
                         
                         if lexx.lookahead(1)[0].type == "ORDERBYDESCENDING" : 
                              python_runtime._append2(lexx.nextToken("ORDERBYDESCENDING"),linqoperator_values)
                              
                              
                         else:
                              
                              if lexx.lookahead(1)[0].type == "THENBY" : 
                                   python_runtime._append2(lexx.nextToken("THENBY"),linqoperator_values)
                                   
                                   
                              else:
                                   
                                   if lexx.lookahead(1)[0].type == "THENBYDESCENDING" : 
                                        python_runtime._append2(lexx.nextToken("THENBYDESCENDING"),linqoperator_values)
                                        
                                        
                                   else:
                                        
                                        if lexx.lookahead(1)[0].type == "ANY" : 
                                             python_runtime._append2(lexx.nextToken("ANY"),linqoperator_values)
                                             
                                             
                                        else:
                                             
                                             if lexx.lookahead(1)[0].type == "FIRST" : 
                                                  python_runtime._append2(lexx.nextToken("FIRST"),linqoperator_values)
                                                  
                                                  
                                             else:
                                                  
                                                  if lexx.lookahead(1)[0].type == "LAST" : 
                                                       python_runtime._append2(lexx.nextToken("LAST"),linqoperator_values)
                                                       
                                                       
                                                  else:
                                                       
                                                       if lexx.lookahead(1)[0].type == "SINGLE" : 
                                                            python_runtime._append2(lexx.nextToken("SINGLE"),linqoperator_values)
                                                            
                                                            
                                                       else:
                                                            
                                                            if lexx.lookahead(1)[0].type == "GROUPBY" : 
                                                                 python_runtime._append2(lexx.nextToken("GROUPBY"),linqoperator_values)
                                                                 
                                                                 
                                                            else:
                                                                 
                                                                 if lexx.lookahead(1)[0].type == "TAKE" : 
                                                                      python_runtime._append2(lexx.nextToken("TAKE"),linqoperator_values)
                                                                      
                                                                      
                                                                 else:
                                                                      
                                                                      if lexx.lookahead(1)[0].type == "TAKEWHILE" : 
                                                                           python_runtime._append2(lexx.nextToken("TAKEWHILE"),linqoperator_values)
                                                                           
                                                                           
                                                                      else:
                                                                           
                                                                           if lexx.lookahead(1)[0].type == "SKIP" : 
                                                                                python_runtime._append2(lexx.nextToken("SKIP"),linqoperator_values)
                                                                                
                                                                                
                                                                           else:
                                                                                
                                                                                if lexx.lookahead(1)[0].type == "SKIPWHILE" : 
                                                                                     python_runtime._append2(lexx.nextToken("SKIPWHILE"),linqoperator_values)
                                                                                     
                                                                                     
                                                                                else:
                                                                                     
                                                                                     if lexx.lookahead(1)[0].type == "ALL" : 
                                                                                          python_runtime._append2(lexx.nextToken("ALL"),linqoperator_values)
                                                                                          
                                                                                          
                                                                                     else:
                                                                                          
                                                                                          if lexx.lookahead(1)[0].type == "JOIN" : 
                                                                                               python_runtime._append2(lexx.nextToken("JOIN"),linqoperator_values)
                                                                                               
                                                                                               
                                                                                          else:
                                                                                               
                                                                                               if lexx.lookahead(1)[0].type == "GROUPJOIN" : 
                                                                                                    python_runtime._append2(lexx.nextToken("GROUPJOIN"),linqoperator_values)
                                                                                                    
                                                                                                    
                                                                                               else:
                                                                                                    
                                                                                                    if lexx.lookahead(1)[0].type == "REVERSE" : 
                                                                                                         python_runtime._append2(lexx.nextToken("REVERSE"),linqoperator_values)
                                                                                                         
                                                                                                         
                                                                                                    else:
                                                                                                         
                                                                                                         if lexx.lookahead(1)[0].type == "INTERSECT" : 
                                                                                                              python_runtime._append2(lexx.nextToken("INTERSECT"),linqoperator_values)
                                                                                                              
                                                                                                              
                                                                                                         else:
                                                                                                              
                                                                                                              if lexx.lookahead(1)[0].type == "UNION" : 
                                                                                                                   python_runtime._append2(lexx.nextToken("UNION"),linqoperator_values)
                                                                                                                   
                                                                                                                   
                                                                                                              else:
                                                                                                                   
                                                                                                                   if lexx.lookahead(1)[0].type == "DISTINCT" : 
                                                                                                                        python_runtime._append2(lexx.nextToken("DISTINCT"),linqoperator_values)
                                                                                                                        
                                                                                                                        
                                                                                                                   else:
                                                                                                                        
                                                                                                                        if lexx.lookahead(1)[0].type == "EXCEPT" : 
                                                                                                                             python_runtime._append2(lexx.nextToken("EXCEPT"),linqoperator_values)
                                                                                                                             
                                                                                                                             
                                                                                                                        else:
                                                                                                                             
                                                                                                                             if lexx.lookahead(1)[0].type == "ZIP" : 
                                                                                                                                  python_runtime._append2(lexx.nextToken("ZIP"),linqoperator_values)
                                                                                                                                  
                                                                                                                                  
                                                                                                                             else:
                                                                                                                                  
                                                                                                                                  if lexx.lookahead(1)[0].type == "CONCAT" : 
                                                                                                                                       python_runtime._append2(lexx.nextToken("CONCAT"),linqoperator_values)
                                                                                                                                       
                                                                                                                                       
                                                                                                                                  else:
                                                                                                                                       
                                                                                                                                       if lexx.lookahead(1)[0].type == "CONTAINS" : 
                                                                                                                                            python_runtime._append2(lexx.nextToken("CONTAINS"),linqoperator_values)
                                                                                                                                            
                                                                                                                                            
                                                                                                                                       else:
                                                                                                                                            
                                                                                                                                            if lexx.lookahead(1)[0].type == "COUNT" : 
                                                                                                                                                 python_runtime._append2(lexx.nextToken("COUNT"),linqoperator_values)
                                                                                                                                                 
                                                                                                                                                 
                                                                                                                                            else:
                                                                                                                                                 
                                                                                                                                                 if lexx.lookahead(1)[0].type == "AGGREGATE" : 
                                                                                                                                                      python_runtime._append2(lexx.nextToken("AGGREGATE"),linqoperator_values)
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                 else:
                                                                                                                                                      
                                                                                                                                                      if lexx.lookahead(1)[0].type == "DEFAULTIFEMPTY" : 
                                                                                                                                                           python_runtime._append2(lexx.nextToken("DEFAULTIFEMPTY"),linqoperator_values)
                                                                                                                                                           
                                                                                                                                                           
                                                                                                                                                      else:
                                                                                                                                                           
                                                                                                                                                           if lexx.lookahead(1)[0].type == "SEQUENCEEQUAL" : 
                                                                                                                                                                python_runtime._append2(lexx.nextToken("SEQUENCEEQUAL"),linqoperator_values)
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                           else:
                                                                                                                                                                
                                                                                                                                                                if lexx.lookahead(1)[0].type == "TOLIST" : 
                                                                                                                                                                     python_runtime._append2(lexx.nextToken("TOLIST"),linqoperator_values)
                                                                                                                                                                     
                                                                                                                                                                     
                                                                                                                                                                else:
                                                                                                                                                                     
                                                                                                                                                                     if lexx.lookahead(1)[0].type == "TODICTIONARY" : 
                                                                                                                                                                          python_runtime._append2(lexx.nextToken("TODICTIONARY"),linqoperator_values)
                                                                                                                                                                          
                                                                                                                                                                          
                                                                                                                                                                     else:
                                                                                                                                                                          
                                                                                                                                                                          if lexx.lookahead(1)[0].type == "TOLOOKUP" : 
                                                                                                                                                                               python_runtime._append2(lexx.nextToken("TOLOOKUP"),linqoperator_values)
                                                                                                                                                                               
                                                                                                                                                                               
                                                                                                                                                                          else:
                                                                                                                                                                               
                                                                                                                                                                               if lexx.lookahead(1)[0].type == "FOREACH" : 
                                                                                                                                                                                    python_runtime._append2(lexx.nextToken("FOREACH"),linqoperator_values)
                                                                                                                                                                                    
                                                                                                                                                                                    
                                                                                                                                                                               else:
                                                                                                                                                                                    
                                                                                                                                                                                    if lexx.lookahead(1)[0].type == "SUM" : 
                                                                                                                                                                                         python_runtime._append2(lexx.nextToken("SUM"),linqoperator_values)
                                                                                                                                                                                         
                                                                                                                                                                                         
                                                                                                                                                                                    else:
                                                                                                                                                                                         
                                                                                                                                                                                         if lexx.lookahead(1)[0].type == "AVERAGE" : 
                                                                                                                                                                                              python_runtime._append2(lexx.nextToken("AVERAGE"),linqoperator_values)
                                                                                                                                                                                              
                                                                                                                                                                                              
                                                                                                                                                                                         else:
                                                                                                                                                                                              
                                                                                                                                                                                              if lexx.lookahead(1)[0].type == "MAX" : 
                                                                                                                                                                                                   python_runtime._append2(lexx.nextToken("MAX"),linqoperator_values)
                                                                                                                                                                                                   
                                                                                                                                                                                                   
                                                                                                                                                                                              else:
                                                                                                                                                                                                   
                                                                                                                                                                                                   if lexx.lookahead(1)[0].type == "MIN" : 
                                                                                                                                                                                                        python_runtime._append2(lexx.nextToken("MIN"),linqoperator_values)
                                                                                                                                                                                                        
                                                                                                                                                                                                        
                                                                                                                                                                                                   else:
                                                                                                                                                                                                        
                                                                                                                                                                                                        if lexx.lookahead(1)[0].type == "RANGE" : 
                                                                                                                                                                                                             python_runtime._append2(lexx.nextToken("RANGE"),linqoperator_values)
                                                                                                                                                                                                             
                                                                                                                                                                                                             
                                                                                                                                                                                                        else:
                                                                                                                                                                                                             
                                                                                                                                                                                                             if lexx.lookahead(1)[0].type == "REPEAT" : 
                                                                                                                                                                                                                  python_runtime._append2(lexx.nextToken("REPEAT"),linqoperator_values)
                                                                                                                                                                                                                  
                                                                                                                                                                                                                  
                                                                                                                                                                                                             else:
                                                                                                                                                                                                                  
                                                                                                                                                                                                                  if lexx.lookahead(1)[0].type == "CONVERT" : 
                                                                                                                                                                                                                       python_runtime._append2(lexx.nextToken("CONVERT"),linqoperator_values)
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
                                                                                                                                                                                                                  else:
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       if lexx.lookahead(1)[0].type == "OFTYPE" : 
                                                                                                                                                                                                                            python_runtime._append2(lexx.nextToken("OFTYPE"),linqoperator_values)
                                                                                                                                                                                                                            
                                                                                                                                                                                                                            
                                                                                                                                                                                                                       else:
                                                                                                                                                                                                                            
                                                                                                                                                                                                                            if lexx.lookahead(1)[0].type == "ELEMENTAT" : 
                                                                                                                                                                                                                                 python_runtime._append2(lexx.nextToken("ELEMENTAT"),linqoperator_values)
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                 if lexx.lookahead(1)[0].type == "EMPTY" : 
                                                                                                                                                                                                                                      python_runtime._append2(lexx.nextToken("EMPTY"),linqoperator_values)
                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                 else:
                                                                                                                                                                                                                                      raise Exception("Error parsing options: No viable alternative for discriminate this options.")
                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                            
                                                                                                                                                                                                                            
                                                                                                                                                                                                                            
                                                                                                                                                                                                                            
                                                                                                                                                                                                                            
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
                                                                                                                                                                                                                  
                                                                                                                                                                                                                  
                                                                                                                                                                                                                  
                                                                                                                                                                                                                  
                                                                                                                                                                                                                  
                                                                                                                                                                                                             
                                                                                                                                                                                                             
                                                                                                                                                                                                             
                                                                                                                                                                                                             
                                                                                                                                                                                                             
                                                                                                                                                                                                        
                                                                                                                                                                                                        
                                                                                                                                                                                                        
                                                                                                                                                                                                        
                                                                                                                                                                                                        
                                                                                                                                                                                                   
                                                                                                                                                                                                   
                                                                                                                                                                                                   
                                                                                                                                                                                                   
                                                                                                                                                                                                   
                                                                                                                                                                                              
                                                                                                                                                                                              
                                                                                                                                                                                              
                                                                                                                                                                                              
                                                                                                                                                                                              
                                                                                                                                                                                         
                                                                                                                                                                                         
                                                                                                                                                                                         
                                                                                                                                                                                         
                                                                                                                                                                                         
                                                                                                                                                                                    
                                                                                                                                                                                    
                                                                                                                                                                                    
                                                                                                                                                                                    
                                                                                                                                                                                    
                                                                                                                                                                               
                                                                                                                                                                               
                                                                                                                                                                               
                                                                                                                                                                               
                                                                                                                                                                               
                                                                                                                                                                          
                                                                                                                                                                          
                                                                                                                                                                          
                                                                                                                                                                          
                                                                                                                                                                          
                                                                                                                                                                     
                                                                                                                                                                     
                                                                                                                                                                     
                                                                                                                                                                     
                                                                                                                                                                     
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                           
                                                                                                                                                           
                                                                                                                                                           
                                                                                                                                                           
                                                                                                                                                           
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                 
                                                                                                                                                 
                                                                                                                                                 
                                                                                                                                                 
                                                                                                                                                 
                                                                                                                                            
                                                                                                                                            
                                                                                                                                            
                                                                                                                                            
                                                                                                                                            
                                                                                                                                       
                                                                                                                                       
                                                                                                                                       
                                                                                                                                       
                                                                                                                                       
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                             
                                                                                                                             
                                                                                                                             
                                                                                                                             
                                                                                                                             
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                   
                                                                                                                   
                                                                                                                   
                                                                                                                   
                                                                                                                   
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                          
                                                                                          
                                                                                          
                                                                                          
                                                                                          
                                                                                     
                                                                                     
                                                                                     
                                                                                     
                                                                                     
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
                                                                           
                                                                           
                                                                           
                                                                           
                                                                           
                                                                      
                                                                      
                                                                      
                                                                      
                                                                      
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                            
                                                            
                                                            
                                                            
                                                            
                                                       
                                                       
                                                       
                                                       
                                                       
                                                  
                                                  
                                                  
                                                  
                                                  
                                             
                                             
                                             
                                             
                                             
                                        
                                        
                                        
                                        
                                        
                                   
                                   
                                   
                                   
                                   
                              
                              
                              
                              
                              
                         
                         
                         
                         
                         
                    
                    
                    
                    
                    
               
               
               
               
               
          
          
          
          
          
     
     
     
     
     linqoperator_val = python_runtime.doAddition(python_runtime.doAddition("%",_strip(linqoperator_values[0].value)),"%")
     
     
     
     if linqoperator_val == "except" : 
          linqoperator_val = "except_"
          
          
          
     
     
     
     
     return linqoperator_val
     
     
     
     
     
     
     

def boolexp ( ):
     boolexp_values = []
     
     
     
     boolexp_val = ""
     
     
     python_runtime._append2(orexp(),boolexp_values)
     
     
     while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "AND" : 
          python_runtime._append2(lexx.nextToken("AND"),boolexp_values)
          
          python_runtime._append2(orexp(),boolexp_values)
          
          
          
     
     
     
     for item in boolexp_values: 
          
          if _type(item) == _type(token()) : 
               boolexp_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(boolexp_val,"  "),item.value)," ")
               
               
               
          else:
               boolexp_val = python_runtime.doAddition(boolexp_val,item)
               
               
               
          
          
          
          
          
     
     
     return boolexp_val
     
     
     
     
     
     

def orexp ( ):
     orexp_values = []
     
     
     
     orexp_val = ""
     
     
     python_runtime._append2(notexp(),orexp_values)
     
     
     while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "OR" : 
          python_runtime._append2(lexx.nextToken("OR"),orexp_values)
          
          python_runtime._append2(notexp(),orexp_values)
          
          
          
     
     
     
     for item in orexp_values: 
          
          if _type(item) == _type(token()) : 
               orexp_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(orexp_val," "),item.value)," ")
               
               
               
          else:
               orexp_val = python_runtime.doAddition(orexp_val,item)
               
               
               
          
          
          
          
          
     
     
     return orexp_val
     
     
     
     
     
     

def notexp ( ):
     notexp_values = []
     
     
     
     notexp_val = ""
     
     
     
     if lexx.lookahead(1)[0].type == "NOT" : 
          python_runtime._append2(lexx.nextToken("NOT"),notexp_values)
          
          python_runtime._append2(cmpexp(),notexp_values)
          
          notexp_val = python_runtime.doAddition(" not ",notexp_values[1])
          
          
          
          
          
     else:
          python_runtime._append2(cmpexp(),notexp_values)
          
          notexp_val = notexp_values[0]
          
          
          
          
     
     
     
     
     return notexp_val
     
     
     
     
     

def cmpexp ( ):
     cmpexp_values = []
     
     
     
     cmpexp_val = ""
     
     
     python_runtime._append2(expr(),cmpexp_values)
     
     
     while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "BOOLOP" : 
          python_runtime._append2(lexx.nextToken("BOOLOP"),cmpexp_values)
          
          python_runtime._append2(expr(),cmpexp_values)
          
          
          
     
     
     
     for item in cmpexp_values: 
          
          if _type(item) == _type(token()) : 
               cmpexp_val = python_runtime.doAddition(cmpexp_val,item.value)
               
               
               
          else:
               cmpexp_val = python_runtime.doAddition(cmpexp_val,item)
               
               
               
          
          
          
          
          
     
     
     return cmpexp_val
     
     
     
     
     
     

def expr ( ):
     expr_values = []
     
     
     
     expr_val = ""
     
     
     python_runtime._append2(term(),expr_values)
     
     
     while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "PLUSMIN" : 
          python_runtime._append2(lexx.nextToken("PLUSMIN"),expr_values)
          
          python_runtime._append2(expr(),expr_values)
          
          
          
     
     
     
     for item in expr_values: 
          
          if _type(item) == _type(token()) : 
               expr_val = python_runtime.doAddition(expr_val,item.value)
               
               
               
          else:
               expr_val = python_runtime.doAddition(expr_val,item)
               
               
               
          
          
          
          
          
     
     
     return expr_val
     
     
     
     
     
     

def term ( ):
     term_values = []
     
     
     
     term_val = ""
     
     
     python_runtime._append2(exp(),term_values)
     
     
     while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "TIMESDIV" : 
          python_runtime._append2(lexx.nextToken("TIMESDIV"),term_values)
          
          python_runtime._append2(exp(),term_values)
          
          
          
     
     
     
     for item in term_values: 
          
          if _type(item) == _type(token()) : 
               term_val = python_runtime.doAddition(term_val,item.value)
               
               
               
          else:
               term_val = python_runtime.doAddition(term_val,item)
               
               
               
          
          
          
          
          
     
     
     return term_val
     
     
     
     
     
     

def exp ( ):
     exp_values = []
     
     
     
     exp_val = ""
     
     
     python_runtime._append2(factor(),exp_values)
     
     
     while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "EXP" : 
          python_runtime._append2(lexx.nextToken("EXP"),exp_values)
          
          python_runtime._append2(factor(),exp_values)
          
          
          
     
     
     
     for item in exp_values: 
          
          if _type(item) == _type(token()) : 
               exp_val = python_runtime.doAddition(exp_val,"**")
               
               
               
          else:
               exp_val = python_runtime.doAddition(exp_val,item)
               
               
               
          
          
          
          
          
     
     
     return exp_val
     
     
     
     
     
     

def factor ( ):
     factor_values = []
     
     
     
     facval = ""
     
     
     
     if lexx.lookahead(1)[0].type == "PLUSMIN" : 
          python_runtime._append2(lexx.nextToken("PLUSMIN"),factor_values)
          
          python_runtime._append2(expr(),factor_values)
          
          facval = python_runtime.doAddition(factor_values[0].value,factor_values[1])
          
          
          
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "NUMBER" : 
               python_runtime._append2(lexx.nextToken("NUMBER"),factor_values)
               
               facval = factor_values[0].value
               
               
               
               
          else:
               
               if lexx.lookahead(1)[0].type == "ID" : 
                    python_runtime._append2(lexx.nextToken("ID"),factor_values)
                    
                    
                    while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "DOT" : 
                         python_runtime._append2(lexx.nextToken("DOT"),factor_values)
                         
                         python_runtime._append2(lexx.nextToken("ID"),factor_values)
                         
                         
                         
                    
                    
                    
                    facval = factor_values[0].value
                    
                    
                    
                    if _size(factor_values) > 1 : 
                         i = 1
                         while i < _size(factor_values) :
                              facval = python_runtime.doAddition(facval,factor_values[i].value)
                              
                              
                              
                              i+=1
                         
                         
                         
                    
                    
                    
                    
                    
                    
                    
                    
               else:
                    
                    if lexx.lookahead(1)[0].type == "STRING" : 
                         python_runtime._append2(lexx.nextToken("STRING"),factor_values)
                         
                         facval = factor_values[0].value
                         
                         
                         
                         
                    else:
                         
                         if lexx.lookahead(1)[0].type == "PIPE" : 
                              lexx.nextToken("PIPE")
                              
                              python_runtime._append2(arglist(),factor_values)
                              
                              lexx.nextToken("PIPE")
                              
                              lexx.nextToken("COLON")
                              
                              python_runtime._append2(boolexp(),factor_values)
                              
                              facval = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("|(",_replace(factor_values[0],"@","")),"): "),factor_values[1]),"|")
                              
                              
                              
                              
                              
                              
                              
                              
                         else:
                              
                              if lexx.lookahead(1)[0].type == "LPAREN" : 
                                   lexx.nextToken("LPAREN")
                                   
                                   python_runtime._append2(boolexp(),factor_values)
                                   
                                   lexx.nextToken("RPAREN")
                                   
                                   facval = python_runtime.doAddition(python_runtime.doAddition("(",factor_values[0]),")")
                                   
                                   
                                   
                                   
                                   
                                   
                              else:
                                   
                                   if lexx.lookahead(1)[0].type == "CALL" : 
                                        python_runtime._append2(lexx.nextToken("CALL"),factor_values)
                                        
                                        python_runtime._append2(funcall(),factor_values)
                                        
                                        facval = factor_values[1]
                                        
                                        
                                        
                                        
                                        
                                   else:
                                        
                                        if lexx.lookahead(1)[0].type == "GET" : 
                                             lexx.nextToken("GET")
                                             
                                             python_runtime._append2(lexx.nextToken("ID"),factor_values)
                                             
                                             
                                             while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "DOT" : 
                                                  python_runtime._append2(lexx.nextToken("DOT"),factor_values)
                                                  
                                                  python_runtime._append2(lexx.nextToken("ID"),factor_values)
                                                  
                                                  
                                                  
                                             
                                             
                                             
                                             python_runtime._append2(lexx.nextToken("LBRACK"),factor_values)
                                             
                                             python_runtime._append2(expr(),factor_values)
                                             
                                             python_runtime._append2(lexx.nextToken("RBRACK"),factor_values)
                                             
                                             
                                             while lexx.lookahead(1) and lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "LBRACK" : 
                                                  python_runtime._append2(lexx.nextToken("LBRACK"),factor_values)
                                                  
                                                  python_runtime._append2(expr(),factor_values)
                                                  
                                                  python_runtime._append2(lexx.nextToken("RBRACK"),factor_values)
                                                  
                                                  
                                                  
                                                  
                                             
                                             
                                             
                                             i = 0
                                             while i < _size(factor_values)-1 :
                                                  
                                                  if _type(factor_values[i]) == _type(token()) : 
                                                       facval = python_runtime.doAddition(facval,factor_values[i].value)
                                                       
                                                       
                                                       
                                                  else:
                                                       facval = python_runtime.doAddition(facval,factor_values[i])
                                                       
                                                       
                                                       
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  i+=1
                                             
                                             
                                             facval = python_runtime.doAddition(facval,"]")
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                        else:
                                             
                                             if lexx.lookahead(2)[0].type == "LBRACK" and lexx.lookahead(2)[1].type == "RBRACK" : 
                                                  python_runtime._append2(lexx.nextToken("LBRACK"),factor_values)
                                                  
                                                  python_runtime._append2(lexx.nextToken("RBRACK"),factor_values)
                                                  
                                                  facval = "[]"
                                                  
                                                  
                                                  
                                                  
                                                  
                                             else:
                                                  
                                                  if lexx.lookahead(2)[0].type == "LBRACK" : 
                                                       python_runtime._append2(lexx.nextToken("LBRACK"),factor_values)
                                                       
                                                       python_runtime._append2(expr(),factor_values)
                                                       
                                                       
                                                       while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "COMMA" : 
                                                            lexx.nextToken("COMMA")
                                                            
                                                            python_runtime._append2(expr(),factor_values)
                                                            
                                                            
                                                            
                                                       
                                                       
                                                       
                                                       python_runtime._append2(lexx.nextToken("RBRACK"),factor_values)
                                                       
                                                       facval = python_runtime.doAddition(python_runtime.doAddition("[",_join((filter(lambda x: _type(x) != _type(token()),list(itertools.chain(factor_values)))),",")),"]")
                                                       
                                                       
                                                       
                                                       
                                                       
                                                       
                                                       
                                                  else:
                                                       
                                                       if lexx.lookahead(2)[0].type == "LCURLY" and lexx.lookahead(2)[1].type == "RCURLY" : 
                                                            lexx.nextToken("LCURLY")
                                                            
                                                            lexx.nextToken("RCURLY")
                                                            
                                                            facval = "{}"
                                                            
                                                            
                                                            
                                                            
                                                            
                                                       else:
                                                            
                                                            if lexx.lookahead(2)[0].type == "LCURLY" : 
                                                                 lexx.nextToken("LCURLY")
                                                                 
                                                                 python_runtime._append2(pair(),factor_values)
                                                                 
                                                                 
                                                                 while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "COMMA" : 
                                                                      lexx.nextToken("COMMA")
                                                                      
                                                                      python_runtime._append2(pair(),factor_values)
                                                                      
                                                                      
                                                                      
                                                                 
                                                                 
                                                                 
                                                                 lexx.nextToken("RCURLY")
                                                                 
                                                                 facval = python_runtime.doAddition(python_runtime.doAddition("{",_join(factor_values,",")),"}")
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                            else:
                                                                 
                                                                 if lexx.lookahead(1)[0].type == "QUESTION" : 
                                                                      lexx.nextToken("QUESTION")
                                                                      
                                                                      python_runtime._append2(boolexp(),factor_values)
                                                                      
                                                                      lexx.nextToken("ARROW")
                                                                      
                                                                      python_runtime._append2(expr(),factor_values)
                                                                      
                                                                      lexx.nextToken("COLON")
                                                                      
                                                                      python_runtime._append2(expr(),factor_values)
                                                                      
                                                                      facval = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(factor_values[1]," if "),factor_values[0])," else "),factor_values[2])
                                                                      
                                                                      
                                                                      
                                                                      
                                                                      
                                                                      
                                                                      
                                                                      
                                                                      
                                                                 else:
                                                                      raise Exception("Error parsing options: No viable alternative for discriminate this options.")
                                                                      
                                                                      
                                                                      
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                            
                                                            
                                                            
                                                            
                                                            
                                                       
                                                       
                                                       
                                                       
                                                       
                                                  
                                                  
                                                  
                                                  
                                                  
                                             
                                             
                                             
                                             
                                             
                                        
                                        
                                        
                                        
                                        
                                   
                                   
                                   
                                   
                                   
                              
                              
                              
                              
                              
                         
                         
                         
                         
                         
                    
                    
                    
                    
                    
               
               
               
               
               
          
          
          
          
          
     
     
     
     
     return facval
     
     
     
     
     

def funcall ( ):
     funcall_values = []
     
     
     
     funcall_val = ""
     
     
     
     if lexx.lookahead(1)[0].type == "ID" : 
          python_runtime._append2(lexx.nextToken("ID"),funcall_values)
          
          
          while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "DOT" : 
               python_runtime._append2(lexx.nextToken("DOT"),funcall_values)
               
               python_runtime._append2(lexx.nextToken("ID"),funcall_values)
               
               
               
          
          
          
          lexx.nextToken("LPAREN")
          
          python_runtime._append2(arglist(),funcall_values)
          
          lexx.nextToken("RPAREN")
          
          
          while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "DOT" : 
               python_runtime._append2(lexx.nextToken("DOT"),funcall_values)
               
               python_runtime._append2(funcall(),funcall_values)
               
               
               
          
          
          
          
          
          
          
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "GET" : 
               lexx.nextToken("GET")
               
               python_runtime._append2(lexx.nextToken("ID"),funcall_values)
               
               
               while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "DOT" : 
                    python_runtime._append2(lexx.nextToken("DOT"),funcall_values)
                    
                    python_runtime._append2(lexx.nextToken("ID"),funcall_values)
                    
                    
                    
               
               
               
               python_runtime._append2(lexx.nextToken("LBRACK"),funcall_values)
               
               python_runtime._append2(expr(),funcall_values)
               
               python_runtime._append2(lexx.nextToken("RBRACK"),funcall_values)
               
               
               while lexx.lookahead(1) and lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "LBRACK" : 
                    python_runtime._append2(lexx.nextToken("LBRACK"),funcall_values)
                    
                    python_runtime._append2(expr(),funcall_values)
                    
                    python_runtime._append2(lexx.nextToken("RBRACK"),funcall_values)
                    
                    
                    
                    
               
               
               
               lexx.nextToken("LPAREN")
               
               python_runtime._append2(arglist(),funcall_values)
               
               lexx.nextToken("RPAREN")
               
               
               
               
               
               
               
               
               
               
               
          else:
               raise Exception("Error parsing options: No viable alternative for discriminate this options.")
               
               
               
          
          
          
          
          
     
     
     
     
     i = 0
     while i < _size(funcall_values)-1 :
          
          if _type(funcall_values[i]) == _type(token()) : 
               funcall_val = python_runtime.doAddition(funcall_val,funcall_values[i].value)
               
               
               
          else:
               
               if funcall_values[i] and funcall_values[i][0] == "@" : 
                    funcall_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(funcall_val,"("),_replace(funcall_values[i],"@","")),")")
                    
                    
                    
               else:
                    funcall_val = python_runtime.doAddition(funcall_val,funcall_values[i])
                    
                    
                    
               
               
               
               
               
          
          
          
          
          
          i+=1
     
     
     
     if funcall_values[i] and funcall_values[-1][0] == "@" : 
          funcall_val = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(funcall_val,"("),_replace(funcall_values[-1],"@","")),")")
          
          
          
     else:
          funcall_val = python_runtime.doAddition(funcall_val,funcall_values[-1])
          
          
          
     
     
     
     
     
     if funcall_val[-1] != ")" : 
          funcall_val = python_runtime.doAddition(funcall_val,"()")
          
          
          
     
     
     
     
     return funcall_val
     
     
     
     
     
     
     
     

def arglist ( ):
     arglist_values = []
     
     
     
     arglist_val = ""
     
     
     
     if lexx.lookahead(1)[0].type == "DOT" : 
          python_runtime._append2(lexx.nextToken("DOT"),arglist_values)
          
          arglist_val = "@"
          
          
          
          
     else:
          python_runtime._append2(expr(),arglist_values)
          
          
          while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "COMMA" : 
               lexx.nextToken("COMMA")
               
               python_runtime._append2(expr(),arglist_values)
               
               
               
          
          
          
          arglist_val = arglist_values[0]
          
          
          
          if _size(arglist_values) > 1 : 
               i = 1
               while i < _size(arglist_values) :
                    arglist_val = python_runtime.doAddition(python_runtime.doAddition(arglist_val,","),arglist_values[i])
                    
                    
                    
                    i=python_runtime.doAddition(i,1)
               
               
               
          
          
          
          
          arglist_val = python_runtime.doAddition("@",arglist_val)
          
          
          
          
          
          
          
     
     
     
     
     return arglist_val
     
     
     
     
     

def pair ( ):
     pair_values = []
     
     
     
     
     if lexx.lookahead(1)[0].type == "NUMBER" : 
          python_runtime._append2(lexx.nextToken("NUMBER"),pair_values)
          
          lexx.nextToken("COLON")
          
          python_runtime._append2(expr(),pair_values)
          
          pairval = python_runtime.doAddition(python_runtime.doAddition(pair_values[0].value,":"),pair_values[1])
          
          
          
          
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "STRING" : 
               python_runtime._append2(lexx.nextToken("STRING"),pair_values)
               
               lexx.nextToken("COLON")
               
               python_runtime._append2(expr(),pair_values)
               
               pairval = python_runtime.doAddition(python_runtime.doAddition(pair_values[0].value,":"),pair_values[1])
               
               
               
               
               
               
          else:
               
               if lexx.lookahead(1)[0].type == "ID" : 
                    python_runtime._append2(lexx.nextToken("ID"),pair_values)
                    
                    lexx.nextToken("COLON")
                    
                    python_runtime._append2(expr(),pair_values)
                    
                    pairval = python_runtime.doAddition(python_runtime.doAddition(pair_values[0].value,":"),pair_values[1])
                    
                    
                    
                    
                    
                    
               else:
                    raise Exception("Error parsing options: No viable alternative for discriminate this options.")
                    
                    
                    
               
               
               
               
               
          
          
          
          
          
     
     
     
     
     return pairval
     
     
     
     


_print("Put your code here")

linqy_orders = []



import random


import time


import cStringIO


random_kinds = {"uniform":random.uniform,"betavar":random.betavariate,"expovar":random.expovariate,"gammavar":random.gammavariate,"normal":random.normalvariate,"lognormal":random.lognormvariate,"vonmises":random.vonmisesvariate,"pareto":random.paretovariate,"weibull":random.weibullvariate}




def randomSample ( numels, kind, p1, p2):
     global random_kinds
     
     samples = []
     
     
     params = []
     
     
     fun = random_kinds[kind]
     
     
     
     if kind in ["expovar","paretovar"] : 
          params = [p1]
          
          
          
     else:
          params = [p1,p2]
          
          
          
     
     
     
     
     i = 0
     while i < numels :
          python_runtime._append2((fun(*params)),samples)
          
          
          i+=1
     
     
     return linq(samples)
     
     
     
     
     
     
     
     

def getRandom ( ):
     return random.random()
     
     

def getRandint ( start, end):
     return random.randint(start,end)
     
     

def getRandomSample ( seq, numels):
     seq = seq.iterable
     
     
     return linq(random.sample(seq,numels))
     
     
     

def strAggregate ( seq, init=""):
     buffer = cStringIO.StringIO()
     
     
     
     if init != "" : 
          buffer.write(init)
          
          
     
     
     
     
     for item in seq: 
          buffer.write(item)
          
          
     
     
     return buffer.getvalue()
     
     
     
     

def checkForBridge ( cad):
     for item in [".where",".select",".take",".count",".foreach",".groupby"]: 
          cad = _replace(cad,item,python_runtime.doAddition(python_runtime.doAddition(".%",item.strip(".")),"%"))
          
          
          
     
     
     return cad
     
     

def dictAdd ( dict, key, value):
     dict[key] = value
     
     
     

def listAdd ( l, value):
     python_runtime._append2(value,l)
     
     

def getIterable ( linq_item):
     return linq_item.iterable
     
     

def queryDB ( kind, db, connstr, query):
     results = None
     
     
     
     if kind == "sqlite" : 
          dbase0=[]
          dbase0_conn=sqlite3.connect(db,isolation_level=None)
          dbase0_cursor=dbase0_conn.cursor()
          dbase0_cursor.execute(query)
          for i in dbase0_cursor:
              if type(i)==type((0,)):
                  dbase0.append(list(i))
              else:
                  dbase0.append(i)
          names = [description[0] for description in dbase0_cursor.description] if dbase0_cursor.description else []
          dbase0_conn.commit()
          dbase0= {"data":dbase0 ,"names": names,"affected":dbase0_cursor.rowcount}
          
          results = dbase0
          
          
          
     else:
          
          if kind == "ado" : 
               dbase1=[]
               dbase1= python_runtime._queryADO(connstr,query)
               
               results = dbase1
               
               
               
          else:
               raise Exception("Linqy Error: Unsupported database type.")
               
               
               
          
          
          
          
          
     
     
     
     
     return results
     
     
     
     


data = ""
lnq = ""



cmdln = _cmdline()



_print(python_runtime.doAddition("cmdline: ",_tostring(cmdln)))


if cmdln == [] : 
     
     while True : 
          data = _input("linqy>")
          
          
          
          if data == ".exit" : 
               break
               
               
          
          
          
          
          lexx.setInput(data)
          
          lnq = linqy()
          
          
          lnq = checkForBridge(lnq)
          
          
          minimal_py.__reflected=1
          exec minimal_py.parser.parse(lnq)
          minimal_py.__reflected=0
          
          
          python_runtime._append2(data,linqy_orders)
          
          
          
          
          
          
          
          
     
     
     
     _print(python_runtime.doAddition("Ordenes ejecutadas en esta sesion:\n",_tostring(linqy_orders)))
     
     
     
else:
     read = _readf(cmdln[0])
     
     
     
     lexx.setInput(read)
     
     lnq = linqy()
     
     
     lnq = checkForBridge(lnq)
     
     
     _print(python_runtime.doAddition("A ejecutar: ",lnq))
     
     minimal_py.__reflected=1
     exec minimal_py.parser.parse(lnq)
     minimal_py.__reflected=0
     
     
     
     
     
     
     
     




























