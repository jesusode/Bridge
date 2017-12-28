"""
@version: 0.96(2010-06-25)
@note:
EasyGui provides an easy-to-use interface for simple GUI interaction
with a user.  It does not require the programmer to know anything about
tkinter, frames, widgets, callbacks or lambda.  All GUI interactions are
invoked by simple function calls that return results.


@note:
WARNING about using EasyGui with IDLE

You may encounter problems using IDLE to run programs that use EasyGui. Try it
and find out.  EasyGui is a collection of Tkinter routines that run their own
event loops.  IDLE is also a Tkinter application, with its own event loop.  The
two may conflict, with unpredictable results. If you find that you have
problems, try running your EasyGui program outside of IDLE.

Note that EasyGui requires Tk release 8.0 or greater.
"""
egversion = __doc__.split()[1]

__all__ = ['ynbox'
    , 'ccbox'
    , 'boolbox'
    , 'indexbox'
    , 'msgbox'
    , 'buttonbox'
    , 'integerbox'
    , 'multenterbox'
    , 'enterbox'
    , 'exceptionbox'
    , 'choicebox'
    , 'codebox'
    , 'textbox'
    , 'diropenbox'
    , 'fileopenbox'
    , 'filesavebox'
    , 'passwordbox'
    , 'multpasswordbox'
    , 'multchoicebox'
    , 'abouteasygui'
    , 'egversion'
    , 'egdemo'
    , 'EgStore'
    ]

import sys, os, string, types, pickle,traceback
import pprint
#Opciones para que funcione con codigo Mini--------
#import Image as PILImage
#import ImageTk as PILImageTk
#import fnmatch
from Tables import *
from TableModels import *
#--------------------------------------------------


from Tkinter import *
import Tkinter
#from Tix import *
import tkFileDialog as tk_FileDialog
from StringIO import StringIO


#Mini
class TkScrolledCanvas:
    def __init__(self, master, **opts):
        if not opts.has_key('yscrollincrement'):
            opts['yscrollincrement'] = 17
        self.master = master
        self.frame = Frame(master)
        self.current_coords=[]
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.canvas = Canvas(self.frame, **opts)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vbar = Scrollbar(self.frame, name="vbar")
        self.vbar.grid(row=0, column=1, sticky="nse")
        self.hbar = Scrollbar(self.frame, name="hbar", orient="horizontal")
        self.hbar.grid(row=1, column=0, sticky="ews")
        self.canvas['yscrollcommand'] = self.vbar.set
        self.vbar['command'] = self.canvas.yview
        self.canvas['xscrollcommand'] = self.hbar.set
        self.hbar['command'] = self.canvas.xview
        self.canvas.bind("<Key-Prior>", self.page_up)
        self.canvas.bind("<Key-Next>", self.page_down)
        self.canvas.bind("<Key-Up>", self.unit_up)
        self.canvas.bind("<Key-Down>", self.unit_down)
        self.canvas.bind("<Key-Left>", self.unit_left)
        self.canvas.bind("<Key-Right>", self.unit_right)        
        #if isinstance(master, Toplevel) or isinstance(master, Tk):
        self.canvas.focus_set()
    def page_up(self, event):
        self.canvas.yview_scroll(-1, "page")
        return "break"
    def page_down(self, event):
        self.canvas.yview_scroll(1, "page")
        return "break"
    def unit_up(self, event):
        self.canvas.yview_scroll(-1, "unit")
        return "break"
    def unit_down(self, event):
        self.canvas.yview_scroll(1, "unit")
        return "break"
    def unit_left(self, event):
        self.canvas.xview_scroll(-1, "unit")
        return "break"
    def unit_right(self, event):
        self.canvas.xview_scroll(1, "unit")
        return "break"



def write(*args):
    args = [str(arg) for arg in args]
    args = " ".join(args)
    sys.stdout.write(args)

def writeln(*args):
    write(*args)
    sys.stdout.write("\n")

say = writeln
def dq(s):
    return '"%s"' % s

rootWindowPosition = "+300+200"

PROPORTIONAL_FONT_FAMILY = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY    = ("Courier")

PROPORTIONAL_FONT_SIZE  = 10
MONOSPACE_FONT_SIZE     =  9  #a little smaller, because it it more legible at a smaller size
TEXT_ENTRY_FONT_SIZE    = 12  # a little larger makes it easier to see

#STANDARD_SELECTION_EVENTS = ["Return", "Button-1"]
STANDARD_SELECTION_EVENTS = ["Return", "Button-1", "space"]

# Initialize some global variables that will be reset later
__choiceboxMultipleSelect = None
__widgetTexts = None
__replyButtonText = None
__choiceboxResults = None
__firstWidget = None
__enterboxText = None
__enterboxDefaultText=""
__multenterboxText = ""
choiceboxChoices = None
choiceboxWidget = None
entryWidget = None
boxRoot = None

#Variable que contiene el toplevel global
topmaster=None



#Flags Mini:
tk=None
#Permite texto multilinea
__large_text=0
#Mantiene abierto un buttonbox
__buttonbox_no_close=1


ImageErrorMsg = (
    "\n\n---------------------------------------------\n"
    "Error: %s\n%s")
#-------------------------------------------------------------------
# various boxes built on top of the basic buttonbox
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# ynbox
#-----------------------------------------------------------------------
def ynbox(msg="Shall I continue?"
    , title=" "
    , choices=("Yes", "No")
    , image=None
    , icon=None #Tuneado para soportar un icono
    ):
    return boolbox(msg, title, choices, image=image, noCode=1, icon=icon)


#-----------------------------------------------------------------------
# ccbox
#-----------------------------------------------------------------------
def ccbox(msg="Shall I continue?"
    , title=" "
    , choices=("Continue", "Cancel")
    , image=None
    ):
    """
    Display a msgbox with choices of Continue and Cancel.

    The default is "Continue".

    The returned value is calculated this way::
        if the first choice ("Continue") is chosen, or if the dialog is cancelled:
            return 1
        else:
            return 0

    If invoked without a msg argument, displays a generic request for a confirmation
    that the user wishes to continue.  So it can be used this way::

        if ccbox():
            pass # continue
        else:
            sys.exit(0)  # exit the program

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    return boolbox(msg, title, choices, image=image)


#-----------------------------------------------------------------------
# boolbox
#-----------------------------------------------------------------------
def boolbox(msg="Shall I continue?"
    , title=" "
    , choices=("Yes","No")
    , image=None
    , icon=None #Tuneado para soportar un icono
    , noCode=0 #Tuneado para permitir codigo y no codigo
    ):

    reply = buttonbox(msg=msg, choices=choices, title=title, image=image, icon=icon, noCode=noCode)
    #if reply == choices[0]: return 1
    #else: return 0
    return reply


#-----------------------------------------------------------------------
# indexbox
#-----------------------------------------------------------------------
def indexbox(msg="Shall I continue?"
    , title=" "
    , choices=("Yes","No")
    , image=None
    ):
    """
    Display a buttonbox with the specified choices.
    Return the index of the choice selected.
    """
    reply = buttonbox(msg=msg, choices=choices, title=title, image=image)
    index = -1
    for choice in choices:
        index = index + 1
        if reply == choice: return index
    raise AssertionError(
        "There is a program logic error in the EasyGui code for indexbox.")


#-----------------------------------------------------------------------
# msgbox
#-----------------------------------------------------------------------
def msgbox(msg="(Your message goes here)", title=" ", ok_button="OK",image=None,root=None, icon=None, noCode=1):
    """
    Display a messagebox
    """
    if type(ok_button) != type("OK"):
        raise AssertionError("The 'ok_button' argument to msgbox must be a string.")

    return buttonbox(msg=msg, title=title, choices=[ok_button], image=image,root=root,icon=icon, noCode=noCode)


#-------------------------------------------------------------------
# buttonbox
#-------------------------------------------------------------------
def buttonbox(msg="",title=" "
    ,choices=("Button1", "Button2", "Button3")
    , image=None
    , root=None
    , icon=None #Tuneado para poder poner un icono
    , vert=0  #Opcion para alinear en vertical los botones
    , code_opts={} #Diccionario opcion: codigo a ejecutar
    , default_code='' #Codigo por defecto
    , noCode=0 #Flag para que no se ejecute codigo
    ):
    """
    Display a msg, a title, and a set of buttons.
    The buttons are defined by the members of the choices list.
    Return the text of the button that the user selected.

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    global topmaster,boxRoot, __replyButtonText, __widgetTexts, buttonsFrame,__buttonbox_no_close,__buttonbox_codes, __noExec, __defaultCode

    #Pasar dicc de codigos a global:
    __buttonbox_codes=code_opts
    # Initialize __replyButtonText to the first choice.
    # This is what will be used if the window is closed by the close button.
    __replyButtonText = '' #choices[0]

    #Por defecto se ejecuta codigo-----------
    __noExec=0
    __defaultCode=default_code
    if noCode==1: __noExec=1
    #----------------------------------------
    

    if root:
        root.withdraw()
        boxRoot = Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = Tk()
        boxRoot.withdraw()
        topmaster=boxRoot
    #Para permitir una apariencia estandar-------------------------
    #El archivo de configuracion DEBE estar separado por caracteres de nueva linea!!!!
    #if os.path.exists(SYMTAB['__GUI_CONFIG__']):
    #    boxRoot.option_readfile (SYMTAB['__GUI_CONFIG__'])
    #--------------------------------------------------------------
        

    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(rootWindowPosition)
    boxRoot.minsize(400, 100)
    #Tuneado para poder poner un icono---------------------------
    if icon:
        boxRoot.wm_iconbitmap(icon)
    #------------------------------------------------------------

    # ------------- define the messageFrame ---------------------------------
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the imageFrame ---------------------------------


    tk_Image = None
    if image:
        imageFilename = os.path.normpath(image)
        junk,ext = os.path.splitext(imageFilename)

        if os.path.exists(imageFilename):
            if ext.lower() in [".gif", ".pgm", ".ppm"]:
                tk_Image = PhotoImage(file=imageFilename)
            else:
                try:
                    from PIL import Image   as PILImage
                    from PIL import ImageTk as PILImageTk
                    PILisLoaded = True
                except:
                    PILisLoaded = False

                if PILisLoaded:
                    try:
                        pil_Image = PILImage.open(imageFilename)
                        tk_Image = PILImageTk.PhotoImage(pil_Image)
                    except:
                        msg += ImageErrorMsg % (imageFilename,
                            "\nThe Python Imaging Library (PIL) could not convert this file to a displayable image."
                            "\n\nPIL reports:\n" + exception_format())

                else:  # PIL is not loaded
                    msg += ImageErrorMsg % (imageFilename,
                    "\nI could not import the Python Imaging Library (PIL) to display the image.\n\n"
                    "You may need to install PIL\n"
                    "(http://www.pythonware.com/products/pil/)\n"
                    "to display " + ext + " image files.")

        else:
            msg += ImageErrorMsg % (imageFilename, "\nImage file not found.")

    if tk_Image:
        imageFrame = Frame(master=boxRoot)
        imageFrame.pack(side=TOP, fill=BOTH)
        label = Label(imageFrame,image=tk_Image)
        label.image = tk_Image # keep a reference!
        label.pack(side=TOP, expand=YES, fill=X, padx='1m', pady='1m')

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)

    # -------------------- place the widgets in the frames -----------------------
    messageWidget = Message(messageFrame, text=msg, width=400)
    #messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=TOP, expand=YES, fill=X, padx='3m', pady='3m')
    __put_buttons_in_buttonframe(choices,vert=vert)

    # -------------- the action begins -----------
    # put the focus on the first button
    __firstWidget.focus_force()

    boxRoot.deiconify()
    boxRoot.mainloop()
    if root: root.deiconify()
    return __replyButtonText



def __buttonEvent(event):
    """
    HAY QUE CAMBIARLO TODO
    """
    global  topmaster, boxRoot, __widgetTexts, __replyButtonText, __buttonbox_codes, __noExec, __defaultCode,__buttonbox_no_close
    __replyButtonText = __widgetTexts[event.widget]
    if __replyButtonText=='Close':
        boxRoot.destroy() # quit the main loop
        topmaster=None
        return 'break'
    else: #Ejecutar codigo asociado al boton o devolver texto del boton si __noExec
        if __buttonbox_codes and __noExec==0:
            #print 'Codigo a ejecutar: %s' % code
            #__buttonbox_codes[event
            __buttonbox_codes[event.widget.config('text')[-1]](event)
        if __noExec:
            boxRoot.quit()
            #boxRoot.destroy()
            __buttonbox_no_close=0
            topmaster=None
        return 'break'


def __put_buttons_in_buttonframe(choices,vert=0):
    """Put the buttons in the buttons frame
    """
    global __widgetTexts, __firstWidget, buttonsFrame, __noExec

    __firstWidget = None
    __widgetTexts = {}

    i = 0
    for buttonText in choices:
        tempButton = Button(buttonsFrame, takefocus=1, text=buttonText)
        bindArrows(tempButton)
        if vert==0:
            tempButton.pack(expand=YES, side=LEFT, fill=X, padx='1m', pady='1m', ipadx='2m', ipady='1m')
        else:
            tempButton.pack(expand=YES, side=TOP, fill=X, padx='1m', pady='1m', ipadx='2m', ipady='1m')

        # remember the text associated with this widget
        __widgetTexts[tempButton] = buttonText

        # remember the first widget, so we can put the focus there
        if i == 0:
            __firstWidget = tempButton
            i = 1

        # for the commandButton, bind activation events to the activation event handler
        commandButton  = tempButton
        handler = __buttonEvent
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind("<%s>" % selectionEvent, handler)


    if __noExec==0: #Poner boton Close solo si se quiere ejecutar codigo
        closeButton = Button(buttonsFrame, takefocus=1, text='Close')
        #hideButton = Button(buttonsFrame, takefocus=1, text='Hide')
        if vert==0:
            closeButton.pack(expand=YES, side=LEFT, fill=X, padx='1m', pady='1m', ipadx='2m', ipady='1m')
            #hideButton.pack(expand=YES, side=LEFT, fill=X, padx='1m', pady='1m', ipadx='2m', ipady='1m')
        else:
            closeButton.pack(expand=YES, side=TOP, fill=X, padx='1m', pady='1m', ipadx='2m', ipady='1m')
            #hideButton.pack(expand=YES, side=LEFT, fill=X, padx='1m', pady='1m', ipadx='2m', ipady='1m')
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            closeButton.bind("<%s>" % selectionEvent, handler)
            #hideButton.bind("<%s>" % selectionEvent, handler)
        __widgetTexts[closeButton] = 'Close'
        #__widgetTexts[hideButton]='Hide'



#-------------------------------------------------------------------
# integerbox
#-------------------------------------------------------------------
def integerbox(msg=""
    , title=" "
    , default=""
    , lowerbound=0
    , upperbound=99
    , real= 0 #Tuneado para permitir un float
    , image = None
    , root  = None
    , icon = None #Tuneado para permitir un icono
    , **invalidKeywordArguments
    ):
    """
    Show a box in which a user can enter an integer.

    In addition to arguments for msg and title, this function accepts
    integer arguments for "default", "lowerbound", and "upperbound".

    The default argument may be None.

    When the user enters some text, the text is checked to verify that it
    can be converted to an integer between the lowerbound and upperbound.

    If it can be, the integer (not the text) is returned.

    If it cannot, then an error msg is displayed, and the integerbox is
    redisplayed.

    If the user cancels the operation, None is returned.

    NOTE that the "argLowerBound" and "argUpperBound" arguments are no longer
    supported.  They have been replaced by "upperbound" and "lowerbound".
    """
    if "argLowerBound" in invalidKeywordArguments:
        raise AssertionError(
            "\nintegerbox no longer supports the 'argLowerBound' argument.\n"
            + "Use 'lowerbound' instead.\n\n")
    if "argUpperBound" in invalidKeywordArguments:
        raise AssertionError(
            "\nintegerbox no longer supports the 'argUpperBound' argument.\n"
            + "Use 'upperbound' instead.\n\n")

    if default != "":
        if type(default) != type(1):
            raise AssertionError(
                "integerbox received a non-integer value for "
                + "default of " + dq(str(default)) , "Error")

    if type(lowerbound) != type(1):
        raise AssertionError(
            "integerbox received a non-integer value for "
            + "lowerbound of " + dq(str(lowerbound)) , "Error")

    if type(upperbound) != type(1):
        raise AssertionError(
            "integerbox received a non-integer value for "
            + "upperbound of " + dq(str(upperbound)) , "Error")

    if msg == "":
        msg = ("Enter an integer between " + str(lowerbound)
            + " and "
            + str(upperbound)
            )

    while 1:
        reply = enterbox(msg, title, str(default), image=image, root=root, icon=icon)
        if reply == None: return None

        try:
            reply=float(reply)
            if not real:#Tuneado para permitir un float
                reply = int(reply)
        except:
            msgbox ("The value that you entered:\n\t%s\nis not an number." % dq(str(reply))
                    , "Error")
            continue

        if reply < lowerbound:
            msgbox ("The value that you entered is less than the lower bound of "
                + str(lowerbound) + ".", "Error")
            continue

        if reply > upperbound:
            msgbox ("The value that you entered is greater than the upper bound of "
                + str(upperbound) + ".", "Error")
            continue

        # reply has passed all validation checks.
        # It is an integer between the specified bounds.
        return reply

#-------------------------------------------------------------------
# multenterbox
#-------------------------------------------------------------------
def multenterbox(msg="Fill in values for the fields."
    , title=" "
    , fields=()
    , values=()
    , icon=None #Tuneado para permitir un icono
    , large_text=0                 
    ):
    r"""
    Show screen with multiple data entry fields.

    If there are fewer values than names, the list of values is padded with
    empty strings until the number of values is the same as the number of names.

    If there are more values than names, the list of values
    is truncated so that there are as many values as names.

    Returns a list of the values of the fields,
    or None if the user cancels the operation.

    Here is some example code, that shows how values returned from
    multenterbox can be checked for validity before they are accepted::
        ----------------------------------------------------------------------
        msg = "Enter your personal information"
        title = "Credit Card Application"
        fieldNames = ["Name","Street Address","City","State","ZipCode"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multenterbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg += ('"%s" is a required field.\n\n' % fieldNames[i])
            if errmsg == "":
                break # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

        writeln("Reply was: %s" % str(fieldValues))
        ----------------------------------------------------------------------

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg fields: a list of fieldnames.
    @arg values:  a list of field values
    """
    return __multfillablebox(msg,title,fields,values,None,icon,large_text)


#-----------------------------------------------------------------------
# multpasswordbox
#-----------------------------------------------------------------------
def multpasswordbox(msg="Fill in values for the fields."
    , title=" "
    , fields=tuple()
    ,values=tuple()
    , icon=None #Tuneado para permitir un icono
    , large_text=0                    
    ):
    r"""
    Same interface as multenterbox.  But in multpassword box,
    the last of the fields is assumed to be a password, and
    is masked with asterisks.

    Example
    =======

    Here is some example code, that shows how values returned from
    multpasswordbox can be checked for validity before they are accepted::
        msg = "Enter logon information"
        title = "Demo of multpasswordbox"
        fieldNames = ["Server ID", "User ID", "Password"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multpasswordbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
                if errmsg == "": break # no problems found
            fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)

        writeln("Reply was: %s" % str(fieldValues))
    """
    return __multfillablebox(msg,title,fields,values,"*",icon,large_text)

def bindArrows(widget):
    widget.bind("<Down>", tabRight)
    widget.bind("<Up>"  , tabLeft)

    widget.bind("<Right>",tabRight)
    widget.bind("<Left>" , tabLeft)

def tabRight(event):
    boxRoot.event_generate("<Tab>")

def tabLeft(event):
    boxRoot.event_generate("<Shift-Tab>")

#-----------------------------------------------------------------------
# __multfillablebox
#-----------------------------------------------------------------------
def __multfillablebox(msg="Fill in values for the fields."
    , title=" "
    , fields=()
    , values=()
    , mask = None
    , icon= None #Tuneado para permitir un icono
    , large_text=0
    ):
    global boxRoot, __multenterboxText, __multenterboxDefaultText, cancelButton, entryWidget, okButton, scwin

    choices = ["OK", "Cancel"]
    if len(fields) == 0: return None

    fields = list(fields[:])  # convert possible tuples to a list
    values = list(values[:])  # convert possible tuples to a list

    if   len(values) == len(fields): pass
    elif len(values) >  len(fields):
        fields = fields[0:len(values)]
    else:
        while len(values) < len(fields):
            values.append("")

    boxRoot = Tk()
    
    #Para permitir una apariencia estandar-------------------------
    #El archivo de configuracion DEBE estar separado por caracteres de nueva linea!!!!
    #if os.path.exists(SYMTAB['__GUI_CONFIG__']):
    #    boxRoot.option_readfile (SYMTAB['__GUI_CONFIG__'])
    #--------------------------------------------------------------
    

    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(rootWindowPosition)
    #Tuneado para poder poner un icono---------------------------
    if icon:
        boxRoot.wm_iconbitmap(icon)
    #------------------------------------------------------------
    boxRoot.bind("<Escape>", __multenterboxCancel)

    scwin=TkScrolledCanvas(boxRoot)
    scwin.frame.pack(expand=YES, fill=BOTH)
    #masterFrameWin=Frame(boxRoot)
    masterFrameWin=Frame(scwin.canvas)
    scwin.canvas.create_window(0, 0, window=masterFrameWin, anchor="nw")
    #masterFrameWin.pack()

    # -------------------- put subframes in the boxRoot --------------------
    #messageFrame = Frame(master=boxRoot)
    messageFrame = Frame(masterFrameWin)
    messageFrame.pack(side=TOP, fill=BOTH)

    #-------------------- the msg widget ----------------------------
    messageWidget = Message(messageFrame,text=msg)#, width="4.5i", )
    #messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=RIGHT, expand=1, fill=BOTH, padx='3m', pady='3m')

    global entryWidgets,__large_text
    entryWidgets = []

    lastWidgetIndex = len(fields) - 1

    for widgetIndex in range(len(fields)):
        argFieldName  = fields[widgetIndex]
        argFieldValue = values[widgetIndex]
        #entryFrame = Frame(master=boxRoot)
        entryFrame = Frame(masterFrameWin)
        entryFrame.pack(side=TOP, fill=BOTH)

        # --------- entryWidget ----------------------------------------------
        labelWidget = Label(entryFrame, text=argFieldName)
        labelWidget.pack(side=LEFT)
        entryWidget=None
        if large_text==0:
            entryWidget = Entry(entryFrame, width=40)
        else:
           entryWidget = Text(entryFrame, width=40, height=3)
           __large_text=1
        entryWidgets.append(entryWidget)
        entryWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,TEXT_ENTRY_FONT_SIZE))
        entryWidget.pack(side=RIGHT, padx="3m")

        bindArrows(entryWidget)
        if large_text==0:
            entryWidget.bind("<Return>", __multenterboxGetText)
        entryWidget.bind("<Escape>", __multenterboxCancel)

        # for the last entryWidget, if this is a multpasswordbox,
        # show the contents as just asterisks
        if widgetIndex == lastWidgetIndex:
            if mask:
                if large_text==0:
                    entryWidgets[widgetIndex].configure(show=mask)

        # put text into the entryWidget
        if large_text==0:
            entryWidgets[widgetIndex].insert(0,argFieldValue)
        else:
            entryWidgets[widgetIndex].insert(END,argFieldValue, "normal")
        widgetIndex += 1       

    # ------------------ ok button -------------------------------
    #buttonsFrame = Frame(master=boxRoot)
    buttonsFrame = Frame(masterFrameWin)
    buttonsFrame.pack(side=BOTTOM, fill=BOTH)

    okButton = Button(buttonsFrame, takefocus=1, text="OK")
    bindArrows(okButton)
    okButton.pack(expand=1, side=LEFT, fill=X, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = okButton
    handler = __multenterboxGetText
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)


    # ------------------ cancel button -------------------------------
    cancelButton = Button(buttonsFrame, takefocus=1, text="Cancel")
    bindArrows(cancelButton)
    cancelButton.pack(expand=1, side=RIGHT, fill=X, padx='3m', pady='3m', ipadx='2m', ipady='1m')


    # for the commandButton, bind activation events to the activation event handler
    commandButton  = cancelButton
    handler = __multenterboxCancel
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)

    # ------------------- time for action! -----------------
    entryWidgets[0].focus_force()    # put the focus on the entryWidget
    #Habilitar scroll si se necesita
    masterFrameWin.bind("<Configure>", configureFORM)
    boxRoot.mainloop()  # run it!

    # -------- after the run has completed ----------------------------------
    boxRoot.destroy()  # button_click didn't destroy boxRoot, so we do it now
    return __multenterboxText

def configureFORM(event):
    global scwin
    region=(0,0,event.width,event.height)
    scwin.canvas.config(scrollregion=region)

#-----------------------------------------------------------------------
# __multenterboxGetText
#-----------------------------------------------------------------------
def __multenterboxGetText(event):
    global __multenterboxText,__large_text

    __multenterboxText = []
    for entryWidget in entryWidgets:
        if __large_text==0:
            __multenterboxText.append(entryWidget.get())
        else:
            __multenterboxText.append(entryWidget.get(0.0,END))
    boxRoot.quit()


def __multenterboxCancel(event):
    global __multenterboxText
    __multenterboxText = None
    boxRoot.quit()


#-------------------------------------------------------------------
# enterbox
#-------------------------------------------------------------------
def enterbox(msg="Enter something."
    , title=" "
    , default=""
    , strip=True
    , image=None
    , root=None
    , icon=None #Tuneado para permitir un icono
    ):
    """
    Show a box in which a user can enter some text.

    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.

    Returns the text that the user entered, or None if he cancels the operation.

    By default, enterbox strips its result (i.e. removes leading and trailing
    whitespace).  (If you want it not to strip, use keyword argument: strip=False.)
    This makes it easier to test the results of the call::

        reply = enterbox(....)
        if reply:
            ...
        else:
            ...
    """
    result = __fillablebox(msg, title, default=default, mask=None,image=image,root=root,icon=icon)
    if result and strip:
        result = result.strip()
    return result


def passwordbox(msg="Enter your password."
    , title=" "
    , default=""
    , image=None
    , root=None
    , icon=None
    ):
    """
    Show a box in which a user can enter a password.
    The text is masked with asterisks, so the password is not displayed.
    Returns the text that the user entered, or None if he cancels the operation.
    """
    return __fillablebox(msg, title, default, mask="*",image=image,root=root,icon=icon)


def __fillablebox(msg
    , title=""
    , default=""
    , mask=None
    , image=None
    , root=None
    , icon=None #Tuneado para permitir un icono
    ):
    """
    Show a box in which a user can enter some text.
    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.
    Returns the text that the user entered, or None if he cancels the operation.
    """

    global boxRoot, __enterboxText, __enterboxDefaultText
    global cancelButton, entryWidget, okButton

    if title == None: title == ""
    if default == None: default = ""
    __enterboxDefaultText = default
    __enterboxText        = __enterboxDefaultText

    if root:
        root.withdraw()
        boxRoot = Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = Tk()
        boxRoot.withdraw()
    #Para permitir una apariencia estandar-------------------------
    #El archivo de configuracion DEBE estar separado por caracteres de nueva linea!!!!
    #if os.path.exists(SYMTAB['__GUI_CONFIG__']):
    #    boxRoot.option_readfile (SYMTAB['__GUI_CONFIG__'])
    #--------------------------------------------------------------
        

    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(rootWindowPosition)
    boxRoot.bind("<Escape>", __enterboxCancel)
    #Tuneado para poder poner un icono---------------------------
    if icon:
        boxRoot.wm_iconbitmap(icon)
    #------------------------------------------------------------

    if image:
        image = os.path.normpath(image)
        junk,ext = os.path.splitext(image)
        if ext.lower() == ".gif":
            if os.path.exists(image):
                pass
            else:
                msg += ImageErrorMsg % (image, "Image file not found.")
                image = None
        else:
            msg += ImageErrorMsg % (image, "Image file is not a .gif file.")
            image = None
    # ------------- define the messageFrame ---------------------------------
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the imageFrame ---------------------------------
    if image:
        imageFrame = Frame(master=boxRoot)
        imageFrame.pack(side=TOP, fill=BOTH)
        image = PhotoImage(file=image)
        label = Label(imageFrame,image=image)
        label.image = image # keep a reference!
        label.pack(side=TOP, expand=YES, fill=X, padx='1m', pady='1m')

    # ------------- define the entryFrame ---------------------------------
    entryFrame = Frame(master=boxRoot)
    entryFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)

    #-------------------- the msg widget ----------------------------
    messageWidget = Message(messageFrame,  text=msg)#width="4.5i",
    #messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=RIGHT, expand=1, fill=BOTH, padx='3m', pady='3m')

    # --------- entryWidget ----------------------------------------------
    entryWidget = Entry(entryFrame, width=40)
    bindArrows(entryWidget)
    entryWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,TEXT_ENTRY_FONT_SIZE))
    if mask:
        entryWidget.configure(show=mask)
    entryWidget.pack(side=LEFT, padx="3m")
    entryWidget.bind("<Return>", __enterboxGetText)
    entryWidget.bind("<Escape>", __enterboxCancel)
    # put text into the entryWidget
    entryWidget.insert(0,__enterboxDefaultText)

    # ------------------ ok button -------------------------------
    okButton = Button(buttonsFrame, takefocus=1, text="OK")
    bindArrows(okButton)
    okButton.pack(expand=1, side=LEFT, fill=X, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = okButton
    handler = __enterboxGetText
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)


    # ------------------ cancel button -------------------------------
    cancelButton = Button(buttonsFrame, takefocus=1, text="Cancel")
    bindArrows(cancelButton)
    cancelButton.pack(expand=1, side=RIGHT, fill=X, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = cancelButton
    handler = __enterboxCancel
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)

    # ------------------- time for action! -----------------
    entryWidget.focus_force()    # put the focus on the entryWidget
    boxRoot.deiconify()
    boxRoot.mainloop()  # run it!

    # -------- after the run has completed ----------------------------------
    if root: root.deiconify()
    boxRoot.destroy()  # button_click didn't destroy boxRoot, so we do it now
    return __enterboxText


def __enterboxGetText(event):
    global __enterboxText
    __enterboxText = entryWidget.get()
    boxRoot.quit()


def __enterboxRestore(event):
    global entryWidget
    entryWidget.delete(0,len(entryWidget.get()))
    entryWidget.insert(0, __enterboxDefaultText)


def __enterboxCancel(event):
    global __enterboxText
    __enterboxText = None
    boxRoot.quit()

def denyWindowManagerClose():
    """ don't allow WindowManager close
    """
    x = Tk()
    x.withdraw()
    x.bell()
    x.destroy()



#-------------------------------------------------------------------
# multchoicebox
#-------------------------------------------------------------------
def multchoicebox(msg="Pick as many items as you like."
    , title=" "
    , choices=()
    , icon=None
    , width=300
    , height=300
    , **kwargs
    ):
    """
    Present the user with a list of choices.
    allow him to select multiple items and return them in a list.
    if the user doesn't choose anything from the list, return the empty list.
    return None if he cancelled selection.

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    if len(choices) == 0: choices = ["Program logic error - no choices were specified."]

    global __choiceboxMultipleSelect
    __choiceboxMultipleSelect = 1
    return __choicebox(msg, title, choices, icon, width, height)


#-----------------------------------------------------------------------
# choicebox
#-----------------------------------------------------------------------
def choicebox(msg="Pick something."
    , title=" "
    , choices=()
    , icon=None
    , width=300
    , height=300
    ):
    """
    Present the user with a list of choices.
    return the choice that he selects.
    return None if he cancels the selection selection.

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    if len(choices) == 0: choices = ["Program logic error - no choices were specified."]

    global __choiceboxMultipleSelect
    __choiceboxMultipleSelect = 0
    return __choicebox(msg,title,choices, icon, width, height)


#-----------------------------------------------------------------------
# __choicebox
#-----------------------------------------------------------------------
def __choicebox(msg
    , title
    , choices
    , icon=None
    , width=None
    , height=None
    ):
    """
    internal routine to support choicebox() and multchoicebox()
    """
    global boxRoot, __choiceboxResults, choiceboxWidget, defaultText
    global choiceboxWidget, choiceboxChoices
    #-------------------------------------------------------------------
    # If choices is a tuple, we make it a list so we can sort it.
    # If choices is already a list, we make a new list, so that when
    # we sort the choices, we don't affect the list object that we
    # were given.
    #-------------------------------------------------------------------
    choices = list(choices[:])
    if len(choices) == 0:
        choices = ["Program logic error - no choices were specified."]
    defaultButtons = ["OK", "Cancel"]

    # make sure all choices are strings
    for index in range(len(choices)):
        choices[index] = str(choices[index])

    #lines_to_show = min(len(choices), 20)
    #lines_to_show = 20
    lines_to_show =len(choices)

    if title == None: title = ""

    # Initialize __choiceboxResults
    # This is the value that will be returned if the user clicks the close icon
    __choiceboxResults = None

    boxRoot = Tk()
    #Para permitir una apariencia estandar-------------------------
    #El archivo de configuracion DEBE estar separado por caracteres de nueva linea!!!!
    #if os.path.exists(SYMTAB['__GUI_CONFIG__']):
    #    boxRoot.option_readfile (SYMTAB['__GUI_CONFIG__'])
    #--------------------------------------------------------------
    
    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    screen_width  = boxRoot.winfo_screenwidth()
    screen_height = boxRoot.winfo_screenheight()
    root_width    = int((screen_width * 0.8))
    #Tuneado para controlar width--------------------------------    
    if width:
        root_width=int(width)
    #------------------------------------------------------------         
    root_height   = int((screen_height * 0.5))
    #Tuneado para controlar heigth-------------------------------    
    if height:
        root_height=int(height)
    #------------------------------------------------------------             
    root_xpos     = int((screen_width * 0.1))
    root_ypos     = int((screen_height * 0.05))

    boxRoot.title(title)
    #Tuneado para poder poner un icono---------------------------
    if icon:
        boxRoot.wm_iconbitmap(icon)
    #------------------------------------------------------------        
    boxRoot.iconname('Dialog')
    rootWindowPosition = "+0+0"
    boxRoot.geometry(rootWindowPosition)
    boxRoot.expand=NO
    boxRoot.minsize(root_width, root_height)
    rootWindowPosition = "+" + str(root_xpos) + "+" + str(root_ypos)
    boxRoot.geometry(rootWindowPosition)

    # ---------------- put the frames in the window -----------------------------------------
    message_and_buttonsFrame = Frame(master=boxRoot)
    message_and_buttonsFrame.pack(side=TOP, fill=X, expand=NO)

    messageFrame = Frame(message_and_buttonsFrame)
    messageFrame.pack(side=LEFT, fill=X, expand=YES)
    #messageFrame.pack(side=TOP, fill=X, expand=YES)

    buttonsFrame = Frame(message_and_buttonsFrame)
    buttonsFrame.pack(side=RIGHT, expand=NO, pady=0)
    #buttonsFrame.pack(side=TOP, expand=YES, pady=0)

    choiceboxFrame = Frame(master=boxRoot)
    choiceboxFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)

    # -------------------------- put the widgets in the frames ------------------------------

    # ---------- put a msg widget in the msg frame-------------------
    messageWidget = Message(messageFrame, anchor=NW, text=msg, width=int(root_width * 0.9))
    #messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=LEFT, expand=YES, fill=BOTH, padx='1m', pady='1m')

    # --------  put the choiceboxWidget in the choiceboxFrame ---------------------------
    choiceboxWidget = Listbox(choiceboxFrame
        , height=lines_to_show
        #, borderwidth="1m"
        #, relief="flat"
        #, bg="white"
        )

    if __choiceboxMultipleSelect:
        choiceboxWidget.configure(selectmode=MULTIPLE)

    #choiceboxWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))

    # add a vertical scrollbar to the frame
    rightScrollbar = Scrollbar(choiceboxFrame, orient=VERTICAL, command=choiceboxWidget.yview)
    choiceboxWidget.configure(yscrollcommand = rightScrollbar.set)

    # add a horizontal scrollbar to the frame
    bottomScrollbar = Scrollbar(choiceboxFrame, orient=HORIZONTAL, command=choiceboxWidget.xview)
    choiceboxWidget.configure(xscrollcommand = bottomScrollbar.set)

    # pack the Listbox and the scrollbars.  Note that although we must define
    # the textArea first, we must pack it last, so that the bottomScrollbar will
    # be located properly.

    bottomScrollbar.pack(side=BOTTOM, fill = X)
    rightScrollbar.pack(side=RIGHT, fill = Y)

    choiceboxWidget.pack(side=LEFT, padx="1m", pady="1m", expand=YES, fill=BOTH)

    #---------------------------------------------------
    # sort the choices
    # eliminate duplicates
    # put the choices into the choiceboxWidget
    #---------------------------------------------------
    for index in range(len(choices)):
        choices[index] == str(choices[index])

##    if runningPython3:
##        choices.sort(key=str.lower)
##    else:
    choices.sort( lambda x,y: cmp(x.lower(),    y.lower())) # case-insensitive sort

    lastInserted = None
    choiceboxChoices = []
    for choice in choices:
        if choice == lastInserted: pass
        else:
            choiceboxWidget.insert(END, choice)
            choiceboxChoices.append(choice)
            lastInserted = choice

    boxRoot.bind('<Any-Key>', KeyboardListener)

    # put the buttons in the buttonsFrame
    if len(choices) > 0:
        okButton = Button(buttonsFrame, takefocus=YES, text="OK", height=1, width=6)
        bindArrows(okButton)
        okButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")

        # for the commandButton, bind activation events to the activation event handler
        commandButton  = okButton
        handler = __choiceboxGetChoice
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind("<%s>" % selectionEvent, handler)

        # now bind the keyboard events
        choiceboxWidget.bind("<Return>", __choiceboxGetChoice)
        choiceboxWidget.bind("<Double-Button-1>", __choiceboxGetChoice)
    else:
        # now bind the keyboard events
        choiceboxWidget.bind("<Return>", __choiceboxCancel)
        choiceboxWidget.bind("<Double-Button-1>", __choiceboxCancel)

    cancelButton = Button(buttonsFrame, takefocus=YES, text="Cancel", height=1, width=6)
    bindArrows(cancelButton)
    cancelButton.pack(expand=NO, side=LEFT, padx='2m', pady='1m', ipady="1m", ipadx="2m")

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = cancelButton
    handler = __choiceboxCancel
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)


    # add special buttons for multiple select features
    if len(choices) > 0 and __choiceboxMultipleSelect:
        selectionButtonsFrame = Frame(messageFrame)
        selectionButtonsFrame.pack(side=RIGHT, fill=Y, expand=NO)

        selectAllButton = Button(selectionButtonsFrame, text="Select All", height=1, width=6)
        bindArrows(selectAllButton)

        selectAllButton.bind("<Button-1>",__choiceboxSelectAll)
        selectAllButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")

        clearAllButton = Button(selectionButtonsFrame, text="Clear All", height=1, width=6)
        bindArrows(clearAllButton)
        clearAllButton.bind("<Button-1>",__choiceboxClearAll)
        clearAllButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")


    # -------------------- bind some keyboard events ----------------------------
    boxRoot.bind("<Escape>", __choiceboxCancel)

    # --------------------- the action begins -----------------------------------
    # put the focus on the choiceboxWidget, and the select highlight on the first item
    choiceboxWidget.select_set(0)
    choiceboxWidget.focus_force()

    # --- run it! -----
    boxRoot.mainloop()

    boxRoot.destroy()
    return __choiceboxResults


def __choiceboxGetChoice(event):
    global boxRoot, __choiceboxResults, choiceboxWidget

    if __choiceboxMultipleSelect:
        __choiceboxResults = [choiceboxWidget.get(index) for index in choiceboxWidget.curselection()]

    else:
        choice_index = choiceboxWidget.curselection()
        __choiceboxResults = choiceboxWidget.get(choice_index)

    # writeln("Debugging> mouse-event=", event, " event.type=", event.type)
    # writeln("Debugging> choice=", choice_index, __choiceboxResults)
    boxRoot.quit()


def __choiceboxSelectAll(event):
    global choiceboxWidget, choiceboxChoices
    choiceboxWidget.selection_set(0, len(choiceboxChoices)-1)

def __choiceboxClearAll(event):
    global choiceboxWidget, choiceboxChoices
    choiceboxWidget.selection_clear(0, len(choiceboxChoices)-1)



def __choiceboxCancel(event):
    global boxRoot, __choiceboxResults

    __choiceboxResults = None
    boxRoot.quit()


def KeyboardListener(event):
    global choiceboxChoices, choiceboxWidget
    key = event.keysym
    if len(key) <= 1:
        if key in string.printable:
            # Find the key in the list.
            # before we clear the list, remember the selected member
            try:
                start_n = int(choiceboxWidget.curselection()[0])
            except IndexError:
                start_n = -1

            ## clear the selection.
            choiceboxWidget.selection_clear(0, 'end')

            ## start from previous selection +1
            for n in range(start_n+1, len(choiceboxChoices)):
                item = choiceboxChoices[n]
                if item[0].lower() == key.lower():
                    choiceboxWidget.selection_set(first=n)
                    choiceboxWidget.see(n)
                    return
            else:
                # has not found it so loop from top
                for n in range(len(choiceboxChoices)):
                    item = choiceboxChoices[n]
                    if item[0].lower() == key.lower():
                        choiceboxWidget.selection_set(first = n)
                        choiceboxWidget.see(n)
                        return

                # nothing matched -- we'll look for the next logical choice
                for n in range(len(choiceboxChoices)):
                    item = choiceboxChoices[n]
                    if item[0].lower() > key.lower():
                        if n > 0:
                            choiceboxWidget.selection_set(first = (n-1))
                        else:
                            choiceboxWidget.selection_set(first = 0)
                        choiceboxWidget.see(n)
                        return

                # still no match (nothing was greater than the key)
                # we set the selection to the first item in the list
                lastIndex = len(choiceboxChoices)-1
                choiceboxWidget.selection_set(first = lastIndex)
                choiceboxWidget.see(lastIndex)
                return

#-----------------------------------------------------------------------
# exception_format
#-----------------------------------------------------------------------
def exception_format():
    """
    Convert exception info into a string suitable for display.
    """
    return "".join(traceback.format_exception(
           sys.exc_info()[0]
        ,  sys.exc_info()[1]
        ,  sys.exc_info()[2]
        ))

#-----------------------------------------------------------------------
# exceptionbox
#-----------------------------------------------------------------------
def exceptionbox(msg=None, title=None):
    """
    Display a box that gives information about
    an exception that has just been raised.

    The caller may optionally pass in a title for the window, or a
    msg to accompany the error information.

    Note that you do not need to (and cannot) pass an exception object
    as an argument.  The latest exception will automatically be used.
    """
    if title == None: title = "Error Report"
    if msg == None:
        msg = "An error (exception) has occurred in the program."

    codebox(msg, title, exception_format())

#-------------------------------------------------------------------
# codebox
#-------------------------------------------------------------------

def codebox(msg=""
    , title=" "
    , text=""
    ):
    """
    Display some text in a monospaced font, with no line wrapping.
    This function is suitable for displaying code and text that is
    formatted using spaces.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.
    """
    return textbox(msg, title, text, codebox=1 )

#-------------------------------------------------------------------
# textbox
#-------------------------------------------------------------------
def textbox(msg=""
    , title=" "
    , text=""
    , edit=1
    , font=''
    , color=None
    , bgcolor=None
    , icon=None
    , width=None
    , height=None
    , showfiles=0
    , codebox=0
    ):
    """
    Display some text in a proportional font with line wrapping at word breaks.
    This function is suitable for displaying general written text.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.
    """

    if msg == None: msg = ""
    if title == None: title = ""

    global boxRoot, __replyButtonText, __widgetTexts, buttonsFrame
    global rootWindowPosition,textArea
    choices = ["OK","Hide","Save","Load"]
    __replyButtonText = choices[0]


    boxRoot = Tk()
    
    #Para permitir una apariencia estandar-------------------------
    #El archivo de configuracion DEBE estar separado por caracteres de nueva linea!!!!
    #if os.path.exists(SYMTAB['__GUI_CONFIG__']):
    #    boxRoot.option_readfile (SYMTAB['__GUI_CONFIG__'])
    #--------------------------------------------------------------

    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )

    screen_width = boxRoot.winfo_screenwidth()
    screen_height = boxRoot.winfo_screenheight()
    root_width = int((screen_width * 0.8))
    #Tuneado para controlar width--------------------------------    
    if width:
        root_width=int(width)
    #------------------------------------------------------------           
    root_height = int((screen_height * 0.5))
    #Tuneado para controlar heigth-------------------------------    
    if height:
        root_height=int(height)
    #------------------------------------------------------------           
    root_xpos = int((screen_width * 0.1))
    root_ypos = int((screen_height * 0.05))

    boxRoot.title(title)
    #Tuneado para poder poner un icono---------------------------
    if icon:
        boxRoot.wm_iconbitmap(icon)
    #------------------------------------------------------------         
    boxRoot.iconname('Dialog')
    rootWindowPosition = "+0+0"
    boxRoot.geometry(rootWindowPosition)
    boxRoot.expand=NO
    #boxRoot.minsize(root_width, root_height)
    rootWindowPosition = "+" + str(root_xpos) + "+" + str(root_ypos)
    boxRoot.geometry(rootWindowPosition)

    mainframe = Frame(master=boxRoot)
    mainframe.pack(side=TOP, fill=BOTH, expand=YES)

    # ----  put frames in the window -----------------------------------
##    # we pack the textboxFrame first, so it will expand first
##    textboxFrame = Frame(mainframe, borderwidth=3)
##    textboxFrame.pack(side=BOTTOM , fill=BOTH, expand=YES)

    message_and_buttonsFrame = Frame(mainframe)
    message_and_buttonsFrame.pack(side=TOP, fill=X, expand=NO)

    messageFrame = Frame(message_and_buttonsFrame)
    messageFrame.pack(side=LEFT, fill=X, expand=YES)

    buttonsFrame = Frame(message_and_buttonsFrame)
    buttonsFrame.pack(side=RIGHT, expand=NO)

    textboxFrame = Frame(mainframe, borderwidth=3)
    textboxFrame.pack(side=BOTTOM , fill=BOTH, expand=YES)

    # -------------------- put widgets in the frames --------------------

    # put a textArea in the top frame
    if codebox:
        character_width = int((root_width * 0.6) / MONOSPACE_FONT_SIZE)
        textArea = Text(textboxFrame,height=25,width=character_width, padx="2m", pady="1m")
        textArea.configure(wrap=NONE)
        textArea.configure(font=(MONOSPACE_FONT_FAMILY, MONOSPACE_FONT_SIZE))

    else:
        character_width = int((root_width * 0.6) / MONOSPACE_FONT_SIZE)
        textArea = Text(
            textboxFrame
            , height=5
            #, width=character_width
            , padx="2m"
            , pady="1m"
            )
        textArea.configure(wrap=WORD)
        textArea.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
        
        #Fuente a utilizar-------------------------------------------------------
        if font:
            textArea.configure(font=font)
        #------------------------------------------------------------------------

        #Color de Fuente---------------------------------------------------------
        if color:
            textArea.configure(fg=color)
        #------------------------------------------------------------------------

        #Color de fondo----------------------------------------------------------
        if bgcolor:
            textArea.configure(bg=bgcolor)
        #------------------------------------------------------------------------            


    # some simple keybindings for scrolling
    mainframe.bind("<Next>" , textArea.yview_scroll( 1,PAGES))
    mainframe.bind("<Prior>", textArea.yview_scroll(-1,PAGES))

    mainframe.bind("<Right>", textArea.xview_scroll( 1,PAGES))
    mainframe.bind("<Left>" , textArea.xview_scroll(-1,PAGES))

    mainframe.bind("<Down>", textArea.yview_scroll( 1,UNITS))
    mainframe.bind("<Up>"  , textArea.yview_scroll(-1,UNITS))


    # add a vertical scrollbar to the frame
    rightScrollbar = Scrollbar(textboxFrame, orient=VERTICAL, command=textArea.yview)
    textArea.configure(yscrollcommand = rightScrollbar.set)

    # add a horizontal scrollbar to the frame
    bottomScrollbar = Scrollbar(textboxFrame, orient=HORIZONTAL, command=textArea.xview)
    textArea.configure(xscrollcommand = bottomScrollbar.set)

    # pack the textArea and the scrollbars.  Note that although we must define
    # the textArea first, we must pack it last, so that the bottomScrollbar will
    # be located properly.

    # Note that we need a bottom scrollbar only for code.
    # Text will be displayed with wordwrap, so we don't need to have a horizontal
    # scroll for it.
    if codebox:
        bottomScrollbar.pack(side=BOTTOM, fill=X)
    rightScrollbar.pack(side=RIGHT, fill=Y)

    textArea.pack(side=LEFT, fill=BOTH, expand=YES)


    # ---------- put a msg widget in the msg frame-------------------
    messageWidget = Message(messageFrame, anchor=NW, text=msg, width=int(root_width * 0.9))
    #messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=LEFT, expand=YES, fill=X, padx='1m', pady='1m')

    # put the buttons in the buttonsFrame
    okButton = Button(buttonsFrame, takefocus=YES, text="OK", height=1, width=6)
    okButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")
    hideButton = Button(buttonsFrame, takefocus=YES, text="Hide", height=1, width=6)
    hideButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")
    if showfiles:
        saveButton = Button(buttonsFrame, takefocus=YES, text="Save", height=1, width=6)
        saveButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")
        loadButton = Button(buttonsFrame, takefocus=YES, text="Load", height=1, width=6)
        loadButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")    
    

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = okButton
    handler = __textboxOK
    for selectionEvent in ["Return","Button-1","Escape"]:
        commandButton.bind("<%s>" % selectionEvent, handler)

    hideButton.bind("<Button-1>",__textboxHIDE)
    if showfiles:
        saveButton.bind("<Button-1>",__textboxSAVE)
        loadButton.bind("<Button-1>",__textboxLOAD)      

    # ----------------- the action begins ----------------------------------------
    try:
        # load the text into the textArea
        if type(text) == type("abc"): pass
        else:
            try:
                text = "".join(text)  # convert a list or a tuple to a string
            except:
                msgbox("Exception when trying to convert "+ str(type(text)) + " to text in textArea")
                sys.exit(16)
        textArea.insert(END,text, "normal")
        #Evitar que se edite el texto--------------------------------------------
        if edit!=1:
            textArea.configure(state='disabled')
        #------------------------------------------------------------------------         

    except:
        msgbox("Exception when trying to load the textArea.")
        sys.exit(16)

    try:
        okButton.focus_force()
    except:
        msgbox("Exception when trying to put focus on okButton.")
        sys.exit(16)

    boxRoot.mainloop()

    # this line MUST go before the line that destroys boxRoot
    areaText = textArea.get(0.0,END)
    boxRoot.destroy()
    return areaText # return __replyButtonText

#-------------------------------------------------------------------
# __textboxOK
#-------------------------------------------------------------------
def __textboxOK(event):
    global boxRoot
    boxRoot.quit()

def __textboxHIDE(event):
    global boxRoot
    #boxRoot.withdraw()
    boxRoot.iconify()

##def __textboxSHOW(event):
##    global boxRoot
##    boxRoot.deiconify()

def __textboxSAVE(event):
    global textArea
    f = tk_FileDialog.asksaveasfilename(parent=boxRoot
        , title='Save text contents'
        , initialdir='.\*.txt'
        #, initialfile='new_textfile.txt'
        #, filetypes=[["*.htm", "*.html", "HTML files"]  ] #[['*.txt',"Text Files"]]
        )

    if not f: return None
    fl=open(os.path.normpath(f),'w')
    fl.write(textArea.get(0.0,END))
    fl.close()
    return 1

def __textboxLOAD(event):
    global textArea
    f = tk_FileDialog.askopenfilename(parent=boxRoot
        , title='Load text contents'
        , initialdir='.\*.txt'
        #, initialfile='new_textfile.txt'
        #, filetypes=[["*.htm", "*.html", "HTML files"]  ] #[['*.txt',"Text Files"]]
        )

    if not f: return None
    fl=open(os.path.normpath(f),'r')
    txt=fl.read()
    textArea.insert(END,txt, "normal")
    fl.close()
    return 1
#-------------------------------------------------------------------
# diropenbox
#-------------------------------------------------------------------
def diropenbox(msg=None
    , title=None
    , default=None
    ):
    """
    A dialog to get a directory name.
    Note that the msg argument, if specified, is ignored.

    Returns the name of a directory, or None if user chose to cancel.

    If the "default" argument specifies a directory name, and that
    directory exists, then the dialog box will start with that directory.
    """
    title=getFileDialogTitle(msg,title)
    boxRoot = Tk()
    boxRoot.withdraw()
    if not default: default = None
    f = tk_FileDialog.askdirectory(
          parent=boxRoot
        , title=title
        , initialdir=default
        , initialfile=None
        )
    boxRoot.destroy()
    if not f: return None
    return os.path.normpath(f)



#-------------------------------------------------------------------
# getFileDialogTitle
#-------------------------------------------------------------------
def getFileDialogTitle(msg
    , title
    ):
    if msg and title: return "%s - %s" % (title,msg)
    if msg and not title: return str(msg)
    if title and not msg: return str(title)
    return None # no message and no title

#-------------------------------------------------------------------
# class FileTypeObject for use with fileopenbox
#-------------------------------------------------------------------
class FileTypeObject:
    def __init__(self,filemask):
        if len(filemask) == 0:
            raise AssertionError('Filetype argument is empty.')

        self.masks = []

        if type(filemask) == type("abc"):  # a string
            self.initializeFromString(filemask)

        elif type(filemask) == type([]): # a list
            if len(filemask) < 2:
                raise AssertionError('Invalid filemask.\n'
                +'List contains less than 2 members: "%s"' % filemask)
            else:
                self.name  = filemask[-1]
                self.masks = list(filemask[:-1] )
        else:
            raise AssertionError('Invalid filemask: "%s"' % filemask)

    def __eq__(self,other):
        if self.name == other.name: return True
        return False

    def add(self,other):
        for mask in other.masks:
            if mask in self.masks: pass
            else: self.masks.append(mask)

    def toTuple(self):
        return (self.name,tuple(self.masks))

    def isAll(self):
        if self.name == "All files": return True
        return False

    def initializeFromString(self, filemask):
        # remove everything except the extension from the filemask
        self.ext = os.path.splitext(filemask)[1]
        if self.ext == "" : self.ext = ".*"
        if self.ext == ".": self.ext = ".*"
        self.name = self.getName()
        self.masks = ["*" + self.ext]

    def getName(self):
        e = self.ext
        if e == ".*"  : return "All files"
        if e == ".txt": return "Text files"
        if e == ".py" : return "Python files"
        if e == ".pyc" : return "Python files"
        if e == ".xls": return "Excel files"
        if e.startswith("."):
            return e[1:].upper() + " files"
        return e.upper() + " files"


#-------------------------------------------------------------------
# fileopenbox
#-------------------------------------------------------------------
def fileopenbox(msg=None
    , title=None
    , default="*"
    , filetypes=None
    ):
    """
    A dialog to get a file name.

    About the "default" argument
    ============================
        The "default" argument specifies a filepath that (normally)
        contains one or more wildcards.
        fileopenbox will display only files that match the default filepath.
        If omitted, defaults to "*" (all files in the current directory).

        WINDOWS EXAMPLE::
            ...default="c:/myjunk/*.py"
        will open in directory c:\myjunk\ and show all Python files.

        WINDOWS EXAMPLE::
            ...default="c:/myjunk/test*.py"
        will open in directory c:\myjunk\ and show all Python files
        whose names begin with "test".


        Note that on Windows, fileopenbox automatically changes the path
        separator to the Windows path separator (backslash).

    About the "filetypes" argument
    ==============================
        If specified, it should contain a list of items,
        where each item is either::
            - a string containing a filemask          # e.g. "*.txt"
            - a list of strings, where all of the strings except the last one
                are filemasks (each beginning with "*.",
                such as "*.txt" for text files, "*.py" for Python files, etc.).
                and the last string contains a filetype description

        EXAMPLE::
            filetypes = ["*.css", ["*.htm", "*.html", "HTML files"]  ]

    NOTE THAT
    =========

        If the filetypes list does not contain ("All files","*"),
        it will be added.

        If the filetypes list does not contain a filemask that includes
        the extension of the "default" argument, it will be added.
        For example, if     default="*abc.py"
        and no filetypes argument was specified, then
        "*.py" will automatically be added to the filetypes argument.

    @rtype: string or None
    @return: the name of a file, or None if user chose to cancel

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg default: filepath with wildcards
    @arg filetypes: filemasks that a user can choose, e.g. "*.txt"
    """
    boxRoot = Tk()
    boxRoot.withdraw()

    initialbase, initialfile, initialdir, filetypes = fileboxSetup(default,filetypes)

    #------------------------------------------------------------
    # if initialfile contains no wildcards; we don't want an
    # initial file. It won't be used anyway.
    # Also: if initialbase is simply "*", we don't want an
    # initialfile; it is not doing any useful work.
    #------------------------------------------------------------
    if (initialfile.find("*") < 0) and (initialfile.find("?") < 0):
        initialfile = None
    elif initialbase == "*":
        initialfile = None

    f = tk_FileDialog.askopenfilename(parent=boxRoot
        , title=getFileDialogTitle(msg,title)
        , initialdir=initialdir
        , initialfile=initialfile
        , filetypes=filetypes
        )

    boxRoot.destroy()

    if not f: return None
    return os.path.normpath(f)


#-------------------------------------------------------------------
# filesavebox
#-------------------------------------------------------------------
def filesavebox(msg=None
    , title=None
    , default=""
    , filetypes=None
    ):
    """
    A file to get the name of a file to save.
    Returns the name of a file, or None if user chose to cancel.

    The "default" argument should contain a filename (i.e. the
    current name of the file to be saved).  It may also be empty,
    or contain a filemask that includes wildcards.

    The "filetypes" argument works like the "filetypes" argument to
    fileopenbox.
    """

    boxRoot = Tk()
    boxRoot.withdraw()

    initialbase, initialfile, initialdir, filetypes = fileboxSetup(default,filetypes)

    f = tk_FileDialog.asksaveasfilename(parent=boxRoot
        , title=getFileDialogTitle(msg,title)
        , initialfile=initialfile
        , initialdir=initialdir
        , filetypes=filetypes
        )
    boxRoot.destroy()
    if not f: return None
    return os.path.normpath(f)


#-------------------------------------------------------------------
#
# fileboxSetup
#
#-------------------------------------------------------------------
def fileboxSetup(default,filetypes):
    if not default: default = os.path.join(".","*")
    initialdir, initialfile = os.path.split(default)
    if not initialdir : initialdir  = "."
    if not initialfile: initialfile = "*"
    initialbase, initialext = os.path.splitext(initialfile)
    initialFileTypeObject = FileTypeObject(initialfile)

    allFileTypeObject = FileTypeObject("*")
    ALL_filetypes_was_specified = False

    if not filetypes: filetypes= []
    filetypeObjects = []

    for filemask in filetypes:
        fto = FileTypeObject(filemask)

        if fto.isAll():
            ALL_filetypes_was_specified = True # remember this

        if fto == initialFileTypeObject:
            initialFileTypeObject.add(fto) # add fto to initialFileTypeObject
        else:
            filetypeObjects.append(fto)

    #------------------------------------------------------------------
    # make sure that the list of filetypes includes the ALL FILES type.
    #------------------------------------------------------------------
    if ALL_filetypes_was_specified:
        pass
    elif allFileTypeObject == initialFileTypeObject:
        pass
    else:
        filetypeObjects.insert(0,allFileTypeObject)
    #------------------------------------------------------------------
    # Make sure that the list includes the initialFileTypeObject
    # in the position in the list that will make it the default.
    # This changed between Python version 2.5 and 2.6
    #------------------------------------------------------------------
    if len(filetypeObjects) == 0:
        filetypeObjects.append(initialFileTypeObject)

    if initialFileTypeObject in (filetypeObjects[0], filetypeObjects[-1]):
        pass
    else:
        if runningPython26:
            filetypeObjects.append(initialFileTypeObject)
        else:
            filetypeObjects.insert(0,initialFileTypeObject)

    filetypes = [fto.toTuple() for fto in filetypeObjects]

    return initialbase, initialfile, initialdir, filetypes

#-------------------------------------------------------------------
# utility routines
#-------------------------------------------------------------------
# These routines are used by several other functions in the EasyGui module.


#Solo para Mini------------------------------------------------------------------------
def message(title,msg,_type,icon): #tkMessageBox
    '''
    Muestra un mensaje.
    Prototipo: message(mensaje,titulo[,icon])
    '''
    '''default constant
    Which button to make default: ABORT, RETRY, IGNORE, OK, CANCEL, YES, or NO
    (the constants are defined in the tkMessageBox module).
    icon (constant)
    Which icon to display: ERROR, INFO, QUESTION, or WARNING
    message (string)
    The message to display (the second argument to the convenience functions).
    May contain newlines.
    parent (widget)
    Which window to place the message box on top of. When the message box is closed,
    the focus is returned to the parent window.
    title (string)
    Message box title (the first argument to the convenience functions).
    type (constant)
    Message box type; that is, which buttons to display: ABORTRETRYIGNORE,
    OK, OKCANCEL, RETRYCANCEL, YESNO, or YESNOCANCEL.
    '''
    global topmaster
    icons=['info','warning','error','question']
    if topmaster==None:
        top=Tkinter.Tk()
        top.withdraw()
    options={
        'ok': tkMessageBox.OK,
        'okcancel': tkMessageBox.OKCANCEL,
        'yesno': tkMessageBox.YESNO,
        'yesnocancel': tkMessageBox.YESNOCANCEL,
        'abortretryignore': tkMessageBox.ABORTRETRYIGNORE,
        'retrycancel': tkMessageBox.RETRYCANCEL
        }
    t=tkMessageBox.OK
    if _type in options:
        t=options[_type]
    retval=None
    if icon=='info':
        retval=tkMessageBox.showinfo(title,msg,type=t)
    elif icon=='warning':
        retval=tkMessageBox.showwarning(title,msg)
    elif icon=='error':
        retval=tkMessageBox.showerror(title,msg)
    elif icon=='question':
        retval=tkMessageBox.showquestion(title,msg)
    if topmaster==None:
        top.destroy()
    return retval



import time
import calendar
year = time.localtime()[0]
month = time.localtime()[1]
day =time.localtime()[2]
strdate = (str(year) +  "/" + str(month) + "/" + str(day))

tk = Tkinter 

fnta = ("Times", 12)
fnt = ("Times", 14)
fntc = ("Times", 18, 'bold')

lang="engl"
#lang = "span" #else lang="engl"

if lang == "span":
    #Spanish Options 
    strtitle = "Calendario"
    strdays= "Do  Lu  Ma  Mi  Ju  Vi  Sa"
    dictmonths = {'1':'Ene','2':'Feb','3':'Mar','4':'Abr','5':'May','6':'Jun','7':'Jul','8':'Ago','9':'Sep','10':'Oct','11':'Nov','12':'Dic'}
else :
    #English Options 
    strtitle = "Calendar"
    strdays = "Su  Mo  Tu  We  Th  Fr  Sa"
    dictmonths = {'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'Jun','7':'Jul','8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}

##############################################
#  BEGIN CLASS
class tkCalendar :
  def __init__ (self, master, arg_year, arg_month, arg_day, arg_parent_updatable_var):
    self.master=master
    self.update_var = arg_parent_updatable_var
    #top = self.top = tk.Toplevel(master)
    top = self.top = Tkinter.Frame(master)
    try : self.intmonth = int(arg_month)
    except: self.intmonth = int(1)
    self.canvas =Tkinter.Canvas (top, width =200, height =220,
      relief =Tkinter.RIDGE, background ="white", borderwidth =1)
    self.canvas.create_rectangle(0,0,303,30, fill="#a4cae8",width=0 )
    self.canvas.create_text(100,17, text=strtitle,  font=fntc, fill="#2024d6")
    stryear = str(arg_year)

    self.year_var=Tkinter.StringVar()
    self.year_var.set(stryear)
    self.lblYear = Tkinter.Label(top, textvariable = self.year_var, font = fnta, background="white")
    self.lblYear.place(x=85, y = 30)

    self.month_var=Tkinter.StringVar()
    strnummonth = str(self.intmonth)
    strmonth = dictmonths[strnummonth]
    self.month_var.set(strmonth)

    self.lblYear = Tkinter.Label(top, textvariable = self.month_var, font = fnta, background="white")
    self.lblYear.place(x=85, y = 50)
    #Variable muy usada
    tagBaseButton = "Arrow"
    self.tagBaseNumber = "DayButton"
    #draw year arrows
    x,y = 40, 43
    tagThisButton = "leftyear"  
    tagFinalThisButton = tuple((tagBaseButton,tagThisButton))
    self.fnCreateLeftArrow(self.canvas, x,y, tagFinalThisButton)
    x,y = 150, 43
    tagThisButton = "rightyear"  
    tagFinalThisButton = tuple((tagBaseButton,tagThisButton))
    self.fnCreateRightArrow(self.canvas, x,y, tagFinalThisButton)
    #draw month arrows
    x,y = 40, 63
    tagThisButton = "leftmonth"  
    tagFinalThisButton = tuple((tagBaseButton,tagThisButton))
    self.fnCreateLeftArrow(self.canvas, x,y, tagFinalThisButton)
    x,y = 150, 63
    tagThisButton = "rightmonth"  
    tagFinalThisButton = tuple((tagBaseButton,tagThisButton))
    self.fnCreateRightArrow(self.canvas, x,y, tagFinalThisButton)
    #Print days 
    self.canvas.create_text(100,90, text=strdays, font=fnta)
    self.canvas.pack (expand =1, fill =Tkinter.BOTH)
    self.canvas.tag_bind ("Arrow", "<ButtonRelease-1>", self.fnClick)
    self.canvas.tag_bind ("Arrow", "<Enter>", self.fnOnMouseOver)
    self.canvas.tag_bind ("Arrow", "<Leave>", self.fnOnMouseOut)   
    self.fnFillCalendar()

  def fnCreateRightArrow(self, canv, x, y, strtagname):
    canv.create_polygon(x,y, [[x+0,y-5], [x+10, y-5] , [x+10,y-10] , [x+20,y+0], [x+10,y+10] , [x+10,y+5] , [x+0,y+5]],tags = strtagname , fill="blue", width=0)

  def fnCreateLeftArrow(self, canv, x, y, strtagname):
    canv.create_polygon(x,y, [[x+10,y-10], [x+10, y-5] , [x+20,y-5] , [x+20,y+5], [x+10,y+5] , [x+10,y+10] ],tags = strtagname , fill="blue", width=0)

  def fnClick(self,event):
    owntags =self.canvas.gettags(Tkinter.CURRENT)
    if "rightyear" in owntags:
        intyear = int(self.year_var.get())
        intyear +=1
        stryear = str(intyear)
        self.year_var.set(stryear)
    if "leftyear" in owntags:
        intyear = int(self.year_var.get())
        intyear -=1
        stryear = str(intyear)
        self.year_var.set(stryear)
    if "rightmonth" in owntags:
        if self.intmonth < 12 :
            self.intmonth += 1 
            strnummonth = str(self.intmonth)
            strmonth = dictmonths[strnummonth]
            self.month_var.set(strmonth)
        else :
            self.intmonth = 1 
            strnummonth = str(self.intmonth)
            strmonth = dictmonths[strnummonth]
            self.month_var.set(strmonth)
            intyear = int(self.year_var.get())
            intyear +=1
            stryear = str(intyear)
            self.year_var.set(stryear)
    if "leftmonth" in owntags:
        if self.intmonth > 1 :
            self.intmonth -= 1 
            strnummonth = str(self.intmonth)
            strmonth = dictmonths[strnummonth]
            self.month_var.set(strmonth)
        else :
            self.intmonth = 12
            strnummonth = str(self.intmonth)
            strmonth = dictmonths[strnummonth]
            self.month_var.set(strmonth)
            intyear = int(self.year_var.get())
            intyear -=1
            stryear = str(intyear)
            self.year_var.set(stryear)
    self.fnFillCalendar()	    
    
  def fnFillCalendar(self):
    init_x_pos = 20
    arr_y_pos = [110,130,150,170,190,210]
    intposarr = 0
    self.canvas.delete("DayButton")
    self.canvas.update()
    intyear = int(self.year_var.get())
    monthcal = calendar.monthcalendar(intyear, self.intmonth)    
    for row in monthcal:
        xpos = init_x_pos 
        ypos = arr_y_pos[intposarr]
        for item in row:	
            stritem = str(item)
            if stritem == "0":
                xpos += 27
            else :
                tagNumber = tuple((self.tagBaseNumber,stritem))
                self.canvas.create_text(xpos, ypos , text=stritem, 
                font=fnta,tags=tagNumber)	
                xpos += 27
        intposarr += 1
        self.canvas.tag_bind ("DayButton", "<ButtonRelease-1>", self.fnClickNumber)
        self.canvas.tag_bind ("DayButton", "<Enter>", self.fnOnMouseOver)
        self.canvas.tag_bind ("DayButton", "<Leave>", self.fnOnMouseOut)   

  def fnClickNumber(self,event):
    owntags =self.canvas.gettags(Tkinter.CURRENT)
    for x in owntags:
        if (x == "current") or (x == "DayButton"):pass
        else : 
            strdate = (str(self.year_var.get()) + "/" + 
                str(self.intmonth) + "/" +  
                str(x)) 
            self.update_var.set(strdate)
            #self.top.withdraw()
            self.master.quit()
  def fnOnMouseOver(self,event):
    x=Tkinter.CURRENT
    self.canvas.move(Tkinter.CURRENT, 1, 1)
    self.canvas.itemconfigure(x, fill='blue')
    self.canvas.update()

  def fnOnMouseOut(self,event):
    x=Tkinter.CURRENT
    self.canvas.move(Tkinter.CURRENT, -1, -1)
    self.canvas.itemconfigure(x, fill='black')    
    self.canvas.update()


def calendarbox(title,y,m,d,icon=None):
    tk=Tk()
    #Para permitir una apariencia estandar-------------------------
    #El archivo de configuracion DEBE estar separado por caracteres de nueva linea!!!!
    #if os.path.exists(SYMTAB['__GUI_CONFIG__']):
    #    tk.option_readfile (SYMTAB['__GUI_CONFIG__'])
    #--------------------------------------------------------------

    tk.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    
    tk.title(title)
    #Tuneado para poder poner un icono---------------------------
    if icon:
        tk.wm_iconbitmap(icon)
    #------------------------------------------------------------
    date_var = Tkinter.StringVar()
    date_var.set(strdate)
        
    cal=tkCalendar(tk, year, month, day, date_var )
    cal.top.pack(fill=BOTH,expand=YES)
    tk.mainloop()
    date=date_var.get()    
    tk.destroy()
    return date
    

def gridview(title,colnames,rows_list,icon=None):
    #_guiGridViewBox(titulo,mensaje,cols_title_list,matrix_name,result_list_name,allow_multisel,allow_delete,allow_find[,icon])
    global tk,griddict,model
    tk = Tk()
    #Para permitir una apariencia estandar-------------------------
    #El archivo de configuracion DEBE estar separado por caracteres de nueva linea!!!!
    #if os.path.exists(SYMTAB['__GUI_CONFIG__']):
    #    tk.option_readfile (SYMTAB['__GUI_CONFIG__'])
    #--------------------------------------------------------------

    #tk.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    
    tk.title(title)
    #Tuneado para poder poner un icono---------------------------
    if icon:
        tk.wm_iconbitmap(icon)
    #------------------------------------------------------------
    tframe = Frame(tk) 
    tframe.pack()
    griddict={}
    #Colocar las columnas
    dic={'columnnames':colnames}
    coltypes={}
    collabs={}
    for el in colnames:
        coltypes[el]='text'
        collabs[el]=el
    dic['columntypes']=coltypes
    dic['columnlabels']=collabs
    
    model=TableModel(dic)
    #print rows_list
    for i in xrange(len(rows_list)):
        model.addRow()
        for j in xrange(len(rows_list[i])):
            #print 'Valor actual: %s' % str(rows_list[i][j])
            model.setValueAt(str(rows_list[i][j]),i,j)

            
    table = TableCanvas(tframe,model) 
    table.createTableFrame()

    # OK button
    okButton = Button(tk, takefocus=YES, text="OK", height=1, width=6, command=__gridboxOK)
    okButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")    

    tk.mainloop()
    #
    return str(griddict)

def __gridboxOK(event=None):
    global tk,griddict,model
    griddict=model.getAllCells()
    #print griddict
    tk.destroy()
        

def imagebox(msg,title,images_list,icon=None):
    global tk,numimages,actimage,images,tkImage,sc,contador,last_mouse
    tk = Tk()
    actimage=''
    last_mouse=[]
    
    #Para permitir una apariencia estandar-------------------------
    #El archivo de configuracion DEBE estar separado por caracteres de nueva linea!!!!
    if os.path.exists(SYMTAB['__GUI_CONFIG__']):
        tk.option_readfile (SYMTAB['__GUI_CONFIG__'])
    #--------------------------------------------------------------

    tk.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    
    tk.title(title)
    #Tuneado para poder poner un icono---------------------------
    if icon:
        tk.wm_iconbitmap(icon)
    #------------------------------------------------------------
    images=images_list 
    #print 'Archivos a mostrar: %s' %images
    
    #Numero de imagenes a mostrar
    numimages=len(images)        

    sc=TkScrolledCanvas(tk)
    sc.frame.pack(expand=YES, fill=BOTH)

    #Navegacion de las imagenes con el teclado y doble click para salir
    sc.canvas.bind("<Button-1>", __imageboxCLICK)    
    sc.canvas.bind("<Double-Button-1>", __imageboxOK)
    sc.canvas.bind('<Up>',__imageboxFIRST)
    sc.canvas.bind('<Down>',__imageboxLAST)
    sc.canvas.bind('<Right>',__imageboxNEXT)
    sc.canvas.bind('<Left>',__imageboxPREV)
    sc.canvas.bind('<Return>',__imageboxOK)    

    buttonsFrame = Frame(tk)
    buttonsFrame.pack(side=RIGHT, expand=NO)

    #Botones adelante-atras para navegacion
    firstButton = Button(buttonsFrame, takefocus=YES, text="<<", height=1, width=6, command=__imageboxFIRST, relief='flat')
    firstButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")
    prevButton = Button(buttonsFrame, takefocus=YES, text="<", height=1, width=6, command=__imageboxPREV, relief='flat')
    prevButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")       
    nextButton = Button(buttonsFrame, takefocus=YES, text=">", height=1, width=6, command=__imageboxNEXT, relief='flat')
    nextButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")
    lastButton = Button(buttonsFrame, takefocus=YES, text=">>", height=1, width=6, command=__imageboxLAST, relief='flat')
    lastButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")       

    # put the buttons in the buttonsFrame
    okButton = Button(buttonsFrame, takefocus=YES, text="OK", height=1, width=6, relief='flat')
    okButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")
    # for the commandButton, bind activation events to the activation event handler
    commandButton  = okButton
    handler = __imageboxOK
    for selectionEvent in ["Return","Button-1","Escape"]:
        commandButton.bind("<%s>" % selectionEvent, handler)

    #Mostrar la primera imagen e iniciar contador
    __changeImage(images[0])
    contador=0

    tk.mainloop()
    tk.destroy()
    if last_mouse==[]:
        return actimage
    else:
        last_mouse=[str(int(i)) for i in last_mouse]
        return actimage + '|' + '|'.join(last_mouse)



def __changeImage(image):
    global images,sc,tk_Image
    #print 'image: %s' %image
   #Gestion de las imagenes-------------------------------------
    tk_Image = None
    if image:
        imageFilename = os.path.normpath(image)
        junk,ext = os.path.splitext(imageFilename)

        if os.path.exists(imageFilename):
            if ext.lower() in [".gif", ".pgm", ".ppm"]:
                tk_Image = PhotoImage(file=imageFilename)
            else:
                pil_Image = PILImage.open(imageFilename)
                tk_Image = PILImageTk.PhotoImage(pil_Image)
        #-----------------------------------------------------------------


        #El canvas debera permitir desplazamiento a lo largo y ancho de la imagen---------
        region=(0,0,tk_Image.width(),tk_Image.height())
        #sc.canvas.delete('all')
        sc.canvas.create_image(0, 0, image =tk_Image, anchor = NW)
        sc.canvas.config(scrollregion=region)
        #---------------------------------------------------------------------------------
    

def __imageboxCLICK(event):
    global last_mouse
    last_mouse=[event.x,event.y]

def __imageboxOK(event):
    global tk
    tk.quit()


def __imageboxFIRST(event=None):
    global tk,numimages,actimage,contador
    if contador!=0:
        __changeImage(images[0])
        actimage=images[0]
        #print 'Cambiando a: %s' % actimage
        #print 'Contador vale: %s' % contador
        contador=0

def __imageboxLAST(event=None):
    global tk,numimages,actimage,contador
    if contador!=len(images)-1:
        __changeImage(images[-1])
        actimage=images[-1]
        #print 'Cambiando a: %s' % actimage
        #print 'Contador vale: %s' % contador        
        contador=len(images)-1

def __imageboxPREV(event=None):
    global tk,numimages,actimage,contador
    if contador > 0:
        contador-=1
        __changeImage(images[contador])
        actimage=images[contador]
        #print 'Cambiando a: %s' % actimage
        #print 'Contador vale: %s' % contador        

def __imageboxNEXT(event=None):
    global tk,numimages,actimage,contador
    if contador!=len(images)-1:
        contador+=1
        __changeImage(images[contador])
        actimage=images[contador]
        #print 'Cambiando a en NEXT: %s' % actimage
        #print 'Contador vale: %s' % contador        


MOVE_LINES = 0
MOVE_PAGES = 1
MOVE_TOEND = 2

class MultiListbox2(Frame):
    """
    MultiListbox Class.

    Defines a multi-column listbox.  The constructor takes a list of
    tuples, where each tuple is (column-label, character-width).  The
    list will have as many columns as tuples.  Add items to the list by
    passing tuples or lists of items, one for each column.

    Each column will be given the specified width in character units,
    with a header of column-label.  Also takes many of the normal
    Listbox options for background, font, etc.
    """
    def __init__(self, master, lists, allow_multi=0, command=None, **options):
        defaults = {
            'background': None,
            'borderwidth': 2,
            'font': None,
            'foreground': None,
            'height': 10,
            'highlightcolor': None,
            'highlightthickness': 1,
            'relief': SUNKEN,
            'takefocus': 1,
            }

        aliases = {'bg':'background', 'fg':'foreground', 'bd':'borderwidth'}

        for k in aliases.keys ():
            if options.has_key (k):
                options [aliases[k]] = options [k]
            
        for key in defaults.keys():
            if not options.has_key (key):
                options [key] = defaults [key]

        apply (Frame.__init__, (self, master), options)
        self.lists = []

        self.fields=[] #Campos a devolver
        self.allow_multi=allow_multi #Flag para permitir seleccion multiple           

        # MH (05/20049
        # These are needed for sorting
        self.colmapping={}
        self.origData = None

        #  Keyboard navigation.
        
        self.bind ('<Up>',    lambda e, s=self: s._move (-1, MOVE_LINES))
        self.bind ('<Down>',  lambda e, s=self: s._move (+1, MOVE_LINES))
        self.bind ('<Prior>', lambda e, s=self: s._move (-1, MOVE_PAGES))
        self.bind ('<Next>',  lambda e, s=self: s._move (+1, MOVE_PAGES))
        self.bind ('<Home>',  lambda e, s=self: s._move (-1, MOVE_TOEND))
        self.bind ('<End>',   lambda e, s=self: s._move (+1, MOVE_TOEND))
        if command:
            self.bind ('<Return>', command)

        # Columns are a frame with listbox and label in it.
        
        # MH (05/2004):
        # Introduced a PanedWindow to make the columns resizable
        
        m = Tkinter.PanedWindow(self, orient=HORIZONTAL, bd=0, background=options['background'], showhandle=0, sashpad=1)
        m.pack(side=LEFT, fill=BOTH, expand=1)

        for label, width in lists:
            lbframe = Frame(m)
            m.add(lbframe, width=width)
            # MH (05/2004)
            # modified this, click to sort
            b = Label(lbframe, text=label, borderwidth=1, relief=RAISED)
            b.pack(fill=X)
            b.bind('<Button-1>', self._sort)

            self.colmapping[b]=(len(self.lists),1)
            
            lb = Listbox (lbframe,
                          width=width,
                          height=options ['height'],
                          borderwidth=0,
                          font=options ['font'],
                          background=options ['background'],
                          selectborderwidth=0,
                          relief=SUNKEN,
                          takefocus=FALSE,
                          exportselection=FALSE,
                          selectmode=MULTIPLE)
            lb.pack (expand=YES, fill=BOTH)
            self.lists.append (lb)

            # Mouse features
            
            lb.bind ('<B1-Motion>', lambda e, s=self: s._select (e.y))
            lb.bind ('<Button-1>',  lambda e, s=self: s._select (e.y))
            lb.bind ('<Leave>',     lambda e: 'break')
            lb.bind ('<B2-Motion>', lambda e, s=self: s._b2motion (e.x, e.y))
            lb.bind ('<Button-2>',  lambda e, s=self: s._button2 (e.x, e.y))
            if command:
                lb.bind ('<Double-Button-1>', command)

        sbframe = Frame (self)
        sbframe.pack (side=LEFT, fill=Y)
        l = Label (sbframe, borderwidth=1, relief=RAISED)
        l.bind ('<Button-1>', lambda e, s=self: s.focus_set ())
        l.pack(fill=X)
        sb = Scrollbar (sbframe,
                        takefocus=FALSE,
                        orient=VERTICAL,
                        command=self._scroll)
        sb.pack (expand=YES, fill=Y)
        self.lists[0]['yscrollcommand']=sb.set

        return


    # MH (05/2004)
    # Sort function, adopted from Rick Lawson 
    # http://tkinter.unpythonic.net/wiki/SortableTable
    
    def _sort(self, e):
        # get the listbox to sort by (mapped by the header button)
        b=e.widget
        col, direction = self.colmapping[b]

        # get the entire table data into mem
        tableData = self.get(0,END)
        if self.origData == None:
            import copy
            self.origData = copy.deepcopy(tableData)

        rowcount = len(tableData)

        #remove old sort indicators if it exists
        for btn in self.colmapping.keys():
            lab = btn.cget('text')
            if lab[0]=='[': btn.config(text=lab[4:])

        btnLabel = b.cget('text')
        #sort data based on direction
        if direction==0:
            tableData = self.origData
        else:
            if direction==1: b.config(text='[+] ' + btnLabel)
            else: b.config(text='[-] ' + btnLabel)
            # sort by col
            def colsort(x, y, mycol=col, direction=direction):
                return direction*cmp(x[mycol], y[mycol])

            tableData.sort(colsort)

        #clear widget
        self.delete(0,END)

        # refill widget
        for row in range(rowcount):
            self.insert(END, tableData[row])

        # toggle direction flag 
        if(direction==1): direction=-1
        else: direction += 1
        self.colmapping[b] = (col, direction) 
        

    def _move (self, lines, relative=0):
        """
        Move the selection a specified number of lines or pages up or
        down the list.  Used by keyboard navigation.
        """
        selected = self.lists [0].curselection ()
        try:
            selected = map (int, selected)
        except ValueError:
            pass

        try:
            sel = selected [0]
        except IndexError:
            sel = 0

        old  = sel
        size = self.lists [0].size ()
        
        if relative == MOVE_LINES:
            sel = sel + lines
        elif relative == MOVE_PAGES:
            sel = sel + (lines * int (self.lists [0]['height']))
        elif relative == MOVE_TOEND:
            if lines < 0:
                sel = 0
            elif lines > 0:
                sel = size - 1
        else:
            print "MultiListbox._move: Unknown move type!"

        if sel < 0:
            sel = 0
        elif sel >= size:
            sel = size - 1
        
        self.selection_clear (old, old)
        self.see (sel)
        self.selection_set (sel)
        return 'break'


    def _select (self, y):
        """
        User clicked an item to select it.
        """
##        row = self.lists[0].nearest (y)
##        self.selection_clear (0, END)
##        self.selection_set (row)
##        self.focus_set ()
##        return 'break'
        row = self.lists[0].nearest(y)
        #print self.allow_multi
        if self.allow_multi==0:
            self.selection_clear(0, END)
            self.selection_set(row)
        else:
            if self.selection_includes(row):
                self.selection_clear(row)
            else:
                self.selection_set(row)
        #self.focus_set()
        return 'break'


    def _button2 (self, x, y):
        """
        User selected with button 2 to start a drag.
        """
        for l in self.lists:
            l.scan_mark (x, y)
        return 'break'


    def _b2motion (self, x, y):
        """
        User is dragging with button 2.
        """
        for l in self.lists:
            l.scan_dragto (x, y)
        return 'break'


    def _scroll (self, *args):
        """
        Scrolling with the scrollbar.
        """
        #print args
        for l in self.lists:
            apply(l.yview,args)

    def curselection (self):
        """
        Return index of current selection.
        """
        return self.lists[0].curselection()


    def delete (self, first, last=None):
        """
        Delete one or more items from the list.
        """
        for l in self.lists:
            l.delete(first, last)


    def get (self, first, last=None):
        """
        Get items between two indexes, or one item if second index
        is not specified.
        """
        result = []
        for l in self.lists:
            result.append (l.get (first,last))
        if last:
            return apply (map, [None] + result)
        return result

            
    def index (self, index):
        """
        Adjust the view so that the given index is at the top.
        """
        for l in self.lists:
            l.index (index)


    def insert (self, index, *elements):
        """
        Insert list or tuple of items.
        """
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert (index, e[i])
                i = i + 1
        if self.size () == 1:
            self.selection_set (0)
            

    def size (self):
        """
        Return the total number of items.
        """
        return self.lists[0].size ()


    def see (self, index):
        """
        Make sure given index is visible.
        """
        for l in self.lists:
            l.see (index)


    def selection_anchor (self, index):
        """
        Set selection anchor to index.
        """
        for l in self.lists:
            l.selection_anchor (index)


    def selection_clear (self, first, last=None):
        """
        Clear selections between two indexes.
        """
        for l in self.lists:
            l.selection_clear (first, last)


    def selection_includes (self, index):
        """
        Determine if given index is selected.
        """
        return self.lists[0].selection_includes (index)


    def selection_set (self, first, last=None):
        """
        Select a range of indexes.
        """
        for l in self.lists:
            l.selection_set (first, last)





class MultiListbox(Frame):
    def __init__(self, master, lists, allow_multi=0):
        Frame.__init__(self, master)
        self.lists = []
        self.colmapping={}
        self.origData = None
        self.fields=[] #Campos a devolver
        self.allow_multi=allow_multi #Flag para permitir seleccion multiple        
        for l,w in lists:
            frame = Frame(self)
            frame.pack(side=LEFT, expand=YES, fill=BOTH)
            b = Button(frame, text=l, borderwidth=1, relief=RAISED)
            b.pack(fill=X)
            b.bind('<Button-1>', self._sort)
            self.colmapping[b]=(len(self.lists),1)
            lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                         relief=FLAT, exportselection=FALSE, selectmode=MULTIPLE)
            lb.pack(expand=YES, fill=BOTH)
            self.lists.append(lb)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        frame = Frame(self); frame.pack(side=LEFT, fill=Y)
        Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
        sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        self.lists[0]['yscrollcommand']=sb.set        


    def _select(self, y):
        row = self.lists[0].nearest(y)
        if self.allow_multi==0:
            self.selection_clear(0, END)
            self.selection_set(row)
        else:
            if self.selection_includes(row):
                self.selection_clear(row)
            else:
                self.selection_set(row)
        return 'break'

    def _button2(self, x, y):
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            apply(l.yview, args)
            

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        if last: return apply(map, [None] + result)
        return result

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

    def _sort(self, e):
        # get the listbox to sort by (mapped by the header button)
        b=e.widget
        col, direction = self.colmapping[b]

        # get the entire table data into mem
        tableData = self.get(0,END)
        if self.origData == None:
            import copy
            self.origData = copy.deepcopy(tableData)

        rowcount = len(tableData)

        #remove old sort indicators if it exists
        for btn in self.colmapping.keys():
            lab = btn.cget('text')
            if lab[0]=='[': btn.config(text=lab[4:])

        btnLabel = b.cget('text')
        #sort data based on direction
        if direction==0:
            tableData = self.origData
        else:
            if direction==1: b.config(text='[+] ' + btnLabel)
            else: b.config(text='[-] ' + btnLabel)
            # sort by col
            def colsort(x, y, mycol=col, direction=direction):
                return direction*cmp(x[mycol], y[mycol])

            tableData.sort(colsort)

        #clear widget
        self.delete(0,END)

        # refill widget
        for row in range(rowcount):
            self.insert(END, tableData[row])

        # toggle direction flag 
        if(direction==1): direction=-1
        else: direction += 1
        self.colmapping[b] = (col, direction)



def listview(msg,title,titles,elems,allow_multi,allow_delete=0,allow_find=1,icon=None):
    global tk,mlb,findText
    tk = Tk()
    #Para permitir una apariencia estandar-------------------------
    #El archivo de configuracion DEBE estar separado por caracteres de nueva linea!!!!
    #if os.path.exists(SYMTAB['__GUI_CONFIG__']):
    #    tk.option_readfile (SYMTAB['__GUI_CONFIG__'])
    #--------------------------------------------------------------

    tk.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    
    tk.title(title)
    #Tuneado para poder poner un icono---------------------------
    if icon:
        tk.wm_iconbitmap(icon)
    #------------------------------------------------------------       
    Label(tk, text=msg).pack()

    #print titles
    titls=[(x,len(x)+30) for x in titles]
    mlb = MultiListbox2(tk, titls, allow_multi)
    mlb.pack(expand=YES, fill=BOTH) 

    for lst in mlb.lists:
        lst.bind("<Double-Button-1>", __listboxDOUBLE)
            
    for i in xrange(len(elems)):
        mlb.insert(END, elems[i])
    mlb.pack(expand=YES,fill=BOTH)
    
    buttonsFrame = Frame(tk)
    buttonsFrame.pack(side=RIGHT, expand=NO)

    # put the buttons in the buttonsFrame
    okButton = Button(buttonsFrame, takefocus=YES, text="OK", height=1, width=6)
    okButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")
    if allow_delete==1:
        delButton = Button(buttonsFrame, takefocus=YES, text="Delete", height=1, width=6)
        delButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")    
        delButton.bind("<Button-1>",__listboxDELETE)

    if allow_find==1:
        findButton = Button(buttonsFrame, takefocus=YES, text="Find", height=1, width=6)
        findButton.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")    
        findButton.bind("<Button-1>",__listboxFIND)
        findText=Entry(buttonsFrame, width=40)
        findText.pack(expand=NO, side=LEFT,  padx='2m', pady='1m', ipady="1m", ipadx="2m")
    # for the commandButton, bind activation events to the activation event handler
    commandButton  = okButton
    handler = __listboxOK
    for selectionEvent in ["Return","Button-1","Escape"]:
        commandButton.bind("<%s>" % selectionEvent, handler)

    tk.mainloop()

    mlb.fields=[]
    sel=mlb.curselection()
    for item in sel:
        mlb.fields.append(mlb.get(item))
    tk.destroy()
    return mlb.fields


def __listboxOK(event):
    global tk
    tk.quit()

def __listboxDOUBLE(event):
    global tk
    tk.quit()    

def __listboxDELETE(event):
    global mlb
    sel=mlb.curselection()
    #print sel
    contador=0
    for item in sel:
        #print item
        if item==0:
            mlb.delete(item)
        else:
            mlb.delete(int(item)-contador)
        contador+=1

def __listboxFIND(event):
    global tk,mlb,findText
    mlb.selection_clear(0,END)
    for x in xrange(mlb.size()):
        #print mlb.get(x)
        line=''
        for el in mlb.get(x):
            if type(el) in [type(0),type(0.0),type(0L),"<type 'time'>"]:
                line+=str(el)
            else:
                line+=el    
        text=findText.get()
        if text in line:
            mlb.selection_set(x)
    


#-----------------------------------------------------------------------------------------
