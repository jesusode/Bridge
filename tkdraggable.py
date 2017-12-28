from Tkinter import *
tk = Tk()
#tk.withdraw()
root=Toplevel(tk)
root2=Toplevel(tk)
class WindowDraggable():

    def __init__(self, widget):
        self.widget = widget
        widget.bind('<ButtonPress-1>', self.StartMove)
        widget.bind('<ButtonRelease-1>', self.StopMove)
        widget.bind('<B1-Motion>', self.OnMotion)

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self,event):
        x = (event.x_root - self.x - self.widget.winfo_rootx() + self.widget.winfo_rootx())
        y = (event.y_root - self.y - self.widget.winfo_rooty() + self.widget.winfo_rooty())
        root.geometry("+%s+%s" % (x, y))

label = Label(root, text='drag me')
label2 = Text(root2)
label.pack()
label2.pack()
WindowDraggable(label)
WindowDraggable(label2)
root.overrideredirect(1)
root2.overrideredirect(1)
tk.mainloop()