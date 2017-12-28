#!Python
import sys
import shutil
import os
import re

#Incluimos minimal para poder tener controladores minimal----------------
import bridge
import stlex2
miniparser=bridge.parser
#------------------------------------------------------------------------

#Patch para la ultima version de ply(no va con jython)
#Version de ply:2.5, superiores no van con jython
#Problema: usa parsetab.py para todos los analizadores
if 'java' in sys.platform: 
    #print 'como java'
    if not 'lex' in sys.modules:
        lex=__import__('lex')
    else:
        lex=sys.modules['lex']
    if not 'yacc' in sys.modules:
        yacc=__import__('yacc')
    else:
        yacc=sys.modules['yacc']
else:
    #print 'como cpython'
    from ply import lex
    from ply import yacc

import gui_lexer

#Para generacion automatizada de ejecutables en win32------
import exegen
#----------------------------------------------------------

#Texto del programa
program=''

# Get the token map from the lexer.  This is required.
tokens=gui_lexer.tokens

#Tabla global de definiciones para plantillas de variables y nombres de las funciones de evento
namespace={}

#Lista de globales a incluir
py_globals=['root']

#Lista de tipos de gui aceptados
guis=['tkinter','xhtml','dotnet','qt','gtk','swing','wx']

#Cadena con la libreria objetivo
target_gui=''

#Cadena con el codigo de la aplicacion
codestring=''

#Cadena con el codigo de soporte(manejadores de eventos dependientes de lenguaje, etc)
supportstring=''

#Cadena con el codigo de inicializacion de la app
initstring=''

#Cadena con el codigo de cabecera (util sobre todo para xhtml)
headerstring=''

#Cadena con el nombre del archivo a generar
fname='gui_parser_output.py'

#Nombre del elemento(frame o window) principal(solo para wx)
TOPLEVEL_WINDOW=''

outputfile='gui.py' #Nombre del archivo de salida (opcion -o)
outputdir='.' #Directorio de salida donde se pondra el archivo generado y/o el ejecutable (opcion -d)

#Variables globales controlables para generar ejecutables--------------------------------------
create_exe=0 #Crear o no un ejecutable (opcion -e)
exe_type='console' #Opcion -k en linea de comandos
#Disponibles: [console,windows,service,com_server,ctypes_com_server]
exe_props='' #Archivo de propiedades para generar el ejecutable (opcion -p)
extra_files=[] #Archivos de usuario a copiar el el dir del ejecutable (opcion -i)
#Archivos de los que depende para compilar con py2exe
__dependencies=[]
#-----------------------------------------------------------------------------------------------

#funcion de utilidad que asegura que no se repitan identificadores??
def checkID(id): #REVISAR ESTO!!!
    #global py_globals
    #if id in py_globals: raise Exception('Error: El identificador "%s" ya se ha utilizado'%id)
    pass

#Funciones y plantilla para XHTML-------------------------------------------
xhtml_template="""
<!DOCTYPE html"
        "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>--Put your title here--</title>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script>%%SUPPORT_CODE%%</script>
<script>
$(document).ready(function() {

%%INIT_CODE%%

});
</script>
%%HEADER_CODE%%
</head>
<body>
<div id="root">
%%GUI_CODE%%
</div>
</body>
</html>""";

xhtml_table={
    'label' : '<span id="%s" %s>%s</span>',
    'button' : '<input type="button" name="%s" id="%s" %s/>',
    'textbox' : '<input type="text" name="%s" id="%s" %s/>',
    'textarea' : '<textarea name="%s" id="%s" %s>%s</textarea>',
    'frame' : '<iframe id="%s" %s></iframe>',
    'form' : '<form id="%s" %s></form>',
    'listbox' : '<select multiple id="%s" name="%s" %s>%s</select>',
    'image' : '<img id="%s" %s/>',
    'check' : '<input type="checkbox" name="%s" id="%s" %s/>',
    'option' : '<option value="%s">%s</option>',
    'radio' : '<input type="radio" name="%s" id="%s" %s/><span id="radiovalue">%s</span>',
    'combobox' : '<select id="%s" name="%s" %s>%s</select>',
    'tablebox' : '<table id="%s" %s>%s</table>',
    'submit' : '<input type="submit" name="%s" id="%s" %s/>',
    'hidden' : '<input type="hidden" name="%s" id="%s" %s/>',
    'password' : '<input type="password" name="%s" id="%s" %s/>',
    'link' : '<a id="%s" %s>%s</a>',
    'raw' : '<div id="%s" %s>%s<div>',
    'file' : '<input type="file" name="%s" id="%s" %s/>',
    'color' : '<input type="color" name="%s" id="%s" %s/>',
    'date' : '<input type="date" name="%s" id="%s" %s/>',
    'datetime' : '<input type="datetime" name="%s" id="%s" %s/>',
    'datetime-local': '<input type="datetime-local" name="%s" id="%s" %s/>',
    'email' : '<input type="email" name="%s" id="%s" %s/>',
    'month' : '<input type="month" name="%s" id="%s" %s/>',
    'number' : '<input type="number" name="%s" id="%s" %s/>',
    'range' : '<input type="range" name="%s" id="%s" %s/>',
    'search' : '<input type="search" name="%s" id="%s" %s/>',
    'tel' : '<input type="tel" name="%s" id="%s" %s/>',
    'time' : '<input type="time" name="%s" id="%s" %s/>',
    'url' : '<input type="url" name="%s" id="%s" %s/>',
    'pattern' : '<input type="pattern" name="%s" id="%s" %s/>',
    'week' : '<input type="week" name="%s" id="%s" %s/>'
}

#Entradas de tipo {'template':cadena_final,'parts':[partes]}
xhtml_globals={}

def xhtml_process_toplevel_elem(name,stack,props):
    global xhtml_globals #Excepcion si name ya esta definido
    checkID(name)
    xhtml_globals[name]={'template':('<div id="%s" %s>'%(name,props)) + '%s</div>\n','parts':[]}
    return ''

def xhtml_process_window_elem(name,stack,props):
    global xhtml_globals #Excepcion si name ya esta definido
    checkID(name)
    xhtml_globals[name]={'template':('<div id="%s" %s>'%(name,props)) + '%s</div>\n','parts':[]}
    return ''

def xhtml_process_bind_event(name,callb,evt_name):#frame.bind("<Button-1>", callback)
    global initstring #Enlazamos con jquery
    initstring+='$("#%s").bind(%s,%s);\n'%(name,evt_name,callb)
    return ''

def xhtml_process_app_elem_desc(klass,name,parent,props,stack):
    global xhtml_globals,namespace
    checkID(name)
    s=xhtml_table[klass]
    prps={}
    #print 'valor de s: %s' % s
    if parent=='nothing':
        parent=''
    if not props:
        props=''
    else: #Ojo, se permiten formas no a=b en props!!!!!
        for p in props.split(','):
            k,v= p.strip().split('=')
            prps[k]=v
        #print 'prps: %s' % prps
        props=' '.join([i + '=%s'%prps[i] for i in prps if i!='text'])
        #print 'props: %s' % props
    if klass in ['button','textbox','textarea','listbox','check','radio','option',
    'combobox','submit','hidden','password','file','color','date','datetime',
    'datetime-local','email','month','number','range','search','tel','time','url','week','pattern']:
        #'<input type="text" name="%s" id="%s" %s/>',
        cont=''
        if klass in ['combobox','listbox']: #opciones en atributo options
            if parent:
                if prps.has_key('options'):
                    if prps['options'][0]=='@': #Sustituir antes de expandir!!
                       opts= namespace[prps['options']]
                       cont='\n'.join(['<option value="%s">%s</option>'%(item,item) for item in opts.split(',')])
                    xhtml_globals[parent]['parts'].append((s + '\n')%(name,name,props,cont))
        elif klass in ['textarea']:
            if parent:
                if prps.has_key('text'):
                    cont=prps['text']
                    xhtml_globals[parent]['parts'].append((s + '\n')%(name,name,props,cont.strip('"')))
        else:
            if parent:
                if klass=='radio' and prps.has_key('options'):
                    if prps['options'][0]=='@': #Sustituir antes de expandir!!
                       opts= namespace[prps['options']].split(',')
                       print 'VALOR DE OPTS: %s' % opts
                       t=''
                       for item in opts: #Copiar tantas veces la plantilla como opciones haya
                           t+=(s + '\n')%(name,name,props,item.strip('"'))
                       xhtml_globals[parent]['parts'].append(t + '\n')
                else:
                    xhtml_globals[parent]['parts'].append((s + '\n')%(name,name,props))
    else:
        #print 'cadena a sustituir: %s' % s
        cont=''
        if klass=='image':
            if parent:
                    xhtml_globals[parent]['parts'].append((s + '\n')%(name,props))
        elif klass in ['label','link']:
            if parent:
                if prps.has_key('text'):
                    cont=prps['text']
                    xhtml_globals[parent]['parts'].append((s + '\n')%(name,props,cont.strip('"')))
    return ''

def xhtml_process_user_desc(klass,name,parent,props,stack): #Revisar
    global py_globals #Excepcion si name ya esta definido
    checkID(name)
    prps={}
    #solo se acepta "raw": el resto da excepcion porque no existen, contenido en opcion "html"
    s=xhtml_table[klass]
    if parent:
        for p in props.split(','):
            k,v= p.strip().split('=')
            prps[k]=v
        #print 'prps: %s' % prps
        props=' '.join([i + '=%s'%prps[i] for i in prps if i!='html'])
        html=prps['html'].strip('"')
        xhtml_globals[parent]['parts'].append((s + '\n')%(name,props,html))
    return ''

def xhtml_process_menu_desc(klass,name,parent,props,topmenu):
    return ''

def xhtml_process_menuitem_desc(klass,name,parent,props):
    return ''

#---------------------------------------------------------------------------

#Funciones y plantillas para Tkinter----------------------------------------
tkinter_template='''
import sys
sys.path.append('.')#Para py2exe
sys.path.append('./modules')#Para py2exe
sys.path.append('library.zip')#Para py2exe

%%HEADER_CODE%%

import Tkinter
import Tix
import ttk
root=Tkinter.Tk()

%%SUPPORT_CODE%%

%%GUI_CODE%%

def init_code():
    global %%GLOBALVARS%%
%%INIT_CODE%%

init_code()

root.mainloop()

'''

tkinter_table={
  'label' : '%s=Tkinter.Label(',
  'button' : '%s=Tkinter.Button(',
  'textbox' : '%s=Tkinter.Entry(',
  'textarea' : '%s=Tkinter.Text(',
  'panel' : '%s=Tkinter.Panel(',
  'frame' : '%s=Tkinter.Frame(',
  'listbox' : '%s=Tkinter.Listbox(',
  'spinbox' : '%s=Tkinter.Spinbox(',
  'image' : '%s=Tkinter.PhotoImage(',
  'canvas' : '%s=Tkinter.Canvas(',
  'stringvar' : '%s=Tkinter.StringVar(',
  'intvar' : '%s=Tkinter.IntVar(',
  'doublevar' : '%s=Tkinter.DoubleVar(',
  'boolvar' : '%s=Tkinter.BooleanVar(',
  'check' : '%s=Tkinter.Checkbutton(',
  'option' : '%s=Tkinter.OptionMenu(',
  'scale' : '%s=Tkinter.Scale(',
  'radio' : '%s=Tkinter.Radiobutton(',
  'scroll' : '%s=Tkinter.Scrollbar(',
  'menu' :  '%s=Tkinter.Menu(',
  'menuitem' : '%s=Tkinter.Menubutton(',
  'combobox' : '%s=ttk.Combobox(',
  'notebook' : '%s=ttk.Notebook(',
  'progressbar' : '%s=ttk.Progressbar(',
  'separator' : '%s=ttk.Separator(',
  'sizegrip' : '%s=ttk.Sizegrip(',
  'treeview' : '%s=ttk.treeview('
}

def tkinter_process_toplevel_elem(name,stack,props):
    global py_globals #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    return '%s=Tkinter.Toplevel(root)\n'%name

def tkinter_process_window_elem(name,stack,props):
    global py_globals #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    if stack:
        return '%s=Tkinter.Frame(root)\n%s.%s\n'%(name,name,stack)
    else:
        return '%s=Tkinter.Frame(root)\n'% name

def tkinter_process_bind_event(name,callb,evt_name):#frame.bind("<Button-1>", callback)
    global py_globals #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    return '%s.bind(%s,%s)\n'%(name,evt_name,callb)

def tkinter_process_app_elem_desc(klass,name,parent,props,stack):
    global py_globals #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    s=tkinter_table[klass] % name
    if parent=='nothing':parent='None'
    if klass in ['image','stringvar','intvar','boolvar','doublevar']:#ignorar stack
        if props:
            s+='%s,%s)\n'%(parent,props)
        else:
            s+=')\n'
    else:
        if props:
            s += '%s,%s)\n'%(parent,props)
        else:
            s += '%s)\n'%parent
        if stack:
            s += '%s.%s\n'%(name,stack)
    #print 'valor de s: %s' %s
    return s

def tkinter_process_user_desc(klass,name,parent,props,stack): #Revisar
    global py_globals #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    s= name + " = " + klass + '('
    if parent=='nothing': parent='None'
    if props: 
        #print 'props: %s'%props
        return s + '%s,%s)\n%s.%s\n'%(parent,props,name,stack)
    else:
        return s + '%s)\n%s.%s\n'%(parent,name,stack)

def tkinter_process_menu_desc(klass,name,parent,props,topmenu):
    global py_globals #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    s= tkinter_table[klass] % name
    if props: 
        s+= '%s,%s)\n'%(parent,props)
    else:
        s+= '%s)\n'%parent
    if topmenu:
        s+='%s.config(menu=%s)\n'%(parent,name)
    return s

def tkinter_process_menuitem_desc(klass,name,parent,props):
    global py_globals #En Tkinter ignoramos klass
    checkID(name)
    py_globals.append(name)
    s= ''
    if not name in ['cascade','command','separator']:
        raise Exception('Error: En Tkinter solo se aceptan items de menu de tipo "cascade","command" o "separator"')
    if name=='separator':
        return s + '.add_separator()\n'
    s+= parent + '.add_' + name + '('       
    if props: 
        return s + '%s)\n'%props
    else:
        return s + ')\n'

#--------------------------------------------------------------

#Funciones y plantillas para Tkinter----------------------------------------
wx_template='''
import sys
sys.path.append('.')#Para py2exe
sys.path.append('./modules')#Para py2exe
sys.path.append('library.zip')#Para py2exe
import wx
import wx.grid
import wx.html
from wx_support import *

%%HEADER_CODE%%

%%SUPPORT_CODE%%

root=wx.App()

%%GUI_CODE%%

%%INIT_CODE%%

root.MainLoop()
'''

wx_table={
  'label' : '%s=wx.StaticText(',
  'button' : '%s=wx.Button(',
  'textbox' : '%s=wx.TextCtrl(',
  'textarea' : '%s=wx.TextCtrl(',
  'panel' : '%s=wx.Panel(',
  'listbox' : '%s=wx.ListBox(',
  'checklistbox' : '%s=wx.CheckListBox(',
  'spinbox' : '%s=wx.SpinCtrl(',
  'image' : '%s=wx.Image(',
  'bitmap' : '%s=wx.Bitmap(',
  'icon' : '%s=wx.Icon(',
  'check' : '%s=wx.CheckBox(',
  'scale' : '%s=wx.Scale(',
  'radio' : '%s=wx.RadioButton(',
  'radiobox' : '%s=wx.RadioBox(',
  'slider' : '%s=wx.Slider(',
  'topmenu' : '%s=wx.MenuBar(',
  'menu' :  '%s=wx.Menu(',
  'menuitem' : '%s=wx.MenuItem(',
  'combobox' : '%s=wx.ComboBox(',
  'progressbar' : '%s=wx.Gauge(',
  'separator' : '%s.AppendSeparator(',
  'treeview' : '%s=treeFactory(',
  'tablebox' : '%s=tableFactory(',
  'font' : '%s=wx.Font(',
  'splitter' : '%s=wx.SplitterWindow(',
  'boxsizer' : '%s=wx.BoxSizer(',
  'gridsizer' : '%s=wx.GridSizer(',
  'flexgridsizer' : '%s=wx.FlexGridSizer(',
  'gridbagsizer' : '%s=wx.GridBagSizer(',
  'staticboxsizer' : '%s=wx.StaticBoxSizer(',
  'splitter' : '%s=wx.SplitterWindow(',
  'grid' : '%s=gridFactory(',
  'htmlbox' : '%s=htmlWinFactory(',
  'taskbar' : '%s=MinimalTaskBarIcon(',
  'datepicker' : '%s=wx.DatePickerCtrl(',
  'notebook' : '%s=wx.Notebook(',
  'sashwin' : '%s=wx.SashLayoutWindow(',
  'platebutton' : '%s=wx.lib.platebtn.PlateButton(',
  'linkbutton' : '%s=wx.CommandLinkButton(',
  'aquabutton' : '%s=wx.lib.agw.aquabutton.AquaButton(',
  'colourbutton' : '%s=wx.lib.colourselect.ColourSelect(',
  'hyperlink' : '%s=wx.lib.agw.hyperlink.HyperLinkCtrl(',
  'webbrowser' : '%s=wx.html2.WebView.New(',
  'captionbox' : '%s=captionBoxFactory(', #??
  'dialog' : '%s=wx.Dialog(',
  'collapsiblepanel' : '%s=wx.CollapsiblePane(',
  'floatwindow' : '%s=FloatWin(',
  'filebrowsebutton' : '%s=wx.lib.filebrowsebutton.FileBrowseButton(',
  'dirbrowsebutton' : '%s=wx.lib.filebrowsebutton.DirBrowseButton(',
  'line' : '%s=wx.StaticLine(',
  'space' : '',
  'listbook' : '%s=wx.Listbook(',
  'imagelist' : '%s=wx.ImageList(',
  'fontenumerator' : '%s=wx.FontEnumerator(',
  'searchcontrol' : '%s=wx.SearchCtrl('
}

def wx_process_toplevel_elem(name,stack,props):
    global py_globals,TOPLEVEL_WINDOW #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    TOPLEVEL_WINDOW=name
    if props:
        return '%s=wx.Frame(%s)\n'% (name,props)
    else:
        return '%s=wx.Frame()\n'% name

def wx_process_window_elem(name,stack,props):
    global py_globals #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    if props:
        return '%s=wx.ScrolledWindow(%s)\n'% (name,props)
    else:
        return '%s=wx.ScrolledWindow()\n'% name

def wx_process_notebook_elem(name,stack,props):
    global py_globals #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    if props:
        return '%s=wx.Notebook(%s)\n'% (name,props)
    else:
        return '%s=wx.Notebook()\n'% name

def wx_process_bind_event(name,callb,evt_name):#frame.bind("<Button-1>", callback)
    global py_globals,TOPLEVEL_WINDOW #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    if evt_name=='wx.EVT_MENU':
        return '%s.Bind(%s,%s,%s)\n'%(TOPLEVEL_WINDOW,evt_name,callb,name)
    else:
        return '%s.Bind(%s,%s)\n'%(name,evt_name,callb)

def wx_process_app_elem_desc(klass,name,parent,props,stack):
    global py_globals #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    if klass=='separator':
        s=wx_table[klass] % parent
        return s+')\n'
    elif klass=='space':
        #buscar amount
        elems=props.split(',')
        amount=''
        for i in range(len(elems)):
            if elems[i].find('amount')==0:
                amount=elems[i].split('=')[1]
        if amount!='':
            return parent +'.Add((' + amount + ',' + amount + '))\n'
        else:
            return ''
    elif klass in ['image','bitmap','icon']:
        s=wx_table[klass] % name
        if klass in ['icon','image'] and parent not in [None,'nothing']:
            if klass=='icon':
                return s+'%s)\n%s.SetIcon(%s)\n' % (props,parent,name)
            else:
                return s+'%s)\n%s.SetImage(%s)\n' % (props,parent,name)
        else:
            return s+'%s)\n' % props
    s=wx_table[klass] % name
    #print "VALOR de S: %s" % s
    if klass=='taskbar':
        return s+'%s)\n'%props
    if parent=='nothing':
        parent='None'
    if klass in ['boxsizer','gridsizer','gridbagsizer','flexgridsizer','staticbox']:#ignorar stack
        if props:
            s+='%s)\n'%props
        else:
            s+=')\n'
    elif klass=='captionbox':
        #buscar items y caption
        elems=props.split(',')
        items=''
        caption=''
        for i in range(len(elems)):
            if elems[i].find('items')==0:
                items=elems[i].split('=')[1]
            if elems[i].find('caption')==0:
                caption=elems[i].split('=')[1]
        s=s + parent + ',' + caption +')\n'
        #print 'valor de s aqiui: %s' % s
        if stack:
            #print 'valor de stack: %s'%stack
            sz,p=stack.split('$')
            #s += '%s.Add(%s)\n'%(stack, name)
            s += '%s.Add(%s%s)\n'%(sz, name,',' + p if p else '')
        return s
    else:
        if props:
            s += '%s,%s)\n'%(parent,props)
        else:
            s += '%s)\n'%parent
        if stack:
            #print 'valor de stack: %s'%stack
            sz,p=stack.split('$')
            #s += '%s.Add(%s)\n'%(stack, name)
            s += '%s.Add(%s%s)\n'%(sz, name,',' + p if p else '')
    return s

def wx_process_user_desc(klass,name,parent,props,stack): #Revisar
    checkID(name)
    py_globals.append(name)
    s=wx_table[klass] % name
    if parent=='nothing':
        parent='None'
    if props:
        s += '%s,%s)\n'%(parent,props)
    else:
        s += '%s)\n'%parent
    if stack:
        sz,p=stack.split('$')
        s += '%s.Add(%s%s)\n'%(sz, name,',' + p if p else '')
    return s

def wx_process_menu_desc(klass,name,parent,props,topmenu):
    global py_globals #Excepcion si name ya esta definido
    checkID(name)
    py_globals.append(name)
    s=''
    if topmenu:
        s= wx_table['topmenu'] % name + ')\n'
        s+='%s.SetMenuBar(%s)\n'%(parent,name)
    else:
        s= wx_table[klass] % name + ')\n'
        if parent!='nothing':
            s+='%s.Append(%s,%s)\n'%(parent,name,props)
    return s

def wx_process_menuitem_desc(klass,name,parent,props):
    global py_globals #
    checkID(name)
    py_globals.append(name)
    ps=props.split(',')
    props=[]
    image=''
    for it in ps:
        parts=it.split('=')
        if parts[0]=='bitmap':
            image=parts[1]
        else:
            props.append(it)
    props=','.join(props)
    s= wx_table[klass] % name
    s+= '%s,wx.NewId(),%s)\n' %(parent,props)
    if image:
        s+='%s.SetBitmap(%s)\n'%(name,image)
    s+='%s.AppendItem(%s)\n'%(parent,name)
    return s

#--------------------------------------------------------------

#Tabla de managers instalados----------------------------------
gui_managers={
    'tkinter' : { 'template': tkinter_template,
                  'table' : tkinter_table,
                  'class_template' : None,
                  'default_sizer' : 'pack()',
                  'toplevel' : tkinter_process_toplevel_elem,
                  'window' : tkinter_process_window_elem,
                  'appelem' : tkinter_process_app_elem_desc,
                  'bind' : tkinter_process_bind_event,
                  'user' : tkinter_process_user_desc,
                  'menu' : tkinter_process_menu_desc,
                  'menuitem' : tkinter_process_menuitem_desc
                },

    'xhtml' : { 'template': xhtml_template,
                  'table' : xhtml_table,
                  'class_template' : None,
                  'default_sizer' : '',
                  'toplevel' : xhtml_process_toplevel_elem,
                  'window' : xhtml_process_window_elem,
                  'appelem' : xhtml_process_app_elem_desc,
                  'bind' : xhtml_process_bind_event,
                  'user' : xhtml_process_user_desc,
                  'menu' : xhtml_process_menu_desc,
                  'menuitem' : xhtml_process_menuitem_desc
                },

    'wx' :    { 'template': wx_template,
                  'table' : wx_table,
                  'class_template' : None,
                  'default_sizer' : '',
                  'toplevel' : wx_process_toplevel_elem,
                  'window' : wx_process_window_elem,
                  'notebook' : wx_process_notebook_elem,
                  'appelem' : wx_process_app_elem_desc,
                  'bind' : wx_process_bind_event,
                  'user' : wx_process_user_desc,
                  'menu' : wx_process_menu_desc,
                  'menuitem' : wx_process_menuitem_desc
                }
}


#Esto para que no molesten los warnings------------------------
if not 'warnings' in sys.modules:
    warnings=__import__('warnings')
else:
    warnings=sys.modules['warnings']
sys.modules['warnings'].filterwarnings('ignore')
#--------------------------------------------------------------

# Get the token map from the lexer.  This is required.
tokens=gui_lexer.tokens

def p_guiapp(t): 
    '''guiapp : def_list precode initcode VIEW ID FOR ID COLON toplevel_list app_elems_list END'''
    global codestring,supportstring,initstring,tkinter_template,py_globals,fname,namespace,gui_managers,target_gui,xhtml_globals,headerstring
    t[0]=t[9] + t[10]
    appname=t[5]
    if '-h' in sys.argv:
        headerstring=open(sys.argv[sys.argv.index('-h')+1],'r').read()
    if target_gui!='xhtml':
        codestring=t[0]
    else:
        codestring=''
        for item in xhtml_globals:
            s=xhtml_globals[item]['template']%'\n'.join(xhtml_globals[item]['parts'])
            codestring+=s
    template=gui_managers[target_gui]['template']
    template=template.replace('%%HEADER_CODE%%',headerstring)
    template=template.replace('%%SUPPORT_CODE%%',supportstring)
    template=template.replace('%%GUI_CODE%%',codestring)
    if target_gui=='wx':
        initstring= [x for x in initstring.split("\n")]
    else:
        initstring= ["    " + x for x in initstring.split("\n")]
    template=template.replace('%%INIT_CODE%%',"\n".join(initstring))
    template=template.replace('%%GLOBALVARS%%',",".join(py_globals))
    #reemplazar las ocurrencias de las claves de namespace por sus valores
    for item in namespace:
        template=template.replace(item,namespace[item])
    if '-p' in sys.argv:
        print template
    if target_gui=='xhtml':
        fname= appname + '.html'
    else:
        fname=appname + '.py'
    if '-o' in sys.argv:
        fname=sys.argv[sys.argv.index('-o')+1]
    #-------------------------------------------------------------------------------------------------
    #CAMBIO: procesamos code para coger todos los "from __future__ import ..." y ponerlos al principio
    #o si no dan error.
    #--------------------------------------------------------------------------------
    futures= re.findall("from\s+__future__\s+.+",template)
    for item in futures:
        template= re.sub(item,"",template)
    template= '\n'.join(futures) + template
    #---------------------------------------------------------------------------------------------------
    f=open(fname,"w")
    f.write(template)
    f.close()
    t[0]=template
    #print 'lexer en uso: %s' %t.lexer


def p_precode(t):
    '''precode : CONTROLLER VERBATIM
       | CONTROLLER IMPORT idlist
       | CONTROLLER INCLUDE STRING
       | CONTROLLER BRIDGE STRING
       | CONTROLLER BRIDGE VERBATIM'''
    global supportstring,miniparser
    t[0]=''
    if t[2]=='import':
        supportstring=t[2] + ' ' + t[3] + '\n'
    elif t[2]=='include':
        supportstring=open(t[3].strip('"')).read() + '\n'
    elif t[2]=='bridge':
        if t[3][0] in ['"',"'"]:
            code=open(t[3].strip('"')).read()
        else:
            code=t[3].strip('{').strip('}')
        #supportstring=bridge.preprocess(code)
        code=bridge.preprocess(code)
        bridge.__program=code
        bridge.__reflected=0
        #code=bridge.preprocess(code)
        code=code.strip()
        #print 'CODE: %s' % repr(code)
        if code not in [None,'']:
            supportstring=miniparser.parse(code,lexer=stlex2.lexer)
        else:
            supportstring=''
        #print 'SUPPORTSTRING al final: %s' % supportstring
    else:
        supportstring=t[2].strip('{').strip('}') + '\n'



def p_initcode(t): 
    '''initcode : INIT VERBATIM
       | INIT IMPORT ID
       | INIT INCLUDE STRING
       | INIT BRIDGE VERBATIM
       | INIT BRIDGE STRING'''
    global initstring
    #initstring=t[2].strip('{').strip('}') + '\n'
    t[0]=''
    if t[2]=='import':
        initstring=t[2] + t[3] + '\n'
    elif t[2]=='include':
        initstring=open(t[3].strip('"')).read() + '\n'
    elif t[2]=='bridge':
        if t[3][0] in ['"',"'"]:
            code=open(t[3].strip('"')).read()
        else:
            code=t[3].strip('{').strip('}')
        initstring=bridge.preprocess(code)
        bridge.__program=code
        bridge.__reflected=1 #no reimportar nada
        initstring=miniparser.parse(code,lexer=stlex2.lexer)
    else:
        initstring=t[2].strip('{').strip('}') + '\n'


def p_def_list(t):
    '''def_list : pair2 SEMI 
    | pair2 SEMI def_list 
    | empty'''
    global namespace
    if len(t)==3:
        t[0]=t[1] + t[2] + '\n'
    parts=t[1] .strip().split('=')
    if len(parts)>1:
        namespace[parts[0]]='='.join(parts[1:])
    #print 'namespace: %s' % namespace


def p_toplevel_list(t):
    '''toplevel_list : toplevel_elem 
    | toplevel_elem toplevel_list'''
    if len(t)==3:
        t[0]=t[1] + t[2]
    else:
        t[0]=t[1]
    #print 't[0] en toplevellist: %s'%t[0]


def p_toplevel_elem(t): 
    '''toplevel_elem : top_item ID opt_stack opt_props SEMI'''
    global target_gui,gui_managers
    if t[1]=='window':
        #t[0]=tkinter_process_window_elem(t[2],t[3])
        t[0]=gui_managers[target_gui]['window'](t[2],t[3],t[4])
    elif t[1]=='form': #???????
        #t[0]=tkinter_process_window_elem(t[2],t[3])
        t[0]=gui_managers[target_gui]['window'](t[2],t[3],t[4])
    elif t[1]=='notebook': #???????
        #t[0]=tkinter_process_window_elem(t[2],t[3])
        t[0]=gui_managers[target_gui]['notebook'](t[2],t[3],t[4])
    else:
        #t[0]=tkinter_process_toplevel_elem(t[2],t[3])
        t[0]=gui_managers[target_gui]['toplevel'](t[2],t[3],t[4])
    #print 't[0] en toplevel_elem: %s' %t[0]


def p_top_item(t): 
    '''top_item : WINDOW
    | FORM
    | TOPLEVEL
    | NOTEBOOK'''
    t[0]=t[1]
    #print 't[0] en top_item: %s' %t[0]


def p_opt_props(t): 
    '''opt_props : WITH widget_props
    | empty'''
    if len(t)==3:
        t[0]=t[2]
    else:
        t[0]=t[1]
    #print 't[0] en opt_props: %s' %t[0]

def p_app_elems_list(t): 
    '''app_elems_list : app_elem_desc 
    | app_elem_desc app_elems_list'''
    if len(t)==3:
        t[0]=t[1] + t[2]
    else:
        t[0]=t[1]
    #print 't[0] en app_elems_list: %s' %t[0]


def p_app_elem_desc(t): 
    '''app_elem_desc : app_widget ID FOR parent opt_stack WITH widget_props SEMI
      | USER idlist ID FOR parent opt_stack WITH widget_props SEMI
      | BIND fname TO widget_name evt_name SEMI
      | MENU ID FOR parent WITH widget_props opt_top SEMI
      | MENUITEM ID FOR parent WITH widget_props SEMI'''
    if len(t)==10:
        t[0]=gui_managers[target_gui]['user'](t[2] ,t[3] ,t[5] ,t[8],t[6]) 
    elif len(t)==9 and t[1]!='menu':
        t[0]=gui_managers[target_gui]['appelem'](t[1] ,t[2] ,t[4] ,t[7],t[5]) 
    elif len(t)==9:
        t[0]=gui_managers[target_gui]['menu'](t[1],t[2],t[4],t[6],t[7]) 
    elif len(t)==8:
        t[0]=gui_managers[target_gui]['menuitem'](t[1],t[2],t[4],t[6]) 
    else:
        t[0]=gui_managers[target_gui]['bind'](t[4] ,t[2] ,t[5]) 
    #print 't[0] en app_elem_desc: %s' %t[0]


def p_parent(t):
    '''parent : ID
    | NOTHING'''
    t[0]=t[1]


def p_opt_stack(t): 
    '''opt_stack : STACK st_kind 
    | empty'''
    global gui_managers
    if len(t)==3:
        t[0]=t[2]
    else:
        t[0]=gui_managers[target_gui]['default_sizer']   


def p_st_kind(t): #Controla los sizers: stack clase
    '''st_kind : ID stack_props'''
    global target_gui
    if target_gui=='wx': #ESTO es un parche chapuza. hay que revisarlo
        t[0]=t[1] + '$' + t[2]
    else:
        t[0]=t[1] + '(%s)'%t[2]
    #print 't[0] en st_kind:%s' % t[0]


def p_stack_props(t): 
    '''stack_props : pair_list
    | empty'''
    t[0]=t[1]


def p_empty(t): 
    '''empty : '''
    t[0]=''

def p_opt_top(t): 
    '''opt_top : TOPMENU 
    | empty'''
    t[0]=t[1]  

def p_fname(t): 
    '''fname : idlist
       | AID'''
    t[0]=t[1]

    
def p_widget_name(t): 
    '''widget_name : ID
       | AID'''
    t[0]=t[1]

    
def p_evt_name(t): 
    '''evt_name : idlist
    | AID
    | STRING'''
    t[0]=t[1]

        
def p_app_widget(t): 
    '''app_widget : FRAME 
    | PANEL 
    | BUTTON 
    | LABEL
    | TEXTBOX
    | TEXTAREA 
    | COMBOBOX 
    | LISTBOX 
    | TABLEBOX 
    | TREEBOX
    | CHECKBOX
    | FONT
    | MENU
    | RADIO
    | ID'''
    t[0]=t[1]
    #print 't[0] en app_widget: %s' %t[0]

    
def p_widget_props(t): 
    '''widget_props : pair_list
    | NOTHING'''
    if t[1]=='nothing':
        t[0]=''
    else:
        t[0]=t[1]

def p_pair_list(t): 
    '''pair_list : pair 
    | pair COMMA pair_list'''
    if len(t)==4:
        t[0]=t[1] + t[2] + t[3]
    else:
        t[0]=t[1]

    
def p_pair(t): 
    '''pair : idlist EQUAL value
    | KEY EQUAL value
    | value'''
    if len(t)==2:
        t[0]=t[1]
    else:
        if t[1][0]=='@' and t[1][-1]=='@':
            t[1]=t[1] .strip('@')
        t[0]=t[1] + t[2] + t[3]


def p_pair2(t): 
    '''pair2 : AID EQUAL value
    | AID EQUAL list
    | AID EQUAL item_list'''
    t[0]=t[1] + t[2] + t[3]

def p_list(t):
    ''' list : LBRACK item_list RBRACK
    | LBRACK RBRACK'''
    if len(t)==4:
        t[0]=t[1] + t[2] + t[3]
    else:
        t[0]=t[1] + t[2]



def p_item_list(t):
    '''item_list : item COMMA item_list
    | item'''
    if len(t)==4:
        t[0]=t[1] + t[2] + t[3]
    else:
        t[0]=t[1]



def p_item(t):
    '''item :  NUMBER 
    | STRING 
    | idor
    | list'''
    t[0]=t[1]

    
def p_value(t): 
    '''value : NUMBER 
    | STRING 
    | idor
    | AID'''
    t[0]=t[1]


def p_idlist(t): 
    '''idlist : ID
    | ID DOT idlist '''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2] +t[3]

def p_idor(t): 
    '''idor : idlist
    | idlist PIPE idor '''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2] +t[3]



def p_error(t):
    global program
    if t!=None:
        print '\nError de sintaxis (token no permitido) evaluando token "%s" en:\n'%t.value if hasattr(t,"value") else str(t)
        print " ==> %s,...,etc.\n" %program[t.lexpos:t.lexpos + 75]
        print 'en la linea %s\n' %(t.lexer.lineno)
    else:
        print '\nError inesperado: t es None'
    raise Exception(">>> Gui parser: Programa terminado con errores.")                                                                



def parserFactory():
    #Cuando se usa tabmodule, si se hacen cambios, hay que anularlo y luego renombrar parsetab.py
    #Si hay mas de un parser, es necesario especificar el lexer PARA CADA UNO o si no, usa el ultimo y alguno de los dos peta!!!!
    if 'java' in sys.platform: #Version de ply:2.5, superiores no van con jython
        return yacc.yacc(debug=1)#,write_tables=False)#Poner a debug=0 en produccion
    else:
        return yacc.yacc(debug=1,tabmodule='gui_parsetab',write_tables=False)#Poner a debug=0 en produccion

parser=parserFactory()


if __name__=='__main__':
    if len(sys.argv)>1:
        program=open(sys.argv[1]).read()
        if not '-t' in sys.argv: #gui objetivo
            raise Exception('Error: No se ha especificado libreria gui objetivo con -t')
        else:
            target_gui=sys.argv[sys.argv.index('-t')+1]
            if target_gui not in guis: raise Exception('Error: "%s" no es una de las guis soportadas'%target_gui)
        while '-i' in sys.argv: #extra files
            i=sys.argv.index('-i')
            extra_files.append(sys.argv[i+1])
            del sys.argv[i]
            del sys.argv[i]
        if '-d' in sys.argv: #dir de salida para ejecutables
            i=sys.argv.index('-d')
            outputdir=sys.argv[i+1]
        #print 'parser del gui_parser:%s' % parser
        code=parser.parse(program,tracking=True,lexer=gui_lexer.guilexer)
        if '-o' in sys.argv: #archivo de salida (se permite un directorio de salida tambien)
            if outputdir!='.':
                os.makedirs(outputdir)
                #outputfile=sys.argv[sys.argv.index('-o')+1]
            outputfile=sys.argv[sys.argv.index('-o')+1]
            f=open(outputfile,'w')
            f.write(code)
            f.close()
        if '-k' in sys.argv: #tipo de ejcutable a generar(console,windows)
            i=sys.argv.index('-k')
            exe_type=sys.argv[i+1]
        if '-e' in sys.argv:
            #generateExe()
            exegen.generateExe(outputfile,outputdir=outputdir,exe_type=exe_type,
                               extra_files=extra_files,
                               dependencies=__dependencies,description='GUI Parser generated program')
        if '-r' in sys.argv: #ejecutar
            if 'darwin' in sys.platform:
                os.system("python " + fname) #Esto es mas seguro.
            else:
                if target_gui=='xhtml':
                    os.system('explorer ' + fname) #Solo win32
                else:
                    exec code #esto falla al menos en Mac!!!

