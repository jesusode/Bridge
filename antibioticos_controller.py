
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
from python_runtime import _toMatrix,_invert,_toDict,_copy,_appendRow,_getList,_insertRow,_appendCol,_insertCol,_getCol,_getRow,_getDimensions,_size,_toint,_tofloat,_abs,_strip,_count,_indexof,_histogram
from python_runtime import _chain,_zip,_cartessian, _combinations,_combinations_with_r, _permutations,_enumerate, _starmap, _list,_cycle,_split,_join,_readf,_readflines,_system,_lisp,_scheme,_lispModule,_clojure
from python_runtime import _xmltod,_dtoxml,_transaction,_rollback,_isclass,_cmdline,_toUnicode,_slice,_checkType,_xmlstr,_applyXSLT,_geturl
#-----------------------------------------------------------------------------------------------------


__typedefs={'numeric':[],'chain':[]}
__type_instances={}
__basecons={}
__pyBases=[]

a = None
b = None
c = None
xsl = None
t = None
x = None
atbs = None
cont = None
row = None
colnames = None
htm = None
sel = None
url = None



import prettytable


htmltemplate = None



htmltemplate = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>{0}</title>
</head>
<body>
<pre>
{1}
</pre>
</body>
</html>"""



def toTable ( seq, titles):
     t = prettytable.PrettyTable(titles)
     
     
     for item in seq: 
          
          if type(item) == type([]) : 
                  t.add_row(item)
                  
                  
          else:
                  t.add_row([item])
                  
                  
          
          
          
          
          
     
     
     return t
     
     
     

def toHTML ( seq, titles, label):
     t = toTable(seq,titles)
     
     
     t = python_runtime.doFormat(htmltemplate,[label,t])
     
     
     return t
     
     
     
     


url = "http://apache.intranet.net:8080/clinica_DAE/hos/hos12-11_xml.php?comboantib=TODOS"


b = _geturl(url)


open("atbhunsc.xml","w").close()


text0=""
if os.path.exists("atbhunsc.xml") and os.path.isfile("atbhunsc.xml"):
    text0=open("atbhunsc.xml","w")
    text0.write(b)
    text0.close()
else:
     raise Exception('Error: "%s" debe ser un archivo valido'%"atbhunsc.xml")

xml0=None
if type(b) in [type(""),type(u"")]: b=minidom.parseString(b)
xml0=xpath.find("//column/@id",b)

x = xml0


colnames = list(itertools.imap(lambda z: _xmlstr(z),list(itertools.chain(x))))


xml1=None
if type(b) in [type(""),type(u"")]: b=minidom.parseString(b)
xml1=xpath.find("//(row/cell[1]|  row/cell[2] | row/cell[3] | row/cell[4] | row/cell[5] |  row/cell[6] |  row/cell[7] |  row/cell[8] | row/cell[9])/child::node()",b)

x = xml1


a = list(itertools.imap(lambda y: _xmlstr(y),list(itertools.chain(x))))


atbs = []


cont = 0



while cont < _size(a) : 
     row = [a[cont],a[python_runtime.doAddition(cont,1)],a[python_runtime.doAddition(cont,2)],a[python_runtime.doAddition(cont,3)],a[python_runtime.doAddition(cont,4)],a[python_runtime.doAddition(cont,5)],a[python_runtime.doAddition(cont,6)],a[python_runtime.doAddition(cont,7)]]
     
     
     python_runtime._append2(row,atbs)
     
     cont = python_runtime.doAddition(cont,8)
     
     
     
     
     



htm = toHTML(atbs,colnames,python_runtime.doAddition(python_runtime.doAddition("Prescripciones HUNSC: ",_size(atbs))," prescripciones"))


open("atbhunsc.html","w").close()


text1=""
if os.path.exists("atbhunsc.html") and os.path.isfile("atbhunsc.html"):
    text1=open("atbhunsc.html","w")
    text1.write(htm)
    text1.close()
else:
     raise Exception('Error: "%s" debe ser un archivo valido'%"atbhunsc.html")

_system("explorer atbhunsc.html")






















