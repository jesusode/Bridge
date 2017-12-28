
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
from python_runtime import _find,_strinsert,_regroups,_writef,_writeflines,_foreach,_setencoding,_divmod,_fact,_sqrt,_index,_exp,_ln,_log,_sin,_asin,_cos,_acos,_tan,_atan
from python_runtime import _profilepy,_pause,_close,_setWinConsoleCodePage,_getStdin,_getStdout,_getStderr
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

import sys


import colorama


python_runtime._check_py_bases([ctypes.Structure])
class COORD(ctypes.Structure):
    def __init__(self,*k,**kw):
        ctypes.Structure.__init__(self,*k,**kw)
    



def wprint ( l, fore="", back="", style=""):
     sys.stdout.write("\r")
     
     attr = ""
     
     
     
     if fore != "" : 
             attr = python_runtime.doAddition(attr,AnsiFore[fore])
             
             
             
     
     
     
     
     
     if back != "" : 
          attr = python_runtime.doAddition(attr,AnsiBack[back])
          
          
          
     
     
     
     
     
     if style != "" : 
          attr = python_runtime.doAddition(attr,AnsiStyle[style])
          
          
          
     
     
     
     
     sys.stdout.write(python_runtime.doAddition(attr,l))
     
     sys.stdout.flush()
     
     
     
     
     
     
     
     

def wnl ( ):
     sys.stdout.write("\r")
     
     sys.stdout.write(" "*80)
     
     sys.stdout.write("\r")
     
     sys.stdout.flush()
     
     
     
     
     

def cursorUp ( n):
     return AnsiCursor["up"](n)
     
     

def cursorDown ( n):
     return AnsiCursor["down"](n)
     
     

def cursorForward ( n):
     return AnsiCursor["forward"](n)
     
     

def cursorBack ( n):
     return AnsiCursor["back"](n)
     
     

def putCursor ( x, y):
     return AnsiCursor["pos"](x,y)
     
     

def clearScreen ( ):
     colorama.ansi.clear_screen()
     
     


AnsiFore = {"black":colorama.Fore.BLACK,"red":colorama.Fore.RED,"green":colorama.Fore.GREEN,"yellow":colorama.Fore.YELLOW,"blue":colorama.Fore.BLUE,"magenta":colorama.Fore.MAGENTA,"cyan":colorama.Fore.CYAN,"white":colorama.Fore.WHITE,"reset":colorama.Fore.RESET,"LIGHTBLACK_EX":colorama.Fore.LIGHTBLACK_EX,"LIGHTRED_EX":colorama.Fore.LIGHTRED_EX,"LIGHTGREEN_EX":colorama.Fore.LIGHTGREEN_EX,"LIGHTYELLOW_EX":colorama.Fore.LIGHTYELLOW_EX,"LIGHTBLUE_EX":colorama.Fore.LIGHTBLUE_EX,"LIGHTMAGENTA_EX":colorama.Fore.LIGHTMAGENTA_EX,"LIGHTCYAN_EX":colorama.Fore.LIGHTCYAN_EX,"LIGHTWHITE_EX":colorama.Fore.LIGHTWHITE_EX}



AnsiBack = {"black":colorama.Back.BLACK,"red":colorama.Back.RED,"green":colorama.Back.GREEN,"yellow":colorama.Back.YELLOW,"blue":colorama.Back.BLUE,"magenta":colorama.Back.MAGENTA,"cyan":colorama.Back.CYAN,"white":colorama.Back.WHITE,"reset":colorama.Back.RESET,"LIGHTBLACK_EX":colorama.Back.LIGHTBLACK_EX,"LIGHTRED_EX":colorama.Back.LIGHTRED_EX,"LIGHTGREEN_EX":colorama.Back.LIGHTGREEN_EX,"LIGHTYELLOW_EX":colorama.Back.LIGHTYELLOW_EX,"LIGHTBLUE_EX":colorama.Back.LIGHTBLUE_EX,"LIGHTMAGENTA_EX":colorama.Back.LIGHTMAGENTA_EX,"LIGHTCYAN_EX":colorama.Back.LIGHTCYAN_EX,"LIGHTWHITE_EX":colorama.Back.LIGHTWHITE_EX}



AnsiStyle = {"bright":colorama.Style.BRIGHT,"dim":colorama.Style.DIM,"normal":colorama.Style.NORMAL,"reset":colorama.Style.RESET_ALL}



AnsiCursor = {"up":colorama.Cursor.UP,"down":colorama.Cursor.DOWN,"forward":colorama.Cursor.FORWARD,"back":colorama.Cursor.BACK,"pos":colorama.Cursor.POS}



box_tl = "\u250C"



box_tr = "\u2510"



box_bl = "\u2514"



box_br = "\u2518"



vborder = "\u2500"



hborder = "\u2502"



MB_OK = 0x0



MB_OKCXL = 0x01



MB_YESNOCXL = 0x03



MB_YESNO = 0x04



MB_HELP = 0x4000



ICON_EXLAIM = 0x30



ICON_INFO = 0x40



ICON_STOP = 0x10



MessageBoxW = ctypes.windll.user32.MessageBoxW



MessageBox = ctypes.windll.user32.MessageBoxA



colorama.init()

wprint("Esto debe ser amarillo","yellow","white","bright")

wprint("\n","reset","reset","reset")

wprint("Ok")

wprint(cursorUp(1))

wprint("Adios")

wprint(python_runtime.doAddition(putCursor(30,10),"Ondia"))

_pause(3)

clearScreen()

MessageBox(None,"Adios","Todo OK!",MB_YESNO|MB_HELP|ICON_STOP)

_print(_getSystem())





































