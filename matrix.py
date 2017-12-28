#!Python

__version__='4.0'

__date__='26/10/2011'

#import datetime

import pprint

#import minilistitem

class Matrix:

   """
      Clase que implementa la funcionalidad  de
      una matriz de MxN elementos. 
   """ 


   def __init__(self,valores=None):
     self.__matrix=[]
     self.__rows=0
     self.__cols=0
     self.__actRow=0
     self.__actCol=0
     if valores:
       #print repr(valores),isinstance(valores[0],minilistitem.MiniListItem)
       #Asegurarse de que los elementos son listas y no tuplas
       #if isinstance(valores[0],minilistitem.MiniListItem):
       #    valores=[list(el.value) for el in valores]
       #else:
       valores=[list(el) for el in valores]
       self.__matrix=valores
       self.__rows=len(valores)
       self.__cols=len(valores[0])
            

   def cols(self):
     return self.__cols

   def rows(self):
     return self.__rows

   def size(self):
      return self.__cols * self.__rows

   def getDimensions(self):
      return [self.__rows,self.__cols]

   def getRow(self,row):
      '''
      Devuelve una fila de la matriz
      '''
      if self.__matrix and row in range(self.__rows):
         return self.__matrix[row]


   def getCol(self,col):
      '''
      Devuelve una columna de la matriz
      '''
      columna=[]
      if self.__matrix and col in range(self.__cols):
         for i in range(self.__rows):
            columna.append(self.__matrix[i][col])
      return columna
   
   def getList(self):
      return self.__matrix

   def loadFromFile(self,file,sepEls='\n',sepRows='$'):
     cad=open(file,'r').read()
     #print cad
     self.loadFromString(cad,sepEls,sepRows)

   def loadFromString(self,cad,sepEls,sepRows):
     #Carga una matrix desde una cadena que tiene un formato
     #compatible con el que genera Matrix.toString()
     #Separar las filas
      filas=cad.split(sepRows)      
      for fila in filas:
         self.__matrix.append(fila.split(sepEls))
      self.__rows=len(self.__matrix)
      self.__cols=len(self.__matrix[0])


   def toString(self,sepEls="$",sepRows="\n",encode='latin1'):
     mat=""
     row=""
     if self.__rows and self.__cols:
       for i in range(self.__rows):
         for j in range(self.__cols):
           if j<self.__cols-1:
              if type(self.__matrix[i][j]) in [type(0),type(0L),type(0.0)]:
                 self.__matrix[i][j]=str(self.__matrix[i][j]).strip(' ') 
              #print type(self.__matrix[i][j])
              if 'time' in repr(type(self.__matrix[i][j])):
                 row+= str(self.__matrix[i][j]).strip(' ') + sepEls
              elif self.__matrix[i][j]==None:
                 row+='null' + sepEls
              else:
                 row+= self.__matrix[i][j] + sepEls
           else:
              if type(self.__matrix[i][j]) in [type(0),type(0L),type(0.0)]:
                 self.__matrix[i][j]=str(self.__matrix[i][j]).strip(' ')            
              row+=self.__matrix[i][j].strip(' ')
         if i < self.__rows-1:
            mat+= row + sepRows
         else:
            mat+=row
         row=""
     return mat



   def toDict(self,colnames):
      #Devolvemos un diccionario donde la clave es el nombre de la columna
      #y el valor una lista con los valores de la columna
      table={}
      if colnames==[]: #lista vacia: usar como nombres primera fila
          colnames=self.getRow(0)
          for i in range(self.__cols):
             table[colnames[i]]=self.getCol(i)[1:]         
      else: #usar colnames
          if len(colnames)!= self.__cols:
             return {}
          for i in range(self.__cols):
             table[colnames[i]]=self.getCol(i)
      return table


   def loadFromDict(self,dic):
      #1.-Comprobar que todos los elementos del diccionario son listas
      #y tienen la misma longitud
      lng=len(dic[dic.keys()[0]])
      for el in dic:
         if type(dic[el])!=type([]):
            raise Exception('Error: Todos los elementos del diccionario deben ser listas')
         if len(dic[el])!=lng:
            raise Exception('Error: Todos los elementos del diccionario deben ser listas con la misma longitud')
      #2.-La primera fila de la matrix son las claves del diccionario
      mtx=[]
      mtx.append(dic.keys())
      #3.-Recorrer los valores anyadiendo uno cada vez
      row=[]
      for i in range(lng):
          for el in dic:
              row.append(dic[el][i])
          #print 'row: %s' % row
          mtx.append(row)
          row=[]
      #print mtx
      self.__matrix=mtx
      self.__rows=len(self.__matrix)
      self.__cols=len(self.__matrix[0])      
         

   def invert(self,M=None):
      #Invierte filas y columnas
      if M==None: M=self.__matrix
      if len(M)==0: return []
      inverted=[]
      for i in range(len(M[0])):
         row=[]
         for j in range(len(M)):
            #print 'i: %d, j:%d' %(i,j)
            row.append(M[j][i])
         inverted.append(row)
      return Matrix(inverted)


   def copy(self):
      #Copia la Matrix en otra
      return Matrix(self.__matrix[:])




   def groupby(self,index1,index2):
      #1.- Obtener los elementos diferentes de filas y cols
      #2.- efectuar el recuento por el pivote
      filas=set(self.getCol(index1))
      cols=set(self.getCol(index2))
      results={}   
      for i in range(self.rows()):
         row= self.getRow(i)
         for fila in filas:
            if not results.has_key(fila): results[fila]={}
            if fila in row:
               for col in cols:
                  if not results[fila].has_key(col):
                     results[fila][col]=0               
                  if col in row:
                     results[fila][col]+=1
      return results

   def groupby2(self,index1):
      #1.- Obtener los elementos diferentes de filas y cols
      #2.- efectuar el recuento por el pivote
      cols=set(self.getCol(index1))
      #print 'cols: %s' %cols
      results={}   
      for i in range(self.rows()):
         row= self.getRow(i)
         #print row
         for col in cols:
            if not results.has_key(col):
               results[col]=0               
            if col in row:
               results[col]+=1
      return results


   def groupby3(self,master,_list,limit):
      #print 'master: %s'%master
      if (type(master)==type(0) or len(master)==0) and limit==len(_list):
         #print 'por aqui???'
         limit=0
         return
      if len(master)==0:
         #print 'entrando por =0'
         #print 'limit: %s' % limit
         #print '_list: %s' % _list
         #print 'comprobando: %s,%s' %(_list[limit],_list[-1])
         #print _list[limit]==_list[-1]
         for item in _list[limit]:
            if _list[limit]==_list[-1]:
               master[item]=0
            else:
               master[item]={}
         limit+=1
         #print 'master en caso vacio: %s' % master
      for dic in master:
         #print 'llamada recursiva'
         self.groupby3(master[dic],_list,limit)
         #limit+=1
            
      


   def appendRow(self,row):
       #Anyade una fila
       if len(self.__matrix)==0:
           self.__matrix.append(row)
       else:
           if len(row)!=len(self.__matrix[0]):
               raise Exception('Error: La longitud de la lista y el numero de columnas de la matrix deben ser iguales.')
           else:
                self.__matrix.append(row)
                self.__rows=len(self.__matrix)
                self.__cols=len(row)
           

   def insertRow(self,row,index):
       if index > len(self.__matrix):
           raise Exception('Error: El indice debe ser menor o igual al numero de filas de la matrix.')       
       #Anyade una fila en index
       if len(self.__matrix)==0:
           self.__matrix.append(row)
       else:
           if len(row)!=len(self.__matrix[0]):
               raise Exception('Error: La longitud de la lista y el numero de columnas de la matrix deben ser iguales.')
           else:
                self.__matrix.insert(index,row)
                self.__rows=len(self.__matrix)
                self.__cols=len(row)


   def appendCol(self,col):
       #Anyade una columna al final
       if len(self.__matrix)==0:
           self.__matrix.append(col)
       else:
           if len(col)!=len(self.__matrix):
               raise Exception('Error: La longitud de la lista y el numero de filas de la matrix deben ser iguales.')
           else:
               if self.__matrix:
                 for i in range(self.__rows):
                    self.__matrix[i].append(col[i])
               self.__rows=len(self.__matrix)
               self.__cols=len(self.__matrix[0])


   def insertCol(self,col,index):
       #Anyade una columna en index
       if index > len(self.__matrix[0]):
           raise Exception('Error: El indice debe ser menor o igual al numero de columnas de la matrix.')             
       if len(self.__matrix)==0:
           self.__matrix.append(col)
       else:
           if len(col)!=len(self.__matrix):
               raise Exception('Error: La longitud de la lista y la de la columna de la matrix deben ser iguales.')
           else:
               if self.__matrix:
                 for i in range(self.__rows):
                    self.__matrix[i].insert(index,col[i])
               self.__rows=len(self.__matrix)
               self.__cols=len(self.__matrix[0])


   def __contains__(self,elem):
      for el in self.__matrix:
         if elem in el:
            return 1
      return 0
   
   def __getitem__(self,fila):
      try:
       return self.__matrix[fila]
      except:
       return None


   def __iter__(self):
      return self

   def __len__(self):
      return len(self.__matrix)


   def next(self):
      if self.__actCol < self.__cols and self.__actRow < self.__rows:
         x=self.__actRow
         y=self.__actCol
         
         #Ojo con los limites
         if self.__actCol>=self.__cols-1:
            self.__actCol=0
            self.__actRow+=1
         else:
            self.__actCol+=1
         return self.__matrix[x][y]
      else:
         raise StopIteration
         
         
   

if __name__=="__main__":


   m=Matrix([['staf','3n','wound',2,2,'ex'],['staf','1n','wound',6,5,'lv'],['strep','2n','joint',6,5,'ex'],['coli','3n','joint',9,8,'ex']])
   #l=[['staf','strep','coli'],['3n' ,'2n', '1n'],['wound','joint'],[2,6,9],['ex','lv']]
   #l=[['wound','joint'],['staf','strep','coli'],['3n' ,'2n', '1n'],[2,6,9]]
   #l=[['wound','joint'],['staf','strep','coli']]
   table={}
   #m.groupby3(table,l,0)
   #pprint.pprint(table)
   print 'pivote 0-1: %s' % m.groupby(0,1)
   #print 'pivote 0: %s' % m.groupby2(2)
   #print 'pivote 0-2: %s' % m.groupby(0,2)
   #print 'pivote 1-2: %s' % m.groupby(1,2)
   #print 'pivote 2-0: %s' % m.groupby(2,0)


      
