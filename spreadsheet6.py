#!Python

import math

'''
Cambios:
-Se debe permitir cambiar el nombre de las filas
(algo como rename(old,new)) pero hay que mantener una tabla con los cambios de nombre(??)
para que funcionen las funciones de suma, media, etc.
'''

#Funciones de utilidad para generar nombres de columnas
#y descomponer una cadena letras-digitos en sus partes
def genColNames(numero):
    una=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    dos=[a+b for a in una for b in una]
    tres=[a+b+c for a in una for b in una for c in una]
    todos=una + dos + tres
    return todos[:numero]

def getColRow(nombre):
    numbers='0123456789'
    fila=''
    col=''
    for c in nombre:
        if c in numbers:
            fila+=c
        else:
            col+=c
    return [col,fila]


class SpreadSheet:
    '''
    Modificada de una receta de Raymond Hettinger
    en ASPN Python Cookbook.
    '''
    def __init__(self,rows,cols,init_value=0,funcs={}):
        self.__rows=rows
        self.__cols=cols
        self.__cells={}
        self.__namespace={}
        self.__funcs=funcs
        #Valor inicial de las celdas
        self.__init_value=str(init_value)
        #Tabla para nombres de celda, filas y columnas definidos por el usuario
        self.__alias={}
        self.__row_alias={}
        self.__col_alias={}
        #Nombres de las columnas
        self.__colNames=genColNames(self.__rows)
        #print self.__colNames
        #Crear las celdas e inicializarlas
        for name in self.__colNames:
            for i in range(cols):
                self.__cells[name + str(i)]=self.__init_value
                self.__namespace[name + str(i)]=self.__cells[name + str(i)]
        

    def getFormula(self,key):
        return self.__cells[key]
    
    def getNumRows(self):return self.__rows
    
    def getNumCols(self): return self.__cols

    def getNamespace(self):return self.__namespace

    def getCells(self): return self.__cells    

    def toMatrix(self,start='',end=''):
        if not start: start=self.__colNames[0] + '0'
        if not end: end=self.__colNames[-1] + str(len(self.__colNames)-1)
        #print '(%s,%s)' %(start,end)
        mtx=[]
        row=[]
        rng=self.getRange(start,end)[0] #Valores
        col0,row0=getColRow(start)
        col1,row1=getColRow(end)
        rowstart=int(row0)
        rowend=int(row1)
        rowlen=rowend-rowstart+1
        #print 'rowlen: %s' % rowlen
        #Rowlen no puede ser negativo
        if rowlen<=0: return None
        for elem in rng:
            row.append(elem)
            #print row
            if len(row)==rowlen:
                mtx.append(row)
                row=[]
        return mtx
    

    def getRange(self,begin,end,astable=0):
        values=[]
        names=[]
        table={}
        col0,row0=getColRow(begin)
        col1,row1=getColRow(end)
        colstart=self.__colNames.index(col0)
        colend=self.__colNames.index(col1)
        if astable:
            cls=self.__colNames[colstart:colend+1]
            for i in cls:
                for j in range(int(row0),int(row1)+1):
                    table[(cls.index(i),j)]=self.__getitem__(i + str(j))
            return table
        else:
            for i in self.__colNames[colstart:colend+1]:
                for j in range(int(row0),int(row1)+1):
                    values.append(self.__namespace[i + str(j)])
                    names.append(i + str(j))
            #return (values,names)
            return (names,values)       


    def setAlias(self,actual,nuevo):
        if nuevo and self.__cells.has_key(actual):
            self.__alias[nuevo]=actual


    def getAlias(self,nuevo):
        if self.__alias.has_key(nuevo):
            return self.__alias[nuevo]
        else:
            return None

    def __setitem__(self,key,formula):
        #print 'en setitem con (%s,%s)' %(key,formula)
        self.__cells[key]=formula
        self.__namespace[key]=self.__init_value
        #print type(self.__namespace[key])

    def __getitem__(self,key):
        '''
        Tipo de evaluacion:
        -Si no hay prefijos especiales, se evalua tal cual
        -Sumatorio: _sum(a1:an) donde a1:an es un rango de celdas.
        Asume que las columnas van de la a a la z y las filas de 1 a n
        Pendiente de resolver: Control de errores cuando una de las celdas
        contiene una formula.
        '''
        #print 'Dentro de getitem con key: %s' % key
        try:
            if self.__cells[key][0]=='_': #Es una funcion
                #print 'Es una funcion'
                #Asumimos que es _sum, pero el proceso es generalizable
                #------------------------------------------------------
                #rango=self.__cells[key].strip('_sum(').strip(')')
                fname=self.__cells[key][:self.__cells[key].index('(')]
                #print 'fname: %s' % fname
                rango=self.__cells[key].strip(')')
                rango=rango[rango.index('(')+1:]
                #print 'RANGO:%s' %rango
                partes=rango.split(':')
                #print partes
                colname=partes[0][0]
                #print colname
                #1.- Obtener el rango de celdas con el que queremos trabajar
                rng=self.getRange(partes[0],partes[1])[0] #[1]
                #print 'rango: %s' % rng
                #2.- Aplicar la funcion que se quiera a cada uno de los elementos del rango
                contador=0
                for name in rng:
                    contador+=1
                    #print 'name: %s' %name
                    self.__namespace[name]=eval(self.__cells[name],self.__namespace,self.__funcs)
                    if rng.index(name)!=0 and fname=='_sum':
                        self.__namespace[key]=str(float(self.__namespace[key]) + float(self.__namespace[name]))
                    elif rng.index(name)!=0 and fname=='_prod':
                        self.__namespace[key]=str(float(self.__namespace[key]) * self.__namespace[name])
                    elif rng.index(name)!=0 and fname=='_sum2':
                        self.__namespace[key]=str(float(self.__namespace[key]) + self.__namespace[name]**2)
                    elif rng.index(name)!=0 and fname=='_prod2':
                        self.__namespace[key]=str(float(self.__namespace[key]) * self.__namespace[name]**2)
                    elif rng.index(name)!=0 and fname=='_count':
                        self.__namespace[key]=str(contador)
                    else: #seguir si no se conoce la funcion
                        continue
                #-------------------------------------------------------------------------
                
                return self.__namespace[key]
            else: #No es una funcion. Evaluamos como una cadena
                #Ojo!!!: Considerar que lo que hay no sea algo evaluable(una cadena) y entonces no evaluar
                try:
                    #print repr(self.__cells[key])
                    #print eval(self.__cells[key],self.__namespace,self.__funcs)
                    self.__namespace[key]=eval(self.__cells[key],self.__namespace,self.__funcs)
                except:
                    print 'Error al evaluar!!'
                    pass
                return self.__namespace[key]
        
        except Exception,e:
            print 'Ocurrio una excepcion durante la evaluacion: %s' %str(e)
            return None



if __name__=='__main__':
    funciones={'pi':math.pi,'sin':math.sin,'cos':math.cos} #Incluir todo el modulo math
    print 'Codigo de prueba'
    xls=SpreadSheet(100,100,50,funciones)
    print str(xls['a9'])
    #print xls.getCells()
    xls['c1']='_count(a0:a9)'
    xls['c2']='a0 + a1 + cos(a2)'
    xls['c3']='(a0**2 + a1) * 0.25'    
    print xls['c1']
    print xls['c2']
    print xls['c3']    
    print xls.getRange('a1','c9')
    print xls.toMatrix('a1','c9')
    print xls.getRange('a1','c9',0)
    
