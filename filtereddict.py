#!Python

import re
from fnmatch import *
import os.path

'''
Implementar:
-Operador +:adiciona todas las columnas de otra tabla siempre y cuando
coincidan los nombres
-Cargar desde un archivo CSV o similar (nombres en primera columna)
'''

class NotEqualLengthException(Exception):
    pass

class FilteredTable(object):
    '''
    Clase que implementa una tabla con nombres de columnas
    y puede filtrar por los valores de sus celdas.
    Restriccion: todas las columnas deben tener la misma longitud.
    Si no es asi, se lanza una excepcion.
    '''
    def __init__(self,table):
        self.__table={}
        self.__result={}
        self.__names=[]
        if type(table)==dict:
            self.__table=table
            self.__names=self.__table.keys()
            #Buffer para filtrado multiple
            self.__result=self.__table
        elif os.path.isfile(table): #Cargar desde el archivo
            lineas=[line.strip() for line in open(table,'r').readlines() if line[0] and line[0] not in['#',' ','\n']]
            #print lineas
            #Nombres de columnas
            self.__names=lineas[0].split('|')
            print self.__names
            #Datos
            #Crear la entrada en la tabla
            for item in self.__names:
                self.__table[item]=[]
            #E ir metiendo los datos
            for item in lineas[1:]:
                partes=item.split('|')
                for i in range(len(partes)):
                    print self.__names[i],partes[i]
                    self.__table[self.__names[i]].append(partes[i].strip())
            print self.__table
            self.__result=self.__table
        #Contador para iterar filas
        self.__counter=0


    def getCol(self,name):
        if self.__table.has_key(name):
            return self.__table[name]
        else:
            return None

    def getColNames(self):
        return self.__names

    def getTable(self):
        return self.__table

    def setTable(self,newTable):
        pass

    def filter(self,col,op,args):
        #Genera una vista filtrada de los datos
        #op: operador
        #args: debe ser una lista con los argumentos
        filtrado={}
        #Si el operador no es valido, devolvemos la tabla vacia
        if op not in ['=','>','>=','<','<=','not','in','not_in','between','not_between','like','regexp']: return filtrado
        if self.__table:
            #Si es un nombre de columna valido,
            #metemos en filtrado todas las filas para las que se
            #cumpla cond en la columna pedida
            if self.__table.has_key(col):
                #Aproximacion naive (tiene que haber algo mejor):
                #1.-Crear una replica vacia de self.__table
                for name in self.__names:
                    filtrado[name]=[]
                #2.-Recorrer la columna filtrada y ver si se cumple cond
                #Si se cumple,ponemos toda la fila en filtrado
                for i in range(len(self.__result[col])):
                    #Proceder segun operador:
                    if op=='=' and self.__result[col][i]==args[0]:
                        for name in self.__names:
                            filtrado[name].append(self.__result[name][i])
                    elif op=='>' and self.__result[col][i]>args[0]:
                        for name in self.__names:
                            filtrado[name].append(self.__result[name][i])
                    elif op=='>=' and self.__result[col][i]>=args[0]:
                        for name in self.__names:
                            filtrado[name].append(self.__result[name][i])
                    elif op=='<' and self.__result[col][i]<args[0]:
                        for name in self.__names:
                            filtrado[name].append(self.__result[name][i])
                    elif op=='<=' and self.__result[col][i]<=args[0]:
                        for name in self.__names:
                            filtrado[name].append(self.__result[name][i])
                    elif op=='not' and self.__result[col][i]!=args[0]:
                        for name in self.__names:
                            filtrado[name].append(self.__result[name][i])
                    elif op=='in' and self.__result[col][i] in args:
                        for name in self.__names:
                            filtrado[name].append(self.__result[name][i])
                    elif op=='not_in' and self.__result[col][i] not in args:
                        for name in self.__names:
                            filtrado[name].append(self.__result[name][i])
                    elif op=='between' and self.__result[col][i]>=args[0] and self.__result[col][i]<=args[1]:
                        for name in self.__names:
                            filtrado[name].append(self.__result[name][i])
                    elif op=='not_between' and (self.__result[col][i]<args[0] or self.__result[col][i]>args[1]):
                        for name in self.__names:
                            filtrado[name].append(self.__result[name][i])
                    elif op=='like' or op=='regexp':
                        #print 'patron: %s' % args[0]
                        regex=re.compile(args[0], re.IGNORECASE | re.LOCALE | re.DOTALL)
                        #print 'probando: ' + self.__result[col][i]
                        if  regex.match(self.__result[col][i]):
                            #print 'Coincidencia encontrada!!'
                            for name in self.__names:
                                filtrado[name].append(self.__result[name][i])                                
        return filtrado

    def multiFilter(self,conditions):
        '''
        Permite filtros sucesivos.
        Conditions es una lista de tuplas (col,op,args)
        '''
        for cond in conditions:
            #print 'cond: %s' %str(cond)
            self.__result=self.filter(cond[0],cond[1],cond[2])
            #print 'temp: %s' % self.__result
        return self.__result


    def toMatrix(self,firstnames=1):
        mtx=[]
        row=[]
        if firstnames:
            mtx.append(self.__table.keys())
        collen=len(self.__table.keys())
        print collen
        contador=0
        while(contador<collen):
            print contador
            for name in self.__table.keys():
                row.append(self.__table[name][contador])
            mtx.append(row)
            row=[]
            contador+=1
        return mtx

    def filterToMatrix(self,firstnames=1):
        mtx=[]
        row=[]
        if firstnames:
            mtx.append(self.__table.keys())
        collen=len(self.__result[self.__names[0]])
        contador=0
        while(contador<collen):
            for name in self.__table.keys():
                row.append(self.__result[name][contador])
            mtx.append(row)
            row=[]
            contador+=1
        return mtx        

    def toTable(self,firstnames=1):
        mtx=self.toMatrix(firstnames)
        table={}
        if mtx:
            rows=len(mtx)
            print rows
            cols=len(mtx[0])
            print cols
            for i in range(rows):
                for j in range(cols):
                    table[(i,j)]=mtx[i][j]
        return table


    def filterToTable(self,firstnames=1):
        mtx=self.filterToMatrix(firstnames)
        table={}
        if mtx:
            rows=len(mtx)
            print rows
            cols=len(mtx[0])
            print cols
            for i in range(rows):
                for j in range(cols):
                    table[(i,j)]=mtx[i][j]
        return table


    def __len__(self):
        try:
            return len(self.__table[self.__names[0]])
        except:
            return 0
    
    def __getitem__(self,index):
        item={}
        if self.__table and index<=len(self.__table[self.__names[0]]):
            for name in self.__names:
                item[name]=(self.__table[name][self.__counter])
        return item

       
    def __setitem__(self,value):
        pass            

    def __iter__(self):
      return self


    def next(self):
      if self.__table and self.__counter <len(self.__table[self.__names[0]]):
         item={}

         for name in self.__names:
            item[name]=(self.__table[name][self.__counter])

         self.__counter+=1
         return item         

      else:
         raise StopIteration        




if __name__=='__main__':
    print 'codigo de prueba'
    datos={
        'id':[1,2,3,4,5,6,7,8,9],
        'nota':[4,6,7,7,8,5,6,7,2],
        'sexo':['m','h','h','h','h','m','m','m','m'],
        'misc':['mime','her','hwer','hfg','hvc','ertm','qwm','xcxcm','45tm']
        }
    filt=FilteredTable(datos)
    #filt=FilteredTable('antib.txt')
    print filt.getColNames()
    filtrado=filt.multiFilter([('misc','like','h*'),('nota','=',[7])]) 
    #filt2=FilteredTable(filtrado)
    print 'resultado:%s' % filtrado
    #print filt[3]
    print filt.filterToMatrix()
    #print filt.toTable()
    #print filt.filterToMatrix(0)

    