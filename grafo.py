#!Python

from pila import *
from cola import *
import random

class Nodo:
    """
    Clase que implementa el nodo de un grafo
    """
    def __init__(self):
        self.__id=0
        self.__nombre=''
        self.__contenido=None
        self.__visitado=0


    def setId(self,id):
        self.__id=id

    def getId(self):
        return self.__id

    def setNombre(self,nombre):
        self.__nombre=nombre

    def getNombre(self):
        return self.__nombre

    def setContenido(self,contenido):
        self.__contenido=contenido

    def getContenido(self):
        return self.__contenido

    def setVisitado(self,visitado):
        self.__visitado=visitado


    def isVisitado(self):
        return self.__visitado
    
    def toString(self):
        return 'Node "%s" with content "%s"'%(self.getNombre(),self.getContenido())


class Arco:
    """
    Clase que implementa un arco ponderado
    entre dos nodos de un grafo
    """
    def __init__(self,n1,n2,w):
        self.id=str(long(random.random()*10000000000))
        self.node1=n1
        self.node2=n2
        self.weight=w
    def toString(self):
        return 'Arc id "%s" between "%s" and "%s" with weight: "%s"' %(self.id,self.node1,self.node2,self.weight)


class Grafo:
    """
    Clase que implementa un grafo
    como lista de adyacencia
    """
    def __init__(self):
        #Estructura que soporta el grafo
        #grafo={id_nodo:[arco1..arcon]...}
        self.__grafo={}
        #Estructura que soporta los nodos
        #grafo={id_nodo:nodo,...}        
        self.__nodos={}
        self.__nodos_by_name={}
        #Estructura que soporta los arcos
        self.__arcos={}
        #Lista con los contenidos para evitar dobles inserciones
        #Variable para dar las id de los nodos
        self.__contador=0

    def addNodo(self,contenido,nombre=''):
        nodo=Nodo()
        nodo.setId(self.__contador)
        self.__contador+=1
        nodo.setContenido(contenido)
        nodo.setVisitado(0)
        if nombre=='':
            nombre=str(long(random.random()*10000000000))
        nodo.setNombre(nombre)
        self.__grafo[nodo.getId()]=[]
        self.__nodos[nodo.getId()]=nodo
        self.__nodos_by_name[nodo.getNombre()]=nodo        
        return nodo.getId()


    def getNodo(self,idNodo):
        if self.__nodos.has_key(idNodo):
            return self.__nodos[idNodo]
        else:
            return None


    def getNodos(self,byname=0):
        if not byname:
            return self.__nodos
        else:
            return self.__nodos_by_name


    def getContenidos(self):
        return [n.getContenido() for n in self.__nodos.values()]


    def getSucesores(self,idNodo):
        if self.__nodos.has_key(idNodo):
            return self.__grafo[idNodo]
        else:
            return None
        
    #Arco deberia ser un objeto y deberia poderse
    #elegir si es simetrico o no.
    def addArco(self,id1,id2,wght=0,bidi=0):
        arco=Arco(id1,id2,wght)
        #print arco.toString()
        if self.__grafo.has_key(id1) and self.__grafo.has_key(id2):
            self.__grafo[id1].append(id2)
            self.__arcos[arco.id]=arco
            if bidi: #Si bidi es 1, el grafo es no dirigido
                self.__grafo[id2].append(id1)
            return 1
        else:
            return 0



    def resetNodos(self):
        for nodo in self.__nodos.keys():
            self.__nodos[nodo].setVisitado(0)
            

    def toString(self):
        #print 'Grafo:'
        #print str(self.__grafo)
        #print 'Nodos:'
        #print str(self.__nodos)
        #print 'Arcos:'
        #print str(self.__arcos)
        result={}
        for el in self.__grafo:
           result['ID ' + str(el) + ' that is '+self.getNodo(el).toString()+ ' has connections with: ' ]=[self.getNodo(i).getNombre() for i in self.__grafo[el]]
        #return str(self.__grafo)
        return result

    def arcsToString(self):
        result=""
        for el in self.__arcos:
            result+=self.__arcos[el].toString() + '\n'
        return result

        
    #Si el primer nodo no tiene sucesores, falla. Es correcto?
    def recorrerEnAnchura(self):
        """
        Recorrido en anchura del grafo
        """
        self.resetNodos()
        camino=[]
        cola=Cola()
        #Empezamos por el primer nodo (id=0)
        nodo=self.__nodos[0]
        nodo.setVisitado(1)
        camino.append(nodo.getId())
        #Encolar sucesores del primer nodo
        for sucesor in self.__grafo[nodo.getId()]:
            cola.meter(self.__nodos[sucesor])
        actual=cola.sacar()
        while actual:
            if not actual.getId() in camino:           
                camino.append(actual.getId())
            #Visitar el nodo actual
            actual.setVisitado(1)
            #Encolar sus sucesores no visitados
            for sucesor in self.__grafo[actual.getId()]:
                if not self.__nodos[sucesor].isVisitado():
                    cola.meter(self.__nodos[sucesor])
                    #self.__nodos[sucesor].setVisitado(1)#?parece que si
            #print str(camino)
            actual=cola.sacar()
        return camino

    #Si el primer nodo no tiene sucesores, falla. Es correcto?
    def recorrerEnProfundidad(self):
        """
        Recorrido en profundidad del grafo
        """
        self.resetNodos()
        camino=[]
        pila=Pila()
        #Empezamos por el primer nodo (id=0)
        nodo=self.__nodos[0]
        nodo.setVisitado(1)
        camino.append(nodo.getId())
        #Apilar sucesores del primer nodo
        for sucesor in self.__grafo[nodo.getId()]:
            pila.push(self.__nodos[sucesor])
        actual=pila.pop()
        while actual:
            camino.append(actual.getId())
            #Visitar el nodo actual
            actual.setVisitado(1)
            #Apilar sus sucesores no visitados
            for sucesor in self.__grafo[actual.getId()]:
                if not self.__nodos[sucesor].isVisitado():
                    pila.push(self.__nodos[sucesor])
                    #print pila.toString()
            #print str(camino)
            actual=pila.pop()
        return camino


    def __noVisitados(self,elem):
        """
        Devuelve una lista con los sucesores
        no visitados de un nodo
        """
        no_visitados=[]
        for sucesor in self.getSucesores(elem):
            if not self.__nodos[sucesor].isVisitado():
                no_visitados.append(sucesor)
                #print 'No Visitados: ' + str(no_visitados)
        return no_visitados

    def buscaCamino(self,nodo1,nodo2):
        """
        Busca un camino entre dos nodos de un grafo
        Algoritmo:
        1.- Poner en camino el primer nodo
        2.- Poner en la pila sus sucesores
        3.- Mientras haya sucesores sin visitar hacer:
        4.- Sacar un elemento de la pila y ponerlo en camino
        5.- Si es el nodo2,retornar camino
        6.- Si no, poner sus sucesores no visitados en la pila
        7.- Si el elemento no tiene sucesores sin visitar,
            sacar de camino el ultimo elemento si no tiene sucesores sin visitar
            mientras se pueda
        8.- Si no quedan nodos sin visitar,devolver la lista vacia        
        """
        if nodo1==nodo2: #De un nodo a si mismo siempre hay camino
            return [nodo1]
        self.resetNodos()
        #Pila que soporta la busqueda con retroceso
        pila=Pila()
        camino=[]
        #Poner en camino el primer nodo:
        camino.append(nodo1)
        #Marcarlo como visitado
        self.__nodos[nodo1].setVisitado(1)
        #Poner en la pila sus sucesores
        for sucesor in self.getSucesores(nodo1):
            pila.push(sucesor)
        #print pila.toString()
        while not pila.isEmpty():
            #print 'Contenido de la pila: ' + pila.toString()
            #Sacar un elemento de la pila y ponerlo en camino
            elem=pila.pop()
            #Marcarlo como visitado
            self.__nodos[elem].setVisitado(1)
            camino.append(elem)
            #Si es el nodo final devolvemos camino
            if elem==nodo2:
                return camino
            else:
                antes=pila.size()
                #Poner sus sucesores no visitados en la pila
                if self.__noVisitados(elem) != []:
                    for sucesor in self.__noVisitados(elem):
                        pila.push(sucesor)
                despues=pila.size()
                #print 'Contenido de la pila: ' + pila.toString()
                #Si no hay cambio en la longitud de la pila
                #es que no hay ningun sucesor no visitado
                #y tenemos que dar marcha atras
                if antes==despues:
                    #print 'Realizando marcha atras...'
                    #Quitar el ultimo elemento de camino
                    #hasta que alguno tenga algun sucesor
                    #no visitado
                    # o se vacie
                    #"""
                    while len(camino) > 0:
                        ultimo=camino[len(camino)-1]
                        #print 'Camino: ' + str(camino)
                        #print 'ultimo= ' + str(ultimo)
                        if self.__noVisitados(ultimo)==[]:
                            del camino[len(camino)-1]
                        else:
                            break
                    #"""
        if len(camino)==1: #no se ha encontrado camino
               camino=[]                   
        return camino


    def buscaTodosLosCaminos(self,node1,node2 ,path=[]):
        path = path + [node1]
        if node1 == node2:
            return [path]        
        if not self.__grafo.has_key(node1):
            return []
        paths = []
        for node in self.getSucesores(node1):
            if node not in path:
                newpaths = self.buscaTodosLosCaminos(node, node2, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def buscaCaminoMasCorto(self,node1,node2,path=[]):
        path = path + [node1]
        if node1 == node2:
            return path         
        if not self.__grafo.has_key(node1):
            return []
        shortest=None
        for node in self.getSucesores(node1):
            if node not in path:
                newpath = self.buscaCaminoMasCorto(node, node2, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest=newpath
        return shortest

               
##    def find_all_paths(graph, start, end, path=[]):
##        path = path + [start]
##        if start == end:
##            return [path]
##        if not graph.has_key(start):
##            return []
##        paths = []
##        for node in graph[start]:
##            if node not in path:
##                newpaths = find_all_paths(graph, node, end, path)
##                for newpath in newpaths:
##                    paths.append(newpath)
##        return paths


##    def find_shortest_path(graph, start, end, path=[]):
##            path = path + [start]
##            if start == end:
##                return path
##            if not graph.has_key(start):
##                return None
##            shortest = None
##            for node in graph[start]:
##                if node not in path:
##                    newpath = find_shortest_path(graph, node, end, path)
##                    if newpath:
##                        if not shortest or len(newpath) < len(shortest):
##                            shortest = newpath
##            return shortest    

    
#Codigo de prueba
if __name__=='__main__':
    g=Grafo()
    g.addNodo('nodo0')
    g.addNodo('nodo1')
    g.addNodo('nodo2')
    g.addNodo('nodo3')
    g.addNodo('nodo4')
    g.addNodo('nodo5')
    g.addArco(0,1,5)
    g.addArco(0,2,5)
    g.addArco(1,5,5)
    g.addArco(2,3,8)    
    g.addArco(2,4,16)
    g.addArco(3,4,7)
    g.addArco(5,4,9)
    g.addArco(0,4,1000)
    print g.toString()
    print 'Recorrido en profundidad:'
    print str(g.recorrerEnProfundidad())
    print 'Recorrido en anchura:'
    print str(g.recorrerEnAnchura())
    print 'Camino entre nodos 4 y 1:'
    print str(g.buscaCamino(4,3))
    print 'Camino entre nodos 0 y 4:'
    print str(g.buscaCamino(0,4))
    print 'Buscar todos los caminos entre 0 y 4'
    print str(g.buscaTodosLosCaminos(0,4))
    print 'Buscar el camino mas corto entre 0 y 4'
    print str(g.buscaCaminoMasCorto(0,4))