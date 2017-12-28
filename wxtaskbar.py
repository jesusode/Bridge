import wx

ID_ICON_TIMER = wx.NewId()

class TaskBarFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, style=wx.FRAME_NO_TASKBAR | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.icon_state = False
        self.blink_state = False

        self.tbicon = wx.TaskBarIcon()
        icon = wx.Icon('icono.ico', wx.BITMAP_TYPE_ICO)
        self.tbicon.SetIcon(icon, '')
        wx.EVT_TASKBAR_LEFT_DCLICK(self.tbicon, self.OnTaskBarLeftDClick)
        wx.EVT_TASKBAR_RIGHT_UP(self.tbicon, self.OnTaskBarRightClick)
        self.Show(True)

    def OnTaskBarLeftDClick(self, evt):
        try:
            self.icontimer.Stop()
        except:
            pass
        if self.icon_state:
            icon = wx.Icon('icono.ico', wx.BITMAP_TYPE_ICO)
            self.tbicon.SetIcon(icon, 'Yellow')
            self.icon_state = False
        else:
            self.SetIconTimer()
            self.icon_state = True

    def OnTaskBarRightClick(self, evt):
        self.Close(True)
        wx.GetApp().ProcessIdle()

    def SetIconTimer(self):
        self.icontimer = wx.Timer(self, ID_ICON_TIMER)
        wx.EVT_TIMER(self, ID_ICON_TIMER, self.BlinkIcon)
        self.icontimer.Start(1000)

    def BlinkIcon(self, evt):
        if not self.blink_state:
            icon = wx.Icon('faicon.ico', wx.BITMAP_TYPE_ICO)
            self.tbicon.SetIcon(icon, 'Red')
            self.blink_state = True
        else:
            icon = wx.Icon('favicon.ico', wx.BITMAP_TYPE_ICO)
            self.tbicon.SetIcon(icon, 'Black')
            self.blink_state = False


app = wx.App(False)
frame = TaskBarFrame(None)
frame.Show(False)
app.MainLoop()