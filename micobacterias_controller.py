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
    "M. fortuitum 1" : [1,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0],
    "M. fortuitum 2/M. magentense" : [1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
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

# as_interp={
    # "Bacteria Gram Positiva con alto contenido en G+C" : [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # "Mycobacterium spp." : [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # "M. simiae" : [1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
    # "M. mucogenicum" : [1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0],
    # "M. goodii" : [1,1,1,0,1,1,0,0,0,0,0,0,0,1,0,0,0],
    # "M. celatum I + III" : [1,1,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0],
    # "M. smegmatis" : [1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    # "M. genavense/M. triplex" : [1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
    # "M. lentiflavum" : [1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0],
    # "M. heckeshornense" : [1,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0],
    # "M. szulgai/M. intermedium" : [1,1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
    # "M. phlei" : [1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0],
    # "M. haemophilum" : [1,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0],
    # "M. kansasii I" : [1,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0],
    # "M. kansasii II" : [1,1,1,0,0,0,0,0,1,1,0,1,1,0,0,0,0],
    # "M. kansasii III" : [1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0],
    # "M. kansasii IV" : [1,1,1,0,0,0,0,0,0,1,0,1,1,0,0,0,0],
    # "M. ulcerans" : [1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
    # "M. gastri" : [1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
    # "M. asiaticum" : [1,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0],
    # "M. shimodei" : [1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0]
    # }
#Cambio de version del AS
as_interp={
    "Bacteria Gram Positiva con alto contenido en G+C" : [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Mycobacterium spp." : [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "M. simiae" : [1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
    "M. mucogenicum" : [1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0],
    "M. goodii" : [1,1,1,0,1,1,0,0,0,0,0,0,0,1,0,0,0],
    "M. celatum I + III" : [1,1,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0],
    "M. smegmatis" : [1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    "M. genavense/M. triplex" : [1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
    "M. lentiflavum" : [1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0],
    "M. heckeshornense" : [1,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0],

    "M. szulgai(perfil 1)" : [1,1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0],
    "M. szulgai(perfil 2)/Intermedium" : [1,1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
    #"M. intermedium" : [1,1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0],

    "M. phlei" : [1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0],
    "M. haemophilum" : [1,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0],

    "M. kansasii(perfil 1)" : [1,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0],
    "M. kansasii(perfil 2)" : [1,1,1,0,0,0,0,0,0,1,0,1,1,0,0,0,0],

    "M. ulcerans" : [1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
    "M. gastri" : [1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
    "M. asiaticum" : [1,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0],
    "M. shimodei" : [1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0]
    }

#Todas las micobacterias
mycos=cm_interp.keys() + as_interp.keys()

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
    for item in cm_interp:
        temp= cm_interp[item]
        for el in bands:
            if el>2 and temp[el]==1:
                similes.append([item,get_bands(temp)])
                break
    for item in as_interp:
        temp= as_interp[item]
        for el in bands:
            if el>2 and temp[el]==1:
                similes.append([item,get_bands(temp)])
                break
    return similes

def calcular_click(evt):
    global tabla
    #Asegurar que hay una tabla seleccionada si esta calcular activo!
    if not tabla: tabla = cm_interp 
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
    if sel=='Panel AS': 
        tabla = as_interp
    elif sel=='Panel CM': 
        tabla = cm_interp
    else:
        dlg = wx.MessageDialog(main, 'Panel pendiente de implementar', 'Panel no implementado', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    if sel in ['Panel AS','Panel CM']:
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
    if mb in cm_interp:
        panel='Panel CM'
        bandas=cm_interp[mb]
    else:
        panel='Panel AS'
        bandas=as_interp[mb]
    lb_bandas.Enable(True)
    limpiar_click(evt)
    bs= get_bands(bandas)
    for item in [x-1 for x in bs]:
        lb_bandas.Check(item,True)
    resultados.SetValue('%s esta en %s'%(mb,panel) + '\nPresenta las siguientes bandas: %s'%str(bs) )