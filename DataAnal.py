from adoV6 import *
import cStringIO
from struct import *

class DataAnal:
   """
       Envoltorio sobre el campo DataAnal de la tabla Pet en OpenData
       Este campo es una serie de estructuras en C guardadas en
       binario. La estructura es la siguiente:
       struct sInfoAna{
           long IdAna;
           long MetTrab[4]
           long SecVal
           long SecImp
           long Muestra
           long Modif //TRUE si se ha modificado
           BOOL Pet //TRUE si aparece en la peticion
           BYTE flag //Flag de estado
           BYTE Imp //Controla impresion multiple
           BOOL Fixed //Si TRUE no se analiza ni controla el flujo
           }
   """


   def __init__(self):
       #Lista con las estructuras decodificadas
       self.__analisis_bin=[]
       #Lista con tuplas (id estudio,id muestra, id localizacion)
       self.__analisis=[]
       
           
   def getMicroInfo(self,dataanal):
     #Borrar los analisis que pudieran haberse procesado en otra llamada
     #print "dataanal: %s" % dataanal
     if dataanal==None: #Si es null devolvemos una lista vacia
         return []
     self.__analisis_bin=[]
     self.__analisis=[]
     
     #Definicion de la estructura
     dataanal_def='lllllllllbbbb'
     size_ana=calcsize(dataanal_def)

     #Metemos los bytes en s
     s=cStringIO.StringIO(dataanal)
     bin2=s.getvalue()
     num_bytes=len(bin2)
     num_anas=num_bytes/size_ana
     contador=0
     inicio=0
     fin=size_ana
     for an in range(num_anas):
        self.__analisis_bin.append(unpack(dataanal_def,bin2[inicio:fin]))
        inicio=fin
        fin+=size_ana
     #Todos son analisis de micro
     for danal in self.__analisis_bin:
        estudio,muestra,loc=self.__decodeMicro(danal[0])
        self.__analisis.append((estudio,muestra,loc))
     #Y devolver los analisis procesados
     return self.__analisis
        

   def __decodeMicro(self,micro):
       '''
       La micro se codifica en resul como
       MMLLEEEE en hexa
       MM->nid de la muestra
       LL->nid de la localizacion
       EEEE->nid del estudio
       '''
       hexa=str(hex(micro))
       
       hexa=hexa[2:]
       while len(hexa)<8:
          hexa='0' + hexa
       muestra=hexa[:2]
       loc=hexa[2:4]
       estudio=hexa[4:]
       return [int(estudio,16),int(muestra,16),int(loc,16)]

  
