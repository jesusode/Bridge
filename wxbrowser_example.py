import wx 
import wx.html2 

class MyBrowser(wx.Frame): 
  def __init__(self, *args, **kwds): 
    wx.Frame.__init__(self, *args, **kwds) 
    sizer = wx.BoxSizer(wx.VERTICAL) 
    self.browser = wx.html2.WebView.New(self) 
    sizer.Add(self.browser, 1, wx.EXPAND, 10) 
    self.SetSizer(sizer) 
    self.SetSize((700, 700)) 

if __name__ == '__main__': 
    _html="""
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
            "http://www.w3.org/TR/html4/loose.dtd">
    <html><head><title>Pruebas</title></head>
    <body>
    <h3>Formulario<h3>
    <form>
    <span>campo 1</span>
    <input type="text" name="txt1" id="txt1"/>
    </form>
    <a href="www.noplace.com">Enlace</a>
    </body>
    </html>"""
    app = wx.App() 
    dialog = MyBrowser(None, -1) 
    #dialog.browser.LoadURL("http://www.google.com") 
    dialog.browser.SetPage(_html,"") 
    dialog.Show() 
    app.MainLoop() 