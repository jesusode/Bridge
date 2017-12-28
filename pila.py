#!Python

class Pila:
    """
    Clase que implementa una pila
    """
    def __init__(self):
        self.__pila=[]


    def pop(self):
        if len(self.__pila)!= 0:
            return self.__pila.pop()


    def push(self,element):
        self.__pila.append(element)


    def getList(self):
        return self.__pila


    def size(self):
        return len(self.__pila)



    def isEmpty(self):
        return self.__pila==[]


    def empty(self):
        self.__pila=[]


    def peek(self):
        if not self.isEmpty():
            return self.__pila[0]
        else:
            return None

    def toString(self):
        return str(self.__pila)



#Codigo de prueba

if __name__=='__main__':
    p=Pila()
    p.push('uno')
    p.push('dos')
    p.push('tres')
    print p.pop()
    print p.pop()
    print p.pop()