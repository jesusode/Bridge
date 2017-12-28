
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
from python_runtime import _urlencode,_urldecode,_linqlike,_append2,_reverse
#-----------------------------------------------------------------------------------------------------



class EnumMetaClass(type):
    def __setattr__(self, name, value):
        raise Exception('Error: You cannot set an enum value. Enum values are inmutable')

class Enum:
    __metaclass__= EnumMetaClass

__typedefs={'numeric':[],'chain':[]}
__type_instances={}
__basecons={}
__pyBases=[]


def guardar ( evt):
     temp = None
     f = None
     query = None
     rst = None
     seg = None
     pacnid = None
     
     
     
     global dets,mues,micobacts,LAST_NID
     
     query = ""
     
     
     f = validar_controles()
     
     
     
     if f == 0 : 
             return 
             
             
     
     
     
     
     temp = {}
     
     
     f = fecha.GetValue()
     
     
     temp["fecha"] = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(_tostring(f.GetDay()),"/"),_tostring(python_runtime.doAddition(f.GetMonth(),1))),"/"),_tostring(f.GetYear()))
     
     
     temp["nhc"] = nhc.GetValue().strip()
     
     
     temp["idmues"] = idmues.GetValue().strip()
     
     
     f = fecham.GetValue()
     
     
     temp["fecham"] = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(_tostring(f.GetDay()),"/"),_tostring(python_runtime.doAddition(f.GetMonth(),1))),"/"),_tostring(f.GetYear()))
     
     
     temp["det"] = _tostring(dets[det.GetValue()])
     
     
     temp["muestra"] = _tostring(mues[muestra.GetValue()])
     
     
     temp["resultado"] = resultado.GetValue().strip()
     
     
     temp["aislamiento"] = _tostring(micobacts[aislamiento.GetValue()]) if aislamiento.GetValue() else "NULL"
     
     
     
     temp["atb1l"] = mico1l.GetValue().strip()
     
     
     temp["atb2l"] = mico2l.GetValue().strip()
     
     
     temp["acciones"] = acciones.GetValue().strip()
     
     
     temp["seguir"] = True if seguir.IsChecked() else False
     
     
     
     query = python_runtime.doAddition(python_runtime.doAddition("select nid,seguimiento from pacientes where nhc='",_strip(temp["nhc"])),"';")
     
     
     dbase0=[]
     dbase0_conn=sqlite3.connect("micobacterias",isolation_level=None)
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
     
     rst = dbase0
     
     
     
     if rst["data"] == [] : 
          seg = "1" if _tostring(temp["seguir"]) == True else "0"
          
          
          
          query = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("insert into pacientes(nhc,nombre,apell1,apell2,seguimiento) values('",temp["nhc"]),"','sin datos','sin datos', 'sin datos',"),seg),");")
          
          
          dbase1=[]
          dbase1_conn=sqlite3.connect("micobacterias",isolation_level=None)
          dbase1_cursor=dbase1_conn.cursor()
          dbase1_cursor.execute(query)
          for i in dbase1_cursor:
              if type(i)==type((0,)):
                  dbase1.append(list(i))
              else:
                  dbase1.append(i)
          names = [description[0] for description in dbase1_cursor.description] if dbase1_cursor.description else []
          dbase1_conn.commit()
          dbase1= {"data":dbase1 ,"names": names,"affected":dbase1_cursor.rowcount}
          
          rst = dbase1
          
          
          dbase2=[]
          dbase2_conn=sqlite3.connect("micobacterias",isolation_level=None)
          dbase2_cursor=dbase2_conn.cursor()
          dbase2_cursor.execute(python_runtime.doAddition(python_runtime.doAddition("select nid from pacientes where nhc='",temp["nhc"]),"';"))
          for i in dbase2_cursor:
              if type(i)==type((0,)):
                  dbase2.append(list(i))
              else:
                  dbase2.append(i)
          names = [description[0] for description in dbase2_cursor.description] if dbase2_cursor.description else []
          dbase2_conn.commit()
          dbase2= {"data":dbase2 ,"names": names,"affected":dbase2_cursor.rowcount}
          
          rst = dbase2
          
          
          pacnid = rst["data"][0][0]
          
          
          
          
          
          
          
     else:
          dbase3=[]
          dbase3_conn=sqlite3.connect("micobacterias",isolation_level=None)
          dbase3_cursor=dbase3_conn.cursor()
          dbase3_cursor.execute(python_runtime.doAddition(python_runtime.doAddition("select nid from pacientes where nhc='",temp["nhc"]),"';"))
          for i in dbase3_cursor:
              if type(i)==type((0,)):
                  dbase3.append(list(i))
              else:
                  dbase3.append(i)
          names = [description[0] for description in dbase3_cursor.description] if dbase3_cursor.description else []
          dbase3_conn.commit()
          dbase3= {"data":dbase3 ,"names": names,"affected":dbase3_cursor.rowcount}
          
          rst = dbase3
          
          
          pacnid = rst["data"][0][0]
          
          
          
          
     
     
     
     
     
     if temp["seguir"] == True : 
          query = python_runtime.doAddition(python_runtime.doAddition("update pacientes set seguimiento=1 where nhc='",temp["nhc"]),"';")
          
          
          dbase4=[]
          dbase4_conn=sqlite3.connect("micobacterias",isolation_level=None)
          dbase4_cursor=dbase4_conn.cursor()
          dbase4_cursor.execute(query)
          for i in dbase4_cursor:
              if type(i)==type((0,)):
                  dbase4.append(list(i))
              else:
                  dbase4.append(i)
          names = [description[0] for description in dbase4_cursor.description] if dbase4_cursor.description else []
          dbase4_conn.commit()
          dbase4= {"data":dbase4 ,"names": names,"affected":dbase4_cursor.rowcount}
          
          rst = dbase4
          
          
          
          
     
     
     
     
     
     if LAST_NID > -1 : 
          query = python_runtime.doAddition(python_runtime.doAddition("delete from determinaciones where nid=",LAST_NID),";")
          
          
          dbase5=[]
          dbase5_conn=sqlite3.connect("micobacterias",isolation_level=None)
          dbase5_cursor=dbase5_conn.cursor()
          dbase5_cursor.execute(query)
          for i in dbase5_cursor:
              if type(i)==type((0,)):
                  dbase5.append(list(i))
              else:
                  dbase5.append(i)
          names = [description[0] for description in dbase5_cursor.description] if dbase5_cursor.description else []
          dbase5_conn.commit()
          dbase5= {"data":dbase5 ,"names": names,"affected":dbase5_cursor.rowcount}
          
          rst = dbase5
          
          
          LAST_NID = -1
          
          
          _print(python_runtime.doAddition("borrados: ",_tostring(rst["affected"])))
          
          
          
          
          
     
     
     
     
     query = " insert into determinaciones(pac,id_mues,fecha_det,fecha_mues,determinacion,muestra,resultado,aislamiento,atb1l,atb2l,acciones) values("
     
     
     query = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(query,_tostring(pacnid)),",'"),temp["idmues"]),"','"),temp["fecha"]),"','"),temp["fecham"]),"',")
     
     
     query = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(query,temp["det"]),","),temp["muestra"]),",'"),temp["resultado"]),"',"),temp["aislamiento"]),",'")
     
     
     query = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(query,temp["atb1l"]),"','"),temp["atb2l"]),"','"),temp["acciones"]),"');")
     
     
     dbase6=[]
     dbase6_conn=sqlite3.connect("micobacterias",isolation_level=None)
     dbase6_cursor=dbase6_conn.cursor()
     dbase6_cursor.execute(query)
     for i in dbase6_cursor:
         if type(i)==type((0,)):
             dbase6.append(list(i))
         else:
             dbase6.append(i)
     names = [description[0] for description in dbase6_cursor.description] if dbase6_cursor.description else []
     dbase6_conn.commit()
     dbase6= {"data":dbase6 ,"names": names,"affected":dbase6_cursor.rowcount}
     
     rst = dbase6
     
     
     borrar(None)
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     

def buscar ( evt):
     global LAST_NID
     
     m = txtbus.GetValue()
     
     
     
     if m != "" : 
          query = python_runtime.doAddition(python_runtime.doAddition("select * from determinaciones where nid=",m.strip()),";")
          
          
          dbase7=[]
          dbase7_conn=sqlite3.connect("micobacterias",isolation_level=None)
          dbase7_cursor=dbase7_conn.cursor()
          dbase7_cursor.execute(query)
          for i in dbase7_cursor:
              if type(i)==type((0,)):
                  dbase7.append(list(i))
              else:
                  dbase7.append(i)
          names = [description[0] for description in dbase7_cursor.description] if dbase7_cursor.description else []
          dbase7_conn.commit()
          dbase7= {"data":dbase7 ,"names": names,"affected":dbase7_cursor.rowcount}
          
          rst = dbase7
          
          
          
          if rst["data"] != [] : 
               d = rst["data"][0]
               
               
               LAST_NID = d[0]
               
               
               p = d[1]
               
               
               query2 = python_runtime.doAddition(python_runtime.doAddition("select nhc,seguimiento from pacientes where nid=",_tostring(p)),";")
               
               
               dbase8=[]
               dbase8_conn=sqlite3.connect("micobacterias",isolation_level=None)
               dbase8_cursor=dbase8_conn.cursor()
               dbase8_cursor.execute(query2)
               for i in dbase8_cursor:
                   if type(i)==type((0,)):
                       dbase8.append(list(i))
                   else:
                       dbase8.append(i)
               names = [description[0] for description in dbase8_cursor.description] if dbase8_cursor.description else []
               dbase8_conn.commit()
               dbase8= {"data":dbase8 ,"names": names,"affected":dbase8_cursor.rowcount}
               
               rst2 = dbase8
               
               
               nhc.SetValue(rst2["data"][0][0])
               
               idmues.SetValue(d[2])
               
               l = _split(d[3],"/")
               
               
               l = list(itertools.imap(lambda x: int(x),list(itertools.chain(l))))
               
               
               l[1] = l[1]-1
               
               
               fecha.SetValue(wx.DateTimeFromDMY(*l))
               
               l = _split(d[4],"/")
               
               
               l = list(itertools.imap(lambda x: int(x),list(itertools.chain(l))))
               
               
               l[1] = l[1]-1
               
               
               fecham.SetValue(wx.DateTimeFromDMY(*l))
               
               det.SetSelection(d[5]-1 if d[5] > 0 else d[5]
               )
               
               muestra.SetSelection(d[6]-1 if d[6] > 0 else d[6]
               )
               
               resultado.SetValue(d[7])
               
               aislamiento.SetSelection(d[8]-1 if d[8] > 0 else d[8]
               )
               
               acciones.SetValue(d[11])
               
               mico1l.SetValue(d[9])
               
               mico2l.SetValue(d[10])
               
               seguir.SetValue(False if rst2["data"][0][1] == 0 else True
               )
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
          else:
               messagebox("No hay determinaciones registradas para ese numero de muestra")
               
               
          
          
          
          
          
          
          
     
     
     
     
     
     
     

def borrar ( evt):
     nhc.SetValue("")
     
     idmues.SetValue("")
     
     det.SetValue("")
     
     muestra.SetValue("")
     
     resultado.SetValue("")
     
     acciones.SetValue("")
     
     aislamiento.SetValue("")
     
     mico1l.SetValue("")
     
     mico2l.SetValue("")
     
     fecha.SetValue(wx.DateTime.Today())
     
     fecham.SetValue(wx.DateTime.Today())
     
     seguir.SetValue(False)
     
     
     
     
     
     
     
     
     
     
     
     
     

def borrarq ( evt):
     qpac.SetValue("")
     
     qmues.SetValue("")
     
     qseguir.SetValue(False)
     
     
     
     

def consultar ( evt):
     queryres.SetPage("")
     
     queryst = "select * from resultados "
     
     
     
     if qpac.GetValue() != "" : 
          queryst = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(queryst,"where nhc='"),qpac.GetValue()),"' ")
          
          
          
     
     
     
     
     
     if qmues.GetValue() != "" : 
          
          if qpac.GetValue() != "" : 
               queryst = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(queryst," and id_mues='"),qmues.GetValue()),"' ")
               
               
               
          else:
               queryst = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(queryst," where id_mues='"),qmues.GetValue()),"' ")
               
               
               
          
          
          
          
          
     
     
     
     
     
     if qseguir.IsChecked() : 
          queryst = python_runtime.doAddition(queryst,"where seguim=1 ")
          
          
          
     
     
     
     
     queryst = python_runtime.doAddition(queryst,";")
     
     
     dbase9=[]
     dbase9_conn=sqlite3.connect("micobacterias",isolation_level=None)
     dbase9_cursor=dbase9_conn.cursor()
     dbase9_cursor.execute(queryst)
     for i in dbase9_cursor:
         if type(i)==type((0,)):
             dbase9.append(list(i))
         else:
             dbase9.append(i)
     names = [description[0] for description in dbase9_cursor.description] if dbase9_cursor.description else []
     dbase9_conn.commit()
     dbase9= {"data":dbase9 ,"names": names,"affected":dbase9_cursor.rowcount}
     
     rst = dbase9
     
     
     queryres.SetPage(toTable(rst["data"]))
     
     
     
     
     
     
     
     
     

def guardarq ( evt):
     _print("guardando consulta")
     
     

def salir ( evt):
     frm1.Destroy()
     
     

def validar_controles ( ):
     
     if nhc.GetValue() == "" : 
          messagebox("El campo NHC es obligatorio.")
          
          return 0
          
          
          
     
     
     
     
     
     if idmues.GetValue() == "" : 
          messagebox("El campo Id. muestra es obligatorio.")
          
          return 0
          
          
          
     
     
     
     
     
     if det.GetValue() == "" : 
          messagebox("El campo Determinacion es obligatorio.")
          
          return 0
          
          
          
     
     
     
     
     
     if muestra.GetValue() == "" : 
          messagebox("El campo Muestra es obligatorio.")
          
          return 0
          
          
          
     
     
     
     
     
     if aislamiento.GetValue() == "" : 
          messagebox("El campo Aislamiento es obligatorio.")
          
          return 0
          
          
          
     
     
     
     
     
     if resultado.GetValue() == "" : 
          messagebox("El campo Resultado es obligatorio.")
          
          return 0
          
          
          
     
     
     
     
     return 1
     
     
     
     
     
     
     
     

def messagebox ( text, title="Datos no validos"):
     dlg = wx.MessageDialog(frm1,text,title,wx.OK|wx.ICON_ERROR)
     
     
     dlg.ShowModal()
     
     dlg.Destroy()
     
     
     
     

def toTable ( cells):
     tblstr = """<table border="1" padding="0" border="0">"""
     
     
     tblstr = python_runtime.doAddition(tblstr,"<tr><th>ID</th><th>NHC</th><th>Peticion</th><th>Fecha</th><th>Fecha Peticion</th><th>Determinacion</th><th>")
     
     
     tblstr = python_runtime.doAddition(tblstr,"Muestra</th><th>Resultado</th><th>Aislamiento</th><th>Micobiograma primera linea</th><th>Micobiograma segunda linea</th><th>Acciones</th><th>Seguimiento</th>")
     
     
     for row in cells: 
          tblstr = python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition(tblstr,"<tr><td>"),_join(row,"</td><td>")),"</td></tr>")
          
          
          
     
     
     tblstr = python_runtime.doAddition(tblstr,"</table>")
     
     
     return tblstr
     
     
     
     
     
     






root=wx.App()

frm1=wx.Frame(parent=None)
nb1=wx.Notebook(parent=frm1)
mainsizer=wx.BoxSizer(orient=wx.VERTICAL)
mainpanel=wx.Panel(nb1)
labtitulo=wx.StaticText(mainpanel,label="Determinaciones\n",style=wx.ALIGN_CENTRE_HORIZONTAL)
mainsizer.Add(labtitulo,flag=wx.ALL|wx.EXPAND,border=16)
gridpanel=wx.Panel(mainpanel)
mainsizer.Add(gridpanel,flag=wx.ALL|wx.EXPAND)
s1=wx.GridSizer(rows=13,cols=2,hgap=10,vgap=3)
labbus=wx.StaticText(gridpanel,label="   Buscar por ID (el ID cambia se se edita)")
s1.Add(labbus,flag=wx.ALL|wx.EXPAND,border=5)
txtbus=wx.TextCtrl(gridpanel)
s1.Add(txtbus,flag=wx.ALL|wx.EXPAND,border=5)
labfecha=wx.StaticText(gridpanel,label="   Fecha")
s1.Add(labfecha,flag=wx.ALL|wx.EXPAND,border=5)
fecha=wx.DatePickerCtrl(gridpanel,style=wx.DP_DROPDOWN)
s1.Add(fecha,flag=wx.ALL|wx.EXPAND,border=5)
labnhc=wx.StaticText(gridpanel,label="   NHC")
s1.Add(labnhc,flag=wx.ALL|wx.EXPAND,border=5)
nhc=wx.TextCtrl(gridpanel)
s1.Add(nhc,flag=wx.ALL|wx.EXPAND,border=5)
labidmues=wx.StaticText(gridpanel,label="   Id. muestra")
s1.Add(labidmues,flag=wx.ALL|wx.EXPAND,border=5)
idmues=wx.TextCtrl(gridpanel)
s1.Add(idmues,flag=wx.ALL|wx.EXPAND,border=5)
labfecham=wx.StaticText(gridpanel,label="   Fecha muestra")
s1.Add(labfecham,flag=wx.ALL|wx.EXPAND,border=5)
fecham=wx.DatePickerCtrl(gridpanel,style=wx.DP_DROPDOWN)
s1.Add(fecham,flag=wx.ALL|wx.EXPAND,border=5)
labdet=wx.StaticText(gridpanel,label="   Determinacion")
s1.Add(labdet,flag=wx.ALL|wx.EXPAND,border=5)
det=wx.ComboBox(gridpanel)
s1.Add(det,flag=wx.ALL|wx.EXPAND,border=5)
labmues=wx.StaticText(gridpanel,label="   Muestra")
s1.Add(labmues,flag=wx.ALL|wx.EXPAND,border=5)
muestra=wx.ComboBox(gridpanel)
s1.Add(muestra,flag=wx.ALL|wx.EXPAND,border=5)
labres=wx.StaticText(gridpanel,label="   Resultado")
s1.Add(labres,flag=wx.ALL|wx.EXPAND,border=5)
resultado=wx.TextCtrl(gridpanel,style=wx.TE_MULTILINE)
s1.Add(resultado,flag=wx.ALL|wx.EXPAND,border=5)
labais=wx.StaticText(gridpanel,label="   Aislamiento")
s1.Add(labais,flag=wx.ALL|wx.EXPAND,border=5)
aislamiento=wx.ComboBox(gridpanel)
s1.Add(aislamiento,flag=wx.ALL|wx.EXPAND,border=5)
labacc=wx.StaticText(gridpanel,label="   Acciones")
s1.Add(labacc,flag=wx.ALL|wx.EXPAND,border=5)
acciones=wx.TextCtrl(gridpanel,style=wx.TE_MULTILINE)
s1.Add(acciones,flag=wx.ALL|wx.EXPAND,border=5)
labmico1=wx.StaticText(gridpanel,label="   Micobiograma primera linea")
s1.Add(labmico1,flag=wx.ALL|wx.EXPAND,border=5)
mico1l=wx.TextCtrl(gridpanel,style=wx.TE_MULTILINE)
s1.Add(mico1l,flag=wx.ALL|wx.EXPAND,border=5)
labmico2=wx.StaticText(gridpanel,label="   Micobiograma segunda linea")
s1.Add(labmico2,flag=wx.ALL|wx.EXPAND,border=5)
mico2l=wx.TextCtrl(gridpanel,style=wx.TE_MULTILINE)
s1.Add(mico2l,flag=wx.ALL|wx.EXPAND,border=5)
labseguir=wx.StaticText(gridpanel,label="   Seguir paciente")
s1.Add(labseguir,flag=wx.ALL|wx.EXPAND,border=5)
seguir=wx.CheckBox(gridpanel)
s1.Add(seguir,flag=wx.ALL|wx.EXPAND,border=5)
buttonpanel=wx.Panel(mainpanel)
mainsizer.Add(buttonpanel,flag=wx.ALL|wx.EXPAND)
btnsizer=wx.GridSizer(rows=1,cols=4,hgap=10,vgap=10)
buscar_btn=wx.Button(buttonpanel,label="Buscar")
btnsizer.Add(buscar_btn,flag=wx.ALL|wx.EXPAND,border=5)
guardar_btn=wx.Button(buttonpanel,label="Guardar")
btnsizer.Add(guardar_btn,flag=wx.ALL|wx.EXPAND,border=5)
borrar_btn=wx.Button(buttonpanel,label="Borrar")
btnsizer.Add(borrar_btn,flag=wx.ALL|wx.EXPAND,border=5)
salir_btn=wx.Button(buttonpanel,label="Salir")
btnsizer.Add(salir_btn,flag=wx.ALL|wx.EXPAND,border=5)
guardar_btn.Bind(wx.EVT_BUTTON,guardar)
borrar_btn.Bind(wx.EVT_BUTTON,borrar)
salir_btn.Bind(wx.EVT_BUTTON,salir)
buscar_btn.Bind(wx.EVT_BUTTON,buscar)
querypanel=wx.Panel(nb1)
querysizer=wx.BoxSizer(orient=wx.VERTICAL)
labqtitulo=wx.StaticText(querypanel,label="Consultas\n",style=wx.ALIGN_CENTRE_HORIZONTAL)
querysizer.Add(labqtitulo,flag=wx.ALL|wx.EXPAND,border=16)
gridpanel2=wx.Panel(querypanel)
querysizer.Add(gridpanel2,flag=wx.ALL|wx.EXPAND)
s2=wx.GridSizer(rows=3,cols=2,hgap=10,vgap=3)
labqpac=wx.StaticText(gridpanel2,label="   Paciente")
s2.Add(labqpac,flag=wx.ALL|wx.EXPAND,border=5)
qpac=wx.TextCtrl(gridpanel2)
s2.Add(qpac,flag=wx.ALL|wx.EXPAND,border=5)
labqmues=wx.StaticText(gridpanel2,label="   Muestra")
s2.Add(labqmues,flag=wx.ALL|wx.EXPAND,border=5)
qmues=wx.TextCtrl(gridpanel2)
s2.Add(qmues,flag=wx.ALL|wx.EXPAND,border=5)
labqseguir=wx.StaticText(gridpanel2,label="   En seguimiento")
s2.Add(labqseguir,flag=wx.ALL|wx.EXPAND,border=5)
qseguir=wx.CheckBox(gridpanel2)
s2.Add(qseguir,flag=wx.ALL|wx.EXPAND,border=5)
consultar_btn=wx.Button(querypanel,label="Consultar")
querysizer.Add(consultar_btn,flag=wx.ALL|wx.EXPAND,border=20)
consultar_btn.Bind(wx.EVT_BUTTON,consultar)
queryres=htmlWinFactory(querypanel,html="""<h3>Pulse consultar para ejecutar la consulta</h3>""",size=[400,540])
querysizer.Add(queryres,flag=wx.EXPAND)
buttonpanelq=wx.Panel(querypanel)
querysizer.Add(buttonpanelq,flag=wx.ALL|wx.EXPAND)
btnsizerq=wx.GridSizer(rows=1,cols=3,hgap=10,vgap=10)
borrarq_btn=wx.Button(buttonpanelq,label="Borrar")
btnsizerq.Add(borrarq_btn,flag=wx.ALL|wx.EXPAND,border=5)
guardarq_btn=wx.Button(buttonpanelq,label="Guardar")
btnsizerq.Add(guardarq_btn,flag=wx.ALL|wx.EXPAND,border=5)
salirq_btn=wx.Button(buttonpanelq,label="Salir")
btnsizerq.Add(salirq_btn,flag=wx.ALL|wx.EXPAND,border=5)
borrarq_btn.Bind(wx.EVT_BUTTON,borrarq)
salirq_btn.Bind(wx.EVT_BUTTON,salir)
guardarq_btn.Bind(wx.EVT_BUTTON,guardarq)



font = None
rst = None
dets = None
mues = None
micobacts = None
LAST_NID = None



dets = {}


mues = {}


micobacts = {}


LAST_NID = -1


sqlite3.connect("micobacterias",isolation_level=None).close()


dbase10=[]
dbase10_conn=sqlite3.connect("micobacterias",isolation_level=None)
dbase10_cursor=dbase10_conn.cursor()
dbase10_cursor.execute("select nombre,nid from tipo_det")
for i in dbase10_cursor:
    if type(i)==type((0,)):
        dbase10.append(list(i))
    else:
        dbase10.append(i)
names = [description[0] for description in dbase10_cursor.description] if dbase10_cursor.description else []
dbase10_conn.commit()
dbase10= {"data":dbase10 ,"names": names,"affected":dbase10_cursor.rowcount}

rst = dbase10


for item in rst["data"]: 
     dets[item[0]] = item[1]
     
     
     det.Append(item[0])
     
     
     


dbase11=[]
dbase11_conn=sqlite3.connect("micobacterias",isolation_level=None)
dbase11_cursor=dbase11_conn.cursor()
dbase11_cursor.execute("select nombre,nid from muestras")
for i in dbase11_cursor:
    if type(i)==type((0,)):
        dbase11.append(list(i))
    else:
        dbase11.append(i)
names = [description[0] for description in dbase11_cursor.description] if dbase11_cursor.description else []
dbase11_conn.commit()
dbase11= {"data":dbase11 ,"names": names,"affected":dbase11_cursor.rowcount}

rst = dbase11


for item in rst["data"]: 
     mues[item[0]] = item[1]
     
     
     muestra.Append(item[0])
     
     
     


dbase12=[]
dbase12_conn=sqlite3.connect("micobacterias",isolation_level=None)
dbase12_cursor=dbase12_conn.cursor()
dbase12_cursor.execute("select nombre,nid from micobacterias")
for i in dbase12_cursor:
    if type(i)==type((0,)):
        dbase12.append(list(i))
    else:
        dbase12.append(i)
names = [description[0] for description in dbase12_cursor.description] if dbase12_cursor.description else []
dbase12_conn.commit()
dbase12= {"data":dbase12 ,"names": names,"affected":dbase12_cursor.rowcount}

rst = dbase12


for item in rst["data"]: 
     micobacts[item[0]] = item[1]
     
     
     aislamiento.Append(item[0])
     
     
     


mainpanel.SetSizer(mainsizer)

gridpanel.SetSizer(s1)

buttonpanel.SetSizer(btnsizer)

querypanel.SetSizer(querysizer)

gridpanel2.SetSizer(s2)

buttonpanelq.SetSizer(btnsizerq)

nb1.AddPage(mainpanel,"Determinaciones")

nb1.AddPage(querypanel,"Consultas")

frm1.SetTitle("Registro Determinaciones Micobacterias")

frm1.SetIcon(wx.Icon("microscope.ico"))

font = wx.Font(24,wx.MODERN,wx.NORMAL,wx.BOLD,True,"Microsoft Sans Serif")


labtitulo.SetFont(font)

labqtitulo.SetFont(font)

font = wx.Font(11,wx.MODERN,wx.NORMAL,wx.NORMAL,False,"Microsoft Sans Serif")


labbus.SetFont(font)

txtbus.SetFont(font)

labfecha.SetFont(font)

fecha.SetFont(font)

labnhc.SetFont(font)

nhc.SetFont(font)

labidmues.SetFont(font)

idmues.SetFont(font)

labfecham.SetFont(font)

fecham.SetFont(font)

labdet.SetFont(font)

det.SetFont(font)

labmues.SetFont(font)

muestra.SetFont(font)

labres.SetFont(font)

resultado.SetFont(font)

labacc.SetFont(font)

acciones.SetFont(font)

labseguir.SetFont(font)

labais.SetFont(font)

aislamiento.SetFont(font)

labmico1.SetFont(font)

mico1l.SetFont(font)

labqpac.SetFont(font)

qpac.SetFont(font)

labqmues.SetFont(font)

qmues.SetFont(font)

labmico2.SetFont(font)

labqseguir.SetFont(font)

mico2l.SetFont(font)

font = wx.Font(11,wx.MODERN,wx.NORMAL,wx.NORMAL,False,"Microsoft Sans Serif")


buscar_btn.SetFont(font)

guardar_btn.SetFont(font)

borrar_btn.SetFont(font)

salir_btn.SetFont(font)

guardarq_btn.SetFont(font)

borrarq_btn.SetFont(font)

salirq_btn.SetFont(font)

consultar_btn.SetFont(font)

labtitulo.SetForegroundColour([80,80,80])

labqtitulo.SetForegroundColour([80,80,80])

labbus.SetForegroundColour([80,80,80])

labfecha.SetForegroundColour([80,80,80])

labnhc.SetForegroundColour([80,80,80])

labidmues.SetForegroundColour([80,80,80])

labfecham.SetForegroundColour([80,80,80])

labdet.SetForegroundColour([80,80,80])

labmues.SetForegroundColour([80,80,80])

labres.SetForegroundColour([80,80,80])

labacc.SetForegroundColour([80,80,80])

labseguir.SetForegroundColour([80,80,80])

labais.SetForegroundColour([80,80,80])

labmico1.SetForegroundColour([80,80,80])

labmico2.SetForegroundColour([80,80,80])

labqpac.SetForegroundColour([80,80,80])

labqmues.SetForegroundColour([80,80,80])

labqseguir.SetForegroundColour([80,80,80])

frm1.Show()

frm1.SetSize([800,950])

frm1.Center()























































































root.MainLoop()
