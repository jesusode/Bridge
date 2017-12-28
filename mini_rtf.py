


#Cambio para poder crear y usar RTF-------------------------------------
import PyRTF
import os
#-----------------------------------------------------------------------

#Tablas para RTF--------------------------------------------------
RTF_PAPERS=[
 'LETTER'             ,
 'LETTERSMALL'        ,
 'TABLOID'            ,
 'LEDGER'             ,
 'LEGAL'              ,
 'STATEMENT'          ,
 'EXECUTIVE'          ,
 'A3'                 ,
 'A4'                 ,
 'A4SMALL'            ,
 'A5'                 , 
 'B4'                 ,
 'B5'                 ,
 'FOLIO'              ,
 'QUARTO'             ,
 '10X14'              , 
 '11X17'              ,
 'NOTE'               ,
 'ENV_9'              ,
 'ENV_10'             ,
 'ENV_11'             ,
 'ENV_12'             ,
 'ENV_14'             ,
 'CSHEET'             ,
 'DSHEET'             ,
 'ESHEET'             ,
 'ENV_DL'             ,
 'ENV_C5'             ,
 'ENV_C3'             ,
 'ENV_C4'             ,
 'ENV_C6'             ,
 'ENV_C65'            ,
 'ENV_B4'             ,
 'ENV_B5'             ,
 'ENV_B6'             ,
 'ENV_ITALY'          ,
 'ENV_MONARCH'        ,
 'ENV_PERSONAL'       ,
 'FANFOLD_US'         ,
 'FANFOLD_STD_GERMAN' ,
 'FANFOLD_LGL_GERMAN' 
]

RTF_FONTS=[
 'Arial'                   ,
 'Arial Black'             ,
 'Arial Narrow'            ,
 'Bitstream Vera Sans Mono',
 'Bitstream Vera Sans'     ,
 'Bitstream Vera Serif'    ,
 'Book Antiqua'            ,
 'Bookman Old Style'       ,
 'Castellar'               ,
 'Century Gothic'          ,
 'Comic Sans MS'           ,
 'Courier New'             ,
 'Franklin Gothic Medium'  ,
 'Garamond'                ,
 'Georgia'                 , 
 'Haettenschweiler'        , 
 'Impact'                  ,
 'Lucida Console'          , 
 'Lucida Sans Unicode'     , 
 'Microsoft Sans Serif'    , 
 'Monotype Corsiva'        , 
 'Palatino Linotype'       , 
 'Papyrus'                 , 
 'Sylfaen'                 , 
 'Symbol'                  , 
 'Tahoma'                  , 
 'Times New Roman'         , 
 'Trebuchet MS'            , 
 'Verdana'                 
]

RTF_COLORS=[
 'black', 
 'blue',  
 'turquoise',
 'green', 
 'pink', 
 'red', 
 'yellow',
 'white', 
 'darkblue', 
 'teal', 
 'darkgreen',
 'violet', 
 'darkred',
 'rdarkyellow',
 'darkgrey',
 'grey'
]

RTF_ALIGNMENT=[
 'left',
 'right',
 'center',
 'justify',
 'distribute'
]

RTF_BORDER_STYLES=[
 'single', 'double', 'shadowed', 'doubled', 'dotted','dashed', 'hairline'
]

RTF_SHADING_PATTERNS=['horizontal',
				 'vertical',
				 'forward_diagonal',
				 'backward_diagonal',
				 'vertical_cross',
				 'diagonal_cross',
				 'dark_horizontal',
				 'dark_vertical',
				 'dark_forward_diagonal',
				 'dark_backward_diagonal',
				 'dark_vertical_cross',
				 'dark_diagonal_cross' ]


RTF_TAB_ALIGNMENT=['left', 'right', 'center', 'decimal' ]

RTF_TAB_LEADERS=['dots', 'hyphens', 'underline', 'thick_line', 'equal_sign' ]

RTF_SECTION_BREAK_TYPES= [ 'none', 'column', 'page', 'even', 'odd' ]

RTF_TABLE_ALIGNMENT = [ 'left', 'right', 'center']

RTF_TABLE_WRAPPING = [ 'no_wrap', 'wrap_around' ]

RTF_CELL_ALIGN={'top': 1, 'center': 2, 'bottom' : 3}

RTF_CELL_FLOW={
    'lr_tb'          : 1,
    'rl_tb'          : 2,
    'lr_bt'          : 3,
    'vertical_lr_tb' : 4,
    'vertical_tb_lr' : 5 }

__RTFS__={}
__RTFCELLS__={}
__RTFPARS__={}
__RTFSECTIONS__={}
__RTFTABLES__={}

#----------------------------------------------------------------

#-----------------------------------------------------
#     Funciones para manejo de RTF
#----------------------------------------------------- 
def rtfCreateDoc(*args):
    if len(args) !=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfCreateDoc(name, title)'''
        raise Exception(msg)      
    __RTFS__[args[0]]=PyRTF.Document()
    __RTFS__[args[0]].SetTitle(args[1])  
    return 1


def rtfSaveDoc(*args):
    if len(args) !=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfSaveDoc(doc_name, path)'''
        #
        raise Exception(msg)   
    else:
        doc=__RTFS__[args[0]]
        r = PyRTF.Renderer()
        r.Write(doc,file( args[1], 'w' ))
    return 1


def rtfCreateSection(*args):
    if len(args) not in [1,11]:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfCreateSection(name,paper,margin_t,margin_l,margin_b,margin_r,landscape,headery,footery,numcols, break_type)'''
        raise Exception(msg);       
    paper=8 #por defecto es A4
    margins=PyRTF.MarginsPropertySet( top=1000, left=1200, bottom=1000, right=1200 )
    heady=None
    footy=None
    breakt=None
    numcols=1
    landscape=0
    try:
        paper=RTF_PAPERS.index(args[1].strip())
        margins=PyRTF.MarginsPropertySet( int(args[2]), int(args[3]), int(args[4]), int(args[5]) )
        heady=int(args[7])
        footy=int(args[8])
        if args[10].strip() in RTF_SECTION_BREAK_TYPES: breakt=PyRTF.Section.BREAK_TYPES[RTF_SECTION_BREAK_TYPES.index(args[10].strip())]
        numcols=int(args[9])
    except:
        pass
    __RTFSECTIONS__[args[0]]=PyRTF.Section(paper=PyRTF.StandardPaper[paper], landscape=landscape, margins=margins, headery=heady, footery=footy, break_type=breakt, cols=numcols) 
    return 1


def rtfSetHeader(*args):
    if len(args) !=8:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfSetHeader(sec_name, text, font, size, bold, italic, underline, colour))'''
        #
        raise Exception(msg)
    if not __RTFSECTIONS__.has_key(args[0]):
        raise Exception('Error: La seccion RTF "%s" no esta definida.' % args[0])
    else:
        p=PyRTF.Paragraph()
        f=0 #Por defecto Arial
        col=PyRTF.StandardColours[0] #Por defecto negro
        b=int(args[4])==1 or None
        i=int(args[5])==1 or None
        u=int(args[6])==1 or None
        try:
            col=PyRTF.StandardColours[RTF_COLORS.index(args[7].strip())]
            f=RTF_FONTS.index(args[2].strip())
        except:
            pass
        p.append(PyRTF.TEXT(args[1],font=PyRTF.StandardFonts[f],size=int(args[3]),colour=col, italic=i, bold=b, underline=u))
        __RTFSECTIONS__[args[0]].Header.append(p)
    return 1


def rtfSetFooter(*args):
    if len(args) !=8:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfSetFooter(sec_name, text, font, size, bold, italic, underline, colour))'''
        #
        raise Exception(msg)
    if not __RTFSECTIONS__.has_key(args[0]):
        raise Exception('Error: La seccion RTF "%s" no esta definida.' % args[0])
    else:
        p=PyRTF.Paragraph()
        f=0 #Por defecto Arial
        col=PyRTF.StandardColours[0] #Por defecto negro
        b=int(args[4])==1 or None
        i=int(args[5])==1 or None
        u=int(args[6])==1 or None
        try:
            col=PyRTF.StandardColours[RTF_COLORS.index(args[7].strip())]
            f=RTF_FONTS.index(args[2].strip())
        except:
            pass
        p.append(PyRTF.TEXT(args[1],font=PyRTF.StandardFonts[f],size=int(args[3]),colour=col, italic=i, bold=b, underline=u))        
        __RTFSECTIONS__[args[0]].Footer.append(p)
    return 1




def rtfAddText(*args):
    if len(args) !=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfAddText(sec_name, text)'''
        #
        raise Exception(msg)
    if not __RTFSECTIONS__.has_key(args[0]):
        raise Exception('Error: La seccion RTF "%s" no esta definida.' % args[0])
    else:
        p=PyRTF.Paragraph()
        p.append(args[1])
        __RTFSECTIONS__[args[0]].append(p)
    return 1


def rtfAddPageBreak(*args):
    if len(args) !=1:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfAddPageBreak(sec_name)'''
        #
        raise Exception(msg)
    if not __RTFSECTIONS__.has_key(args[0]):
        raise Exception('Error: La seccion RTF "%s" no esta definida.' % args[0])
    else:
        p=PyRTF.Paragraph(None,PyRTF.ParagraphPS().SetPageBreakBefore( True ))
        p.append('')
        __RTFSECTIONS__[args[0]].append(p)   


def rtfAddStyledText(*args):
    if len(args) !=8:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfAddStyledText(sec_name, text, font, size, bold, italic, underline, colour)'''
        #
        raise Exception(msg)
    if not __RTFSECTIONS__.has_key(args[0]):
        raise Exception('Error: La seccion RTF "%s" no esta definida.' % args[0])
    else:
        p=PyRTF.Paragraph()
        f=0 #Por defecto Arial
        col=PyRTF.StandardColours[0] #Por defecto negro
        b=int(args[4])==1 or None
        i=int(args[5])==1 or None
        u=int(args[6])==1 or None
        try:
            col=PyRTF.StandardColours[RTF_COLORS.index(args[7].strip())]
            f=RTF_FONTS.index(args[2].strip())
        except:
            pass
        p.append(PyRTF.TEXT(args[1],font=PyRTF.StandardFonts[f],size=int(args[3]),colour=col, italic=i, bold=b, underline=u))
        __RTFSECTIONS__[args[0]].append(p)
    return 1


def rtfAddSection(*args):
    if len(args) !=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfAddSection(doc_name, sec_name)'''
        #
        raise Exception(msg)
    if not __RTFS__.has_key(args[0]):
        raise Exception('Error: El documento RTF "%s" no esta definido.' % args[0])    
    if not __RTFSECTIONS__.has_key(args[1]):
        raise Exception('Error: La seccion RTF "%s" no esta definida.' % args[1])
    else:
        __RTFS__[args[0]].Sections.append(__RTFSECTIONS__[args[1]])
    return 1


def rtfAddImage(*args):
    if len(args) !=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfAddImage(sec_name, img_path)'''
        #
        raise Exception(msg)
    if not __RTFSECTIONS__.has_key(args[0]):
        raise Exception('Error: La seccion RTF "%s" no esta definida.' % args[0])
    else:
        __RTFSECTIONS__[args[0]].append(PyRTF.Paragraph(PyRTF.Image(args[1])))
    return 1



def rtfOpenParagraph(*args):
    if len(args) not in [1,2]:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfOpenParagraph(name, props_dict_name)'''
        raise Exception(msg)      
    #Si hay diccionario de propiedades, crear estilo de parrafo y aplicarlo
    if len(args)==2:
        props=args[1]
        parst=PyRTF.ParagraphPropertySet()
        #Propiedades definidas para un paragraph: alignment, tabs, space_after, space_before, first_line_indent
        #left_indent, right_indent space_between_lines. Por defecto estan a None
        align=props.get('text-align',None)
        if align in RTF_ALIGNMENT:
            align=RTF_ALIGNMENT.index(align)
        else:
            align=0
        flind=props.get('first-line-indent',None)
        if flind: flind=int(flind)
        spaft=props.get('space-after',None)
        if spaft: spaft=int(spaft)
        spbef=props.get('space-before',None)
        if spbef: spbef=int(spbef)
        linesp=props.get('space-between-lines',None)
        if linesp: linesp=int(linesp)
        lind=props.get('left-indent',None)
        if lind: lind=int(lind)
        rind=props.get('right-indent',None)
        if rind: rind=int(rind)            
        parst.SetAlignment(PyRTF.ParagraphPropertySet.ALIGNMENT[align])
        parst.SetFirstLineIndent(flind)
        parst.SetSpaceAfter(spaft)
        parst.SetSpaceBefore(spbef)
        parst.SetSpaceBetweenLines(linesp)
        parst.SetLeftIndent(lind)
        parst.SetRightIndent(rind)
        
        #Propiedades del borde si lo hay (deben ir en un FramePropertySet: width, style, colour, space
        ##Poner un borde generico!!!! 
        btw=props.get('border-top-width',None)
        if btw: btw=int(btw)
        bts=props.get('border-top-space',None)
        if bts: bts=int(bts)
        btc=props.get('border-top-color',None)
        if btc and btc in RTF_COLORS: btc=PyRTF.StandardColours[RTF_COLORS.index(btc)]
        bts=props.get('border-top-style',None)
        if bts and bts in RTF_BORDER_STYLES: bts=PyRTF.BorderPropertySet.STYLES[RTF_BORDER_STYLES.index(bts)]       

        bbw=props.get('border-bottom-width',None)
        if bbw: bbw=int(bbw)
        bbs=props.get('border-bottom-space',None)
        if bbs: bbs=int(bbs)
        bbc=props.get('border-bottom-color',None)
        if bbc and bbc in RTF_COLORS: bbc=PyRTF.StandardColours[RTF_COLORS.index(bbc)]
        bbs=props.get('border-bottom-style',None)
        if bbs and bbs in RTF_BORDER_STYLES: bbs=PyRTF.BorderPropertySet.STYLES[RTF_BORDER_STYLES.index(bbs)]      

        blw=props.get('border-left-width',None)
        if blw: blw=int(blw)
        bls=props.get('border-left-space',None)
        if bls: bls=int(bls)
        blc=props.get('border-left-color',None)
        if blc and blc in RTF_COLORS: blc=PyRTF.StandardColours[RTF_COLORS.index(blc)]
        bls=props.get('border-left-style',None)
        if bls and bls in RTF_BORDER_STYLES: bls=PyRTF.BorderPropertySet.STYLES[RTF_BORDER_STYLES.index(bls)]      

        brw=props.get('border-right-width',None)
        if brw: brw=int(brw)
        brs=props.get('border-right-space',None)
        if brs: brs=int(brs)
        brc=props.get('border-right-color',None)
        if brc and brc in RTF_COLORS: brc=PyRTF.StandardColours[RTF_COLORS.index(brc)]
        brs=props.get('border-right-style',None)
        if brs and brs in RTF_BORDER_STYLES: brs=PyRTF.BorderPropertySet.STYLES[RTF_BORDER_STYLES.index(brs)]
        
        borderst=bordersb=bordersl=bordersr=None
       
        if btw: borderst=PyRTF.BorderPropertySet(width=btw, spacing=bts, colour=btc, style=bts)
        if bbw: bordersb=PyRTF.BorderPropertySet(width=bbw, spacing=bbs, colour=bbc, style=bbs)
        if blw: bordersl=PyRTF.BorderPropertySet(width=blw, spacing=bls, colour=blc, style=bls)
        if brw: bordersr=PyRTF.BorderPropertySet(width=brw, spacing=brs, colour=brc, style=brs)
        framest=PyRTF.FramePropertySet(top=borderst,left=bordersl,bottom=bordersb,right=bordersr)
        #Propiedades de sombreado si las hay:  shading=None, pattern=None, foreground=None, background=None
        sh=props.get('shading',None)
        if sh: sh=int(sh)
        shpat=props.get('shading-pattern',None)
        if shpat and shpat in RTF_SHADING_PATTERNS: shpat=PyRTF.ShadingPropertySet.PATTERNS[RTF_SHADING_PATTERNS.index(shpat)]
        shcol=props.get('shading-color',None)
        if shcol and shcol in RTF_COLORS: shcol=PyRTF.StandardColours[RTF_COLORS.index(shcol)]
        shbgcol=props.get('shading-bgcolor',None)
        if shbgcol and shbgcol in RTF_COLORS: shbgcol=PyRTF.StandardColours[RTF_COLORS.index(shbgcol)]
        shadingst=PyRTF.ShadingPropertySet(shading=sh, pattern=shpat, foreground=shcol, background=shbgcol)
        __RTFPARS__[args[0]]=PyRTF.Paragraph(parst,framest,shadingst)          
    else:
        __RTFPARS__[args[0]]=PyRTF.Paragraph()       
    return 1    


def rtfFillParagraph(*args):
    if len(args) !=9:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfGetParagraph(name,text_or_image, font, size, bold, italic, underline, colour, is_image)'''
        raise Exception(msg)
    if not __RTFPARS__.has_key(args[0]):
        raise Exception('Error: El parrafo RTF "%s" no esta definido.' % args[0])
    if int(args[8])==1: #Es una imagen
        __RTFPARS__[args[0]].append(PyRTF.Image(args[1]))
    else: #Es un texto
        f=0 #Por defecto Arial
        col=PyRTF.StandardColours[0] #Por defecto negro
        b=int(args[4])==1 or None
        i=int(args[5])==1 or None
        u=int(args[6])==1 or None
        try:
            col=PyRTF.StandardColours[RTF_COLORS.index(args[7].strip())]
            f=RTF_FONTS.index(args[2].strip())
        except:
            pass
        __RTFPARS__[args[0]].append(PyRTF.TEXT(args[1],font=PyRTF.StandardFonts[f],size=int(args[3]),colour=col, italic=i, bold=b, underline=u))
    return 1    


def rtfAddParagraph(*args):
    if len(args) !=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfAddParagraph(name,sec_name)'''
        raise Exception(msg)
    if not __RTFPARS__.has_key(args[0]):
        raise Exception('Error: El parrafo RTF "%s" no esta definido.' % args[0])
    if not __RTFSECTIONS__.has_key(args[1]):
        raise Exception('Error: La seccion RTF "%s" no esta definida.' % args[1])    
    __RTFSECTIONS__[args[1]].append(__RTFPARS__[args[0]])
    return 1    


def rtfCreateTable(*args):
    if len(args) < 5:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfCreateTable(name,align, left_offset, gap_between_cells, col1,col2,...,coln)'''
        raise Exception(msg)     
    align=args[1]
    if align.strip() in RTF_TABLE_ALIGNMENT:
        align=PyRTF.Table.ALIGNMENT[RTF_TABLE_ALIGNMENT.index(align.strip())]
    loffset=int(args[2])
    cells_gap=int(args[3])
    cols=[int(i) for i in args[4:]]
    kw={'alignment':align, 'left_offset':loffset, 'gap_between_cells':cells_gap}
    __RTFTABLES__[args[0]]=PyRTF.Table(*cols, **kw)   
    return 1    




def rtfAddTableRow(*args):
    if len(args) < 2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfAddTableRow(table_name,cell1,cell2,...,celln)'''
        raise Exception(msg)
    if not __RTFTABLES__.has_key(args[0]):
        raise Exception('Error: La tabla RTF "%s" no esta definida.' % args[0])
    
    #cels=[PyRTF.Cell(i) for i in args[1:]]
    #Si el valor de cell se corresponde al nombre de una celda definida,
    #la ponemos. Si no, ponerlo como literal.
    cels=[]
    for item in args[1:]:
        if __RTFCELLS__.has_key(item):
            cels.append(__RTFCELLS__[item])
        else:
            cels.append(PyRTF.Cell(item))
    __RTFTABLES__[args[0]].AddRow(*cels)
    return 1


def rtfAddTable(*args):
    if len(args) != 2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfAddTable(table_name,sec_name)'''
        raise Exception(msg)
    if not __RTFTABLES__.has_key(args[0]):
        raise Exception('Error: La tabla RTF "%s" no esta definida.' % args[0])
    if not __RTFSECTIONS__.has_key(args[1]):
        raise Exception('Error: La seccion RTF "%s" no esta definida.' % args[1])        
    __RTFSECTIONS__[args[1]].append(__RTFTABLES__[args[0]])
    return 1


def rtfCreateCell(*args):
    if len(args) < 3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _rtfCreateCell(name, par_name, style_dict_name)'''
        raise Exception(msg)     
    if not __RTFPARS__.has_key(args[1]):
        raise Exception('Error: El Parrafo RTF "%s" no esta definido.' % args[1])
    props=args[2]
    align=props.get('alignment',None)
    if align in RTF_ALIGNMENT:
        align=RTF_CELL_ALIGNMENT.index(align)
    else:
        align=0
    flow=props.get('flow',None)
    if flow in RTF_CELL_FLOW:
        flow=RTF_CELL_FLOW.index(flow)
    else:
        flow=0        
    span=props.get('colspan',1)
    if span: span=int(span)
    vmerge=props.get('vertical-merge',False)
    if vmerge: vmerge=True
    svmerge=props.get('start-vertical-merge',False)
    if svmerge: svmerge=True
    cell=PyRTF.Cell(__RTFPARS__[args[1]])
    __RTFCELLS__[args[0]]=cell  
    return 1

'''
section.append( 'Table Three' )
    table = Table( col1, col2, col3, col4 )
    table.AddRow( Cell( 'This is pretty amazing', flow=Cell.FLOW_LR_BT, start_vertical_merge=True ),
                  Cell( 'one' ), Cell( 'two' ), Cell( 'three' ) )

    for i in range( 10 ) :  
        table.AddRow( Cell( vertical_merge=True ),
                      Cell( 'one' ), Cell( 'two' ), Cell( 'three' ) )
    section.append( table )
'''
