
import sys
sys.path.append('.')#Para py2exe
sys.path.append('./modules')#Para py2exe
sys.path.append('library.zip')#Para py2exe
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
# try: #no hay sqlite3 en jython
    # if not 'sqlite3' in sys.modules:
         # sqlite3=__import__('sqlite3')
    # else:
         # sqlite3=sys.modules['sqlite3']
# except:
     # pass
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
from python_runtime import _chain,_zip,_cartessian, _combinations,_combinations_with_r, _permutations,_enumerate, _starmap, _list,_cycle,_split,_join,_readf,_readflines,_system,_lisp,_scheme,_cmdline,_toUnicode,_slice
from python_runtime import _xmltod,_dtoxml
#-----------------------------------------------------------------------------------------------------


__typedefs={'numeric':[],'chain':[]}
__type_instances={}
__basecons={}
__pyBases=[]

import mini_tkbasic

import tkFont

import Tkinter

import minimalfpdf

import mini_rtf

import mini_pdfbasic

import codecs


def init_code ( ):
        global tcl
        tcl = Tkinter.Tcl()
        
        

def archivo_abrir ( ):
     text0=""
     text0+=python_runtime.getPathText(mini_tkbasic.getTkFile("Abrir archivo","open"))
     
     f = text0
     
     mini_tkbasic.setFormItemValue("applet1","texto",f)
     

def archivo_guardar ( ):
     f = mini_tkbasic.getTkFile("Guardar archivo","save")
     
     
     if f != None : 
          open(f,"w").close()
          
          
          try : 
               t = codecs.encode(mini_tkbasic.getFormItemValue("applet1","texto"),"latin-1","ignore")
               
               text1=""
               if os.path.exists(f) and os.path.isfile(f):
                   text1=open(f,"w")
                   text1.write(t)
                   text1.close()
               else:
                    raise Exception('Error: "%s" debe ser un archivo valido'%f)
               
               
          
          
          
          except : 
               mini_tkbasic.messageBox("Error","Error guardando el archivo.","warning")
               
          
          
          
          
     
     
     
     

def archivo_guardar_como ( ):
     mini_tkbasic.messageBox("Menu Archivo Guardar como...","implementame!!","info")
     

def archivo_exportar_pdf ( ):
     pdf = minimalfpdf.MinimalFPDF()
     
     pdf.add_page()
     pdf.write_html(mini_tkbasic.getFormItemValue("applet1","texto"))
     pdf.output(mini_tkbasic.getTkFile("Guardar archivo","save"),"F")
     

def archivo_exportar_rtf ( ):
     rtf = mini_rtf.rtfCreateDoc("tmp","nuevo")
     
     section = mini_rtf.rtfCreateSection("sec1")
     
     mini_rtf.rtfAddSection("tmp","sec1")
     text = codecs.encode(mini_tkbasic.getFormItemValue("applet1","texto"),"latin-1","ignore")
     
     split0=[]
     if os.path.exists(text) and os.path.isfile(text):
         split0 += re.split(open(text).read(),"\n")
     else:
         split0+=re.split("\n",text)
     
     text = split0
     
     for line in text: 
          mini_rtf.rtfAddText("sec1",line)
          
     
     mini_rtf.rtfSaveDoc("tmp",mini_tkbasic.getTkFile("Guardar archivo","save"))
     

def archivo_guardar_config ( ):
     f = mini_tkbasic.getTkFile("Guardar configuracion actual","save")
     
     
     if f != None : 
          save_config(f)
          
     
     
     
     

def archivo_cargar_config ( ):
     f = mini_tkbasic.getTkFile("Cargar configuracion","open")
     
     
     if f != None : 
          load_config(f)
          
     
     
     
     

def archivo_salir ( ):
     mini_tkbasic._exitForms()
     

def editar_buscar ( ):
     mini_tkbasic.messageBox("Menu Editar","implementame!!","info")
     

def editar_reemplazar ( ):
     mini_tkbasic.messageBox("Menu Editar","implementame!!","info")
     

def editar_copiar ( ):
     
     try : 
          tbox = mini_tkbasic.getFormItem("applet1","texto@text")
          
          tbox.clipboard_clear()
          tbox.clipboard_append(tbox.get("sel.first","sel.last"))
          
     
     
     
     except : 
          mini_tkbasic.messageBox("Error al copiar","Debe existir texto seleccionado para poderlo copiar","error")
          
     
     
     
     

def editar_pegar ( ):
     tbox = mini_tkbasic.getFormItem("applet1","texto@text")
     
     tbox.insert("insert",tbox.clipboard_get())
     

def editar_borrar ( ):
     tbox = mini_tkbasic.getFormItem("applet1","texto@text")
     
     tbox.delete("1.0","end")
     

def editar_fuente ( ):
     formfonts = mini_tkbasic.formBox(appopts2,labs2,labels2,values2,1,0)
     _print(formfonts)
     
     if formfonts != {} : 
          font = tkFont.Font(**formfonts["font"])
          
          mini_tkbasic.callFormItem("applet1","texto@text","configure",{"font":font})
          
     
     
     
     

def editar_color_fuente ( ):
     c = mini_tkbasic.getTkColor("Cambiar color de fuente")
     
     
     if c != None : 
          mini_tkbasic.callFormItem("applet1","texto@text","configure",{"foreground":c})
          tbox = mini_tkbasic.getFormItem("applet1","texto@text")
          
          f = tkFont.Font(font=tbox["font"])
          
          
     
     
     
     

def editar_fondo ( ):
     c = mini_tkbasic.getTkColor("Cambiar color de fondo")
     
     
     if c != None : 
          mini_tkbasic.callFormItem("applet1","texto@text","configure",{"background":c})
          
     
     
     
     

def tools_minimal ( ):
     tbox = mini_tkbasic.getFormItemValue("applet1","texto")
     
     minimal_py.__reflected=1
     exec minimal_py.parser.parse(tbox)
     minimal_py.__reflected=0
     
     

def tools_python ( ):
     tbox = mini_tkbasic.getFormItemValue("applet1","texto")
     
     exec tbox
     
     

def tools_tcl ( ):
     tbox = mini_tkbasic.getFormItemValue("applet1","texto")
     
     tcl.eval(tbox)
     

def tools_scheme ( ):
     tbox = mini_tkbasic.getFormItemValue("applet1","texto")
     
     _scheme(_tostring(tbox))
     

def tools_program ( ):
     mini_tkbasic.messageBox("Menu Herramientas","implementame!!","info")
     _print(mini_tkbasic.getMainFrame())
     mini_tkbasic.addFormItem("applet1",{"nueva":"label"},{"nueva":"soy dinamica!!!"},"pack",0)
     mini_tkbasic.addFormItem("applet1",{"nuevotxt":"text"},{"nuevotxt":"Me han creado..."},"pack",1)
     

def save_config ( fname):
     tbox = mini_tkbasic.getFormItem("applet1","texto@text")
     
     f = tkFont.Font(font=tbox["font"])
     
     d = f.actual()
     
     bg = tbox["background"]
     
     fg = tbox["foreground"]
     
     config = [fg,bg,d]
     
     open(fname,"w").close()
     
     python_runtime.doSerialize(config,fname)
     
     

def load_config ( fname):
     config = python_runtime.doDeserialize(fname)
     
     
     tbox = mini_tkbasic.getFormItem("applet1","texto@text")
     
     f = tkFont.Font(**config[2])
     
     tbox.configure(font=f,background=config[1],foreground=config[0])
     

appopts = None
menulabels = None
submenu = None
menucodes = None
menuarchivo = None
menueditar = None
menutools = None
labs = None
labels = None
values = None
valores = None
formvals = None


appopts2 = None
labs2 = None
labels2 = None
values2 = None
formfonts = None
config = None


tcl = None


appopts = {"name":"applet1","title":"Minimal Text Editor","width":800,"height":600,"x":200,"y":200,"resize":0,"oninit":init_code,"minwidth":100,"minheight":100,"sizer":"pack","style":"xpnative","nolabels":1}

labs = ["texto"]

labels = {"texto":"textbox"}

values = {"texto":"Valor por defecto"}

menulabels = ["Archivo","Editar","Herramientas"]

menuarchivo = [["Abrir","-","Guardar","-","Guardar_como...","-","Exportar_a_pdf","Exportar_a_rtf","-","Guardar_configuracion","Cargar_configuracion","-","Salir"],[archivo_abrir,None,archivo_guardar,None,archivo_guardar_como,None,archivo_exportar_pdf,archivo_exportar_rtf,None,archivo_guardar_config,archivo_cargar_config,None,archivo_salir]]

menueditar = [["Buscar","Reemplazar","-","Copiar","Pegar","-","Cambiar_fuente","Cambiar_color_fuente","Cambiar_fondo","-","Borrar"],[editar_buscar,editar_reemplazar,None,editar_copiar,editar_pegar,None,editar_fuente,editar_color_fuente,editar_fondo,None,editar_borrar]]

menutools = [["Minimal","-","Python","-","Tcl","-","Scheme","-","Programa..."],[tools_minimal,None,tools_python,None,tools_tcl,None,tools_scheme,None,tools_program]]

menucodes = {"Archivo":menuarchivo,"Editar":menueditar,"Herramientas":menutools}

appopts2 = {"name":"fonts","title":"Cambiar fuente","width":600,"height":200,"x":200,"y":200,"resize":0,"minwidth":100,"minheight":100,"sizer":"grid","style":"xpnative","nolabels":1}

labs2 = ["font"]

labels2 = {"font":"font"}

values2 = {}

formvals = mini_tkbasic.formBox(appopts,labs,labels,values,1,0,menulabels,menucodes)
_print(formvals)
_print("Ok!")


