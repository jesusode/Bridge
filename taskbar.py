
import sys
sys.path.append('.')#Para py2exe
sys.path.append('./modules')#Para py2exe
sys.path.append('library.zip')#Para py2exe
import wx
import wx.grid
import wx.html
from wx_support import *





def menu_callb(evt):
    print 'Item de menu pulsado!'

def show_form(evt):
    print 'mostrando form'
    frm1.Show()

def exit_app(evt):
    root.ExitMainLoop()




root=wx.App()

frm1=wx.Frame(parent=None)
ico1=wx.Icon("icono.ico",wx.BITMAP_TYPE_ICO)
tsk=MinimalTaskBarIcon(labels=["Form","Salir"],callbacks=[show_form,exit_app])
file=wx.Menu()
tsk.Bind(wx.EVT_TASKBAR_LEFT_DCLICK,exit_app)
tsk.Bind(wx.EVT_TASKBAR_RIGHT_DCLICK,show_form)




tsk.SetIcon(ico1, "Taskbar applet!")




root.MainLoop()
