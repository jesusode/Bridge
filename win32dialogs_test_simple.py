from win32_dialogs_framework import *
from win32commdlgs import *
from win32gui_utils import *
#import random
import win32ui

###PRUEBAS

def fclick(form,*args):
    print 'SE HA HECHO CLICK EN EL FORMULARIO!!'

def frclick(form,*args):
    print 'SE HA HECHO CLICK DERECHO EN EL FORMULARIO!!'
    menuf=MenuFactory()
    #[name,callback,type,text,submenu,image]
    menulist=[['pop1',menucallb1,'','Popup menu item 1',0,''],['pop2',menucallb1,'','Popup menu item 2',0,''],['pop3',menucallb1,'','Popup menu item 3',0,'']]
    popmenu=menuf.createPopupMenu('popup',menulist)
    form.showPopupMenu(popmenu)

def menucallb1(msg='sin argumentos',*args):
    print 'Llamada a la funcion del menu %s' %msg


def button1Click(form,*args):
    print 'Se ha pulsado el boton 1 y se ha disparado el evento click!!'

def initApp(form,*args):
    print 'CODIGO DE INICIALIZACION!!!\n\n'


def DemoCreateWindow():
    winst=winStyleMaker('WS_THICKFRAME|WS_CAPTION|WS_SYSMENU') #WS_SIZEBOX Sin borde y sin botones
    tplfact=DialogTemplateFactory('NombreDeLaClase','Titulo del dialogo en la ventana2',xf=300,yf=300,ftname='Courier New',style=winst)
    dlg=tplfact.getDialogTemplate()
    
    wf=WidgetsFactory()
    hfont=fontFactory('Trebuchet',18)
    stcolor=hex2colorref('0x0000ff')
    txcolor=hex2colorref('0xff0000')
    txbgcolor=hex2colorref('0x00ff00')
    bgmode=0
    
    w=MiniWindow('NombreDeLaClase',dlg,icon=os.getcwd() + '\\icono.ico')
    control=wf.createButton('button1',200,45,70,20,'Dialogo','center',1)
    dlg.append(control)
    
    w.registerEvent('self','rclick',frclick)
    w.registerEvent('self','click',fclick)
    w.registerEvent('button1','command',button1Click)
 
    w.registerEvent('self','init',initApp)
    w.CreateWindow()

    # PumpMessages runs until PostQuitMessage() is called by someone.
    win32gui.PumpMessages()

#DemoCreateWindow()    