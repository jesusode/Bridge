#!Python

import wx
from wx.grid import *
from wx.lib.mixins.grid import GridAutoEditMixin
from matrix import *
import types

class GridFactory:
   """
     Crea un wx.Grid a medida y lo devuelve
   """
   def __init__(self,ancho=200,alto=300,rows=2,cols=2,titulo="Rejilla"
            ,nombreCols=None,nombreRows=None,tabla=None):

      self.__eventos={}
      self.__rows=rows
      self.__cols=cols

      #Crear la instancia del formulario que vamos a construir
      self.__frame=wx.Frame(None,-1,titulo,wx.DefaultPosition,
                 wx.Size(ancho,alto),eval("wx.MINIMIZE_BOX  |wx.SYSTEM_MENU | wx.CAPTION"))#|wxRESIZE_BORDER|wxMAXIMIZE_BOX)

      #self.__panel =wxScrolledWindow(self.__frame,-1,wxPoint(0, 0),
       #          wxDefaultSize)#,wxVSCROLL)
      self.__grid=Grid(self.__frame,-1)
      self.__grid.CreateGrid(self.__rows,self.__cols)
      #self.__grid.SetColSize(1, 45)
      #self.__grid.SetRowSize(1, 45)


      if tabla:
        self.__tabla=tabla
        print 'Nos quedamos con la tabla del constructor'
        #Poner las celdas en la tabla
        self.update()
      else:
        self.__tabla=Matrix()
        print 'No nos quedamos con la tabla del constructor'


      if nombreCols:
        for n in range(len(nombreCols)):
          self.__grid.SetColLabelValue(n,nombreCols[n])
      if nombreRows:
        for n in range(len(nombreRows)):
          self.__grid.SetRowLabelValue(n,nombreRows[n])




      # test all the events
      EVT_GRID_CELL_LEFT_CLICK(self.__frame, self.OnCellLeftClick)
      EVT_GRID_CELL_RIGHT_CLICK(self.__grid, self.OnCellRightClick)
      EVT_GRID_CELL_LEFT_DCLICK(self.__grid, self.OnCellLeftDClick)
      EVT_GRID_CELL_RIGHT_DCLICK(self.__grid, self.OnCellRightDClick)

      EVT_GRID_LABEL_LEFT_CLICK(self.__grid, self.OnLabelLeftClick)
      EVT_GRID_LABEL_RIGHT_CLICK(self.__grid, self.OnLabelRightClick)
      EVT_GRID_LABEL_LEFT_DCLICK(self.__grid, self.OnLabelLeftDClick)
      EVT_GRID_LABEL_RIGHT_DCLICK(self.__grid, self.OnLabelRightDClick)

      EVT_GRID_ROW_SIZE(self.__grid, self.OnRowSize)
      EVT_GRID_COL_SIZE(self.__grid, self.OnColSize)

      EVT_GRID_RANGE_SELECT(self.__grid, self.OnRangeSelect)
      EVT_GRID_CELL_CHANGE(self.__grid, self.OnCellChange)
      EVT_GRID_SELECT_CELL(self.__grid, self.OnSelectCell)

      EVT_GRID_EDITOR_SHOWN(self.__grid, self.OnEditorShown)
      EVT_GRID_EDITOR_HIDDEN(self.__grid, self.OnEditorHidden)
      EVT_GRID_EDITOR_CREATED(self.__grid, self.OnEditorCreated)          


   def update(self):
      for i in range(self.__tabla.rows()):
        for j in range(self.__tabla.cols()):
          self.__grid.SetCellValue(i,j,str(self.__tabla[i][j]))
          #print self.__tabla.toString()
          print str(i) + ":" + str(j) + "=" + str(self.__tabla[i][j])   



   def getGrid(self):
      """
         Crea el wx.Grid y lo devuelve
      """

      return self.__frame

   def setTable(self,tabla):
      self.__tabla=tabla
      self.update()





   #Manejadores de eventos
   def OnCellLeftClick(self, evt):
        evt.Skip()

   def OnCellRightClick(self, evt):
        evt.Skip()

   def OnCellLeftDClick(self, evt):
        evt.Skip()

   def OnCellRightDClick(self, evt):
        evt.Skip()

   def OnLabelLeftClick(self, evt):
        evt.Skip()
      
   def OnLabelRightClick(self, evt):
        evt.Skip()

   def OnLabelLeftDClick(self, evt):
        evt.Skip()

   def OnLabelRightDClick(self, evt):
        evt.Skip()


   def OnRowSize(self, evt):
        evt.Skip()

   def OnColSize(self, evt):
        evt.Skip()

   def OnRangeSelect(self, evt):
        evt.Skip()


   def OnCellChange(self, evt):
        evt.Skip()


   def OnIdle(self, evt):
        evt.Skip()

   def OnSelectCell(self, evt):
        evt.Skip()


   def OnEditorShown(self, evt):
        evt.Skip()


   def OnEditorHidden(self, evt):
        evt.Skip()

   def OnEditorCreated(self, evt):
        evt.Skip()


      

if __name__=="__main__":
    print 'ejecutando codigo de prueba'
    class MyApp(wx.App):
      def OnInit(self):
        m=Matrix([['bla','ble','bli','blo'],['ddd','dd2','dd3','dd4'],['dd5','dd6','dd7','dd8'],['xx2','xx3','xx4','xx5']])       
        pf=GridFactory(400,300,4,4,'Mi rejilla',['ColUno','ColDos'],['RowUno','RowDos'],m)
        #pf=GridFactory(400,300,1,20,'Mi rejilla',['ColUno'],['RowUno'],p)
        frame =pf.getGrid() 

        frame.Show(True)
        self.SetTopWindow(frame)
        return True        

    win=MyApp(0)
    #win2=MyApp(0)
    win.MainLoop()

    #win2.MainLoop()