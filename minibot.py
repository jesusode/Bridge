
from __future__ import division
#Bridge generated code 
import sys
sys.path.append('.')#Para py2exe
sys.path.append('./modules')#Para py2exe
sys.path.append('library.zip')#Para py2exe
#Para evitar el error de desbordamiento que da el parser actual con jython

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
from python_runtime import _find,_strinsert,_regroups,_writef,_writeflines,_foreach,_setencoding
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



table = [["\s+","WHITESPACE",None,False],["\.","DOT",None,False],["define","DEFINE",None,False],["guarda","GUARDA",None,False],["carga","CARGA",None,False],["borra","BORRA",None,False],["muestra","MUESTRA",None,False],["acciones","ACCIONES",None,False],["accion","ACCION",None,False],["como","COMO",None,False],["con","CON",None,False],["comprueba","COMPRUEBA",None,False],["entonces","ENTONCES",None,False],["en","EN",None,False],["si","SI",None,False],["suma","SUMA",None,False],["cambia","CAMBIA",None,False],["macros","MACROS",None,False],["macro","MACRO",None,False],["pregunta","PREGUNTA",None,False],["igual","IGUAL",None,False],["distinto","DISTINTO",None,False],["ultimo","ULTIMO",None,False],["mayor","MAYOR",None,False],["menor","MENOR",None,False],["mientras","MIENTRAS",None,False],["hacer","HACER",None,False],["fin","FIN",None,False],["[a-zA-Z_][a-zA-Z_0-9]+","ID",None,False],["\"[^\"]+\"","STRING",None,False],["\+","PLUS",None,False],["\-","MINUS",None,False],["\*","TIMES",None,False],["/","DIV",None,False],["\^","EXP",None,False],["\(","LPAREN",None,False],["\)","RPAREN",None,False],["\[","LBRACK",None,False],["\]","RBRACK",None,False],["\{","LCURLY",None,False],["\}","RCURLY",None,False],["[0-9]+","NUMBER",None,False],[",","COMMA",None,False],[":","COLON",None,False],["call","CALL",None,False],["get","GET",None,False]]



lexx.setTable(table)

ignore_list = ["WHITESPACE"]



lexx.setIgnore(ignore_list)


def on_enter_bot ( rule_values):
     global lexx
     
     _print("enter bot callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_exit_bot ( rule_values):
     global lexx
     
     _print("exit bot callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_enter_orden ( rule_values):
     global lexx
     
     _print("enter orden callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_exit_orden ( rule_values):
     global lexx
     
     _print("exit orden callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_enter_condexp ( rule_values):
     global lexx
     
     _print("enter condexp callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_exit_condexp ( rule_values):
     global lexx
     
     _print("exit condexp callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_enter_expr ( rule_values):
     global lexx
     
     _print("enter expr callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_exit_expr ( rule_values):
     global lexx
     
     _print("exit expr callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_enter_termtail ( rule_values):
     global lexx
     
     _print("enter termtail callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_exit_termtail ( rule_values):
     global lexx
     
     _print("exit termtail callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_enter_term ( rule_values):
     global lexx
     
     _print("enter term callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_exit_term ( rule_values):
     global lexx
     
     _print("exit term callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_enter_exptail ( rule_values):
     global lexx
     
     _print("enter exptail callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_exit_exptail ( rule_values):
     global lexx
     
     _print("exit exptail callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_enter_exp ( rule_values):
     global lexx
     
     _print("enter exp callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_exit_exp ( rule_values):
     global lexx
     
     _print("exit exp callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_enter_factortail ( rule_values):
     global lexx
     
     _print("enter factortail callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_exit_factortail ( rule_values):
     global lexx
     
     _print("exit factortail callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_enter_factor ( rule_values):
     global lexx
     
     _print("enter factor callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     

def on_exit_factor ( rule_values):
     global lexx
     
     _print("exit factor callback code")
     
     _print(python_runtime.doAddition("REST: ",lexx.getRest()))
     
     
     
     


acciones = {}



macros = {}



uservars = {}



last = ""




def dispatchOrder ( name, _args):
     global acciones,macros
     
     
     if name in _keys(acciones) : 
          runAction(name,_args)
          
          
     else:
          
          if name in _keys(macros) : 
               runMacro(name,_args)
               
               
          else:
               raise Exception(python_runtime.doFormat("Error: {0} no es una orden o macro definida.",[name]))
               
               
               
          
          
          
          
          
     
     
     
     
     
     

def runAction ( name, _args):
     global acciones,last
     
     cmd = acciones[name]
     
     
     
     if _size(_args) > 1 : 
          last = _system(python_runtime.doAddition(python_runtime.doAddition(cmd," "),_strip(_args,"\"")))
          
          
          
     else:
          last = _system(cmd)
          
          
          
     
     
     
     
     
     
     

def runMacro ( name, _args):
     global macros,last
     
     mcr = macros[name]
     
     
     for item in mcr: 
          runAction(item,_args)
          
          
     
     
     
     
     

def updateDictionary ( old, news):
     if not _type(old) == _type({}) and _type(news) == _type({}):
      raise Exception("""assertion error: '_type(old) == _type({}) and _type(news) == _type({})' is false""")
     
     for item in news: 
          old[item] = news[item]
          
          
          
     
     
     



def bot ( ):
     bot_values = []
     
     
     
     on_enter_bot(bot_values)
     
     python_runtime._append2(orden(),bot_values)
     
     lexx.nextToken("DOT")
     
     
     while lexx.lookahead(1) and lexx.lookahead(1)[0].type != "EOF" : 
          python_runtime._append2(orden(),bot_values)
          
          lexx.nextToken("DOT")
          
          
          
     
     
     
     on_exit_bot(bot_values)
     
     return bot_values
     
     
     
     
     
     
     
     

def orden ( ):
     orden_values = []
     
     
     
     on_enter_orden(orden_values)
     
     global acciones,macros,uservars,last
     
     
     if lexx.lookahead(1)[0].type == "MIENTRAS" : 
          lexx.nextToken("MIENTRAS")
          
          python_runtime._append2(condexp(),orden_values)
          
          lexx.nextToken("HACER")
          
          python_runtime._append2(orden(),orden_values)
          
          
          while lexx.lookahead(1)[0].type != "FIN" : 
               python_runtime._append2(orden(),orden_values)
               
               
          
          
          
          lexx.nextToken("FIN")
          
          
          
          
          
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "SI" : 
               lexx.nextToken("SI")
               
               python_runtime._append2(condexp(),orden_values)
               
               lexx.nextToken("ENTONCES")
               
               python_runtime._append2(lexx.nextToken("ID"),orden_values)
               
               
               while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "STRING" : 
                    python_runtime._append2(lexx.nextToken("STRING"),orden_values)
                    
                    
               
               
               
               
               if orden_values[0] == "si" : 
                    args = _cdr(orden_values)
                    
                    
                    ord = _car(args)
                    
                    
                    arg = _cdr(args)
                    
                    
                    
                    if arg != [] : 
                         arg = reduce(lambda x,y: python_runtime.doAddition(python_runtime.doAddition(x," "),y),itertools.chain(list(itertools.imap(lambda x: x.value,list(itertools.chain(arg))))))
                         
                         
                         
                    
                    
                    
                    
                    dispatchOrder(ord.value,arg)
                    
                    
                    
                    
                    
                    
               
               
               
               
               
               
               
               
               
               
          else:
               
               if lexx.lookahead(1)[0].type == "COMPRUEBA" : 
                    lexx.nextToken("COMPRUEBA")
                    
                    python_runtime._append2(condexp(),orden_values)
                    
                    last = orden_values[0]
                    
                    
                    
                    
                    
               else:
                    
                    if lexx.lookahead(1)[0].type == "SUMA" : 
                         lexx.nextToken("SUMA")
                         
                         python_runtime._append2(lexx.nextToken("ID"),orden_values)
                         
                         lexx.nextToken("CON")
                         
                         python_runtime._append2(lexx.nextToken("ID"),orden_values)
                         
                         last = python_runtime.doAddition(uservars[orden_values[0].value],uservars[orden_values[1].value])
                         
                         
                         
                         
                         
                         
                         
                    else:
                         
                         if lexx.lookahead(1)[0].type == "CAMBIA" : 
                              lexx.nextToken("CAMBIA")
                              
                              python_runtime._append2(lexx.nextToken("ID"),orden_values)
                              
                              lexx.nextToken("CON")
                              
                              python_runtime._append2(lexx.nextToken("ID"),orden_values)
                              
                              lexx.nextToken("EN")
                              
                              python_runtime._append2(lexx.nextToken("ID"),orden_values)
                              
                              _print("Cambio de IDs: Pendiente de implementar")
                              
                              
                              
                              
                              
                              
                              
                              
                         else:
                              
                              if lexx.lookahead(1)[0].type == "PREGUNTA" : 
                                   lexx.nextToken("PREGUNTA")
                                   
                                   
                                   if lexx.lookahead(1)[0].type == "STRING" : 
                                        python_runtime._append2(lexx.nextToken("STRING"),orden_values)
                                        
                                        
                                   
                                   
                                   
                                   
                                   python_runtime._append2(lexx.nextToken("ID"),orden_values)
                                   
                                   last = _input(_strip(orden_values[0].value,"\""))
                                   
                                   
                                   uservars[orden_values[1].value] = last
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                              else:
                                   
                                   if lexx.lookahead(1)[0].type == "ULTIMO" : 
                                        python_runtime._append2(lexx.nextToken("ULTIMO"),orden_values)
                                        
                                        _print(python_runtime.doAddition("Ultimo: ",last))
                                        
                                        
                                        
                                   else:
                                        
                                        if lexx.lookahead(2)[0].type == "DEFINE" and lexx.lookahead(2)[1].type == "ACCION" : 
                                             lexx.nextToken("DEFINE")
                                             
                                             lexx.nextToken("ACCION")
                                             
                                             python_runtime._append2(lexx.nextToken("ID"),orden_values)
                                             
                                             lexx.nextToken("COMO")
                                             
                                             python_runtime._append2(lexx.nextToken("STRING"),orden_values)
                                             
                                             acciones[orden_values[0].value] = _strip(orden_values[1].value,"\"")
                                             
                                             
                                             _print(_tostring(acciones))
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                        else:
                                             
                                             if lexx.lookahead(2)[0].type == "DEFINE" and lexx.lookahead(2)[1].type == "MACRO" : 
                                                  lexx.nextToken("DEFINE")
                                                  
                                                  lexx.nextToken("MACRO")
                                                  
                                                  python_runtime._append2(lexx.nextToken("ID"),orden_values)
                                                  
                                                  lexx.nextToken("COMO")
                                                  
                                                  python_runtime._append2(lexx.nextToken("ID"),orden_values)
                                                  
                                                  
                                                  while lexx.lookahead(1) and lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "ID" : 
                                                       python_runtime._append2(lexx.nextToken("ID"),orden_values)
                                                       
                                                       
                                                  
                                                  
                                                  
                                                  _print(python_runtime.doAddition("orden_values: ",_tostring(orden_values)))
                                                  
                                                  macros[orden_values[0].value] = list(itertools.imap(lambda x: x.value,list(itertools.chain(list(itertools.chain(orden_values))[ 1: None]
                                                  ))))
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                             else:
                                                  
                                                  if lexx.lookahead(2)[0].type == "DEFINE" and lexx.lookahead(2)[1].type == "ID" : 
                                                       lexx.nextToken("DEFINE")
                                                       
                                                       python_runtime._append2(lexx.nextToken("ID"),orden_values)
                                                       
                                                       lexx.nextToken("COMO")
                                                       
                                                       python_runtime._append2(lexx.nextToken("ULTIMO"),orden_values)
                                                       
                                                       uservars[orden_values[0].value] = last
                                                       
                                                       
                                                       _print(_tostring(uservars))
                                                       
                                                       
                                                       
                                                       
                                                       
                                                       
                                                       
                                                  else:
                                                       
                                                       if lexx.lookahead(2)[0].type == "GUARDA" and lexx.lookahead(2)[1].type == "ACCIONES" : 
                                                            lexx.nextToken("GUARDA")
                                                            
                                                            lexx.nextToken("ACCIONES")
                                                            
                                                            lexx.nextToken("COMO")
                                                            
                                                            python_runtime._append2(lexx.nextToken("STRING"),orden_values)
                                                            
                                                            python_runtime.doSerialize(acciones,_strip(orden_values[0].value,"\""))
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                       else:
                                                            
                                                            if lexx.lookahead(2)[0].type == "CARGA" and lexx.lookahead(2)[1].type == "ACCIONES" : 
                                                                 lexx.nextToken("CARGA")
                                                                 
                                                                 lexx.nextToken("ACCIONES")
                                                                 
                                                                 lexx.nextToken("COMO")
                                                                 
                                                                 python_runtime._append2(lexx.nextToken("STRING"),orden_values)
                                                                 
                                                                 aux = python_runtime.doDeserialize(_strip(orden_values[0].value,"\""))
                                                                 
                                                                 
                                                                 
                                                                 updateDictionary(acciones,aux)
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                            else:
                                                                 
                                                                 if lexx.lookahead(2)[0].type == "GUARDA" and lexx.lookahead(2)[1].type == "MACROS" : 
                                                                      lexx.nextToken("GUARDA")
                                                                      
                                                                      lexx.nextToken("MACROS")
                                                                      
                                                                      lexx.nextToken("COMO")
                                                                      
                                                                      python_runtime._append2(lexx.nextToken("STRING"),orden_values)
                                                                      
                                                                      python_runtime.doSerialize(macros,_strip(orden_values[0].value,"\""))
                                                                      
                                                                      
                                                                      
                                                                      
                                                                      
                                                                      
                                                                      
                                                                 else:
                                                                      
                                                                      if lexx.lookahead(2)[0].type == "CARGA" and lexx.lookahead(2)[1].type == "MACROS" : 
                                                                           lexx.nextToken("CARGA")
                                                                           
                                                                           lexx.nextToken("MACROS")
                                                                           
                                                                           lexx.nextToken("COMO")
                                                                           
                                                                           python_runtime._append2(lexx.nextToken("STRING"),orden_values)
                                                                           
                                                                           _print("Carga Macros: Pendiente de implementar")
                                                                           
                                                                           
                                                                           
                                                                           
                                                                           
                                                                           
                                                                      else:
                                                                           
                                                                           if lexx.lookahead(2)[0].type == "BORRA" and lexx.lookahead(2)[1].type == "ACCIONES" : 
                                                                                lexx.nextToken("BORRA")
                                                                                
                                                                                lexx.nextToken("ACCIONES")
                                                                                
                                                                                acciones = {}
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
                                                                           else:
                                                                                
                                                                                if lexx.lookahead(2)[0].type == "BORRA" and lexx.lookahead(2)[1].type == "MACROS" : 
                                                                                     lexx.nextToken("BORRA")
                                                                                     
                                                                                     lexx.nextToken("MACROS")
                                                                                     
                                                                                     macros = {}
                                                                                     
                                                                                     
                                                                                     
                                                                                     
                                                                                     
                                                                                else:
                                                                                     
                                                                                     if lexx.lookahead(2)[0].type == "MUESTRA" and lexx.lookahead(2)[1].type == "STRING" : 
                                                                                          lexx.nextToken("MUESTRA")
                                                                                          
                                                                                          python_runtime._append2(lexx.nextToken("STRING"),orden_values)
                                                                                          
                                                                                          _print(_strip(orden_values[0].value,"\""))
                                                                                          
                                                                                          
                                                                                          
                                                                                          
                                                                                     else:
                                                                                          
                                                                                          if lexx.lookahead(2)[0].type == "MUESTRA" and lexx.lookahead(2)[1].type == "ID" : 
                                                                                               lexx.nextToken("MUESTRA")
                                                                                               
                                                                                               python_runtime._append2(lexx.nextToken("ID"),orden_values)
                                                                                               
                                                                                               
                                                                                               if orden_values[0].value in _keys(uservars) : 
                                                                                                    _print(python_runtime.doAddition(python_runtime.doAddition(orden_values[0].value,"  ->  "),uservars[orden_values[0].value]))
                                                                                                    
                                                                                                    
                                                                                               else:
                                                                                                    _print(python_runtime.doFormat("La variable de usuario {0} no esta definida",[orden_values[0].value]))
                                                                                                    
                                                                                                    
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                          else:
                                                                                               
                                                                                               if lexx.lookahead(2)[0].type == "MUESTRA" and lexx.lookahead(2)[1].type == "ACCION" : 
                                                                                                    lexx.nextToken("MUESTRA")
                                                                                                    
                                                                                                    lexx.nextToken("ACCION")
                                                                                                    
                                                                                                    python_runtime._append2(lexx.nextToken("ID"),orden_values)
                                                                                                    
                                                                                                    
                                                                                                    if orden_values[0].value in _keys(acciones) : 
                                                                                                         _print(python_runtime.doAddition(python_runtime.doAddition(orden_values[0].value,"  ->  "),acciones[orden_values[0].value]))
                                                                                                         
                                                                                                         
                                                                                                    else:
                                                                                                         _print(python_runtime.doFormat("La accion {0} no esta definida",[orden_values[0].value]))
                                                                                                         
                                                                                                         
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                               else:
                                                                                                    
                                                                                                    if lexx.lookahead(2)[0].type == "MUESTRA" and lexx.lookahead(2)[1].type == "MACRO" : 
                                                                                                         lexx.nextToken("MUESTRA")
                                                                                                         
                                                                                                         lexx.nextToken("MACRO")
                                                                                                         
                                                                                                         python_runtime._append2(lexx.nextToken("ID"),orden_values)
                                                                                                         
                                                                                                         
                                                                                                         if orden_values[0].value in _keys(macros) : 
                                                                                                              _print(python_runtime.doAddition(python_runtime.doAddition(orden_values[0].value,"  ->  "),_tostring(macros[orden_values[0].value])))
                                                                                                              
                                                                                                              
                                                                                                         else:
                                                                                                              _print(python_runtime.doFormat("La macro {0} no esta definida",[orden_values[0].value]))
                                                                                                              
                                                                                                              
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                    else:
                                                                                                         
                                                                                                         if lexx.lookahead(2)[0].type == "MUESTRA" and lexx.lookahead(2)[1].type == "ACCIONES" : 
                                                                                                              lexx.nextToken("MUESTRA")
                                                                                                              
                                                                                                              lexx.nextToken("ACCIONES")
                                                                                                              
                                                                                                              for item in acciones: 
                                                                                                                   _print(python_runtime.doAddition(python_runtime.doAddition(item,"  ->  "),acciones[item]))
                                                                                                                   
                                                                                                                   
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                         else:
                                                                                                              
                                                                                                              if lexx.lookahead(2)[0].type == "MUESTRA" and lexx.lookahead(2)[1].type == "MACROS" : 
                                                                                                                   lexx.nextToken("MUESTRA")
                                                                                                                   
                                                                                                                   lexx.nextToken("MACROS")
                                                                                                                   
                                                                                                                   for item in macros: 
                                                                                                                        _print(python_runtime.doAddition(python_runtime.doAddition(item,"  ->  "),_tostring(macros[item])))
                                                                                                                        
                                                                                                                        
                                                                                                                   
                                                                                                                   
                                                                                                                   
                                                                                                                   
                                                                                                                   
                                                                                                              else:
                                                                                                                   
                                                                                                                   if lexx.lookahead(2)[0].type == "ID" and lexx.lookahead(2)[1].type == "STRING" : 
                                                                                                                        python_runtime._append2(lexx.nextToken("ID"),orden_values)
                                                                                                                        
                                                                                                                        
                                                                                                                        while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "STRING" : 
                                                                                                                             python_runtime._append2(lexx.nextToken("STRING"),orden_values)
                                                                                                                             
                                                                                                                             
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        args = list(itertools.chain(orden_values))[ 1: None]
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        if args != [] : 
                                                                                                                             args = reduce(lambda x,y: python_runtime.doAddition(python_runtime.doAddition(x," "),y),itertools.chain(list(itertools.imap(lambda x: x.value,list(itertools.chain(args))))))
                                                                                                                             
                                                                                                                             
                                                                                                                             
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        dispatchOrder(orden_values[0].value,args)
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                   else:
                                                                                                                        
                                                                                                                        if lexx.lookahead(2)[0].type == "ID" and lexx.lookahead(2)[1].type == "IGUAL" : 
                                                                                                                             python_runtime._append2(lexx.nextToken("ID"),orden_values)
                                                                                                                             
                                                                                                                             lexx.nextToken("IGUAL")
                                                                                                                             
                                                                                                                             python_runtime._append2(expr(),orden_values)
                                                                                                                             
                                                                                                                             uservars[orden_values[0].value] = _strip(orden_values[1].value,"\"")
                                                                                                                             
                                                                                                                             
                                                                                                                             
                                                                                                                             
                                                                                                                             
                                                                                                                             
                                                                                                                        else:
                                                                                                                             raise Exception("Error parsing options: No viable alternative for discriminate this options.")
                                                                                                                             
                                                                                                                             
                                                                                                                             
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                                                                                   
                                                                                                                   
                                                                                                                   
                                                                                                                   
                                                                                                                   
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                         
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                          
                                                                                          
                                                                                          
                                                                                          
                                                                                          
                                                                                     
                                                                                     
                                                                                     
                                                                                     
                                                                                     
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
                                                                           
                                                                           
                                                                           
                                                                           
                                                                           
                                                                      
                                                                      
                                                                      
                                                                      
                                                                      
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                            
                                                            
                                                            
                                                            
                                                            
                                                       
                                                       
                                                       
                                                       
                                                       
                                                  
                                                  
                                                  
                                                  
                                                  
                                             
                                             
                                             
                                             
                                             
                                        
                                        
                                        
                                        
                                        
                                   
                                   
                                   
                                   
                                   
                              
                              
                              
                              
                              
                         
                         
                         
                         
                         
                    
                    
                    
                    
                    
               
               
               
               
               
          
          
          
          
          
     
     
     
     
     on_exit_orden(orden_values)
     
     return None
     
     
     
     
     
     
     

def condexp ( ):
     condexp_values = []
     
     
     
     on_enter_condexp(condexp_values)
     
     boolval = "no"
     
     
     
     if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "IGUAL" and lexx.lookahead(3)[2].type == "ULTIMO" : 
          python_runtime._append2(lexx.nextToken("ID"),condexp_values)
          
          lexx.nextToken("IGUAL")
          
          python_runtime._append2(lexx.nextToken("ULTIMO"),condexp_values)
          
          boolval = "si" if condexp_values[0].value == last else "no"
          
          
          
          
          
          
          
     else:
          
          if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "IGUAL" and lexx.lookahead(3)[2].type == "STRING" : 
               python_runtime._append2(lexx.nextToken("ID"),condexp_values)
               
               lexx.nextToken("IGUAL")
               
               python_runtime._append2(lexx.nextToken("STRING"),condexp_values)
               
               boolval = "si" if condexp_values[0].value == _strip(condexp_values[1].value,"\"") else "no"
               
               
               
               
               
               
               
          else:
               
               if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "IGUAL" and lexx.lookahead(3)[2].type == "ID" : 
                    python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                    
                    lexx.nextToken("IGUAL")
                    
                    python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                    
                    boolval = "si" if condexp_values[0].value == condexp_values[1].value else "no"
                    
                    
                    
                    
                    
                    
                    
               else:
                    
                    if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "DISTINTO" and lexx.lookahead(3)[2].type == "ULTIMO" : 
                         python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                         
                         lexx.nextToken("DISTINTO")
                         
                         python_runtime._append2(lexx.nextToken("ULTIMO"),condexp_values)
                         
                         boolval = "si" if condexp_values[0].value != last else "no"
                         
                         
                         
                         
                         
                         
                         
                    else:
                         
                         if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "DISTINTO" and lexx.lookahead(3)[2].type == "STRING" : 
                              python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                              
                              lexx.nextToken("DISTINTO")
                              
                              python_runtime._append2(lexx.nextToken("STRING"),condexp_values)
                              
                              boolval = "si" if condexp_values[0].value != _strip(condexp_values[1].value,"\"") else "no"
                              
                              
                              
                              
                              
                              
                              
                         else:
                              
                              if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "DISTINTO" and lexx.lookahead(3)[2].type == "ID" : 
                                   python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                                   
                                   lexx.nextToken("DISTINTO")
                                   
                                   python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                                   
                                   boolval = "si" if condexp_values[0].value != condexp_values[1].value else "no"
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                              else:
                                   
                                   if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "MAYOR" and lexx.lookahead(3)[2].type == "ULTIMO" : 
                                        python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                                        
                                        python_runtime._append2(lexx.nextToken("MAYOR"),condexp_values)
                                        
                                        python_runtime._append2(lexx.nextToken("ULTIMO"),condexp_values)
                                        
                                        boolval = "si" if condexp_values[0].value > last else "no"
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                   else:
                                        
                                        if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "MAYOR" and lexx.lookahead(3)[2].type == "STRING" : 
                                             python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                                             
                                             python_runtime._append2(lexx.nextToken("MAYOR"),condexp_values)
                                             
                                             python_runtime._append2(lexx.nextToken("STRING"),condexp_values)
                                             
                                             boolval = "si" if condexp_values[0].value > _strip(condexp_values[1].value,"\"") else "no"
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                        else:
                                             
                                             if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "MAYOR" and lexx.lookahead(3)[2].type == "ID" : 
                                                  python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                                                  
                                                  python_runtime._append2(lexx.nextToken("MAYOR"),condexp_values)
                                                  
                                                  python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                                                  
                                                  boolval = "si" if condexp_values[0].value > condexp_values[1].value else "no"
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                             else:
                                                  
                                                  if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "MENOR" and lexx.lookahead(3)[2].type == "ULTIMO" : 
                                                       python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                                                       
                                                       python_runtime._append2(lexx.nextToken("MENOR"),condexp_values)
                                                       
                                                       python_runtime._append2(lexx.nextToken("ULTIMO"),condexp_values)
                                                       
                                                       boolval = "si" if condexp_values[0].value < last else "no"
                                                       
                                                       
                                                       
                                                       
                                                       
                                                       
                                                       
                                                  else:
                                                       
                                                       if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "MENOR" and lexx.lookahead(3)[2].type == "STRING" : 
                                                            python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                                                            
                                                            python_runtime._append2(lexx.nextToken("MENOR"),condexp_values)
                                                            
                                                            python_runtime._append2(lexx.nextToken("STRING"),condexp_values)
                                                            
                                                            boolval = "si" if condexp_values[0].value < _strip(condexp_values[1].value,"\"") else "no"
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                       else:
                                                            
                                                            if lexx.lookahead(3)[0].type == "ID" and lexx.lookahead(3)[1].type == "MENOR" and lexx.lookahead(3)[2].type == "ID" : 
                                                                 python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                                                                 
                                                                 python_runtime._append2(lexx.nextToken("MENOR"),condexp_values)
                                                                 
                                                                 python_runtime._append2(lexx.nextToken("ID"),condexp_values)
                                                                 
                                                                 boolval = "si" if condexp_values[0].value < condexp_values[1].value else "no"
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                            else:
                                                                 raise Exception("Error parsing options: No viable alternative for discriminate this options.")
                                                                 
                                                                 
                                                                 
                                                            
                                                            
                                                            
                                                            
                                                            
                                                       
                                                       
                                                       
                                                       
                                                       
                                                  
                                                  
                                                  
                                                  
                                                  
                                             
                                             
                                             
                                             
                                             
                                        
                                        
                                        
                                        
                                        
                                   
                                   
                                   
                                   
                                   
                              
                              
                              
                              
                              
                         
                         
                         
                         
                         
                    
                    
                    
                    
                    
               
               
               
               
               
          
          
          
          
          
     
     
     
     
     on_exit_condexp(condexp_values)
     
     return boolval
     
     
     
     
     
     
     

def expr ( ):
     expr_values = []
     
     
     
     on_enter_expr(expr_values)
     
     expr_val = ""
     
     
     python_runtime._append2(term(),expr_values)
     
     python_runtime._append2(termtail(),expr_values)
     
     expr_val = python_runtime.doAddition(expr_values[0].value,(expr_values[1].value if _size(expr_values) > 1 else ""
     ))
     
     
     on_exit_expr(expr_values)
     
     return expr_val
     
     
     
     
     
     
     
     
     

def termtail ( ):
     termtail_values = []
     
     
     
     on_enter_termtail(termtail_values)
     
     
     if lexx.lookahead(1)[0].type == "PLUS" : 
          python_runtime._append2(lexx.nextToken("PLUS"),termtail_values)
          
          python_runtime._append2(term(),termtail_values)
          
          
          while lexx.lookahead(1) and lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "PLUS" : 
               python_runtime._append2(lexx.nextToken("PLUS"),termtail_values)
               
               python_runtime._append2(term(),termtail_values)
               
               
               
          
          
          
          
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "MINUS" : 
               python_runtime._append2(lexx.nextToken("MINUS"),termtail_values)
               
               python_runtime._append2(term(),termtail_values)
               
               
               while lexx.lookahead(1) and lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "MINUS" : 
                    python_runtime._append2(lexx.nextToken("MINUS"),termtail_values)
                    
                    python_runtime._append2(term(),termtail_values)
                    
                    
                    
               
               
               
               
               
               
          else:
               __dummy_value_for_empty_option__ = 0
               
               
               
          
          
          
          
          
     
     
     
     
     on_exit_termtail(termtail_values)
     
     return termtail_values
     
     
     
     
     
     

def term ( ):
     term_values = []
     
     
     
     on_enter_term(term_values)
     
     term_val = ""
     
     
     python_runtime._append2(exp(),term_values)
     
     python_runtime._append2(exptail(),term_values)
     
     term_val = python_runtime.doAddition(term_values[0].value,(term_values[1].value if _size(term_values) > 1 else ""
     ))
     
     
     on_exit_term(term_values)
     
     return term_val
     
     
     
     
     
     
     
     
     

def exptail ( ):
     exptail_values = []
     
     
     
     on_enter_exptail(exptail_values)
     
     
     if lexx.lookahead(1)[0].type == "EXP" : 
          python_runtime._append2(lexx.nextToken("EXP"),exptail_values)
          
          python_runtime._append2(factor(),exptail_values)
          
          
          while lexx.lookahead(1) and lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "EXP" : 
               python_runtime._append2(lexx.nextToken("EXP"),exptail_values)
               
               python_runtime._append2(factor(),exptail_values)
               
               
               
          
          
          
          
          
          
     else:
          __dummy_value_for_empty_option__ = 0
          
          
          
     
     
     
     
     on_exit_exptail(exptail_values)
     
     return exptail_values
     
     
     
     
     
     

def exp ( ):
     exp_values = []
     
     
     
     on_enter_exp(exp_values)
     
     exp_val = ""
     
     
     python_runtime._append2(factor(),exp_values)
     
     python_runtime._append2(factortail(),exp_values)
     
     exp_val = python_runtime.doAddition(exp_values[0].value,(exp_values[1].value if _size(exp_values) > 1 else ""
     ))
     
     
     on_exit_exp(exp_values)
     
     return exp_val
     
     
     
     
     
     
     
     
     

def factortail ( ):
     factortail_values = []
     
     
     
     on_enter_factortail(factortail_values)
     
     
     if lexx.lookahead(1)[0].type == "TIMES" : 
          python_runtime._append2(lexx.nextToken("TIMES"),factortail_values)
          
          python_runtime._append2(factor(),factortail_values)
          
          
          while lexx.lookahead(1) and lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "TIMES" : 
               python_runtime._append2(lexx.nextToken("TIMES"),factortail_values)
               
               python_runtime._append2(factor(),factortail_values)
               
               
               
          
          
          
          
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "DIV" : 
               python_runtime._append2(lexx.nextToken("DIV"),factortail_values)
               
               python_runtime._append2(factor(),factortail_values)
               
               
               while lexx.lookahead(1) and lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "DIV" : 
                    python_runtime._append2(lexx.nextToken("DIV"),factortail_values)
                    
                    python_runtime._append2(factor(),factortail_values)
                    
                    
                    
               
               
               
               
               
               
          else:
               __dummy_value_for_empty_option__ = 0
               
               
               
          
          
          
          
          
     
     
     
     
     on_exit_factortail(factortail_values)
     
     return factortail_values
     
     
     
     
     
     

def factor ( ):
     factor_values = []
     
     
     
     on_enter_factor(factor_values)
     
     facval = ""
     
     
     
     if lexx.lookahead(1)[0].type == "MINUS" : 
          python_runtime._append2(lexx.nextToken("MINUS"),factor_values)
          
          python_runtime._append2(expr(),factor_values)
          
          
          
     else:
          raise Exception("Error parsing options: No viable alternative for discriminate this options.")
          
          
          
     
     
     
     
     facval = python_runtime.doAddition("-",factor_values[0].value)
     
     
     
     if lexx.lookahead(1)[0].type == "NUMBER" : 
          python_runtime._append2(lexx.nextToken("NUMBER"),factor_values)
          
          facval = factor_values[0].value
          
          
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "ID" : 
               python_runtime._append2(lexx.nextToken("ID"),factor_values)
               
               
               while lexx.lookahead(1)[0].type != "EOF" and lexx.lookahead(1)[0].type == "DOT" : 
                    lexx.nextToken("DOT")
                    
                    python_runtime._append2(lexx.nextToken("ID"),factor_values)
                    
                    
                    
               
               
               
               
               
          else:
               raise Exception("Error parsing options: No viable alternative for discriminate this options.")
               
               
               
          
          
          
          
          
     
     
     
     
     facval = factor_values[0].value
     
     
     
     if _size(factor_values) > 1 : 
          i = 1
          while i < _size(factor_values) :
               facval = python_runtime.doAddition(facval,factor_values[0].value)
               
               
               
               i+=1
          
          
          
     
     
     
     
     
     if lexx.lookahead(1)[0].type == "STRING" : 
          python_runtime._append2(lexx.nextToken("STRING"),factor_values)
          
          facval = factor_values[0].value
          
          
          
          
     else:
          
          if lexx.lookahead(1)[0].type == "LPAREN" : 
               python_runtime._append2(lexx.nextToken("LPAREN"),factor_values)
               
               python_runtime._append2(expr(),factor_values)
               
               python_runtime._append2(lexx.nextToken("RPAREN"),factor_values)
               
               
               
               
          else:
               raise Exception("Error parsing options: No viable alternative for discriminate this options.")
               
               
               
          
          
          
          
          
     
     
     
     
     facval = python_runtime.doAddition(python_runtime.doAddition("(",factor_values[0].value),")")
     
     
     on_exit_factor(factor_values)
     
     return facval
     
     
     
     
     
     
     
     
     
     
     
     
     


userinput = None



session = []




while True : 
     userinput = _input("\nBOT>")
     
     
     
     if userinput == "salir." : 
          break
          
          
     
     
     
     
     lexx.setInput(userinput)
     
     python_runtime._append2(userinput,session)
     
     bot()
     
     
     
     
     
     



_print("Put your code here")





















