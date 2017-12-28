#Soporte para wx

import wx
import wx.grid
import wx.html
import wx.lib.printout
import wx.lib.platebtn
import wx.stc
import wx.html2
import wx.lib.colourselect
import wx.lib.agw.aquabutton
import wx.lib.agw.hyperlink
import wx.lib.filebrowsebutton

#wx.Grid-------------------------------------------------------------------------
class MinimalGridTableModel(wx.grid.PyGridTableBase):
    def __init__(self, rows,cols,data,colnames=[],rownames=[],oddcol=wx.Colour(250,250,250),evencol="white"):
        wx.grid.PyGridTableBase.__init__(self)
        self.rows = rows
        self.cols=cols
        self.data=data
        self.colnames=colnames
        self.rownames=rownames
        self.oddcol=oddcol
        self.evencol=evencol
        self.odd=wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour(self.oddcol)
        self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.even=wx.grid.GridCellAttr()
        self.even.SetBackgroundColour(self.evencol)
        self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

    def GetData(self):
        return self.data

    def GetAttr(self, row, col, kind):
        attr = [self.even, self.odd][row % 2]
        attr.IncRef()
        return attr
    
    def GetNumberRows(self):
        return self.rows

    def GetNumberCols(self):
        return self.cols

    def IsEmptyCell(self, row, col):
        try:
            return self.data[row][col] is not None
        except:
            return False

    def GetValue(self, row, col):
        #value = self.data.get((row, col))
        value = self.data[row][col]
        if value is not None:
          return value
        else:
          return ''

    def SetValue(self, row, col, value):
        self.data[row][col] = value

    def GetColLabelValue(self, col):
        return self.colnames[col]

    def GetRowLabelValue(self, row):
        if self.rownames:
            return self.rownames[row]
        else:
            return ""


def gridFactory(parent,data=[['',''],['','']],colnames=[],rownames=[],oddcol="#f0f0f0",evencol="white",**gridargs):
    grid=wx.grid.Grid(parent,**gridargs)
    model=MinimalGridTableModel(len(data),len(data[0]),data,colnames,rownames,oddcol,evencol)
    grid.SetTable(model,True)
    return grid


def changeGrid(grid,data,colnames,rownames,oddcol="#f0f0f0",evencol="white"):
    if len(data)>0:
        model=MinimalGridTableModel(len(data),len(data[0]),data,colnames,rownames,oddcol,evencol)
        grid.SetTable(model,True)
        grid.Refresh()
        grid.AutoSizeRows()
        grid.AutoSizeColumns()
        return grid

def corners_to_cells(top_lefts, bottom_rights):
    """
    Take lists of top left and bottom right corners, and
    return a list of all the cells in that range
    """
    cells = []
    for top_left, bottom_right in zip(top_lefts, bottom_rights):

        rows_start = top_left[0]
        rows_end = bottom_right[0]

        cols_start = top_left[1]
        cols_end = bottom_right[1]

        rows = range(rows_start, rows_end+1)
        cols = range(cols_start, cols_end+1)

        cells.extend([(row, col)
            for row in rows
            for col in cols])

    return cells

def getGridSelectedCells(grid):
    """
    Return the selected cells in the grid as a list of
    (row, col) pairs.
    We need to take care of three possibilities:
    1. Multiple cells were click-selected (GetSelectedCells)
    2. Multiple cells were drag selected (GetSelectionBlock...)
    3. A single cell only is selected (CursorRow/Col)
    """

    top_left = grid.GetSelectionBlockTopLeft()

    if top_left:
        bottom_right = grid.GetSelectionBlockBottomRight()
        return [grid.GetCellValue(x[0],x[1]) for x in corners_to_cells(top_left, bottom_right)]

    selection = grid.GetSelectedCells()

    if not selection:
        row = grid.GetGridCursorRow()
        col = grid.GetGridCursorCol()
        return [grid.GetCellValue(row,col)]

    return [grid.GetCellValue(x[0],x[1]) for x in selection]
#------------------------------------------------------------------

#wx.ListCtrl-------------------------------------------------------
def tableFactory(parent,data=[],colnames=[],**tableargs):
    table=wx.ListCtrl(parent,**tableargs)
    if colnames!=[]:
        for i in range(len(colnames)):
            table.InsertColumn(i,colnames[i])
    if data!=[]:
        for item in data:
            table.Append(item)
    return table

def getRowText(table, idx,sep=","):
    txt = []
    for col in range(table.ColumnCount):
        txt.append(table.GetItemText(idx, col))
    return sep.join(txt)

def getTableTextList(table, sep=","):
    txts = []
    for i in range(table.ItemCount):
        txts.append(getRowText(table,i,sep))
    return txts

def getTableText(table, sep=",",sep2="\n"):
    txts = []
    for i in range(table.ItemCount):
        txts.append(getRowText(table,i,sep))
    return sep2.join(txts)

def selectAll(table):
    for item in range(table.ItemCount):
        table.Select(item, 1)

def getSelectedText(table,sep=","):
    items = []
    nColumns = table.ColumnCount
    for item in range(table.ItemCount):
        if table.IsSelected(item):
            items.append(getRowText(table,item,sep))
    return items
#------------------------------------------------------------------

#wx.TreeCtrl-------------------------------------------------------
def addTreeNodes(tree, parentItem, items):
    for item in items:
        if type(item) in[str,unicode]:
            tree.AppendItem(parentItem, item)
        else:
            newItem = tree.AppendItem(parentItem, item[0])
            if len(item)>1:
                addTreeNodes(tree,newItem, item[1])

            
def treeFactory(parent,root,data,**args):
    tree=wx.TreeCtrl(parent,**args)
    r=tree.AddRoot(root)
    if data:
        addTreeNodes(tree,r,data)
    return tree

def tree_item_exists(tree, text, root):
    item, cookie = tree.GetFirstChild(root)
    while item.IsOk():
        if tree.GetItemText(item) == text:
            return True
        item, cookie = tree.GetNextChild(root, cookie)
    return False
#Solo busca en un nivel??
def get_tree_item(tree, text, root):
    item, cookie = tree.GetFirstChild(root)
    while item.IsOk():
        if tree.GetItemText(item) == text:
            return item
        item, cookie = tree.GetNextChild(root, cookie)
    return None

#wx.html.HTMLWindow------------------------------------------------------
class MinimalHtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent,**kw):
        self.onlink=None #tipo: f(linkinfo)
        self.endlink=0 #Flag para deshabilitar navegacion por links
        self.oncellclicked=None #tipo: f(cell,x,y,evt)
        self.oncellhover=None #tipo: f(cell,x,y)
        self.onsettitle=None #tipo: f(title)
        self.onurlopen=None #tipo: f(type,url)
        if 'cellclicked' in kw:
            self.oncellclicked=kw['cellclicked']
            del kw['cellclicked']
        if 'onlink' in kw:
            self.onlink=kw['onlink']
            del kw['onlink']
        if 'onurlopen' in kw:
            self.onurlopen=kw['onurlopen']
            del kw['onurlopen']
        if 'endlink' in kw:
            self.endlink=1
            del kw['endlink']
        if 'cellhover' in kw:
            self.oncellhover=kw['cellhover']
            del kw['cellhover']
        if 'settitle' in kw:
            self.onsettitle=kw['onsettitle']
            del kw['onsettitle']
        wx.html.HtmlWindow.__init__(self, parent,**kw)
        if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, linkinfo):
        if self.onlink:
            self.onlink(linkinfo)
        if not self.endlink:
            super(MinimalHtmlWindow, self).OnLinkClicked(linkinfo)

    def OnSetTitle(self, title):
        if self.onsettitle:
            self.onsettitle(title)
        super(MinimalHtmlWindow, self).OnSetTitle(title)

    def OnCellMouseHover(self, cell, x, y):
        if self.oncellhover:
            self.oncellhover(cell,x,y)
        super(MinimalHtmlWindow, self).OnCellMouseHover(cell, x, y)

    def OnCellClicked(self, cell, x, y, evt):
        if self.oncellclicked:
            self.oncellclicked(cell,x,y,evt)
        super(MinimalHtmlWindow, self).OnCellClicked(cell, x, y, evt)

    def OnOpeningURL(self, type,url):
        if self.onurlopen:
            self.onurlopen(type,url)
        super(MinimalHtmlWindow, self).OnOpeningURL(type,url)


def htmlWinFactory(parent,html,**args):
    htw=MinimalHtmlWindow(parent,**args)
    htw.SetPage(html)
    return htw

#wx.TaskBarIcon----------------------------------------------------------
class MinimalTaskBarIcon(wx.TaskBarIcon):
    def __init__(self,labels,callbacks):
        wx.TaskBarIcon.__init__(self)
        self.labels=labels
        self.callbacks=callbacks
        assert len(labels)==len(callbacks)

    def CreatePopupItems(self,menu, labels=[], funcs=[]):
        for i in range(len(labels)):
            item = wx.MenuItem(menu, -1, labels[i])
            menu.Bind(wx.EVT_MENU, funcs[i], id=item.GetId())
            menu.AppendItem(item)
        return menu

    def CreatePopupMenu(self):
        return self.CreatePopupItems(wx.Menu(),self.labels,self.callbacks)

class CaptionBox(wx.PyPanel):
    def __init__(self, parent, caption, flag=wx.VERTICAL):
        super(CaptionBox, self).__init__(parent,style=wx.NO_BORDER)
        self.Label = caption
        self._csizer = wx.BoxSizer(flag)
        self.__DoLayout()
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def __DoLayout(self):
        msizer = wx.BoxSizer(wx.VERTICAL)
        tsize = self.GetTextExtent(self.Label)
        msizer.AddSpacer(tsize[1] + 3) # extra space for caption
        msizer.Add(self._csizer, 0, wx.EXPAND|wx.ALL, 8)
        self.SetSizer(msizer)

    def DoGetBestSize(self):
        size = super(CaptionBox, self).DoGetBestSize()
        # Make sure there is room for the label
        tsize = self.GetTextExtent(self.Label)
        size.SetWidth(max(size.width, tsize[0]+20))
        return size

    def AddItem(self, item):
        self._csizer.Add(item, 0, wx.ALL, 5)

    def OnPaint(self, event):

        dc = wx.PaintDC(self)
        rect = self.ClientRect
        # Get the system color to draw the caption
        ss = wx.SystemSettings
        color = ss.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)
        txtcolor = ss.GetColour(wx.SYS_COLOUR_CAPTIONTEXT)
        dc.SetTextForeground(txtcolor)
        # Draw the border
        self.OnDrawBorder(dc, color, rect)
        # Add the Caption
        self.OnDrawCaption(dc, color, rect)

    def OnDrawBorder(self, dc, color, rect):
        rect.Inflate(-2, -2)
        dc.SetPen(wx.Pen(color))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangleRect(rect)

    def OnDrawCaption(self, dc, color, rect):
        tsize = dc.GetTextExtent(self.Label)
        rect = wx.Rect(rect.x, rect.y,rect.width, tsize[1] + 3)
        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangleRect(rect)
        rect.Inflate(-5, 0)
        dc.SetFont(self.GetFont())
        dc.DrawLabel(self.Label, rect, wx.ALIGN_LEFT)



def captionBoxFactory(parent,caption,items=[]):#??????????????????
    cb=CaptionBox(parent,caption)
    for item in items:
        cb.AddItem(item)
    return cb


#wx.PopupWindow: admite 1 widget(cualquiera)
class FloatWin(wx.PopupWindow):
    def __init__(self, parent,widget=None, style=wx.SIMPLE_BORDER,color="CADET BLUE",die_r=0):
        wx.PopupWindow.__init__(self, parent, style)
        pnl = self.pnl = wx.Panel(self)
        pnl.SetBackgroundColour(color)
        self.SetBackgroundColour(color)
        self.destroy_on_rclick=die_r
        sz=wx.Rect(200,200)
        if widget!=None:
            sz = widget.GetBestSize()
        self.SetSize( (sz.width+20, sz.height+20) )
        pnl.SetSize( (sz.width+20, sz.height+20) )

        pnl.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        pnl.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        pnl.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        pnl.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        wx.CallAfter(self.Refresh)
        
    def addWidget(self,widget):
        self.widget=widget
        sz = widget.GetSize()#widget.GetBestSize()
        self.SetSize( (sz.width+20, sz.height+20) )
        self.pnl.SetSize( (sz.width+20, sz.height+20) )
        self.widget.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.widget.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.widget.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.widget.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

    def OnMouseLeftDown(self, evt):
        self.Refresh()
        self.ldPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        self.wPos = self.ClientToScreen((0,0))
        self.pnl.CaptureMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            dPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
            nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
                    self.wPos.y + (dPos.y - self.ldPos.y))
            self.Move(nPos)

    def OnMouseLeftUp(self, evt):
        if self.pnl.HasCapture():
            self.pnl.ReleaseMouse()

    def OnRightUp(self, evt):
        self.Show(False)
        if self.destroy_on_rclick==1:
            self.Destroy()

