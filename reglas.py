#!Python

from xml.dom.minidom import *
import cStringIO
import sys

__version__='4.0'
__date__='21/09/2011'

'''
modulo para manejar reglas al estilo de PROLOG:
Hecho->propiedad(nombre|?variable).
Regla->Cabeza_de_la_regla->hecho_1,hecho_2 ,... , hecho_n.
'''

#Valores extremos de prioridad
MIN_PRIORITY=0
MAX_PRIORITY=3#90

#Predicados especiales
SPECIALS=['write','writeln','read','assert','retract','system','readoneof',
          'apply','concat','setvalue','getvalue','newlist','getlist',
          'setlist','first','rest','set','append','empty','nonempty']


def sustituir2(tabla,elem):
    '''
    Devuelve otro elemento con las sustituciones aplicadas
    '''
    salida=[]
    #print 'Tabla a sustituir: %s' % str(tabla)
    if not tabla or tabla=={}:
        return elem
    for el in elem.getElementos():
        if el in tabla.keys():
            salida.append(str(tabla[el]))
        else:
            salida.append(str(el))
        salida.append(',')
    salida=salida[:-1]
    s=[]
    s.append(elem.getNombre())
    s.append('(')
    for el in salida:
        s.append(el)
    s.append(')')
    return Elemento(''.join(s))

def sustituir(tabla,elem):
    '''
    Devuelve otro elemento con todas las sustituciones de tabla aplicadas
    (tabla es una lista de sustituciones)
    '''
    if not tabla or tabla==[]:
        return elem
    salida=elem
    for sust in tabla:
       salida= sustituir2(sust,salida)
    return salida

        
def componer(sust1,sust2,elem):
    return sustituir(sust2,sustituir(sust1,elem))


def unificar(el1,el2):
    #Ojo, considerar el caso de que coincidan los nombres
    #Ej: perro(tobi) con perro(tobi)
    sust={}
    els1=el1.getElementos()
    els2=el2.getElementos()
    #print el1.getNombre(),el2.getNombre()
    #print els1,els2
    if el1.getNombre()!=el2.getNombre():
        return None
    if len(els1)!=len(els2):
        return None
    for i in range(len(els1)):
        #print 'probando %s y %s' % (els1[i],els2[i])
        if els1[i][0]=='?' and els2[i][0]!='?':
            sust[els1[i]]=els2[i]
        elif els2[i][0]=='?' and els1[i][0]!='?':
            sust[els2[i]]=els1[i]
        elif els1[i]==els2[i] or (els1[i][0]=='?' and els2[i][0]=='?') :
            sust[els1[i]]=els2[i]
        else:
            return None
    #print str(sust)
    return sust


def unificar_b(el1,el2):
    #Ojo, considerar el caso de que coincidan los nombres
    #Ej: perro(tobi) con perro(tobi)
    sust={}
    els1=el1.getElementos()
    els2=el2.getElementos()
    #print el1.getNombre()
    #print el2.getNombre()
    if el1.getNombre()!=el2.getNombre():
        #print 'No coinciden los nombres y nos vamos!!'
        return None
    if len(els1)!=len(els2):
        return None
    for i in range(len(els1)):
        print els1[i]
        print els2[i]
        if els1[i][0]=='?' and els2[i][0]!='?':
            sust[els1[i]]=els2[i]
        elif els2[i][0]=='?' and els1[i][0]!='?':
            sust[els2[i]]=els1[i]
        elif els1[i]==els2[i] or els1[i][0]=='?' and els2[i][0]=='?' :
            sust[els1[i]]=els2[i]
        else:
            return None
    #print str(sust)
    return sust

class SyntaxException(Exception):
    pass

class Elemento:
    '''
    Elemento de una regla o hecho
    Se forma de una cadena del tipo
    <nombre(elementos)>
    Se puede saber si se ha evaluado mirando a su propiedad evaluado
    '''
    #Contador estatico para las expresiones
    #exp_counter=0
    def __init__(self,cadena,probabilidad=1):
        self.__nombre=''
        self.__elementos=[]
        self.__probabilidad=probabilidad
        self.__evaluado=0
        self.__special=0
        self.__ignorar=0
        #print 'cadena del elemento: %s' %cadena
        #print cadena[0:4]
        if cadena:
            #Si es un eval, cogemos lo que este entre parentesis tal cual
            if cadena[0:4]=='eval':
                cadena=cadena.lstrip('eval(')
                cadena=cadena[:-1]
                #print 'cadena a evaluar: %s' % cadena
                self.__nombre='eval'
                self.__elementos=[cadena]
            #Llenarla
            else:
                partes=cadena.split('(')
                #print 'partes del elemento %s: ' %str(partes)
                self.__nombre=partes[0]
                
                #marcar como especial si es preciso-----------------
                if self.__nombre in SPECIALS:
                    self.__special=1
                    #print 'predicado especial: %s!!!'%self.__nombre
                #----------------------------------------------------
                    
                self.__elementos=partes[1].strip(')').split(',')
            #Evitar que haya dos variables con el mismo nombre en un elemento
            for el in self.__elementos:
                e=self.__elementos[self.__elementos.index(el)]
                if type(e) in [type(''),type(u'')] and e[0]=='?' and self.__elementos.count(el)>1:
                    #print 'Hay un elemento repetido'
                    raise SyntaxException('Error de sintaxis. Elemento repetido: %s' %el)

    def getNombre(self):
        return self.__nombre

    def getElementos(self):
        return self.__elementos

    def getIgnorar(self):
        return self.__ignorar

    def setIgnorar(self,value):
        self.__ignorar=value

    def setSpecial(self,value):
        self.__special=value

    def isSpecial(self):
        return self.__special    

    def isEvaluado(self):
        return self.__evaluado

    def setEvaluado(self,nuevo):
        self.__evaluado=nuevo
   
    def __str__(self):
        s=[]
        s.append(self.__nombre)
        s.append('(')
        for el in self.__elementos:
            s.append(el)
            s.append(',')
        #print str(s)
        s=s[:-1]
        #print str(s)
        if not s[-1]==')':s.append(')')
        return ''.join(s)

    

class Regla:
    '''
    Clase comodin que representa tanto
    a reglas como hechos
    en un diccionario con la siguiente estructura:
    {si:[Elementos<lista_de_condiciones>],entonces:[Elemento<cabeza_de_la_regla>]}
    Los hechos tienen en la entrada si un None
    '''
    def __init__(self,id=0):
        self.__dict={}
        self.__activada=0
        self.__id=id
        self.__prioridad=MIN_PRIORITY
        self.__certeza=1
        self.__comandos=''
        self.__tema=''
        self.__explicacion=''
        self.__probabilidad=1


    def getId(self):
        return self.__id

    def setId(self,id):
        self.__id=id

    def setPrioridad(self,valor):
        if valor < MIN_PRIORITY:
            self.__prioridad=MIN_PRIORITY
        elif valor >MAX_PRIORITY:
            self.__prioridad=MAX_PRIORITY
        else:
            self.__prioridad=valor

    def getPrioridad(self):
        return self.__prioridad

    def getCerteza(self):
        return self.__certeza

    def setCerteza(self,nueva):
        self.__certeza=nueva

    def getProbabilidad(self):
        return self.__probabilidad

    def setProbabilidad(self,nueva):
        self.__probabilidad=nueva        
    
    def setTema(self,nuevo):
        self.__tema=nuevo

    def getTema(self):
        return self.__tema

    def setExplicacion(self,nueva):
        self.__expicacion=nueva

    def getExplicacion(self):
        return self.__explicacion

    def setComandos(self,comandos):
        self.__comandos=comandos

    def getComandos(self):
        return self.__comandos       

    def activar(self):
        self.__activada=1

    def desactivar(self):
        self.__activada=0

    def isActivada(self):
        return self.__activada

    def getDict(self):
        return self.__dict

    def isFact(self):
        if self.__dict['si']==None:
            return 1
        else:
            return 0

    def isRecursive(self):
        if self.isFact(): return 0
        if self.__dict['entonces'][0].getNombre() in [i.getNombre() for i in self.__dict['si']]:
            return 1
        else:
            return 0        

    def getKeys(self):
        return self.__dict.keys()

    def getValues(self):
        return self.__dict.values()

    def getItems(self):
        return self.__dict.items()

    def __getitem__(self,clave):
      try:
       return self.__dict[clave]
      except:
       return None

    def __setitem__(self,clave,valor):
        self.__dict[clave]=valor


    def toXML(self):
        #Crear XML a partir de una plantilla
        template='''<rule priority="%prior%" confidence="%confidence%" probability="%probability%">
                    <if_part>
                    <![CDATA[
                    %si%
                    ]]>
                    </if_part>
                    <then_part>
                    <![CDATA[
                    %entonces%
                    ]]>
                    </then_part>                    
                    <explanation>
                    %expl%
                    </explanation>
                    <actions>
                    %actions%
                    </actions>
                    </rule>
                    '''
        template=template.replace('%prior%',str(self.__prioridad))
        template=template.replace('%confidence%',str(self.__id))
        template=template.replace('%probability%',str(self.__probabilidad))
        #Parte si
        si=','.join([str(el) for el in self.__dict['si']])
        template=template.replace('%si%',si)
        entonces=','.join([str(el) for el in self.__dict['entonces']])
        template=template.replace('%entonces%',entonces)
        template=template.replace('%expl%',self.__explicacion)
        template=template.replace('%actions%',self.__comandos)
        return template
        
        

    def toString(self):
        out=cStringIO.StringIO()
        r=self.__dict
        #print str(r)
        out.write('\nRULE ID=%d\n' % self.__id)
        if r['si'] is not None:
           out.write('IF:\n')
           for el in r['si']:
              out.write('\t' + str(el) + '\n')
           out.write('THEN:\n')
        else:
            out.write('FACT\n')
        #out.write('ENTONCES:\n')
        for el in r['entonces']:
            out.write('\t' + str(el) + '\n')
        out.write('\n')
        s=out.getvalue()
        #print s
        return s



if __name__=='__main__':
    print 'codigo de prueba'