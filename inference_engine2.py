#!Python
from reglas import *
from basecon import *
if not 'minimal_py' in sys.modules:
     minimal_py=__import__('minimal_py')
else:
     minimal_py=sys.modules['minimal_py']
from pila import *
import sys
import os

__version__='8.0'
__date__='09/09/2013'

#Palabras reservadas que se interpretan como comandos
reserved=['eval']

#Espacio de nombres global
EXP_NAMESPACE={} #{'test':0,'test2':10}

#Query global
QUERY=''

#Cambiar esto para permitir que no se pongan los (?x)!!
def preparar(query):
    #print 'query en preparar:%s' % query
    partes=query.split('),')#Esto falla si solo hay un elemento!!!
    salida=[]
    if len(partes)>1:
        for parte in partes:
            if parte[-1]!=')':
                parte+=')'
            salida.append(Elemento(parte))
    else:
        salida.append(Elemento(query))
    #print 'query preparada: %s' % str([el.getNombre() for el in salida])
    return salida

def isString(el):
    return type(el) in [type(''),type(u'')]

def isNumber(n):
    for i in n:
        if not i in '0123456789':
            return 0
    return 1


def findElInSust(el,sust):
    if not el in sust:
        raise Exception('Error: la variable "%s" no esta definida'%el)
    else:
        return sust[el]


def solveSpecialPred(el,s):
    retvalue=1
    #print 'VALOR DE S AQUI: %s' %s
    if el.getNombre()=='write':
        #print 'EN WRITE'
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
            p=findElInSust(el.getElementos()[0],s)
        sys.stdout.write(str(p).strip('"'))
        sys.stdout.flush()
        
    elif el.getNombre()=='writeln':
        p=el.getElementos()[0]
        #print 'EN WRITELN',el.getElementos()[0],[i for i in el.getElementos()]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
            p=findElInSust(el.getElementos()[0],s)
        print str(p).strip('"')
        
    elif el.getNombre()=='system':
        #print 'EN SYSTEM'
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
            p=findElInSust(el.getElementos()[0],s)
        os.system(p)
        
    elif el.getNombre()=='read':
        #print 'EN READ'
        if len(el.getElementos())!=2:
            raise Exception('Error: El predicado especial "read" debe tener 2 argumentos')
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]!='?':
            raise Exception('Error: solo se pueden leer variables')
        else:
            s[el.getElementos()[1]]=raw_input(p.strip('"'))
            #print 's tras leer: %s' % s

    elif el.getNombre()=='readoneof': #askoneof(text,list_of_options,var)
        #print 'EN ASKONEOF'
        if len(el.getElementos())!=3:
            raise Exception('Error: El predicado especial "readoneof" debe tener 3 argumentos')
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)
        l=el.getElementos()[1]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           l=findElInSust(el.getElementos()[1],s)
        if type(l)!=type([]):
            if not l.strip('"') in EXP_NAMESPACE:
                raise('Error: "%s" no es una lista y tiene que serlo'%l)
        if isString(el.getElementos()[2]) and el.getElementos()[2][0]!='?':
            raise Exception('Error: solo se pueden leer variables')
        else:
            while 1:
                s[el.getElementos()[2]]=raw_input(p.strip('"'))
                if s[el.getElementos()[2]] in l:
                    break
                print '"%s" no es un valor aceptable. Debe ser uno de "%s"'%(s[el.getElementos()[2]],l)
            
    elif el.getNombre()=='assert': #PTE. IMPLEMENTAR
        #print 'EN ASSERT'
        if len(el.getElementos())!=2:
            raise Exception('Error: El predicado especial "assert" debe tener 2 argumentos')
        #
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           el.getElementos()[0]=findElInSust(el.getElementos()[0],s)
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]=='?':
            el.getElementos()[1]=findElInSust(el.getElementos()[1],s)
        #Crear la nueva regla
        parts=el.getElementos()[0].split('===>>')
        print parts

    elif el.getNombre()=='retract': #PTE. IMPLEMENTAR
        #print 'EN ASSERT'
        if len(el.getElementos())!=2:
            raise Exception('Error: El predicado especial "assert" debe tener 2 argumentos')
        #
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           el.getElementos()[0]=findElInSust(el.getElementos()[0],s)
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]=='?':
            el.getElementos()[1]=findElInSust(el.getElementos()[1],s)
        #Crear la nueva regla
        parts=el.getElementos()[0].split('===>>')
        print parts        

    elif el.getNombre()=='concat': #????
        #print 'EN CONCAT'
        if len(el.getElementos())!=3:
            raise Exception('Error: El predicado especial "concat" debe tener 3 argumentos')
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)
        q=el.getElementos()[1]
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]=='?':
            q=findElInSust(el.getElementos()[1],s)
        if isString(el.getElementos()[2]) and el.getElementos()[2][0]!='?':
            raise Exception('Error: el tercer argumento de concat debe ser una variable')            
        s[el.getElementos()[2]]= str(p) + str(q)

    elif el.getNombre()=='setvalue': #
        #print 'EN SETVALUE'
        if len(el.getElementos())!=2:
            raise Exception('Error: El predicado especial "setvalue" debe tener 2 argumentos')
        p=el.getElementos()[0]
        p1=el.getElementos()[1]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]=='?':
            p1=findElInSust(el.getElementos()[1],s)           
        EXP_NAMESPACE[p.strip('"')]=str(p1)
        #print EXP_NAMESPACE

    elif el.getNombre()=='newlist': #
        #print 'EN NEWLIST'
        if len(el.getElementos())!=1:
            raise Exception('Error: El predicado especial "newlist" debe tener 1 argumento')
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)          
        EXP_NAMESPACE[p.strip('"')]=[]

    elif el.getNombre()=='empty': #
        #print 'EN EMPTY'
        if len(el.getElementos())!=1:
            raise Exception('Error: El predicado especial "empty" debe tener 1 argumento')
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)          
        if EXP_NAMESPACE[p.strip('"')]==[]:
            retvalue=1
        else:
            retvalue=0

    elif el.getNombre()=='nonempty': #
        #print 'EN NONEMPTY'
        if len(el.getElementos())!=1:
            raise Exception('Error: El predicado especial "nonempty" debe tener 1 argumento')
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)          
        if EXP_NAMESPACE[p.strip('"')]==[]:
            retvalue=0
        else:
            retvalue=1
        #print 'retvalue aqui: %s' % retvalue
        

    elif el.getNombre()=='getlist': #
        #print 'EN GETLIST'
        if len(el.getElementos())!=2:
            raise Exception('Error: El predicado especial "getlist" debe tener 2 argumentos')
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)
        if not isString(el.getElementos()[1]):
            raise Exception('Error: el segundo argumento de first debe ser una variable')            
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]!='?':
            raise Exception('Error: el segundo argumento de first debe ser una variable')
        if not p.strip('"') in EXP_NAMESPACE:
            raise Exception('Error: La lista "%s" no esta definida'%p.strip('"'))
        if EXP_NAMESPACE[p.strip('"')]==[]:
            s[el.getElementos()[1]]=[]
        else:
            s[el.getElementos()[1]]=EXP_NAMESPACE[p.strip('"')]


    elif el.getNombre()=='setlist': #
        #print 'EN SETLIST'
        if len(el.getElementos())!=2:
            raise Exception('Error: El predicado especial "setlist" debe tener 2 argumentos')
        p=el.getElementos()[0]
        p1=el.getElementos()[1]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]=='?':
            p1=findElInSust(el.getElementos()[1],s)              
        if not p.strip('"') in EXP_NAMESPACE:
            raise Exception('Error: La lista "%s" no esta definida'%p.strip('"'))
        EXP_NAMESPACE[p.strip('"')]=p1            
        

    elif el.getNombre()=='append': #
        #print 'EN APPEND'
        if len(el.getElementos())!=2:
            raise Exception('Error: El predicado especial "append" debe tener 2 argumentos')
        p=el.getElementos()[0]
        p1=el.getElementos()[1]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]=='?':
            p1=findElInSust(el.getElementos()[1],s)              
        if not p.strip('"') in EXP_NAMESPACE:
            raise Exception('Error: La lista "%s" no esta definida'%p.strip('"'))
        EXP_NAMESPACE[p.strip('"')].append(p1)
        #print EXP_NAMESPACE
        

    elif el.getNombre()=='first': #
        #print 'EN FIRST'
        if len(el.getElementos())!=2:
            raise Exception('Error: El predicado especial "first" debe tener 2 argumentos')
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)
        if not isString(el.getElementos()[1]):
            raise Exception('Error: el segundo argumento de first debe ser una variable')            
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]!='?':
            raise Exception('Error: el segundo argumento de first debe ser una variable')
        if not p.strip('"') in EXP_NAMESPACE:
            raise Exception('Error: La lista "%s" no esta definida'%p.strip('"'))
        if EXP_NAMESPACE[p.strip('"')]==[]:
            s[el.getElementos()[1]]=[]
        else:
            s[el.getElementos()[1]]=EXP_NAMESPACE[p.strip('"')][0]

    elif el.getNombre()=='rest': #
        #print 'EN REST'
        if len(el.getElementos())!=2:
            raise Exception('Error: El predicado especial "rest" debe tener 2 argumentos')
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)
        if not isString(el.getElementos()[1]):
            raise Exception('Error: el segundo argumento de rest debe ser una variable')            
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]!='?':
            raise Exception('Error: el segundo argumento de rest debe ser una variable')
        if not p.strip('"') in EXP_NAMESPACE:
            raise Exception('Error: La lista "%s" no esta definida'%p.strip('"'))
        if EXP_NAMESPACE[p.strip('"')]==[]:
            s[el.getElementos()[1]]=[]
        else:
            s[el.getElementos()[1]]=EXP_NAMESPACE[p.strip('"')][1:]

    elif el.getNombre()=='set': #
        #print 'EN SET'
        if len(el.getElementos())!=2:
            raise Exception('Error: El predicado especial "set" debe tener 2 argumentos')
        if not isString(el.getElementos()[0]):
            raise Exception('Error: el primer argumento de set debe ser una variable')            
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]!='?':
            raise Exception('Error: el primer argumento de set debe ser una variable')
        p=el.getElementos()[1]
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]=='?':
           p=findElInSust(el.getElementos()[1],s)        
        s[el.getElementos()[0]]=p             
        
    elif el.getNombre()=='getvalue': #????
        #print 'EN GETVALUE'
        #print [i for i in el.getElementos()]
        if len(el.getElementos())!=2:
            raise Exception('Error: El predicado especial "getvalue" debe tener 2 argumentos')
        p=el.getElementos()[0]
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?':
           p=findElInSust(el.getElementos()[0],s)
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]!='?':
            raise Exception('Error en setvalue: solo se pueden leer valores en variables')         
        s[el.getElementos()[1]]=EXP_NAMESPACE[p.strip('"')]
       

    elif el.getNombre()=='apply':
        #print 'EN APPLY'
        if len(el.getElementos())!=4:
            raise Exception('Error: El predicado especial "apply" debe tener 4 argumentos')
        #Buscar operando
        op=el.getElementos()[0].strip('"')
        if isString(el.getElementos()[0]) and el.getElementos()[0][0]=='?': #operador
           op=findElInSust(el.getElementos()[0],s)
        if op not in ['+','-','*','/','=','!=','>','<','>=','<=']:
            raise Exception('Error: "%s" no es un operador permitido'%op)
        oper1=el.getElementos()[1]
        if isString(el.getElementos()[1]) and el.getElementos()[1][0]=='?': #operando 1
            oper1=findElInSust(el.getElementos()[1],s)
        oper2=el.getElementos()[2]
        if isString(el.getElementos()[2]) and el.getElementos()[2][0]=='?': #operando 2
            oper2=findElInSust(el.getElementos()[2],s)
        if isString(el.getElementos()[3]) and el.getElementos()[3][0]!='?':
            raise Exception('Error en apply: el cuarto argumento debe ser una variable')              
        #Proceder segun operador
        if op=='+':
            s[el.getElementos()[3]]= int(oper1) + int(oper2)
        elif op=='-':
            s[el.getElementos()[3]]= int(oper1) - int(oper2)
        elif op=='*':
            s[el.getElementos()[3]]= int(oper1) * int(oper2)
        elif op=='/':
            s[el.getElementos()[3]]= int(oper1) / int(oper2)
        elif op=='==':
            if isNumber(str(oper1)):
                s[el.getElementos()[3]]= 1 if int(oper1)==int(oper2) else 0
            else:
                s[el.getElementos()[3]]= 1 if str(oper1)==str(oper2) else 0  
        elif op=='!=':
            if isNumber(str(oper1)):
                s[el.getElementos()[3]]= 1 if int(oper1)!=int(oper2) else 0
            else:
                s[el.getElementos()[3]]= 1 if str(oper1)!=str(oper2) else 0  
        elif op=='>=':
            if isNumber(str(oper1)):
                s[el.getElementos()[3]]= 1 if int(oper1)>=int(oper2) else 0
            else:
                s[el.getElementos()[3]]= 1 if str(oper1)>=str(oper2) else 0  
        elif op=='<=':
            if isNumber(str(oper1)):
                s[el.getElementos()[3]]= 1 if int(oper1)<=int(oper2) else 0
            else:
                s[el.getElementos()[3]]= 1 if str(oper1)<=str(oper2) else 0  
        elif op=='>':         
            if isNumber(str(oper1)):
                s[el.getElementos()[3]]= 1 if int(oper1)>int(oper2) else 0
            else:
                s[el.getElementos()[3]]= 1 if str(oper1)>str(oper2) else 0            
        elif op=='<':
            if isNumber(str(oper1)):
                s[el.getElementos()[3]]= 1 if int(oper1)<int(oper2) else 0
            else:
                s[el.getElementos()[3]]= 1 if str(oper1)<str(oper2) else 0
        retvalue=s[el.getElementos()[3]]
        #print 'VALOR DE RETVALUE: %s' % retvalue
    return retvalue


#Flag resultado de la evaluacion del ultimo elemento
global ULTIMO_EVALUADO

#Query global
QUERY=[]

class MotorInferencia:
    '''
    Motor de inferencia
    '''
    def __init__(self,basecon=None,corte_de_prioridad=-1,namespace=globals()):
        self.__query=[]
        self.__basecon=basecon
        #Si estan definidas, son reglas que se ejecutan al final de la query
        #self.__on_end_rules=None
        self.__sust=[]
        self.__contador=0
        self.__respuesta=[]
        self.__agenda=[]
        self.__corte_prioridad=corte_de_prioridad
        self.__namespace=namespace
        self.__namespace['__Engine__']=self
        self.__namespace['__BaseCon__']=self.__basecon
        self.__namespace['@__buffer__']=''        
        #self.__interprete=interprete(self.__namespace)
        self.__backresults=[]


    def resetEngine(self):
        self.__query=[]
        self.__basecon=basecon
        self.__sust=[]
        self.__contador=0
        self.__respuesta=[]
        self.__agenda=[]        


    def getQuery(self):
        return self.__query

    def query(self,query,reset=0):
        '''
        La consulta es una serie de clausulas
        query1(args),query2(args2),...,queryN(argsN)
        que hay que transformar en elementos
        para poder usarlos.
        '''
        global QUERY
        #Desactivar todas las reglas y vaciar agenda antes de hacer la consulta------
        self.__basecon.resetReglas()
        self.__agenda=[]
        #----------------------------------------------------------------------------
        #----------------------------------------------------------------------------        
        #-----------------CAMBIO 02/2009: self.__query=SYMTAB[__query__]-------------
        #Permite actualizar dinamicamente la query ??
        if reset==0:
            QUERY=[] #Borrar query antigua ????
        #self.__query=SYMTAB['__QUERY__']
        #print 'self.__query: %s\n' %SYMTAB['__QUERY__']
        #-----------------------------------------------------------------------------
        #-----------------------------------------------------------------------------
        
        if query =='':
            query='true(?x)'
        QUERY.extend(preparar(query))
        #print 'self.__query: %s\n' %SYMTAB['__QUERY__']
        #print 'self.__query despues de prepararla: %s\n' %SYMTAB['__QUERY__']
        self.__respuesta=self.__forwardchain(QUERY)
        print 'self.__respuesta: %s' %self.__respuesta
        #Revisar agenda
        self.revisarAgenda(self.__corte_prioridad)
        if self.__respuesta and len(self.__respuesta)>0 and len(self.__respuesta[0])>1:
            return [dict(el) for el in self.__respuesta]
        else:
            return self.__respuesta    

    def getBaseCon(self):
        return self.__basecon

    def setBaseCon(self,nueva):
        self.__basecon=nueva
        self.__namespace['BaseCon']=self.__basecon

    def addBaseCon(self,basecon):
        '''
        Adiciona todas las reglas de basecon a
        la base de conocimientos actual
        '''
        if basecon:
            for regla in basecon.getReglas():
                self.__basecon.addRegla(regla)


    def saveBasecon(self,name):
        '''
        Serializa la base de conocimiento actual
        '''
        self.__basecon.save(name)

    def __preparar(self,query):
        partes=query.split('),')
        salida=[]
        if len(partes)>1:
            for parte in partes:
                if parte[-1]!=')':
                    parte+=')'
                salida.append(Elemento(parte))
        else:
            salida.append(Elemento(query))
        return salida

    def __forwardchain(self,query):
        '''
        Rutina de encadenamiento hacia adelante
        '''
        ULTIMO_EVALUADO=0
        RECURSIVAS_ACTIVADAS=[] #0
        sust=[]
        deducido=[]
        query_antes=[]
        unificados=0
        contador=0
        print self.__basecon.toString()
        #print "Query en esta vuelta de forwardChain: %s" %query
        #while len(query_antes)< len(query) or RECURSIVAS_ACTIVADAS==1:
        while len(query_antes)< len(query) or len(RECURSIVAS_ACTIVADAS)!=0:            
            print 'vuelta: %d' %contador
            print "Query en esta vuelta de forwardChain: %s" %str([str(i) for i in query]) #str([i.getNombre() for i in query])
            #print 'len(query): %d' % len(query)
            #print 'len(query_antes): %d' % len(query_antes)
            print 'valor de deducido: %s' % deducido
            #resetar RECURSIVAS_ACTIVADAS
            #if contador==5:
            #    print 'BREAKING ALL!!!!'
            #    break
            RECURSIVAS_ACTIVADAS=[] #0
            contador+=1
            query_antes=query[:] #ojo:es una copia lo que necesitamos, no un puntero compartido!!
            for regla in self.__basecon.getReglas():
                #optimizacion: si activada, continuamos
                if regla.isActivada():
                    #print 'NOS SALTAMOS REGLA %s PQ ESTA ACTIVADA'% str(regla['entonces'][0])
                    continue
                #--------------------------------------
                print 'probando regla: %s' % str(regla['entonces'][0])
                print 'es RECURSIVA: %s' % regla.isRecursive()
                unificados=0
                for qel in query:
                    print 'probando query_el: %s' % qel.getNombre()
                    print 'unificados: %d' %unificados
                    #Sin predicados especiales-------------------------------------
                    if qel.isSpecial():
                        raise Exception('Error: no se permiten predicados especiales en la consulta')                       
                    #--------------------------------------------------------------
                    ##Cambio para poder manejar hechos--------------------------------------------------
                    if regla.isFact():
                        print 'Es un fact: %s!'%regla['entonces'][0].getNombre()
                        s=unificar(qel,regla['entonces'][0])#un hecho solo necesita un elemento
                        print 'valor de s: %s' % s
                        numidents=0
                        partial_resp=[]
                        if s:
                            regla.activar()
                            self.__agenda.append(regla)
                            #print 'poniendo EN LA AGENDA LA REGLA %s' %str(regla['entonces'][0])
                            #print self.__agenda
                            #Meter sustituciones validas en respuesta
                            for item in s:
                                print 'item: %s,%s'%(item,item[0])
                                if item[0]=='?':
                                    partial_resp.append([item,s[item]])
                                    #partial_resp.append(item)
                                    #partial_resp.append(s[item])
                                else:
                                    numidents+=1
                            if numidents==len(s): #and len(query)==1:
                                partial_resp.append("True")
                            
                            if partial_resp:
                                print 'metiendo en deducido: %s' % partial_resp
                                deducido.append([partial_resp])
                        ###
                    ##Fin cambio para poder manejar hechos----------------------------------------------                    
                        
                    else:
                        for el in regla['si']:
                            print 'con el: %s' % el.getNombre()
                                #print 'Intentando unificar %s y %s' % (qel.getNombre(),el.getNombre())
                            if ULTIMO_EVALUADO and el.isSpecial():
                                #print 'detectado elemento especial en la regla!',[i for i in el.getElementos()]
                                if solveSpecialPred(el,s):
                                    #print 'ESTO SE CUMPLE!!!'
                                    unificados+=1
                                    continue
                                else:
                                    #print 'FALLO AL EVALUAR PREDICADO ESPECIAL!!!!'
                                    if regla.getId() in RECURSIVAS_ACTIVADAS:
                                        del RECURSIVAS_ACTIVADAS[RECURSIVAS_ACTIVADAS.index(regla.getId())]
                                    #RECURSIVAS_ACTIVADAS=0
                                    break
                                    
                             
                            else:
                                s= unificar(qel,el)
                                print 'resultado de la unificacion: %s' %s
                            if s: #Si hay unificacion, agregamos a sustitucion
                                unificados+=1
                                #--------------------------------------------------------------
                                #Cambio para que las expresiones se evaluen solo si el elemento
                                #que se ha evaluado antes de llegar a ellas es true
                                ULTIMO_EVALUADO=1
                                #print 'puesto ultimo evaluado a 1 con %s' %el.getNombre()
                                #--------------------------------------------------------------
                                sust.append(s)
                            else:
                                ULTIMO_EVALUADO=0
                print 'unificados: %d' %unificados
                if not regla.isFact() and unificados==len(regla['si']): #Coinciden todos los elementos
                    print 'SUST: %s' % sust
                    print regla['entonces']
                    #nueva=sustituir(sust,regla['entonces'][0])#RECUPERAR SI VA MAL!!!!!!!!!
                    nueva=[sustituir(sust,p) for p in regla['entonces']]
                    #deducido.append(nueva)
                    print 'NUEVA: %s' % nueva
                    #print 'ESTAN ASI: ',nueva.getNombre(),[i.getNombre() for i in query]
                    for item in nueva: #QUITAR EL FOR SI VA MAL!!!!!!! y cambiar item por nueva!!
                        if item.getNombre() not in [i.getNombre() for i in query]:#?????????
                            query.append(item)
                            print 'AUMENTAMOS QUERY EN UN ELEMENTO'
                        else: #Sustituir la antigua por la nueva
                            idx=[i.getNombre() for i in query].index(item.getNombre())
                            query[idx]=item
                            print 'SUSTITUIMOS LA ANTIGUA!!!'
                    #print [elem.getNombre() for elem in query]
                    if not regla.isRecursive():
                        regla.activar() #Para evitar evaluar mas de una vez una regla activada
                    else:
                        #RECURSIVAS_ACTIVADAS=1
                        RECURSIVAS_ACTIVADAS.append(regla.getId())
                        #print "RECURSIVAS_ACTIVADAS: %s" %RECURSIVAS_ACTIVADAS
                        #print 'HAY REGLAS RECURSIVAS ACTIVADAS!!!!!!!!!'
                    ULTIMO_EVALUADO=0 #Resetear el flag
                    #print 'puesto ultimo evaluado a 0'
                    if not regla in self.__agenda:
                        #print 'PONIENDO EN LA AGENDA LA REGLA %s' %str(regla['entonces'][0])
                        self.__agenda.append(regla)
                    sust=[]
                unificados=0
            #print 'len(query) al final de los for: %d' % len(query)
            #print 'len(query_antes) al final de los for: %d' % len(query_antes)
        return deducido
                
                        
    
    #Metodo que permite evaluar expresiones logicas validas
    #Se evaluan a 0 o 1    
    def evalua_elemento(self,elemento,last_result):#????????????
        #print 'ultimo evaluado en evalua_elemento: %s' %str(ULTIMO_EVALUADO)
        expr=elemento.getElementos()[0] #De momento solo evaluamos el primer elemento
        #print 'evaluando expresion: %s' %expr
        #try:
        if last_result:
            #Intentamos evaluarla. Si se puede
            #devolvemos 1, si no, un cero
            program=minimal_py.preprocess(program)
            code=minimal_py.parser.parse(program)
            #print code
            exec code
            resul=1
            #print 'resultado: %s' %str(resul)
            elemento.setEvaluado(1)
            return resul
        else:
            #print 'no evaluamos la expresion pq ultimo evaluado vale 0'
            return 0
##        except:
##            print "Excepcion en evalua elemento\n"
##            return 0

    def revisarAgenda(self,corte_prioridad,corte_certeza=1):
        '''
        Ejecuta las acciones de las reglas que estan en ella
        en orden de prioridad y grado de certeza creciente. Si existe
        un corte de prioridad, solo se ejecutan
        aquellas cuya prioridad es igual o mayor
        que la del corte
        '''
        #print 'revisando agenda...'
        #print self.__agenda
        resultado=[]
        if len(self.__agenda) > 0:
            #Ejecutar los comandos de las reglas
            #que estan en la agenda
            #por orden de prioridad
            for p in range(MAX_PRIORITY):
                for item in self.__agenda:
                    #print item,item.getPrioridad()
                    if item.getPrioridad()==p and item.getComandos() <> '' and p>=corte_prioridad and item.getCerteza()>=corte_certeza:
                        resultado.append(item.getComandos())
            #Cambio: no ejecutamos codigo, sino que evaluamos las acciones
            #Las acciones son codigo interpretable por parse_expr.py
            #print 'Resultado: %s' %resultado
            for com in resultado:
                program=minimal_py.preprocess(program)
                code=minimal_py.parser.parse(program)
                print code
                exec code


    def getCortePrioridad(self):
        return self.__corte_prioridad

    def setCortePrioridad(self,nuevo):
        self.__corte_prioridad=nuevo


    def getNamespace(self):
        return self.__namespace


    def setNamespace(self,nuevo):
        self.__namespace=nuevo
        #Ponemos a disposicion del codigo el motor de inferencia
        #y la base de conocimientos cargada
        self.__namespace['__Engine__']=self
        self.__namespace['__BaseCon__']=self.__basecon
        self.__namespace['@__buffer__']=''





if __name__=='__main__':
    print 'Codigo de prueba...\n\n'

 