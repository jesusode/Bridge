import sys
import os
import pprint
import re

#PyPDF2------------------------------------------------------------
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter,PdfFileMerger
import fpdf
#-----------------------------------------------------------------

#Clase mixin que permite usar html
class Pdf(fpdf.FPDF,fpdf.HTMLMixin):
    def __init__(self,orientation='P',unit='mm',format='A4'):
        fpdf.FPDF.__init__(self,orientation,unit,format)
        fpdf.HTMLMixin.__init__(self)
        self.fixedels={}
        self.headerstr=''
        self.footerstr=''

    def getPageno(self,el):
        return self.page
        
    def header(self):
        self.processHeaderFooterFixed(self.headerstr)
        
    def footer(self):
        self.processHeaderFooterFixed(self.footerstr)
        
    def putfixedels(self):
        #Guardar offset antiguo
        oldy=self.get_y()
        #Escribir elementos fijos
        for el in self.fixedels:
            self.processHeaderFooterFixed(self.fixedels[el])
        #y recuperar el offset
        self.set_y(oldy)
        
    def addFixedEl(self,el,name):
        self.fixedels[name]=el

    def delFixedEl(self,el):
        if el in self.fixedels:
            del self.fixedels[el]       

    def processHeaderFooterFixed(self,text):
        if text=='':
            return
        for line in text.split('\n'):
            #Primero reemplazar el numero corriente de pagina si esta en la linea
            line=line.replace('%%pageno%%',str(self.page))
            m=re.search('%%\s*(Y|y)\s*\=\s*(\d+)\s*%%',line)
            if m!=None:
                self.set_y(int(m.group(2)))
                continue
            m=re.search('%%\s*(X|x)\s*\=\s*(\d+)\s*%%',line) #Esto no va
            if m!=None:
                self.set_x(int(m.group(2)))
                continue
            m=re.search('%%\s*rotate\s+(\d+)\s*%%',line)
            if m!=None:
                self.rotate(int(m.group(1)))
                continue             
            m=re.search('%%\s*space\s*\=\s*(\d+)\s*%%',line)
            if m!=None:
                self.ln(int(m.group(1)))
                continue            
            m=re.search('%%abstext\s+(\d+)\s*,\s*(\d+)\s*,\s*\"(.*)\"\s*,\s*((L|T|R|B){0,4})\s*,\s*(L|R|C){0,1}\s*,\s*(0|1){0,1}\s*,\s*(0|1){0,1}\s*%%',line)
            if m!=None:
                self.cell(int(m.group(1)),int(m.group(2)),txt=m.group(3),border=m.group(4),align=m.group(6),fill=int(m.group(7)))
                continue
            m=re.search('%%textcolor\s+(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*%%',line)
            if m!=None:
                self.set_text_color(int(m.group(1)),int(m.group(2)),int(m.group(3)))
                continue                
            m=re.search('%%drawcolor\s+(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*%%',line)
            if m!=None:
                self.set_draw_color(int(m.group(1)),int(m.group(2)),int(m.group(3)))
                continue             
            m=re.search('%%bgcolor\s+(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*%%',line)
            if m!=None:
                self.set_fill_color(int(m.group(1)),int(m.group(2)),int(m.group(3)))
                continue            
            m=re.search('%%line\s+(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*%%',line)
            if m!=None:
                self.line(int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)))
                continue
            m=re.search('%%rect\s+(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(FD|F|S)%%',line)
            if m!=None:
                self.rect(int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)),style=m.group(5))
                continue
            self.write_html(line)

def pdfGetNumPages(*args):#OK
    if len(args)!=1:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfGetNumPages(pdffile).
        '''
        raise Exception(msg)
    input1 = PyPDF2.PdfFileReader(file(args[0], "rb"))
    return input1.getNumPages()



def pdfConcat(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfConcat(pdffilelist,outfile).
        '''
        raise Exception(msg)
    merger = PdfFileMerger()
    if type(args[0])!=type([]):
        raise Exception('Error: se esperaba una lista de archivos')
    for item in args[0]:
        merger.append(fileobj=item)
    merger.write(open(args[1], 'wb'))
    return 1


def pdfGetPages(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfPages(filename,[pages]).
        '''
        raise Exception(msg)
    reader = PdfFileReader(file(args[0], "rb"))
    pages=[]
    for item in args[1]:
        pages.append(reader.getPage(item))
    return pages

def pdfGetPage(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfPages(filename,page).
        '''
        raise Exception(msg)
    reader = PdfFileReader(file(args[0], "rb"))
    return reader.getPage(args[1])


def pdfAddPages(*args):#OK
    if len(args)!=3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfAddPages(filename,[pages],outfile).
        '''
        raise Exception(msg)
    reader = PdfFileReader(file(args[0], "rb"))
    writer=PdfFileWriter()
    for i in range(reader.getNumPages()):
        writer.addPage(reader.getPage(i))    
    for page in args[1]:
        writer.addPage(page)
    writer.write(file(args[2],'wb'))        
    return 1


def pdfEncrypt(*args):#OK, pero requiere hackear PdfFileWriter.encrypt
    if len(args)!=3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfEncrypt(filename,password,newname).
        '''
        raise Exception(msg)
    reader = PdfFileReader(file(args[0], "rb"))
    writer=PdfFileWriter()   
    for i in range(reader.getNumPages()):
        writer.addPage(reader.getPage(i))
    #encriptar y guardar
    writer.encrypt(args[1])         
    writer.write(file(args[2],'wb'))
    return 1



def pdfFromPages(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfFromPages(pageslist,outfile).
        '''
        raise Exception(msg)
    writer=PdfFileWriter()   
    for page in args[0]:
        writer.addPage(page)
    #encriptar y guardar        
    writer.write(file(args[1],'wb'))
    return 1

def pdfTransformPages(*args):#FALLA!!
    if len(args)!=3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfTransformPages(pageslist,transform,argslist).
        '''
        raise Exception(msg)
    print repr(args[0])
    print 'numero de elementos: %s' % len(args[0])
    transforms=['rotatec','rotatecc','scale','transform']
    if args[1] not in transforms:
        raise Exception('Error: "%s" no es una transformacion permitida'%args[1])
    for page in args[0]:
        if args[1]=='rotatec':
            page.rotateClockwise(*args[2])
        elif args[1]=='rotatecc':
            page.rotateCounterClockwise(*args[2])
        elif args[1]=='scale':
            page.scale(*args[2])
        elif args[1]=='transform':
            page.addTransformation(*args[2]) #Debe ser una lista de 6 elementos
    return 1

def pdfMergePages(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfMergePages(page1,page2).
        '''
        raise Exception(msg)
    args[0].mergePage(args[1])
    return args[0]
            

#pdfGetInfo()
#pdfDocSetInfo(doc,title,author)

def pdfDoc(*args):#OK
    if len(args)not in [0,3]:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDoc() o _pdfDoc(orientation,unit,size).
        '''
        raise Exception(msg)
    if len(args)==0:
        #return fpdf.FPDF()
        pdf=Pdf()
        #pdf.alias_nb_pages()
        return pdf
    else:
        #El tercer argumento puede ser una cadena o una lista
        if type(args[2])==type([]):
            if not len(args[2])==2:
                raise Exception('Error: el descriptor de pagina debe ser una cadena o una lista de dos elementos')
        #return fpdf.FPDF(args[0],args[1],args[2])
        return Pdf(args[0],args[1],args[2])


def pdfDocSetInfo(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocSetInfo(pdfdoc,infodict).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    if type(args[1])!=type({}):
        raise Exception('Error: el segundo argumento de la funcion debe ser un diccionario')
    if 'author' in args[1]:
        args[0].set_author(args[1]['author'])
    if 'title' in args[1]:
        args[0].set_title(args[1]['title'])
    if 'creator' in args[1]:
        args[0].set_creator(args[1]['creator'])
    if 'subject' in args[1]:
        args[0].set_subject(args[1]['subject'])
    if 'keywords' in args[1]:
        args[0].set_keywords(args[1]['keywords'])         
    return 1    


def pdfDocSetMargins(*args):#OK
    if len(args)!=4:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocSetMargins(pdfdoc,left,top,right).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].set_margins(args[1],args[2],args[3])
    return 1

def pdfDocSetHeader(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocSetHeader(pdfdoc,headerstring).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].headerstr=args[1]
    return 1

def pdfDocSetFooter(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocSetFooter(pdfdoc,footerstring).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].footerstr=args[1]
    return 1


def pdfDocAddFixed(*args):#OK
    if len(args)!=3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocAddFixed(pdfdoc,fixedstring,name).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].addFixedEl(args[1],args[2])
    return args[2]

def pdfDocDeleteFixed(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocDeleteFixed(pdfdoc,name).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].delFixedEl(args[1])
    return 1


def pdfDocAddFont(*args):#OK
    if len(args)!=4:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocAddFont(pdfdoc,fontname,fontfile,unicode).
        '''
        raise Exception(msg)
    uni=True
    if args[3]==0:
        uni=False
    #Comprobar que es un documento valido!
    args[0].add_font(args[1],'',args[2],args[3])
    return 1



def pdfDocSetFont(*args):#OK
    if len(args)!=4:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocSetFont(pdfdoc,name,props,size).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].set_font(args[1],args[2],args[3])
    return 1


def pdfDocSetTextColor(*args):#OK
    if len(args)!=4:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocSetTextColor(pdfdoc,r,g,b).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].set_text_color(args[1],args[2],args[3])
    return 1


def pdfDocSetDrawColor(*args):#OK
    if len(args)!=4:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocSetDrawColor(pdfdoc,r,g,b).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].set_draw_color(args[1],args[2],args[3])
    return 1


def pdfDocSetBgColor(*args):#OK
    if len(args)!=4:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocSetBgColor(pdfdoc,r,g,b).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].set_fill_color(args[1],args[2],args[3])
    return 1


def pdfDocSetY(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocSetY(pdfdoc,y).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].set_y(args[1])
    return args[1]

def pdfDocGetY(*args):#OK
    if len(args)!=1:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocGetY(pdfdoc).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    return args[0].get_y()

def pdfDocMoveX(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocMoveX(pdfdoc,x).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].cell(args[1])
    return args[1]

def pdfDocSetLineWidth(*args):#No parece hacer nada
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocSetLineWidth(pdfdoc,width).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].set_line_width(args[1])
    return args[1]

def pdfDocLine(*args):#OK
    if len(args)!=5:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocLine(pdfdoc,x1,y1,x2,y2).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].line(args[1],args[2],args[3],args[4])
    return 1

def pdfDocRect(*args):#OK
    if len(args)!=6:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocRect(pdfdoc,x,y,w,h,style).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].rect(args[1],args[2],args[3],args[4],args[5])
    return 1


def pdfDocRotate(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocLine(pdfdoc,angle).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].rotate(args[1])
    return args[1]

def pdfDocAddSpace(*args):#OK
    if len(args)not in [1,2]:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocAddSpace(pdfdoc),_pdfDocAddSpace(pdfdoc,y).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    dy=0
    if len(args)==1:
        args[0].ln()
    else:
        args[0].ln(args[1])
        dy=args[1]
    return dy


def pdfDocGetPageNo(*args):#OK
    if len(args)!=1:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocGetPageNo(pdfdoc).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].page_no()
    return 1

def pdfDocAddPage(*args):#OK
    if len(args)not in [1,2]:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocAddPage(pdfdoc) o _pdfDocAddPage(pdfdoc,orientation).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    if len(args)==1:
        args[0].add_page()
    else:
        args[0].add_page(orientation=args[1]);
    return 1


def pdfDocAddImage(*args):#OK
    if len(args)!=6:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocAddImage(pdfdoc,imgefile,x,y,w,h).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].image(args[1],args[2],args[3],args[4],args[5]);
    return args[3] #El offset


def pdfDocBuild(*args):#OK
    if len(args)!=3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocBuild(pdfdoc,filename,local_file_or_string(FoS)).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    if args[2] not in ['F','f','S','s']:
        raise Exception('Error: el tercer argumento debe ser "F" o "S"')
    args[0].alias_nb_pages()
    args[0].output(args[1],args[2])
    return 1


def pdfDocWriteTextBox(*args):#OK
    if len(args)!=7:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocWriteTextBox(pdfdoc,w,h,text,border,align,fill).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].multi_cell(args[1],args[2],args[3],args[4],args[5],args[6])
    return 1

def pdfDocWriteHTML(*args):#OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _pdfDocWriteHTML(pdfdoc,html).
        '''
        raise Exception(msg)
    #Comprobar que es un documento valido!
    args[0].write_html(args[1])
    return 1