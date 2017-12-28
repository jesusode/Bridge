from ctypes import *
import win32con
WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)

NULL = c_int(win32con.NULL)
_user32 = windll.user32

def ErrorIfZero(handle):
    if handle == 0:
        raise WinError()
    else:
        return handle

CreateWindowEx = _user32.CreateWindowExW
CreateWindowEx.argtypes = [c_int,
                           c_wchar_p,
                           c_wchar_p,
                           c_int,
                           c_int,
                           c_int,
                           c_int,
                           c_int,
                           c_int,
                           c_int,
                           c_int,
                           c_int]
CreateWindowEx.restype = ErrorIfZero

class WNDCLASS(Structure):
    _fields_ = [('style', c_uint),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', c_int),
                ('hIcon', c_int),
                ('hCursor', c_int),
                ('hbrBackground', c_int),
                ('lpszMenuName', c_wchar_p),
                ('lpszClassName', c_wchar_p)]

    def __init__(self,
                 wndProc,
                 style=win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                 clsExtra=0,
                 wndExtra=0,
                 menuName=None,
                 className=u"PythonWin32",
                 instance=None,
                 icon=None,
                 cursor=None,
                 background=None,
                 ):

        if not instance:
            instance = windll.kernel32.GetModuleHandleW(c_int(win32con.NULL))
        if not icon:
            icon = _user32.LoadIconW(c_int(win32con.NULL),
                                     c_int(win32con.IDI_APPLICATION))
        if not cursor:
            cursor = _user32.LoadCursorW(c_int(win32con.NULL),
                                         c_int(win32con.IDC_ARROW))
        if not background:
            background = windll.gdi32.GetStockObject(c_int(win32con.WHITE_BRUSH))

        self.lpfnWndProc=wndProc
        self.style=style
        self.cbClsExtra=clsExtra
        self.cbWndExtra=wndExtra
        self.hInstance=instance
        self.hIcon=icon
        self.hCursor=cursor
        self.hbrBackground=background
        self.lpszMenuName=menuName
        self.lpszClassName=className

class RECT(Structure):
    _fields_ = [('left', c_long),
                ('top', c_long),
                ('right', c_long),
                ('bottom', c_long)]
    def __init__(self, left=0, top=0, right=0, bottom=0 ):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

class PAINTSTRUCT(Structure):
    _fields_ = [('hdc', c_int),
                ('fErase', c_int),
                ('rcPaint', RECT),
                ('fRestore', c_int),
                ('fIncUpdate', c_int),
                ('rgbReserved', c_wchar * 32)]

class POINT(Structure):
    _fields_ = [('x', c_long),
                ('y', c_long)]
    def __init__( self, x=0, y=0 ):
        self.x = x
        self.y = y

class MSG(Structure):
    _fields_ = [('hwnd', c_int),
                ('message', c_uint),
                ('wParam', c_int),
                ('lParam', c_int),
                ('time', c_int),
                ('pt', POINT)]

def pump_messages():
    """Calls message loop"""
    msg = MSG()
    pMsg = pointer(msg)

    while _user32.GetMessageW(pMsg, NULL, 0, 0):
        _user32.TranslateMessage(pMsg)
        _user32.DispatchMessageW(pMsg)

    return msg.wParam

class Window(object):
    """Wraps an HWND handle"""

    def __init__(self, hwnd=NULL):
        self.hwnd = hwnd

        self._event_handlers = {}

        # Register event handlers
        for key in dir(self):
            method = getattr(self, key)
            if hasattr(method, "win32message") and callable(method):
                self._event_handlers[method.win32message] = method

    def GetClientRect(self):
        rect = RECT()
        _user32.GetClientRect(self.hwnd, byref(rect))
        return rect

    def Create(self,
            exStyle=0 ,        #  DWORD dwExStyle
            className=u"WndClass",
            windowName=u"Window",
            style=win32con.WS_OVERLAPPEDWINDOW,
            x=win32con.CW_USEDEFAULT,
            y=win32con.CW_USEDEFAULT,
            width=win32con.CW_USEDEFAULT,
            height=win32con.CW_USEDEFAULT,
            parent=NULL,
            menu=NULL,
            instance=NULL,
            lparam=NULL,
            ):

        self.hwnd = CreateWindowEx(exStyle,
                              className,
                              windowName,
                              style,
                              x,
                              y,
                              width,
                              height,
                              parent,
                              menu,
                              instance,
                              lparam)
        return self.hwnd

    def Show(self, flag):
        return _user32.ShowWindow(self.hwnd, flag)

    def Update(self):
        if not _user32.UpdateWindow(self.hwnd):
            raise WinError()

    def WndProc(self, hwnd, message, wParam, lParam):

        event_handler = self._event_handlers.get(message, None)
        if event_handler:
            return event_handler(message, wParam, lParam)
        return _user32.DefWindowProcW(c_int(hwnd),
                                      c_int(message),
                                      c_int(wParam),
                                      c_int(lParam))

## Lifted shamelessly from WCK (effbot)'s wckTkinter.bind
def EventHandler(message):
    """Decorator for event handlers"""
    def decorator(func):
        func.win32message = message
        return func
    return decorator

class HelloWindow(Window):
    """The application window"""

    @EventHandler(win32con.WM_PAINT)
    def OnPaint(self, message, wParam, lParam):
        """Draw 'Hello World' in center of window"""
        ps = PAINTSTRUCT()
        rect = self.GetClientRect()
        hdc = _user32.BeginPaint(c_int(self.hwnd), byref(ps))
        rect = self.GetClientRect()
        flags = win32con.DT_SINGLELINE|win32con.DT_CENTER|win32con.DT_VCENTER
        _user32.DrawTextW(c_int(hdc),
                          u"Hello, world!",
                          c_int(-1),
                          byref(rect),
                          flags)
        _user32.EndPaint(c_int(self.hwnd), byref(ps))
        return 0

    @EventHandler(win32con.WM_DESTROY)
    def OnDestroy(self, message, wParam, lParam):
        """Quit app when window is destroyed"""
        _user32.PostQuitMessage(0)
        return 0

def RunHello():
    """Create window and start message loop"""

    # two-stage creation for Win32 windows
    hello = HelloWindow()

    # register window class
    wndclass = WNDCLASS(WNDPROC(hello.WndProc))
    wndclass.lpszClassName = u"HelloWindow"

    if not _user32.RegisterClassW(byref(wndclass)):
        raise WinError()

    # then create Window

    hello.Create( className=wndclass.lpszClassName,
                  instance=wndclass.hInstance,
                  windowName=u"Hello World")

    # Show Window
    hello.Show(win32con.SW_SHOWNORMAL)
    hello.Update()

    pump_messages()

RunHello()