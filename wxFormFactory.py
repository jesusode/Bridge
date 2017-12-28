#!Python
import wx
import wx.calendar
from wx.calendar import *
from matrix import *
import time

SIZER_STYLES={
   'expand':wx.EXPAND,
   'propor':wx.SHAPED,
   'min':wx.ADJUST_MINSIZE
   }

MENU_STYLES={
   'sep':wx.ITEM_SEPARATOR,
   'normal':wx.ITEM_NORMAL,
   'check':wx.ITEM_CHECK,
   'radio':wx.ITEM_RADIO
   }

PROGRESS_STYLE={
    'horiz':wx.GA_HORIZONTAL,
    'vert':wx.GA_VERTICAL,
    'progress':wx.GA_PROGRESSBAR,
    'soft':wx.GA_SMOOTH
    }
LISTCTRL_STYLES={
    'report':wx.LC_REPORT,
    'list':wx.LC_LIST
    }


BITMAP_TYPES={
    'bmp':wx.BITMAP_TYPE_BMP,
    'gif':wx.BITMAP_TYPE_GIF,
    'jpg':wx.BITMAP_TYPE_JPEG,
    'png':wx.BITMAP_TYPE_PNG,
    'tif':wx.BITMAP_TYPE_TIF,
    'ico':wx.BITMAP_TYPE_ICO,
    'cur':wx.BITMAP_TYPE_CUR,
    'any':wx.BITMAP_TYPE_ANY
    }


TEXT_STYLES={
    'multi':wx.TE_MULTILINE,
    'pass':wx.TE_PASSWORD,
    'readonly':wx.TE_READONLY,
    'rich':wx.TE_RICH,
    'url':wx.TE_AUTO_URL,
    'hscroll':wx.HSCROLL,
    'right':wx.TE_RIGHT,
    'centre':wx.TE_CENTRE,
    'left':wx.TE_LEFT
    }


WIN_STYLES={
    'title':wx.CAPTION,
    'minim':wx.MINIMIZE_BOX,
    'maxim':wx.MAXIMIZE_BOX,
    'close':wx.CLOSE_BOX,
    'resize':wx.RESIZE_BORDER,
    'border':wx.THICK_FRAME,
    'sysmenu':wx.SYSTEM_MENU,
    'transp':wx.TRANSPARENT_WINDOW,
    #'no3d':wx.NO_3D,
    'shape':wx.FRAME_SHAPED
    }

FONT_FAMILY={
    'times':wx.ROMAN,
    'script':wx.SCRIPT,
    'arial':wx.SWISS,
    'fixed':wx.MODERN,
    'decortive':wx.DECORATIVE
    }

FONT_STYLE={
   'normal':wx.NORMAL,
   'slant':wx.SLANT,
   'italic':wx.ITALIC
   }

FONT_WEIGHT={
   'normal':wx.NORMAL,
   'light':wx.LIGHT,
   'bold':wx.BOLD
   }
#Manejadores para imagenes
#-------------------------
wx.InitAllImageHandlers()
#-------------------------
class FontFactory:
   """
      Clase que gestiona una fuente
   """
   def __init__(self,points=8,style='arial',weight='normal',italic='normal',underline=0):
      self.__points=points
      #print str(self.__points)
      if FONT_WEIGHT.has_key(weight):
         self.__weight=FONT_WEIGHT[weight]
      else:
         self.__weight=wx.NORMAL
      #print str(self.__weight)
      if FONT_FAMILY.has_key(style):
         self.__style=FONT_FAMILY[style]
      else:
         self.__style=wx.ROMAN
      #print str(self.__style)
      if FONT_STYLE.has_key(italic):
         self.__italic=FONT_STYLE[italic]
      else:
         self.__italic=wx.NORMAL
      #print str(self.__italic)
      if underline:
         self.__underline=1
      else:
         self.__underline=0
      #print str(self.__underline)

   def getFont(self):
      return wx.Font(self.__points,self.__style,self.__italic,self.__weight,self.__underline)

class StyleFactory:
   """
     Clase para dar estilo
     a un wdiget: color de fondo,
     color y tipo de fuente
   """
   def __init__(self):
     self.__font=None
     self.__bgcolor=None
     self.__color=None
     self.__tooltip=None

   def getFont(self):
     return self.__font

   def setFont(self,font):
     self.__font=font

   def getBgColour(self):
     return self.__bgcolor

   def setBgColour(self,red,green,blue):
     self.__bgcolor=wx.Colour(red,green,blue)

   def getColour(self):
     return self.__color

   def setColour(self,red,green,blue):
     self.__color=wx.Colour(red,green,blue)

   def applyStyle(self,widget):
      if self.__bgcolor and hasattr(widget,'SetBackgroundColour'):
         widget.SetBackgroundColour(self.__bgcolor)
      if self.__color and hasattr(widget,'SetForegroundColour'):
         widget.SetForegroundColour(self.__color)
      if self.__font and hasattr(widget,'SetFont'):
         widget.SetFont(self.__font)
     
   def applyStyleToForm(self,form):
      controls=form.getControls()
      for control in controls.keys():
        #print 'cambiando...  ' + str(control)
        self.applyStyle(controls[control])


class FrameFactory:

   """
      Crea un panel de formulario a medida
   """


   def __init__(self,ancho=300,alto=300,rows=2,cols=2,vspace=5,hspace=5,titulo="Formulario",estilo=''):

      #Icono del formulario
      self.__icon=''

      #Tabla {nombre_interno_control:puntero al control}
      self.__controls={}
      #Tabla {tipo_Evento#nombre_control:funcion manejadora de eventos}
      self.__eventos={}
      #Tabla {nombre_sizer:sizer}
      self.__sizers={}
      #Menu del formulario
      self.__menu=wx.MenuBar()
      #Tabla de menus principales
      self.__menus={}
      #Tabla de elementos de menu
      self.__menu_items={}
      #Generador de id para los menus
      self.__menu_counter=1000
     
      #Crear la instancia del formulario que vamos a construir

      if estilo == '':
        estilo="wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX|wx.SYSTEM_MENU |wx.CAPTION|wx.CLOSE_BOX"
      else:
        #Evaluar el estilo
        est=[]
        for item in estilo.split('|'):
           est.append(str(WIN_STYLES[item]))
           print est
        estilo='|'.join(est)

      self.__frame=wx.Frame(None,-1,titulo,wx.DefaultPosition,
               wx.Size(ancho,alto),eval(estilo))
      #print "estilo=" + estilo
      self.__panel =wx.ScrolledWindow(self.__frame,-1,wx.Point(0, 0),
                 wx.DefaultSize)
      self.__panel.EnableScrolling(1,1)
      self.__panel.SetScrollbars(20, 20, 0,0)
      #self.__panel.SetBackgroundColour(wxColour(255,0,0))
      #self.__panel.SetForegroundColour(wxColour(0,255,0))


   def setBgColour(self,red,green,blue):
      self.__panel.SetBackgroundColour(wx.Colour(red,green,blue))


   def getFrame(self):
      """
         Crea el wxFrame y lo devuelve
      """
      #self.__panel.SetSizer(self.__grid)
      #Asignar gestores de eventos
      self.SET_EVENT_HANDLER()
      #print str(self.__eventos)

      #Asignar el icono del marco (si lo hay)
      if self.__icon <> '':
        ico=wx.Icon(self.__icon,wx.BITMAP_TYPE_ICO)
        self.__frame.SetIcon(ico)
      #Asignar el menu:
      self.__frame.SetMenuBar(self.__menu)
      #print str(self.__menu_items)
      return self.__frame


   def addSizer(self,nombre,sizer,parent=None,style='propor'):
      self.__sizers[nombre]=sizer
      #print str(self.__sizers)
      #Si no pertenece a otro sizer,
      #Adicionarlo al panel del frame
      if not parent:
         self.__panel.SetSizer(sizer)
      else:
         parent.Add(sizer,flag=SIZER_STYLES[style])


   def setIcon(self,file):
     self.__icon=file


   def getControlsInfo(self):
     return str(self.__controls)

   def getEventsInfo(self):
     return str(self.__eventos)

   def getSizersInfo(self):
      return str(self.__sizers)


   def addLabel(self,sizer,texto,nombre,ancho=100,alto=25,style='propor'):
     """
        Crea  una etiqueta
        y la anyade al formulario
     """
     #Etiqueta 
     label=wxStaticText(self.__panel, -1, texto,size=wx.Size(ancho,alto))
     self.__sizers[sizer].Add(label,0,flag=SIZER_STYLES[style])
     self.__controls[nombre]=label




   def addTextBox(self,sizer,nombre,multiline=0,textoInicial='',ancho=100,alto=25,style=None):

      """
        Crea un cuadro de texto 
        y lo anyade al formulario
      """
 
      #Cuadro de texto  
      if style:
        #Evaluar el estilo
        est=[]
        for item in style.split('|'):
           est.append(str(TEXT_STYLES[item]))
           #print est
        estilo='|'.join(est)
        text=wx.TextCtrl(self.__panel, -1, textoInicial,size=wx.Size(ancho,alto),style=eval(estilo))
      else:
        text=wx.TextCtrl(self.__panel, -1, textoInicial,size=wx.Size(ancho,alto))
      self.__sizers[sizer].Add(text,0)
      #Meterlo en la tabla de controles
      self.__controls[nombre]=text
 

   def addCombo(self,sizer,nombre,size,contenidos,texIni):
      """
        Crea un combo 
        y lo anyade al formulario
      """
      combo=wxComboBox(self.__panel, -1,  texIni,wx.DefaultPosition,wx.Size(size), contenidos)
      self.__sizers[sizer].Add(combo)           
      #Meterlo en la tabla de controles
      self.__controls[nombre]=combo

   def addListBox(self,sizer,nombre,ancho,alto,contenidos):
      """
        Crea un cuadro de lista 
        y lo anyade al formulario
      """

      #Lista
      lista=wx.ListBox(self.__panel, -1,wx.DefaultPosition,wx.Size(ancho,alto), contenidos)
      self.__sizers[sizer].Add(lista)
      self.__controls[nombre]=lista

   def addButton(self,sizer,nombre,texto,ancho=100,alto=25,style='propor'):
     """
        Crea  un boton
        y lo anyade al formulario
     """

     button=wx.Button(self.__panel, -1, texto)
     self.__sizers[sizer].Add(button,0,flag=SIZER_STYLES[style])
     self.__controls[nombre]=button



   def addCheckBox(self,sizer,nombre,texto,ancho=100,alto=25):
     """
        Crea  un CheckBox
        y lo anyade al formularioo
     """

     check=wx.CheckBox(self.__panel, -1, texto)
     self.__sizers[sizer].Add(check,0)
     self.__controls[nombre]=check


   def addRadioBox(self,sizer,nombre,titulo,opciones,ancho=100,alto=25):
     """
        Crea  un grupo de RadioButtons
        y los anyade al formularioo
     """

     radio=wx.RadioBox(self.__panel, -1, titulo,wx.DefaultPosition,wx.DefaultSize,opciones)
     self.__sizers[sizer].Add(radio,0)
     #Meterlo en la tabla de controles
     self.__controls[nombre]=radio


   def addStatusBar(self,secciones=1):
     #Crea una barra de estado con (secciones) partes
     self.__frame.CreateStatusBar(secciones)


   def addStaticBitmap(self,sizer,nombre,bitmap,tipo='bmp',ancho=100,alto=100):
      #Crea una imagen
      img=wx.Image(bitmap)
      if BITMAP_TYPES.has_key(tipo):
         #bmp=wxBitmap(bitmap,BITMAP_TYPES[tipo])
         bmp=wx.BitmapFromImage(img)
         bitmap=wx.StaticBitmap(self.__panel,-1,bmp,size=wx.Size(ancho,alto))
         self.__sizers[sizer].Add(bitmap,0)
         self.__controls[nombre]=bitmap
         #bitmap.SetBackgroundColour(wxColour(255,255,255))
         


   def addListControl(self,sizer,nombre,headers,matrix,ancho=200,alto=200):
       #Crea un control de lista
       listctrl=wx.ListCtrl(self.__panel,-1,size=wx.Size(ancho,alto),style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
       self.__controls[nombre]=listctrl
       self.__sizers[sizer].Add(listctrl,0)
       for i in range(len(headers)):
         listctrl.InsertColumn(i,headers[i])
       
       for x in range(matrix.rows()):
         listctrl.InsertStringItem(x,matrix[x][0])
         for y in range(1,matrix.cols()):
            #print str(x),str(y), matrix[x][y]
            listctrl.SetStringItem(x,y,matrix[x][y])
       
       #listctrl.SetStringItem(1,1,"hola")
       #listctrl.SetItemText(1,"hola")
       for x in range(len(headers)):
          listctrl.SetColumnWidth(x,50)


   def addTreeControl(self,sizer,nombre,root,nodes,ancho=200,alto=200):
      #Crea un control de vista de arbol
      tree=wx.TreeCtrl(self.__panel,-1,size=wx.Size(ancho,alto),style=wx.TR_HAS_BUTTONS|wx.TR_EDIT_LABELS)
      #Crear el nodo raiz
      raiz=tree.AddRoot(root)
      #Asignar datos asociados
      tree.SetPyData(raiz,None)
      #Adicionarlo
      self.__controls[nombre]=tree
      self.__sizers[sizer].Add(tree,0)
      #Cargar los nodos
      for x in range(len(nodes)):
         nodo=tree.AppendItem(raiz,nodes[x])
         tree.SetPyData(nodo,None)
      

   def addCalendarControl(self,sizer,nombre,ancho,alto,style=None):
      #Crea un control de calendario
      cal=CalendarCtrl(self.__panel,-1,size=wx.Size(ancho,alto))
      #Adicionarlo
      self.__controls[nombre]=cal
      self.__sizers[sizer].Add(cal,0)


   def addMenu(self,nombre,items,style='normal'):
      #Meter los items en la tabla
      #Cada item es una lista del tipo
      #[nombre,helpstring]
      menu=wx.Menu()
      self.__menus[nombre]=menu
      contador=1000
      for item in items:
         #Poner el nuevo item
         menu.Append(self.__menu_counter,item[0],item[1],MENU_STYLES[style])
         #Registrarlo
         self.__menu_items[item[0]]=self.__menu_counter
         #Incrementar el generador de id
         self.__menu_counter+=1
         
      self.__menu.Append(menu,nombre)

   def addSubMenu(self,nombre,parent,items,helpstring='',style='normal'):
      #Meter los items en la tabla
      #Cada item es una lista del tipo
      #[nombre,helpstring]
      menu=wx.Menu()
      self.__menus[nombre]=menu
      contador=1000
      for item in items:
         #Poner el nuevo item
         menu.Append(self.__menu_counter,item[0],item[1],MENU_STYLES[style])
         #Registrarlo
         self.__menu_items[item[0]]=self.__menu_counter
         #Incrementar el generador de id
         self.__menu_counter+=1
         
      self.__menus[parent].AppendMenu(self.__menu_counter,nombre,menu,helpstring)
      self.__menu_counter+=1
      


   def addProgressBar(self,sizer,nombre,rango,ancho,alto,style=wx.GA_HORIZONTAL):
      bar=wx.Gauge(self.__panel,-1,rango,size=wx.Size(ancho,alto),style=wx.GA_SMOOTH)
      bar.SetValue(25)
      #Adicionarlo
      self.__controls[nombre]=bar
      self.__sizers[sizer].Add(bar,0)



   def addWebBrowserControl(self,sizer,nombre,url):
      '''w=WebBrowserControl(self.__panel)
      web=w.getBrowser()
      web.Navigate(url)
      #Adicionarlo
      self.__controls[nombre]=web
      self.__sizers[sizer].Add(web,1,wx.EXPAND)'''
      #Cambiar para usar wxPython 2.8
      pass



   def addTimer(self,nombre,intervalo):
      t=wx.Timer(self.__panel)
      #Adicionarlo
      self.__controls[nombre]=t
      t.Start(intervalo)

   def getControl(self,nombre):
      if self.__controls.has_key(nombre):
         return self.__controls[nombre]
      else:
         return None


   def getControls(self):
      #print str(self.__controls)
      return self.__controls


   def addEventHandler(self,tipoEvento,nombreControl,handler):
      #Anadir el nombre del control y el gestor al diccionario de eventos
      if tipoEvento != 'EVT_TIMER':
         self.__eventos[tipoEvento + "#" + nombreControl]=handler
      else:
         self.__eventos[tipoEvento]=handler

   def SET_EVENT_HANDLER(self):

      if len(self.__eventos) > 0:
        for key in self.__eventos:
          evt=key.split('#')[0]
          #print evt
          if evt=="EVT_BUTTON":
             wx.EVT_BUTTON(self.__frame,self.__controls[key.split('#')[1]].GetId(),self.__eventos[key])
          elif evt=="EVT_COMBOBOX":
             wx.EVT_COMBOBOX(self.__frame,self.__controls[key.split('#')[1]].GetId(),self.__eventos[key])             
          elif evt=="EVT_LISTBOX":
             wx.EVT_LISTBOX(self.__frame,self.__controls[key.split('#')[1]].GetId(),self.__eventos[key])             
          elif evt=="EVT_LISTBOX_DCLICK":
             wx.EVT_LISTBOX(self.__frame,self.__controls[key.split('#')[1]].GetId(),self.__eventos[key])             
          elif evt=="EVT_CHECKBOX":
             wx.EVT_CHECKBOX(self.__frame,self.__controls[key.split('#')[1]].GetId(),self.__eventos[key])             
          elif evt=="EVT_RADIOBOX":
             wx.EVT_RADIOBOX(self.__frame,self.__controls[key.split('#')[1]].GetId(),self.__eventos[key])             
          elif evt=="EVT_TEXT":
             wx.EVT_TEXT(self.__frame,self.__controls[key.split('#')[1]].GetId(),self.__eventos[key])             
          elif evt=="EVT_TEXT_ENTER":
             wx.EVT_TEXT_ENTER(self.__frame,self.__controls[key.split('#')[1]].GetId(),self.__eventos[key])             
          elif evt=="EVT_CLOSE":
             wx.EVT_CLOSE(self.__frame,self.__eventos[key])
          elif evt=="EVT_TIMER":
             wx.EVT_TIMER(self.__panel,-1,self.__eventos[key])
          elif evt=="EVT_MENU":
             id=self.__menu_items[key.split('#')[1]]
             wx.EVT_MENU(self.__frame,id,self.__eventos[key])


#Codigo para pruebas
if __name__=='__main__':

   class MyApp(wx.App):
      def OnInit(self):
        #wxApp.wxInitAllImageHandlers()
        #grid=wxFlexGridSizer(2,2,50,50)
        grid=wx.BoxSizer(wx.HORIZONTAL)
        grid2=wx.BoxSizer(wx.VERTICAL)
        grid3=wx.BoxSizer(wx.VERTICAL)
        self.pf=FrameFactory(600,600,0,2,5,50,titulo='Mi formulario',estilo="title|sysmenu|minim|maxim|close|resize" )
        #self.pf=FrameFactory(600,600,0,2,5,50,titulo='Mi formulario',estilo="" )
        #ojo, poner el menu lo primero
        #ojo, poner el menu lo primero
        #self.pf.addMenu("ccccc")
        self.pf.addMenu('Archivo',[['Nuevo','nuevo'],['Abrir','abrir']])
        self.pf.addMenu('Editar',[['Copiar','copiar'],['Pegar','pegar']],'radio')
        self.pf.addEventHandler("EVT_MENU","Nuevo",self.OnNuevo)
        self.pf.addSubMenu('Submenu','Archivo',[['Sub1','sub1'],['Sub2','sub2']])
        self.pf.addSizer("grid",grid)
        f=StyleFactory()
        f.setColour(255,200,80)
        f.setBgColour(50,150,0)


        for i in range(2):
           self.pf.addTextBox("grid","Texto" + str(i),0,"hola" + str(i))
        self.pf.addSizer("interno",grid2,grid)
        '''
        for i in range(2):
           pf.addButton("interno","Boton" + str(i),"Boton" + str(i))
           pf.addTextBox("interno","Texto2" + str(i),0,"" + str(i))
        '''
        self.pf.addSizer("lateral",grid3,grid)


        #self.pf.addWebBrowserControl("grid","web",r'file://c:/html.html')
        #pf.addWebBrowserControl("grid","web2",r'file://c:/cs.pdf')        
        for i in range(2):
           self.pf.addCheckBox("lateral","Check" + str(i),"Check" + str(i))
           
        self.pf.addTextBox("interno","Texto8",1,ancho=100,alto=100,style='multi|left')
        #pf.addStaticBitmap("interno","bmp1",'c:\\canarias_atl.bmp','bmp',100,100)
        #pf.addStaticBitmap("interno","bmp1",'c:\\margarita.gif','bmp',100,100)

        h=['uno','dos','tres','cuatro']
        m=Matrix([['ddd','dd2','dd3','dd4'],['bla','ble','bli','blo'],['dd5','dd6','dd7','dd8'],['xx2','xx3','xx4','xx5']])       
        self.pf.addListControl("interno","rejilla",h,m)
        #t1=pf.getControl("Boton1")
        self.pf.addTreeControl("interno","tree1","raiz",['uno','dos','tres','cuatro'],100,100)
        self.pf.addCalendarControl("interno","cal1",150,150)
        self.pf.addProgressBar("interno","p1",25,100,25)
        
        #self.pf.addTimer("time1",1000)
        
        #self.pf.addEventHandler("EVT_TIMER","time1",self.OnTimer)
        #self.pf.getControl("time1").Start()
        
        #timerclass.KILL_ALL_TIMERS=1
        #self.pf.addTimer2("timer1",1,self.OnTimer2)
        #self.pf.addTimer2("timer2",1,self.OnTimer3)        
        self.pf.addEventHandler("EVT_CLOSE","timer1",self.OnCerrar)
        
        #ff=FontFactory(14,'fixed','bold','italic',1)
        ff=FontFactory()
        fnt=ff.getFont()
        f.setFont(fnt)
        '''
        fnt=wxFont(14,wxSWISS,wxITALIC,wxBOLD,1)
        f.setFont(fnt)
        '''
        #f.applyStyle(t1)
        #pf.setBgColour(255,255,255)
        
        #self.pf.setIcon(r'c:/iconos/cab.ico')
        self.pf.addStatusBar(2)
        #f.applyStyleToForm(pf)
        del f

        #print pf.getControlsInfo()
        #print pf.getEventsInfo()             
        frame =self.pf.getFrame()

        frame.SetStatusText(time.strftime("%a, %d %b %Y ", time.gmtime()),1)
        #frame.SetTitle("Pedazo formulario!!")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True        


      def OnTimer(self,event):
         print 'Lanzado por el Timer a las ' + time.strftime("%h, %m %s ", time.gmtime())

      def OnTimer2(self,event):
         print 'OnTimer2: ' + str(timerclass.KILL_ALL_TIMERS)

      def OnTimer3(self,event):
         print 'OnTimer3: ' + str(timerclass.KILL_ALL_TIMERS)

      def OnNuevo(self,event):
         print 'Evento de menu activado...'


      def OnCerrar(self,event):
         print 'cerrando el programa...'
         self.GetTopWindow().Destroy()
         

   win=MyApp(0)
   win.MainLoop()


