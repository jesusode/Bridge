#Clases de utilidad para manejar dialogos, ventanas y controles via win32gui

import sys

import winxpgui as win32gui
import win32api
import win32con
import win32gui_struct
import struct, array
import commctrl
import os

import win32ui

#Estructuras para listviews y treeviews
from win32_aux_structs import *

import pywinauto

from matrix import *


# Need to do this go get rich-edit working.
#win32api.LoadLibrary("Riched20.dll")

WINDOW_STYLES={}

#Estilos para alinear el texto en los controles
ALIGN={
    'left': win32con.SS_LEFT,
    'right': win32con.SS_RIGHT,
    'center': win32con.SS_CENTER
    }

TEXTBOXALIGN={
    'left': win32con.ES_LEFT,
    'right': win32con.ES_RIGHT,
    'center': win32con.ES_CENTER
    }

MENU_TYPES={ #??????
    'radio': win32con.MFT_RADIOCHECK,
    'check': win32con.MFT_RADIOCHECK,
    'separator': win32con.MFT_SEPARATOR,
    '-': win32con.MFT_SEPARATOR,
    }

WIN_STYLES={
    'WS_BORDER': win32con.WS_BORDER,
    'WS_MAXIMIZEBOX': win32con.WS_MAXIMIZEBOX,
    'WS_MINIMIZEBOX': win32con.WS_MINIMIZEBOX,
    'WS_CAPTION': win32con.WS_CAPTION,
    'WS_SYSMENU': win32con.WS_SYSMENU,
    'WS_THICKFRAME': win32con.WS_THICKFRAME,
    'WS_VSCROLL': win32con.WS_VSCROLL,
    'WS_HSCROLL': win32con.WS_HSCROLL,
    'WS_POPUP': win32con.WS_POPUP,
    'WS_SIZEBOX': win32con.WS_SIZEBOX,
    'WS_HSCROLL': win32con.WS_HSCROLL,
    'WS_VSCROLL': win32con.WS_VSCROLL,
    'WS_DLGFRAME': win32con.WS_DLGFRAME
    }

def winStyleMaker(style_str):
    items=style_str.split('|')
    #print items
    style=win32con.WS_VISIBLE | win32con.WS_POPUP #Como minimo debe ser visible
    for item in items:
        print item
        if WIN_STYLES.has_key(item):
            style |=WIN_STYLES[item]
    return style

'''
integer lfHeight 
integer lfWidth 
integer lfEscapement 
integer lfOrientation 
integer lfWeight 
integer lfItalic 
integer lfUnderline 
integer lfStrikeOut 
integer lfCharSet 
integer lfOutPrecision 
integer lfClipPrecision 
integer lfQuality 
integer lfPitchAndFamily 
string lfFaceName 
Name of the typeface, at most 31 characters        
'''

def fontFactory(name,size=12,bold=0,italic=0,underline=0,strike=0,angle=0):
    logfont=win32gui.LOGFONT()
    logfont.lfFaceName=name
    logfont.lfStrikeOut=strike
    logfont.lfUnderline=underline
    logfont.lfItalic=italic
    logfont.lfEscapement=angle*10 #El angulo viene en decimas de grado
    if bold:
        logfont.lfWeight=700 #700: negrita normal
    else:
        logfont.lfWeight=400 #400: normal
    #Tamanyo en puntos
    #lfHeight = -MulDiv(PointSize, GetDeviceCaps(hDC, LOGPIXELSY), 72);
    dw=win32gui.GetDesktopWindow()
    hdc=win32gui.GetWindowDC(dw)
    #pw,ph=win32gui.GetTextExtentPoint32(hdc,'a')
    ph=win32ui.GetDeviceCaps(hdc,win32con.LOGPIXELSY)
    win32gui.ReleaseDC(dw,hdc)
    logfont.lfHeight=int((size*ph)/72)
    #print 'LONGITUD DE LA FUENTE: %d' % logfont.lfHeight
    #Tener en cuenta resto de posibilidades de LOGFONT???
    hfont=win32gui.CreateFontIndirect(logfont)
    return hfont


#Contador para generar IDs para controles
IDC_COUNTER=1500 #1100
#Contador para generar IDs para menus
MENU_ITEM_COUNTER=1123
#Contador para generar IDs para menus emergentes
POPUP_MENU_ITEM_COUNTER=1023

#Constante para estilo de ventana de dialogo normal (con titulo, menu de sistema, borde y botones de cerrar y minimizar)
DLG_STYLE_NORMAL=win32con.WS_THICKFRAME | win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT | win32con.WS_MINIMIZEBOX |win32con.DS_MODALFRAME

class DialogTemplateFactory(object):
    '''
    Crea plantillas de dialogo
    '''
    def __init__(self,classname,title='Mini Dialog Template',xi=0,yi=0,xf=200,yf=200,style=DLG_STYLE_NORMAL,ftname="MS Sans Serif",ftsize=8):
        #dlg = [ [title, (0, 0, 210, 250), style, None, (8, "MS Sans Serif"), None, dlgClassName], ]
        self.__dlgClassName=classname
        self.__title=title
        self.__xi=xi
        self.__yi=yi
        self.__xf=xf
        self.__yf=yf
        self.__style=style
        self.__ftname=ftname
        self.__ftsize=ftsize
        self.__dlgTemplate=[]

    def setTemplate(self,classname,title='Mini Dialog Template',xi=0,yi=0,w=200,h=200,style=DLG_STYLE_NORMAL,ftname="MS Sans Serif",ftsize=8):
        self.__dlgClassName=classname
        self.__title=title
        self.__xi=xi
        self.__yi=yi
        self.__xf=w
        self.__yf=h
        self.__style=style
        self.__ftname=ftname
        self.__ftsize=ftsize

    def getDialogTemplate(self):
        self.__dlgTemplate=[[self.__title,(self.__xi,self.__yi,self.__xf,self.__yf),self.__style,None,(self.__ftsize,self.__ftname),None,self.__dlgClassName],]
        return self.__dlgTemplate


class MenuFactory(object):
    '''
    Crea menus a medida
    '''
    def __init__(self):
        #self.menuitems=menuitems
        self.hmenu=None
        #Tabla {name_item: iditem}
        self.nameid={}
        #Tabla {name_item: callback}
        self.namecallb={}
        #Tabla temporal para menus popup {name_item: iditem}
        self.tempnameid={}
        #Tabla temporal para menus popup {name_item: callback}
        self.tempnamecallb={}        
        #Tabla de uso interno para submenus{name:submenu}
        self.submenus={}


    def createMenuBar(self,itemlist):
        #Solo lo creamos una vez!!
        if self.hmenu:
            return self.hmenu
        #Crea y devuelve una barra de menus
        global MENU_ITEM_COUNTER
        #Cada item de la lista tiene la estructura: [name,callback,type,text,submenu,image]
        self.hmenu=win32gui.CreateMenu()
        contador=0
        for item in itemlist:
            #Coger los elementos
            _name=item[0]
            callback=item[1]
            _type=item[2]
            _text=item[3]
            submenu=None
            image=None
            if item[4] not in ['',0,None]:
                submenu=item[4]
            if item[5] not in ['',None]:
                image=win32gui.LoadImage(0,item[5],win32con.IMAGE_BITMAP,20,20,win32con.LR_LOADFROMFILE | win32con.LR_LOADTRANSPARENT)
            item=extras=None
            if _type in ['-','separator']: #Separador
                #print 'Separador!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                fType=win32con.MFT_SEPARATOR,
                                                hbmpItem=image,
                                                wID=MENU_ITEM_COUNTER)            
            elif image and not submenu: #Imagen + texto
                #print 'item con imagen + texto!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                hbmpItem=image,
                                                wID=MENU_ITEM_COUNTER)
            elif submenu and image: #Imagen y submenu
                #print 'item con imagen, texto y submenu!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                hbmpItem=image,
                                                hSubMenu=submenu,
                                                wID=MENU_ITEM_COUNTER)
            elif submenu and not image: #Cadena y submenu
                #print 'item con submenu sin imagen!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                hSubMenu=submenu,
                                                wID=MENU_ITEM_COUNTER)
            else: #Por defecto es una cadena
                #print 'item con solo texto!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                wID=MENU_ITEM_COUNTER)                         
            win32gui.InsertMenuItem(self.hmenu, contador, 1, item)
            contador+=1
            #Registrar el elemento creado
            self.nameid[_name]=MENU_ITEM_COUNTER
            self.namecallb[_name]=callback
            MENU_ITEM_COUNTER+=1            
        #print (self.hmenu,self.nameid,self.namecallb)
        return (self.hmenu,self.nameid,self.namecallb)



    def createMenu(self,name,itemlist):
        global MENU_ITEM_COUNTER
        #Cada item de la lista tiene la estructura: [name,callback,type,text,submenu,image]
        menu=win32gui.CreatePopupMenu()
        contador=0
        for item in itemlist:
            #Coger los elementos
            _name=item[0]
            callback=item[1]
            #type
            _type=item[2]
            _text=item[3]
            submenu=None
            image=None
            if item[4] not in ['',0,None]:
                submenu=item[4]
            if item[5] not in ['',None]:
                image=win32gui.LoadImage(0,item[5],win32con.IMAGE_BITMAP,20,20,win32con.LR_LOADFROMFILE | win32con.LR_LOADTRANSPARENT)
                #print 'Cargada imagen %d' %image
            item=extras=None
            if _type in ['-','separator']: #Separador
                #print 'Separador!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                fType=win32con.MFT_SEPARATOR,
                                                wID=MENU_ITEM_COUNTER)                 
            elif image and not submenu:
                #print 'item con imagen + texto!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                hbmpItem=image,
                                                wID=MENU_ITEM_COUNTER)
            elif submenu and image:
                #print 'item con imagen, texto y submenu!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                hbmpItem=image,
                                                hSubMenu=submenu,
                                                wID=MENU_ITEM_COUNTER)
            elif submenu and not image:
                #print 'item con submenu sin imagen!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                hSubMenu=submenu,
                                                wID=MENU_ITEM_COUNTER)
            else: #Por defecto es una cadena
                #print 'item con solo texto!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                wID=MENU_ITEM_COUNTER)                
            #print submenu
            #print image
            win32gui.InsertMenuItem(menu, contador, 1, item)
            contador+=1
            #Registrar el elemento creado
            self.nameid[_name]=MENU_ITEM_COUNTER
            self.namecallb[_name]=callback
            MENU_ITEM_COUNTER+=1
        #Registrar el menu creado
        self.submenus[name]=menu
        return 1


    def createPopupMenu(self,name,itemlist):
        self.tempnamecallb={}
        self.tempnameid={}
        global POPUP_MENU_ITEM_COUNTER
        #Cada item de la lista tiene la estructura: [name,callback,type,text,submenu,image]
        menu=win32gui.CreatePopupMenu()
        contador=0
        for item in itemlist:
            #Coger los elementos
            _name=item[0]
            callback=item[1]
            #type
            _type=item[2]
            _text=item[3]
            submenu=None
            image=None
            if item[4] not in ['',0,None]:
                submenu=item[4]
            if item[5] not in ['',None]:
                image=win32gui.LoadImage(0,item[5],win32con.IMAGE_BITMAP,20,20,win32con.LR_LOADFROMFILE | win32con.LR_LOADTRANSPARENT)
                #print 'Cargada imagen %d' %image
            item=extras=None
            if _type in ['-','separator']: #Separador
                #print 'Separador!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                fType=win32con.MFT_SEPARATOR,
                                                wID=POPUP_MENU_ITEM_COUNTER)                 
            elif image and not submenu:
                #print 'item con imagen + texto!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                hbmpItem=image,
                                                wID=POPUP_MENU_ITEM_COUNTER)
            elif submenu and image:
                #print 'item con imagen, texto y submenu!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                hbmpItem=image,
                                                hSubMenu=submenu,
                                                wID=POPUP_MENU_ITEM_COUNTER)
            elif submenu and not image:
                #print 'item con submenu sin imagen!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                hSubMenu=submenu,
                                                wID=POPUP_MENU_ITEM_COUNTER)
            else: #Por defecto es una cadena
                #print 'item con solo texto!'
                item, extras = win32gui_struct.PackMENUITEMINFO(text=_text,
                                                wID=POPUP_MENU_ITEM_COUNTER)                
            #print submenu
            #print image
            win32gui.InsertMenuItem(menu, contador, 1, item)
            contador+=1
            #Registrar el elemento creado
            self.tempnameid[_name]=POPUP_MENU_ITEM_COUNTER
            self.tempnamecallb[_name]=callback
            POPUP_MENU_ITEM_COUNTER+=1
            if POPUP_MENU_ITEM_COUNTER >= 1122:
                POPUP_MENU_ITEM_COUNTER=1023
        return (menu,self.tempnameid,self.tempnamecallb)

    def getMenu(self,name):
        return self.submenus.get(name,None)

    def getMenuBar(self):
        #print self.hmenu
        return self.hmenu



class WidgetsFactory(object):
    '''
    Crea controles para meter en dialogos
    '''
    def __init__(self):
        self.__control=[]
        self.__style=win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.SS_NOTIFY
        self.__properties={} #textcolor,bgcolor,bgmode
        
    #dlg.append([130, "Enter something", -1, (5, 5, 200, 9), cs | win32con.SS_LEFT])
    def createLabel(self,name,text,xi,yi,xf,yf,align='left',font=None,bgcolor=None,textcolor=None,textbgcolor=None,bgmode=None):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=self.__style
        LABEL_MAGIC=130 #Esto indica que queremos crear un label. Es el mismo IDC para todas???
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop        
        if ALIGN.has_key(align):
            st=self.__style | ALIGN[align]
        self.__control=[LABEL_MAGIC,text,idc,(xi,yi,xf,yf),st]
        #Establecer propiedades si se han pasado
        if bgcolor:
            self.__properties['bgcolor']=bgcolor #Se pasa como colorref
        if textcolor:
            self.__properties['textcolor']=textcolor #Se pasa como colorref
        if textcolor:
            self.__properties['textbgcolor']=textbgcolor #Se pasa como colorref            
        if bgmode:
            self.__properties['bgmode']=bgmode #OPAQUE, TRANSPARENT
        if font:
            self.__properties['font']=font #hfont              
        return [name,idc,self.__control,'label',self.__properties]

    def createTextBox(self,name,xi,yi,xf,yf,text=None,align='left',multiline=1,tabstop=1,font=None,bgcolor=None,textcolor=None,bgmode=None):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=self.__style
        TEXTBOX_MAGIC='EDIT' #Esto indica que queremos crear un textbox.
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        #OJO!!!! El or para que tenga borde TIENE que ser el ultimo o no funciona!!
        st=st |  win32con.WS_BORDER
        #Contemplar que sea multiline
        if multiline:
            #print 'Es multilinea!!'
            st= win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_HSCROLL | win32con.WS_VSCROLL | win32con.WS_BORDER | win32con.WS_TABSTOP | win32con.ES_MULTILINE | win32con.ES_AUTOHSCROLL | win32con.ES_AUTOVSCROLL
        if TEXTBOXALIGN.has_key(align):
            st=st | TEXTBOXALIGN[align]            
        self.__control=[TEXTBOX_MAGIC,name,idc,(xi,yi,xf,yf),st]
        #Establecer propiedades si se han pasado
        if bgcolor:
            self.__properties['bgcolor']=bgcolor #Se pasa como colorref
        if textcolor:
            self.__properties['textcolor']=textcolor #Se pasa como colorref
        if bgmode:
            self.__properties['bgmode']=bgmode #OPAQUE, TRANSPARENT
        if font:
            self.__properties['font']=font #hfont                      
        return [name,idc,self.__control,'textbox',self.__properties]


    def createRichTextBox(self,name,xi,yi,xf,yf,text=None,align='left',tabstop=1):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=self.__style | win32con.ES_AUTOHSCROLL
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        if ALIGN.has_key(align):
            st=self.__style | ALIGN[align]
        #OJO!!!! El or para que tenga borde TIENE que ser el ultimo o no funciona!!
        st=st |  win32con.WS_BORDER
        ##self.__control=["msctls_trackbar32",'',idc,(xi,yi,xf,yf),st]#Plantilla para controles
        self.__control=["RICHEDIT20A",name,idc,(xi,yi,xf,yf),st]
        return [name,idc,self.__control,'richtextbox',self.__properties]


    def createListBox(self,name,xi,yi,xf,yf,align='left',tabstop=1,font=None,bgcolor=None,textcolor=None,bgmode=None):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=self.__style | win32con.LBS_NOTIFY
        LISTBOX_MAGIC='LISTBOX' #Esto indica que queremos crear un listbox.
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        if ALIGN.has_key(align):
            st=st | ALIGN[align]
        #OJO!!!! El or para que tenga borde TIENE que ser el ultimo o no funciona!!
        st=st |  win32con.WS_BORDER
        self.__control=[LISTBOX_MAGIC,name,idc,(xi,yi,xf,yf),st]#HAY QUE PONER UN TEXTO O NO LO EJECUTA!!!!
        #Establecer propiedades si se han pasado
        if bgcolor:
            self.__properties['bgcolor']=bgcolor #Se pasa como colorref
        if textcolor:
            self.__properties['textcolor']=textcolor #Se pasa como colorref
        if bgmode:
            self.__properties['bgmode']=bgmode #OPAQUE, TRANSPARENT
        if font:
            self.__properties['font']=font #hfont         
        return [name,idc,self.__control,'listbox',self.__properties]


    def createComboBox(self,name,xi,yi,xf,yf,align='left',tabstop=1,font=None,bgcolor=None,textcolor=None,bgmode=None):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=self.__style | win32con.CBS_DROPDOWNLIST | win32con.CBS_SORT | win32con.WS_VSCROLL
        COMBOBOX_MAGIC='COMBOBOX' #Esto indica que queremos crear un combobox.
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        if ALIGN.has_key(align):
            st=st | ALIGN[align]
        #OJO!!!! El or para que tenga borde TIENE que ser el ultimo o no funciona!!
        st=st |  win32con.WS_BORDER
        self.__control=[COMBOBOX_MAGIC,name,idc,(xi,yi,xf,yf),st] #HAY QUE POENER UN TEXTO O NO LO EJECUTA!!!!
        #Establecer propiedades si se han pasado
        if bgcolor:
            self.__properties['bgcolor']=bgcolor #Se pasa como colorref
        if textcolor:
            self.__properties['textcolor']=textcolor #Se pasa como colorref
        if bgmode:
            self.__properties['bgmode']=bgmode #OPAQUE, TRANSPARENT
        if font:
            self.__properties['font']=font #hfont               
        return [name,idc,self.__control,'combobox',self.__properties]



    def createFrameBox(self,name,xi,yi,xf,yf,text,align='center',tabstop=1,font=None,bgcolor=None,textcolor=None,bgmode=None): ##NO FUNCIONA!!!
        global IDC_COUNTER
        self.__properties={}
        st=self.__style | win32con.BS_GROUPBOX | win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_GROUP
        FRAMEBOX_MAGIC=128 #Esto indica que queremos crear un listbox.
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        if tabstop:
            st= st | win32con.WS_TABSTOP        
        if ALIGN.has_key(align):
            st=self.__style | ALIGN[align]
        #OJO!!!! El or para que tenga borde TIENE que ser el ultimo o no funciona!!
        #st=st |  win32con.WS_BORDER
        self.__control=['BUTTON',text,idc,(xi,yi,xf,yf),st]#HAY QUE PONER UN TEXTO O NO LO EJECUTA!!!!
        #Establecer propiedades si se han pasado
        if bgcolor:
            self.__properties['bgcolor']=bgcolor #Se pasa como colorref
        if textcolor:
            self.__properties['textcolor']=textcolor #Se pasa como colorref
        if bgmode:
            self.__properties['bgmode']=bgmode #OPAQUE, TRANSPARENT
        if font:
            self.__properties['font']=font #hfont             
        return [name,idc,self.__control,'framebox',self.__properties]



    def createButton(self,name,xi,yi,xf,yf,label,align='center',default=0,tabstop=1,font=None,bgcolor=None,textcolor=None,bgmode=None):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=win32con.BS_PUSHBUTTON | self.__style
        if default:
            #print 'Cambiado a boton por defecto!!'
            st=win32con.BS_DEFPUSHBUTTON | self.__style
        
        BUTTON_MAGIC=128 #Esto indica que queremos crear un boton
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        if ALIGN.has_key(align):
            st=st | ALIGN[align]
        self.__control=[BUTTON_MAGIC,label,idc,(xi,yi,xf,yf),st]
        #Establecer propiedades si se han pasado
        if bgcolor:
            self.__properties['bgcolor']=bgcolor #Se pasa como colorref
        if textcolor:
            self.__properties['textcolor']=textcolor #Se pasa como colorref
        if bgmode:
            self.__properties['bgmode']=bgmode #OPAQUE, TRANSPARENT
        if font:
            self.__properties['font']=font #hfont           
        return [name,idc,self.__control,'button',self.__properties]



    def createCheckBox(self,name,xi,yi,xf,yf,label,align='center',tabstop=1,font=None,bgcolor=None,textcolor=None,bgmode=None):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=win32con.BS_CHECKBOX | self.__style
        BUTTON_MAGIC=128 #Esto indica que queremos crear un textbox.
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        if ALIGN.has_key(align):
            st=st | ALIGN[align]
        self.__control=[BUTTON_MAGIC,label,idc,(xi,yi,xf,yf),st]
        #Establecer propiedades si se han pasado
        if bgcolor:
            self.__properties['bgcolor']=bgcolor #Se pasa como colorref
        if textcolor:
            self.__properties['textcolor']=textcolor #Se pasa como colorref
        if bgmode:
            self.__properties['bgmode']=bgmode #OPAQUE, TRANSPARENT
        if font:
            self.__properties['font']=font #hfont             
        return [name,idc,self.__control,'checkbox',self.__properties]


    def createRadioBox(self,name,xi,yi,xf,yf,label,align='center',tabstop=1,font=None,bgcolor=None,textcolor=None,bgmode=None): ##NO REVISADA!!!!
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=win32con.BS_CHECKBOX | self.__style
        BUTTON_MAGIC=128 #Esto indica que queremos crear un textbox.
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        if ALIGN.has_key(align):
            st=st | ALIGN[align]
        self.__control=[BUTTON_MAGIC,label,idc,(xi,yi,xf,yf),st]
        #Establecer propiedades si se han pasado
        if bgcolor:
            self.__properties['bgcolor']=bgcolor #Se pasa como colorref
        if textcolor:
            self.__properties['textcolor']=textcolor #Se pasa como colorref
        if bgmode:
            self.__properties['bgmode']=bgmode #OPAQUE, TRANSPARENT
        if font:
            self.__properties['font']=font #hfont                 
        return [name,idc,self.__control,'radiobox',self.__properties]


    def createScrollBar(self,name,xi,yi,xf,yf,label,align='center',tabstop=1,font=None,bgcolor=None,textcolor=None,bgmode=None): ##NO REVISADA!!!!
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=win32con.BS_CHECKBOX | self.__style
        BUTTON_MAGIC=128 #Esto indica que queremos crear un textbox.
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        if ALIGN.has_key(align):
            st=st | ALIGN[align]
        self.__control=[BUTTON_MAGIC,label,idc,(xi,yi,xf,yf),st]
        #Establecer propiedades si se han pasado
        if bgcolor:
            self.__properties['bgcolor']=bgcolor #Se pasa como colorref
        if textcolor:
            self.__properties['textcolor']=textcolor #Se pasa como colorref
        if bgmode:
            self.__properties['bgmode']=bgmode #OPAQUE, TRANSPARENT
        if font:
            self.__properties['font']=font #hfont                
        return [name,idc,self.__control,'scrollbar',self.__properties]



    def createSlider(self,name,xi,yi,xf,yf,tabstop=1):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=self.__style
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        self.__control=["msctls_trackbar32",name,idc,(xi,yi,xf,yf),st]
        return [name,idc,self.__control,'slider',self.__properties]
    

    def createSpinControl(self,name,xi,yi,xf,yf,tabstop=1):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=self.__style
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        self.__control=["msctls_updown32",name,idc,(xi,yi,xf,yf),st]
        return [name,idc,self.__control,'spin',self.__properties]


    def createProgressBar(self,name,xi,yi,xf,yf):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=self.__style
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        self.__control=["msctls_progress32",name,idc,(xi,yi,xf,yf),st]
        return [name,idc,self.__control,'progress',self.__properties]


    def createListView(self,name,xi,yi,xf,yf,kind,multisel=0,tabstop=1):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_BORDER | win32con.WS_HSCROLL | win32con.WS_VSCROLL
        if not multisel:
            st|=commctrl.LVS_SINGLESEL
        st|=commctrl.LVS_SHOWSELALWAYS
        #Tipo de vista
        if kind=='report':
            st|=commctrl.LVS_REPORT
        elif kind=='iconlist':
            st|=commctrl.LVS_ICON
        elif kind=='smallicon':
            st|=commctrl.LVS_SMALLICON
        elif kind=='list':
            st|=commctrl.LVS_LIST
        else: #Por defecto report
            st|=commctrl.LVS_REPORT
        st|=commctrl.LVS_EDITLABELS #Por defecto las celdas pueden editarse
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        self.__control=["SysListView32",name,idc,(xi,yi,xf,yf),st]
        return [name,idc,self.__control,'listview',self.__properties]


    def createTreeView(self,name,xi,yi,xf,yf,tabstop=1):
        global IDC_COUNTER
        global ALIGN
        self.__properties={}
        st=self.__style | commctrl.TVE_EXPAND
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        self.__control=["SysTreeView32",name,idc,(xi,yi,xf,yf),st]
        return [name,idc,self.__control,'treeview',self.__properties]
    

    def createTabControl(self,name,xi,yi,xf,yf,tabstop=1):
        global IDC_COUNTER
        self.__properties={}
        st=self.__style | win32con.WS_BORDER
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        self.__control=["SysTabControl32",name,idc,(xi,yi,xf,yf),st]
        return [name,idc,self.__control,'tabcontrol',self.__properties]


    def createDateTimePicker(self,name,xi,yi,xf,yf,tabstop=1):
        global IDC_COUNTER
        self.__properties={}
        st=win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.DTS_RIGHTALIGN #No usar self.__style
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        self.__control=["SysDateTimePick32",name,idc,(xi,yi,xf,yf),st]
        return [name,idc,self.__control,'timepicker',self.__properties]
    

    def createMonthCalendar(self,name,xi,yi,xf,yf,tabstop=1):
        global IDC_COUNTER
        self.__properties={}
        st=win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.MCS_NOTODAY #No usar self.__style
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        #Contemplar que sea tabstop
        if tabstop:
            st= st | win32con.WS_TABSTOP
        self.__control=["SysMonthCal32",name,idc,(xi,yi,xf,yf),st]
        return [name,idc,self.__control,'calendar',self.__properties]

    def createStatusBar(self,name,xi,yi,xf,yf): #Esto no funciona!!!!!
        global IDC_COUNTER
        self.__properties={}
        st=win32con.WS_CHILD | win32con.WS_VISIBLE #No usar self.__style
        #Generar un id para el control
        idc=IDC_COUNTER
        #incrementar generador de ids
        IDC_COUNTER+=1
        self.__control=["msctls_statusbar32",name,idc,(xi,yi,xf,yf),st]
        return [name,idc,self.__control,'statusbar',self.__properties]

##----------Clases envoltorio para controles--------------------------------
class ControlAccessException(Exception): pass



class StaticText(object):
    #Envoltorio sobre un control StaticText
    def __init__(self,name,hwnd,parent):
        self.name=name
        self.hwnd=hwnd
        self.type='static'
        self.parent=parent

    def getText(self):
        #Devuelve el texto contenido en el StaticText
        return win32gui.GetWindowText(self.hwnd)

    def setText(self,text):
        #Cambia el texto contenido en el StaticText
        return win32gui.SetWindowText(self.hwnd,text)

    def disable(self):
        win32gui.EnableWindow(self.hwnd,False)

    def enable(self):
        #Esta en user32, por si se necesita para usar ctypes.
        win32gui.EnableWindow(self.hwnd,True)

    def isEnabled(self):
        #Esta en user32, por si se necesita para usar ctypes.
        return win32gui.IsWindowEnabled(self.hwnd)    

    def setFont(self,hfont): #hfont es una fuente creada con fontFactory()
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['font']=hfont        
        win32gui.SendMessage(self.hwnd,win32con.WM_SETFONT,hfont,0)
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)

    def getFont(self):
        return self.parent.getControlProperties(self.name).get('font',None)

    def getBgColor(self):
        return self.parent.getControlProperties(self.name).get('bgcolor',None)   

    def setBgColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['bgcolor']=color        
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)

    def getBgMode(self):
        return self.parent.getControlProperties(self.name).get('bgmode',None)

    def setBgMode(self,mode):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['bgmode']=mode        
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)

    def getTextColor(self):
        return self.parent.getControlProperties(self.name).get('textcolor',None)    

    def setTextColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['textcolor']=color        
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)

    def getTextBgColor(self):
        return self.parent.getControlProperties(self.name).get('textbgcolor',None)    

    def setTextBgColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['textbgcolor']=color        
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)


class TextBox(object):
    #Envoltorio sobre un control StaticText
    def __init__(self,name,hwnd,parent):
        self.name=name
        self.hwnd=hwnd
        self.type='static'
        self.parent=parent

    def getText(self):
        #Devuelve el texto contenido en el StaticText
        return win32gui.GetWindowText(self.hwnd)

    def setText(self,text):
        #Cambia el texto contenido en el StaticText
        return win32gui.SetWindowText(self.hwnd,text)

    def disable(self):
        win32gui.EnableWindow(self.hwnd,False)

    def enable(self):
        #Esta en user32, por si se necesita para usar ctypes.
        win32gui.EnableWindow(self.hwnd,True)

    def isEnabled(self):
        #Esta en user32, por si se necesita para usar ctypes.
        return win32gui.IsWindowEnabled(self.hwnd)    

    def setFont(self,hfont): #hfont es una fuente creada con fontFactory()
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['font']=hfont        
        win32gui.SendMessage(self.hwnd,win32con.WM_SETFONT,hfont,0)
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)

    def getFont(self):
        return self.parent.getControlProperties(self.name).get('font',None)

    def getBgColor(self):
        return self.parent.getControlProperties(self.name).get('bgcolor',None)   

    def setBgColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['bgcolor']=color        
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)

    def getBgMode(self):
        return self.parent.getControlProperties(self.name).get('bgmode',None)

    def setBgMode(self,mode):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['bgmode']=mode        
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)

    def getTextColor(self):
        return self.parent.getControlProperties(self.name).get('textcolor',None)    

    def setTextColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['textcolor']=color        
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)

    def getTextBgColor(self):
        return self.parent.getControlProperties(self.name).get('textbgcolor',None)    

    def setTextBgColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['textbgcolor']=color        
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)

class Button(object):
    #Envoltorio sobre un control Button
    def __init__(self,name,hwnd,parent):
        self.name=name
        self.hwnd=hwnd
        self.type='button'
        self.parent=parent        

    def getText(self):
        #Devuelve el texto contenido en el StaticText
        return win32gui.GetWindowText(self.hwnd)

    def setText(self,text):
        #Cambia el texto contenido en el StaticText
        return win32gui.SetWindowText(self.hwnd,text)

    def disable(self):
        #win32gui.SendMessage(self.hwnd,win32con.BN_DISABLE,0,0)
        win32gui.EnableWindow(self.hwnd,False)

    def enable(self):
        #Esta en user32, por si se necesita para usar ctypes.
        win32gui.EnableWindow(self.hwnd,True)

    def isEnabled(self):
        #Esta en user32, por si se necesita para usar ctypes.
        return win32gui.IsWindowEnabled(self.hwnd)              

    def click(self):
        win32gui.SendMessage(self.hwnd,win32con.BM_CLICK,0,0)   

    def setFont(self,hfont):#hfont es una fuente creada con fontFactory()
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['font']=hfont
        win32gui.SendMessage(self.hwnd,win32con.WM_SETFONT,hfont,0)
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)

    def setBgColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['bgcolor']=color                
        hdc = win32gui.GetDC(self.hwnd);
        win32gui.SendMessage(self.parent.hwnd,win32con.WM_CTLCOLORBTN,hdc,self.hwnd)

    def getFont(self):
        return self.parent.getControlProperties(self.name).get('font',None)


    def getBgColor(self):
        return self.parent.getControlProperties(self.name).get('bgcolor',None)   


    def getBgMode(self):
        return self.parent.getControlProperties(self.name).get('bgmode',None)


    def setBgMode(self,mode):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['bgmode']=mode        
        hdc = win32gui.GetDC(self.hwnd);
        win32gui.SendMessage(self.parent.hwnd,win32con.WM_CTLCOLORBTN,hdc,self.hwnd)


    def getTextColor(self):
        return self.parent.getControlProperties(self.name).get('textcolor',None)    


    def setTextColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['textcolor']=color        
        hdc = win32gui.GetDC(self.hwnd);
        win32gui.SendMessage(self.parent.hwnd,win32con.WM_CTLCOLORBTN,hdc,self.hwnd)

        
    def getTextBgColor(self):
        return self.parent.getControlProperties(self.name).get('textbgcolor',None)    


    def setTextBgColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['textbgcolor']=color        
        hdc = win32gui.GetDC(self.hwnd);
        win32gui.SendMessage(self.parent.hwnd,win32con.WM_CTLCOLORBTN,hdc,self.hwnd)



class CheckBox(object):
    #Envoltorio sobre un control Button
    def __init__(self,name,hwnd,parent):
        self.name=name
        self.hwnd=hwnd
        self.type='checkbox'
        self.parent=parent        

    def getText(self):
        #Devuelve el texto contenido en el StaticText
        return win32gui.GetWindowText(self.hwnd)

    def setText(self,text):
        #Cambia el texto contenido en el StaticText
        return win32gui.SetWindowText(self.hwnd,text)

    def isChecked(self):
        status=win32gui.SendMessage(self.hwnd,win32con.BM_GETCHECK,0,0)
        if status==win32con.BST_CHECKED:
            return 1
        else:
            return 0
        
    def setChecked(self,status):
        if status==1:
            return win32gui.SendMessage(self.hwnd,win32con.BM_SETCHECK,win32con.BST_CHECKED,0)
        elif status==0:
            return win32gui.SendMessage(self.hwnd,win32con.BM_SETCHECK,win32con.BST_UNCHECKED,0)
        elif status==-1:
            return win32gui.SendMessage(self.hwnd,win32con.BM_SETCHECK,win32con.BST_INDETERMINATE,0)
            

    def disable(self):
        win32gui.SendMessage(self.hwnd,win32con.BN_DISABLE,0,0)

    def isChecked(self):
        win32gui.SendMessage(self.hwnd,win32con.BN_CLICKED,0,0)   

    def setFont(self,hfont):#hfont es una fuente creada con fontFactory()
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['font']=hfont
        win32gui.SendMessage(self.hwnd,win32con.WM_SETFONT,hfont,0)
        #Obligar a que se repinte (hay que invalidar toda el area cliente del parent!!)
        win32gui.InvalidateRect(self.parent.hwnd,win32gui.GetClientRect(self.parent.hwnd),1)

    def setBgColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['bgcolor']=color                
        hdc = win32gui.GetDC(self.hwnd);
        win32gui.SendMessage(self.parent.hwnd,win32con.WM_CTLCOLORBTN,hdc,self.hwnd)

    def getFont(self):
        return self.parent.getControlProperties(self.name).get('font',None)


    def getBgColor(self):
        return self.parent.getControlProperties(self.name).get('bgcolor',None)   


    def getBgMode(self):
        return self.parent.getControlProperties(self.name).get('bgmode',None)


    def setBgMode(self,mode):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['bgmode']=mode        
        hdc = win32gui.GetDC(self.hwnd);
        win32gui.SendMessage(self.parent.hwnd,win32con.WM_CTLCOLORBTN,hdc,self.hwnd)


    def getTextColor(self):
        return self.parent.getControlProperties(self.name).get('textcolor',None)    


    def setTextColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['textcolor']=color
        print self.parent,getControlProperties(self.name)
        hdc = win32gui.GetDC(self.hwnd);
        win32gui.SendMessage(self.parent.hwnd,win32con.WM_CTLCOLORBTN,hdc,self.hwnd)

        
    def getTextBgColor(self):
        return self.parent.getControlProperties(self.name).get('textbgcolor',None)    


    def setTextBgColor(self,color):
        #Cambiar el valor de font en las propiedades del control por el nuevo
        self.parent.getControlProperties(self.name)['textbgcolor']=color        
        hdc = win32gui.GetDC(self.hwnd);
        win32gui.SendMessage(self.parent.hwnd,win32con.WM_CTLCOLORBTN,hdc,self.hwnd)



class RadioButton(object):
    #Envoltorio sobre un control Button
    def __init__(self,name,hwnd,parent):
        self.name=name
        self.hwnd=hwnd
        self.type='radio'
        self.parent=parent        

    def getText(self):
        #Devuelve el texto contenido en el StaticText
        return win32gui.GetWindowText(self.hwnd)

    def setText(self,text):
        #Cambia el texto contenido en el StaticText
        return win32gui.SetWindowText(self.hwnd,text)

    def isChecked(self):
        status=win32gui.SendMessage(self.hwnd,win32con.BM_GETCHECK,0,0)
        if status==win32con.BST_CHECKED:
            return 1
        else:
            return 0
        
    def setChecked(self,status):
        if status==1:
            return win32gui.SendMessage(self.hwnd,win32con.BM_SETCHECK,win32con.BST_CHECKED,0)
        elif status==0:
            return win32gui.SendMessage(self.hwnd,win32con.BM_SETCHECK,win32con.BST_UNCHECKED,0)
        elif status==-1:
            return win32gui.SendMessage(self.hwnd,win32con.BM_SETCHECK,win32con.BST_INDETERMINATE,0)
            

    def disable(self):
        win32gui.SendMessage(self.hwnd,win32con.BN_DISABLE,0,0)

    def isChecked(self):
        win32gui.SendMessage(self.hwnd,win32con.BN_CLICKED,0,0)   

    def setFont(self,font):
        pass

    def setBgColor(self,color):
        pass    


class ProgressBar(object):
    #Envoltorio sobre un control ProgressBar
    def __init__(self,name,hwnd,parent):
        self.name=name
        self.hwnd=hwnd
        self.type='progress'
        self.parent=parent        

    def setStep(self,increment):
        #Establece el incremento
        return win32gui.SendMessage(self.hwnd,commctrl.PBM_SETSTEP,increment,0)

    def setRange(self,min,max):
        #Establece el rango
        return win32gui.SendMessage(self.hwnd,commctrl.PBM_SETRANGE,0,win32api.MAKELONG(min,max))
    
    def setPos(self,pos):
        #Establece el rango
        return win32gui.SendMessage(self.hwnd,commctrl.PBM_SETPOS,pos,0)    

    def stepIt(self):
        #Hace que avance una posicion
        return win32gui.SendMessage(self.hwnd,commctrl.PBM_STEPIT,0,0)

    def stepDelta(self,delta):
        #Hace que avance una posicion
        return win32gui.SendMessage(self.hwnd,commctrl.PBM_DELTAPOS,delta,0)    

    def disable(self):
        pass

    def setFont(self,font):
        pass

    def setBgColor(self,color):
        pass



class ListBox(object):
    #Envoltorio sobre un control Button
    def __init__(self,name,hwnd,parent):
        self.name=name
        self.hwnd=hwnd
        self.type='listbox'
        self.parent=parent        

    def addString(self,cad):
        #Pone una nueva linea en la lista
        return win32gui.SendMessage(self.hwnd,win32con.LB_ADDSTRING,0,cad)

    def insertString(self,cad,pos):
        #Pone una nueva linea en la lista en la posicion pos
        return win32gui.SendMessage(self.hwnd,win32con.LB_INSERTSTRING,pos,cad)

    def findString(self,cad,pos):
        #Pone una nueva linea en la lista en la posicion pos
        return win32gui.SendMessage(self.hwnd,win32con.LB_FINDSTRING,pos,cad)        

    def deleteString(self,pos):
        #Pone una nueva linea en la lista en la posicion pos
        return win32gui.SendMessage(self.hwnd,win32con.LB_DELETESTRING,pos,0)

    def addStringList(self,text_list):
        #Pone todas las lineas en la lista
        for line in text_list:
            self.addString(line)
        return 1

    def addStringListAt(self,text_list,pos):
        #Pone todas las lineas en la lista en la posicion pos
        for line in text_list:
            self.insertString(line,pos)
        return 1

    def getCurSel(self):
        #Pone una nueva linea en la lista en la posicion pos
        return win32gui.SendMessage(self.hwnd,win32con.LB_GETCURSEL,0,0)


    def setCurSel(self,pos):
        #Pone una nueva linea en la lista en la posicion pos
        return win32gui.SendMessage(self.hwnd,win32con.LB_SETCURSEL,pos,0)


    def getItemText(self,pos):
        #Devuelve el texto en la posicion pos
        #1.-Calcular la longitud del buffer
        txtl=win32gui.SendMessage(self.hwnd,win32con.LB_GETTEXTLEN,pos,0)
        #2.-Crear el buffer y obtener el texto
        buf='x'* txtl
        #3.-Coger el texto en el buffer
        win32gui.SendMessage(self.hwnd,win32con.LB_GETTEXT,pos,buf)
        return buf

    def getSelectedString(self):
        return self.getItemText(self.getCurSel())

    def getNumEls(self):
        #Devuelve el numero de elementos en la lista
        return win32gui.SendMessage(self.hwnd,win32con.LB_GETCOUNT,0,0)


    def disable(self):
        pass

    def setFont(self,font):
        pass

    def setBgColor(self,color):
        pass


class ComboBox(object):
    #Envoltorio sobre un control Combobox
    def __init__(self,name,hwnd,parent):
        self.name=name
        self.hwnd=hwnd
        self.type='combobox'
        self.parent=parent        

    def addString(self,cad):
        #Pone una nueva linea en la lista
        return win32gui.SendMessage(self.hwnd,win32con.CB_ADDSTRING,0,cad)

    def insertString(self,cad,pos):
        #Pone una nueva linea en la lista en la posicion pos
        return win32gui.SendMessage(self.hwnd,win32con.CB_INSERTSTRING,pos,cad)

    def findString(self,cad,pos):
        #Pone una nueva linea en la lista en la posicion pos
        return win32gui.SendMessage(self.hwnd,win32con.CB_FINDSTRING,pos,cad)        

    def deleteString(self,pos):
        #Pone una nueva linea en la lista en la posicion pos
        return win32gui.SendMessage(self.hwnd,win32con.CB_DELETESTRING,pos,0)

    def addStringList(self,text_list):
        #Pone todas las lineas en la lista
        for line in text_list:
            self.addString(line)
        return 1

    def addStringListAt(self,text_list,pos):
        #Pone todas las lineas en la lista en la posicion pos
        for line in text_list:
            self.insertString(line,pos)
        return 1

    def getCurSel(self):
        #Pone una nueva linea en la lista en la posicion pos
        return win32gui.SendMessage(self.hwnd,win32con.CB_GETCURSEL,0,0)


    def setCurSel(self,pos):
        #Pone una nueva linea en la lista en la posicion pos
        return win32gui.SendMessage(self.hwnd,win32con.CB_SETCURSEL,pos,0)


    def getItemText(self,pos):
        #Devuelve el texto en la posicion pos
        #1.-Calcular la longitud del buffer
        txtl=win32gui.SendMessage(self.hwnd,win32con.CB_GETLBTEXTLEN,pos,0)
        #2.-Crear el buffer y obtener el texto
        buf='x'* txtl
        #3.-Coger el texto en el buffer
        win32gui.SendMessage(self.hwnd,win32con.CB_GETLBTEXT,pos,buf)
        return buf

    def getSelectedString(self):
        return self.getItemText(self.getCurSel())

    def getNumEls(self):
        #Devuelve el numero de elementos en la lista
        return win32gui.SendMessage(self.hwnd,win32con.CB_GETCOUNT,0,0)

    def disable(self):
        pass

    def setFont(self,font):
        pass

    def setBgColor(self,color):
        pass



class ListView(object):
    #Envoltorio sobre un control ListView
    def __init__(self,name,hwnd,parent):
        self.name=name
        self.hwnd=hwnd
        self.type='listview'
        self.parent=parent
        #Inicializar el control
        child_ex_style = win32gui.SendMessage(self.hwnd, commctrl.LVM_GETEXTENDEDLISTVIEWSTYLE, 0, 0)
        child_ex_style |= commctrl.LVS_EX_FULLROWSELECT
        ##child_ex_style |= commctrl.LVS_EDITLABELS #?????
        win32gui.SendMessage(self.hwnd, commctrl.LVM_SETEXTENDEDLISTVIEWSTYLE, 0, child_ex_style)
        

    def insertColumn(self,label,pos=0,width=80,align='left'):
        # Inserta una columna en el listview en modo report
        lvc = LVCOLUMN(mask = commctrl.LVCF_FMT | commctrl.LVCF_WIDTH | commctrl.LVCF_TEXT | commctrl.LVCF_SUBITEM)
        if align=='left':
            lvc.fmt = commctrl.LVCFMT_LEFT
        elif align=='right':
            lvc.fmt = commctrl.LVCFMT_RIGHT
        elif align in ['center','centre']:
            lvc.fmt = commctrl.LVCFMT_CENTER
        else:
            lvc.fmt = commctrl.LVCFMT_LEFT
        lvc.iSubItem = pos
        lvc.text = label
        lvc.cx = width
        win32gui.SendMessage(self.hwnd, commctrl.LVM_INSERTCOLUMN, 0, lvc.toparam())


    def insertColumnList(self,label_list,width=100,align='left'):
        label_list.reverse() #Asi se insertan en el orden correcto!!
        for label in label_list:
            self.insertColumn(label,0,width,align)
        

    def clearItems(self):
        win32gui.SendMessage(self.hwnd, commctrl.LVM_DELETEALLITEMS)

    def addItem(self,columns,image=''):
        num_items = win32gui.SendMessage(self.hwnd, commctrl.LVM_GETITEMCOUNT)
        #print 'NUM_ITEMS_LV=%d\n' %num_items
        item = LVITEM(text=columns[0], iItem = num_items)
        new_index = win32gui.SendMessage(self.hwnd, commctrl.LVM_INSERTITEM, 0, item.toparam())
        col_no = 1
        for col in columns[1:]:
            item = LVITEM(text=col, iItem = new_index, iSubItem = col_no)
            win32gui.SendMessage(self.hwnd, commctrl.LVM_SETITEM, 0, item.toparam())
            col_no += 1

    def addItems(self,item_list):
        for item in item_list:
            self.addItem(item)

    def delItem(self,item):
        pass


    def getRowCount(self):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        return lv.ItemCount()        


    def getColCount(self):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        return lv.ColumnCount()
    

    def getCell(self,row,col):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        print lv.GetItem(row,col)
        return lv.GetItem(row, col)['text']


    def setCell(self,row,col,_text):
        item=LVITEM(text=_text,iSubItem=col)
        win32gui.SendMessage(self.hwnd, commctrl.LVM_SETITEM, row, item.toparam())

    def getCellWidth(self,row,col):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        return lv.GetColumn(col)['width']

    def getCells(self):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        return lv.Texts()[1:]#El primer elemento es el nombre de la lista

    def cells2matrix(self):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        rows=lv.ItemCount()
        cols=lv.ColumnCount()
        cells=lv.Texts()[1:]
        mtx=[]
        #Coger los elementos de cols en cols y meterlos en mtx
        cont=0
        while cont < len(cells):
            mtx.append(cells[cont:cont+cols])
            cont+=cols
        return Matrix(mtx)


    def getHeaderCell(self,col):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        return lv.GetColumn(col)['text']

    def getHeaderCellWidth(self,col):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        return lv.GetColumn(col)['width']
    
    def getHeaderCells(self):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        return [el['text'] for el in lv.Columns()]

    
    def addImageList(self,icon_path_list=[]):
        # Add an image list - use the builtin shell folder icon - this
        # demonstrates the problem with alpha-blending of icons on XP if
        # winxpgui is not used in place of win32gui.
        if not icon_path_list:
            il = win32gui.ImageList_Create(
                        win32api.GetSystemMetrics(win32con.SM_CXSMICON),
                        win32api.GetSystemMetrics(win32con.SM_CYSMICON),
                        commctrl.ILC_COLOR32 | commctrl.ILC_MASK,
                        1, # initial size
                        0) # cGrow

            shell_dll = os.path.join(win32api.GetSystemDirectory(), "shell32.dll")
            large, small = win32gui.ExtractIconEx(shell_dll, 4, 1)
            win32gui.ImageList_ReplaceIcon(il, -1, small[0])
            win32gui.DestroyIcon(small[0])
            win32gui.DestroyIcon(large[0])
            win32gui.SendMessage(self.hwnd, commctrl.LVM_SETIMAGELIST,
                                 commctrl.LVSIL_SMALL, il)
        else:
            il = win32gui.ImageList_Create(
                        win32api.GetSystemMetrics(win32con.SM_CXSMICON),
                        win32api.GetSystemMetrics(win32con.SM_CYSMICON),
                        commctrl.ILC_COLOR32 | commctrl.ILC_MASK,
                        len(icon_path_list), # initial size
                        0) # cGrow
            for item in icon_path_list:
                #Cargar cada icono y meterlo en la lista
                pass


    def selectRow(self,row):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        lv.Select(row)

    def deselectRow(self,row):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        lv.Deselect(row)

    def getSelectedCount(self):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        return lv.GetSelectedCount()

    def checkRow(self,row):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        lv.Check(row)

    def uncheckRow(self,row):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        lv.UnCheck(row)    
        
    def disable(self):
        win32gui.EnableWindow(self.hwnd,0)
        return 1

    def enable(self):
        win32gui.EnableWindow(self.hwnd,1)
        return 1
    
    def isEnabled(self):
        return win32gui.IsWindowEnabled(self.hwnd)

    def getFont(self):
        pass

    def setFont(self,font):
        pass

    def editLabel(self,item):
        win32gui.SetFocus(self.hwnd)
        win32gui.SendMessage(self.hwnd, commctrl.LVM_EDITLABEL,item,0)


    def getTextColor(self):
        bgcol=win32gui.SendMessage(self.hwnd, commctrl.LVM_GETTEXTCOLOR,0,0)
        return bgcol

    def setTextColor(self,r,g,b):
        colorref=win32api.RGB(r,g,b)
        bgcol=win32gui.SendMessage(self.hwnd, commctrl.LVM_SETTEXTCOLOR,0,colorref)
        return 1


    def getBgColor(self):
        bgcol=win32gui.SendMessage(self.hwnd, commctrl.LVM_GETBKCOLOR,0,0)
        return bgcol

    def setBgColor(self,r,g,b):
        colorref=win32api.RGB(r,g,b)
        bgcol=win32gui.SendMessage(self.hwnd, commctrl.LVM_SETBKCOLOR,0,colorref)
        return 1

    def getTextBgColor(self): #que hace esto???
        bgcol=win32gui.SendMessage(self.hwnd, commctrl.LVM_GETTEXTBKCOLOR,0,0)
        return bgcol

    def setTextBgColor(self,r,g,b): #que hace esto???
        colorref=win32api.RGB(r,g,b)
        bgcol=win32gui.SendMessage(self.hwnd, commctrl.LVM_SETTEXTBKCOLOR,0,colorref)
        return 1

    def getRect(self):
        ph=win32gui.GetParent(self.hwnd)
        l,t,r,b = win32gui.GetWindowRect(self.hwnd)
        lc,tc=win32gui.ScreenToClient(ph,(l,t))
        rc,bc=win32gui.ScreenToClient(ph,(r,b))
        return [lc,tc,rc,bc]
    
    def getWidth(self):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        r=lv.ClientRect()    
        return r.width()

    def getHeight(self):
        lv=pywinauto.controls.common_controls.ListViewWrapper(self.hwnd)
        r=lv.ClientRect()    
        return r.height()

    def hasPoint(self,x,y):
        l,t,r,b=win32gui.GetWindowRect(self.hwnd) #El cursor viene en screen coordinates!!
        if x>=l and x<=r and y>=t and y<=b:
            return 1
        else:
            return 0

class TreeView(object):
    #Envoltorio sobre un control ListView
    pass


##------------------------------------------------------------------------------    

if __name__=='__main__':
    tpl=DialogTemplateFactory('myTemplate')
    print tpl.getDialogTemplate()
    ft=fontFactory('Arial',12)