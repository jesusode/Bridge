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

from win32gui_utils import *
from win32_aux_structs import *

#from interprete import *



class MiniWindowBase:
    def __init__(self,className,win_template=[],menu=None,icon=None):
        win32gui.InitCommonControls()
        # Need to do this go get rich-edit working.
        win32api.LoadLibrary("Riched20.dll")
        
        self.hinst = win32gui.dllhandle
        self.g_iconPathName=icon
        self.g_registeredClass = 0
        
        self.title='Mini Windows Base'
        self.__className=className
        #Tabla de controles por nombre {nombre_control:idc}
        self.controls = {}
        #Tabla de controles por id {nombre_control:idc}
        self.idcontrols={}
        #Tabla de controles por clase {idc:kind}
        self.kindcontrols={}        
        #Tabla de eventos registrados
        self.events={}

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


    def registerControl(self,name,idc,kind):
        #Registra un control para poder usarlo luego por su nombre, su id o su clase
        print 'Registrando control %s!!' % name
        self.controls[name]=idc
        self.idcontrols[idc]=name
        self.kindcontrols[idc]=kind


    def _SetupListView(self,idc):
        pass

    
    def getControl(self,idorname):
        #Devuelve un hcontrol dado su id o el nombre con el que se ha registrado
        control=0 #Por defecto un hcontrol nulo
        if type(idorname)==type(""): #Nombre
            control=win32gui.GetDlgItem(self.hwnd,self.controls[idorname])
        elif type(idorname)==type('3'): #Idcontrol
            control=win32gui.GetDlgItem(self.hwnd,idorname)
        print 'HWND CONTROL: %d' %control
        return control
            

    def registerEvent(self,evt_src,evt_name,callback_func):
        #Registra un evento:
        #evt_src: idc del control para el que lo definimos
        #evt_name: nombre del evento (ej: click, mouseout, etc)
        #callb_func_name:
        #Para poder manejar eventos iguales para diferentes controles,
        #las entradas de la tabla son nombre_control|nombre_evento:callback_func
        print evt_src
        print evt_name
        #No se puede comprobar que el control exista porque hasta que
        #se llama a _DoCreate no se registran los controles!!
        self.events[evt_src + '|' + evt_name]=callback_func
        print 'Registrando evento:%s' %str(self.events)


    def dispatchEvents(self,evt_type,idc_src,wparam,lparam):
        #Llama a la funcion definida para cada evento si existe
        #idc = win32api.LOWORD(wparam)
        ###Si el evento se refiere al formulario, se registra con el nombre de 'self'------------------
        if evt_type=='command':
            if self.idcontrols.has_key(idc_src):
                evt_name=self.idcontrols[idc_src] + '|' + 'command'
                if self.events.has_key(evt_name):
                    self.events[evt_name](self,wparam,lparam) #Hay que pasar una referencia al formulario para que pueda manejarlo el codigo externo
        elif evt_type=='paint':
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


    def showPopupMenu(self, menu):
        #Muestra un menu emergente
        x,y = win32gui.GetCursorPos()
        #Hay que registrar el menu para poder coger sus eventos
        #(self.hmenu,self.nameid,self.namecallb)
        print menu
        hmenu=menu[0] #hmenu
        for item in menu[1]:
            self.registerControl(item,menu[1][item],'menuitem')
        for item in menu[2]:
            self.registerEvent(item,'command',menu[2][item])
        print self.controls
        win32gui.TrackPopupMenu(hmenu, win32con.TPM_LEFTALIGN, x, y, 0, self.hwnd, None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        #Una vez usado, hay que borrarlo
        for item in menu[1]:
            del self.controls[item]
            del self.events[item + '|command']           

                    

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
        print 'Dentro de GetDlgTemplate!!'
        templ=self.win_template
        dlg=[templ[0]]
        for item in templ[1:]:
            name,idc,control,kind=item
            self.registerControl(name,idc,kind)
            dlg.append(control)
        #print dlg
        print self.controls
        return dlg

    def _DoCreate(self, fn):
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
            win32con.WM_MOVE: self.OnMouseMove, #Movimiento del raton
            win32con.WM_PAINT: self.OnPaint, #Eventos Paint
            win32con.WM_CHAR: self.OnChar, #Pulsacion de teclado paratextbox
            win32con.WM_KEYDOWN: self.OnKeyDown, #Respuesta a pulsacion de teclado
            win32con.WM_NOTIFY: self.OnNotify, #Mensajes Notify
            win32con.WM_SETFOCUS: self.OnGetFocus, #Obtencion del foco
            win32con.WM_KILLFOCUS: self.OnLoseFocus, #Perdida del foco
            win32con.WM_TIMER: self.OnTimer #Evento timer
        }
        dlgClassName = self._RegisterWndClass()
        template = self._GetDialogTemplate(dlgClassName)
        return fn(self.hinst, template, 0, message_map)


    def OnInitDialog(self, hwnd, msg, wparam, lparam):
        self.hwnd = hwnd
        #Asignar el menu
        win32gui.SetMenu(self.hwnd,self.hmenu)
        #Registrar el formulario para poder recibir eventos
        self.registerControl('self',self.hwnd,'form')
        #Inicializar listviews y otros controles que lo requieran: Es necesario o se hace en self|init???
        for item in self.controls:
            if self.kindcontrols[self.controls[item]]=='listview':
                self._SetupListView(self.controls[item])            
        
        # centrar el dialogo
        desktop = win32gui.GetDesktopWindow()
        l,t,r,b = win32gui.GetWindowRect(self.hwnd)
        dt_l, dt_t, dt_r, dt_b = win32gui.GetWindowRect(desktop)
        centre_x, centre_y = win32gui.ClientToScreen( desktop, ( (dt_r-dt_l)/2, (dt_b-dt_t)/2) )
        win32gui.MoveWindow(hwnd, centre_x-(r/2), centre_y-(b/2), r-l, b-t, 0)

        
        #Ejecutar codigo de inicializacion de usuario
        if self.events.has_key('self|init'):
            self.events['self|init'](self)


    def OnSize(self, hwnd, msg, wparam, lparam):
        #x = win32api.LOWORD(lparam)
        #y = win32api.HIWORD(lparam)
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('size',idc,wparam,lparam)
        

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
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('startclick',idc,wparam,lparam)        

    def OnClick(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        if hwnd==self.hwnd: #Comprobar si la fuente es el formulario y no un control
            idc=self.hwnd                
        self.dispatchEvents('click',idc,wparam,lparam)        

    def OnDblClick(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('dblclick',idc,wparam,lparam)        

    def OnMouseMove(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('mousemove',idc,wparam,lparam)        
##------------------------------------------------------------------

    def OnPaint(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('paint',idc,wparam,lparam)        

    def OnChar(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('char',idc,wparam,lparam)        

    def OnKeyDown(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('keydown',idc,wparam,lparam)        

    def OnCommand(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        print 'Capturado un mensaje OnCommand. idc,nombre de la fuente: %d,%s' % (idc,self.idcontrols[idc])
        #Llamar a la funcion que maneja los eventos
        self.dispatchEvents('command',idc,wparam,lparam)
        print 'Despues de llamar a DispatchEvents'

    def OnNotify(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('notify',idc,wparam,lparam)        

    def OnGetFocus(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('getfocus',idc,wparam,lparam)        

    def OnLoseFocus(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('lostfocus',idc,wparam,lparam)        
        
    def OnTimer(self, hwnd, msg, wparam, lparam):
        idc = win32api.LOWORD(wparam)
        self.dispatchEvents('timer',idc,wparam,lparam)        


    # These function differ based on how the window is used, so may be overridden
    def OnClose(self, hwnd, msg, wparam, lparam):
        raise NotImplementedError

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        pass



# An implementation suitable for use with the Win32 Window functions (ie, not
# a true dialog)
class MiniWindow(MiniWindowBase):
    def CreateWindow(self):
        # Create the window via CreateDialogBoxIndirect - it can then
        # work as a "normal" window, once a message loop is established.
        self._DoCreate(win32gui.CreateDialogIndirect)

    def OnClose(self, hwnd, msg, wparam, lparam):
        win32gui.DestroyWindow(hwnd)

    # We need to arrange to a WM_QUIT message to be sent to our
    # PumpMessages() loop.
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        win32gui.PostQuitMessage(0) # Terminate the app.



# An implementation suitable for use with the Win32 Dialog functions.
class MiniDialog(MiniWindowBase):
    def DoModal(self):
        return self._DoCreate(win32gui.DialogBoxIndirect)

    def OnClose(self, hwnd, msg, wparam, lparam):
        win32gui.EndDialog(hwnd, 0)

        