
import sys
sys.path.append('.')#Para py2exe
sys.path.append('./modules')#Para py2exe
sys.path.append('library.zip')#Para py2exe
import wx
import wx.grid
import wx.html
from wx_support import *



#Codigo del controlador del genotipo de VHC

bands=['Banda 1','Banda 2','Banda 3','Banda 4',
'Banda 5','Banda 6','Banda 7','Banda 8',
'Banda 9','Banda 10','Banda 11','Banda 12',
'Banda 13','Banda 14','Banda 15','Banda 16','Banda 17',
'Banda 18','Banda 19','Banda 20','Banda 21']

core=['Banda 23','Banda 24','Banda 25','Banda 26']

types=['Genotipo VHC']

vhc_interp={
    "Genotipo 1a I" : [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Genotipo 1a II" : [1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	"Genotipo 1a III" : [1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Genotipo 1b I" : [1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Genotipo 1b II" : [1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	"Genotipo 1b III" : [1,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Genotipo 1b IV" : [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Genotipo 1b V" : [1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Genotipo 1b VI" : [1,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	"Genotipo 1b VII" : [1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Genotipo 1b VIII" : [1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	"Genotipo 1b IX" : [1,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Genotipo 1a o 1b I" : [1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	"Genotipo 1a o 1b II" : [1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Genotipo 1a o 1b III" : [1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	
    }

core_interp={
    "Genotipo 1a" : [1,0,1,0],
    "Genotipo 1b" : [1,0,0,1],
    "Genotipo 1" : [1,0,1,1],
    "No concluyente I" : [1,0,0,0],
    "No concluyente II" : [0,0,0,0],
    "Genotipo 6" : [1,1,0,0]
}


#Todas las micobacterias
mycos=vhc_interp.keys()

#Global que indica la tabla a usar para las interpretaciones
tabla=None

def get_bands(table):
    bands=[]
    for i in range(len(table)):
        if table[i]:
            bands.append(i+1)
    return bands

def find_similars(bands):
    similes=[]
    for item in vhc_interp:
        temp= vhc_interp[item]
        for el in bands:
            if el>2 and temp[el]==1:
                similes.append([item,get_bands(temp)])
                break
    return similes

def calcular_click(evt):
    global tabla
    #Asegurar que hay una tabla seleccionada si esta calcular activo!
    if not tabla: tabla = vhc_interp 
    #print 'calculando!'
    checkedItems = [i for i in range(lb_bandas.GetCount()) if lb_bandas.IsChecked(i)]
    #Buscar coincidencias
    success=0
    found='Sin coincidencias para ese patron de bandas'
    report=''
    for item in tabla:
        if len(checkedItems)< tabla[item].count(1): continue
        for it in checkedItems:
            if tabla[item][it]!=1:
                break
            else:
                success+=1
        if len(checkedItems)==success:
            found=item
            break
        success=0
    coinc_str='\n'.join(['\t' + x[0] + '. Bandas: ' + str(x[1]) for x in find_similars(checkedItems)])
    resultados.SetValue('Coincidencia total:\n\t' + found + '\nCoincidencias parciales:\n' + coinc_str)

def limpiar_click(evt):
    resultados.SetValue("")
    #Check(self, unsigned int index, int check=True)
    #GetCheckedStrings() devuelve las cadenas de los items seleccionados
    its=lb_bandas.GetChecked()
    for it in its:
        lb_bandas.Check(it,False)
    calcular.Enable(False)

def salir_click(evt):
    main.Destroy()

def check_band(evt):
    if lb_bandas.GetChecked():
        if not calcular.IsEnabled():
            calcular.Enable(True)
    else:
        calcular.Enable(False)


def lb_types_dclick(evt):
    #Borrar elementos en lb_bandas
    global tabla
    lb=evt.GetEventObject()
    sel=lb.GetString(lb.GetSelection())
    l=range(lb_bandas.GetCount())
    l.reverse()
    calcular.Enable(False)
    for i in l:
        lb_bandas.Delete(i)
    if sel=='Genotipo VHC': 
        tabla = vhc_interp
    else:
        dlg = wx.MessageDialog(main, 'Panel pendiente de implementar', 'Panel no implementado', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    if sel in ['Genotipo VHC']:
        lb_bandas.InsertItems(bands,0)
        lb_bandas.Enable(True)
        #calcular.Enable(True)

def simulate_start(evt):
    chk=evt.GetEventObject()
    resultados.SetValue("")
    if chk.IsChecked():
        sym_label.Enable(True)
        sym_combo.Enable(True)
        lb_types.Enable(False)
        limpiar_click(evt)
    else:
        sym_label.Enable(False)
        sym_combo.Enable(False)
        lb_types.Enable(True)
        limpiar_click(evt)

def simulate(evt):
    if lb_bandas.GetCount() ==1:
        lb_bandas.Delete(0)
        lb_bandas.InsertItems(bands,0)
    mb=evt.GetEventObject().GetValue()
    panel=''
    bandas=[]
    panel='Genotipo VHC'
    bandas=vhc_interp[mb]
    lb_bandas.Enable(True)
    limpiar_click(evt)
    bs= get_bands(bandas)
    for item in [x-1 for x in bs]:
        lb_bandas.Check(item,True)
    resultados.SetValue('%s esta en %s'%(mb,panel) + '\nPresenta las siguientes bandas: %s'%str(bs) )


root=wx.App()

main=wx.Frame(parent=None,size=[900,750])
mainpanel=wx.Panel(main)
mainsizer=wx.BoxSizer(orient=wx.VERTICAL)
panel_lab=wx.Panel(mainpanel)
mainsizer.Add(panel_lab,flag=wx.EXPAND)
lbl_sizer=wx.GridSizer(rows=1,cols=3,hgap=10,vgap=3)
panel_lb=wx.Panel(mainpanel)
mainsizer.Add(panel_lb,flag=wx.EXPAND)
lbs_sizer=wx.GridSizer(rows=1,cols=3,hgap=10,vgap=3)
types_label=wx.StaticText(panel_lab,label="Paneles")
lbl_sizer.Add(types_label,flag=wx.ALL|wx.EXPAND,border=10)
bands_label=wx.StaticText(panel_lab,label="Bandas 5'UTR")
lbl_sizer.Add(bands_label,flag=wx.ALL|wx.EXPAND,border=10)
core_label=wx.StaticText(panel_lab,label="Bandas core")
lbl_sizer.Add(core_label,flag=wx.ALL|wx.EXPAND,border=10)
lb_types=wx.ListBox(panel_lb,id=-1,choices=types,style=wx.LB_SINGLE)
lbs_sizer.Add(lb_types,flag=wx.ALL|wx.EXPAND,border=10)
lb_types.Bind(wx.EVT_LISTBOX_DCLICK,lb_types_dclick)
lb_bandas=wx.CheckListBox(panel_lb,id=-1,choices=["Haga doble doble click en la lista de paneles"],style=wx.LB_SINGLE)
lbs_sizer.Add(lb_bandas,flag=wx.ALL|wx.EXPAND,border=10)
lb_bandas.Bind(wx.EVT_CHECKLISTBOX,check_band)
lb_core=wx.CheckListBox(panel_lb,id=-1,choices=core,style=wx.LB_SINGLE)
lbs_sizer.Add(lb_core,flag=wx.ALL|wx.EXPAND,border=10)
lb_core.Bind(wx.EVT_CHECKLISTBOX,check_band)
text_label=wx.StaticText(mainpanel,label="Resultado")
mainsizer.Add(text_label,flag=wx.ALL|wx.EXPAND,border=10)
resultados=wx.TextCtrl(mainpanel,style=wx.TE_MULTILINE)
mainsizer.Add(resultados,flag=wx.ALL|wx.EXPAND,border=10)
sym_panel=wx.Panel(mainpanel)
mainsizer.Add(sym_panel,flag=wx.EXPAND)
sym_sizer=wx.GridSizer(rows=1,cols=3,hgap=10,vgap=3)
sym_check=wx.CheckBox(sym_panel,label=" Simulador")
sym_sizer.Add(sym_check,flag=wx.ALL|wx.EXPAND,border=10)
sym_check.Bind(wx.EVT_CHECKBOX,simulate_start)
sym_label=wx.StaticText(sym_panel,label="Genotipo VHC a simular:")
sym_sizer.Add(sym_label,flag=wx.ALL|wx.EXPAND,border=10)
sym_combo=wx.ComboBox(sym_panel,choices=mycos)
sym_sizer.Add(sym_combo,flag=wx.ALL|wx.EXPAND,border=10)
sym_combo.Bind(wx.EVT_COMBOBOX,simulate)
btn_panel=wx.Panel(mainpanel)
mainsizer.Add(btn_panel,flag=wx.EXPAND)
btn_sizer=wx.GridSizer(rows=1,cols=3,hgap=10,vgap=3)
calcular=wx.Button(btn_panel,id=-1,label="Calcular")
btn_sizer.Add(calcular,flag=wx.ALL|wx.EXPAND,border=10)
calcular.Bind(wx.EVT_BUTTON,calcular_click)
limpiar=wx.Button(btn_panel,id=-1,label="Limpiar")
btn_sizer.Add(limpiar,flag=wx.ALL|wx.EXPAND,border=10)
limpiar.Bind(wx.EVT_BUTTON,limpiar_click)
salir=wx.Button(btn_panel,id=-1,label="Salir")
btn_sizer.Add(salir,flag=wx.ALL|wx.EXPAND,border=10)
salir.Bind(wx.EVT_BUTTON,salir_click)



lb_bandas.SetMinSize([150,300])
lb_bandas.Enable(False)
lb_core.Enable(False)
calcular.Enable(False)
#Simulador
sym_label.Enable(False)
sym_combo.Enable(False)
resultados.SetMinSize([150,200])
#mainpanel.SetSize([800,800])
mainpanel.SetSizer(mainsizer)
btn_panel.SetSizer(btn_sizer)
panel_lb.SetSizer(lbs_sizer)
panel_lab.SetSizer(lbl_sizer)
sym_panel.SetSizer(sym_sizer)
main.SetTitle("Genotipo VHC");
main.SetIcon(wx.Icon('icono.ico'))
main.Show()




root.MainLoop()
