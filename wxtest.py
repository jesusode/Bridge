from __future__ import division
import sys
sys.path.append('.')#Para py2exe
sys.path.append('./modules')#Para py2exe
sys.path.append('library.zip')#Para py2exe
import wx
import wx.grid
import wx.html
from wx_support import *






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
from python_runtime import _profilepy,_pause,_close,_setWinConsoleCodePage,_getStdin,_getStdout,_getStderr,_floor,_ceil
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


import wx_support


import codecs


import time


import datetime


import DataAnal


colnames = ["nhc","nompac","cama","farmaco","fcrea","dosis","via","frecu","diagnostico","servicio","fingreso"]


colnames2 = ["nhc","servicio","diagnostico","fecha ingreso"]


title_init = "Unidad de Infecciones HUNSC"



connstr = "DRIVER={sql server};server=openlabdb.intranet.net;Database=OpenData;UID=openlab;PWD=Pat1t0degoma"



posmicro_colnames = ["fcrea","ana","idee","nhisto","servicio","nombre","apell1","apell2","muestra","organismo","ufcs","observ"]



posmicro_string = """
    select opendata.dbo.resorganismos.fcrea,openconf.dbo.ana.abr as ana,
    opendata.dbo.pet.idee,
    opendata.dbo.pac.nhisto,
    openconf.dbo.ser.nombre as servicio,
    opendata.dbo.pac.nombre,
    opendata.dbo.pac.apell1,
    opendata.dbo.pac.apell2,
    openconf.dbo.muestras.abr as muestra,
    openconf.dbo.microorganismos.nombre as organismo,
    opendata.dbo.resorganismos.ufcs,
    opendata.dbo.resorganismos.obs
     from opendata.dbo.resorganismos,opendata.dbo.pac,
    openconf.dbo.ana,openconf.dbo.microorganismos,
    opendata.dbo.pet,openconf.dbo.muestras,
    openconf.dbo.ser
    where opendata.dbo.resorganismos.fcrea  between '{0}' and '{1}'  
    and opendata.dbo.resorganismos.pac=opendata.dbo.pac.nid
    and opendata.dbo.resorganismos.pet=opendata.dbo.pet.nid
    and opendata.dbo.resorganismos.muestra=openconf.dbo.muestras.nid
    and opendata.dbo.resorganismos.estudio=openconf.dbo.ana.nid
    and opendata.dbo.resorganismos.organismo=openconf.dbo.microorganismos.nid
    and opendata.dbo.pet.serv1=openconf.dbo.ser.nid
    order by opendata.dbo.resorganismos.fcrea;
"""



atb_string = """
select 
openconf.dbo.antibioticos.nombre,
sensibilidad, 
cmi from ResAntibioticos,
openconf.dbo.antibioticos
 where resorganismo={0}
and openconf.dbo.antibioticos.nid=resantibioticos.antibiotico;"""



anas_from_interest = ["CREA","HB","HEM","LEU","PLQ"]



anas_from_pac = """
select top 20 fechapet as fecha,pet.id as peticion,openconf.dbo.ana.abr as determinacion,vnum as resultado 
 from resul,pet,openconf.dbo.ana
 where pet.pac=(select nid from pac where pac.nhisto='{0}')
and resul.ana=openconf.dbo.ana.nid
and resul.pet=pet.nid
and openconf.dbo.ana.abr in ('CREA','PCR','PROCALC','HB','LEU','PLQ') 
order by fechapet desc,abr asc"""



anas_from_pac2 = """
select top 30
 fechapet as fecha,
pet.id as peticion,
ana as determinacion,
vnum as resultado 
from resul,pet,pac
 where
 pet.pac=(select nid from pac where pac.nhisto='{0}')
and resul.pac=pac.nid
and resul.pet=pet.nid
and ana in (1666,427,2954,911,909,918) 
order by fechapet desc,ana desc"""



aislam_str = """
select Pet.fecha,
Pet.id,
Pet.estado,
openconf.dbo.muestras.nombre as muestra,
openconf.dbo.microorganismos.nombre as aislamiento,
resorganismos.ufcs,
resorganismos.obs as observaciones,
Resorganismos.nid from ResOrganismos, openconf.dbo.microorganismos,
openconf.dbo.muestras,
Pet where
 ResOrganismos.pac=(select nid from Pac where Pac.nhisto='{0}')
 and Pet.nid=ResOrganismos.pet
 and ResOrganismos.organismo=openconf.dbo.microorganismos.nid
 and ResOrganismos.muestra=openconf.dbo.muestras.nid
order by ResOrganismos.fcrea desc;"""



pac_pendientes3 = """
SELECT pet.fecha,
pet.id,
pet.estado,
pet.diag as observaciones,
pet.dataanal as danal
 from Pet,pac
 where pet.TIPO=25  
 and pet.pac=(select nid from pac where nhisto='{0}') and pet.pac=pac.nid 
 order by pet.fecha desc;
"""



pac_pendientes = """
SELECT pet.fecha,
pet.id,
pet.estado,
resul.vdic as resultado,
pet.diag as observaciones,
pet.dataanal as danal
 from Pet,pac,resul
 where pet.TIPO=25  
and pet.pac=(select nid from pac where nhisto='{0}') 
and pet.pac=pac.nid 
and resul.pet=pet.nid
order by pet.fecha desc;
"""



pac_pendientes2 = """
SELECT pet.fecha,pet.id,resorganismos.muestra as muestra,pet.estado,pet.diag as observaciones 
from Pet,pac,resorganismos
 where pet.TIPO=25  
 and pet.pac=(select nid from pac where nhisto='{0}') 
and pet.pac=pac.nid 
and pet.nid=resorganismos.pet
order by pet.fecha desc;
"""



resmicro = """
select resul.pet,resul.vmemo from resul where resul.pet in
 (select nid from pet 
 where pet.tipo=25 
 and pet.pac=(select nid from pac where nhisto='1219886'))
;
"""



aislam_str2 = """
select openconf.dbo.microorganismos.nombre as aislamiento,
openconf.dbo.muestras.nombre as muestra,
resorganismos.ufcs,
resorganismos.obs,
Pet.fecha,
Pet.id,
Pac.nombre,
Pac.apell1,
Pac.apell2,
Pet.estado,
Resorganismos.nid from ResOrganismos, openconf.dbo.microorganismos,
openconf.dbo.muestras,
Pet,Pac where
 ResOrganismos.pac=(select nid from Pac where Pac.nhisto='{0}')
 and Pet.nid=ResOrganismos.pet
 and Pac.nid=ResOrganismos.pac 
 and ResOrganismos.organismo=openconf.dbo.microorganismos.nid
 and ResOrganismos.muestra=openconf.dbo.muestras.nid
order by ResOrganismos.fcrea desc;"""



class modo (Enum):
    histomicro=0
    posmicro=1
    proa=2

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
     global colnames,ingresados,title_init,actual_colnames
     
     model = None
     
     
     
     datos = process_pacs()
     
     
     model = wx_support.MinimalGridTableModel(len(datos),len(datos[0]),datos,colnames,list(itertools.imap(lambda x: str(x),list(itertools.chain(range(len(datos)))))))
     
     
     tabla.SetTable(model,True)
     
     tabla.AutoSizeColumns()
     
     tabla.Refresh()
     
     frm1.SetTitle(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(title_init," Listado PROA: "),_size(datos))," prescripciones "),"en "),ingresados)," pacientes. Tasa: "),str(_size(datos)/_tofloat(ingresados))))
     
     export_calc.Enable(True)
     
     export_print.Enable(True)
     
     actual_colnames = colnames
     
     
     
     
     
     
     
     
     
     
     
     
     

def excel_click ( evt):
     global ingresados,colnames2,pactable,actual_mode,actual_colnames
     
     cells = None
     filename = None
     dlg = None
     csv = None
     
     
     
     censo = None
     
     
     
     cells = tabla.GetTable().GetData()
     
     
     cells = python_runtime.doAddition([actual_colnames],cells)
     
     
     filename = ""
     
     
     
     if actual_mode == "proa" : 
          def_file = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("prescripciones_hunsc_",_tostring(datetime.date.today().day)),"_"),_tostring(datetime.date.today().month)),"_"),_tostring(datetime.date.today().year)),".ods")
          
          
          dlg = wx.FileDialog(frm1,message="Guardar como ODS",defaultDir="",defaultFile=def_file,wildcard="*.*",style=wx.SAVE)
          
          
          
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
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
          
          
          
          
          
          
          
     else:
          def_file = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("positivos_microbiologia_",_tostring(datetime.date.today().day)),"_"),_tostring(datetime.date.today().month)),"_"),_tostring(datetime.date.today().year)),".ods")
          
          
          dlg = wx.FileDialog(frm1,message="Guardar como ODS",defaultDir="",defaultFile=def_file,wildcard="*.*",style=wx.SAVE)
          
          
          
          if dlg.ShowModal() == wx.ID_OK : 
               csv = [[_toUnicode(y,"latin-1") for y in list(itertools.chain(x))] for x in list(itertools.chain(cells))]
               
               
               f = createOds(dlg.GetPath())
               
               
               sheet = createSheet(f,"Positivos Microbiologia")
               
               
               odsWrite(sheet,csv,True)
               
               f.close()
               
               
               
               
               
               
          
          
          
          
          
          
          
     
     
     
     
     
     
     
     
     
     
     

def posmicro_setup ( event):
     global title_init,actual_mode,statusbar,tabla,navigator,splitv
     
     fini_label.Enable(True)
     
     fini.Enable(True)
     
     fend_label.Enable(True)
     
     fend.Enable(True)
     
     posmicro.Enable(True)
     
     nhc_label.Enable(False)
     
     nhc.Enable(False)
     
     historico.Enable(False)
     
     proa_label.Enable(False)
     
     proa.Enable(False)
     
     frm1.SetTitle(python_runtime.doAddition(title_init," - Modo Positivos Microbiologia"))
     
     actual_mode = "posmicro"
     
     
     statusbar.SetStatusText("Modo actual: Positivos Microbiologia")
     
     export_calc.Enable(False)
     
     export_print.Enable(False)
     
     changeGrid(tabla,[[""]],[""],[""])
     
     tabla.Enable(True)
     
     navigator.Enable(False)
     
     splitv.SplitVertically(tabla,navigator,-650)
     
     splitv.Unsplit(navigator)
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     

def histomicro_setup ( event):
     global title_init,actual_mode,statusbar,tabla,navigator
     
     nhc_label.Enable(True)
     
     nhc.Enable(True)
     
     historico.Enable(True)
     
     proa_label.Enable(False)
     
     proa.Enable(False)
     
     fini_label.Enable(False)
     
     fini.Enable(False)
     
     fend_label.Enable(False)
     
     fend.Enable(False)
     
     posmicro.Enable(False)
     
     frm1.SetTitle(python_runtime.doAddition(title_init," - Modo Historico Paciente"))
     
     actual_mode = "histomicro"
     
     
     statusbar.SetStatusText("Modo actual: Historico Paciente")
     
     export_calc.Enable(False)
     
     export_print.Enable(False)
     
     changeGrid(tabla,[[""]],[""],[""])
     
     navigator.Enable(True)
     
     tabla.Enable(False)
     
     splitv.SplitVertically(tabla,navigator,-650)
     
     splitv.Unsplit(tabla)
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     

def proa_setup ( event):
     global title_init,actual_mode,statusbar,tabla,navigator
     
     proa_label.Enable(True)
     
     proa.Enable(True)
     
     fini_label.Enable(False)
     
     fini.Enable(False)
     
     fend_label.Enable(False)
     
     fend.Enable(False)
     
     posmicro.Enable(False)
     
     historico.Enable(False)
     
     nhc_label.Enable(False)
     
     nhc.Enable(False)
     
     frm1.SetTitle(python_runtime.doAddition(title_init," - Modo Listado PROA"))
     
     actual_mode = "proa"
     
     
     statusbar.SetStatusText("Modo actual: PROA")
     
     export_calc.Enable(False)
     
     export_print.Enable(False)
     
     changeGrid(tabla,[[""]],[""],[""])
     
     tabla.Enable(True)
     
     navigator.Enable(False)
     
     splitv.SplitVertically(tabla,navigator,-650)
     
     splitv.Unsplit(navigator)
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     

def imprimir ( evt):
     global actual_colnames,cells,actual_mode
     
     cells = tabla.GetTable().GetData()
     
     
     printer = wx.lib.printout.PrintTable(frm1)
     
     
     printer.SetLandscape()
     
     h = ""
     
     
     
     if actual_mode == "posmicro" : 
          h = "Positivos Microbiologia"
          
          
          
     else:
          
          if actual_mode == "proa" : 
               h = "Listado PROA"
               
               
               
          else:
               h = "Historico de Paciente"
               
               
               
          
          
          
          
          
     
     
     
     
     printer.SetHeader(h)
     
     printer.SetFooter()
     
     printer.SetFooter("Fecha: ",type="Date",align=wx.ALIGN_RIGHT,indent=-1,colour=wx.NamedColour("BLACK"))
     
     printer.data = cells
     
     
     printer.label = actual_colnames
     
     
     printer.Preview()
     
     
     
     
     
     
     
     
     
     
     
     
     

def adaptDate ( date):
     y = _tostring(date.GetYear())
     
     
     m = _tostring(python_runtime.doAddition(date.GetMonth(),1))
     
     
     
     if len(m) == 1 : 
          m = python_runtime.doAddition("0",m)
          
          
          
     
     
     
     
     d = _tostring(date.GetDay())
     
     
     
     if len(d) == 1 : 
          d = python_runtime.doAddition("0",d)
          
          
          
     
     
     
     
     return python_runtime.doAddition(python_runtime.doAddition(y,m),d)
     
     
     
     
     
     
     

def adaptSQLDate ( date):
     parts = _split(_tostring(date),"/")
     
     
     return python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(parts[1],"/"),parts[0]),"/"),parts[2])
     
     
     

def positivos_micro ( event):
     global actual_colnames,posmicro_string,connstr,actual_colnames
     
     date1 = fini.GetValue()
     
     
     date2 = fend.GetValue()
     
     
     q = python_runtime.doFormat(posmicro_string,[adaptDate(date1),adaptDate(date2)])
     
     
     dbase0=[]
     dbase0= python_runtime._queryADO(connstr,q)
     
     rst = dbase0
     
     
     actual_colnames = rst["names"]
     
     
     filas = list(itertools.imap(lambda x: [adaptSQLDate(x[0]),x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11]],list(itertools.chain(rst["data"]))))
     
     
     changeGrid(tabla,filas,actual_colnames,list(itertools.imap(lambda x: _tostring(x),list(itertools.chain(python_runtime.genRange(0,_size(rst["data"])))))))
     
     export_calc.Enable(True)
     
     export_print.Enable(True)
     
     
     
     
     
     
     
     
     
     
     

def historico_micro_backup ( event):
     global tabla,aislam_str,nhc,connstr,actual_colnames,anas_from_pac
     
     navigator.SetPage("<html><head><title></title></head><body><h3>Sin datos de paciente</h3></body></html>","")
     
     nhisto = nhc.GetValue()
     
     
     q = python_runtime.doFormat(aislam_str,[nhisto])
     
     
     dbase1=[]
     dbase1= python_runtime._queryADO(connstr,q)
     
     rst = dbase1
     
     
     
     if rst["data"] == [] : 
          dlg = wx.MessageDialog(frm1,python_runtime.doAddition(python_runtime.doAddition("El paciente ",nhisto)," no tiene aislamientos microbiologicos."),"Historico Paciente ",wx.YES_NO|wx.ICON_QUESTION)
          
          
          dlg.ShowModal()
          
          dlg.Destroy()
          
          changeGrid(tabla,[[""]],[""],[""])
          
          
          
          
          
     else:
          actual_colnames = rst["names"]
          
          
          rows = rst["data"]
          
          
          changeGrid(tabla,rows,actual_colnames,list(itertools.imap(lambda x: _tostring(x),list(itertools.chain(python_runtime.genRange(0,_size(rst["data"])))))))
          
          htreport = build_report(rows,actual_colnames,nhisto)
          
          
          splitv.SplitVertically(tabla,navigator,-650)
          
          splitv.Unsplit(tabla)
          
          navigator.Enable(True)
          
          navigator.SetPage(htreport,"")
          
          navigator.Reload()
          
          
          
          
          
          
          
          
          
          
     
     
     
     
     
     
     
     
     
     

def historico_micro ( event):
     global tabla,aislam_str,nhc,connstr,actual_colnames,anas_from_pac
     
     navigator.SetPage("<html><head><title></title></head><body><h3>Sin datos de paciente</h3></body></html>","")
     
     nhisto = nhc.GetValue()
     
     
     q = python_runtime.doFormat(aislam_str,[nhisto])
     
     
     dbase2=[]
     dbase2= python_runtime._queryADO(connstr,q)
     
     rst = dbase2
     
     
     actual_colnames = rst["names"]
     
     
     rows = rst["data"]
     
     
     changeGrid(tabla,rows,actual_colnames,list(itertools.imap(lambda x: _tostring(x),list(itertools.chain(python_runtime.genRange(0,_size(rst["data"])))))))
     
     htreport = build_report(rows,actual_colnames,nhisto)
     
     
     splitv.SplitVertically(tabla,navigator,-650)
     
     splitv.Unsplit(tabla)
     
     navigator.Enable(True)
     
     navigator.SetPage(htreport,"")
     
     navigator.Reload()
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     

def build_report ( rows, headers, nhc):
     global tabla,aislam_str,connstr,actual_colnames,anas_from_pac,atb_string,pac_pendientes,pac_pendientes2,anas,anas_from_pac2,anas_conf,muestras_conf
     
     htmlstr = "<html><head><meta charset=\"latin-1\">"
     
     
     htmlstr = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(htmlstr,"<script>"),_readf("./hunsc_data/jquery-latest.js")),"</script>")
     
     
     htmlstr = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(htmlstr,"<script>var nhcs=["),nhc),"];</script>")
     
     
     htmlstr = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(htmlstr,_readf("./hunsc_data/htmlview.txt")),"<title>Informe para paciente "),nhc),"</title>")
     
     
     htmlstr = python_runtime.doAddition(htmlstr,"</head><body>")
     
     
     htmlstr = python_runtime.doAddition(htmlstr,"<h1 class='main_title'>Unidad de Control de la Infeccion HUNSC </h1><br/><br/>")
     
     
     htmlstr = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(htmlstr,"<hr/><h2>Informe de paciente NHC "),nhc),"</h2><hr/><br/><br/>")
     
     
     htmlstr = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(htmlstr,"<h3 class =\"clickable\" id=\"hmedicacion_"),nhc),"\" >Medicacion actual</h3>")
     
     
     url = python_runtime.doFormat("http://apache.intranet.net:8080/clinica_DAE/farmacia/ordenmedica/ordenmedica.php?nhc={0}",[nhc])
     
     
     xml6=""
     if _toUnicode(_geturl(url),"latin-1").strip().find("http://")==0:
         xml6=BeautifulSoup.BeautifulSoup(urllib.urlopen(_toUnicode(_geturl(url),"latin-1")).read())
     elif os.path.exists(_toUnicode(_geturl(url),"latin-1")):
         xml6=BeautifulSoup.BeautifulSoup(open(_toUnicode(_geturl(url),"latin-1")).read())
     else:
         xml6=BeautifulSoup.BeautifulSoup(_toUnicode(_geturl(url),"latin-1"))
     
     htm = xml6
     
     
     xml7=""
     parts="table"
     if len(parts.split(','))!=0:
        parts=parts.split(',')
     __elems=htm.findAll(parts)
     xml7=BeautifulSoup.BeautifulSoup(''.join([str(el) for el in __elems]))
     
     htm2 = xml7
     
     
     htm2 = _tostring(reduce(lambda x,y: python_runtime.doAddition(python_runtime.doAddition(_toUnicode(x,"latin-1"),"<br/><br/>\n"),_toUnicode(y,"latin-1")),itertools.chain(htm2)))
     
     
     htm2 = _replace(htm2,"\\","|")
     
     
     anas = python_runtime.doAddition(python_runtime.doAddition("<h3 class =\"clickable\" id=\"hanas_",nhc),"\" >Ultimas analiticas</h3>")
     
     
     anas_q = python_runtime.doFormat(anas_from_pac2,[nhc])
     
     
     dbase3=[]
     dbase3= python_runtime._queryADO(connstr,anas_q)
     
     rst = dbase3
     
     
     vals = rst["data"]
     
     
     vals = list(itertools.imap(lambda x: [adaptSQLDate(x[0]),x[1],anas_conf[x[2]],x[3]],list(itertools.chain(vals))))
     
     
     anas = python_runtime.doAddition(anas,build_html_table(rst["names"],vals,style="font-size: 10pt",id=python_runtime.doAddition("anas_",nhc),klass="discard"))
     
     
     pends_h = python_runtime.doAddition(python_runtime.doAddition("<h3 class =\"clickable\" id=\"hpeticiones_",nhc),"\" >Peticiones Microbiologia</h3>")
     
     
     htmlstr = python_runtime.doAddition(htmlstr,"{0}</body></html>")
     
     
     pends_str = "<h4>El paciente no tiene muestras de microbiologia pendientes.</h4>"
     
     
     pends_q = python_runtime.doFormat(pac_pendientes,[nhc])
     
     
     dbase4=[]
     dbase4= python_runtime._queryADO(connstr,pends_q)
     
     rst = dbase4
     
     
     pendientes_micro = []
     
     
     
     if rst["data"] != [] : 
          for item in rst["data"]: 
               danal = DataAnal.DataAnal()
               
               
               info = ""
               
               
               info = danal.getMicroInfo(item[5])
               
               
               
               if info != [] : 
                    info = info[0]
                    
                    
                    python_runtime._append2([_sublist(adaptSQLDate(item[0]),0,8),item[1],anas_conf[info[0]],"Pendiente" if item[2] < 8 else "Terminado"
                    ,resmicro_conf.get(item[3],"Sin datos"),item[4] if item[4] != None else ""
                    ],pendientes_micro)
                    
                    
                    
               
               
               
               
               
               
               
               
          
          
          
     
     
     
     
     flds = ["fecha","id","muestra","estado","resultado","observaciones"]
     
     
     pends_str = build_html_table(flds,pendientes_micro,id=python_runtime.doAddition("peticiones_",nhc),style="font-size: 10pt")
     
     
     toolstr = python_runtime.doAddition(python_runtime.doAddition("<div id=\"toolbar_",nhc),"\"></div><br/>")
     
     
     atb_nids = list(itertools.imap(lambda x: x[-1],list(itertools.chain(rows))))
     
     
     atbs = {}
     
     
     for item in atb_nids: 
          atbs_q = python_runtime.doFormat(atb_string,[item])
          
          
          dbase5=[]
          dbase5= python_runtime._queryADO(connstr,atbs_q)
          
          rst = dbase5
          
          
          
          if rst["data"] != [] : 
               atbs[item] = build_html_table(rst["names"],rst["data"],"antibiograma",style="font-size: 10pt")
               
               
               
          else:
               atbs[item] = ""
               
               
               
          
          
          
          
          
          
          
     
     
     ais_h = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("<h3 class =\"clickable\"  id=\"haislamientos_",nhc),"\" >Aislamientos  ("),_size(atb_nids)),")</h3><br/>")
     
     
     rxstr = ""
     
     
     bodystr = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(htm2,"<br/><br/>"),anas),"<br/><br/>"),pends_h),pends_str),"<br/><br/>"),ais_h),"<br/><br/>"),toolstr),"<br/><br/>"),build_aislam_table((list(itertools.chain(headers))[ None: -1]
     ),(list(itertools.imap(lambda x: list(itertools.chain(x))[ None: -1],list(itertools.chain(rows))))),atb_nids,atbs,nhc)),rxstr)
     
     
     s = python_runtime.doFormat(htmlstr,[bodystr])
     
     
     return s
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     

def build_aislam_table ( headers, rows, atbs_nids, atbs_dic, nhc):
     
     if rows == [] : 
          return ""
          
          
     
     
     
     
     hds = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("<table id=\"aislamientos_",nhc),"\" style='font-size: 10pt'><thead><tr><th><b>\n"),(reduce(lambda y,z: python_runtime.doAddition(python_runtime.doAddition(y,"</b></th><th><b>\n"),z),itertools.chain(headers)))),"</b></th></tr></thead><tbody><tr><td>")
     
     
     rows = list(itertools.imap(lambda x: [_sublist(adaptSQLDate(x[0]),0,8),x[1],"Pendiente" if x[2] < 8 else "Terminado"
     ,x[3],x[4],x[5] if x[5] != None else ""
     ,x[6]],list(itertools.chain(rows))))
     
     
     i = 0
     while i < _size(atbs_nids) :
          rows[i][4] = python_runtime.doAddition(rows[i][4],atbs_dic[atbs_nids[i]])
          
          
          
          i+=1
     
     
     bodystr = list(itertools.imap(lambda x: reduce(lambda y,z: python_runtime.doAddition(python_runtime.doAddition(_toUnicode(y,"utf-8"),"</td><td>\n"),_toUnicode(z,"utf-8")),itertools.chain(x)),list(itertools.chain(rows))))
     
     
     bodystr = python_runtime.doAddition((reduce(lambda x,y: python_runtime.doAddition(python_runtime.doAddition(x,"</tr><tr><td>\n"),y),itertools.chain(bodystr))),"\n</td></tr></tbody></table>")
     
     
     return python_runtime.doAddition(hds,bodystr)
     
     
     
     
     
     
     
     

def build_html_table ( headers, rows, id="", klass="", style=""):
     hds = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("<table ","id='"),id),"' class='"),klass),"'")," style='"),style),"'><thead><tr><th><b>\n"),(reduce(lambda y,z: python_runtime.doAddition(python_runtime.doAddition(y,"</b></th><th><b>\n"),z),itertools.chain(headers)))),"</b></th></tr></thead><tbody>")
     
     
     bodystr = ""
     
     
     
     if rows != [] : 
          bodystr = list(itertools.imap(lambda x: python_runtime.doAddition(python_runtime.doAddition("<td>",(reduce(lambda y,z: python_runtime.doAddition(python_runtime.doAddition(_tostring(y),"</td><td>"),_tostring(z)),itertools.chain(x)))),"</td>"),list(itertools.chain(rows))))
          
          
          bodystr = python_runtime.doAddition(python_runtime.doAddition("<tr>",(reduce(lambda y,z: python_runtime.doAddition(python_runtime.doAddition(_toUnicode(y,"utf-8"),"</tr><tr>"),_toUnicode(z,"utf-8")),itertools.chain(bodystr)))),"</tr>")
          
          
          bodystr = python_runtime.doAddition(bodystr,"</tbody></table>")
          
          
          
          
          
     
     
     
     
     return python_runtime.doAddition(hds,bodystr)
     
     
     
     
     

def salir ( evt):
     frm1.Destroy()
     
     




































root=wx.App()

frm1=wx.Frame(parent=None)
mbar=wx.MenuBar()
frm1.SetMenuBar(mbar)
file=wx.Menu()
mbar.Append(file,title="Modo de uso")
export=wx.Menu()
mbar.Append(export,title="Utilidades")
file_posmicro=wx.MenuItem(file,wx.NewId(),text="Positivos &Microbiologia\tCtrl+M",kind=wx.ITEM_NORMAL)
file.AppendItem(file_posmicro)
frm1.Bind(wx.EVT_MENU,posmicro_setup,file_posmicro)
file.AppendSeparator()
file_histomicro=wx.MenuItem(file,wx.NewId(),text="&Historico Paciente\tCtrl+H",kind=wx.ITEM_NORMAL)
file.AppendItem(file_histomicro)
frm1.Bind(wx.EVT_MENU,histomicro_setup,file_histomicro)
file.AppendSeparator()
file_proa=wx.MenuItem(file,wx.NewId(),text="&PROA\tCtrl+P",kind=wx.ITEM_NORMAL)
file.AppendItem(file_proa)
frm1.Bind(wx.EVT_MENU,proa_setup,file_proa)
file.AppendSeparator()
file_salir=wx.MenuItem(file,wx.NewId(),text="&Salir\tCtrl+S",kind=wx.ITEM_NORMAL)
file.AppendItem(file_salir)
frm1.Bind(wx.EVT_MENU,salir,file_salir)
export_calc=wx.MenuItem(export,wx.NewId(),text="Exportar a &OpenOffice Calc\tCtrl+X",kind=wx.ITEM_NORMAL)
export.AppendItem(export_calc)
frm1.Bind(wx.EVT_MENU,excel_click,export_calc)
file.AppendSeparator()
export_print=wx.MenuItem(export,wx.NewId(),text="Imprimir tabla\tCtrl+I",kind=wx.ITEM_NORMAL)
export.AppendItem(export_print)
frm1.Bind(wx.EVT_MENU,imprimir,export_print)
splith=wx.SplitterWindow(frm1,style=wx.SP_3DBORDER|wx.SP_BORDER)
formpanel=wx.Panel(splith,style=wx.SUNKEN_BORDER)
mainsizer=wx.BoxSizer(orient=wx.VERTICAL)
mainsizer.Add((10,10))
butspanel=wx.Panel(formpanel)
mainsizer.Add(butspanel,flag=wx.EXPAND,border=5)
mainsizer.Add((10,10))
butsizer=wx.GridSizer(rows=1,cols=3,hgap=10,vgap=10)
nhc_label=wx.StaticText(butspanel,id=-1,label="NHC paciente:")
butsizer.Add(nhc_label,border=5)
nhc=wx.TextCtrl(butspanel,style=wx.TE_PROCESS_ENTER)
butsizer.Add(nhc,flag=wx.EXPAND,border=5)
nhc.Bind(wx.EVT_TEXT_ENTER,historico_micro)
historico=wx.Button(butspanel,id=-1,label="Historico")
butsizer.Add(historico,flag=wx.EXPAND,border=5)
historico.Bind(wx.EVT_BUTTON,historico_micro)
pospanel=wx.Panel(formpanel)
mainsizer.Add(pospanel,flag=wx.EXPAND)
possizer=wx.GridSizer(rows=1,cols=5,hgap=10,vgap=10)
fini_label=wx.StaticText(pospanel,label="Desde:")
possizer.Add(fini_label,flag=wx.EXPAND,border=10)
fini=wx.DatePickerCtrl(pospanel,style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
possizer.Add(fini,flag=wx.EXPAND,border=10)
fend_label=wx.StaticText(pospanel,label="Hasta:")
possizer.Add(fend_label,flag=wx.EXPAND,border=10)
fend=wx.DatePickerCtrl(pospanel,style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
possizer.Add(fend,flag=wx.EXPAND,border=10)
posmicro=wx.Button(pospanel,id=-1,label="Pos. Micro")
possizer.Add(posmicro,flag=wx.EXPAND,border=5)
posmicro.Bind(wx.EVT_BUTTON,positivos_micro)
mainsizer.Add((10,10))
proapanel=wx.Panel(formpanel)
mainsizer.Add(proapanel,flag=wx.EXPAND)
proasizer=wx.GridSizer(rows=1,cols=2,hgap=10,vgap=10)
proa_label=wx.StaticText(proapanel,label="Obtener listado PROA")
proasizer.Add(proa_label,flag=wx.EXPAND,border=10)
proa=wx.Button(proapanel,id=-1,label="PROA")
proasizer.Add(proa,flag=wx.EXPAND,border=5)
proa.Bind(wx.EVT_BUTTON,procesar_click)
splitv=wx.SplitterWindow(splith,style=wx.SP_3DBORDER|wx.SP_BORDER|wx.SP_PERMIT_UNSPLIT)
tabla=gridFactory(splitv,data=[[""]],colnames=[""],rownames=[""])
navigator=wx.html2.WebView.New(splitv)



#Bridge generated code
formpanel.SetSizer(mainsizer)
butspanel.SetSizer(butsizer)

pospanel.SetSizer(possizer)

proapanel.SetSizer(proasizer)

splith.SplitHorizontally(formpanel,splitv,-50)

splitv.SplitVertically(tabla,navigator,-650)

splitv.Unsplit(navigator)

nhc_label.Enable(False)

nhc.Enable(False)

historico.Enable(False)

proa_label.Enable(False)

proa.Enable(False)

fini_label.Enable(False)

fini.Enable(False)

fend_label.Enable(False)

fend.Enable(False)

posmicro.Enable(False)

navigator.Enable(False)

tabla.Enable(False)

tabla.SetMinSize([100,600])

tabla.EnableEditing(False)

navigator.SetPage("<html><head><title></title></head><body><h3>Sin datos de paciente</h3></body></html>","")

frm1.SetTitle("Unidad de Infecciones HUNSC")

frm1.SetIcon(wx.Icon("pills.ico"))

statusbar = frm1.CreateStatusBar()



statusbar.SetStatusText("Elija un modo de uso")

export_calc.Enable(False)

export_print.Enable(False)

frm1.Show()

frm1.SetSize(wx.Size(1200,800))

frm1.CenterOnScreen()

xml8=""
if "http://apache.intranet.net:8080/clinica_dae/adm/resumen_camas.php?perfil=20&usr=jodefeb".strip().find("http://")==0:
    xml8=BeautifulSoup.BeautifulSoup(urllib.urlopen("http://apache.intranet.net:8080/clinica_dae/adm/resumen_camas.php?perfil=20&usr=jodefeb").read())
elif os.path.exists("http://apache.intranet.net:8080/clinica_dae/adm/resumen_camas.php?perfil=20&usr=jodefeb"):
    xml8=BeautifulSoup.BeautifulSoup(open("http://apache.intranet.net:8080/clinica_dae/adm/resumen_camas.php?perfil=20&usr=jodefeb").read())
else:
    xml8=BeautifulSoup.BeautifulSoup("http://apache.intranet.net:8080/clinica_dae/adm/resumen_camas.php?perfil=20&usr=jodefeb")

h = xml8


xml9=""
parts="table"
if len(parts.split(','))!=0:
   parts=parts.split(',')
__elems=h.findAll(parts)
xml9=BeautifulSoup.BeautifulSoup(''.join([str(el) for el in __elems]))

h = xml9


h = str(h)


xml10=None
if type(h) in [type(""),type(u"")]: h=minidom.parseString(h)
xml10=xpath.find("//table/tr[4]/td/text()",h)

h = xml10


h = list(itertools.imap(lambda z: _xmlstr(z),list(itertools.chain(h))))


ingresados = h[0]


actual_mode = ""



actual_colnames = []



confstr = "DRIVER={sql server};server=openlabdb.intranet.net;Database=OpenConf;UID=openlab;PWD=Pat1t0degoma"



conf_q = "select nid,nombre from ana"



conf_m = "select nid,texto from diclin where tabla=142;"



abr_anas = []
muestras = []
resmicro = []



anas_conf = {}
muestras_conf = {}
resmicro_conf = {}




if not os.path.exists("anas_conf.ser") : 
     dbase6=[]
     dbase6= python_runtime._queryADO(confstr,conf_q)
     
     abr_anas = dbase6
     
     
     for item in abr_anas["data"]: 
          anas_conf[item[0]] = _strip(item[1])
          
          
          
     
     
     python_runtime.doSerialize(anas_conf,"anas_conf.ser")
     
     
     _print("Cargando anas desde base de datos!")
     
     
     
     
else:
     anas_conf = python_runtime.doDeserialize("anas_conf.ser")
     
     
     
     _print("Deserializando anas desde archivo!")
     
     
     





if not os.path.exists("muestras_conf.ser") : 
     conf_q = "select nid,nombre from muestras"
     
     
     dbase7=[]
     dbase7= python_runtime._queryADO(confstr,conf_q)
     
     muestras = dbase7
     
     
     for item in muestras["data"]: 
          muestras_conf[item[0]] = _strip(item[1])
          
          
          
     
     
     python_runtime.doSerialize(muestras_conf,"muestras_conf.ser")
     
     
     _print("Cargando muestras desde base de datos!")
     
     
     
     
     
else:
     muestras_conf = python_runtime.doDeserialize("muestras_conf.ser")
     
     
     
     _print("Deserializando muestras desde archivo!")
     
     
     





if not os.path.exists("diclin_conf.ser") : 
     conf_m = "select nid,texto from diclin"
     
     
     dbase8=[]
     dbase8= python_runtime._queryADO(confstr,conf_m)
     
     resmicro = dbase8
     
     
     for item in resmicro["data"]: 
          resmicro_conf[item[0]] = _strip(item[1]) if item[1] != None else ""
          
          
          
          
     
     
     python_runtime.doSerialize(resmicro_conf,"diclin_conf.ser")
     
     
     _print("Cargando diccionarios desde base de datos!")
     
     
     
     
     
else:
     resmicro_conf = python_runtime.doDeserialize("diclin_conf.ser")
     
     
     
     _print("Deserializando diccionarios desde archivo!")
     
     
     





















































root.MainLoop()
