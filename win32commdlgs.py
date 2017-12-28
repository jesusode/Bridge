#Clases envoltorio sobre los dialogos comunes para fuentes, colores e impresoras

import win32ui
import win32api
import win32con

##Funciones de utilidad para conversion de colores###

def checkHex(_hex):
    #Ajusta a 6 con ceros a la izquierda la cadena hexadecimal
    #y quita el # o el 0x que pueda tener como prefijo
    _hex=_hex.lstrip('#')
    _hex=_hex.lstrip('0x')
    if len(_hex)<6:
        for i in range(6-len(_hex)):
            _hex= '0' + _hex
    print _hex
    return _hex


def colorref2hex(colorref):
    c='%06x' %colorref
    b=c[0:2]
    g=c[2:4]
    r=c[4:6]
    c=r+g+b
    return c


def colorref2rgb(colorref):
    h=colorref2hex(colorref)
    r=eval('0x' + h[0:2])
    g=eval('0x' + h[2:4])
    b=eval('0x' + h[4:6])
    return [r,g,b]


def hex2colorref(_hex):
    _hex=checkHex(_hex)
    r=_hex[0:2]
    g=_hex[2:4]
    b=_hex[4:6]
    c=b+g+r
    v=eval('0x' + c)
    if v:
        print 'Devuelve v'
        return v
    else:
        print 'Devuelve -1'
        return -1



def hex2rgb(_hex):
    _hex=checkHex(_hex)
    r=eval('0x' + _hex[0:2])
    g=eval('0x' + _hex[2:4])
    b=eval('0x' + _hex[4:6])
    return [r,g,b]


def rgb2hex(r,g,b):
    return '%02x%02x%02x' % (r,g,b)


def rgb2colorref(r,g,b):
    return win32api.RGB(r,g,b)
    
##Fin##

class ColorsDialog(object):
    def __init__(self, _initColor=0, _flags=0 , _parent=None ):
        self.initColor=_initColor
        self.flags=_flags
        self.parent=_parent
        self.color=0
        self.hexcolor='000000'
        self.rgbcolor=[0,0,0]
        self.customcolors=[]
        self.dlg=win32ui.CreateColorDialog(self.initColor,self.flags,self.parent)


    def setColor(self,r,g,b):
        colorref=win32api.RGB(r,g,b)
        if not self.dlg:
            self.dlg=win32ui.CreateColorDialog(self.initColor,self.flags,self.parent)
        self.dlg.SetColor(colorref)


    def setCustomColors(self,*colors):
        if len(colors)==0: return
        if not self.dlg:
            self.dlg=win32ui.CreateColorDialog(self.initColor,self.flags,self.parent)
        #Solo se pueden tener 16 colores definidos
        if len(colors)>16:
            colors=colors[0:16]
        self.dlg.SetCustomColors(colors)        


    def show(self):
        if not self.dlg:
            self.dlg=win32ui.CreateColorDialog(self.initColor,self.flags,self.parent)
        #Mostrar el dialogo y guardar la informacion obtenida
        result=self.dlg.DoModal()
        if result!=0: #Si se cancela, devuelve 0
            self.color=self.dlg.GetColor()
            self.customcolors=self.dlg.GetCustomColors()
            #Chapucilla para coger las partes r,g, y b
            #un colorref es 0x00bbggrr
            c='%06x' %self.color
            print c
            b=c[0:2]
            g=c[2:4]
            r=c[4:6]
            c=r+g+b
            print c
            self.hexcolor=c
            r=eval('0x' + r)
            g=eval('0x' + g)
            b=eval('0x' + b)
            self.rgbcolor=[r,g,b] 


    def getColor(self,format=0):
        color=0
        if not self.color:
            return self.color
        elif format==0: #Devolver como entero(COLORREF)
            return self.color
        elif format==1: #Devolver como hexa
            return self.hexcolor
        elif format==2:
            return self.rgbcolor


    def getCustomColors(self,format=1):
        if format==1:
            return [colorref2hex(el) for el in self.customcolors]
        elif format==2:
            return [colorref2hex(el) for el in self.customcolors]        
        else:
            return self.customcolors



class FontsDialog(object):
    def __init__(self, _font=None, _flags=win32con.CF_EFFECTS|win32con.CF_SCREENFONTS ,_dcPrinter=None, _parent=None ):
        self.flags=_flags
        self.parent=_parent
        self.font=_font
        self.fontcolor=None
        self.dcPrinter=_dcPrinter
        self.dlg=win32ui.CreateFontDialog(self.font,self.flags,self.dcPrinter,self.parent)


    def show(self):
        if not self.dlg:
            self.dlg=win32ui.CreateFontDialog(self.initColor,self.flags,self.parent)
        #Mostrar el dialogo y guardar la informacion obtenida
        result=self.dlg.DoModal()
        if result!=0: #Si se cancela, devuelve 0
            self.font=self.dlg.GetCurrentFont()
            self.fontcolor=self.dlg.GetColor()
            print 'Fuente: %s' %str(self.font)
            print self.fontcolor


    def getFontColor(self):
        #El color es un COLORREF
        return self.fontcolor


    def getFontName(self):
        if self.font:
            return self.dlg.GetFaceName()
        else:
            return ''


    def getFontSize(self,inPoints=1):
        if self.font:
            if not inPoints: #El tamanyo se devuelve en puntos*10
                return self.dlg.GetSize()
            else:
                return int(self.dlg.GetSize()/10)
        else:
            return 0


    def isBold(self):
        if self.font:
            return self.dlg.IsBold()
        else:
            return False

    def isItalic(self):
        if self.font:        
            return self.dlg.IsItalic()
        else:
            return False        

    def isUnderline(self):
        if self.font:        
            return self.dlg.IsUnderline()
        else:
            return False        

    def isStrikeOut(self):
        if self.font:        
            return self.dlg.IsStrikeOut()
        else:
            return False        
            
if __name__=='__main__':
    print hex2colorref('0x000000')
    cdlg=ColorsDialog()
    cdlg.show()
    fdlg=FontsDialog()
    fdlg.show()