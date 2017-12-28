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
    name=generateClassName()
    print 'nuevo nombre de clase: %s' %name
    #Crear un dialogo y mostrarlo
    tplfact=DialogTemplateFactory(name,'Dialogo emergente!!',xf=300,yf=300,ftname='Arial')
    dlg2=tplfact.getDialogTemplate()
    w2=MiniDialog(name,dlg2)#,icon=os.getcwd() + '\\nut.ico')
    w2.registerEvent('self','rclick',frclick)
    w2.registerEvent('self','click',fclick)
    #w2.addImage('img1',os.getcwd() + '\\img1.bmp',0,0,500,550)
    hcontrol=form.getControl('check1')
    b1=Button('check1',hcontrol,form)
    hfont=fontFactory('Arial',14)
    b1.setFont(hfont)
    b1.setBgMode(0)
    b1.setTextColor(hex2colorref('0xff0000'))
    b1.setTextBgColor(hex2colorref('0x00ff00'))
    b1.setBgColor(hex2colorref('0xffffff'))
    hcontrol=form.getControl('button2')
    b2=Button('button2',hcontrol,form)
    hfont=fontFactory('Comic Sans MS',15)    
    b2.setFont(hfont)
    if b2.isEnabled():
        b2.disable()
    else:
        b2.enable()
    hcontrol=form.getControl('label1')
    st=StaticText('label1',hcontrol,form)
    hfont=fontFactory('Trebuchet MS',12)   
    st.setFont(hfont)
    #Para ver el color de fondo del texto hay que poner bgmode a 0
    st.setBgMode(0)    
    bgcol=hex2colorref('0x00ff00')
    st.setBgColor(bgcol)
    txbgcol=hex2colorref('0x000000')
    st.setTextBgColor(txbgcol)    
    if st.isEnabled():
        st.disable()
    else:
        st.enable()
    #Cambiar de color el fondo del formulario
    #form.setBgColor(hex2colorref('ffac00'))
    #form.setBgColor(-1)
    hfont=fontFactory('Comic Sans MS',12)
    form.setFont(hfont)
    #form.setTextColor(hex2colorref('ffac00'))
    form.setTitle('Funciona!!!')
    print st.getFont()
    print st.getBgMode()
    print st.getBgColor()
    print st.getTextColor()
    if form.isDraggable():
        form.setDraggable(0)
        form.acceptDropFiles(0)
    else:
        form.setDraggable(1)
        form.acceptDropFiles(1)
    form.setBgMode(0)
    form.setAlpha(200)
    ###--------------------------------------------------------------------------
    ##Si se pasa un color de fondo, la transparencia lo usa.
    ##Si se pasa -1 como color de fondo, el fondo es transparente por completo
    ###--------------------------------------------------------------------------
    form.setBgColor(hex2colorref('ffacfc'))
    #classId, windowName , style , rect , parent , id , obPersist , bStorage , licKey )
    
    #form.moveControl(form.getControl('button3'),100,100,70,20)
    w2.DoModal(form.hwnd)


def button4Click(form,*args):
    #Prueba del dialogo de seleccion de color
    cold=ColorsDialog()
    cold.setCustomColors(4210816,15387874)
    cold.show()
    print 'COLOR ELEGIDO:%s' %cold.getColor()
    print 'Colores personalizados: %s' %str(cold.getCustomColors())
    #Prueba del dialogo de seleccion de fuente
    fontd=FontsDialog()
    fontd.show()
    print fontd.getFontName()
    print fontd.getFontSize()
    print fontd.getFontColor()
    print fontd.isBold()
    print fontd.isItalic()
    print fontd.isUnderline()
    print fontd.isStrikeOut()
    



def button2Click(form,*args):
    print 'Se ha pulsado el boton 1 y se ha disparado el evento click!!'
    #Crear un dialogo y mostrarlo
    #form.moveWindow(500,0,form.getWidth(),form.getHeight())
    form.center()
    #Cambiar el color de fondo del otro boton
    hcontrol=form.getControl('button2')
    b2=Button('button2',hcontrol,form)
    form.changeStyle('WS_CHILD|WS_VISIBLE',1)
    #b2.setBgColor(255,0,0)


def button3Click(form,*args):
    print 'Se ha pulsado el boton 3 y nos vamos!!'
    form.destroy()

def initApp(form,*args):
    hcontrol=form.getControl('textbox1')
    t1=TextBox('textbox1',hcontrol,form)
    t1.setText('En un lugar de La Mancha, de cuyo nombre no quiero acordarme...')
    txbgcolor=hex2colorref('0x00ff00')
    t1.setTextBgColor(txbgcolor)
    txcolor=hex2colorref('0xff0000')
    bgcolor=hex2colorref('0x0000ff')
    hfont=fontFactory('Trebuchet MS',12)
    t1.setFont(hfont)
    t1.setTextColor(txcolor)
    t1.setBgColor(bgcolor)
    print 'CODIGO DE INICIALIZACION !!\n\n'


def DemoCreateWindow():
    winst=winStyleMaker('WS_THICKFRAME|WS_CAPTION') #WS_SIZEBOX Sin borde y sin botones
    tplfact=DialogTemplateFactory('NombreDeLaClase','Titulo del dialogo en la ventana2',xf=300,yf=300,ftname='Courier New',style=winst)
    dlg=tplfact.getDialogTemplate()
    
    wf=WidgetsFactory()
    hfont=fontFactory('Trebuchet',18)
    stcolor=hex2colorref('0x0000ff')
    txcolor=hex2colorref('0xff0000')
    txbgcolor=hex2colorref('0x00ff00')
    bgmode=0
    
    w=MiniWindow('NombreDeLaClase',dlg) #,icon=os.getcwd() + '\\icono.ico')
    control=wf.createButton('button1',200,45,70,20,'Dialogo','center',1)
    dlg.append(control)
    control=wf.createButton('button2',100,45,70,20,'Mover ventana','center',0)
    dlg.append(control)
    control=wf.createButton('button3',100,65,70,20,'Cerrar','center',0)
    dlg.append(control)
    control=wf.createButton('button4',100,160,70,20,'CommDlgs','center',0)
    dlg.append(control)    
    control=wf.createLabel('label1','\n\nEtiquetilla!!\n',100,95,200,50,'center',hfont,stcolor,txcolor,txbgcolor,bgmode)
    dlg.append(control)
    control=wf.createCheckBox('check1',200,165,180,20,'Soy un checkbox, oyes!!')
    dlg.append(control)
    control=wf.createTextBox('textbox1',200,185,150,50,'Texto interior',align='left')
    dlg.append(control)
    control=wf.createStatusBar('status1',200,185,150,50)
    dlg.append(control)        
    w.registerEvent('self','rclick',frclick)
    w.registerEvent('self','click',fclick)
    w.registerEvent('button1','command',button1Click)
    w.registerEvent('button2','command',button2Click)
    w.registerEvent('button3','command',button3Click)
    w.registerEvent('button4','command',button4Click)
    w.registerEvent('self','init',initApp)
    #w.addImage('img1',os.getcwd() + '\\img1.bmp',0,150,100,100)
    w.CreateWindow()

    # PumpMessages runs until PostQuitMessage() is called by someone.
    win32gui.PumpMessages()

DemoCreateWindow()    