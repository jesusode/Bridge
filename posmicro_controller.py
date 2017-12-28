#Posmicro_controller

import adoV6
import wx_support
import string
import codecs

constr="DRIVER={sql server};server=openlabdb.intranet.net;Database=OpenData;UID=openlab;PWD=Pat1t0degoma";
colnames=["fcrea","ana","idee","nhisto","servicio","nombre","apell1","apell2","muestra","organismo","ufcs","observ"]
solo_hospi=0

querystr='''
    select opendata.dbo.resorganismos.fcrea,openconf.dbo.ana.abr as ana,
    opendata.dbo.pet.idee,
    opendata.dbo.pac.nhisto,
    openconf.dbo.ser.nombre as servicio,
    opendata.dbo.pac.nombre,
    opendata.dbo.pac.apell1,
    opendata.dbo.pac.apell2,
    openconf.dbo.muestras.abr as muestra,
    openconf.dbo.microorganismos.nombre as organismo,
    opendata.dbo.resorganismos.ufcs,
    opendata.dbo.resorganismos.obs
     from opendata.dbo.resorganismos,opendata.dbo.pac,
    openconf.dbo.ana,openconf.dbo.microorganismos,
    opendata.dbo.pet,openconf.dbo.muestras,
    openconf.dbo.ser
    where opendata.dbo.resorganismos.fcrea  between '%s' and '%s'  
    and opendata.dbo.resorganismos.pac=opendata.dbo.pac.nid
    and opendata.dbo.resorganismos.pet=opendata.dbo.pet.nid
    and opendata.dbo.resorganismos.muestra=openconf.dbo.muestras.nid
    and opendata.dbo.resorganismos.estudio=openconf.dbo.ana.nid
    and opendata.dbo.resorganismos.organismo=openconf.dbo.microorganismos.nid
    and opendata.dbo.pet.serv1=openconf.dbo.ser.nid
    order by opendata.dbo.resorganismos.fcrea;
'''

def do_query(constr,query):
    con=adoV6.Connection(constr,1).getConnection()
    rst=adoV6.Recordset()
    rst.open(query,con)
    fnames=rst.getFieldsNames()
    filas=rst.getRows()
    rst.close()
    table=[]
    for i in range(len(filas[0])):
        temp=[]
        for j in range(len(filas)):
            temp.append(filas[j][i])
        table.append(temp)
    return table

def procesar_click(evt):
    global solo_hospi
    procesar.Enable(False)
    main.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))
    date1=fini.GetValue()
    date2=fend.GetValue()
    #Fechas formateadas para el SQL Server
    f1="{0}{1:0>2d}{2:0>2d}".format(date1.GetYear(),date1.GetMonth()+1,date1.GetDay())
    f2="{0}{1:0>2d}{2:0>2d}".format(date2.GetYear(),date2.GetMonth()+1,date2.GetDay())
    query=querystr%(f1,f2)
    query=query.strip()
    model=do_query(constr,query)
    model=wx_support.MinimalGridTableModel(len(model),len(model[0]),model,colnames,map(str,range(len(model))))
    tabla.SetTable(model,True)
    tabla.AutoSizeColumns()
    tabla.Refresh()
    procesar.Enable(True)
    main.Fit()#?
    main.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

def excel_click(evt):
    cells= tabla.GetTable().GetData()
    filename=''
    dlg=wx.FileDialog(main, message="Guardar como CSV", defaultDir="",defaultFile="positivos_micro.csv", wildcard="*.*", style=wx.SAVE)
    if dlg.ShowModal() == wx.ID_OK:
        csv='\n'.join( ['\t'.join(map(string.strip,map(unicode,x))) for x in cells])
        csv='\t'.join(colnames) + '\n' + csv
        f=codecs.open(dlg.GetPath(), 'w', encoding='latin-1')
        f.write(csv)
        f.close()

def check_hospi(evt):
    global solo_hospi
    if hospicheck.IsChecked():
        solo_hospi=1
    else:
        solo_hospi=0

def row_dclick(evt):
    print 'doble click en fila'

def imprimir_click(evt):
    cells= tabla.GetTable().GetData()
    printer=wx.lib.printout.PrintTable(main)
    printer.SetLandscape()
    printer.SetHeader("Positivos Microbiologia")
    printer.SetFooter()
    printer.SetFooter("Fecha: ", type = "Date", align=wx.ALIGN_RIGHT, indent = -1, colour = wx.NamedColour('BLACK'))
    printer.data=cells
    printer.label=colnames
    printer.Preview()

def salir_click(evt):
    main.Destroy()