#!Python

__version__='2.1'

__date__='2009/04/11'

#Clase para manejar expresiones regulares
import re

default='IGNORECASE|MULTILINE|DOTALL|LOCALE'

###REVISAR COMO OBTENER LOS GRUPOS Y LAS POSICIONES DE LAS COINCIDENCIAS!!!!!!!!!

class RegExp:
  """
     Clase para manejar expresiones regulares.
     Opciones:
     DOTALL: Hace que el punto(\.) reconozca tambien \n
     IGNORECASE: No diferencia mayusculas de minusculas
     LOCALE: Hace que \w, \W, \b, y \B dependan de el LOCALE 
     MULTILINE: Hace que ^ y $ afecten a todas las lineas
     UNICODE: Hace \w, \W, \b, y \B dependientes de las propiedades Unicode 
     VERBOSE: Permite que se puedan poner comentarios en la expresion    
  """


  def __init__(self,patron,opciones=default):
    self.__patron=patron
    #Evluar opciones
    opts=['re.' + el for el in opciones.split('|')]
    #print opts
    opcs='|'.join(opts)
    #print opcs
    self.__regex=re.compile(self.__patron,eval(opcs))
    #print 'patron: %s' % self.__patron

    
  def setPatron(self,nuevo):
    self.__patron=nuevo
    #print 'patron: %s' % nuevo
    self.__regex=re.compile(self.__patron)
  
  def getPatron(self):
    return self.__patron
    
  def getMatches(self,cadena,grupo=-1):
    coincidencias=self.__regex.findall(cadena)
    #print coincidencias
    if  grupo==-1:
      return coincidencias
    else:
      try:
        return [el[grupo] for el in coincidencias if type(el)in [type([]),type(())]]
      except:
        print 'Excepcion atrapada'
        return []

  def testCadena(self,cadena,pos=-1):
    '''
    Devuelve 0 si no encuentra el patron en cadena.
    Si lo encuentra devuelve la posicion en la que
    empieza +1 (para contemplar que se encuentre al
    principio de la cadena, en posicion=0)
    '''
    if self.__regex.search(cadena):
      #Cambio con respecto a la version anterior!!!!!
      if pos > -1:
        return self.__regex.search(cadena,pos).start()+1
      else:
        return self.__regex.search(cadena).start()+1
    else:
      return 0


  def getMatchInterval(self,cadena,pos=-1):
    '''
    Devuelve una tupla con el principio y el fin
    de la coincidencia si la hay. Si no, devuelve (-1,-1)
    '''
    #print 'Valor de pos: %d' % pos
    if pos > -1:
      m=self.__regex.search(cadena,pos)
      if m==None: return (-1,-1)
      return (m.start(0),m.end(0))
    else:
      m=self.__regex.search(cadena)
      if m==None: return (-1,-1)
      return (m.start(0),m.end(0))
    

  def testFile(self,archivo):
    s=self.__archToString(archivo)
    return testCadena(s)

  def getSingleMatches(self,cadena):
    coincidencias=self.regex.findall(cadena)
    res=[]
    for x in coincidencias:
      if not x in res:
        res.append(x)
    return res
    
  def getFileMatches(self,archivo,grupos=-1):
    s=self.__archToString(archivo)
    return self.getMatches(s,grupos)

  def getFileSingleMatches(self,archivo):
    s=self.__archToString(archivo)
    return self.getSingleMatches(s)

  def replace(self,cadena,nuevo):
    return self.__regex.sub(nuevo,cadena)

  def replaceInFile(self,archivo,nuevo):
    s=self.__archToString(archivo)
    return self.replace(s,nuevo)

  def split(self,cadena):
    return self.__regex.split(cadena)

  def splitFile(self,archivo):
    s=self.__archToString(archivo)
    return self.split(s)

  def batchMatch(self,cadena, patrones):
    results=[]
    for pat in patrones:
      self.setPatron(pat)
      results.append(self.getMatches(pat))
    return results

  def batchMatchInFile(self,archivo,patrones):
    s=self.__archToString(archivo)
    return batchMatch(s,nuevos)
  
  def batchReplace(self,cadena,patrones,nuevos):
    for pat in range(len(patrones)):
      self.setPatron(patrones[pat])
      resul=self.replace(cadena,nuevos[pat])
      cadena=resul
    return resul     

  def batchReplaceInFile(self,archivo,patrones,nuevos):
    s=self.__archToString(archivo)
    return batchReplace(s,nuevos)
  
  def __archToString(self,arch):   
    return open(arch,'r').read()



class RegExpCallback:

  """
     Clase para manejar expresiones regulares
     que llama a funciones de callback registradas
     cuando encuentra coincidencias
  """


  def __init__(self,opciones=default):
    self.__callback={}
    self.__regx=RegExp('[0-9]+')

  def setCallback(self,patron,callback,args):
    funcion=[callback,args]
    self.__callback[patron]=funcion

  def getMatches(self,cadena):
    resultados=[]
    for patron in self.__callback.keys():
      self.__regx.setPatron(patron)
      resul=self.__regx.getMatches(cadena)
      #Llamar a la funcion de callback si existe
      for item in resul:
        self.__callback[patron][0](self.__callback[patron][1])
      resultados.append(resul)
    return resultados

    
  def __archToString(self,arch):   
    return open(arch,'r').read()   


  def getFileMatches(self,archivo):
    resultados=[]
    cadena=self.__archToString(archivo)
    for patron in self.__callback.keys():
      self.__regx.setPatron(patron)
      resul=self.__regx.getMatches(cadena)
      #Llamar a la funcion de callback si existe
      for item in resul:
        self.__callback[patron][0](self.__callback[patron][1])
      resultados.append(resul)
    return resultados


  def toString(self):
    return str(self.__callback)


class KeyWords:
  """
  Clase que busca sinonimos para
  una expresion regular
  """
  def __init__(self,dict={}):
    if dict!={}:
      self.__keywords=dict
    else:
      self.__keywords={}
    self.__re=RegExp('',opciones=default)


  def addKeyWord(self,clave,sinonimos):
    self.__keywords[clave]=sinonimos

  def getKeyWords(self):
    return self.__keywords

  def findKeyWords(self,cadena):
    resul=[]
    #Para cada sinonimo de la clave
    for clave in self.__keywords.keys():
      for item in self.__keywords[clave]:
        self.__re.setPatron(item)
        for elem in self.__re.getMatches(cadena):
          if clave not in resul:
            resul.append(clave)
            break
    return resul

  def __archToString(self,arch):   
    return open(arch,'r').read()

  def findKeyWordsInFile(self,archivo):
    cad=self.__archToString(archivo)
    return self.findKeyWords(cad)



if __name__=='__main__':
  r=RegExp('oop')
  print "\n\nIniciando busqueda\n\n"
  r.setPatron("(</)p(ar)a>")
  print r.getFileMatches('c:/pdf.txt',1)




  