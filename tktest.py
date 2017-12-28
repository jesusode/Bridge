


import wx

#Codigo del controlador de micobacterias

bands=['Banda 1','Banda 2','Banda 3','Banda 4',
'Banda 5','Banda 6','Banda 7','Banda 8',
'Banda 9','Banda 10','Banda 11','Banda 12',
'Banda 13','Banda 14','Banda 15','Banda 16','Banda 17']

types=['Panel CM','Panel AS','Panel PL','Panel SL']

cm_interp={
    "Bacteria Gram Positiva con alto contenido en G+C" : [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Mycobacterium spp." : [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "M. avium" : [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "M. chelonae/M. immugenicum" : [1,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0],
    "M. abscessus/M. inmugenicum" : [1,1,1,0,1,1,0,0,0,1,0,0,0,0,0,0,0],
    "M. fortuitum/M. magentense" : [1,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0],
    "M. gordonae" : [1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0],
    "M. intracellulare." : [1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    "M. scrofulaceum" : [1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
    "M. interjectum" : [1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
    "M. kansasii" : [1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0],
    "M. malmoense/M. haemophilum/M. palustre" : [1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0],
    "M. marinum/M. ulcerans" : [1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0],
    "M. tuberculosis complex" : [1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0],
    "M. peregrinum/M. alvei/M. septicum" : [1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    "M. xenopi" : [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    }

def callb(evt):
    print 'callback llamado!'

def lb_bandas_check(evt):
    print 'Cambiado estado en item de lista de bandas!'

def lb_types_check(evt):
    print 'Cambiado estado en item de lista de tipos!'


root=wx.App()

main=wx.Frame(parent=None)
mainpanel=wx.Panel(main)
mainsizer=wx.BoxSizer(orient=wx.VERTICAL)
panel_lab=wx.Panel(mainpanel)
mainsizer.Add(panel_lab,flag=wx.EXPAND)
lbl_sizer=wx.GridSizer(rows=1,cols=2,hgap=10,vgap=3)
panel_lb=wx.Panel(mainpanel)
mainsizer.Add(panel_lb,flag=wx.EXPAND)
lbs_sizer=wx.GridSizer(rows=1,cols=2,hgap=10,vgap=3)
types_label=wx.StaticText(panel_lab,label="Paneles")
lbl_sizer.Add(types_label,flag=wx.ALL|wx.EXPAND,border=10)
bands_label=wx.StaticText(panel_lab,label="Bandas")
lbl_sizer.Add(bands_label,flag=wx.ALL|wx.EXPAND,border=10)
lb_types=wx.ListBox(panel_lb,id=-1,choices=types,style=wx.LB_SINGLE)
lbs_sizer.Add(lb_types,flag=wx.ALL|wx.EXPAND,border=10)
lb_types.Bind(wx.EVT_LISTBOX_DCLICK,lb_types_check)
lb_bandas=wx.CheckListBox(panel_lb,id=-1,choices=bands,style=wx.LB_SINGLE)
lbs_sizer.Add(lb_bandas,flag=wx.ALL|wx.EXPAND,border=10)
lb_bandas.Bind(wx.EVT_CHECKLISTBOX,lb_bandas_check)
resultados=wx.TextCtrl(mainpanel,style=wx.TE_MULTILINE)
mainsizer.Add(resultados,flag=wx.ALL|wx.EXPAND,border=10)
btn_panel=wx.Panel(mainpanel)
mainsizer.Add(btn_panel)
btn_sizer=wx.GridSizer(rows=1,cols=3,hgap=10,vgap=3)
calcular=wx.Button(btn_panel,id=-1,label="Calcular")
btn_sizer.Add(calcular,flag=wx.EXPAND,border=10)
calcular.Bind(wx.EVT_BUTTON,callb)
limpiar=wx.Button(btn_panel,id=-1,label="Limpiar")
btn_sizer.Add(limpiar,flag=wx.EXPAND,border=10)
calcular.Bind(wx.EVT_BUTTON,callb)
calcular=wx.Button(btn_panel,id=-1,label="Salir")
btn_sizer.Add(calcular,flag=wx.EXPAND,border=10)
calcular.Bind(wx.EVT_BUTTON,callb)



lb_bandas.SetMinSize([150,300])
resultados.SetMinSize([150,200])
mainpanel.SetMinSize([1000,1200])
mainpanel.SetSizer(mainsizer)
btn_panel.SetSizer(btn_sizer)
panel_lb.SetSizer(lbs_sizer)
panel_lab.SetSizer(lbl_sizer)
calcular.SetMinSize([300,30])
main.SetTitle("Paneles de Micobacterias");
main.Show()




root.MainLoop()
