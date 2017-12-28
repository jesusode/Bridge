# Hacked from the win32gui demo ;)
import sys
if "--noxp" in sys.argv:
    import win32gui
else:
    import winxpgui as win32gui
import win32api
import win32con
import struct, array
import commctrl
import os
import random

from win32gui_utils import *
#from _globals import *
from win32_aux_structs import *
from win32com.client import gencache
from pywin.mfc import activex

from win32commdlgs import *
import pywintypes
import ctypes

#Intento de crear controles activeX---
#from activexwrapper_MODIFIED import *
#-------------------------------------

#Importar el control webbrowser ??
#from webctrl import *

#Tabla de modos de imagen
IMAGE_MODES={
    'copy':win32con.SRCCOPY,
    'and': win32con.SRCAND,
    'paint': win32con.SRCPAINT,
    'invert': win32con.SRCINVERT,
    'erase': win32con.SRCERASE
    }


#Funcion de utilidad para generar nombres de clase de ventana
def generateClassName(size=7):
    letters=list('abcdefghijklmnopqrstuvwxyz1234567890')
    name='WND_CLASS_'
    for i in range(size):
        name+=random.choice(letters)
    return name


##WebBrowserModule = gencache.EnsureModule("{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}", 0, 1, 1)
##if WebBrowserModule is None:
##  raise ImportError, "IE4 does not appear to be installed."
##
##class MyWebBrowser(activex.Control, WebBrowserModule.WebBrowser):
##  pass
#  def OnBeforeNavigate2(self, pDisp, URL, Flags, TargetFrameName, PostData, Headers, Cancel):
#    self.GetParent().OnNavigate(URL)



class MiniWindowBase:
    def __init__(self,className,win_template=[],menu=None,icon=None):
        win32gui.InitCommonControls()
        # Need to do this go get rich-edit working.
        win32api.LoadLibrary("Riched20.dll")
        
        self.hinst = win32gui.dllhandle
        self.hwnd=None
        self.g_iconPathName=icon
        self.g_registeredClass = 0
        self.dlgClassName=None


        self.iecontrol=None        
        
        self.title='Mini Windows Base'
        self.__className=className
        #Tabla de controles por nombre {nombre_control:idc}
        self.controls = {}
        #Tabla de controles por id {idc:nombre_control}
        self.idcontrols={}
        #Tabla de controles por clase {idc:kind}
        self.kindcontrols={}
        #Tabla de propiedades del control {idc:properties}
        self.controlsprops={}         
        #Tabla de eventos registrados
        self.events={}

        #Propiedades de fondo del dialogo: bgcolor, textcolor, bgmode,font,alpha----
        self.bgcolor=0
        self.textcolor=0
        self.bgmode=0
        self.font=0
        self.alpha=255 #0: transparente, 255: opaco
        #Flag para saber si es transparente (alpha < 255)
        self.transparent=1
        #---------------------------------------------------------------------


        #Flag para saber si tiene barra de estado
        self.__hasStatusBar=0

        #Buffer en memoria para acelerar el repintado
        self.memdc=None


        #Flag para saber si se esta arrastrando el raton
        self.dragging=0

        #Flag para saber si se ha hecho click y no se ha levantado el boton izquierdo
        self.isClicked=0


        #Flag para saber si la ventana se mueve al arrastrar el raton sobre ella
        self.__draggable=0

        #Flag para saber si la ventana acepta arrastrar archivos sobre ella
        self.__canDropFiles=0

        #Lista que contiene los archivos arrastrados, si los hay
        self.__droppedFiles=[]
        
        #Tabla con las imagenes registradas.
        #Cada imagen debe redibujarse en OnPaint.
        #Para cada imagen se define una tupla (filename,xi,yi,w,h,mode,xini=0,yini=0)
        self.images={}

        #Plantilla con los controles y el tipo de ventana a crear
        #win_template es una lista de listas con la estructura: [[name,idc,[control]],...]
        self.win_template=win_template

        #Menu de la ventana si se ha especificado un HMENU
        #Crear menu y registrar sus elementos y funciones
        self.hmenu=None
        if menu!=None:
            #(self.hmenu,self.nameid,self.namecallb)
            self.hmenu=menu[0] #hmenu
            for item in menu[1]:
                self.registerControl(item,menu[1][item],'menuitem')
            for item in menu[2]:
                self.registerEvent(item,'command',menu[2][item])
        
        #Instancia del interprete
        #self.interp=Interprete()



    def getClassName(self):
        return self.__className

    def registerControl(self,name,idc,kind,properties={}):
        #Registra un control para poder usarlo luego por su nombre, su id o su clase
        #print 'Registrando control %s!!' % name
        self.controls[name]=idc
        self.idcontrols[idc]=name
        self.kindcontrols[idc]=kind
        self.controlsprops[idc]=properties

    
    def getControl(self,idorname):
        #Devuelve un hcontrol dado su id o el nombre con el que se ha registrado
        control=0 #Por defecto un hcontrol nulo
        if type(idorname)==type(""): #Nombre
            control=win32gui.GetDlgItem(self.hwnd,self.controls[idorname])
        elif type(idorname)==type('3'): #Idcontrol
            control=win32gui.GetDlgItem(self.hwnd,idorname)
        #print 'HWND CONTROL: %d' %control
        return control


    def getControlProperties(self,idorname):
        #Devuelve el diccionario de propiedades de un control dado su id o el nombre con el que se ha registrado
        props={} 
        if type(idorname)==type(""): #Nombre
            props=self.controlsprops[self.controls[idorname]]
        elif type(idorname)==type('3L'): #Idcontrol
            props=self.controlsprops[idorname]
        #print 'PROPIEDADES DEL CONTROL: %s' %str(props)
        return props


    def addImage(self,name,_file,x,y,w,h,mode='copy',xini=0,yini=0):
        imgprops=[_file,x,y,w,h,mode,xini,yini]
        self.images[name]=imgprops
        #Obligar a que se repinte la ventana si ya se ha creado
        if self.hwnd:
            win32gui.InvalidateRect(self.hwnd,win32gui.GetClientRect(self.hwnd),1)        

    def delImage(self,name):
        if self.images.has_key(name):
            del self.images[name]
            #Obligar a que se repinte la ventana
            if self.hwnd:
                win32gui.InvalidateRect(self.hwnd,win32gui.GetClientRect(self.hwnd),1)
            return 1
        return 0


    def getImage(self,name):
        if self.images.has_key(name):
            return self.images[name]
        return 0


    def setImage(self,name,_file,x,y,w,h,mode='copy',xini=0,yini=0):
        imgprops=[_file,x,y,w,h,mode,xini,yini]
        self.images[name]=imgprops
        #Obligar a que se repinte la ventana si ya se ha creado
        if self.hwnd:
            win32gui.InvalidateRect(self.hwnd,win32gui.GetClientRect(self.hwnd),1)        

    def moveWindow(self,x,y,w,h):
        win32gui.MoveWindow(self.hwnd, x,y, w, h, 1)

    def moveControl(self,hcontrol,x,y,w,h):
        win32gui.MoveWindow(hcontrol, x,y, w, h, 1)

    def createStatusBar(self,numPanes): #Solo puede haber una!!
        pass

    def hasStatusBar(self):
        return self.__hasStatusBar

    def drawImage(self,name):
        '''
        HANDLE LoadImage(
        HINSTANCE hinst, 	// handle of the instance that contains the image
        LPCTSTR lpszName,	// name or identifier of image
        UINT uType,	// type of image
        int cxDesired,	// desired width
        int cyDesired,	// desired height
        UINT fuLoad	// load flags
       );
       '''        
        #Dibujamos segun la api win32:
        if self.images.has_key(name):
            props=self.images[name]
            #1.- Cargar imagen: TIENE QUE SER UN .BMP!!
            hbmp=win32gui.LoadImage(0,props[0],win32con.IMAGE_BITMAP,props[3],props[4],win32con.LR_LOADFROMFILE)
            #2.- Obtener el DC de la ventana
            hdc=win32gui.GetDC(self.hwnd)
            #3.- Crear un DC compatible en memoria
            memdc=win32gui.CreateCompatibleDC(hdc)
            #4.- Seleccionar el bitmap
            win32gui.SelectObject(memdc,hbmp)
            #5.- Copiar el bitmap en el DC de la ventana
            win32gui.BitBlt(hdc,props[1],props[2],props[3],props[4],memdc,props[6],props[7],IMAGE_MODES[props[5]])
            #6.- Borrar contextos de dispositivo
            win32gui.ReleaseDC(self.hwnd,hdc)
            win32gui.DeleteDC(memdc)
            win32gui.DeleteObject(hbmp)
    

    def registerEvent(self,evt_src,evt_name,callback_func):
        #Registra un evento:
        #evt_src: idc del control para el que lo definimos
        #evt_name: nombre del evento (ej: click, mouseout, etc)
        #callb_func_name:
        #Para poder manejar eventos iguales para diferentes controles,
        #las entradas de la tabla son nombre_control|nombre_evento:callback_func
        #print evt_src
        #print evt_name
        #No se puede comprobar que el control exista porque hasta que
        #se llama a _DoCreate no se registran los controles!!
        self.events[evt_src + '|' + evt_name]=callback_func
        #print 'Registrando evento:%s' %str(self.events)


    def dispatchEvents(self,evt_type,idc_src,wparam,lparam,*args):
        #Llama a la funcion definida para cada evento si existe
        #idc = win32api.LOWORD(wparam)
        ###Si el evento se refiere al formulario, se registra con el nombre de 'self'------------------
        if evt_type=='command':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'command'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam) #Hay que pasar una referencia al formulario para que pueda manejarlo el codigo externo
        elif evt_type=='paint': #lo manejamos aqui???
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'paint'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)
        elif evt_type=='startclick':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'startclick'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)                    
        elif evt_type=='click':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'click'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)
        elif evt_type=='startrclick':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'startrclick'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)                    
        elif evt_type=='rclick':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'rclick'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)
        elif evt_type=='dblclick':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'dblclick'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)
        elif evt_type=='rdblclick':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'rdblclick'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)
        elif evt_type=='mousemove':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'mousemove'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)                    
        elif evt_type=='size':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'size'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)
        elif evt_type=='keydown':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'keydown'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)
        elif evt_type=='char':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'char'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)
        elif evt_type=='notify':
            #dispatchEvents(self,evt_type,idc_src,wparam,lparam,*args)
            #self.dispatchEvents('notify',idFrom,code,hwndFrom)
##            print 'Procesando evento notify'
##            print 'idc fuente: %d' %idc_src
##            print 'evt code: %d' %wparam
##            print commctrl.NM_CLICK
            #Proceder segun tipo codigo de evento detectado
            if wparam==commctrl.NM_CLICK:
                print 'Detectado click en algo!!'
            elif wparam==commctrl.NM_CHAR:
                print 'Se ha pulsado un caracter!!'
            elif wparam==commctrl.NM_RCLICK:
                print 'Detectado click derecho en algo!!'
            elif wparam==commctrl.NM_DBLCLK:
                print 'Detectado doble click en algo!!'
            elif wparam==commctrl.NM_RDBLCLK:
                print 'Detectado doble click derecho en algo!!'
            elif wparam==commctrl.NM_SETFOCUS:
                print 'Detectado foco en elgo!!'
            elif wparam==commctrl.NM_KILLFOCUS:
                print 'Detectado perdida de foco en algo!!'
                
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'notify'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)
        elif evt_type=='getfocus':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'getfocus'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)
        elif evt_type=='lostfocus':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'lostfocus'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam)
        elif evt_type=='dropfiles':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'dropfiles'
                if self.events.has_key(evt_name):
                    print 'Detectado arrastre de archivos desde codigo de usuario!!'
                    self.events[evt_name](self,wparam,lparam)

    def showPopupMenu(self, menu):
        #Muestra un menu emergente
        x,y = win32gui.GetCursorPos()
        #Hay que registrar el menu para poder coger sus eventos
        #(self.hmenu,self.nameid,self.namecallb)
        #print menu
        hmenu=menu[0] #hmenu
        for item in menu[1]:
            self.registerControl(item,menu[1][item],'menuitem')
        for item in menu[2]:
            self.registerEvent(item,'command',menu[2][item])
        #print self.controls
        win32gui.TrackPopupMenu(hmenu, win32con.TPM_LEFTALIGN, x, y, 0, self.hwnd, None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

                    

    def _RegisterWndClass(self):
        className = self.__className
        if not self.g_registeredClass:
            message_map = {}
            wc = win32gui.WNDCLASS()
            wc.SetDialogProc() # Make it a dialog class.
            wc.hInstance = self.hinst
            wc.lpszClassName = className
            wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
            wc.hCursor = win32gui.LoadCursor( 0, win32con.IDC_ARROW )
            wc.hbrBackground = win32con.COLOR_WINDOW + 1
            wc.lpfnWndProc = message_map # could also specify a wndproc.
            # C code: wc.cbWndExtra = DLGWINDOWEXTRA + sizeof(HBRUSH) + (sizeof(COLORREF));
            wc.cbWndExtra = win32con.DLGWINDOWEXTRA + struct.calcsize("Pi")
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            if self.g_iconPathName:
                wc.hIcon = win32gui.LoadImage(self.hinst, self.g_iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
            classAtom = win32gui.RegisterClass(wc)
            self.g_registeredClass = 1
        return className

    def _GetDialogTemplate(self, dlgClassName):
        #print 'Dentro de GetDlgTemplate!!'
        templ=self.win_template
        dlg=[templ[0]]
        for item in templ[1:]:
            #print item
            name,idc,control,kind,props=item
            self.registerControl(name,idc,kind,props)
            dlg.append(control)
        #print dlg
        #print self.controls
        return dlg

    def _DoCreate(self, fn,parent=0):
        message_map = {
            win32con.WM_SIZE: self.OnSize, #Cambio de tamanyo
            win32con.WM_COMMAND: self.OnCommand, #Mensajes command: todos los controles comunes y los menus
            win32con.WM_INITDIALOG: self.OnInitDialog, #Inicializacion de la ventana
            win32con.WM_CLOSE: self.OnClose, #Cierre de la ventana
            win32con.WM_DESTROY: self.OnDestroy, #Destruccion de la ventana
            win32con.WM_LBUTTONDOWN: self.OnStartClick, #Comienzo click de raton izquierdo
            win32con.WM_LBUTTONUP: self.OnClick, #Fin click de raton izquierdo
            win32con.WM_RBUTTONDOWN: self.OnStartRightClick, #Comienzo click de raton derecho
            win32con.WM_RBUTTONUP: self.OnRightClick, #Fin click de raton derecho
            win32con.WM_LBUTTONDBLCLK: self.OnDblClick, #Doble click izquierdo
            win32con.WM_RBUTTONDBLCLK: self.OnRightDblClick, #Doble click derecho
            win32con.WM_MOUSEMOVE: self.OnMouseMove, #Movimiento del raton
            win32con.WM_PAINT: self.OnPaint, #Eventos Paint
            win32con.WM_CHAR: self.OnChar, #Pulsacion de teclado paratextbox
            win32con.WM_KEYDOWN: self.OnKeyDown, #Respuesta a pulsacion de teclado
            win32con.WM_NOTIFY: self.OnNotify, #Mensajes Notify
            win32con.WM_SETFOCUS: self.OnGetFocus, #Obtencion del foco
            win32con.WM_KILLFOCUS: self.OnLoseFocus, #Perdida del foco
            win32con.WM_TIMER: self.OnTimer, #Evento timer
            win32con.WM_CTLCOLORSTATIC: self.OnStaticColorChange, #Cambio de color para etiquetas
            win32con.WM_CTLCOLORBTN: self.OnButtonColorChange, #Cambio de color para botones
            win32con.WM_CTLCOLOREDIT: self.OnEditColorChange, #Cambio de color para TextBox
            win32con.WM_CTLCOLORLISTBOX: self.OnListBoxColorChange, #Cambio de color para listbox
            win32con.WM_CTLCOLORDLG: self.OnDlgColorChange, #Cambio de color para dialogos
            win32con.WM_CTLCOLORSCROLLBAR: self.OnStaticColorChange, #Cambio de color para scroll bars
            win32con.WM_MOVE: self.OnMove,
            win32con.WM_DROPFILES: self.OnDropFiles
        }
        self.dlgClassName = self._RegisterWndClass()
        template = self._GetDialogTemplate(self.dlgClassName)
        #return fn(self.hinst, template, 0, message_map)
        return fn(self.hinst, template, parent, message_map)


    def setFont(self,hfont): #hfont es una fuente creada con fontFactory()
        #Cambiar el valor de font en las propiedades por el nuevo
        self.font=hfont        
        win32gui.SendMessage(self.hwnd,win32con.WM_SETFONT,hfont,0)
        #Obligar a que se repinte (hay que invalidar toda el area cliente!!)
        win32gui.InvalidateRect(self.hwnd,win32gui.GetClientRect(self.hwnd),1)

    def getFont(self):
        return self.font

    def getBgColor(self):
        return self.bgcolor   

    def setBgColor(self,color):
        #Cambiar el valor de font en las propiedades por el nuevo
        self.bgcolor=color        
        #Obligar a que se repinte (hay que invalidar toda el area cliente!!)
        win32gui.InvalidateRect(self.hwnd,win32gui.GetClientRect(self.hwnd),1)

    def getBgMode(self):
        return self.bgmode

    def setBgMode(self,mode):
        #Cambiar el valor de font en las propiedades por el nuevo
        self.bgmode=mode        
        #Obligar a que se repinte (hay que invalidar toda el area cliente!!)
        win32gui.InvalidateRect(self.hwnd,win32gui.GetClientRect(self.hwnd),1)

    def getTextColor(self):
        return self.textcolor  

    def setTextColor(self,color):
        #Cambiar el valor de font en las propiedades por el nuevo
        self.textcolor=color        
        #Obligar a que se repinte (hay que invalidar toda el area cliente!!)
        win32gui.InvalidateRect(self.hwnd,win32gui.GetClientRect(self.hwnd),1)

    def setTitle(self,title):
        win32gui.SetWindowText(self.hwnd,title)
        return win32gui.GetWindowText(self.hwnd)

    def getTitle(self):
        return win32gui.GetWindowText(self.hwnd)
        

    def setDraggable(self,_new):
        if _new==0:
            self.__draggable=0
        else:
            self.__draggable=1

    def isDraggable(self):
        return self.__draggable

    def setAlpha(self,alpha):
        if alpha > 255:
            self.alpha = 255
            self.transparent=0
        elif alpha <= 0:
            self.alpha = 0
            self.transparent=1
        else:
            self.alpha=alpha
            self.transparent=1
        #Obligar a que se repinte (hay que invalidar toda el area cliente!!)
        win32gui.InvalidateRect(self.hwnd,win32gui.GetClientRect(self.hwnd),1)            

    def getAlpha(self):
        return self.alpha


    def getWidth(self):
        l,t,r,b = win32gui.GetWindowRect(self.hwnd)
        return r-l

    def getHeight(self):
        l,t,r,b = win32gui.GetWindowRect(self.hwnd)
        return b-t

    def canAcceptDropFiles(self):
        return self.__canDropFiles

    def acceptDropFiles (self,value):
        pycwnd=win32ui.CreateWindowFromHandle(self.hwnd)       
        if value!=0:            
            self.__canDropFiles=1
            pycwnd.ModifyStyleEx(0,win32con.WS_EX_ACCEPTFILES)
        else:
            self.__canDropFiles=0
            pycwnd.ModifyStyleEx(win32con.WS_EX_ACCEPTFILES,0)

    def getDroppedFiles(self):
        return self.__droppedFiles

    def delDroppedFiles(self):
        self.__droppedFiles=[]

    def center(self):
        # centrar el dialogo
        win32ui.CreateWindowFromHandle(self.hwnd).CenterWindow()

    def changeStyle(self,style,ex_style=0): #ESTO NO VA BIEN!!!!
        pycwnd=win32ui.CreateWindowFromHandle(self.hwnd)
        style=winStyleMaker(style)
        #print '\nESTILO CAMBIADO!!!!\n'
        #Borramos estilo anterior y ponemos el nuevo
        pycwnd.ModifyStyle(pycwnd.GetStyle(),style)
        #Cambiar estilo extendido si procede
        if ex_style:
            pycwnd.ModifyStyleEx(win32con.WS_EX_LAYERED,0)
            #Obligar a que el fondo sea opaco
            self.transparent=0
            self.alpha=256


    def OnInitDialog(self, hwnd, msg, wparam, lparam):
        #Esto es necesario para tener controles OLE
        win32ui.EnableControlContainer()
        win32ui.Enable3dControls()
        win32ui.InitRichEdit()
        
        self.hwnd = hwnd

        #Asignar el menu si lo hay
        if self.hmenu:
            win32gui.SetMenu(self.hwnd,self.hmenu)
        #Registrar el formulario para poder recibir eventos
        self.registerControl('self',self.hwnd,'form')


        #Otro intento de conseguir un control activex(no lo destruye al cerrar la aplicacion)      
        #self.iecontrol=Browser(self.hwnd,"http://google.co.uk")
        #win32gui.MoveWindow(self.iecontrol.getHwnd(), 10,200, 200, 200, 1)

        #Ejecutar codigo de inicializacion de usuario
        if self.events.has_key('self|init'):
            self.events['self|init'](self)

        #Crear barra de estado
        self.createStatusBar(3)


    def _destroy(self):
        #print 'en _destroy'
        win32gui.DestroyWindow(self.hwnd)

    def destroy(self):
        self._destroy()
        #sys.exit(0)#Es necesario esto!!!!
        

    def OnSize(self, hwnd, msg, wparam, lparam):
        #x = win32api.LOWORD(lparam)
        #y = win32api.HIWORD(lparam)
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('size',idc,wparam,lparam)
        #Deberiamos colocar aqui la barra de estado si la tiene?????


    def OnMove(self, hwnd, msg, wparam, lparam): #?????????????????????
        win32gui.InvalidateRect(self.hwnd,win32gui.GetClientRect(self.hwnd),0)     

##Manejo basico del raton------------------------------------------

    def OnStartRightClick(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('startrclick',idc,wparam,lparam)
        
    def OnRightClick(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        if hwnd==self.hwnd: #Comprobar si la fuente es el formulario y no un control
            idc=self.hwnd
        print 'CAPTURADO UN CLICK DERECHO!!!!'            
        self.dispatchEvents('rclick',idc,wparam,lparam)        

    def OnRightDblClick(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('rdblclick',idc,wparam,lparam)        

    def OnStartClick(self, hwnd, msg, wparam, lparam):
        #print 'Se ha empezado a hacer click en algo!!'
        idc = win32api.LOWORD(wparam)
        #Calcular posicion de la ventana---------------
        x,y=win32gui.GetCursorPos()
        l,t,r,b=win32gui.GetWindowRect(self.hwnd)
        self.dx=x-l #Constante para tamanyo fijo de ventana
        self.dy=y-t #Constante para tamanyo fijo de ventana
        self.isClicked=1
        #----------------------------------------------
        self.dispatchEvents('startclick',idc,wparam,lparam)        

    def OnClick(self, hwnd, msg, wparam, lparam):
        #print 'Se ha hecho click en algo!!'
        idc = win32api.LOWORD(wparam)
        if hwnd==self.hwnd: #Comprobar si la fuente es el formulario y no un control
            idc=self.hwnd
        self.isClicked=0
        self.dispatchEvents('click',idc,wparam,lparam)        

    def OnDblClick(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('dblclick',idc,wparam,lparam)        

    def OnMouseMove(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        #Mover el formulario si isDraggable=1-------------------------
        #print 'Se ha movido el raton!!'
        #print 'ESTADO DE SELF.ISCLICKED: %d' %self.isClicked
        if self.__draggable and self.isClicked:
            x,y=win32gui.GetCursorPos()
            l,t,r,b=win32gui.GetWindowRect(self.hwnd)
            new_l=x-self.dx
            new_t=y-self.dy
            win32gui.MoveWindow(self.hwnd, new_l, new_t, r-l, b-t, 1)
        #-------------------------------------------------------------
            
        self.dispatchEvents('mousemove',idc,wparam,lparam)        
##------------------------------------------------------------------

    def OnPaint(self, hwnd, msg, wparam, lparam):
  
        #Repintar imagenes-----------------------
        for image in self.images:
            self.drawImage(image)
        #----------------------------------------
        idc = win32api.LOWORD(wparam)                  
        self.dispatchEvents('paint',idc,wparam,lparam)


    def OnDlgColorChange(self, hwnd, msg, wparam, lparam): 
        #print 'PROCESANDO CAMBIO DE COLOR DEL FORMULARIO!!!'
        hwnd=self.hwnd
        bgcolor=self.bgcolor
        textcolor=self.textcolor
        bgmode=self.bgmode
        font=self.font
        #print 'bgmode del formulario: %s' %bgmode
        if bgcolor:
            win32gui.SetBkColor(wparam,bgcolor)
        if textcolor:
            win32gui.SetTextColor(wparam,textcolor)
        #bgmode solo adopta 2 valores OPAQUE y TRANSPARENT. Por defecto OPAQUE          
        if bgmode:
            win32gui.SetBkMode(wparam,win32con.TRANSPARENT)
        else:
            win32gui.SetBkMode(wparam,win32con.OPAQUE)
        if font:
            win32gui.SelectObject(wparam,font)
        if bgcolor==-1: #Fondo transparente
            #print 'Entrando por fondo transparente'
            #alpha=255
            if self.transparent:
                win32gui.SetWindowLong (self.hwnd, win32con.GWL_EXSTYLE,win32gui.GetWindowLong (self.hwnd, win32con.GWL_EXSTYLE ) |win32con.WS_EX_LAYERED)
                win32gui.SetLayeredWindowAttributes(self.hwnd, bgcolor, self.alpha, win32con.LWA_COLORKEY|win32con.LWA_ALPHA)            
                return win32gui.GetStockObject(win32con.NULL_BRUSH)
            else:
                return win32gui.CreateSolidBrush(bgcolor)
        elif bgcolor > 0:
            #print 'Entrando por fondo normal con bgcolor:%d' %bgcolor
            if self.transparent:
                win32gui.SetWindowLong (self.hwnd, win32con.GWL_EXSTYLE,win32gui.GetWindowLong (self.hwnd, win32con.GWL_EXSTYLE ) |win32con.WS_EX_LAYERED)
                win32gui.SetLayeredWindowAttributes(self.hwnd, bgcolor, self.alpha,win32con.LWA_ALPHA|win32con.LWA_ALPHA)
                #return win32gui.GetStockObject(win32con.NULL_BRUSH)
                return win32gui.CreateSolidBrush(bgcolor)
            else:
                return win32gui.CreateSolidBrush(bgcolor)
        else:
            return win32api.GetSysColor(win32con.COLOR_WINDOW)


    def OnStaticColorChange(self, hwnd, msg, wparam, lparam):
        #print 'PROCESANDO UN CAMBIO DE COLOR DE UN LABEL!!!'
        idc=win32gui.GetDlgCtrlID(lparam)
        #print idc
        #print self.controlsprops[idc]
        bgcolor=self.controlsprops[idc].get('bgcolor',None)
        textcolor=self.controlsprops[idc].get('textcolor',None)
        textbgcolor=self.controlsprops[idc].get('textbgcolor',None)
        bgmode=self.controlsprops[idc].get('bgmode',0)
        font=self.controlsprops[idc].get('font',None)
        if textbgcolor:
            win32gui.SetBkColor(wparam,textbgcolor)
        if textcolor:
            win32gui.SetTextColor(wparam,textcolor)
        #bgmode solo adopta 2 valores OPAQUE y TRANSPARENT. Por defecto OPAQUE
        if bgmode:
            win32gui.SetBkMode(wparam,win32con.TRANSPARENT)
        else:
            win32gui.SetBkMode(wparam,win32con.OPAQUE)
        if font:
            win32gui.SelectObject(wparam,font)                     
        if bgcolor and bgcolor!=-1:
            return win32gui.CreateSolidBrush(bgcolor)
        else:
            return win32gui.GetStockObject(win32con.NULL_BRUSH) 


    def OnEditColorChange(self, hwnd, msg, wparam, lparam):
        #print 'PROCESANDO UN CAMBIO DE COLOR DE UN TEXTBOX!!!'
        idc=win32gui.GetDlgCtrlID(lparam)
        #print idc
        #print self.controlsprops[idc]
        bgcolor=self.controlsprops[idc].get('bgcolor',None)
        textcolor=self.controlsprops[idc].get('textcolor',None)
        textbgcolor=self.controlsprops[idc].get('textbgcolor',None)
        bgmode=self.controlsprops[idc].get('bgmode',0)
        font=self.controlsprops[idc].get('font',None)
        if textbgcolor:
            win32gui.SetBkColor(wparam,textbgcolor)
        if textcolor:
            win32gui.SetTextColor(wparam,textcolor)
        #bgmode solo adopta 2 valores OPAQUE y TRANSPARENT. Por defecto OPAQUE
        if bgmode:
            win32gui.SetBkMode(wparam,win32con.TRANSPARENT)
        else:
            win32gui.SetBkMode(wparam,win32con.OPAQUE)
        if font:
            win32gui.SelectObject(wparam,font)                     
        if bgcolor and bgcolor!=-1:
            return win32gui.CreateSolidBrush(bgcolor)
        else:
            return win32gui.GetStockObject(win32con.NULL_BRUSH) 


    def OnButtonColorChange(self, hwnd, msg, wparam, lparam):
        #print 'PROCESANDO UN CAMBIO DE COLOR DE UN BUTTON!!!'
        idc=win32gui.GetDlgCtrlID(lparam)
        #print idc
        #print self.controlsprops[idc]
        bgcolor=self.controlsprops[idc].get('bgcolor',None)
        textcolor=self.controlsprops[idc].get('textcolor',None)
        textbgcolor=self.controlsprops[idc].get('textbgcolor',None)
        bgmode=self.controlsprops[idc].get('bgmode',0)
        font=self.controlsprops[idc].get('font',None)
        #print 'textcolor para el boton: %s' % textcolor
        if textbgcolor:
            win32gui.SetBkColor(wparam,textbgcolor)
        if textcolor:
            win32gui.SetTextColor(wparam,textcolor)
        #bgmode solo adopta 2 valores OPAQUE y TRANSPARENT. Por defecto OPAQUE
        if bgmode:
            win32gui.SetBkMode(wparam,win32con.TRANSPARENT)
        else:
            win32gui.SetBkMode(wparam,win32con.OPAQUE)
        if font:
            win32gui.SelectObject(wparam,font)                     
        if bgcolor and bgcolor!=-1:
            return win32gui.CreateSolidBrush(bgcolor)
        else:
            return win32gui.GetStockObject(win32con.NULL_BRUSH) 

    def OnListBoxColorChange(self, hwnd, msg, wparam, lparam):
        #print 'PROCESANDO UN CAMBIO DE COLOR DE UN LISTBOX!!!'
        idc=win32gui.GetDlgCtrlID(lparam)
        #print idc
        #print self.controlsprops[idc]
        bgcolor=self.controlsprops[idc].get('bgcolor',None)
        textcolor=self.controlsprops[idc].get('textcolor',None)
        textbgcolor=self.controlsprops[idc].get('textbgcolor',None)
        bgmode=self.controlsprops[idc].get('bgmode',0)
        font=self.controlsprops[idc].get('font',None)
        if textbgcolor:
            win32gui.SetBkColor(wparam,textbgcolor)
        if textcolor:
            win32gui.SetTextColor(wparam,textcolor)
        #bgmode solo adopta 2 valores OPAQUE y TRANSPARENT. Por defecto OPAQUE
        if bgmode:
            win32gui.SetBkMode(wparam,win32con.TRANSPARENT)
        else:
            win32gui.SetBkMode(wparam,win32con.OPAQUE)
        if font:
            win32gui.SelectObject(wparam,font)                     
        if bgcolor and bgcolor!=-1:
            return win32gui.CreateSolidBrush(bgcolor)
        else:
            return win32gui.GetStockObject(win32con.NULL_BRUSH) 

    def OnEditColorChange(self, hwnd, msg, wparam, lparam):
        #print 'PROCESANDO UN CAMBIO DE COLOR DE UN TEXTBOX!!!'
        idc=win32gui.GetDlgCtrlID(lparam)
        #print idc
        #print self.controlsprops[idc]
        bgcolor=self.controlsprops[idc].get('bgcolor',None)
        textcolor=self.controlsprops[idc].get('textcolor',None)
        textbgcolor=self.controlsprops[idc].get('textbgcolor',None)
        bgmode=self.controlsprops[idc].get('bgmode',0)
        font=self.controlsprops[idc].get('font',None)
        if textbgcolor:
            win32gui.SetBkColor(wparam,textbgcolor)
        if textcolor:
            win32gui.SetTextColor(wparam,textcolor)
        #bgmode solo adopta 2 valores OPAQUE y TRANSPARENT. Por defecto OPAQUE
        if bgmode:
            win32gui.SetBkMode(wparam,win32con.TRANSPARENT)
        else:
            win32gui.SetBkMode(wparam,win32con.OPAQUE)
        if font:
            win32gui.SelectObject(wparam,font)                     
        if bgcolor and bgcolor!=-1:
            return win32gui.CreateSolidBrush(bgcolor)
        else:
            return win32gui.GetStockObject(win32con.NULL_BRUSH) 

    def OnScrollBarColorChange(self, hwnd, msg, wparam, lparam):
        #print 'PROCESANDO UN CAMBIO DE COLOR DE UN SCROLLBAR!!!'
        idc=win32gui.GetDlgCtrlID(lparam)
        #print idc
        #print self.controlsprops[idc]
        bgcolor=self.controlsprops[idc].get('bgcolor',None)
        textcolor=self.controlsprops[idc].get('textcolor',None)
        textbgcolor=self.controlsprops[idc].get('textbgcolor',None)
        bgmode=self.controlsprops[idc].get('bgmode',0)
        font=self.controlsprops[idc].get('font',None)
        if textbgcolor:
            win32gui.SetBkColor(wparam,textbgcolor)
        if textcolor:
            win32gui.SetTextColor(wparam,textcolor)
        #bgmode solo adopta 2 valores OPAQUE y TRANSPARENT. Por defecto OPAQUE
        if bgmode:
            win32gui.SetBkMode(wparam,win32con.TRANSPARENT)
        else:
            win32gui.SetBkMode(wparam,win32con.OPAQUE)
        if font:
            win32gui.SelectObject(wparam,font)                     
        if bgcolor and bgcolor!=-1:
            return win32gui.CreateSolidBrush(bgcolor)
        else:
            return win32gui.GetStockObject(win32con.NULL_BRUSH) 


    def OnChar(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('char',idc,wparam,lparam)        

    def OnKeyDown(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('keydown',idc,wparam,lparam)        

    def OnCommand(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        #print 'Capturado un mensaje OnCommand. idc,nombre de la fuente: %d,%s' % (idc,self.idcontrols.get(idc,0))
        #Llamar a la funcion que maneja los eventos
        self.dispatchEvents('command',idc,wparam,lparam)
        #print 'Despues de llamar a DispatchEvents'

    def OnNotify(self, hwnd, msg, wparam, lparam): ####===>>
        #print 'Dentro de OnNotify'
        #print 'idcontrol:%d'  %wparam
        '''
        typedef struct tagNM_LISTVIEW {  
        NMHDR hdr; 
        int   iItem; 
        int   iSubItem; 
        UINT  uNewState; 
        UINT  uOldState; 
        UINT  uChanged; 
        POINT ptAction; 
        LPARAM lParam; 
    } NM_LISTVIEW; 
        ''' #format="iiiiiiiiiii"
        hwndFrom=idFrom=code=0
        if wparam==0 or self.kindcontrols[wparam]=='listview':
            format = "iiiiiiiiiii"
            buf = win32gui.PyMakeBuffer(struct.calcsize(format), lparam)
            hwndFrom, idFrom, code,iItem,iSubItem,uNewState,uOldState,uChanged,x,y,lParam = struct.unpack(format, buf)
            #print (hwndFrom, idFrom, code,iItem,iSubItem,uNewState,uOldState,uChanged,x,y,lParam)            
            #print "El mensaje es de un listview!!"
            #code += 0x4f0000 # hrm - wtf - commctrl uses this, and it works with mfc.  *sigh*
            #self.dispatchEvents('notify',idc,wparam,lparam)
            self.dispatchEvents('notify',idFrom,code,hwndFrom,(hwndFrom, idFrom, code,iItem,iSubItem,uNewState,uOldState,uChanged,x,y,lParam))
        else:
            # Parse the NMHDR
            format = "iii"
            buf = win32gui.PyMakeBuffer(struct.calcsize(format), lparam)
            hwndFrom, idFrom, code = struct.unpack(format, buf)
            #print (hwndFrom, idFrom, code)
            self.dispatchEvents('notify',idFrom,code,hwndFrom)
        

    def OnGetFocus(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('getfocus',idc,wparam,lparam)        

    def OnLoseFocus(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('lostfocus',idc,wparam,lparam)        
        
    def OnTimer(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('timer',idc,wparam,lparam)        

    def OnDropFiles(self, hwnd, msg, wparam, lparam):
        #print 'OH MY GOD, THEY DROPPED FILES ON ME!!!!\n\n'
        numfiles=win32api.DragQueryFile(wparam)
        #print 'Se han arrastrado %d archivos!!' % numfiles
        #for i in range(numfiles):
        #    print win32api.DragQueryFile(wparam,i)
        #Llamar al codigo de usuario si se ha definido
        self.dispatchEvents('dropfiles',self.hwnd,wparam,lparam)
        #Liberar memoria
        win32api.DragFinish(wparam)

    # These function differ based on how the window is used, so may be overridden
    def OnClose(self, hwnd, msg, wparam, lparam):
        raise NotImplementedError

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        raise NotImplementedError



# An implementation suitable for use with the Win32 Window functions (ie, not
# a true dialog)
class MiniWindow(MiniWindowBase):
    def CreateWindow(self,parent=0):
        # Create the window via CreateDialogBoxIndirect - it can then
        # work as a "normal" window, once a message loop is established.
        self._DoCreate(win32gui.CreateDialogIndirect)
        #Hay que centrar aqui. Cuando es un dialogo modal no pinta bien al crearse
        #self.center()

    def OnClose(self, hwnd, msg, wparam, lparam):
        if self.iecontrol:
            win32gui.DestroyWindow(self.iecontrol)
        win32gui.DestroyWindow(hwnd)
        #print 'en OnClose'
        #sys.exit(0)

    # We need to arrange to a WM_QUIT message to be sent to our
    # PumpMessages() loop.
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        win32gui.PostQuitMessage(0) # Terminate the app.
        #print 'Intentando cerrar esto!!!'



# An implementation suitable for use with the Win32 Dialog functions.
class MiniDialog(MiniWindowBase):
    def DoModal(self,parent):
        return self._DoCreate(win32gui.DialogBoxIndirect,parent)

    def OnClose(self, hwnd, msg, wparam, lparam):
        win32gui.EndDialog(hwnd, 0)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        pass

    def ExitDialog(self, exit_value):
        #Cierra el dialogo con valor exit_value
        #print 'Cerrando el dialogo!'
        win32gui.EndDialog(hwnd, exit_value)


class MiniTaskBarWindow:
    
    def __init__(self, window_title, window_icon, menu, tool_tip_text='MiniTaskBarWindow'):
        win32gui.InitCommonControls()
        # Need to do this go get rich-edit working.
        win32api.LoadLibrary("Riched20.dll")        
        #------------------------------------------------------------------------------------------------------
        #Variable que mantiene el icono asignado a la ventana
        self.icon=window_icon
        #Variable que mantiene el texto que se muestra en el  tooltip
        self.tooltip=tool_tip_text
        #Menu (es obligatorio especificar uno!)
        self.hmenu=menu
        #Tabla de controles por nombre {nombre_control:idc}
        self.controls = {}
        #Tabla de controles por id {idc:nombre_control}
        self.idcontrols={} 
        #Tabla de eventos registrados
        self.events={}
        #------------------------------------------------------------------------------------------------------
        msg_TaskbarRestart = win32gui.RegisterWindowMessage("TaskbarCreated");
        message_map = {
                msg_TaskbarRestart: self.OnRestart,
                win32con.WM_DESTROY: self.OnDestroy,
                win32con.WM_COMMAND: self.OnCommand, #Se llama al pulsar un item de menu
                win32con.WM_USER+20 : self.OnTaskbarNotify,
        }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = generateClassName()#"PythonTaskbarDemo"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        wc.hCursor = win32gui.LoadCursor( 0, win32con.IDC_ARROW )
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = win32gui.RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow( classAtom, window_title, style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        #----------------------------------------------------------------
        #Registrar el formulario para poder recibir eventos
        self.__registerControl('self',self.hwnd,'form')
        #Ejecutar codigo de inicializacion de usuario si lo hay
        if self.events.has_key('self|init'):
            self.events['self|init'](self)        
        #-----------------------------------------------------------------        
        win32gui.UpdateWindow(self.hwnd)
        self._DoCreateIcons()

        
    def _DoCreateIcons(self):
        hinst =  win32gui.GetModuleHandle(None)
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        hicon = win32gui.LoadImage(hinst, self.icon, win32con.IMAGE_ICON, 0, 0, icon_flags)
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, self.tooltip)
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        except:
            # This is common when windows is starting, and this code is hit
            # before the taskbar has been created.
            print "Failed to add the taskbar icon - is explorer running?"
            # but keep running anyway - when explorer starts, we get the
            # TaskbarCreated message.

    def showPopupMenu(self, menu):
        #Muestra un menu emergente
        x,y = win32gui.GetCursorPos()
        #Hay que registrar el menu para poder coger sus eventos
        #(self.hmenu,self.nameid,self.namecallb)
        #print menu
        hmenu=menu[0] #hmenu
        for item in menu[1]:
            self.__registerControl(item,menu[1][item],'menuitem')
        for item in menu[2]:
            self.registerEvent(item,'command',menu[2][item])
        #print self.controls
        win32gui.TrackPopupMenu(hmenu, win32con.TPM_LEFTALIGN, x, y, 0, self.hwnd, None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
##        #Una vez usado, hay que borrarlo
##        for item in menu[1]:
##            del self.controls[item]
##            del self.events[item + '|command']    


    def getControl(self,idorname):
        #Devuelve un hcontrol dado su id o el nombre con el que se ha registrado
        control=0 #Por defecto un hcontrol nulo
        if type(idorname)==type(""): #Nombre
            control=win32gui.GetDlgItem(self.hwnd,self.controls[idorname])
        elif type(idorname) in [type(3),type(3L)]: #Idcontrol
            control=win32gui.GetDlgItem(self.hwnd,idorname)
        #print 'HWND CONTROL: %d' %control
        return control


    def __registerControl(self,name,idc,kind):
        #Registra un control para poder usarlo luego por su nombre, su id o su clase
        #print 'Registrando control %s!!' % name
        self.controls[name]=idc
        self.idcontrols[idc]=name


    def registerEvent(self,evt_src,evt_name,callback_func):
        #Registra un evento:
        #evt_src: idc del control para el que lo definimos
        #evt_name: nombre del evento (ej: click, mouseout, etc)
        #callb_func_name:
        #Para poder manejar eventos iguales para diferentes controles,
        #las entradas de la tabla son nombre_control|nombre_evento:callback_func
        #print evt_src
        #print evt_name
        #No se puede comprobar que el control exista porque hasta que
        #se llama a _DoCreate no se registran los controles!!
        self.events[evt_src + '|' + evt_name]=callback_func
        #print 'Registrando evento:%s' %str(self.events)


    def dispatchEvents(self,evt_type,idc_src,wparam,lparam,*args):
        #Llama a la funcion definida para cada evento si existe
        ###Si el evento se refiere al formulario, se registra con el nombre de 'self'------------------
        #print 'En DispatchEvents'
        #print evt_type
        if evt_type=='command':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'command'
                #print 'Nombre del evento: %s' %evt_name
                #print self.events
                if self.events.has_key(evt_name):
                    if self.events[evt_name] in [None,0,'']:
                        self._destroy()
                    else:
                        #Hay que pasar una referencia al formulario para que pueda manejarlo el codigo externo
                        self.events[evt_name](self)
        elif evt_type=='click':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'click'
                if self.events.has_key(evt_name):
                    if self.events[evt_name] in [None,0,'']:
                        self._destroy()
                    else:
                        self.events[evt_name](self)
        elif evt_type=='dblclick':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'dblclick'
                if self.events.has_key(evt_name):
                    if self.events[evt_name] in [None,0,'']:
                        self._destroy()
                    else:
                        self.events[evt_name](self)

                    
    #Funciones para funcionamiento basico. Se pueden sobreescribir en las clases derivadas para cambiarlo----------------
    def OnClick(self):
        print 'Se ha hecho click en el icono del taskbar' #pass         
        self.dispatchEvents('click',self.hwnd,0,0)                

    def OnDoubleClick(self):
        print 'Se ha hecho doble click en el icono del taskbar' #pass
        self.dispatchEvents('dblclick',self.hwnd,0,0)       

    def OnRightClick(self):
        print 'Se ha hecho click derecho en el icono del taskbar'
        self.showPopupMenu(self.hmenu)

    def _destroy(self):
        win32gui.DestroyWindow(self.hwnd)

    def destroy(self):
        self._destroy()        
    #---------------------------------------------------------------------------------------------------------------------

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self._DoCreateIcons()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0) # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam==win32con.WM_LBUTTONUP:
            self.OnClick()
        elif lparam==win32con.WM_LBUTTONDBLCLK:
            self.OnDoubleClick()
        elif lparam==win32con.WM_RBUTTONUP:
            self.OnRightClick()
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        #print 'Capturado un mensaje OnCommand. idc,nombre de la fuente: %d,%s' % (idc,self.idcontrols.get(idc,0))
        #Llamar a la funcion que maneja los eventos
        self.dispatchEvents('command',idc,wparam,lparam)
        #print 'Despues de llamar a DispatchEvents'



            