#!Python
from xml.dom.minidom import *
import cStringIO
from reglas import *
from RegExp import *
import sys
import cPickle

__version__='4.0'
__date__='26/10/2011'


#Funciones de utilidad para generar reglas dinamicamente---------------------------
def removeWhitespace(cadena):
    #Hay que respetar los espacios cuando es una frase entre comillas simples
    blancos=[' ','\t','\r'] #\n
    salida=[]
    COMILLAS=0
    #print type(cadena)
    for i in range(len(cadena)):
        if cadena[i]=="'":
            COMILLAS= not COMILLAS
            #print 'negando COMILLAS'
        if cadena[i] not in blancos:
            salida.append(cadena[i])
        elif cadena[i] in blancos and COMILLAS:
            salida.append(cadena[i])
    #print 'salida:' + ''.join(salida)
    return ''.join(salida)



def loadElements(cadena):
    partes=cadena.split('),')
    #print 'En loadElements partes %s:' % partes
    salida=[]
    if len(partes)>1:
        for parte in partes:
            #Comprobar que los parentesis estan balanceados
            temp=list(parte)
            if temp.count('(')!= temp.count(')'):
                parte+=')'
            #print 'Llamando a elemento con %s' % parte
            salida.append(Elemento(parte))
    else:
        #print 'solo hay una parte: %s' %repr(cadena)
        if cadena=='':
            return None
        else:
            salida.append(Elemento(cadena))
    return salida
#----------------------------------------------------------------------------------

class BaseConocimiento:
    '''
    Clase que carga, descarga y almacena hechos y reglas
    Las reglas se cargan desde un archivo. Estan escritas en formato xml o bien
    se han serializado a partir de otra base de conocimiento.
    '''
    def __init__(self,archivo=None):
        self.__reglas=[]
        self.__temas=[]
        self.__contador=1
        if archivo:
            #Diferenciar si el archivo es xml o no (texto libre)
            if archivo.split('.')[-1].lower()=='xml':
                self.cargaReglas(archivo)
            elif archivo.split('.')[-1].lower()=='rules':
                self.__deserialize(archivo)



    def cargaReglas(self,archivo):
        
        #print 'reglas cargadas'
        #Cargar las reglas desde el xml
        doc=parse(archivo)
        doc.normalize()
        temas=doc.getElementsByTagName("module")
        #Guardar los temas de las reglas cargadas
        contador=self.__contador
        for t in temas:
            self.__temas.append(t.getAttribute("name").encode("ascii","replace"))
            #Instanciar y cargar las reglas
            for r in t.getElementsByTagName("rule"):
                rgl=Regla()
                rgl.setId(contador)
                contador+=1
                rgl.setPrioridad(int(r.getAttribute("priority").encode("ascii","replace")))
                rgl.setPrioridad(int(r.getAttribute("confidence").encode("ascii","replace")))
                rgl.setTema(t.getAttribute("name").encode("ascii","replace"))
                #Coger la cabeza
                entonces=r.getElementsByTagName("then_part")[0].firstChild.toxml().encode("ascii","replace").strip()
                #Coger los comandos
                rr=r.getElementsByTagName("actions")[0]
                rr.normalize()
                coms=rr.firstChild.nodeValue.encode("ascii","replace").strip()
                rgl.setComandos(coms)                
                rgl.setExplicacion(r.getElementsByTagName("explanation")[0].firstChild.toxml().encode("ascii","replace").strip())                
                #Coger los elementos
                nn=r.getElementsByTagName("if_part")[0]
                nn.normalize()
                '''
                for el in nn:
                    print el.nodeValue
                '''
                xml=nn.toxml().encode("ascii","replace").strip()
                #Cambio para que funcionen los retornos de linea
                xml=xml.replace('\\n','\n')
                #----------------------------------------------------------------------------
                #diferenciar los CDATA del resto
                #print 'xml: %s' %xml
                #print type(xml)
                start=xml.find('<![CDATA[')
                #print 'start: %d' %start
                if start!=-1: #Es un CDATA (ojo, cogemos solo el primer CDATA del nodo)
                    end=xml.find(']]>')
                    els=xml[start+len('<![CDATA['):end].strip()
                    #print 'els en CDATA:%s' %els
                else:
                    els=nn.firstChild.nodeValue.encode("ascii","replace").strip() #.split(",")
                #----------------------------------------------------------------------------
                #print 'Elementos en basecon:%s' % els
                #Poner las partes de la regla
                rgl['si']=self.loadElements(self.removeWhitespace(els))
                rgl['entonces']=self.loadElements(self.removeWhitespace(entonces))
                #Meterla en la base de conocimiento
                self.addRegla(rgl)
            self.__contador=contador #Por si se anyaden reglas con addRules
                

    def getReglas(self):
        return self.__reglas


    def addRegla(self,regla):
        #Ajustar ids a los de esta basecon
        regla.setId(self.__contador)
        self.__contador+=1
        #Si el tema de la regla no esta en esta basecon, anyadirlo
        if regla.getTema() not in self.__temas:
            self.__temas.append(regla.getTema())
        #Y meter la regla en la basecon
        self.__reglas.append(regla)


    def delRegla(self,regla):
        if regla in self.__reglas:
            del self.__reglas[self.__reglas.index(regla)]

    def resetReglas(self):
        for regla in self.__reglas:
            regla.desactivar()

    def getModulos(self):
        return self.__temas

    def save(self,arch):
        self.__serialize(arch)

    def __serialize(self,arch):
        #Guardar temas, reglas y contador
        stream=None
        if arch.split('.')[-1].lower()=='rules':
            stream=open(arch,'wb')
        else:
            stream=open(arch + '.rules','wb')
        cPickle.dump(self.__temas,stream)
        cPickle.dump(self.__reglas,stream)
        cPickle.dump(self.__contador,stream)
        stream.close()

    def __deserialize(self,arch):
        #Cargar temas, reglas y contador y resetear reglas.
        stream=open(arch,'rb')
        self.__temas=cPickle.load(stream)
        self.__reglas=cPickle.load(stream)
        self.__contador=cPickle.load(stream)
        self.resetReglas()
        

    def __archToString(self,archivo):
        return open(archivo,'r').read().strip().strip('\n')

    def removeWhitespace(self,cadena):
        #Hay que respetar los espacios cuando es una frase entre comillas simples
        blancos=[' ','\t','\r'] #\n
        salida=[]
        COMILLAS=0
        #print type(cadena)
        for i in range(len(cadena)):
            if cadena[i]=="'":
                COMILLAS= not COMILLAS
                #print 'negando COMILLAS'
            if cadena[i] not in blancos:
                salida.append(cadena[i])
            elif cadena[i] in blancos and COMILLAS:
                salida.append(cadena[i])
        #print 'salida:' + ''.join(salida)
        return ''.join(salida)
        

    def loadElements(self,cadena):
        partes=cadena.split('),')
        #print 'En loadElements partes %s:' % partes
        salida=[]
        if len(partes)>1:
            for parte in partes:
                #Comprobar que los parentesis estan balanceados
                temp=list(parte)
                if temp.count('(')!= temp.count(')'):
                    parte+=')'
                #print 'Llamando a elemento con %s' % parte
                salida.append(Elemento(parte))
        else:
            #print 'solo hay una parte: %s' %repr(cadena)
            if cadena=='':
                return None
            else:
                salida.append(Elemento(cadena))
        return salida
    

    def toString(self):
        out=''
        for r in self.__reglas:
            out+=r.toString()
        return out

    def toXML(self,archivo='None'):    
        out=''
        for r in self.__reglas:
            out+=r.toXML()
        if archivo:
            f=open(archivo,'w')
            f.write(out)
            f.close()
        return out

if __name__=='__main__':
    print 'codigo de prueba de basecon'
    #bc=BaseConocimiento('reglas_hepatitis.xml')
    #bc=BaseConocimiento('test.xml')
    #bc=BaseConocimiento('ESTAFILOS.txt')
    bc=BaseConocimiento('basecon_expert.txt')    
    print bc.toString()
    print bc.getModulos()
    print bc.toXML()
