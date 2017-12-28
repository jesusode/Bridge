


import Tkinter
import Tix
import ttk
root=Tkinter.Tk()



import tkmultilistbox

def onclick():
    print 'pulsado'

def onmenu():
    print 'se ha pulsado un menu!'

def callb(evt):
    print 'callback llamado!'

def combo_callb(evt):
    print 'callback del combo llamado!'



main=Tkinter.Toplevel(root)
frm1=Tkinter.Toplevel(root)
menubar=Tkinter.Menu(main)
main.config(menu=menubar)
archivo=Tkinter.Menu(menubar,tearoff=0)
archivo.add_command(label="Item 1",command=onmenu)
menubar.add_cascade(label="File",menu=archivo)
l1=Tkinter.Label(main,text="tralari")
l1.pack(fill="both")
b1=Tkinter.Button(main,text="pulsame",command=onclick)
b1.pack(fill="both")
t1=Tkinter.Entry(main,bg="red")
t1.pack(fill="both")
tabla = tkmultilistbox.MultiListbox(main,[["uno",20],["cinco",30],["nueve",50]])
tabla.pack()
cb1=ttk.Combobox(main,values=["uno","dos","tres","cuatro"])
cb1.pack(fill="both")
s1=Tkinter.Spinbox(main,from_=0,to=1000)
s1.pack(fill="both")
stv1=Tkinter.StringVar()
opt1=Tkinter.OptionMenu(main,stv1,"uno","dos","tres","cuatro")
opt1.pack(fill="both")
l1.bind("<Button-1>",callb)
cb1.bind("<<ComboboxSelected>>",combo_callb)
im1=Tkinter.PhotoImage(None,file="perros.gif")
l2=Tkinter.Label(frm1,text="el otro frame",image=im1,compound="bottom")
l2.pack(fill="both")


def init_code():
    global root,main,main,frm1,menubar,archivo,command,cascade,l1,b1,t1,tabla,cb1,s1,stv1,opt1,l1,cb1,im1,l2
    
    
    root.geometry("800x600")
    main.config(width=600,height=600)
    frm1.wm_title("A dog's life!")
    main.wm_title("Morpheus, are you Morpheus?")
    root.wm_title("Welcome to the real world!")
    for i in range(0,20000):
        tabla.insert("end",["valor " + str(i),"segundo "+ str(i),"tercero " + str(i)])
    
    
    

init_code()

root.mainloop()

