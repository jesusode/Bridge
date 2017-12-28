from win32_dialogs_framework import *

###PRUEBAS

def fclick(form,*args):
    print 'SE HA HECHO CLICK EN EL FORMULARIO!!'
    hcontrol=form.getControl('listview1')
    lv=ListView('listview1',hcontrol,form)
    x,y = win32gui.GetCursorPos()
    print 'El formulario contiene el punto (%d,%d): %d' % (x,y,lv.hasPoint(x,y))

def frclick(form,*args):
    print 'SE HA HECHO CLICK DERECHO EN EL FORMULARIO!!'
    menuf=MenuFactory()
    #[name,callback,type,text,submenu,image]
    menulist=[['pop1',menucallb1,'','Popup menu item 1',0,''],['pop2',menucallb1,'','Popup menu item 2',0,''],['pop3',menucallb1,'','Popup menu item 3',0,'']]
    popmenu=menuf.createPopupMenu('popup',menulist)
    form.showPopupMenu(popmenu)

def flvrclick(form,*args):
    print 'SE HA HECHO CLICK DERECHO EN EL listview!!'
    menuf=MenuFactory()
    #[name,callback,type,text,submenu,image]
    menulist=[['lvpop1',menucallb1,'','LV Popup menu item 1',0,''],['lvpop2',menucallb1,'','LV Popup menu item 2',0,''],['lvpop3',menucallb1,'','LV Popup menu item 3',0,'']]
    popmenu=menuf.createPopupMenu('lvpopup',menulist)
    form.showPopupMenu(popmenu)

def menucallb1(msg='sin argumentos',*args):
    print 'Llamada a la funcion del menu %s' %msg

def button1Click(form,*args):
    print 'Se ha pulsado el boton 1 y se ha disparado el evento click!!'
    hcontrol=form.getControl('textbox1')
    numlines=win32gui.SendMessage(hcontrol,win32con.EM_GETLINECOUNT,0,0)
    print 'Lineas del cuadro de texto: %d' % numlines
    text=''
    buf='' 
    for i in range(numlines):
        print 'procesando linea %d' %i
        #Obtener longitud de la linea para ajustar el buffer
        linelen=win32gui.SendMessage(hcontrol,win32con.EM_LINELENGTH,i,0)
        print linelen
        buf='x' * linelen
        win32gui.SendMessage(hcontrol,win32con.EM_GETLINE,i,buf)
        print buf
        text+=buf.strip('x')
        print text
    print 'Contenido del cuadro de texto: %s' %text
    text2=win32gui.GetWindowText(hcontrol)
    print 'Contenido via GetWindowText(): %s' %text2
    #Poner unas cadenas en la lista
    hcontrol=form.getControl('list1')
    lb=ListBox('list1',hcontrol,form)
    #SendMessage(hcontrol,win32con.LB_ADDSTRING,0,'Cadenita')
    lb.addString('Cadenita')
    lb.addStringList(['uno','dos','tres','cuatro'])
    lb.setCurSel(3)
    print 'El item 3 es: %s' % lb.getItemText(3)
    hcontrol=form.getControl('combo1')
    cb=ComboBox('combo1',hcontrol,form)
    cb.addString('Cadenita')
    cb.addStringList(['uno','dos','tres','cuatro'])
    cb.setCurSel(3)
    print 'Numero de elementos del combo: %s' %cb.getNumEls()
    #Barra de progreso
    hcontrol=form.getControl('prog1')
    pb=ProgressBar('prog1',hcontrol,form)
    pb.setRange(0,100)
    pb.stepIt()
    #Cambiar el texto del static box y del boton2
    hcontrol=form.getControl('label1')
    stat=StaticText('label1',hcontrol,form)
    stat.setText("En un lugar de la mancha...")
    print 'El item 3 del combo es: %s' % cb.getItemText(3)
    #SetWindowText(hcontrol,"En un lugar de la mancha...")
    hcontrol=form.getControl('button2')
    b2=Button('button2',hcontrol,form)
    s=b2.getText()
    b2.click()
    print 'Label del button2: %s' % s
    win32gui.SetWindowText(hcontrol,"Nuevo texto")
    hcontrol=form.getControl('check1')
    ch=CheckBox('check1',hcontrol,form)
    ch.setText('Nuevo texto!')
    ch.setChecked(1)
    hcontrol=form.getControl('listview1')
    lv=ListView('listview1',hcontrol,form)
    lv.insertColumnList(['col1','col2','col3','col4','col5'],80,'center')
    for i in range(10):
        lv.addItem(['uno','dos','tres','cuatro','cinco'])
    lv.addItems([['cinco','cinco','cinco','cinco','cinco'],['seis','seis','seis','seis','seis'],['siete','siete','siete','siete','siete',]])
    print lv.getCell(1,1) #Dos!!
    print lv.getCellWidth(1,1)
    lv.addImageList()
    print lv.getCells()
    print len(lv.getCells())
    print lv.getRowCount()
    print lv.getColCount()
    print lv.getHeaderCell(1)
    print lv.getHeaderCellWidth(1)
    print lv.getHeaderCells()
    print lv.getSelectedCount()
    lv.selectRow(1)
    print lv.getSelectedCount()
    lv.checkRow(5)
    print lv.cells2matrix().toString()
    print lv.getBgColor()
    lv.setBgColor(0,0,255)
    print lv.getBgColor()
    print lv.getTextColor()
    lv.setTextColor(0,255,0)
    print lv.getTextColor()
    print lv.getTextBgColor()
    lv.setTextColor(255,0,0)
    print lv.getTextBgColor()        
    #lv.disable()
    print lv.isEnabled()
    lv.setCell(0,1,'capullo')
    #win32gui.FlashWindow(form.hwnd,True)
    #lv.editLabel(1)
    print lv.getRect()
    print lv.getWidth()
    print lv.getHeight()    
    

def DemoModal():
    w=MiniDialog('Titulo del dialogo')
    w.DoModal()


def DemoCreateWindow():
    tplfact=DialogTemplateFactory('NombreDeLaClase','Titulo del dialogo en la ventana2',xf=600,yf=200,ftname='Courier New')
    dlg=tplfact.getDialogTemplate()
    #Cada control se crea usando la calse factory auxiliar
    wf=WidgetsFactory()
    control=wf.createLabel('label1','Hola capullo',200,55,70,20,'right')
    dlg.append(control)
    control=wf.createTextBox('textbox1',200,75,150,50,'Texto interior',align='right')
    dlg.append(control)
    control=wf.createButton('button1',200,145,70,20,'Pulsame, jooo!','center',1)
    dlg.append(control)
    control=wf.createButton('button2',320,145,70,20,'Soy el otro')
    dlg.append(control)
    control=wf.createCheckBox('check1',200,165,70,20,'Soy un checkbox, oyes!!')
    dlg.append(control)
    control=wf.createListBox('list1',120,100,70,80)
    dlg.append(control)
    control=wf.createComboBox('combo1',100,30,70,80)
    dlg.append(control)
    control=wf.createRichTextBox('rich1',20,30,70,80)
    dlg.append(control)
    control=wf.createSlider('slider1',180,30,100,20)
    dlg.append(control)
    control=wf.createSpinControl('spin1',180,10,100,20)
    dlg.append(control)
    control=wf.createListView('listview1',280,10,350,60,'report')
    dlg.append(control)
    control=wf.createTreeView('treeview1',120,200,200,60)
    dlg.append(control)
    control=wf.createDateTimePicker('date1',20,130,80,12)
    dlg.append(control)
    control=wf.createMonthCalendar('cal1',10,170,120,80)
    dlg.append(control)
    control=wf.createProgressBar('prog1',250,180,120,10)
    dlg.append(control)
    control=wf.createFrameBox('frame1',350,190,130,100,'Framebox')
    dlg.append(control)     
    #control=wf.createTabControl('tab1',0,0,800,600)
    #dlg.append(control)           



    #Crear un menu con la clase factory
    menuf=MenuFactory() #['Menu uno','Menu dos'])
    #[name,callback,type,text,submenu,image]
    menulist3=[['m7',menucallb1,'','Submenu_lateral item 1',0,''],['m8',menucallb1,'','Submenu_lateral item 2',0,''],['m9',menucallb1,'','Submenu_lateral item 3',0,'']]
    menuf.createMenu('sub21',menulist3)        
    menulist1=[['m1',menucallb1,'','Submenu1 item 1',menuf.getMenu('sub21'),''],['m2',menucallb1,'','Submenu1 item 2',0,''],['m',menucallb1,'-','Submenu1 item 3',0,''],['m3',menucallb1,'','Submenu1 item 3',0,'']]
    menuf.createMenu('sub1',menulist1)
    print os.getcwd() + '\\smiley.bmp'
    menulist2=[['m4',menucallb1,'','Submenu2 item 1',0,os.getcwd() + '\\nut.bmp'],['m5',menucallb1,'','Submenu2 item 2',0,os.getcwd() + '\\link.bmp'],['m6',menucallb1,'','Submenu2 item 3',0,os.getcwd() + '\\smiley.bmp']]
    menuf.createMenu('sub2',menulist2)

    menubaritems=[['arch',None,'','Archivo',menuf.getMenu('sub1'),''],['edit',None,'','Edicion',menuf.getMenu('sub2'),os.getcwd() + '\\link.bmp']]
    menu=menuf.createMenuBar(menubaritems) #[0]

    
    w=MiniWindow('NombreDeLaClase',dlg,menu,os.getcwd() + '\\icono.ico')
    w.registerEvent('button1','command',button1Click)
    w.registerEvent('self','rclick',frclick)
    w.registerEvent('self','click',fclick)
    w.registerEvent('listview','rclick',flvrclick)
    w.registerEvent('listview','click',flvrclick)
    w.registerEvent('list1','rclick',flvrclick)
    w.addImage('img1',os.getcwd() + '\\img1.bmp',700,300,100,100)
    print dlg
    w.CreateWindow()

    win32gui.PumpMessages()

DemoCreateWindow()    