import win32con
import sys
from ctypes import *
import time


import win32con

from ctypes import *
from ctypes.wintypes import *
from comtypes import IUnknown
from comtypes.automation import IDispatch, VARIANT
from comtypes.client import wrap, GetModule

#from win32com.client import *
#cast = gencache.GetModuleForProgID('htmlfile')

if not hasattr(sys, 'frozen'):
    GetModule('atl.dll')
    GetModule('shdocvw.dll')
    #Esto es necesario porque a veces no crea el modulo solo!!------
    GetModule('mshtml.tlb')
    #---------------------------------------------------------------

kernel32 = windll.kernel32
user32 = windll.user32
atl = windll.atl                  # If this fails, you need atl.dll

import win32con
from ctypes import *
from comtypes import IUnknown
from comtypes.automation import VARIANT
from comtypes.client import GetEvents
from comtypes.gen import SHDocVw
from comtypes.gen import MSHTML

kernel32 = windll.kernel32
user32 = windll.user32

WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)

class WNDCLASS(Structure):
    _fields_ = [('style', c_uint),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', c_int),
                ('hIcon', c_int),
                ('hCursor', c_int),
                ('hbrBackground', c_int),
                ('lpszMenuName', c_char_p),
                ('lpszClassName', c_char_p)]

class RECT(Structure):
    _fields_ = [('left', c_long),
                ('top', c_long),
                ('right', c_long),
                ('bottom', c_long)]

class PAINTSTRUCT(Structure):
    _fields_ = [('hdc', c_int),
                ('fErase', c_int),
                ('rcPaint', RECT),
                ('fRestore', c_int),
                ('fIncUpdate', c_int),
                ('rgbReserved', c_char * 32)]

class POINT(Structure):
    _fields_ = [('x', c_long),
                ('y', c_long)]
    
class MSG(Structure):
    _fields_ = [('hwnd', c_int),
                ('message', c_uint),
                ('wParam', c_int),
                ('lParam', c_int),
                ('time', c_int),
                ('pt', POINT)]

def ErrorIfZero(handle):
    if handle == 0:
        raise Exception('WinError')
    else:
        return handle

class EventSink(object):
    # some DWebBrowserEvents
    def OnVisible(self, this, *args):
        print "OnVisible", args

    def BeforeNavigate(self, this, *args):
        print "BeforeNavigate", args

    def NavigateComplete(self, this, *args):
        if self._loaded:
            return
        self._loaded = True
        print "NavigateComplete", this, args
        return


    # some DWebBrowserEvents2
    def BeforeNavigate2(self, this, *args):
        print "BeforeNavigate2", args

    def NavigateComplete2(self, this, *args):
        print "NavigateComplete2", args

    def DocumentComplete(self, this, *args):
        self.valid_doc = time.time() + 1
        print "DocumentComplete", args

    def NewWindow2(self, this, *args):
        print "NewWindow2", args
        return

    def NewWindow3(self, this, *args):
        print "NewWindow3", args
        return

class Browser(EventSink):
    def __init__(self,parent=win32con.NULL, url='about:blank'):
        EventSink.__init__(self)
        self._loaded = False
        self.valid_doc = False
        CreateWindowEx = windll.user32.CreateWindowExA
        CreateWindowEx.argtypes = [c_int, c_char_p, c_char_p, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int]
        CreateWindowEx.restype = ErrorIfZero

        # Create an instance of IE via AtlAxWin.
        atl.AtlAxWinInit()
        hInstance = kernel32.GetModuleHandleA(None)

        hwnd = CreateWindowEx(0,
                              "AtlAxWin",
                              "Python Window",
                              #win32con.WS_OVERLAPPEDWINDOW |
                              win32con.WS_CHILD |
                              win32con.WS_VISIBLE | 
                              win32con.WS_HSCROLL | win32con.WS_VSCROLL,
                              win32con.CW_USEDEFAULT,
                              win32con.CW_USEDEFAULT,
                              win32con.CW_USEDEFAULT,
                              win32con.CW_USEDEFAULT,
                              parent,
                              win32con.NULL,
                              hInstance,
                              win32con.NULL)

        #Guardar la instancia de hwnd para poder manipularla
        self.hwnd=hwnd
        # Get the IWebBrowser2 interface for the IE control.
        self.pBrowserUnk = POINTER(IUnknown)()
        atl.AtlAxGetControl(hwnd, byref(self.pBrowserUnk))
        # the wrap call querys for the default interface
        self.pBrowser = wrap(self.pBrowserUnk)
        self.pBrowser.RegisterAsBrowser = True
        self.pBrowser.AddRef()

        v = byref(VARIANT())
        self.pBrowser.Navigate(url, v, v, v, v)

        # Show Window
        windll.user32.ShowWindow(c_int(hwnd), c_int(win32con.SW_SHOWNORMAL))
        windll.user32.UpdateWindow(c_int(hwnd))


    def getBrowser(self):
        return self.pBrowser

    def getHwnd(self):
        return self.hwnd    
        

def MainWin():
    b = Browser(url="http://google.com")

    # Pump Messages
    msg = MSG()
    pMsg = pointer(msg)
    NULL = c_int(win32con.NULL)
    
    while windll.user32.GetMessageA( pMsg, NULL, 0, 0) != 0:

        if b.valid_doc:
            print b.valid_doc, time.time()
            if b.valid_doc < time.time():
                b.valid_doc = 0
                print dir(b.pBrowser)
                sys.stdout.flush()
        if hasattr(b.pBrowser, "Document"):
            print "doc", b.pBrowser.Document
        windll.user32.TranslateMessage(pMsg)
        windll.user32.DispatchMessageA(pMsg)

        print msg.message
        if msg.message == 161: #win32con.WM_DESTROY:
            windll.user32.PostQuitMessage(0)


    return msg.wParam
    
if __name__=='__main__':
    sys.exit(MainWin())

