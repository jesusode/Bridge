
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
from python_runtime import _toMatrix,_invert,_toDict,_copy,_appendRow,_getList,_insertRow,_appendCol,_insertCol,_getCol,_getRow,_getDimensions,_size,_toint,_tofloat,_abs,_strip,_count,_indexof,_histogram
from python_runtime import _chain,_zip,_cartessian, _combinations,_combinations_with_r, _permutations,_enumerate, _starmap, _list,_cycle,_split,_join,_readf,_readflines,_system,_lisp,_scheme,_lispModule,_clojure
from python_runtime import _xmltod,_dtoxml,_transaction,_rollback,_isclass,_cmdline,_toUnicode,_slice,_checkType,_xmlstr,_applyXSLT,_geturl,_open,_C,_getC
#-----------------------------------------------------------------------------------------------------


__typedefs={'numeric':[],'chain':[]}
__type_instances={}
__basecons={}
__pyBases=[]

import os


import zipfile


import wx.lib


import wx.lib.imagebrowser


import minimalfpdf


import markdown


import mini_rtf


python_runtime._check_py_bases([minimalfpdf.MinimalFPDF])
class mixin(minimalfpdf.MinimalFPDF):
    def __init__(self,*k,**kw):
        minimalfpdf.MinimalFPDF.__init__(self,*k,**kw)
    



def item_activated ( evt):
        _print(evt.GetEventObject().GetItemText(evt.GetItem()))
        
        

def print_grid ( evt):
     _print("dummy!")
     
     

def menu_callb ( evt):
     _print("item de menu pulsado")
     
     

def exit ( evt):
     frm1.Destroy()
     
     

def add_resource ( evt):
     global resources,statusbar
     
     st = wx.OPEN|wx.FD_MULTIPLE
     
     
     dlg = wx.FileDialog(frm1,message="Add Resources",defaultDir="",defaultFile="",wildcard="*.*",style=st)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          res = dlg.GetPaths()
          
          
          titem = get_tree_item(tree1,"Resources",tree1.GetRootItem())
          
          
          for item in res: 
               
               if item not in resources : 
                    addTreeNodes(tree1,titem,[os.path.basename(item)])
                    
                    python_runtime._append2(item,resources)
                    
                    statusbar.SetStatusText(python_runtime.doAddition("Added resource: ",os.path.basename(item)))
                    
                    
                    
                    
               
               
               
               
               
          
          
          
          
          
     
     
     
     
     
     
     
     

def add_part ( evt):
     global resources,statusbar,part_counter
     
     dlg = wx.FileDialog(frm1,message="Add Part",defaultDir="",defaultFile="",wildcard="*.*",style=wx.SAVE)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          res = dlg.GetPath()
          
          
          open(res,"w").close()
          
          
          text0=""
          if os.path.exists(res) and os.path.isfile(res):
              text0=open(res,"a")
              text0.write(editor.GetValue())
              text0.close()
          else:
               raise Exception('Error: "%s" debe ser un archivo valido'%res)
          
          dirty = False
          
          
          curfile = res
          
          
          part_counter+=1
          
          num = _tostring(part_counter)
          
          
          item = get_tree_item(tree1,"Parts",tree1.GetRootItem())
          
          
          addTreeNodes(tree1,item,[python_runtime.doAddition(python_runtime.doAddition(num," : "),os.path.basename(res))])
          
          parts[num] = res
          
          
          statusbar.SetStatusText(python_runtime.doAddition(python_runtime.doAddition(python_runtime.doAddition("Added part: ",os.path.basename(res))," as "),num))
          
          
          
          
          
          
          
          
          
          
          
          
     
     
     
     
     
     
     

def show_images ( evt):
     global resources,statusbar
     
     _print("Visor de imagenes")
     
     dlg = wx.lib.imagebrowser.ImageDialog(frm1,".")
     
     
     dlg.Center()
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          img = dlg.GetFile()
          
          
          item = get_tree_item(tree1,"Resources",tree1.GetRootItem())
          
          
          addTreeNodes(tree1,item,[os.path.basename(img)])
          
          python_runtime._append2(img,resources)
          
          statusbar.SetStatusText(python_runtime.doAddition("Added resource: ",os.path.basename(img)))
          
          
          
          
          
          
     
     
     
     
     
     
     
     
     

def change_bgcolor ( evt):
     global bgcolor
     
     dlg = wx.ColourDialog(frm1)
     
     
     dlg.GetColourData().SetChooseFull(True)
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          color = list(dlg.GetColourData().GetColour().Get())
          
          
          editor.SetBackgroundColour(color)
          
          bgcolor = color
          
          
          
          
          
     
     
     
     
     
     
     
     

def change_fcolor ( evt):
     global fcolor
     
     dlg = wx.ColourDialog(frm1)
     
     
     dlg.GetColourData().SetChooseFull(True)
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          color = list(dlg.GetColourData().GetColour().Get())
          
          
          editor.SetForegroundColour(color)
          
          fcolor = color
          
          
          
          
          
     
     
     
     
     
     
     
     

def change_font ( evt):
     global fnt,fcolor
     
     data = wx.FontData()
     
     
     data.EnableEffects(True)
     
     data.SetColour(wx.BLACK)
     
     data.SetInitialFont(editor.GetFont())
     
     dlg = wx.FontDialog(frm1,data)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          data = dlg.GetFontData()
          
          
          font = data.GetChosenFont()
          
          
          color = list(data.GetColour())
          
          
          editor.SetFont(font)
          
          editor.SetForegroundColour(color)
          
          fnt = font
          
          
          fcolor = color
          
          
          
          
          
          
          
          
          
     
     
     
     
     
     
     
     
     
     
     

def delete_content ( evt):
     editor.SetValue("")
     
     

def save_editor ( evt):
     global dirty,curfile
     
     
     if curfile == None : 
          dlg = wx.FileDialog(frm1,message="Save as...",defaultDir="",defaultFile="",wildcard="*.*",style=wx.SAVE)
          
          
          
          if dlg.ShowModal() == wx.ID_OK : 
               f = dlg.GetPath()
               
               
               open(f,"w").close()
               
               
               text1=""
               if os.path.exists(f) and os.path.isfile(f):
                   text1=open(f,"a")
                   text1.write(editor.GetValue())
                   text1.close()
               else:
                    raise Exception('Error: "%s" debe ser un archivo valido'%f)
               
               dirty = False
               
               
               curfile = f
               
               
               
               
               
               
               
          
          
          
          
          
          
     else:
          f = _open(curfile,"w")
          
          
          f.write(editor.GetValue())
          
          f.close()
          
          dirty = False
          
          
          
          
          
          
     
     
     
     
     statusbar.SetStatusText(python_runtime.doAddition("Contenido guardado en : ",curfile))
     
     
     
     

def save_editor_as ( evt):
     global curfile
     
     curfile = None
     
     
     save_editor(evt)
     
     
     
     

def load_editor ( evt):
     global curfile,dirty
     
     dlg = wx.FileDialog(frm1,message="Abrir archivo",defaultDir="",defaultFile="",wildcard="*.*",style=wx.OPEN)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          f = dlg.GetPath()
          
          
          editor.SetValue(_readf(f))
          
          dirty = False
          
          
          curfile = f
          
          
          statusbar.SetStatusText(python_runtime.doAddition("Cargado contenido de : ",curfile))
          
          
          
          
          
          
     
     
     
     
     
     
     

def insert_file ( evt):
     global dirty
     
     dlg = wx.FileDialog(frm1,message="Insertar archivo",defaultDir="",defaultFile="",wildcard="*.*",style=wx.OPEN)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          f = dlg.GetPath()
          
          
          cont = editor.GetValue()
          
          
          cont = python_runtime.doAddition(cont,_readf(f))
          
          
          editor.SetValue(cont)
          
          dirty = True
          
          
          statusbar.SetStatusText(python_runtime.doAddition("Insertado contenido de : ",f))
          
          
          
          
          
          
          
     
     
     
     
     
     
     

def save_config ( evt):
     global fcolor,bgcolor,fnt
     
     ft = [fnt.GetPointSize(),fnt.GetFamily(),fnt.GetStyle(),fnt.GetWeight(),fnt.GetUnderlined(),fnt.GetFaceName(),fnt.GetEncoding()]
     
     
     config = [fcolor,bgcolor,ft]
     
     
     dlg = wx.FileDialog(frm1,message="Save Config",defaultDir="",defaultFile="new.cfg",wildcard="*.cfg",style=wx.SAVE)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          python_runtime.doSerialize(config,dlg.GetPath())
          
          
          
     
     
     
     
     
     
     
     
     

def load_config ( evt):
     global fcolor,bgcolor,fnt
     
     dlg = wx.FileDialog(frm1,message="Load Config",defaultDir="",defaultFile="",wildcard="*.cfg",style=wx.OPEN)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          config = python_runtime.doDeserialize(dlg.GetPath())
          
          
          
          _print(config)
          
          _print(repr(config[1]))
          
          editor.SetForegroundColour(config[0])
          
          editor.SetBackgroundColour(config[1])
          
          f = wx.Font(*config[2])
          
          
          _print(f)
          
          _print(f.GetFaceName())
          
          _print(f.GetPointSize())
          
          editor.SetFont(f)
          
          
          
          
          
          
          
          
          
          
          
     
     
     
     
     
     
     

def export_html ( evt):
     dlg = wx.FileDialog(frm1,message="Exportar a HTML",defaultDir="",defaultFile="export.html",wildcard="*.txt",style=wx.SAVE)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          f = dlg.GetPath()
          
          
          open(f,"w").close()
          
          
          text2=""
          if os.path.exists(f) and os.path.isfile(f):
              text2=open(f,"a")
              text2.write(editor.GetValue())
              text2.close()
          else:
               raise Exception('Error: "%s" debe ser un archivo valido'%f)
          
          statusbar.SetStatusText(python_runtime.doAddition("Exportado contenido como HTML a : ",f))
          
          
          
          
          
     
     
     
     
     
     

def export_xml ( evt):
     dlg = wx.FileDialog(frm1,message="Exportar a XML",defaultDir="",defaultFile="export.xml",wildcard="*.txt",style=wx.SAVE)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          f = dlg.GetPath()
          
          
          open(f,"w").close()
          
          
          text3=""
          if os.path.exists(f) and os.path.isfile(f):
              text3=open(f,"a")
              text3.write(editor.GetValue())
              text3.close()
          else:
               raise Exception('Error: "%s" debe ser un archivo valido'%f)
          
          statusbar.SetStatusText(python_runtime.doAddition("Exportado contenido como XML a : ",f))
          
          
          
          
          
     
     
     
     
     
     

def export_md ( evt):
     dlg = wx.FileDialog(frm1,message="Exportar Markdown",defaultDir="",defaultFile="export.html",wildcard="*.html",style=wx.SAVE)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          f = dlg.GetPath()
          
          
          open(f,"w").close()
          
          
          cont = markdown.markdown(editor.GetValue())
          
          
          text4=""
          if os.path.exists(f) and os.path.isfile(f):
              text4=open(f,"a")
              text4.write(cont)
              text4.close()
          else:
               raise Exception('Error: "%s" debe ser un archivo valido'%f)
          
          statusbar.SetStatusText(python_runtime.doAddition("Exportado contenido como Markdown a : ",f))
          
          
          
          
          
          
     
     
     
     
     
     

def export_pdf ( evt):
     dlg = wx.FileDialog(frm1,message="Exportar a PDF",defaultDir="",defaultFile="export.pdf",wildcard="*.txt",style=wx.SAVE)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          f = dlg.GetPath()
          
          
          pdf = mixin()
          
          
          pdf.add_page()
          
          cont = editor.GetValue()
          
          
          match0=[]
          if os.path.exists(cont) and os.path.isfile(cont):
              match0 += re.findall(open(cont).read(),"<.+>")
          else:
              match0+=re.findall("<.+>",cont)
          
          has_html = match0
          
          
          
          if has_html == [] : 
               cont = _join((list(itertools.imap(lambda x: python_runtime.doAddition(python_runtime.doAddition("<p>",x),"</p>"),list(itertools.chain(_split(cont,"\n")))))),"\n")
               
               
               
          
          
          
          
          pdf.write_html(cont)
          
          pdf.output(f,"F")
          
          statusbar.SetStatusText(python_runtime.doAddition("Exportado contenido como PDF a : ",f))
          
          
          
          
          
          
          
          
          
          
     
     
     
     
     
     

def export_rtf ( evt):
     dlg = wx.FileDialog(frm1,message="Exportar a RTF",defaultDir="",defaultFile="export.rtf",wildcard="*.txt",style=wx.SAVE)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          f = dlg.GetPath()
          
          
          open(f,"w").close()
          
          
          text5=""
          if os.path.exists(f) and os.path.isfile(f):
              text5=open(f,"a")
              text5.write(editor.GetValue())
              text5.close()
          else:
               raise Exception('Error: "%s" debe ser un archivo valido'%f)
          
          statusbar.SetStatusText(python_runtime.doAddition("Exportado contenido como RTF a : ",f))
          
          
          
          
          
     
     
     
     
     
     

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
          
          
     
     
     f = mini_tkbasic.getTkFile("Guardar archivo","save")
     
     
     
     if f != None : 
          mini_rtf.rtfSaveDoc("tmp",f)
          
          
     
     
     
     
     
     
     
     
     
     
     

def export_txt ( evt):
     dlg = wx.FileDialog(frm1,message="Exportar a texto",defaultDir="",defaultFile="export.txt",wildcard="*.txt",style=wx.SAVE)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          f = dlg.GetPath()
          
          
          open(f,"w").close()
          
          
          text6=""
          if os.path.exists(f) and os.path.isfile(f):
              text6=open(f,"a")
              text6.write(editor.GetValue())
              text6.close()
          else:
               raise Exception('Error: "%s" debe ser un archivo valido'%f)
          
          statusbar.SetStatusText(python_runtime.doAddition("Exportado contenido como texto a : ",f))
          
          
          
          
          
     
     
     
     
     
     

def build_book ( evt):
     global parts,resources,views
     
     dlg = wx.FileDialog(frm1,message="Construir Book",defaultDir="",defaultFile="new_book.book",wildcard="*.book",style=wx.SAVE)
     
     
     
     if dlg.ShowModal() == wx.ID_OK : 
          f = dlg.GetPath()
          
          
          book = zipfile.ZipFile(f,mode="w")
          
          
          resume = ""
          
          
          for item in parts: 
               book.write(parts[item],python_runtime.doAddition(python_runtime.doAddition("parts/",item),".txt"))
               
               resume = python_runtime.doAddition(python_runtime.doAddition(resume,item),"\r\n")
               
               
               
               
          
          
          book.writestr("parts/index.txt",resume)
          
          resume = ""
          
          
          for item in resources: 
               book.write(item,python_runtime.doAddition("resources/",os.path.basename(item)))
               
               resume = python_runtime.doAddition(python_runtime.doAddition(resume,os.path.basename(item)),"\r\n")
               
               
               
               
          
          
          book.writestr("resources/index.txt",resume)
          
          resume = ""
          
          
          for item in views: 
               book.write(item,python_runtime.doAddition("views/",os.path.basename(item)))
               
               resume = python_runtime.doAddition(python_runtime.doAddition(resume,os.path.basename(item)),"\r\n")
               
               
               
               
          
          
          book.writestr("views/index.txt",resume)
          
          book.close()
          
          statusbar.SetStatusText(python_runtime.doAddition("Built new book : ",f))
          
          
          
          
          
          
          
          
          
          
          
     
     
     
     
     
     
     

def load_book ( evt):
     global parts,resources,views
     
     _print("loading book")
     
     
     














root=wx.App()

frm1=wx.Frame(parent=None)
mbar=wx.MenuBar()
frm1.SetMenuBar(mbar)
file=wx.Menu()
mbar.Append(file,title="A&rchivo")
edit=wx.Menu()
mbar.Append(edit,title="&Editar")
tools=wx.Menu()
mbar.Append(tools,title="&Herramientas")
submenu=wx.Menu()
file_openbook=wx.MenuItem(file,wx.NewId(),text="Abrir Book",kind=wx.ITEM_NORMAL)
file.AppendItem(file_openbook)
frm1.Bind(wx.EVT_MENU,load_book,file_openbook)
file.AppendSeparator()
file_build=wx.MenuItem(file,wx.NewId(),text="Generar book",kind=wx.ITEM_NORMAL)
file.AppendItem(file_build)
frm1.Bind(wx.EVT_MENU,build_book,file_build)
file.AppendSeparator()
file_savepart=wx.MenuItem(file,wx.NewId(),text="Guardar parte",kind=wx.ITEM_NORMAL)
file.AppendItem(file_savepart)
frm1.Bind(wx.EVT_MENU,add_part,file_savepart)
file.AppendSeparator()
file_addres=wx.MenuItem(file,wx.NewId(),text="Incorporar recurso",kind=wx.ITEM_NORMAL)
file.AppendItem(file_addres)
frm1.Bind(wx.EVT_MENU,add_resource,file_addres)
file.AppendSeparator()
file_open=wx.MenuItem(file,wx.NewId(),text="&Abrir archivo\tCtrl+A",kind=wx.ITEM_NORMAL)
file.AppendItem(file_open)
frm1.Bind(wx.EVT_MENU,load_editor,file_open)
file.AppendSeparator()
file_insert=wx.MenuItem(file,wx.NewId(),text="Insertar archivo",kind=wx.ITEM_NORMAL)
file.AppendItem(file_insert)
frm1.Bind(wx.EVT_MENU,insert_file,file_insert)
file.AppendSeparator()
file_close=wx.MenuItem(file,wx.NewId(),text="Cerrar archivo",kind=wx.ITEM_NORMAL)
file.AppendItem(file_close)
frm1.Bind(wx.EVT_MENU,menu_callb,file_close)
file.AppendSeparator()
file_save=wx.MenuItem(file,wx.NewId(),text="&Guardar archivo\tCtrl+S",kind=wx.ITEM_NORMAL)
file.AppendItem(file_save)
frm1.Bind(wx.EVT_MENU,save_editor,file_save)
file.AppendSeparator()
file_saveas=wx.MenuItem(file,wx.NewId(),text="&Guardar archivo como...\tCtrl+Alt+S",kind=wx.ITEM_NORMAL)
file.AppendItem(file_saveas)
frm1.Bind(wx.EVT_MENU,save_editor_as,file_saveas)
file.AppendSeparator()
file_sub=wx.MenuItem(file,wx.NewId(),text="Exportar",kind=wx.ITEM_NORMAL,subMenu=submenu)
file.AppendItem(file_sub)
file.AppendSeparator()
file_saveconf=wx.MenuItem(file,wx.NewId(),text="Guardar configuracion",kind=wx.ITEM_NORMAL)
file.AppendItem(file_saveconf)
frm1.Bind(wx.EVT_MENU,save_config,file_saveconf)
file.AppendSeparator()
file_loadconf=wx.MenuItem(file,wx.NewId(),text="Cargar configuracion",kind=wx.ITEM_NORMAL)
file.AppendItem(file_loadconf)
frm1.Bind(wx.EVT_MENU,load_config,file_loadconf)
file.AppendSeparator()
file_exit=wx.MenuItem(file,wx.NewId(),text="&Salir\tCtrl+S",kind=wx.ITEM_NORMAL)
file.AppendItem(file_exit)
frm1.Bind(wx.EVT_MENU,exit,file_exit)
sub_1=wx.MenuItem(submenu,wx.NewId(),text="HTML",kind=wx.ITEM_NORMAL)
submenu.AppendItem(sub_1)
frm1.Bind(wx.EVT_MENU,export_html,sub_1)
submenu.AppendSeparator()
sub_6=wx.MenuItem(submenu,wx.NewId(),text="XML",kind=wx.ITEM_NORMAL)
submenu.AppendItem(sub_6)
frm1.Bind(wx.EVT_MENU,export_xml,sub_6)
submenu.AppendSeparator()
sub_7=wx.MenuItem(submenu,wx.NewId(),text="Markdown",kind=wx.ITEM_NORMAL)
submenu.AppendItem(sub_7)
frm1.Bind(wx.EVT_MENU,export_md,sub_7)
submenu.AppendSeparator()
sub_2=wx.MenuItem(submenu,wx.NewId(),text="PDF",kind=wx.ITEM_NORMAL)
submenu.AppendItem(sub_2)
frm1.Bind(wx.EVT_MENU,export_pdf,sub_2)
submenu.AppendSeparator()
sub_4=wx.MenuItem(submenu,wx.NewId(),text="RTF",kind=wx.ITEM_NORMAL)
submenu.AppendItem(sub_4)
frm1.Bind(wx.EVT_MENU,export_rtf,sub_4)
submenu.AppendSeparator()
sub_5=wx.MenuItem(submenu,wx.NewId(),text="TXT",kind=wx.ITEM_NORMAL)
submenu.AppendItem(sub_5)
frm1.Bind(wx.EVT_MENU,export_txt,sub_5)
edit_find=wx.MenuItem(edit,wx.NewId(),text="Buscar",kind=wx.ITEM_NORMAL)
edit.AppendItem(edit_find)
edit.AppendSeparator()
edit_replace=wx.MenuItem(edit,wx.NewId(),text="Reemplazar",kind=wx.ITEM_NORMAL)
edit.AppendItem(edit_replace)
edit.AppendSeparator()
edit_copy=wx.MenuItem(edit,wx.NewId(),text="Copiar",kind=wx.ITEM_NORMAL)
edit.AppendItem(edit_copy)
edit_cut=wx.MenuItem(edit,wx.NewId(),text="Cortar",kind=wx.ITEM_NORMAL)
edit.AppendItem(edit_cut)
edit.AppendSeparator()
edit_paste=wx.MenuItem(edit,wx.NewId(),text="Pegar",kind=wx.ITEM_NORMAL)
edit.AppendItem(edit_paste)
edit.AppendSeparator()
edit_font=wx.MenuItem(edit,wx.NewId(),text="Cambiar fuente",kind=wx.ITEM_NORMAL)
edit.AppendItem(edit_font)
frm1.Bind(wx.EVT_MENU,change_font,edit_font)
edit_fontcolor=wx.MenuItem(edit,wx.NewId(),text="Cambiar color de fuente",kind=wx.ITEM_NORMAL)
edit.AppendItem(edit_fontcolor)
frm1.Bind(wx.EVT_MENU,change_fcolor,edit_fontcolor)
edit_bgcolor=wx.MenuItem(edit,wx.NewId(),text="Cambiar color de fondo",kind=wx.ITEM_NORMAL)
edit.AppendItem(edit_bgcolor)
frm1.Bind(wx.EVT_MENU,change_bgcolor,edit_bgcolor)
edit.AppendSeparator()
edit_delete=wx.MenuItem(edit,wx.NewId(),text="Borrar",kind=wx.ITEM_NORMAL)
edit.AppendItem(edit_delete)
frm1.Bind(wx.EVT_MENU,delete_content,edit_delete)
tools_images=wx.MenuItem(tools,wx.NewId(),text="Visor de imagenes",kind=wx.ITEM_NORMAL)
tools.AppendItem(tools_images)
frm1.Bind(wx.EVT_MENU,show_images,tools_images)
split1=wx.SplitterWindow(frm1,style=wx.SP_3DBORDER|wx.SP_BORDER)
p1=wx.Panel(split1,style=wx.SUNKEN_BORDER)
s1=wx.GridSizer(rows=1,cols=1,hgap=0,vgap=0)
editor=wx.TextCtrl(p1,style=wx.TE_MULTILINE)
s1.Add(editor,flag=wx.ALL|wx.EXPAND,border=0)
p2=wx.Panel(split1,style=wx.SUNKEN_BORDER)
s2=wx.GridSizer(rows=1,cols=1,hgap=0,vgap=0)
tree1=treeFactory(p2,data=[["Parts",[]],["Resources",[]],["Views",[]]],root="New Book",size=[200,300],style=wx.TR_HAS_BUTTONS)
s2.Add(tree1,flag=wx.ALL|wx.EXPAND)
tree1.Bind(wx.EVT_TREE_ITEM_ACTIVATED,item_activated)



parts = None
resources = None
views = None
book = None
statusbar = None



fcolor = None
fnt = None
bgcolor = None
dirty = None
curfile = None
part_counter = None



parts = {}


resources = []


views = []


fnt = editor.GetFont()


fcolor = editor.GetForegroundColour()


bgcolor = editor.GetBackgroundColour()


part_counter = 0


dirty = True


frm1.SetTitle("Minimal Book Maker v.1.0")

frm1.SetIcon(wx.Icon("book.ico"))

statusbar = frm1.CreateStatusBar()


frm1.Show()

frm1.SetSize([800,600])

p1.SetSizer(s1)

p2.SetSizer(s2)

split1.SetMinimumPaneSize(40)

split1.SplitVertically(p2,p1,130)

tree1.Expand(tree1.GetRootItem())

frm1.Center()

























root.MainLoop()
