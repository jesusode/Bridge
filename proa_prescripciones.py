from __future__ import division
import sys
sys.path.append('.')#Para py2exe
sys.path.append('./modules')#Para py2exe
sys.path.append('library.zip')#Para py2exe
import wx
import wx.grid
import wx.html
from wx_support import *





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

import odswriter


import os



def listToOds ( fname, headers, _list, sheet=""):
     ods = None
     sht = None
     active = None
     
     
     
     ods = odswriter.writer(_open(fname,"wb"))
     
     
     active = ods
     
     
     
     if sheet != "" : 
             sht = ods.new_sheet(sheet)
             
             
             active = sht
             
             
             
             
     
     
     
     
     
     if headers != [] : 
          active.writerow(headers)
          
          
     
     
     
     
     for item in _list: 
          active.writerow(item)
          
          
     
     
     ods.close()
     
     
     
     
     
     
     

def createOds ( name):
     return odswriter.writer(_open(name,"wb"))
     
     

def createSheet ( ods, sname):
     return ods.new_sheet(sname)
     
     

def odsWrite ( ods_or_sheet, row, multiple=False):
     
     if multiple == True : 
          ods_or_sheet.writerows(row)
          
          
     else:
          ods_or_sheet.writerow(row)
          
          
     
     
     
     
     return 1
     
     
     

def odsWriteFormula ( ods, formula):
     ods.writerow([odswriter.Formula(formula)])
     
     return 1
     
     
     


a = None
b = None
t = None
x = None
h = None
atbs = None
cont = None
row = None
colnames = None
url = None
colnames2 = None



atblist = None
servlist = None
paclist = None
pactable = None
ingresados = None
title = None



atblist = []


servlist = []


paclist = []


pactable = {}


title = "PROA HUNSC: Prescripciones de antibioticos"


import wx_support


import codecs


import time


import datetime


colnames = ["nhc","nompac","cama","farmaco","fcrea","dosis","via","frecu","diagnostico","servicio","fingreso"]


colnames2 = ["nhc","servicio","diagnostico","fecha ingreso"]



def process_pacs ( ):
     global colnames,atblist,servlist,paclist,pactable
     
     urlpacs = "http://apache.intranet.net:8080/clinica_dae/adm/adm08-11_xml.php?usr=jodefeb&perfil=20&comboserv=0"
     
     
     b = _geturl(urlpacs)
     
     
     xml0=None
     if type(b) in [type(""),type(u"")]: b=minidom.parseString(b)
     xml0=xpath.find("//row/cell[1]",b)
     
     x = xml0
     
     
     nhcs = list(itertools.imap(lambda y: _xmlstr(y).lstrip("<cell><![CDATA[").rstrip("]]></cell>"),list(itertools.chain(x))))
     
     
     xml1=None
     if type(b) in [type(""),type(u"")]: b=minidom.parseString(b)
     xml1=xpath.find("//row/cell[5]",b)
     
     x = xml1
     
     
     fings = list(itertools.imap(lambda y: _xmlstr(y).lstrip("<cell><![CDATA[").rstrip("]]></cell>"),list(itertools.chain(x))))
     
     
     xml2=None
     if type(b) in [type(""),type(u"")]: b=minidom.parseString(b)
     xml2=xpath.find("//row/cell[6]",b)
     
     x = xml2
     
     
     servs = list(itertools.imap(lambda y: _xmlstr(y).lstrip("<cell><![CDATA[").rstrip("]]></cell>"),list(itertools.chain(x))))
     
     
     xml3=None
     if type(b) in [type(""),type(u"")]: b=minidom.parseString(b)
     xml3=xpath.find("//row/cell[10]",b)
     
     x = xml3
     
     
     dxs = list(itertools.imap(lambda y: _xmlstr(y).lstrip("<cell><![").rstrip("]]></cell>"),list(itertools.chain(x))))
     
     
     dxs = list(itertools.imap(lambda z: _slice(z,6) if z else "",list(itertools.chain(dxs))))
     
     
     cont = 0
     
     
     
     while cont < _size(nhcs) : 
          pactable[nhcs[cont]] = [dxs[cont],fings[cont],servs[cont]]
          
          
          cont+=1
          
          
          
     
     
     
     url = "http://apache.intranet.net:8080/clinica_DAE/hos/hos12-11_xml.php?comboantib=TODOS"
     
     
     b = _geturl(url)
     
     
     xml4=None
     if type(b) in [type(""),type(u"")]: b=minidom.parseString(b)
     xml4=xpath.find("//column/@id",b)
     
     x = xml4
     
     
     _print("empezando proceso del xml(paso limitante)")
     
     xml5=None
     if type(b) in [type(""),type(u"")]: b=minidom.parseString(b)
     xml5=xpath.find("//(row/cell[1]|  row/cell[2] | row/cell[4] | row/cell[5] | row/cell[6] |  row/cell[7] |  row/cell[8] |  row/cell[9] | row/cell[10])/child::node()",b)
     
     x = xml5
     
     
     _print("Terminado proceso del xml")
     
     a = list(itertools.imap(lambda y: _xmlstr(y),list(itertools.chain(x))))
     
     
     atbs = []
     
     
     cont = 0
     
     
     
     while cont < _size(a) : 
          row = [a[cont],a[python_runtime.doAddition(cont,1)],a[python_runtime.doAddition(cont,2)],a[python_runtime.doAddition(cont,3)],a[python_runtime.doAddition(cont,4)],a[python_runtime.doAddition(cont,5)],a[python_runtime.doAddition(cont,6)],a[python_runtime.doAddition(cont,7)],pactable[a[cont]][0],pactable[a[cont]][2],pactable[a[cont]][1]]
          
          
          python_runtime._append2(row,atbs)
          
          
          if a[cont] not in paclist : 
               python_runtime._append2(a[cont],paclist)
               
               
          
          
          
          
          
          if a[python_runtime.doAddition(cont,2)] not in servlist : 
               python_runtime._append2(a[python_runtime.doAddition(cont,2)],servlist)
               
               
          
          
          
          
          
          if a[python_runtime.doAddition(cont,4)] not in atblist : 
               python_runtime._append2(a[python_runtime.doAddition(cont,4)],atblist)
               
               
          
          
          
          
          cont = python_runtime.doAddition(cont,8)
          
          
          
          
          
          
          
          
     
     
     
     return atbs
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     

def procesar_click ( evt):
     global colnames,ingresados,title
     
     model = None
     
     
     
     _print("antes de procesar el xml")
     
     datos = process_pacs()
     
     
     _print("despues de procesar el xml")
     
     model = wx_support.MinimalGridTableModel(len(datos),len(datos[0]),datos,colnames,list(itertools.imap(lambda x: str(x),list(itertools.chain(range(len(datos)))))))
     
     
     tabla.SetTable(model,True)
     
     tabla.AutoSizeColumns()
     
     tabla.Refresh()
     
     main.SetTitle(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(title,": "),_size(datos))," prescripciones "),"en "),ingresados)," pacientes. Tasa: "),str(_size(datos)/_tofloat(ingresados))))
     
     
     
     
     
     
     
     
     
     
     

def excel_click ( evt):
     global ingresados,colnames2,pactable
     
     cells = None
     filename = None
     dlg = None
     csv = None
     
     
     
     censo = None
     
     
     
     cells = tabla.GetTable().GetData()
     
     
     cells = python_runtime.doAddition([colnames],cells)
     
     
     filename = ""
     
     
     def_file = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("prescripciones_hunsc_",_tostring(datetime.date.today().day)),"_"),_tostring(datetime.date.today().month)),"_"),_tostring(datetime.date.today().year)),".ods")
     
     
     dlg = wx.FileDialog(main,message="Guardar como ODS",defaultDir="",defaultFile=def_file,wildcard="*.*",style=wx.SAVE)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          csv = [[unicode(y) for y in list(itertools.chain(x))] for x in list(itertools.chain(cells))]
          
          
          censo = [[x,pactable[x][2],pactable[x][0],pactable[x][1]] for x in list(itertools.chain(pactable.keys()))]
          
          
          censo = python_runtime.doAddition([colnames2],censo)
          
          
          f = createOds(dlg.GetPath())
          
          
          sheet = createSheet(f,"PROA HUNSC")
          
          
          sheet3 = createSheet(f,"Ingresados")
          
          
          sheet2 = createSheet(f,"Estadisticas")
          
          
          odsWrite(sheet,csv,True)
          
          odsWrite(sheet3,censo,True)
          
          odsWrite(sheet2,["Fecha",python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(_tostring(datetime.date.today().day),"/"),_tostring(datetime.date.today().month)),"/"),_tostring(datetime.date.today().year))])
          
          odsWrite(sheet2,["Pacientes ingresados",_tostring(ingresados)])
          
          odsWrite(sheet2,["Antibioticos prescritos",_tostring(_size(cells)-1)])
          
          odsWrite(sheet2,["Tasa de prescripcion",_tostring((_size(cells)-1)/_tofloat(ingresados))])
          
          f.close()
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
     
     
     
     
     
     
     
     
     
     
     
     
     

def imprimir_click ( evt):
     cells = None
     printer = None
     
     
     
     cells = tabla.GetTable().GetData()
     
     
     printer = wx.lib.printout.PrintTable(main)
     
     
     printer.SetLandscape()
     
     printer.SetHeader("Prescripciones HUNSC")
     
     printer.SetFooter()
     
     printer.SetFooter("Fecha: ",type="Date",align=wx.ALIGN_RIGHT,indent=-1,colour=wx.NamedColour("BLACK"))
     
     printer.data = cells
     
     
     printer.label = colnames
     
     
     printer.Preview()
     
     
     
     
     
     
     
     
     
     
     

def salir_click ( evt):
     main.Destroy()
     
     






















root=wx.App()

main=wx.Frame(parent=None,size=[800,790],style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
mainpanel=wx.Panel(main)
mainsizer=wx.BoxSizer(orient=wx.VERTICAL)
tabla_label=wx.StaticText(mainpanel,label="Resultados")
mainsizer.Add(tabla_label,flag=wx.ALL|wx.EXPAND,border=10)
tabla=gridFactory(mainpanel,data=[["nhc","nompac","cama","farmaco","fcrea","dosis","via","frecu","diagnostico","servicio","fingreso"]],colnames=colnames)
mainsizer.Add(tabla,flag=wx.ALL|wx.EXPAND,border=10)
btnpanel=wx.Panel(mainpanel)
mainsizer.Add(btnpanel,flag=wx.ALL|wx.EXPAND,border=10)
btnsizer=wx.GridSizer(rows=1,cols=4,hgap=10,vgap=3)
procesar=wx.Button(btnpanel,id=-1,label="Procesar")
btnsizer.Add(procesar,flag=wx.ALL|wx.EXPAND)
procesar.Bind(wx.EVT_BUTTON,procesar_click)
excel=wx.Button(btnpanel,id=-1,label="Exportar")
btnsizer.Add(excel,flag=wx.EXPAND)
excel.Bind(wx.EVT_BUTTON,excel_click)
imprimir=wx.Button(btnpanel,id=-1,label="Imprimir")
btnsizer.Add(imprimir,flag=wx.EXPAND)
imprimir.Bind(wx.EVT_BUTTON,imprimir_click)
salir=wx.Button(btnpanel,id=-1,label="Salir")
btnsizer.Add(salir,flag=wx.EXPAND)
salir.Bind(wx.EVT_BUTTON,salir_click)



mainpanel.SetSizer(mainsizer)

btnpanel.SetSizer(btnsizer)

tabla.SetMinSize([400,650])

tabla.EnableEditing(False)

main.SetTitle(title)

main.SetIcon(wx.Icon("injection.ico"))

main.Show()

xml6=""
if "http://apache.intranet.net:8080/clinica_dae/adm/resumen_camas.php?perfil=20&usr=jodefeb".strip().find("http://")==0:
    xml6=BeautifulSoup.BeautifulSoup(urllib.urlopen("http://apache.intranet.net:8080/clinica_dae/adm/resumen_camas.php?perfil=20&usr=jodefeb").read())
elif os.path.exists("http://apache.intranet.net:8080/clinica_dae/adm/resumen_camas.php?perfil=20&usr=jodefeb"):
    xml6=BeautifulSoup.BeautifulSoup(open("http://apache.intranet.net:8080/clinica_dae/adm/resumen_camas.php?perfil=20&usr=jodefeb").read())
else:
    xml6=BeautifulSoup.BeautifulSoup("http://apache.intranet.net:8080/clinica_dae/adm/resumen_camas.php?perfil=20&usr=jodefeb")

h = xml6


xml7=""
parts="table"
if len(parts.split(','))!=0:
   parts=parts.split(',')
__elems=h.findAll(parts)
xml7=BeautifulSoup.BeautifulSoup(''.join([str(el) for el in __elems]))

h = xml7


h = str(h)


xml8=None
if type(h) in [type(""),type(u"")]: h=minidom.parseString(h)
xml8=xpath.find("//table/tr[4]/td/text()",h)

h = xml8


h = list(itertools.imap(lambda z: _xmlstr(z),list(itertools.chain(h))))


ingresados = h[0]


















root.MainLoop()
