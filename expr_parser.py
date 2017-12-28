from __future__ import division
#!Python

#Para medir eficiencia------------------------------------------------
import time
#print 'Comenzando carga de modulos: %s' % time.strftime('%H:%M:%S')
#---------------------------------------------------------------------

from  _globals import *
import _globals
import yacc
import os
import os.path
import sys
import string
from RegExp2 import *
import re
import imp
import runpy
import minitree
import urllib
import xml.dom.minidom as minidom

from matrix import *
from filtereddict import *

import locale
import codecs

import random
import math

#Para ordenar listas eficientemente-------------------------------------
import heapq
#-----------------------------------------------------------------------

#Cambio para poder crear y usar grafos----------------------------------
import grafo
#-----------------------------------------------------------------------

#Para usar BeautifulSoup--------------------------------------------------------------
from BeautifulSoup import BeautifulSoup # For processing HTML
from BeautifulSoup import BeautifulStoneSoup # For processing XML
from BSXPath import BSXPathEvaluator,XPathResult #Para poder usar expresiones XPATH
#-------------------------------------------------------------------------------------

#Para usar xpath con minidom (requiere py-dom-xpath)----------------------------------
import xpath
#-------------------------------------------------------------------------------------

#Para usar iteradores-----------------------------------------------------------------
import itertools
import operator
import itertools_recipies
#-------------------------------------------------------------------------------------



###-------------------Cambio para extensiones TQL--------------
from textformatter import *
from textformatter2 import *
###------------------------------------------------------------


#Esto para que no molesten los warnings------------------------
import warnings
warnings.filterwarnings('ignore')
#--------------------------------------------------------------


#Cambio para funcionar como shell experto------------------------
from inference_engine2 import *
from basecon import *
from reglas import *
#----------------------------------------------------------------

from minilistitem import *

#print 'Antes de llegar a las que dependen del sistema operativo: %s' % time.strftime('%H:%M:%S')

#Cambio para soporte COM nativo--------------------------------
if 'win32' in OSSYSTEM:
    if not 'PyPy' in sys.version: #En PyPy no funcionan las extensiones de momento
        import win32com.client
        import win32con
    #Para usar JPype-------------------------------------------------
        import jpype        
    #--------------------------------------------------------------
        #print 'win32 cargado: %s' % time.strftime('%H:%M:%S')

#Para ejecutar codigo java inline------------------------------
if 'java' in OSSYSTEM:
    import java
    import miniutils
    import jarray
#--------------------------------------------------------------

#Para ejecutar codigo .NET inline------------------------------
if not 'java' in OSSYSTEM and not 'darwin' in OSSYSTEM and not 'linux' in OSSYSTEM and not 'PyPy' in sys.version:
    import clr
    clr.AddReference('System')
    import System
    clr.AddReference('dyncompiler2')
    import dyncompiler2
    #print '.NET cargado: %s' % time.strftime('%H:%M:%S')
#--------------------------------------------------------------

SQLITE_AVAILABLE=0    

#Para permitir extensiones SQL nativas con SQLite--------------
if not 'java' in OSSYSTEM and not 'PyPy' in sys.version: 
    import sqlite3
    SQLITE_AVAILABLE=1
    #print 'sqlite cargado: %s'% time.strftime('%H:%M:%S')
#--------------------------------------------------------------

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')



#funcion que busca un elemento en una lista que puede tener listas anidadas
def findInSublist(lst,el,look_elems=0):#??
    #print 'buscando elem "%s" en lista: "%s"' % (el,lst)
    for i in range(len(lst)):
        #print 'valor de i: %s' % i
        #print 'vamos por list[i]: %s' % lst[i]
        if look_elems==1 and el==lst[i]: 
            #print 'encontrado en %s'%i
            return i
        if type(lst[i])==type([]): #Buscar solo en sublistas
            for item in lst[i]:
                #print 'probando item: "%s" con el "%s"' % (item,el)
                if item==el:
                   #print 'encontrado2 en elemento %s'%i
                   return i
                else:
                    if type(item)==type([]):
                        #Si es el 0, nos vale
                        #print 'item problematico: %s' %item
                        if item and item[0]==el:
                           #print 'Encontrado antes de la recursion como 0'
                           return i
                        #print 'Llamada recursiva!'
                        if findInSublist(item,el) != -1:
                            #print 'Encontrado en llamada recursiva'
                            return i
                        
        #print 'dando otra vuelta al bucle principal'
    return -1


#Funcion que recupera una lista normal a partir de otra de instancias de MiniListItem
def decodeList(itemlist,_result=[]):
    #print 'en decodelist con %s y _result %s' % (itemlist,_result)
    for item in itemlist:
        #print 'recorriendo item: %s' % item
        if isinstance(item,MiniListItem): #trivial, a la lista
            #print 'caso trivial'
            _result.append(item.value)
        elif type(item)==type([]): #lista de items.Recursivo con cada uno
            #print 'caso recursivo'
            _result.append(decodeList(item,[]))
    #print 'devolviendo: %s' % result
    return _result


#Clase que representa a un item de groupby
class GroupItem(object):
	def __init__(self):
		self.count=0
		self.value=0
		self.items=[]
		self.max=-float('inf')
		self.min=float('inf')
	def __repr__(self):
		return '<count: %s , value: %s , items: %s , max: %s , min: %s>'%(self.count,self.value,self.items,self.max,self.min)

#Funcion para construir una tabla de diccionarios para linq-like
def groupbyTable(master,_list,limit):
  if isinstance(master,GroupItem) and limit==len(_list):
     limit=0
     return
  if len(master)==0 and limit==len(_list):
     limit=0
     return
  if len(master)==0:
     for item in _list[limit]:
        if _list[limit]==_list[-1]:
           master[item]=GroupItem()
        else:
           master[item]={}
     limit+=1
  for dic in master:
     groupbyTable(master[dic],_list,limit)


def processGroupbyRows(mtx,table,indexes):
    global attrs_list
    #print '\n\nindexes: %s' %indexes
    filas=mtx.getList()
    #print 'filas: %s' % filas
    #Buscar funcion de agregado si la hay y la posicion
    func=''
    fpos=-1
    for k in attrs_list:
        if k[2]!='':
            func=k[2]
            fpos=k[1]
            break
    #print 'valor de func: %s' %func
    for fila in filas:
        campos=[]
        for item in indexes:
            campos.append(fila[item[1]])
        #print 'Campos: %s' % campos
        actual={}
        last={}
        actual=table
        #Ir obteniendo el subdiccionario de cada campo
        #si falla, salimos
        #si se completa, sumar 1
        #print 'valor de actual: %s' % actual
        actindex=0
        for item in campos:
            if actual.has_key(item):
                #print 'actual:%s' %actual
                last=actual
                actual=actual[item]
                #if type(actual) in [type(0),type(0L),type(0.0)]:
                if isinstance(actual,GroupItem):
                    if func in ['','count']:
                        last[item].count+=1
                    else:
                        if len(fila)< fpos:
                            last[item].count+=1
                            last[item].value+=fila[fpos]
                            #Esto solo se calcula si es necesario
                            if func in ['std','stdp','var','varp']:
                                last[item].items.append(fila[fpos])
                            if func=='max':
                                if fila[fpos]> last[item].max:
                                   last[item].max=fila[fpos]
                            if func=='min':
                                if fila[fpos]< last[item].min:
                                   last[item].min=fila[fpos]                                   
                        else:
                            last[item].count+=1
                            last[item].value+=fila[-1]
                            #Esto solo se calcula si es necesario
                            if func in ['std','stdp','var','varp']:
                                last[item].items.append(fila[-1])
                            if func=='max':
                                if fila[-1]> last[item].max:
                                   last[item].max=fila[-1]
                            if func=='min':
                                if fila[-1]< last[item].min:
                                   last[item].min=fila[-1]                            
            actindex+=1


def groupbyToRows(table,out,row):
    #print 'Valor actual de table:%s' % table
    global group_list
    global attrs_list
    if type(table)==type({}):
     for item in table:
        #print 'Recorriendo item: %s' % item
        #print 'con row: %s'%row
        row.append(item)
        if type(table[item])==type({}):
            #print "llamada recursiva con row: %s"%row
            for el in table[item]:
                row.append(el)
                #print 'recorriendo subitem %s'%el
                #print 'row:%s'%row
                groupbyToRows(table[item][el],out,row)
                row=[item]
                
            row=[]
        else:
            #print "metiendo numero"
            row.append( table[item])
            #print 'row a meter:%s'%row           
            if row[-1]>0:
                functions=[]
                #Si se nos pide un agregado, poner el valor del agregado
                for j in attrs_list:
                    #print 'comprobando campo select aqui: %s' %j
                    if j[2]!='':
                        functions.append(j[1])
                #print 'functions: %s' % functions
                #print 'len(row): %s' %len(row)
                if functions!=[]:
                    if functions[0]>=1:#len(row):
                        out.append(row)
                    else:
                        fval=row[-1]
                        row[functions[0]]=fval
                        out.append(row[:-1])
                else:
                    out.append(row[:-1])
            row=row[:-2]
    else:
        row.append(table)
        #print 'ultima row a meter:%s'%row
        if row[-1]>0:
            functions=[]
            #Si se nos pide un agregado, poner el valor del agregado
            for j in attrs_list:
                #print 'comprobando campo select: %s' %j
                if j[2]!='':
                    functions.append(j[1])
            if functions!=[]:
                if functions[0]>=1:#len(row):
                    out.append(row)
                else:
                    fval=row[-1]
                    row[functions[0]]=fval
                    out.append(row[:-1])
            else:
                out.append(row[:-1])
        #print 'metiendo row:%s'%row
        row=[]        


def satisfyConditions(conds,item,at):
    #comprobar que cumple las condiciones si las hay
    condsOk=1
    at2=None#??
    #print 'conds:%s' % conds
    #print 'attrs_lists: %s' %attrs_list
    #print 'at: %s' %at
    if conds!=[]:
        for cond in conds:
            #Hay que permitir evaluar campos distintos del que se ha mandado(select texto where id...)
            #print 'evaluando item:%s' % item
            #print 'evaluando condicion:%s' % cond
            #print 'con valor de at: %s' %at
            atval=None            
            if isinstance(item,MiniObject):
                if at!=cond[0]:
                    at2=cond[0]
                    atval=getattr(item,at2)
                else:
                    atval=getattr(item,at)
                #print 'atval en objeto:%s' % atval
            elif type(item)==type({}):
                if at!=cond[0]:
                    at2=cond[0]
                    atval=item[at2]
                else:
                    atval=item[at]
                #print 'atval en diccionario:%s' % atval
            elif type(item)==type([]):
                #print 'item:%s' % item
                #print 'at: %s' % at
                atval=item[at[1]]
                #print 'elemento para comprobar: %s' % atval
                at2=at[0] #antes era at aqui y abajo?
            if at2==cond[0]:
                if cond[1]=='=':
                    if atval!=cond[2]:
                        condsOk=0
                        break
                if cond[1] in ['!=','<>']:
                    if atval==cond[2]:
                        condsOk=0
                        break                                
                elif cond[1]=='>':
                    if atval<=cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='<':
                    if atval>=cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='>=':
                    if atval<cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='<=':
                    if atval>cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='contains':
                    if not cond[2] in atval:
                        condsOk=0
                        break
                elif cond[1]=='not contains':
                    if cond[2] in atval:
                        condsOk=0
                        break                     
                elif cond[1]=='in':
                    if atval not in cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='not in':
                    if atval in cond[2]:
                        condsOk=0
                        break
                elif cond[1]=='like':
                    if not cond[2] in atval:
                        condsOk=0
                        break
                elif cond[1]=='not like':
                    if cond[2] in atval:
                        condsOk=0
                        break                     
                elif cond[1]=='between':                   
                    if not (atval>=cond[2] and atval<=cond[3]):
                        condsOk=0
                        break
                elif cond[1]=='not between':                     
                    if atval>=cond[2] and atval<=cond[3]:
                        condsOk=0
                        break
                #FALTA IMPLEMENTAR REGEX!!!!!!!!!!!!!
    return condsOk
            

#print 'interprete' in sys.modules
from interprete import runMiniCode,MiniCoroutine
#print 'interprete cargado: %s' % time.strftime('%H:%M:%S')

#Cambio para permitir S-expresiones, prolog nativo y pseudo Forth------------
import lispy
import prolog3_for_mini
import mini_forth
if not 'java' in OSSYSTEM:
    import pyscheme
#----------------------------------------------------------------------------


#Cambio para poder usar una BD relacional en Python(SnakeSQL)----------------
import datetime
import SnakeSQL
#----------------------------------------------------------------------------

###Correccion para IronPython-------------
##if 'cli' in sys.platform:
##    import stlex2ipy as stlex2
##    print 'lexer alternativo en expr_parser'
##else:
##    print 'importando MAL en expr_parser'
##    import stlex2
###---------------------------------------
import stlex2

# Get the token map from the lexer.  This is required.

tokens=stlex2.tokens
#from stlex2 import tokens (a recuperar si va mal!!!)
#print 'Terminando carga de modulos en expr_parser: %s' % time.strftime('%H:%M:%S')


__version__='2.0'

__date__='2013-01-31'

#Build the lexer
#lexer=stlex2.lex (a recuperar si va mal!!!)

#Variable auxiliar para definicion de diccionarios
pair_list=[]

#Variables auxiliares para parametros de funciones
params_list=[]

#Variables globales para extensiones com
com_pair_list=[]
com_var_counter=0

#Variable auxiliar para definicion de listas
item_list=[]
item_list_aux=[]
expr_counter=0
just_append=0
expr_list=[]
list_op_performed=0
list_depth=0
last_list_expr=''
listexp_from_expr=0
item_list_counter=0

#Variables auxiliares para definicion de accesores
accesor_list=[]
accesor_list2=[]

#Variable auxiliar para acceso a campos de objeto anidados(obj.fld1.fl2.fld3)
object_field_list=[]

#Variable auxiliar para crear grafos
graph_nodes_list=[]
graph_list=[]

#Lista de tipos
types_list=[]
#lista de opciones para tipos
options_list=[]
#Lista de expresiones de tipos
type_exprs=[]
#Flag para definir tipos "uno de"
type_choice=0
#Flag para tipos  "lista de"
type_listof=0
#Lista de valores para get type
gettype_list=[]

#Flag global para obtener resultados select tql como una lista
select_as_list=0

#Lista de valores para atributos de linq like
attrs_list=[]
linqresult_list=[]
where_list=[]
group_list=[]
order_list=[]
order_type=''

#Lista de valores para inicializadores de objetos
objpairs_list=[]

#Lista de tipos de bases de datos soportadas por el lenguaje-------------------------------------------------------------------
ALLOWED_DATABASES=['sqlite','sqlitescript','access','sqlserver','text','excel','ado','mysql','oracle','postgresql','snakesql']
#------------------------------------------------------------------------------------------------------------------------------

#Clase que representa a un item de lista
# class MiniListItem(object):
    # def __init__(self,value):
        # self.value=value
    # def __repr__(self):
        # return str(self.value)

class MiniObjectClass(object):
    def __init__(self):
        self.name=''
        self.fields_names=[]
        self.private_fields=[]
        self.bases=[]
        self.macros=[]
    def findMacros(self):
        #Busca las macros definidas para este tipo en la tabla de simbolos (tendran el tipo: '.<self.name>')
        pass



class MiniObject(object):
    def __init__(self,_type):
        self.__type=_type
        self.__info=None
        self.__flds=[]
        self.__methods=[]
        #Crear objeto segun prototipos pasados en bases
        if not self.__type in SYMTAB['__DEFINED_TYPES__']:
            raise Exception('Excepcion creando objeto: El tipo "%s" no esta definido,' % self.__type)
        if self.__type!='object': #Si el tipo es object, solo tiene un atributo: __type
            #Por cada campo definido en el MiniObjectInfo correspondiente al tipo, crear un atributo
            self.__info=SYMTAB['__DEFINED_OBJECTS__'][self.__type]
            for field in self.__info.fields_names:
                ###Los campos que comienzan con 'private' se consideran privados y no se heredan##### (mejor una palabra clave???)
                setattr(self,field[0],SYMTAB['__NULL__'])
                self.__flds.append(field[0])
                #Comprobar que existe el campo
                ##print 'Valor del atributo %s creado: %s' %(field[0],getattr(self,field[0]))


    def getType(self):
        return self.__type

    def getFieldsNames(self):
        #return [fld[0] for fld in self.__info.fields_names]
        return self.__flds

    def getFields(self):
        return self.__info.fields_names
    

    def getFieldType(self,fldname):
        flds=[fld[0] for fld in self.__info.fields_names]
        ##print flds
        i=flds.index(fldname)
        if i<0:
            raise Exception('El objeto no posee el campo %s' % fldname)
        return self.__info.fields_names[i][1]

    def getBases(self):
        return self.__info.bases

    def hasBase(self,base):
        return base in self.__info.bases

    def findMacros(self):
        #Busca las macros definidas para este tipo en la tabla de simbolos (tendran el tipo: '.<self.name>')
        for item in SYMTAB['__MACROS__']:
            for el in [self.__type] + self.__info.bases:
                if item.find(el)==0:
                    if not item in self.__methods:
                        self.__methods.append(item)
        return self.__methods
    
    def __repr__(self):
        return '<MiniObject instance of type "%s">' %self.__type    



#Clase que envuelve una enumeracion
class Enum(object):
    def __init__(self,values):
        self.list=values
        self.dict={}
        for el in self.list:
            self.dict[el]=self.list.index(el)
        #print self.dict

    def __contains__(self,elem):
        if int(elem) in self.dict.values():
            return 1
        else:
            return 0

    def toList(self):
        return self.list
    

#Clase que envuelve un iterador sobre una secuencia finita
class MiniIter(object):
    def __init__(self,iterable,loop=0):
        self.__iterable=iterable
        self.__next=-sys.maxint
        self.__cursor=0
        self.__len=len(iterable)
        self.__loop=loop

    def getNext(self):
        return self.__next

    def getIterable(self):
        return self.__iterable

    def getLoop(self):
        return self.__loop     

    def next(self):
        if self.__cursor<len(self.__iterable):
            self.__next=self.__iterable[self.__cursor]
            self.__cursor+=1
            #restar 1 al valor de len si no es ciclico
            if self.__loop==0:
                self.__len-=1
            return 1
        else:
            if self.__loop==0:
                self.__next=sys.maxint
                self.__len=0
                return 0
            else: #repetimos
                self.__cursor=0
                self.__next=self.__iterable[self.__cursor]
                self.__cursor+=1
                return 1

    def __len__(self):
        #print 'len del iterador: %s' %self.__len
        return self.__len

#Funcion de utilidad que obtiene el tipo de un campo de un objeto
def findFieldType(objname,fldname): #obsoleta???
    tp=SYMTAB['__OBJECT_INSTANCES__'][objname].getFieldType(fldname)
    #Convertir el tipo a algo que sea compatible con lo que devuelve type()
    if tp=='numeric':
        return "<type 'float'>" #En Mini todos los numeros son floats
    elif tp=='string': #str o unicode
        return "<type 'str'>"
    else: #any
        return tp

#Funcion de utilidad que obtiene el ultimo objeto de una cadena de acceso
def findObjectField(acc_string):
    #print 'En findObjectField: %s' %acc_string
    retval=[]
    elems=[]
    if type(acc_string)==type([]):
        elems=acc_string
    else:
        elems=acc_string.split('.')
    #print elems
    if len(elems)==2: #Un solo campo
        return elems
    else:
        objname=elems[0]
        field=elems[-1]
        fields=elems[1:-1]
        #fields=elems[1:]
        #print fields
        if not SYMTAB['__OBJECT_INSTANCES__'].has_key(objname):
            raise Exception('Error: El objeto "%s" no esta definido'%objname)
        temp=None
        for item in fields:
            #Asegurarse de que cada campo se corresponde con un objeto
            #print item
            if isinstance(temp,MiniObject):
                temp=getattr(objname,item)
            else:
                temp=getattr(SYMTAB['__OBJECT_INSTANCES__'][objname],item)
            #print 'temp: %s' %temp
            objname=temp
        return [objname,field]

def findObjectFieldFromInst(inst,acc_string):
    #print 'En findObjectFieldFromInst: %s' %acc_string
    #print inst
    instance=inst
    retval=[]
    elems=acc_string.split('.')
    #print elems
    for el in elems:
        inst=getattr(inst,el)
        #print inst
    return inst
     

#Funcion de utilidad que lee un archivo de texto o una url
def getPathText(path,getlines=0):
    if path.lower().find('http://')==0:
        if getlines==0:
            #print 'Descargando url: %s' % path
            return urllib.urlopen(path).read()
        else:
            return urllib.urlopen(path).read().split('\r\n') 
    else:
        if getlines==0:
            if os.path.exists(path) and os.path.isfile(path):
                return open(path,'r').read()
            else:
                return path
        else:
            if os.path.exists(path) and os.path.isfile(path):
                return open(path,'r').readlines()
            else:
                return path


#Funcion que evalua una operacion y devuelve el resultado con control de tipos
def performOperation(arg1,op,arg2=None):
    #print 'arg1: %s' %arg1
    #print 'op : %s' %op
    #print 'arg2: %s' % arg2
    if op=='-' and arg2==None: #uminus
        if type(arg1) in [type(2),type(2L),type(2.0)]:
            return -arg1
        else:
            raise Exception('Error: Solo se puede usar el menos unario con numeros.')
    elif op=='+': #cuidadin con los tipos!
        #Control de tipos: puedo sumar numeros y cadenas, numeros y numeros
        #numeros y cadenas,listas y listas y dicts y dicts
        if type(arg1)in [type(''),type(u'')] and type(arg2) in [type(''),type(u'')]:
            #Dos cadenas: el resultado es una cadena
            return str(arg1) + str(arg2)
        elif type(arg1) in [type(''),type(u'')] and type(arg2) in [type(2),type(2L),type(2.0)]:
            #Si alguno es una cadena, el resultado es una cadena
            return str(arg1) + str(arg2)
        elif type(arg1) in [type(2),type(2L),type(2.0)] and type(arg2) in [type(''),type(u'')]:
            #Si alguno es una cadena, el resultado es una cadena
            return str(arg1) + str(arg2)        
        elif type(arg1)in [type(2),type(2L),type(2.0)] and type(arg2) in [type(2),type(2L),type(2.0)]:
            #Si son dos numeros, el resultado es un float
            #return float(arg1 + arg2)
            return arg1 + arg2
        elif type(arg1)==type([]) and type(arg2)==type([]):
            #Dos listas se suman
            return arg1 + arg2
        elif type(arg1)==type([]) and type(arg2)!=type([]):
            #Una lista mas cualquier cosa: se pone en la lista
            arg1.append(arg2)
            return arg1
        elif type(arg2)==type([]) and type(arg1)!=type([]):
            #Una cosa mas una lista: se pone la cosa al principio de la lista
            arg2.insert(0,arg1)
            return arg2         
        elif type(arg1)==type({}) and type(arg2)==type({}):
            #Dos diccionarios: se combinan
            arg1.update(arg2)
            return arg1
        else: #Todo lo demas genera una excepcion
            raise Exception('Error: tipos incompatibles "%s" y "%s" para el operador "+"'%(type(arg1),type(arg2)))
                            
    elif op=='-': #cuidadin con los tipos!
        if type(arg1)in [type(2),type(2L),type(2.0)] and type(arg2) in [type(2),type(2L),type(2.0)]:
            #Si son dos numeros, el resultado es un float
            #return float(arg1 - arg2)
            return arg1 - arg2
        elif type(arg1)==type([]) and type(arg2)==type([]):
            #Dos listas: devolver elementos de la primera que no esten en la segunda
            resul=[]
            for el in arg1:
                if el not in arg2:
                    resul.append(el)
            return resul
        elif type(arg1)==type([]) and type(arg2)!=type([]):
            #Lista - otro: si otro in lista, borrarlo, si no, excepcion
            if arg2 in arg1:
                del arg1[arg1.index(arg2)]
                return arg1
            else:
                raise Exception('Error: El operador "-" elimina un elemento de la lista solo si existe en ella')
        elif type(arg1)==type({}) and type(arg2)==type({}):
            #Dos diccionarios: devolver otro que es dic1 sin las claves de dic2
            resul=copy.deepcopy(arg1)
            for el in arg2:
                if resul.has_key(el):
                    del resul[el]
            return resul
        elif type(arg1)==type({}) and type(arg2)!=type({}):
            #Dict - otro: si otro in dict, borrarlo, si no, excepcion
            if arg2 in arg1:
                del arg1[arg2]
                return arg1
            else:
                raise Exception('Error: El operador "-" elimina un elemento de un diccionario solo si existe en el')        
        else: #Todo lo demas genera una excepcion
            raise Exception('Error: tipos incompatibles "%s" y "%s" para el operador "-"'%(type(arg1),type(arg2)))


    elif op=='*': #cuidadin con los tipos!
        if type(arg1)in [type(2),type(2L),type(2.0)] and type(arg2) in [type(2),type(2L),type(2.0)]:
            #Si son dos numeros, el resultado es un float
            #return float(arg1 * arg2)
            return  arg1 * arg2
        elif type(arg1) in [type(''), type(u'')] and type(arg2) in [type(2),type(2L),type(2.0)]:
            #string * numero: repetir numero veces el string
            return arg1 * int(arg2)        
        elif type(arg1)==type([]) and type(arg2) in [type(2),type(2L),type(2.0)]:
            #lista * numero: repetir numero veces la lista
            return arg1 * int(arg2)
        else: #Todo lo demas genera una excepcion
            raise Exception('Error: tipos incompatibles "%s" y "%s" para el operador "*"'%(type(arg1),type(arg2)))


    elif op=='/': #cuidadin con los tipos!
        if type(arg1)in [type(2),type(2L),type(2.0)] and type(arg2) in [type(2),type(2L),type(2.0)]:
            #Si son dos numeros, el resultado es un float
            return float(arg1)/float(arg2)#?????????????
        else: #Todo lo demas genera una excepcion
            raise Exception('Error: tipos incompatibles "%s" y "%s" para el operador "/"'%(type(arg1),type(arg2)))




#Funcion que evalua una S-expresion
def eval_sexpr(sexpr):
    if not 'java' in OSSYSTEM:
        interp = pyscheme.scheme.AnalyzingInterpreter()
        return interp.eval(pyscheme.parser.parse(sexpr))
    else:
        x=lispy.parse(sexpr)
        if x is lispy.eof_object: return ''
        val=lispy.eval(x)
        return lispy.to_string(val)        

def eval_sexpr_backup(sexpr):
    #print SYMTAB
    x=lispy.parse(sexpr)
    if x is lispy.eof_object: return ''
    val=lispy.eval(x)
    return lispy.to_string(val)

def eval_pcode(pcodew):
    #Obtenemos la pila completa del interprete Forth ??
    mini_forth.tokenizeWords2(pcodew.strip())
    mini_forth.main2()
    return mini_forth.ds

#Mapa de operadores y funciones del modulo operator
operators_map={
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '**': operator.pow
}        


#True si un campo es privado o publico
def isPrivate(objn,fldn):
    flds=[]
    if isinstance(objn,MiniObject):
        flds= objn.getFields()
    else:
        flds= SYMTAB['__OBJECT_INSTANCES__'][objn].getFields()
    for f in flds:
        if f[0]==fldn:
            if f[1]=='private':
                return 1
    return 0

#Buscar un id. Devuelve una lista con la instancia y su tipo
def findId(id):
    #print 'Buscando identificador: %s' %id
    #print SYMTAB['__OBJECT_INSTANCES__']
    #print TYPESTAB
    if id not in TYPESTAB:
        raise Exception('Error: El identificador "%s" no esta definido'%id)
    if TYPESTAB[id]=='t_null':
        return [id,'t_null']
    elif id in SYMTAB['__OBJECT_INSTANCES__']:
        return [SYMTAB['__OBJECT_INSTANCES__'][id],TYPESTAB[id]]
    else:
        return [SYMTAB[mini_tdas[TYPESTAB[id]]][id],TYPESTAB[id]]

#Busca si un id es valido
def isValidId(id):
    if not id in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%id)
    else:
        return 1
    
#Busca si una variable es estatica
def isStaticVar(name):
    if name in SYMTAB['__STATICS__']:
        return 1
    else:
        return 0
    
#Chequea si una variable estatica es valida
def isValidStatic(name):
    if SYMTAB['__CURRENT_FUNCTION__']=='':
        raise Exception('Error: La variable "%s" es estatica y no se puede usar fuera de la funcion en la que se ha definido'%name)
    else:
        if SYMTAB['__FUNC_STATICS__'].has_key(SYMTAB['__CURRENT_FUNCTION__']):
            if name in  SYMTAB['__FUNC_STATICS__'][SYMTAB['__CURRENT_FUNCTION__']]:
                return 1
        else:
            raise Exception('Error: La variable estatica "%s" no esta definida en la funcion "%s"'%(name,SYMTAB['__CURRENT_FUNCTION__']))


def checkInstanceType(exp_list,template_list,kind):
    #print 'Comprobando tipos:'
    if type(template_list)==type([]):
        if kind==1: #choice of vals
            for el in template_list:
                #print 'Comnprobando: %s' %el
                if exp_list==el:
                    correct=1
                    break
        else:#tipo compuesto
            for i in range(len(exp_list)):
                #print 'Comprobando: %s' %exp_list[i]
                if type(exp_list[i]) in [type(0),type(0L),type(0.0)] and not template_list[i]=='t_numeric':
                    raise Exception('Error comprobando tipos: se esperaba "%s" para "%s"'%(template_list[i],exp_list[i]))
                elif  exp_list[i] in TYPESTAB: #Comprobar que los tipos de los IDs coinciden exactamente
                    if template_list[i]!=TYPESTAB[exp_list[i]]:
                        raise Exception('Error comprobando tipos: se esperaba "%s" para "%s"'%(template_list[i],exp_list[i]))
                elif type(exp_list[i]) in [type(''),type(u'')]and not template_list[i]=='t_string':
                    raise Exception('Error comprobando tipos: se esperaba "%s" para "%s"'%(template_list[i],exp_list[i]))
    elif type(template_list) in [type(''),type(u'')]:
        if len(exp_list)!=1:
            raise Exception('Error creando instancia de tipo: Un tipo variante solo pude tener un parametro')
        exp_list=exp_list[0]
        correct=0
        if kind==2: #choice of types
            choices=template_list.split('|')
            for el in choices:
                #print 'Comnprobando: %s' %el
                if type(exp_list) in [type(0),type(0L),type(0.0)] and el=='t_numeric':
                    correct=1
                    break
                elif exp_list in TYPESTAB:
                    if el==TYPESTAB[exp_list]:
                        correct=1
                        break
                elif type(exp_list) in [type(''),type(u'')]and el=='t_string':
                    correct=1
                    break
        if correct==0:
            raise Exception('Error: "%s" no se corresponde con ninguno de los tipos alternativos "%s"'%(exp_list,choices))




def listMatchType(lst,template,kind):
    #print 'Entrando a ListMatchType con:'
    #Valor para diferenciar el tipo de typedef:0:compuesto,1:choice of vals,2:choice of types,3:list(array) of type(???)
    #print lst
    #print template
    #print 'kind: %s' % kind
    if kind!=1 and type(lst)!=type([]):
        raise Exception('Error: "%s" no es una lista y tiene que serlo'%lst)
    #print SYMTAB['__TYPEDEFS__']
    #Proceder segun kind y template
    if kind==1: #Pertenencia a la lista del tipo (trivial)
        if type(lst) in [type(''),type(u'')]:
            #print 'por el if'
            if lst in template:
                return 1
            else:
                #Cambio serio. Permitimos que t_string funcione tb como expresion regular!!!!--------
                for t in template:
                    #print 'probando en el if %s' % t
                    try:
                        if re.match(t,lst):
                            return 1
                    except:
                        return 0
                #Fin cambio--------------------------------------------------------------------------
                return 0
        else:
            #Si es una lisa tienen que encajar todos!
            #print 'por el else'
            for el in lst:
                #print 'el: %s' %el
                if not el in template:
                    #Cambio serio. Permitimos que t_string funcione tb como expresion regular!!!!--------
                    for t in template:
                        #print 'probando %s' % t
                        try:
                            #print re.match(t,el)
                            if not re.match(t,el):
                                continue
                            else:
                                return 1
                        except:
                            #print 'error en regexp!!!'
                            return 0
                    #print 'me salgo del bucle!'
                    return 0
                    #Fin cambio--------------------------------------------------------------------------                
            return 1
    elif kind==0: #tipo compuesto o alias
        if len(lst)>len(template) or len(lst)==1: #Hay que encajar toda la lista
            #print 'probando lista entera: %s'%lst
            tipo=elems=None
            if template[0] not in ['t_numeric','t_string']: ##ESTO SE HA CAMBIADO PARA LA CREACION DE TIPOS-LISTA!!
                tipo,elems=SYMTAB['__TYPEDEFS__'][template[0]]
            #print 'llamada recursiva!'
            #print 'probando "%s" con "%s"'%(lst,str(elems))
            if not listMatchType(lst,elems,tipo):
                #print 'No encaja con nada en el if de k0'
                return 0
            #print 'Encaja con %s en el if de k0'%str(elems)
            return 1
        else:
            for i in range(len(template)):
                #print 'probando elemento: %s'%lst[i]
                if type(lst[i]) in [type(0),type(0L),type(0.0)] and template[i]=='t_numeric':
                    #print '"%s" encaja en t_numeric en k0'%lst[i]
                    continue
                if type(lst[i]) in [type(''),type(u'')] and template[i]=='t_string':
                    #print '"%s" encaja en t_string en k0'%lst[i]
                    continue
                if template[i] not in ['t_numeric','t_string']:
                    tipo,elems=SYMTAB['__TYPEDEFS__'][template[i]]
                    #print 'llamada recursiva!'
                    #print 'probando "%s" con "%s" en k0'%(lst[i],str(elems))
                    if not listMatchType(lst[i],elems,tipo):
                        #print 'No encaja con nada en k0'
                        return 0
                    #print 'Encaja con %s en k0'%str(elems)
                else:
                    #print 'no encaja, no en k0'
                    return 0
            return 1
    elif kind==2: #Uno de varios tipos posibles. Probar TODA la lista. Si alguno coincide, verdadero
        for i in range(len(template)):
            #print 'probando elemento: %s con %s'%(lst,template[i])
            if len(lst)==1 and type(lst[0]) in [type(0),type(0L),type(0.0)] and template[i]=='t_numeric':
                #print '"%s" encaja en t_numeric en k2'%lst[0]
                return 1
            if len(lst)==1 and type(lst[0]) in [type(''),type(u'')] and template[i]=='t_string':
                #print '"%s" encaja en t_string en k2'%lst[0]
                return 1
            if template[i] not in ['t_numeric','t_string']:
                #print 'llamada recursiva!'
                #print 'probando "%s" con "%s" y tipo "%s"'%(lst,[template[i]],0)
                if listMatchType(lst,[template[i]],0):
                    #print 'Encaja via or con %s en k2'%template[i]
                    #print 'saliendo'
                    return 1  

    elif kind==3: #Array de un tipo. Probar que todos los elementos tienen el mismo tipo
        tipo=None
        if template[0] not in ['t_numeric','t_string']:
            tipo=SYMTAB['__TYPEDEFS__'][template[0]][0]
        for i in range(len(lst)):
            #print 'probando elemento: %s con %s y kind 3'%(lst[i],template[0])
            #trivial: t_numeric
            if template[0]=='t_numeric' and not type(lst[i]) in [type(0),type(0L),type(0.0)]:
                return 0
            #trivial: t_string
            if template[0]=='t_string' and not type(lst[i]) in [type(''),type(u'')]:
                return 0
            #recursivo:
            if template[0] not in ['t_numeric','t_string']:
                it=lst[i]
                #print 'it: %s' % it
                #print type(lst[i])
                if type(lst[i])!=type([]):
                    it=lst
                #print 'it: %s' % it
                #print 'tipo: %s' % tipo
                #Ojo, cambio para si tipo del template es 1, pasar la lista de opciones
                tplt=SYMTAB['__TYPEDEFS__'][template[0]][1] if tipo==1 else [template[0]]
                if not listMatchType(it,tplt,tipo):
                   return 0
        return 1;
    return 0


def listMatchType_backup(lst,template,kind):
    #print 'Entrando a ListMatchType con:'
    #Valor para diferenciar el tipo de typedef:0:compuesto,1:choice of vals,2:choice of types,3:list(array) of type(???)
    #print lst
    #print template
    #print 'kind: %s' % kind
    if kind!=1 and type(lst)!=type([]):
        raise Exception('Error: "%s" no es una lista y tiene que serlo'%lst)
    #print SYMTAB['__TYPEDEFS__']
    #Proceder segun kind y template
    if kind==1: #Pertenencia a la lista del tipo (trivial)
        if type(lst) in [type(''),type(u'')]:
            if lst in template:
                return 1
            else:
                return 0
        else:
            if lst[0] in template:
                return 1
            else:
                return 0
    elif kind==0: #tipo compuesto o alias
        if len(lst)>len(template) or len(lst)==1: #Hay que encajar toda la lista
            #print 'probando lista entera: %s'%lst
            tipo=elems=None
            if template[0] not in ['t_numeric','t_string']: ##ESTO SE HA CAMBIADO PARA LA CREACION DE TIPOS-LISTA!!
                tipo,elems=SYMTAB['__TYPEDEFS__'][template[0]]
            #print 'llamada recursiva!'
            #print 'probando "%s" con "%s"'%(lst,str(elems))
            if not listMatchType(lst,elems,tipo):
                #print 'No encaja con nada en el if de k0'
                return 0
            #print 'Encaja con %s en el if de k0'%str(elems)
            return 1
        else:
            for i in range(len(template)):
                #print 'probando elemento: %s'%lst[i]
                if type(lst[i]) in [type(0),type(0L),type(0.0)] and template[i]=='t_numeric':
                    #print '"%s" encaja en t_numeric en k0'%lst[i]
                    continue
                if type(lst[i]) in [type(''),type(u'')] and template[i]=='t_string':
                    #print '"%s" encaja en t_string en k0'%lst[i]
                    continue
                if template[i] not in ['t_numeric','t_string']:
                    tipo,elems=SYMTAB['__TYPEDEFS__'][template[i]]
                    #print 'llamada recursiva!'
                    #print 'probando "%s" con "%s" en k0'%(lst[i],str(elems))
                    if not listMatchType(lst[i],elems,tipo):
                        #print 'No encaja con nada en k0'
                        return 0
                    #print 'Encaja con %s en k0'%str(elems)
                else:
                    #print 'no encaja, no en k0'
                    return 0
            return 1
    elif kind==2: #Uno de varios tipos posibles. Probar TODA la lista. Si alguno coincide, verdadero
        for i in range(len(template)):
            #print 'probando elemento: %s con %s'%(lst,template[i])
            if len(lst)==1 and type(lst[0]) in [type(0),type(0L),type(0.0)] and template[i]=='t_numeric':
                #print '"%s" encaja en t_numeric en k2'%lst[0]
                return 1
            if len(lst)==1 and type(lst[0]) in [type(''),type(u'')] and template[i]=='t_string':
                #print '"%s" encaja en t_string en k2'%lst[0]
                return 1
            if template[i] not in ['t_numeric','t_string']:
                #print 'llamada recursiva!'
                #print 'probando "%s" con "%s" y tipo "%s"'%(lst,[template[i]],0)
                if listMatchType(lst,[template[i]],0):
                    #print 'Encaja via or con %s en k2'%template[i]
                    #print 'saliendo'
                    return 1  

    elif kind==3: #Array de un tipo. Probar que todos los elementos tienen el mismo tipo
        tipo=None
        if template[0] not in ['t_numeric','t_string']:
            tipo=SYMTAB['__TYPEDEFS__'][template[0]][0]
        for i in range(len(lst)):
            #print 'probando elemento: %s con %s y kind 3'%(lst[i],template[0])
            #trivial: t_numeric
            if template[0]=='t_numeric' and not type(lst[i]) in [type(0),type(0L),type(0.0)]:
                return 0
            #trivial: t_string
            if template[0]=='t_string' and not type(lst[i]) in [type(''),type(u'')]:
                return 0
            #recursivo:
            if template[0] not in ['t_numeric','t_string']:
                it=lst[i]
                if type(lst[i])!=type([]):
                    it=lst
                if not listMatchType(it,[template[0]],tipo):
                   return 0
        return 1;
    return 0



#Variables temporales globales para pasar informacion de unos niveles de pila a otros---------
temporal=[]
obj=None
clsname=''
basetypes=''
#-------------------------------------------------------------------------------------------


#Variables temporales globales para SELECT y HTML-------------------------------------------
html_text=''
html_attrs={}
#-------------------------------------------------------------------------------------------


#Reglas de precedencia de operadores
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIV'),
    ('right','UMINUS'),
    )

def p_program(t):
    '''program : definitions_sect order_list'''
    #print 'Llegamos a nivel de programa'
    #print SYMTAB['__USER_NAMESPACES__']
    t[0]=t[1]
    ##print str(lexer)


##Cambios para soportar definiciones de objetos#######################
    
def p_definitions_sect(t):
    '''definitions_sect : object_definition 
    | empty'''
    t[0]=t[1]


def p_object_definition(t):
    '''object_definition : begin_class class_name EXTENDS base_type COLON field_list end_class object_definition
    | begin_class class_name EXTENDS base_type COLON field_list end_class'''
    global temporal
    #print 'Dentro de object_definition'
    obj_name=t[2].strip("'")
    
    ##print 'Nombre del objeto definido: %s' % obj_name   
    temporal=[]
    t[0]=t[1]


def p_begin_class(t):
    '''begin_class : CLASS'''
    ##print 'ENTRANDO EN BEGIN CLASS'
    t[0]=t[1]



def p_class_name(t):
    '''class_name : ID'''
    global clsname
    ##print 'ENTRANDO EN CLASS_NAME: %s'%t[1]
    clsname=t[1]
    t[0]=t[1]


def p_base_type(t):
    '''base_type : id_list
    | OBJECT'''
    global basetypes
    basetypes=t[1]
    ##print '\nVALOR DE basetypes: %s\n' %basetypes
    t[0]=t[1]
    



def p_field_list(t):
    '''field_list : ID COLON ID SEMI field_list
    | ID COLON ID SEMI
    | empty'''
    global temporal
    ##print 'Dentro de field_list'
    if t[1]:
        fname=t[1].strip("'")
        ftype=t[3].strip("'")
        ##print 'Nombre del campo: %s' % fname
        ##print 'Tipo del campo: %s' % ftype
        #Solo se admiten tipos simples en los campos (numeric,string,any,reference??)Generar una excepcion si no es uno de estos
        #if ftype not in ['string','numeric','any']: #'reference'] ??
        #if ftype not in SYMTAB['__BASIC_TYPES__']:
        #    raise Exception('Error: El tipo "%s" no es valido. Los campos de objeto solo pueden ser de uno de los tipos primitivos definidos.' %ftype)
        if ftype not in ['public','private']:
            raise Exception('Error: El tipo "%s" no es valido. Los campos de objeto solo pueden ser "public" o "private".' %ftype)    
        temporal.append((fname,ftype))
        t[0]=temporal
        ##print 'Valor de t[0] en p_field_list: %s' %str(t[0])
    else:
        t[0]=0

    

def p_end_class(t):
    '''end_class : ENDCLASS'''
    global temporal
    global obj
    global clsname
    global basetypes
    t[0]=t[1]
    ##print '\n\nEstamos en end_class y temporal vale %s\n\n' % str(temporal)
    
    ###Dar de alta el objeto definido en la tabla de simbolos---------------------------------------
    obj_name=clsname.strip("'")
    #1.- Dar de alta el tipo como tipo existente o lanzar una excepcion si ya se tiene
    if not obj_name in SYMTAB['__DEFINED_TYPES__']:
        SYMTAB['__DEFINED_TYPES__'].append(obj_name)
    else:
        raise Exception('Error: El tipo %s ya existe!!!' % obj_name)

    #3.- Crear un objeto MiniObjectInfo con la informacion del tipo y guardarlo
    info=MiniObjectClass()
    info.name=obj_name
    temporal.reverse() #Los campos en temporal estan en orden inverso a su definicion!!
    ##print 'basetypes:%s' %str(basetypes)
    ##print type(basetypes)
    info.fields_names=temporal
    if type(basetypes)==type(''):
        #basetypes=[basetypes]
        basetypes=basetypes.split(',')
    #print 'basetypes:%s' %str(basetypes)
    info.bases=[el.strip("'") for el in basetypes]
    ##print SYMTAB['__DEFINED_TYPES__']
    ##HERENCIA DE PROTOTIPOS------------------------------------------------------
    #Copiar los campos de las bases (heredarlos)si no es object
    #EN EL ORDEN DE SU DEFINICION.SE HEREDAN AL FINAL LOS ULTIMOS DE LA CADENA DE BASES.
    #SI ALGUNO COINCIDE SE SUSTITUYE POR LA ULTIMA
    for base in info.bases:
        if not base in SYMTAB['__DEFINED_TYPES__']:
            raise Exception('Error: El tipo "%s" no existe' % base)
        else:
            if base!='object':  # not in ['numeric','string','object','reference']:
                new_fields=SYMTAB['__DEFINED_OBJECTS__'][base].fields_names
                for field in new_fields:
                    if not field in info.fields_names:
                        info.fields_names.append(field)
                ##print 'ANYADIDOS CAMPOS DE %s' % base
    ##-----------------------------------------------------------------------------
        

    ##print 'Nombre de info: %s\n\n' %str(info.name)
    ##print 'Contenido de info: %s\n\n' %str(info.fields_names)
    SYMTAB['__DEFINED_OBJECTS__'][obj_name]=info
    ###----------------------------------------------------------------------------------------------
    
    temporal=[]
    clsname=''
    obj=None
    basetypes=''


def p_order_list(t):
    '''order_list : valid_st SEMI
    | valid_st SEMI order_list'''
    ##print 'alcanzada order_list'
    t[0]=t[1]
    ##print 't[0] en order_list %s' % t[0]


def p_valid_st(t):
    '''valid_st : condic_expr
    | id_assign_exp
    | assign_exp
    | create_obj_st
    | destroy_st
    | shared_st
    | extension_st
    | list_definition_st
    | dict_definition_st
    | instance_definition_st
    | tree_definition_st
    | enum_definition_st
    | matrix_definition_st
    | graph_definition_st
    | iter_definition_st
    | iterator_expr
    | itertolist_st
    | xml_st
    | html_st
    | incr_st
    | prolog_st
    | consult_st
    | sexpr_st
    | pcode_st
    | kb_definition_st
    | rule_definition_st
    | symbolic_st
    | com_st
    | empty
    | apply_st
    | code_definition_st
    | runtemplate_st
    | pipe_definition_st 
    | pipeline_st 
    | enter_leave_st  
    | setvar_st
    | func_inst_st
    | set_static_st
    | id_st
    | typedef_st
    | typeinst_st
    | typeget_st
    | typeset_st
    | linqlike_st
    | list_add_st
    | list_expr_st
    | sql_st
    | assert_st   
    '''
    global listexp_from_expr#???????
    t[0]=t[1]
    #print 'En valid_st: %s'%t[0]
    SYMTAB['_']=t[0]
    #print SYMTAB['_']
    #resetear flag de expresiones con listas
    if listexp_from_expr!=0:
      #print 'puesto flag a cero!!!'''
      listexp_from_expr=0
      
      

def p_assert_st(t):
    '''assert_st : ASSERT condic_expr OR RAISE expr'''
    #print 'en assert: %s'%t[2]
    if not t[2]:
        if type(t[5]) not in [type(''),type(u'')]:
            raise Exception('Error: "%s" no es una cadena de texto')
        raise Exception(t[5])
    t[0]=t[2]


def p_typedef_st(t):
    '''typedef_st : TYPEDEF ID AS types_list
    | TYPEDEF ID AS options_list
    | TYPEDEF ID AS LIST LBRACK expr_list RBRACK
    | TYPEDEF ID AS LIST FROM ID
    '''
    #Valor para diferenciar el tipo de typedef:0:compuesto,1:choice of vals,2:choice of types,3:list of types
    global types_list
    global options_list
    global params_list
    global type_choice,type_listof
    #print 'types_list: %s' % types_list
    #Solo se puden definir tipos en el toplevel
    if not SYMTAB['__CURRENT_FUNCTION__']=='':
        raise Exception('Error: No esta permitido definir tipos en una funcion de usario')
    #Comprobar que empieza por "t_" (obligatorio para todos los tipos definidos por el usuario o primitivos, no para clases)
    if t[2][:2]!='t_':
        raise Exception('Error: el tipo "%s" no es valido. Todos los nombres de tipos deben comenzar por "t_"'%t[2])
    #Comprobar que no esta repetido
    if t[2] in SYMTAB['__TYPEDEFS__'] or t[2] in SYMTAB['__BASIC_TYPES__']:
        raise Exception('Error: el tipo "%s" ya esta definido'%t[2])
    if len(t)==8:
        params_list.reverse()
        #print params_list
        SYMTAB['__TYPEDEFS__'][t[2]]=(1,params_list)
        params_list=[]
    elif len(t)==7:
        print "construyendo un array"
        SYMTAB['__TYPEDEFS__'][t[2]]=(3,[t[6]])
        if t[2]==t[6]:
            raise Exception('Error: No se admiten definiciones recursivas ("%s" en terminos de "%s"'%(t[2],t[6]))
        if t[6] not in SYMTAB['__BASIC_TYPES__']:
            if t[6] not in SYMTAB['__TYPEDEFS__']:
                raise Exception('Error: El tipo "%s" no esta definido.' %t[6])
        #print SYMTAB['__TYPEDEFS__']
    else:
        if type_choice==1:
            #Comprobar que todos son tipos validos
            for el in options_list:
                if el not in SYMTAB['__BASIC_TYPES__']:
                    if el not in SYMTAB['__TYPEDEFS__']:
                        raise Exception('Error: El tipo "%s" no esta definido.' %el)
            #SYMTAB['__TYPEDEFS__'][t[2]]=(2,'|'.join(options_list))
            SYMTAB['__TYPEDEFS__'][t[2]]=(2,options_list[:])            
            #Resetear types_list
            options_list=[]
            type_choice=0
        else:
            #Comprobar que todos son tipos validos
            for el in types_list:
                if el not in SYMTAB['__BASIC_TYPES__']:
                    if el not in SYMTAB['__TYPEDEFS__']:
                        raise Exception('Error: El tipo "%s" no esta definido.' %el)        
            #Dar de alta el tipo
            #SYMTAB['__BASIC_TYPES__'].append(t[2]) ?????
            if len(types_list)>1:
                types_list.reverse()
            SYMTAB['__TYPEDEFS__'][t[2]]=(0,types_list)
            #Resetear types_list
            types_list=[]
    t[0]='1'

def p_types_list(t):
    '''types_list : ID COMMA types_list
    | ID COMMA ID
    | ID'''
    global types_list
    if len(t)==2:
        types_list.append(t[1])
    elif type(t[3])!=type([]):#Ojo al orden!!
        types_list.append(t[3])
        types_list.append(t[1])
    else:
        types_list.append(t[1])
    t[0]=types_list


def p_options_list(t):
    '''options_list : type_expr_elem OR options_list
    | type_expr_elem OR type_expr_elem'''
    global options_list
    global type_choice
    type_choice=1
    if type(t[3])!=type([]):
        if t[1]==t[3]:
            raise Exception('Error: los tipos opcionales deben ser distintos')
        options_list.append(t[3])
        options_list.append(t[1])
    else:
        options_list.append(t[1])
    t[0]=options_list     
    
    
def p_typeinst_st(t):
    '''typeinst_st : ID EQUAL NEW ID list_exp_oper'''
    if not t[1] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[1])
    #print 'En la forma alternativa de typeinst!!!'
    #print SYMTAB['__TYPEDEFS__']
    if not t[4] in SYMTAB['__TYPEDEFS__']:
         if not t[4] in SYMTAB['__BASIC_TYPES__']:
            raise Exception('Error: el tipo "%s" no esta definido'%t[4])
    kind,tplist=SYMTAB['__TYPEDEFS__'][t[4]]
    #print tplist
    if type(tplist)==type([]):
        if kind==0:
            if len(t[5])!=len(tplist):
                raise Exception('Error: Los argumentos de la definicion de la instancia "%s" no coinciden con los de la definicion del tipo "%s"' % (type_exprs,tplist))
    #Cambio:Comprobamos igual que en los condicionales
    if not listMatchType(t[5],tplist,kind):
        raise Exception('Error: Los argumentos no coinciden con los de la plantilla del tipo-lista')
    
    #Todo bien, dar de alta la instancia----------
    SYMTAB['__TYPE_INSTANCES__'][t[1]]=t[5]
    TYPESTAB[t[1]]=t[4]
    #---------------------------------------------
    #print SYMTAB['__TYPE_INSTANCES__']
    #print TYPESTAB
    t[0]='1'    
    t[0]=1


def p_type_expr_elem(t):
    '''type_expr_elem : ID
    | expr'''
    #print 'Creado elemento de expresion de tipo'
    #print 'Con t[1]: %s' %t[1]
    #Si es un id que corresponda a una lista, sustituirlo por su valor
    if type(t[1]) in [type(''),type(u'')] and t[1] in SYMTAB['__LISTS__']:
        t[0]=SYMTAB['__LISTS__'][t[1]]
    elif type(t[1]) in [type(''),type(u'')] and t[1] in SYMTAB['__TYPE_INSTANCES__']:
        t[0]=SYMTAB['__TYPE_INSTANCES__'][t[1]]
    else:
        t[0]=t[1]


def p_typeget_st(t):
    '''typeget_st : GET LBRACK typeget_list RBRACK FROM ID'''
    #1.- Asegurarse de que existe el id
    if not t[6] in SYMTAB['__TYPE_INSTANCES__']:
        raise Exception('Error: La instancia de tipo "%s" no esta definida'%t[6])
    instlist=SYMTAB['__TYPE_INSTANCES__'][t[6]]
    #print 'instlist: %s' %instlist
    global gettype_list
    gettype_list.reverse()
    #print 'gettype_list:%s' %gettype_list
    #2.- Ambas listas deben tener la misma longitud
    if len(gettype_list)!=len(instlist):
        raise Exception('Error de asignacion: La plantilla no tiene la misma longitud que la instancia "%s"' %t[6])
    #3.- Asignar variables
    for i in range(len(gettype_list)):
        if gettype_list[i]=='null': #Ignorar los null
            continue
        else: #asignar variables
            static=0
            if isStaticVar(gettype_list[i]) and isValidStatic(gettype_list[i]):
                static=1
            if static==0 and not SYMTAB.has_key(gettype_list[i]):
                raise Exception('Error: la variable "%s" no esta definida'%gettype_list[i])
            if static==1:
                 SYMTAB['__STATICS__'][gettype_list[i]]=instlist[i]
            else:
                  SYMTAB[gettype_list[i]]=instlist[i]
    gettype_list=[]
    t[0]='1'


def p_typeset_st(t):
    '''typeset_st : SET LBRACK typeget_list RBRACK IN ID'''
    #1.- Asegurarse de que existe el id
    if not t[6] in SYMTAB['__TYPE_INSTANCES__']:
        raise Exception('Error: La instancia de tipo "%s" no esta definida'%t[6])
    instlist=SYMTAB['__TYPE_INSTANCES__'][t[6]]
    #print 'instlist: %s' %instlist
    global gettype_list
    gettype_list.reverse()
    #print 'gettype_list:%s' %gettype_list
    #2.- Ambas listas deben tener la misma longitud
    if len(gettype_list)!=len(instlist):
        raise Exception('Error de asignacion: La plantilla no tiene la misma longitud que la instancia "%s"' %t[6])
    #3.- Asignar variables
    for i in range(len(gettype_list)):
        if gettype_list[i]=='null': #Ignorar los null
            continue
        else: #asignar variables
            static=0
            if isStaticVar(gettype_list[i]) and isValidStatic(gettype_list[i]):
                static=1
            if static==0 and not SYMTAB.has_key(gettype_list[i]):
                raise Exception('Error: la variable "%s" no esta definida'%gettype_list[i])
            if static==1:
                 instlist[i]=SYMTAB['__STATICS__'][gettype_list[i]]
            else:
                  instlist[i]=SYMTAB[gettype_list[i]]
    gettype_list=[]
    t[0]='1'
    

def p_typeget_list(t):
    '''typeget_list : getvalue COMMA typeget_list
    | getvalue'''
    global gettype_list
    gettype_list.append(t[1])
    t[0]='1'

def p_getvalue(t):
    '''getvalue : VAR
    | NULL'''
    t[0]=t[1]
   
    

def p_set_static_st(t):
    "set_static_st : SET STATIC ID DOT ID EQUAL expr"
    #print SYMTAB['__FUNC_STATICS__']
    if not t[3] in SYMTAB['__MACROS__']:
        raise Exception('Error: la funcion "%s" no esta definida'%t[3])
    if not '@'+t[5] in SYMTAB['__FUNC_STATICS__'][t[3]]:
        raise Exception('Error: la variable estatica "@%s" no esta definida en la funcion "%s"'%(t[5],t[3]))
    SYMTAB['__STATICS__']['@'+t[5]]=t[7]
    #print SYMTAB['__STATICS__']

def p_func_inst_st(t):
    "func_inst_st : ID EQUAL NEW FUNCTION ID"
    if t[1] in SYMTAB['__USED_IDS__']:
        raise Exception('Error: El identificador "%s" ya existe'%t[1]);
    if not t[5] in SYMTAB['__MACROS__']:
        raise Exception('Error: la funcion "%s" no esta definida'%t[5])
    SYMTAB['__USED_IDS__'].append(t[1])
    #print 'Instancia de funcion definida!!'
    parent=SYMTAB['__MACROS__'][t[5]]
    finfo={}
    finfo['code']=parent['code']
    #Decorar las variables estaticas
    #finfo['code']=re.sub('static\s+(@[A_Za-z0-9_]+)','static \\1' + '_' + t[1],finfo['code'])
    statics=re.findall('static\s+(@[A_Za-z0-9_]+)',finfo['code'])
    print statics
    if statics!=[]:
        if not t[1] in SYMTAB['__FUNC_STATICS__']:
            SYMTAB['__FUNC_STATICS__'][t[1]]=[]        
##        if not t[5] in SYMTAB['__FUNC_STATICS__']:
##            SYMTAB['__FUNC_STATICS__'][t[5]]=[]
    for var in statics:
        finfo['code']=finfo['code'].replace(var,'@' + t[1] + '_' + var[1:])
        SYMTAB['__FUNC_STATICS__'][t[1]].append('@' + t[1] + '_' + var[1:])
    #Si hay ocurrencias del nombre de la funcion (en un return),sustituirlas por el nuevo nombre
    finfo['code']=finfo['code'].replace('&' + parent['name'],'&'+t[1])
    #print finfo['code']
    finfo['name']=t[1]
    finfo['type']=parent['type']
    finfo['args']=parent['args']
    finfo['returns']=parent['returns']
    #print finfo
    #Darla de alta
    SYMTAB['__MACROS__'][t[1]]=finfo
    #Copiar las variables estaticas si las tiene??
    
    #Y crear una entrada en SYMTAB
    SYMTAB['&' + t[1]]=SYMTAB['__NULL__']
    #print SYMTAB['__MACROS__']
    t[0]=t[1]


def p_id_st(t):
    "id_st : ID"
    #print 'detectado un ID!!'
    isValidId(t[1])
    t[0]=t[1]

def p_setvar_st(t):
    '''setvar_st : SET varlist
    | GLOBAL varlist
    | STATIC VAR EQUAL expr
    | SET VAR EQUAL expr
    | SET id_list2
    | GLOBAL id_list2'''
    #Excepcion si la variuable ya existe!!!!!
    #Namespace temporal: entrada: [creadas,sustituidas]
    #print 'funcion actual: %s'% SYMTAB['__CURRENT_FUNCTION__']
    if len(t)==3 and not '@' in t[2]:
        idlist=t[2].split(',')
        if t[1]=='global':
           #print 'Estamos definiendo identificadores globales'
           for id in idlist:
               if id in TYPESTAB:
                   raise Exception('Error: el identificador "%s" ya esta definido'%id)
               TYPESTAB[id]='t_null'
               SYMTAB['__GLOBAL_IDS__'].append(id)
        else:
            #print 'Estamos definiendo identificadores'
            for id in idlist:
               if id in SYMTAB['__GLOBAL_IDS__']:
                   raise Exception('Error: El identificador "%s" se ha declarado global y no puede redefinirse'%id) 
               if id in TYPESTAB and SYMTAB['__CURRENT_FUNCTION__']=='':
                   raise Exception('Error: el identificador "%s" ya esta definido'%id)
                #Sustituir por los id locales
               if SYMTAB['__ID_NAMESPACES__'] and SYMTAB['__CURRENT_ID_NAMESPACE__']:
                    #print 'Definimos identificadores locales!!'
                    #print TYPESTAB
                    if not id in SYMTAB['__ID_NAMESPACES__'][SYMTAB['__CURRENT_ID_NAMESPACE__']][0]:
                        SYMTAB['__ID_NAMESPACES__'][SYMTAB['__CURRENT_ID_NAMESPACE__']][0].append(id)
                    if id in TYPESTAB: #Guardar valor antiguo y su tipo
                        SYMTAB['__ID_NAMESPACES__'][SYMTAB['__CURRENT_ID_NAMESPACE__']][1][id]=findId(id)
                    #print 'namespace local para ids:%s' % SYMTAB['__ID_NAMESPACES__'][SYMTAB['__CURRENT_ID_NAMESPACE__']]
               TYPESTAB[id]='t_null'            
        #print TYPESTAB
        #print SYMTAB['__GLOBAL_IDS__']
    if len(t)==5:
        if t[1]=='static': # and not t[2] in SYMTAB['__STATICS__']: #definir por primera y unica vez
            #Las variables estaticas se definen en una tabla global. No se permite
            #repetir nombres aun en funciones diferentes.Solo se pueden definir y usar dentro de
            #una funcion. Para cada funcion con variables estaticas hay una entrada que contiene
            #una lista con los nombres de variable asociados a esa funcion
            #print 'definiendo variable estatica'
            if SYMTAB['__CURRENT_FUNCTION__']=='':
                raise Exception('Error: Incorrecta definicion de la variable "%s". Las variables estaticas solo pueden declararse dentro de una funcion'%t[2])                 
            if not SYMTAB['__CURRENT_FUNCTION__'] in SYMTAB['__FUNC_STATICS__']:
                SYMTAB['__FUNC_STATICS__'][SYMTAB['__CURRENT_FUNCTION__']]=[]
            if t[2] not in SYMTAB['__FUNC_STATICS__'][SYMTAB['__CURRENT_FUNCTION__']]:
                #print 'creando la variable estatica %s'%t[2]
                SYMTAB['__FUNC_STATICS__'][SYMTAB['__CURRENT_FUNCTION__']].append(t[2])
            if not t[2] in SYMTAB['__STATICS__']: #Se inicializa al primer valor definido. El resto se ignora
                SYMTAB['__STATICS__'][t[2]]=t[4]
        else:
            if t[2] in SYMTAB['__GLOBALS__']:
                raise Exception('Error: La variable "%s" se ha declarado global y no puede redefinirse'%t[2])
            if SYMTAB['__NAMESPACES__'] and SYMTAB['__CURRENT_NAMESPACE__']:
                if not t[2] in SYMTAB['__NAMESPACES__'][SYMTAB['__CURRENT_NAMESPACE__']][0]:
                    SYMTAB['__NAMESPACES__'][SYMTAB['__CURRENT_NAMESPACE__']][0].append(t[2])
                if t[2] in SYMTAB:
                    SYMTAB['__NAMESPACES__'][SYMTAB['__CURRENT_NAMESPACE__']][1][t[2]]=SYMTAB[t[2]]
                #print SYMTAB['__NAMESPACES__']
            SYMTAB[t[2]]=t[4]
    else:
        #print t[2]
        isglobal=0
        if t[1]=='global': isglobal=1
        varlist=t[2].split(',')
        #print varlist
        for var in varlist:
            if var in SYMTAB['__GLOBALS__']:
                raise Exception('Error: La variable "%s" se ha declarado global y no puede redefinirse'%var)            
            #Sustituir por las locales
            if SYMTAB['__NAMESPACES__'] and SYMTAB['__CURRENT_NAMESPACE__']:
                if not var in SYMTAB['__NAMESPACES__'][SYMTAB['__CURRENT_NAMESPACE__']][0]:
                    SYMTAB['__NAMESPACES__'][SYMTAB['__CURRENT_NAMESPACE__']][0].append(var)
                if var in SYMTAB:
                    SYMTAB['__NAMESPACES__'][SYMTAB['__CURRENT_NAMESPACE__']][1][var]=SYMTAB[var]
                #print SYMTAB['__NAMESPACES__']            
            
            #print 'creando variable %s' %var
            SYMTAB[var]=SYMTAB['__NULL__']
            if isglobal==1:
                if SYMTAB['__NAMESPACES__'] and SYMTAB['__CURRENT_NAMESPACE__']:
                    raise Exception('Error definiendo variable "%s": Solo se permite definir variables globales fuera del ambito de las funciones'%var)
                #print 'guardando global %s' %var
                SYMTAB['__GLOBALS__'].append(var)

        #print 'globals: %s' %SYMTAB['__GLOBALS__']
    #print 'statics: %s' %SYMTAB['__STATICS__']
    t[0]=t[2]



def p_enter_leave_st(t):
    '''enter_leave_st : ENTER ID expr LEAVE
    | ENTER ID expr LEAVE IN ID'''
    if not t[2] in SYMTAB['__ENTER_EXTENSIONS__']:
        raise Exception('Error: "%s" no se corresponde con ninguno de los lenguajes soportados'%t[2]);
    code=t[3]
    table={}
    if len(t)==7: #Se ha pasado un diccionario para interactuar
        if t[2]=='java': #En java se puede pasar una lista o un diccionario
            if not t[6] in SYMTAB['__DICTIONARIES__']:
                if not t[6] in SYMTAB['__LISTS__']:
                    raise Exception('Error: "%s" no esta definido como lista o diccionario'%t[6])
            try:
                table=SYMTAB['__LISTS__'][t[6]]
            except:
                table=SYMTAB['__DICTIONARIES__'][t[6]]
        else: #Para el resto pasar un diccionario
            if not t[6] in SYMTAB['__DICTIONARIES__']:
                raise Exception('Error: el diccionario "%s" no esta definido'%t[6])
            table=SYMTAB['__DICTIONARIES__'][t[6]]
    if t[2]in ['vbscript','jscript']:
        if not 'win32' in OSSYSTEM:
            raise Exception('Las extensiones para usar VBScript y JavaScript solo estan disponibles en plataformas win32')
        #Crear una instancia del ScriptControl
        sc=win32com.client.Dispatch("ScriptControl")
        sc.Language = t[2]
        retval=None
        retval=sc.ExecuteStatement (code)
        if retval==None: retval=SYMTAB['__NULL__']
        #print 'retval: %s' % retval
    elif t[2]=='python':
        exec code in globals(),{t[6]:table}
    elif t[2]=='csharp':
        if 'java' in OSSYSTEM:
            raise Exception('Error: No se pueden usar extensiones para codigo .NET en plataformas Java')
        engine=dyncompiler2.CompileEngine(code)
        table['csharp']=engine.Run()
    elif t[2]=='vbnet':
        if 'java' in OSSYSTEM:
            raise Exception('Error: No se pueden usar extensiones para codigo .NET en plataformas Java')        
        engine=dyncompiler2.CompileEngine(code,dyncompiler2.LanguageType.VB,'Main')
        table['vbnet']=engine.Run()        
    elif t[2]=='java': #Janino via Jython o JPype
        if 'java' in OSSYSTEM:
            janino=miniutils.JaninoWrapper
            script=1
            keyw=['main','public','private','static','final']
            args=['']
            for k in keyw:
                if k in code:
                    if type(table)==type({}):
                        raise Exception('Error: Para este tipo de codigo java los argumentos deben pasarse como una lista')
                    args=jarray.array(table,java.lang.String)
                    janino.runClassBody(code,args)
                    script=0
                    break
            if script==1:
                if type(table)==type([]):
                    raise Exception('Error: Para este tipo de codigo java los argumentos deben pasarse como un diccionario')
                if table!={}:
                    argnames=table.keys()
                    args=table.values()
                    janino.runScript(code,argnames,args)
                else:
                    janino.runScript(code,[''],[''])
        if 'win32' in OSSYSTEM:
            if not SYMTAB['__JVM_LOADED__']==1:
                raise Exception('Error: No se ha cargado ninguna JVM. Para cargar una hay que llamar al interprete con la opcion "-j"')            
            janino=jpype.JPackage('miniutils').JaninoWrapper
            script=1
            keyw=['main','public','private','static','final']
            args=['']
            for k in keyw:
                if k in code:
                    if type(table)==type({}):
                        raise Exception('Error: Para este tipo de codigo java los argumentos deben pasarse como una lista')                    
                    args=jpype.JArray(jpype.java.lang.String,1)(table)
                    janino.runClassBody(code,args)
                    script=0
                    break
            if script==1:
                if type(table)==type([]):
                    raise Exception('Error: Para este tipo de codigo java los argumentos deben pasarse como un diccionario')                
                if table!={}:
                    argnames=table.keys()
                    args=table.values()
                    janino.runScript(code,argnames,args)
                else:
                    janino.runScript(code,[''],[''])
    t[0]=t[2]




def p_pipe_definition_st(t):
    '''pipe_definition_st : PIPELINE ID IS ID opt_listeners'''
    #Definicion de pipeline
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_pipeline','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_pipeline"'%(t[2],TYPESTAB[t[2]]))    
##    if t[2] in SYMTAB['__USED_IDS__']:
##        raise Exception('Error: El nombre "%s" ya existe'%t[2]);
    if not t[4] in SYMTAB['__CODES__']:
        raise Exception('Error: El codigo "%s" no esta definido'%t[4])
    #Comprobar que la lista de ids si existe son todos pipelines
    listeners=[]
    if t[5]!=None:
        listeners=t[5].split(',')
        for id in listeners:
            if not id in SYMTAB['__PIPELINES__']:
                raise Exception('Error: El identificador "%s" no corresponde a ningun pipeline definido.'%id)
    SYMTAB['__PIPELINES__'][t[2]]=MiniCoroutine(t[2],SYMTAB['__CODES__'][t[4]],listeners)
    SYMTAB['__USED_IDS__'].append((t[2]))
    TYPESTAB[t[2]]='t_pipeline'
    #print SYMTAB['__PIPELINES__']
    t[0]=t[2]


def p_pipeline_st(t):
    '''pipeline_st : ID COLON GT ID'''
    if not t[1] in SYMTAB['__ITERATORS__']:
        raise Exception('Error: El identificador "%s" no se corresponde con ningun iterador definido'%t[1]);
    if not t[4] in SYMTAB['__PIPELINES__']:
        raise Exception('Error: El identificador "%s" no se corresponde con ningun pipeline definido'%t[4]);
    #Enviar el iterador al pipeline(OJO, FALLA SI YA SE HA EMPEZADO EL ITERADOR)
    for i in range(len(SYMTAB['__ITERATORS__'][t[1]])):
        SYMTAB['__ITERATORS__'][t[1]].next()
        SYMTAB['__PIPELINES__'][t[4]].send(SYMTAB['__ITERATORS__'][t[1]].getNext())
    t[0]=t[2]


def p_opt_listeners(t):
    '''opt_listeners : COLON GT id_list2
    | empty'''
    if len(t)==4:
        t[0]=t[3]
    else:
        t[0]=t[1]


def p_code_definition_st(t):
    '''code_definition_st : CODE ID IS expr'''
    #Definicion de objeto de codigo (reusable)
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_code','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_code"'%(t[2],TYPESTAB[t[2]]))    
    SYMTAB['__CODES__'][t[2]]=t[4]
    if not t[2] in SYMTAB['__USED_IDS__']: 
        SYMTAB['__USED_IDS__'].append((t[2]))
    TYPESTAB[t[2]]='t_code'                
    t[0]=t[2]


def p_runtemplate_st(t):
    '''runtemplate_st : FREE ID template_list'''
    #Comprobar que la macro existe
    if not SYMTAB['__TEMPLATES__'].has_key(t[2]):
        raise Exception('Error: la template "%s" no esta definida'%t[2])
    macrodict=SYMTAB['__TEMPLATES__'][t[2]]
    sintax=macrodict['syntax']
    args=macrodict['args']
    #print args
    sintax_list2=sintax.split('|')
    sintax_list=[]
    temp_list=t[3].split('|')
    code=macrodict['body']
    #Juntar ->,<< y >> si los hay
    ignore=0
    for i in range(len(sintax_list2)):
       if ignore==1:
           ignore=0
           continue
       if sintax_list2[i]=='-':
           if sintax_list2[i+1]=='>':
               sintax_list.append(sintax_list2[i] + sintax_list2[i+1])
               ignore=1
           else:
                sintax_list.append(sintax_list2[i])
       elif sintax_list2[i]=='<':
           if sintax_list2[i+1] in ['<','>']:
               sintax_list.append(sintax_list2[i] + sintax_list2[i+1])
               ignore=1
           else:
                sintax_list.append(sintax_list2[i])            
       elif sintax_list2[i]=='>':
           if sintax_list2[i+1]=='>':
               sintax_list.append(sintax_list2[i] + sintax_list2[i+1])
               ignore=1
           else:
                sintax_list.append(sintax_list2[i])            
       else:
           sintax_list.append(sintax_list2[i])
    #print 'sintax_list: %s' % sintax_list
    #print 'macro_list: %s' % temp_list
    #Comprobar que coincide la sintaxis escrita con la de la macro
    if len(sintax_list)!=len(temp_list):
        raise Exception('Error: el numero de argumentos de la macro es distinto que el numero de argumentos suministrados')
    #variable temporal
    for i in range(len(sintax_list)):
       #print 'comprobando: %s' %('$' + sintax_list[i])
       if '$' + sintax_list [i] in args: #Codigo que hay que reemplazar
           torepl=args[args.index('$' + sintax_list[i])]
           #print 'Le corresponde en temp_list: %s' %temp_list[i]
           if temp_list[i] in SYMTAB['__CODES__']:
               #print 'reemplazando "%s" por "%s"'%(torepl,temp_list[i])
               code=code.replace(torepl,SYMTAB['__CODES__'][temp_list[i]])
           else:
               raise Exception('Error de sintaxis en el template. Se esperaba un identificador de codigo definido y se obtiene "%s"'%temp_list[i])
       else: #Si no es un id de un code, debe coincidir exactamente con el correspondiente de la macro
           if sintax_list [i]!= temp_list[i]:
               raise Exception('Error: sintaxis de la macro erronea. Se esperaba "%s" en vez de "%s"'%(sintax_list [i],temp_list[i]))
    #print 'Codigo resultante de la macro:\n%s' %code
    runMiniCode(code)


def p_template_list(t):
    '''template_list : temp_item
    | temp_item template_list'''
    try:
        t[0]=t[1] +'|'+ t[2]
    except:
        t[0]=t[1]


def p_temp_item(t):
    '''temp_item : ID
    | LBRACK
    | RBRACK
    | LPAREN
    | RPAREN
    | EQUAL
    | MINUS
    | PLUS
    | TIMES
    | LT
    | GT
    | NE
    | INSERTOR
    | EXTRACTOR
    | ARROW
    | DOT
    | COLON
    | COMMA
    | BEGIN
    | END
    | SELECT
    | INTO
    | WHERE
    | FROM
    | IN
    | WITH
    | FOR
    | OTHER
    | AND
    | OR
    | NOT'''
    t[0]=t[1]




def p_apply_st(t):
    '''apply_st : APPLY expr IN id_list2 WITH varlist
    | APPLY expr IN id_list2 WITH varlist WHERE expr'''
    code=t[2]
    idlist=t[4].split(',')
    varlist=t[6].split(',')
    temp={}
    if len(idlist)!=len(varlist):
        raise Exception('Error: el numero de listas y el de variables temporales debe coincidir')  
    for id in idlist:
        if not SYMTAB['__LISTS__'].has_key(id):
            raise Exception('Error: la lista "%s" no esta definida'%id)
    _lists=[SYMTAB['__LISTS__'][elem] for elem in idlist]            
    #Las variables son temporales.Guardar copia de variables en uso
    for var in varlist:
        if SYMTAB.has_key(var):
            temp[var]=SYMTAB[var]            
    cond=None
    tempcond='@' + str(int(10000000*random.random()))            
    if len(t)==9:
        cond=t[8]
        cond=tempcond + ' = ' + cond
        
    for i in range(len(_lists[0])):
        #print 'recorriendo las listas!!'
        for j in range(len(_lists)):
            #Asignar a las variables temporales los elementos de las listas
            SYMTAB[varlist[j]]=_lists[j][i]
        #Ejecutar el codigo
        #Si hay condicional, solo lo hacemos si el resultado
        #de evaluar el condicional es 1
        if cond!=None:
            #print 'probando condicion: %s' % cond
            #La variable DEBE existir
            SYMTAB[tempcond]=0
            runMiniCode(cond)
            if SYMTAB[tempcond]:
                runMiniCode(code)
                #SYMTAB['__LISTS__'][t[1]].append(SYMTAB[tempvar])
            else:
                continue
        else:
            #print 'Evaluando: %s'%code
            runMiniCode(code)
            #SYMTAB['__LISTS__'][t[1]].append(SYMTAB[tempvar])

    #Restaurar la variable si la hubiera y limpiar
    #del SYMTAB[tempvar]
    if cond!=None:
        del SYMTAB[tempcond]
    if temp:
        for var in temp:
            SYMTAB[var]=temp[var]        
    
        


def p_com_st(t): #Deberia devolver un valor
    '''com_st : COM COMID IS expr
    | COM COMID IS LBRACK com_chain RBRACK
    | COM com_chain
    | COM com_chain COLON EQUAL expr
    | COM com_chain ARROW VAR'''
    #print 'En com_st!!'
    #Definicion de objeto com o expresion com
    global com_var_counter
    if len(t)==3:
        com_obj=t[2].split('.')[0][1:]
        #print 'com_obj: %s' %com_obj
        if not com_obj in SYMTAB['__COM_OBJECTS__']:
            raise Exception('Error: el identificador "%s" no se corresponde con ningun objeto COM definido'%com_obj)
        #print 'cadena a evaluar: %s'% t[2].replace('!','')
        #Si es asi, ejecutar la cadena
        com_order=t[2].replace('!','')
        exec com_order in SYMTAB['__COM_OBJECTS__']
        t[0]=SYMTAB['__NULL__']
    elif t[3]=='is': #Definicion de objeto com a partir de una cadena u otra expresion com
        #if t[2] in SYMTAB['__USED_IDS__']:
        #    raise Exception('Error: El nombre "%s" ya existe'%t[2]);
        #Primero intentamos
        if len(t)==5:
            #print 'Creando el objeto!!!!'
            SYMTAB['__COM_OBJECTS__'][t[2][1:]]=win32com.client.Dispatch(t[4])
            #print SYMTAB['__COM_OBJECTS__'][t[2][1:]].Visible
        else:
            t[5]=t[5].replace('!','')
            #print repr(t[5])
            #print SYMTAB['__COM_OBJECTS__']['explorer'].Document
            #print "Fallo aqui: SYMTAB['__COM_OBJECTS__']['" + t[2][1:] + "']=" + t[5]
            exec "SYMTAB['__COM_OBJECTS__']['" + t[2][1:] + "']=" + t[5] in globals(),SYMTAB['__COM_OBJECTS__']
        if not t[2] in SYMTAB['__USED_IDS__']:  SYMTAB['__USED_IDS__'].append((t[2]))
        TYPESTAB[t[2]]='t_com_object'
        #print SYMTAB['__COM_OBJECTS__']
        t[0]=1
    elif t[4]=='=':
        #Comprobar que el primer item de la cadena es un objeto com valido
        com_obj=t[2].split('.')[0][1:]
        #print 'com_obj: %s' %com_obj
        if not com_obj in SYMTAB['__COM_OBJECTS__']:
            raise Exception('Error: el identificador "%s" no se corresponde con ningun objeto COM definido'%com_obj)
        #print 'cadena a evaluar: %s'% t[2].replace('!','') + t[4] + str(t[5]) #.replace('!','')
        #Si es asi, ejecutar la cadena
        com_order=''
        if type(t[5]) in [type(''),type(u'')]:
            varname='__aux_var_' + str(com_var_counter)
            SYMTAB['__COM_OBJECTS__'][varname]=t[5]
            SYMTAB['__COM_OBJECTS__'][varname]=SYMTAB['__COM_OBJECTS__'][varname].replace('\n','\\n')
            com_var_counter+=1
            com_order=t[2].replace('!','') + t[4] + varname
        else:
            com_order=t[2].replace('!','') + t[4] + str(t[5]) #.replace('!','')
        #print 'cadena a ejecutar: %s' % com_order
        exec com_order in SYMTAB['__COM_OBJECTS__']
        t[0]=SYMTAB['__NULL__']
    elif t[3]=='->':
        #Comprobar que el primer item de la cadena es un objeto com valido
        com_obj=t[2].split('.')[0][1:]
        #print 'com_obj: %s' %com_obj
        #print SYMTAB['__COM_OBJECTS__']
        if not com_obj in SYMTAB['__COM_OBJECTS__']:
            raise Exception('Error: el identificador "%s" no se corresponde con ningun objeto COM definido'%com_obj)
        #print 'cadena a evaluar con arrow: %s'% 'SYMTAB["' + t[4] + '"]=' + t[2].replace('!','')
        #Si es asi, ejecutar la cadena
        if not SYMTAB.has_key(t[4]):
            raise Exception('Error: la variable "%s" no esta definida'%t[4])
        com_order= 'SYMTAB["' + t[4] + '"]=' + t[2].replace('!','')
        #print 'cadena a ejecutar: %s' % com_order
        exec com_order in globals(),SYMTAB['__COM_OBJECTS__']
        if SYMTAB[t[4]]==True: SYMTAB[t[4]]=1
        elif SYMTAB[t[4]]==False: SYMTAB[t[4]]=0
        #print repr(SYMTAB[t[4]])
        t[0]=SYMTAB['__NULL__']        
    t[0]=t[2]
    
def p_com_chain(t):
    '''com_chain : com_chain_element DOT com_chain_element
    | com_chain_element DOT com_chain'''
    #print 'En com_chain!!'
    #Definicion de objeto com
    t[0]=''
    #print 't1 en com_chain:%s' %t[1]
    #print t[2]
    #print t[3]
    t[0]+=t[1]+t[2]+t[3]

def p_com_chain_elem(t):
    '''com_chain_element : COMID
    | COMID LPAREN RPAREN
    | COMID LBRACK LPAREN RPAREN RBRACK
    | COMID LPAREN com_elem_list RPAREN'''
    #print 'En com_chain_elem!!'
    global com_pair_list
    if len(t)==2:
        t[0]=t[1]
    elif len(t)==4:
        t[0]=t[1]+t[2]+t[3]
    elif len(t)==5:
        #print 'Valor de t[3]: %s' % t[3]
        args=','.join(t[3])
        t[0]=t[1]+t[2]+args+t[4]
    elif len(t)==6:
        t[0]=t[1]+t[2]+t[3]+t[4]+t[5]
    #Restaurar lista
    com_pair_list=[]

    
def p_com_pair(t):
    '''com_pair : expr EQUAL expr'''
    if type(t[3]) in [type(''),type(u'')]:
        t[3]="'" + t[3] + "'"
    else:
        t[3]=str(t[3])        
    t[0]= t[1] + '=' + t[3]

def p_com_elem_list(t):
    '''com_elem_list : com_basic
    | com_basic COMMA com_elem_list'''
    #print 'En com_elem_list!!'
    global com_pair_list
    #print [el for el in t]
    #for el in t:
    #    com_pair_list.append(el)
    t[0]=com_pair_list

def p_com_basic(t):
    '''com_basic : expr
    | com_pair'''
    #print 'En com_basic!!'
    global com_pair_list,com_var_counter
    #print type(t[1])
    #print t[1]
    if type(t[1]) in [type(''),type(u'')]:
        #if not '=' in t[1]: #expr
            varname='__aux_var_' + str(com_var_counter)
            SYMTAB['__COM_OBJECTS__'][varname]=t[1]
            SYMTAB['__COM_OBJECTS__'][varname]=SYMTAB['__COM_OBJECTS__'][varname].replace('\n','\\n')
            com_var_counter+=1
            #t[1]="'" + t[1] + "'"
            t[1]=varname
    else:
        #print 'entrando por la alternativa'
        t[1]=str(t[1])
    com_pair_list.append(t[1]) 



    


def p_symbolic_st(t): #Solo con modificador -m en el interprete
    '''symbolic_st : LET ID expr
    | LET ID USE expr COMMA ID WITH ID'''
    if 'java' in OSSYSTEM:
        raise Exception('Error: Las extensiones para simbolos matematicos no estan disponibles en plataformas java')
    if SYMTAB['__MATH_ENABLED__']==0:
        raise Exception('Error: Las extensiones para simbolos matematicos deben activarse con la opcion "-m" al invocar al interprete')
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_mathsymbol','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_mathsymbol"'%(t[2],TYPESTAB[t[2]]))    
    if len(t)==4:
        sympyfuncs=['exp','log','LamberW','floor','ceiling','Piecewise','gamma','Matrix','Normal','Uniform',
                    'piecewise_ford','sin','cos','tan','cot','asin','acos','atan'
                    'acot','pi','Max','Min','sinh','cosh','tanh','coth','asinh','acosh',
                    'atanh','acoth','re','im','sign','abs','arg','conjugate','factorial','binomial']
        for el in sympyfuncs:
            if el=='oo':
                t[3]=t[3].replace(el,'sympy.numbers.'+el)
            elif el=='-oo':
                t[3]=t[3].replace(el,'-sympy.numbers.'+el)
            elif el in ['Normal','Uniform']:
                t[3]=t[3].replace(el,'sympy.statistics.'+el)                 
            else:
                t[3]=t[3].replace(el,'sympy.'+el)
        SYMTAB['__MATH_SYMBOLS__'][t[2]]=eval(t[3])
    else:
        if not SYMTAB['__MATH_SYMBOLS__'].has_key(t[8]):
            raise Exception('Error: El simbolo "%s" no esta definido.'%SYMTAB['__MATH_SYMBOLS__'][t[8]])        
        expr=SYMTAB['__MATH_SYMBOLS__'][t[8]]
        if not SYMTAB['__LISTS__'].has_key(t[6]):
            raise Exception('Error: La lista "%s" no esta definida.'%SYMTAB['__LISTS__'][t[6]])
        args=SYMTAB['__LISTS__'][t[6]]
        for i in range(len(args)):
            if type(args[i])in [type(0.0),type(0L),type(0)]:
                continue #args[i]=str(args[i])
            elif args[i]=='oo':
                args[i]=eval('sympy.numbers.' + args[i])
            elif args[i]=='-oo':
                args[i]=eval('-sympy.numbers.' + args[i][1:])                    
            else:
                if type(args[i]) in [type(''),type(u'')]:
                    args[i]=eval(args[i])
        #Proceder segun el valor de t[4]
        if t[4]=='series':
            SYMTAB['__MATH_SYMBOLS__'][t[2]]=expr.series(*args)#series(x,0,10)  #
        elif t[4] in ['differentiate','diff']:
            SYMTAB['__MATH_SYMBOLS__'][t[2]]=expr.diff(*args)#diff(x,var,n)  #
        elif t[4]=='integrate':
            SYMTAB['__MATH_SYMBOLS__'][t[2]]=sympy.integrate(expr,args)#integrate(expr,var[,lim1,lim2])  #
        elif t[4]=='limit':
            SYMTAB['__MATH_SYMBOLS__'][t[2]]=sympy.limit(expr,*args)#limit(expr,var,point)  #
        elif t[4][-1]==')': #es una funcion, aplicarla
            if args==[]:
                SYMTAB['__MATH_SYMBOLS__'][t[2]]=eval('expr.' + t[4])
            else:
                SYMTAB['__MATH_SYMBOLS__'][t[2]]=eval('expr.' + t[4][:-2] + '(*args)')
    if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append(t[2])
    TYPESTAB[t[2]]='t_mathsymbol'
    

def p_kb_definition_st(t):
    '''kb_definition_st : DEFKB ID'''
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_basecon','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_basecon"'%(t[2],TYPESTAB[t[2]]))       
    SYMTAB['__BASECONS__'][t[2]]=BaseConocimiento()
    if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append(t[2])
    TYPESTAB[t[2]]='t_basecon'

def p_rule_definition_st(t):
    '''rule_definition_st : DEFRULE expr_list ARROW expr FOR expr
    | DEFRULE expr_list ARROW expr WHERE CODE IS expr WITH expr AND NUMBER COMMA NUMBER COMMA NUMBER FOR expr'''
    global params_list
    bname=t[18] if len(t)>7 else t[6]
    if not SYMTAB['__BASECONS__'].has_key(bname):
        raise Exception('Error. La base de conocimiento "%s" no esta definida' % bname)
    basecon=SYMTAB['__BASECONS__'][bname]
    #Comprobar que los elementos de la regla no contienen espacios y no estan vacios
    thenpart=t[4]
    ifpart=''
    if len(params_list)>0:
        ifpart=','.join(params_list)
    code=''
    explain=''
    prior=1
    confidence=1
    probab=1
    if len(t)>7:
        code=t[8]
        explain=t[10]
        prior=int(t[12])
        confidence=t[14]
        probab=t[16]
    rule=Regla()
    rule['si']=loadElements(removeWhitespace(ifpart))
    rule['entonces']=loadElements(removeWhitespace(thenpart))
    rule.setExplicacion(explain)
    rule.setComandos(code)
    rule.setCerteza(confidence)
    rule.setProbabilidad(probab)
    rule.setPrioridad(prior)
    basecon.addRegla(rule)
    #print rule.toString()
    params_list=[]
    t[0]=t[1]
    

def p_incr_st(t):
    '''incr_st : assignable INCR
    | ID accesors INCR'''
    global accesor_list
    if t[2]=='++':
        if t[1][0]=='@' and not '.' in t[1]: #Es una variable
            static=0
            if isStaticVar(t[1]) and isValidStatic(t[1]):
                static=1
            if static==0 and not SYMTAB.has_key(t[1]):
                raise Exception('Error: la variable "%s" no esta definida'%t[1])            
            #Comprobar que no es un null!!
            if static==0:
                if type(SYMTAB[t[1]]) in [type(1),type(1L),type(1.0)]:
                    if SYMTAB[t[1]]==SYMTAB['__NULL__']: raise Exception('Error: No se puede incrementar un null')
                    SYMTAB[t[1]]+= 1
                else:
                    raise Exception('Error: El operador incremento solo se puede aplicar a operandos de tipo numerico')                        
            else:
                if type(SYMTAB['__STATICS__'][t[1]]) in [type(1),type(1L),type(1.0)]:
                    if SYMTAB['__STATICS__'][t[1]]==SYMTAB['__NULL__']: raise Exception('Error: No se puede incrementar un null')
                    #print 'incrementando variable estatica'
                    SYMTAB['__STATICS__'][t[1]]+=1 
                else:
                    raise Exception('Error: El operador incremento solo se puede aplicar a operandos de tipo numerico')
        elif t[1]=='this' or '.' in t[1]: #obj_field
            objn,fldn=t[1].split('.')
            
            #CAMBIO PARA PERMITIR THIS------------------------------------------------------------------
            if objn=='this':
                if not SYMTAB['__INSIDE_OBJECT_MACRO__']==1:
                    raise Exception('Error: solo se puede usar this dentro de una macro de objeto.')
                else:
                    objn=SYMTAB['__MACRO_INSTANCE_OWNER__']
            #FIN CAMBIO PARA THIS-----------------------------------------------------------------------
                    
            value=getattr(SYMTAB['__OBJECT_INSTANCES__'][objn],fldn)
            if type(value) in [type(1),type(1L),type(1.0)]:
                value+=1
                setattr(SYMTAB['__OBJECT_INSTANCES__'][objn],fldn,value)
            else:
                raise Exception('Error: El operador incremento solo se puede aplicar a operandos de tipo numerico')                
        else: #extern_var
            pass
    elif t[2]=='--':
        if t[1][0]=='@' and not '.' in t[1]: #Es una variable
            static=0
            if isStaticVar(t[1]) and isValidStatic(t[1]):
                static=1
            if static==0 and not SYMTAB.has_key(t[1]):
                raise Exception('Error: la variable "%s" no esta definida'%t[1])            
            #Comprobar que no es un null!!
            if static==0:
                if type(SYMTAB[t[1]]) in [type(1),type(1L),type(1.0)]:
                    if SYMTAB[t[1]]==SYMTAB['__NULL__']: raise Exception('Error: No se puede incrementar un null')
                    SYMTAB[t[1]]-= 1
                else:
                    raise Exception('Error: El operador incremento solo se puede aplicar a operandos de tipo numerico')                        
            else:
                if type(SYMTAB['__STATICS__'][t[1]]) in [type(1),type(1L),type(1.0)]:
                    if SYMTAB['__STATICS__'][t[1]]==SYMTAB['__NULL__']: raise Exception('Error: No se puede incrementar un null')
                    #print 'decrementando variable estatica'
                    SYMTAB['__STATICS__'][t[1]]-=1 
                else:
                    raise Exception('Error: El operador incremento solo se puede aplicar a operandos de tipo numerico')
        elif t[1]=='this' or '.' in t[1]: #obj_field
            objn,fldn=t[1].split('.')
            
            #CAMBIO PARA PERMITIR THIS------------------------------------------------------------------
            if objn=='this':
                if not SYMTAB['__INSIDE_OBJECT_MACRO__']==1:
                    raise Exception('Error: solo se puede usar this dentro de una macro de objeto.')
                else:
                    objn=SYMTAB['__MACRO_INSTANCE_OWNER__']
            #FIN CAMBIO PARA THIS-----------------------------------------------------------------------
                    
            value=getattr(SYMTAB['__OBJECT_INSTANCES__'][objn],fldn)
            if type(value) in [type(1),type(1L),type(1.0)]:
                value-=1
                setattr(SYMTAB['__OBJECT_INSTANCES__'][objn],fldn,value)
            else:
                raise Exception('Error: El operador decremento solo se puede aplicar a operandos de tipo numerico')                
        else: #extern_var
            pass
    elif len(t)==4: #Accesors
       temp=''
       temp1=''
       last_key=''
       t[2].reverse()# El orden de los accesores esta al reves!!
       if SYMTAB['__LISTS__'].has_key(t[1]):
           #Proceder por cada elemento de lista de accesores obtenida
           temp=SYMTAB['__LISTS__'][t[1]]
       elif SYMTAB['__DICTIONARIES__'].has_key(t[1]):
           #Proceder por cada elemento de lista de accesores obtenida
           temp=SYMTAB['__DICTIONARIES__'][t[1]]
       elif SYMTAB['__MATRIXES__'].has_key(t[1]):
           #Proceder por cada elemento de lista de accesores obtenida
           temp=SYMTAB['__MATRIXES__'][t[1]].getList()           
       for item in t[2]:
           #Item puede ser un numero, una cadena, una lista o un dict
           #Probar que sea un dict primero
           temp1=temp
           try:
               #print type(temp[item])
               if type(temp1[item]) in (type(Matrix()),type({}),type(''),type(u''),type([]), type(2),type(2L),type(2.0)):
                   temp=temp1[item]
                   last_key=item
           except:
                try:
                    #print 'Probando la lista!!'
                    temp=temp1[int(item)]
                except:
                   raise Exception('Error: El elemento "%s" no es accesible' % temp)
       if type(temp) in [type(1),type(1L),type(1.0)]:
            #Comprobar que no es un null
            if temp==SYMTAB['__NULL__']: raise Exception('Error: No se puede incrementar o decrementar un null.')
            if t[3]=='++':
                if type(temp1)==type([]):
                    temp1[temp1.index(temp)]+= 1
                elif type(temp1)==type({}):
                    temp1[last_key]+=1
                elif type(temp1)==type(Matrix()): #OJO!!!!
                    pass
            elif t[3]=='--':
                if type(temp1)==type([]):
                    temp1[temp1.index(temp)]-= 1
                elif type(temp1)==type({}):
                    temp1[last_key]-=1
                elif type(temp1)==type(Matrix()): #OJO!!!!
                    pass
       else:
            raise Exception('Error: El operador incremento solo se puede aplicar a operandos de tipo numerico')           
       #Resetear lista de accesores
       accesor_list=[]          

        
    t[0]=t[1]


def p_destroy_st(t):
    '''destroy_st : DESTROY VAR
    | DESTROY ID'''
    if t[1] in TYPESTAB:
        del SYMTAB[mini_tdas[TYPESTAB[t[1]]]][t[1]]
    elif t[1] in SYMTAB:
        del SYMTAB[t[1]]
    else:
        raise Exception('Error: El identificador "%s" no esta definido'%id)
    t[0]=t[1]


def p_shared_st(t):
    '''shared_st : SHARED ID'''
    #Crear un namespace en symtab si no existe o generar una excepcion si existe
    #print "SYMTAB['__USER_NAMESPACES__']: %s" % str(SYMTAB['__USER_NAMESPACES__'])
    if t[2] in SYMTAB['__USED_IDS__']:
        raise Exception('Error: El nombre "%s" ya existe'%t[2]);
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_dict','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_dict"'%(t[2],TYPESTAB[t[2]]))    
    if SYMTAB['__USER_NAMESPACES__'].has_key(t[2]):
        raise Exception('Error: Se ha intentado crear un espacio de nombres compartido que ya existe!!')
    else:
        SYMTAB['__USER_NAMESPACES__'][t[2]]={}
    SYMTAB['__USED_IDS__'].append((t[2]))
    TYPESTAB[t[2]]='t_dict'         
    #print SYMTAB['__USER_NAMESPACES__']
    t[0]=t[1]


def p_extension_st(t):
    '''extension_st : tql_st'''
    t[0]=t[1]


def p_create_obj_st(t):
    '''create_obj_st : ID EQUAL NEW obj_type
    | ID EQUAL NEW obj_type LPAREN objpairs_list RPAREN'''
    #print 'entrando a create object'
    global objpairs_list
    #Erro si: No existe el objeto o bien
    #existe pero no coincide el tipo NI EL DE NINGUNA DE SUS BASES!!!!
    if not t[1] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[1])
    elif t[1] in TYPESTAB and TYPESTAB[t[1]] not in [t[4].strip("'"),'t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "%s"'%(t[1],TYPESTAB[t[1]],t[4].strip("'")))          
    #Crear y dar de alta un objeto segun su prototipo
    instance=MiniObject(t[4].strip("'"))      
    SYMTAB['__OBJECT_INSTANCES__'][t[1]]=instance
    #print SYMTAB['__OBJECT_INSTANCES__']
    SYMTAB['__USED_IDS__'].append((t[1]))
    fnames=[i[0] for i in SYMTAB['__DEFINED_OBJECTS__'][t[4]].fields_names]
    #Dar de alta el tipo de la instancia-------------------
    TYPESTAB[t[1]]=t[4].strip("'") #Es el tipo del objeto
    #------------------------------------------------------
    if len(t)==8:
        args=objpairs_list
        #print 'objspair_list: %s' % objpairs_list
        objpairs_list=[] #Resetear
        #Inicializar los campos con los valores pasados
        #for i in range(len(fnames)):
        for arg in args:
            if not hasattr(SYMTAB['__OBJECT_INSTANCES__'][t[1]],arg[0]):
                raise Exception('Error: el objeto "%s" no tiene el campo "%s"'%(SYMTAB['__OBJECT_INSTANCES__'][t[1]],arg[0]))
            setattr(SYMTAB['__OBJECT_INSTANCES__'][t[1]],arg[0],arg[1])

    t[0]=t[1]

def p_objpair(t):
    '''objpair : ID EQUAL expr
    | ID ARROW ID'''
    if t[2]=='->':
    	t[0]=(t[1],findId(t[3])[0])
    else:
        t[0]= (t[1],t[3])


def p_objpairs_list(t):
    '''objpairs_list : objpair COMMA objpairs_list
    | objpair
    | empty'''
    global objpairs_list
    for el in t:
        if type(el)==type((1,2)):
            objpairs_list.append(el)
    t[0]=1    

def p_obj_type(t):
    '''obj_type : ID'''
    t[0]=t[1] #No permitimos crear objetos 'object'


def p_id_assign_exp(t):
    '''id_assign_exp : ID IS id_expr
    | ID IS id_funcall
    | ID IS SELECT condition FROM id_list2'''
    #Asegurarse de que ID esta definido
    minitype=findId(t[1])[1]
    if minitype not in ['t_list','t_dict','t_matrix']:
        raise Exception('Error: no se puede hacer una seleccion sobre el tipo "%s"'%minitype)
    elif len(t)==7: #seleccion de items
        ids=t[6].split(',')#Viene como un cadena de id separados por comas
        op=t[4]
        for elem in ids: #Proceder segun operador
            #Excepcion si no coinciden los tipos
            inst,tipo=findId(elem)
            if minitype!=tipo:
                raise Exception('Error: No coinciden los tipos "%s" y "%s".'%(minitype,tipo))
            if t[4]=='+':
                if minitype=='t_list': #meter elementos en la lista
                    SYMTAB[mini_tdas[TYPESTAB[t[1]]]][t[1]]+=inst
                elif minitype=='t_dict':
                    SYMTAB[mini_tdas[TYPESTAB[t[1]]]][t[1]].update(inst)
                elif minitype=='t_matrix':
                    raise Exception('Error: Operacion no definida para t_matrix: "%s"'%t[4])
            elif t[4]=='->':
                if minitype=='t_list': #meter elementos en la lista
                    SYMTAB[mini_tdas[TYPESTAB[t[1]]]][t[1]].append(inst)
                elif minitype=='t_dict':
                    raise Exception('Error: Operacion no definida para t_dict: "%s"'%t[4])
                elif minitype=='t_matrix':
                    raise Exception('Error: Operacion no definida para t_matrix: "%s"'%t[4])
            elif t[4][0]=='?': #condicion de seleccion
                if minitype=='t_list': 
                    for elem in inst:
                        if eval(repr(elem) + t[4][1:]):
                            SYMTAB[mini_tdas[TYPESTAB[t[1]]]][t[1]].append(elem)
                elif minitype=='t_dict':
                    raise Exception('Error: Operacion no definida para t_dict: "%s"'%t[4])
                elif minitype=='t_matrix':
                    raise Exception('Error: Operacion no definida para t_matrix: "%s"'%t[4])
            elif t[4][0]=='&': #seleccion de intervalo
                if minitype=='t_list':
                    begin,end=[int(el) for el in t[4][1:].split(',')]
                    SYMTAB[mini_tdas[TYPESTAB[t[1]]]][t[1]].extend(inst[begin:end])
                elif minitype=='t_dict':
                    raise Exception('Error: Operacion no definida para t_dict: "%s"'%t[4])
                elif minitype=='t_matrix':
                    raise Exception('Error: Operacion no definida para t_matrix: "%s"'%t[4])
            elif t[4][0]=='_': #aplicar funcion
                if minitype=='t_list':
                    if not SYMTAB['__FUNCTIONS__'].has_key(t[4]):
                        raise Exception('Error invocando a la funcion: "%s". Esta funcion no esta definida.' %t[4])
                    func=SYMTAB['__FUNCTIONS__'][t[4]]
                    #Hay que hacer una copia o si no no se puede usar con una lista y ella misma!!!
                    temp=inst[:]
                    temp=[func(el) for el in temp]
                    #for elem in inst:
                        #SYMTAB[mini_tdas[TYPESTAB[t[1]]]][t[1]].append(func(elem))
                    SYMTAB[mini_tdas[TYPESTAB[t[1]]]][t[1]]=temp
                elif minitype=='t_dict':
                    raise Exception('Error: Operacion no definida para t_dict: "%s"'%t[4])
                elif minitype=='t_matrix':
                    raise Exception('Error: Operacion no definida para t_matrix: "%s"'%t[4])                            
            else: #??
                raise Exception('Error: Operador no permitido: "%s"'%t[4])
                
    else: #operacion con tdas
        #Y cambiar su contenido
        SYMTAB[mini_tdas[TYPESTAB[t[1]]]][t[1]]=t[3]
    


def p_varlist(t):
    '''varlist : VAR
    | VAR COMMA varlist'''
    try:
        t[0]=t[1] + t[2] + t[3]
    except:
        t[0]=t[1]

def p_condition(t):
    '''condition : PLUS
    | ARROW
    | relop expr
    | LPAREN expr COMMA expr RPAREN
    | IDENTIFIER LPAREN RPAREN'''
    #Asegurarse de que ID esta definido
    if len(t)==2:
        t[0]=t[1]
    elif len(t)==3:
        t[0]='?' + t[1] + str(t[2])
    elif len(t)==4:
        t[0]=t[1]
    else:
        t[0]='&' + str(int(t[2])) + ',' + str(int(t[4]))
    

def p_assign_exp(t):
    '''assign_exp : assignable EQUAL condic_expr
    | assignable EQUAL expr  
    | assignable EQUAL select_st
    | assignable EQUAL update_st
    | assignable EQUAL insert_st
    | assignable EQUAL instance_type ID
    | assignable EQUAL instance_type ID ARROW ID
    | assignable EQUAL ID ARROW ID
    | assignable EQUAL ID
    | assignable EQUAL USE ID
    | assignable EQUAL USE ID IN ID
    | assignable EQUAL MACROID
    | assignable EQUAL IDENTIFIER
    | assignable EQUAL GET STATIC ID DOT ID
    | assignable EQUAL linqlike_st
    | assignable EQUAL list_expr_st
    | assignable EQUAL sql_st
    | assignable EQUAL LAMBDA LPAREN varlist RPAREN IS expr'''
    global accesor_list2,item_list
    get_static=0 #Flag que indica que queremos un campo estatico
    empty_list=0
    name=''
    #print 'En assign_exp!!. t[3]=%s' %t[3]
    #print 'len(t): %s'%len(t)
    #print [el for el in t]
    #Cambio para list_expr_st----------------------------------------------------
    #Si t[3] es None, es un list_expr_st
    if t[3]==None:
        t[3]=decodeList(item_list[:],[])
        item_list=[]
    #----------------------------------------------------------------------------
    #Declaracion de una funcion lambda
    if t[3]=='lambda':
        name=str(long(random.random()*10000000000)) 
        code=t[8]  
        #procesar returns y codigo
        #Proteger codigo dentro de strings ??-------------------------------------------------------
        regx=RegExp('\"\"\'\'[\s\S]*?\'\'\"\"')
        scont=0
        strings={}
        strs=regx.getMatches(code)
        for el in strs:
            code=code.replace(el,'%%%%'+str(scont)+'%%%%')
            strings['%%%%'+str(scont)+'%%%%']=el
            scont+=1
        #--------------------------------------------------------------------------------------------
        
        #Procesar los returns en el codigo:----------------------------------------------------------
        regx=RegExp('\s*return\s*([^;]+);')
        old_code=code
        #Considerar varias sentencias return:
        #code=regx.replace(code," _setVar('&" + name + "',\\1);")
        code=re.sub('\s*return\s*([^;]+);',"\n _setVar('&" + name + "',\\1);",code)
        #--------------------------------------------------------------------------------------------
        
        #Recuperar el contenido de las strings-------------------------------------------------------
        for item in strings:
            code=code.replace(item,strings[item])          
        #--------------------------------------------------------------------------------------------
        
        #Cambio para ver si las macros aceptan valor de retorno--------------------------------------
        macro_dict={'type':'function','args':t[5].split(','),'code':code,'name': name,'returns':0}
        #Si se cambia algo en la cadena de codigo, es que hay al menos un return
        if code!=old_code:
            macro_dict['returns']=1
        #--------------------------------------------------------------------------------------------
            
        #Dar de alta las macros. Guardamos un diccionario con los argumentos y el codigo
        #print macro_dict
        SYMTAB['__MACROS__'][name]=macro_dict
        #print SYMTAB['__MACROS__']        
        SYMTAB['__FUNCTIONS_REFS__'][t[1][1:]]=name
        #print SYMTAB['__FUNCTIONS_REFS__']
        
        
        
        
    #Si es una referencia a funcion, crear una entrada en la tabla de referencias
    #PERMITIMOS UN ALIAS PARA UNA FUNCION DE OBJETO???????????
    elif type(t[3]) in [type(''),type(u'')]:
        if len(t[3]) > 2 and t[3][0] in ['_','&']:
            if t[1][0]=='@': #variable
                static=0
                if isStaticVar(t[1]) and isValidStatic(t[1]):
                    static=1
                if static==0 and not SYMTAB.has_key(t[1]):
                    raise Exception('Error: la variable "%s" no esta definida'%t[1])                
                SYMTAB['__FUNCTIONS_REFS__'][t[1][1:]]=t[3]
            else:
                SYMTAB['__FUNCTIONS_REFS__'][t[1]]=t[3]
    #print SYMTAB['__FUNCTIONS_REFS__']
    if len(t)==8 and t[4]=='static': #Asignacion de variable de funcion estatica
        if not t[5] in SYMTAB['__MACROS__']:
            raise Exception('Error: la funcion "%s" no esta definida'%t[5])
        if not '@'+t[7] in SYMTAB['__FUNC_STATICS__'][t[5]]:
            raise Exception('Error: la variable estatica "@%s" no esta definida en la funcion "%s"'%(t[7],t[5]))
        #val=SYMTAB['__STATICS__']['@'+t[7]]
    #Si estamos asignando el valor de un iterador, cambiar el id por el valor----
    #print 'Valor de t[3]: %s' %t[3]
    if type(t[3]) in [type(''),type(u'')] and t[3] in TYPESTAB:
        if t[3] in SYMTAB['__ITERATORS__']:
            itval=findId(t[3])
            t[3]=itval[0].getNext()
        #else:
        #    raise Exception('Error: El identificador "%s" no es un iterador definido'%t[3])
    #----------------------------------------------------------------------------

    assign_inst=0 #Flag que indica asignacion de instancia
    get_enum_string=0 #Flag que indica que queremos el valor del enum
    #CAMBIO PARA PODER MANEJAR INSTANCIAS COMO VARIABLES (SOLO TIPOS INTERNOS)
    if len(t)==7: #Asignacion de enum(el entero)
       assign_inst=1
       if t[3]=='enum':
           if not SYMTAB['__ENUMS__'].has_key(t[4]):
               raise Exception('Excepcion asignando la variable %s. La enum %s no esta definida.' %(t[1],t[4]))
        #Resultado de asignar una sustitucion sobre una expresion simbolica
       elif t[3]=='use':
           if not SYMTAB['__MATH_SYMBOLS__'].has_key(t[6]):
               raise Exception('Excepcion asignando la variable %s. La expresion simbolica %s no esta definida.' %(t[1],t[6]))
       else: #Error de tipo.
               raise Exception('Excepcion asignando la variable %s. El tipo %s no esta definido.' %(t[1],t[4]))

    if len(t)==6:#Asignacion de enum(el string asociado)
       assign_inst=1
       get_enum_string=1
       if not SYMTAB['__ENUMS__'].has_key(t[3]):
           raise Exception('Excepcion asignando la variable %s. La enum %s no esta definida.' %(t[1],t[3]))
           
    if len(t)==5: #Asignacion de instancia o lista vacia
       #print 'Asignacion de instancia'
       assign_inst=1 
       if t[3]!='use':
           if t[3]=='list':
               if not SYMTAB['__LISTS__'].has_key(t[4]):
                   raise Exception('Excepcion asignando la variable %s. La lista %s no esta definida.' %(t[1],t[4]))
           elif t[3]=='dict':
               if not SYMTAB['__DICTIONARIES__'].has_key(t[4]):
                   raise Exception('Excepcion asignando la variable %s. El diccionario %s no esta definido.' %(t[1],t[4]))
           elif t[3]=='matrix':
               if not SYMTAB['__MATRIXES__'].has_key(t[4]):
                   raise Exception('Excepcion asignando la variable %s. La matrix %s no esta definida.' %(t[1],t[4]))
           elif t[3]=='spreadsheet':
               if not SYMTAB['__SPREADSHEETS__'].has_key(t[4]):
                   raise Exception('Excepcion asignando la variable %s. El spreadsheet %s no esta definido.' %(t[1],t[4]))
           elif t[3]=='tree':
               if not SYMTAB['__TREES__'].has_key(t[4]):
                   raise Exception('Excepcion asignando la variable %s. El tree %s no esta definido.' %(t[1],t[4]))
           elif t[3]=='instance':
               if not SYMTAB['__PY_OBJECTS__'].has_key(t[4]):
                   raise Exception('Excepcion asignando la variable %s. La instancia %s no esta definida.' %(t[1],t[4]))            
           elif t[3] =='object':
               if not SYMTAB['__OBJECT_INSTANCES__'].has_key(t[4]):
                   raise Exception('Excepcion asignando la variable %s. El objeto %s no esta definido.' %(t[1],t[4]))
           elif t[3] =='code':
               if not SYMTAB['__CODES__'].has_key(t[4]):
                   raise Exception('Excepcion asignando la variable %s. El codigo %s no esta definido.' %(t[1],t[4]))
           elif t[3] =='sexpr':
               if not SYMTAB['__SEXPRS__'].has_key(t[4]):
                   raise Exception('Excepcion asignando la variable %s. La S-expr %s no esta definida.' %(t[1],t[4]))
           elif t[3] =='pcode':
               if not SYMTAB['__PCODES__'].has_key(t[4]):
                   raise Exception('Excepcion asignando la variable %s. El P-code %s no esta definido.' %(t[1],t[4]))
           elif t[3] =='type':
               if not SYMTAB['__TYPE_INSTANCES__'].has_key(t[4]):
                   raise Exception('Excepcion asignando la variable %s. Laa instancia de tipo %s no esta definida.' %(t[1],t[4]))                                               
           else: #Error de tipo o tipo no estandar: POR IMPLEMENTAR!!!
                   raise Exception('Excepcion asignando la variable %s. El tipo %s no esta definido.' %(t[1],t[3]))         
    # CAMBIO PARA EXTENSIONES TQL!!=>SE PUEDE ASIGNAR EL RESULTADO DE UN SELECT A UNA VARIABLE
    #print '+++++++++++' + t[1] + '++++++++++++++'

    if type(t[1]) in [type([]),type({})] and accesor_list2!=[]: #Accesor
       #print 't[1] en assign: %s' %str(t[1])
       #print 'accesor_list2 in asign: %s' % str(accesor_list2)
       temp=accesor_list2[0]
       if type(t[1])==type([]): temp=int(temp)
       #print 'asignando un accesor!!'
       #if type(t[1])==type({}):
       if len(t)==8 and t[4]=='static': #Asignacion de campo estatico
           t[1][temp]=SYMTAB['__STATICS__']['@'+t[7]]
       elif not assign_inst:
           t[1][temp]=t[3]          
           #print 'Se ha asignado una variable!'
       else: 
           if t[3]=='list':
              t[1][temp]=SYMTAB['__LISTS__'][t[4]]
           elif t[3]=='dict':
              t[1][temp]=SYMTAB['__DICTIONARIES__'][t[4]]
           elif t[3]=='enum' or get_enum_string:
               if get_enum_string==0:
                   t[1][temp]=SYMTAB['__ENUMS__'][t[4]].dict[t[6]]
               else:
                   t[1][temp]=SYMTAB['__ENUMS__'][t[3]].list[SYMTAB['__ENUMS__'][t[3]].dict[t[5]]]
           elif t[3]=='tree':
               t[1][temp]=SYMTAB['__TREES__'][t[4]][t[6]]
           elif t[3]=='matrix':
               t[1][temp]=SYMTAB['__MATRIXES__'][t[4]][t[6]]
           elif t[3]=='spreadsheet':
               t[1][temp]=SYMTAB['__SPREADSHEETS__'][t[4]][t[6]]
           elif t[3]=='instance':
               t[1][temp]=SYMTAB['__PY_OBJECTS__'][t[4]][t[6]]
           elif t[3]=='object':
               SYMTAB[t[1]]=SYMTAB['__OBJECT_INSTANCES__'][t[4]]
               #t[1][temp]=t[4] #Solo necesitamos el nombre ???
           elif t[3]=='code':
              t[1][temp]=SYMTAB['__CODES__'][t[4]]
           elif t[3]=='sexpr':
              t[1][temp]=eval_sexpr(SYMTAB['__SEXPRS__'][t[4]])
           elif t[3]=='pcode':
              t[1][temp]=eval_pcode(SYMTAB['__PCODES__'][t[4]])
           elif t[3]=='type':
              t[1][temp]=SYMTAB['__TYPE_INSTANCES__'][t[4]]                  
           elif t[3]=='use':
              t[1][temp]=SYMTAB['__MATH_SYMBOLS__'][t[6]].subs(SYMTAB['__DICTIONARIES__'][t[4]])
               
       #print 'Secuencia modificada: %s' % str(t[1])
       #print 'Resultado: %s' % str(t[1][temp])
       t[0]=1               
        #Resetear lista de accesores
       accesor_list2=[]
    elif t[1][0]=='@': #Estamos asignando una variable
            #print 'asignando variable'
        #Cambio: generamos una excepcion si la variable no esta definida
            static=0
            if isStaticVar(t[1]) and isValidStatic(t[1]):
                static=1
            if static==0 and not SYMTAB.has_key(t[1]):
                raise Exception('Error: la variable "%s" no esta definida'%t[1])
        #try:#GUARDAR LOS TIPOS!!!!!
            if len(t)==8 and t[4]=='static': #Asignacion de campo estatico
                SYMTAB[t[1]]=SYMTAB['__STATICS__']['@'+t[7]]
            elif not assign_inst:
                if static==0:
                    #print 'len(t): %s'%len(t)
                    #print 'name: %s'% name
                    if t[3]=='lambda' and len(t)==9:
                        #print 'asignando nombre correcto!'
                        SYMTAB[t[1]]=name
                    else:
                        SYMTAB[t[1]]=t[3]
                    #print  'asignado: %s' %SYMTAB[t[1]]
                else:
                    SYMTAB['__STATICS__'][t[1]]=t[3]
                if type(t[3]) in (type(2),type(2L),type(2.0)):#Tiene sentido todavia???????????????
                    TYPESTAB[t[1]]='numeric'
                elif type(t[3]) in (type(''), type(u'')):
                    TYPESTAB[t[1]]='string'
                else:
                    TYPESTAB[t[1]]='any'
                                     
                #print 'Se ha asignado una variable!'
            else: 
                if t[3]=='list':
                   SYMTAB[t[1]]=SYMTAB['__LISTS__'][t[4]]
                   #print SYMTAB[t[1]]
                   TYPESTAB[t[1]]='t_list'
                elif t[3]=='dict':
                   SYMTAB[t[1]]=SYMTAB['__DICTIONARIES__'][t[4]]
                   TYPESTAB[t[1]]='t_dict'
                elif t[3]=='enum' or get_enum_string:
                   if get_enum_string==0:
                       SYMTAB[t[1]]=SYMTAB['__ENUMS__'][t[4]].dict[t[6]]
                       TYPESTAB[t[1]]='t_enum'
                   else:
                       SYMTAB[t[1]]=SYMTAB['__ENUMS__'][t[3]].list[SYMTAB['__ENUMS__'][t[3]].dict[t[5]]]
                       TYPESTAB[t[1]]='t_string'
                elif t[3]=='tree':
                   SYMTAB[t[1]]=SYMTAB['__TREES__'][t[4]][t[6]]
                   TYPESTAB[t[1]]='t_tree'
                elif t[3]=='matrix':
                   SYMTAB[t[1]]=SYMTAB['__MATRIXES__'][t[4]]  #[t[6]]
                   TYPESTAB[t[1]]='t_matrix'
                elif t[3]=='spreadsheet':
                   SYMTAB[t[1]]=SYMTAB['__SPREADSHEETS__'][t[4]]  #[t[6]]
                   TYPESTAB[t[1]]='t_spreadsheet'
                elif t[3]=='instance':
                   SYMTAB[t[1]]=SYMTAB['__PY_OBJECTS__'][t[4]]  #[t[6]]
                   TYPESTAB[t[1]]='t_pyobject'
                elif t[3]=='object':
                   SYMTAB[t[1]]=SYMTAB['__OBJECT_INSTANCES__'][t[4]] #Solo necesitamos el nombre ???
                   #SYMTAB[t[1]]=t[4] #Solo necesitamos el nombre ???
                   TYPESTAB[t[1]]='t_object'
                elif t[3]=='code':
                   SYMTAB[t[1]]=SYMTAB['__CODES__'][t[4]]
                   TYPESTAB[t[1]]='t_code'
                elif t[3]=='sexpr':
                   SYMTAB[t[1]]=eval_sexpr(SYMTAB['__SEXPRS__'][t[4]])
                   TYPESTAB[t[1]]='t_sexpr'                   
                elif t[3]=='pcode':
                   SYMTAB[t[1]]=eval_pcode(SYMTAB['__PCODES__'][t[4]])                   
                   TYPESTAB[t[1]]='t_pcode'
                elif t[3]=='type':
                   SYMTAB[t[1]]=SYMTAB['__TYPE_INSTANCES__'][t[4]]                  
                   TYPESTAB[t[1]]=TYPESTAB[t[4]]                   
                elif t[3]=='use':
                    if len(t)==5: #asignar el id
                        try:
                            SYMTAB[t[1]]=SYMTAB['__MATH_SYMBOLS__'][t[4]].evalf()
                        except:
                            SYMTAB[t[1]]=SYMTAB['__MATH_SYMBOLS__'][t[4]]
                        #Pasar tuplas a listas
                        finally:
                            if type(SYMTAB[t[1]])==type((0,)):
                                SYMTAB[t[1]]=list(SYMTAB[t[1]])
                        
                    else:
                        SYMTAB[t[1]]=SYMTAB['__MATH_SYMBOLS__'][t[6]].subs(SYMTAB['__DICTIONARIES__'][t[4]])
                    TYPESTAB[t[1]]='t_mathsymbol'                   
            t[0]=1
        #except:
            #print 'excepcion asignando variable'
            #pass
    else:#Estamos asignando un campo de objeto
##        try: 
            #1.- Obtener el nombre del objeto y el del campo
            #print 'Asignando campo de objeto'
            #print t[1]
            objn,fldn=findObjectField(t[1])#Cambio para permitir cadenas de acceso a objetos

            #CAMBIO PARA PERMITIR THIS------------------------------------------------------------------
            if objn=='this':
                if not SYMTAB['__INSIDE_OBJECT_MACRO__']==1:
                    raise Exception('Error: solo se puede usar this dentro de una macro de objeto.')
                else:
                    objn=SYMTAB['__MACRO_INSTANCE_OWNER__']
            #FIN CAMBIO PARA THIS-----------------------------------------------------------------------
            private=isPrivate(objn,fldn)
            if isinstance(objn,MiniObject):
                if private==0:
                    setattr(objn,fldn,t[3])
                else:
                    raise Exception('Error de acceso a campo de objeto. El campo "%s" se ha declarado privado'%fldn)
            else:
                if private==0 or SYMTAB['__INSIDE_OBJECT_MACRO__']==1: #public o via this
                    setattr(SYMTAB['__OBJECT_INSTANCES__'][objn],fldn,t[3])
                else:
                    raise Exception('Error de acceso a campo de objeto. El campo "%s" se ha declarado privado'%fldn)
            #print 'Se ha asignado un campo de objeto!'
            t[0]=1
##        except:
##            #print 'excepcion asignando campo de objeto'
        

def p_instance_type(t): #COMO METEMOS EL RESTO DE TIPOS DEFINIDOS O DEFINIBLES????????
    '''instance_type : LIST
    | DICT
    | ENUM
    | TREE
    | MATRIX
    | INSTANCE
    | OBJECT
    | CODE
    | SEXPR
    | PCODE
    | TYPE
    | ID'''
    #REVISAR EL ID FINAL!!!!!!
    t[0]=t[1]

def p_assignable(t):
    '''assignable : VAR
    | obj_field
    | extern_var
    | ID accesors2
    | TIMES VAR accesors2'''
    #print 'En asignable, len(t): %s' %len(t)
    #print [el for el in t]
    #print 't[1]:%s' %t[1]
    temp=None
    acclist=[]
    global accesor_list2


    if len(t)in [3,4]: #Asignacion de un accesor o accesor  con variable     
       if len(t)==4:
            t[3].reverse()# El orden de los accesores esta al reves!!
            temp=SYMTAB[t[2]]
            acclist=t[3]
       else:
           t[2].reverse()# El orden de los accesores esta al reves!!
           acclist=t[2]
           if SYMTAB['__LISTS__'].has_key(t[1]):
               #print 'Entrando por listas!'
               #Proceder por cada elemento de lista de accesores obtenida
               temp=SYMTAB['__LISTS__'][t[1]]
           elif SYMTAB['__DICTIONARIES__'].has_key(t[1]):
               #print 'Entrando por diccionarios'
               #Proceder por cada elemento de lista de accesores obtenida
               temp=SYMTAB['__DICTIONARIES__'][t[1]]
           elif SYMTAB['__MATRIXES__'].has_key(t[1]):
               #print 'Entrando por matrixes'
               #Proceder por cada elemento de lista de accesores obtenida
               temp=SYMTAB['__MATRIXES__'][t[1]].getList()           
           

       #Si la lista de accesores solo tiene un item lo cogemos tal cual
       #Si son varios hay que recuperar la secuencia que corresponde al PENULTIMO elemento
       #y la devolvemos en t[0]
##       if len(t[2])!=1:
##           for item in t[2][:-1]:
       #print 'Valor de acclist: %s' % acclist
       if len(acclist)!=1:
           for item in acclist[:-1]:               
               #print 'Probando2 item2: %s' %str(item)
               #Item puede ser un numero, una cadena, una lista o un dict
               #Probar que sea un dict primero
               try:
                   #print type(temp[item])
                   if type(temp[item]) in (type(Matrix()),type({}),type(''),type(u''),type([]), type(2),type(2L),type(2.0)):
                       temp=temp[item]

               except:
                    try:
                        #print 'Probando la lista!!'
                        temp=temp[int(item)]
                    except:
                       raise Exception('Error: El elemento "%s" no es accesible' % temp)
       #En accesor_list2 enviamos el ultimo elemento, que es el indice de la secuencia a asignar
       accesor_list2=[accesor_list2[-1]]
       t[0]=temp
    else:
        t[0]=t[1]
        #print 'Entrando por el else. t[0]=%s'%t[0]
    #print 'asignable: %s' % t[0]

def p_extern_var(t):
    '''extern_var : EXTERN ID COLON COLON ID'''
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_extern','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_extern"'%(t[2],TYPESTAB[t[2]]))    
    namespace=t[2]
    varname=t[5]
    #1.-Si no hay namespace o no existe la varible en el, lanzamos una excepcion
    if not SYMTAB['__USER_NAMESPACES__'].has_key(namespace):
       raise Exception('Error: El espacio de nombres %s no esta definido en la tabla de simbolos!!' % namespace)
    if not SYMTAB['__USER_NAMESPACES__'][namespace].has_key(varname):
       raise Exception('Error: La variable %s no esta definido en el espacio de nombres %s!!' % (varname,namespace))
    #Si no es una cadena o un numero, lanzar una excepcion de tipo de utilizable
    if type(SYMTAB['__USER_NAMESPACES__'][namespace][varname]) not in [type(1),type(1L),type(.5),type(r''),type(u'')]:
        raise Exception('Error: El tipo de la variable externa %s no es numeric o string. Este tipo no es manejable en Mini!!' % varname)
##    if t[2] in SYMTAB['__USED_IDS__']:
##        raise Exception('Error: El nombre "%s" ya existe'%t[2]);       
    t[0]=SYMTAB['__USER_NAMESPACES__'][namespace][varname]
    SYMTAB['__USED_IDS__'].append((t[2]))
    TYPESTAB[t[2]]='t_extern'    


def p_obj_field(t):
    '''obj_field : THIS
    | obj_prefix DOT ID
    | obj_prefix DOT obj_fields_list'''
    global object_field_list
    #print 'Valor en obj_field: %s' %t[1]
    #print len(t)
    #CAMBIOS PARA USAR THIS-----------------------------------------------------------------
    #Asegurarse de que se puede usar this
    if t[1]=='this' and not SYMTAB['__INSIDE_OBJECT_MACRO__']==1:
        raise Exception('Error: solo se puede usar "this" dentro de una macro de objeto.')
    #Si es una variable, sustituirla por su valor
    if t[1][0]=='@':
        t[1]=SYMTAB[t[1]]
    #FIN CAMBIOS PARA THIS------------------------------------------------------------------
    if len(t)==4:
        #if type(t[3])==type([]):
        if object_field_list!=[]:
            #print 'Lista de accesores a objeto: %s' %object_field_list
            #print t[1]
            #print t[2]
            object_field_list.reverse()
            
            if isinstance(t[1],MiniObject):
                t[0]=[t[1], '.'.join(object_field_list)]
            else:
                t[0]=t[1] + t[2] + '.'.join(object_field_list)#(t[3])
            #print 'Valor de t[0]:%s' % t[0]
            object_field_list=[]
        else:
            #print 't[1] ahora:%s' %t[1]
            if isinstance(t[1],MiniObject): #Variables de objeto
                t[0]=[t[1],t[3]]
            elif type(t[1])==type([]) and isinstance(t[1][0],MiniObject): #Variable procedente de un accesor
                t[0]=[t[1][0],t[3]]
            else:
                t[0]=t[1]+t[2]+t[3]
    else: #Solo this
        #print 'Entrando por solo this'
        #print SYMTAB['__MACRO_INSTANCE_OWNER__']
        #t[0]=t[1]
        t[0]=SYMTAB['__MACRO_INSTANCE_OWNER__']


def p_obj_prefix(t):
    '''obj_prefix : THIS
    | ID
    | VAR'''
    #print 'en objprefix:%s'%t[1]
    t[0]=t[1]


def p_obj_fields_list(t):
    '''
    obj_fields_list : ID DOT ID
    | ID DOT obj_fields_list  
    '''
    global object_field_list
    #print 'En obj_fields_list'
    #print t[1]
    #print t[3]
    #Hay que generar una lista con los campos necesarios
    if t[3]:
        object_field_list.append(t[3])
    if t[1]:
        object_field_list.append(t[1])
    #print 'lista: %s' % object_field_list
    #t[0]=object_field_list


#Cambios para soporte de COM nativo (solo win32)-------------------------------------------
   

#Cambios para aceptar definiciones de listas y otros TDAs dentro del codigo------------------

def p_enum_definition_st(t): ##OJO QUE EXPR_LIST ESTA CAMBIADO!!!!!
    '''enum_definition_st : ENUM ID IS LBRACK expr_list RBRACK'''
    #Definicion de enumeracion
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])    
    global params_list
    contador=0
##    if t[2] in SYMTAB['__USED_IDS__']:
##        raise Exception('Error: El nombre "%s" ya existe'%t[2]);       
    if SYMTAB['__ENUMS__'].has_key(t[2]): #Solo se puede definir una vez una enumeracion
        raise Exception('Error: La enumeracion "%s" ya esta definida' %t[2])        
    for elem in params_list:
        #Comprobar que elem es un ID valido!!
        if not re.match(r'[a-zA-Z][a-zA-Z_0-9]*', elem):
            raise Exception('Error: "%s" es un elemento no valido Los miembros de una enum solo pueden ser cadenas alfanumericas o subrayados. No pueden contener espacios y deben empezar por una letra.'%elem)
        #SYMTAB['__ENUMS__'][t[2]][elem]=contador
        #contador+=1
    #print SYMTAB['__ENUMS__']
    params_list.reverse() #Hay que invertirla porque esta al reves
    SYMTAB['__ENUMS__'][t[2]]=Enum(params_list)
    SYMTAB['__USED_IDS__'].append((t[2]))
    TYPESTAB[t[2]]='t_enum'  
    params_list=[]              
    t[0]=t[2]




def p_list_expr_st(t):
    '''list_expr_st : LIST LBRACK subexp_list RBRACK
    | LIST LBRACK RBRACK'''
    #| list_exp_oper2'''
    global item_list,just_append,expr_list,list_op_performed,listexp_from_expr,last_list_expr,item_list_counter
    #print 'en list_expr_st con t: %s'%[el for el in t]
    #print 'valor de listexp_from_expr: %s' % listexp_from_expr
    #print 'valor de item_list_counter: %s' % item_list_counter
    #Como la gramatica permite que los elementos de un item sean expr,
    #nada nos protege de que se puedan escribir como "->list[...]".
    #Si se hace asi, el mecanismo de definicion de listas no funciona bien
    #cuando hay listas anidadas. Para evitar esto, generamos una excepcion
    #si encontramos mas de un "->list" contabilizado por la variable
    #global listexp_from_expr
    #if listexp_from_expr!=0:
    #    raise Exception('Error de sintaxis en "%s": no se permite utilizar expresiones "->list" como elementos en la definicion de una lista'%last_list_expr)
    if len(t)==4: #lista vacia(REVISAR ESTO!!!!)
        t[0]=[]
    else:
        #print 'Valor de item_list: %s' % item_list
        t[0]=decodeList(item_list[:],[])
        item_list=[]
        last_list_expr='...->' + ''.join([str(el) for el in t][1:-1]) + '...'
        #print 'last_list_expr: %s' %last_list_expr
    #resetear flag ??????????
    #listexp_from_expr=0#-=1


def p_subexp_list(t):
    '''subexp_list : subexp COMMA subexp_list
    | subexp'''
    global item_list,just_append,expr_list,item_list_counter,last_list_expr
    #print 'en subexp_list con ITEM_LIST: %s' % item_list
    #print 'valor de listexp_from_expr: %s' % listexp_from_expr
    #if listexp_from_expr!=0:#RECUPERAR SI FALLA!!!!!!!!!!!!!
    #    raise Exception('Error de sintaxis en "%s": no se permite utilizar expresiones "->list" como elementos en la definicion de una lista'%last_list_expr)    
    #print 'con item_list: %s' % item_list
    #Tiene que ser asi!
    t[0]=t[1]

    

def p_subexp(t):   
    '''subexp : item    
    | LIST LBRACK RBRACK
    | LIST LBRACK subexp_list RBRACK'''
    global item_list,just_append,expr_list,item_list_counter
    #print 'en subexp con item_list:%s'%item_list
    if len(t)==4: #lista vacia
        item_list.append([])#?
        t[0]=[]
    elif len(t)==5:
        #print 'Cierre de un LIST!!'
        #print 'Aqui deberiamos coger los items???'

        #print 'Valor de subexp_list(ultimo elemento): %s\n' % t[3].value

        #print 'item_list:%s' % item_list
        #print 'reduciendo\n'
        #PUEDE ESTAR REPETIDO, OJO!!!!!
        good=index=None       
        if t[3] in item_list:
            #print 'entrando por la entrada normal'
            #print 'indice del ultimo elemento:%s' %item_list.index(t[3])
            indices = [i for i, x in enumerate(item_list) if x ==t[3]]
            #print 'indices completos: %s' % indices
            good=item_list[item_list.index(t[3]):]
            #print 'good:%s' %good
            #expr_list.append(good)
            item_list=item_list[:item_list.index(t[3])]
            item_list.append(good)
        else: #se produce cuando hay un list[list[...
            #print 'por list[list\n'
            #print 'con t[3]: %s'%t[3]
            lst=item_list[:]
            lst.reverse()
#             lst=[]
#             counter=-1
#             while counter > -len(item_list):
#                 lst.append(item_list[counter])
#                 counter-=1
            #print 'lst: %s' % lst
            index=findInSublist(lst,t[3])
            #print 'valor calculado de index: %s' % index
            if index==0:
                index=-1
#             elif index==1:
#                 index=-2
#             elif index==-1:
#                 index=-2                
            else:
                #print 'por la entrada conflictiva'
                #index=0-index#?????????
                if index >0:
                   index=0-index-1
                elif index < 0:#A recuperar si falla
                   index= 0-(-index)-1
            #print 'finding subexp_list:%s' % index
            #print 'item_list: %s' % item_list
            #if index!=-1:
            if index not in[-1,-2]:
                good=item_list[index-1:]
                #print 'good: %s' % good
                item_list=item_list[:index-1]
            else:
                good=item_list[index:]
                #print 'good con listas: %s' % good
                item_list=item_list[:index]                
            item_list.append(good)
        t[0]=t[3]
        #print 'item_list actualizada:%s' % item_list
    else: #item
        #print 'detectado item'
        t[0]=t[1]



        


def p_list_exp_oper(t):
   '''list_exp_oper : ARROW list_expr_st'''
   global listexp_from_expr
   #print 'en list_exp_oper'
   #print 'valor de listexp_from_expr al entrar: %s' % listexp_from_expr
   listexp_from_expr+=1
   #print 'valor de listexp_from_expr al salir: %s' % listexp_from_expr
   t[0]=t[2]        

        

def p_list_definition_st(t):
    #'''list_definition_st : LIST ID IS LBRACK item_list RBRACK
    '''list_definition_st : LIST ID IS list_expr_st
    | LIST ID IS LBRACK  RBRACK
    | LIST ID IS expr EXTRACTOR expr
    | LIST ID IS HTML ID expr opt_attrs opt_text
    | LIST ID IS VAR
    | LIST ID IS expr
    | LIST ID IS linqlike_st
    | LIST ID IS sql_st
    | LIST ID INSERTOR ID'''
    #print 'En list_definition con t[3]: %s'%t[3]
    #print 'En list_definition con t: %s'%[el for el in t]
    #print t[5]
    global item_list
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_list','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_list"'%(t[2],TYPESTAB[t[2]]))
    
    if t[3]=='>>':
        if not t[2] in SYMTAB['__LISTS__']:
            raise Exception('Error: La lista "%s" no esta definida'%t[2])
        if not t[4] in SYMTAB['__LISTS__']:
            raise Exception('Error: La lista "%s" no esta definida'%t[4])
        SYMTAB['__LISTS__'][t[4]].append(SYMTAB['__LISTS__'][t[2]])
    elif len(t)==5: #Definicion a partir de una variable o una expresion o un linqlike_st
        if type(t[4]) in [type(''),type(u'')] and SYMTAB.has_key(t[4]):
            if type(SYMTAB[t[4]])!= type([]):
                raise Exception('Error: La variable "%s" no es una lista' %t[4])
            SYMTAB['__LISTS__'][t[2]]=SYMTAB[t[4]]
        else:
            if t[4]==None: #list_expr_st
                t[4]=decodeList(item_list[:],[])
                item_list=[]
            if type(t[4])!=type([]):
                raise Exception('Error: "%s" no es una lista'%t[4])
            SYMTAB['__LISTS__'][t[2]]=t[4]
            TYPESTAB[t[2]]='t_list'
        #print SYMTAB['__LISTS__'][t[2]]
    elif t[5]=='<<': #Extraccion de nodos XML para la lista(como strings)       
        if not SYMTAB['__XMLS__'].has_key(t[4]):
            raise Exception('Error: El XML %s no esta definido.' %t[4])
        SYMTAB['__LISTS__'][t[2]]=[] #Siempre se crea la lista
        if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
        TYPESTAB[t[2]]='list'        
        source=SYMTAB['__XMLS__'][t[4]]
        pos=xpath.find(t[6], source)
        #print 'Valor de pos: %s' %pos
        #Coger todos los elementos de la lista de nodos
        if type(pos)!=type([]): pos=[pos]
        for node in pos:
            if not hasattr(node,'toxml'):
                raise Exception('Error: La posicion de insercion %s no se corresponde a un nodo.' %node)
            SYMTAB['__LISTS__'][t[2]].append(node.toxml())
        #print SYMTAB['__LISTS__']
            
    elif t[4]=='html':
        global html_text
        global html_attrs      
        if not SYMTAB['__HTMLS__'].has_key(t[5]):
            raise Exception('Error: El HTML %s no esta definido.' %t[5])
        SYMTAB['__LISTS__'][t[2]]=[] #Siempre se crea la lista
        if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
        TYPESTAB[t[2]]='t_list'         
        parts=t[6]
        #print 'parts: %s' %parts
        if len(parts.split(','))!=1:
            parts=parts.split(',')
        if html_text!='':
            elems=SYMTAB['__HTMLS__'][t[5]].findAll(parts, text=html_text)
            #Resetear global
            html_text=''
        elif html_attrs!={}: #Controlar que los valores sean listas o *!!!!!
            elems=SYMTAB['__HTMLS__'][t[5]].findAll(parts, attrs=html_attrs)
            #Resetear global
            html_attrs={}
        else:
            elems=SYMTAB['__HTMLS__'][t[5]].findAll(parts)
        SYMTAB['__LISTS__'][t[2]]=[str(el) for el in elems]

    elif t[5]==']': #Lista vacia
        SYMTAB['__LISTS__'][t[2]]=[]
        if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
        TYPESTAB[t[2]]='t_list'
        item_list=[]
        #print SYMTAB['__LISTS__']

    t[0]=t[2]

def p_item(t):
    '''item : expr
    | linqlike_st
    | id_expr
    | id_funcall'''
    #| LBRACK item_list RBRACK'''
    #print 'en item: %s' % [el for el in t]
    global item_list,just_append,item_list_counter
    item=MiniListItem(t[1])
    if just_append==0 and t[1] is not None:
        item_list.append(item)
    else:
        if t[1] is not None:
            item_list+=[item]
    just_append=0
    t[0]=item

      
def p_id_funcall(t):
    '''id_funcall : IDENTIFIER LPAREN id_expr RPAREN'''
    #Llamamos a una funcion definida en el modulo _functions
    #que debe existir en una tabla functions
    global just_append
    if not SYMTAB['__FUNCTIONS__'].has_key(t[1]):
        raise Exception('Error invocando a la funcion: %s. Esta funcion no esta definida.' %t[1])   
    func=SYMTAB['__FUNCTIONS__'][t[1]]
    target=t[3]
    t[0]=[func(el) for el in target]
    just_append=1

def p_id_expr(t):
    '''id_expr : id_operand id_op id_operand
    | ID
    | ID LBRACK expr COLON expr RBRACK'''
    global item_list,just_append
    t[0]=[]
    #Resolver la expresion y devolver el resultado
    if len(t)==2: #solo ID, append list(puede ser cualquier otra cosa!!!!!)
        if t[1] in SYMTAB['__LISTS__']:
            t[0]=SYMTAB['__LISTS__'][t[1]][:]#Copia!!
        elif t[1] in SYMTAB['__ITERATORS__']: #Iterador como parte de una expr
            t[0]=SYMTAB['__ITERATORS__'][t[1]].getNext()
            just_append=0
        else:
            t[0]=findId(t[1])[0] 
    elif len(t)==7: # list slicing
        if not t[1] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[1])
        t[0]=SYMTAB['__LISTS__'][t[1]][int(t[3]):int(t[5])]#Copia!!
        just_append=1
    #Proceder segun operador (t[2])(solo aceptamos listas!!!)
    elif t[2]=='->':
        #Comprobar que las otras listas existen
        if not t[1] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[1])
        if not t[3] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[3])
        #[id1->id2] mete id1 en id2 como lista
        t[0]=SYMTAB['__LISTS__'][t[1]][:]#Copia!!
        t[0].append(SYMTAB['__LISTS__'][t[3]])
    elif t[2]=='+':
        #[id1+id2] mete todos los elementos de id2 al final de id1
        if not t[1] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[1])
        if not t[3] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[3])        
        t[0]=SYMTAB['__LISTS__'][t[1]][:]#Copia!!
        t[0]=t[0] + SYMTAB['__LISTS__'][t[3]]
        just_append=1
    elif t[2]=='-':
        #[id1-id2] borra todos los elementos de id2 que existan en id1
        if not t[1] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[1])
        if not t[3] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[3])        
        t[0]=SYMTAB['__LISTS__'][t[1]][:]#Copia!!            
        for elem in SYMTAB['__LISTS__'][t[3]]:
           if elem in t[0]:
               del t[0][t[0].index(elem)]
        just_append=1
    elif t[2]=='and':
        #[id1 and id2] interseccion: elementos comunes a id1 e id2
        if not t[1] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[1])
        if not t[3] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[3])            
        for elem in SYMTAB['__LISTS__'][t[1]] + SYMTAB['__LISTS__'][t[3]]:
           if elem in SYMTAB['__LISTS__'][t[1]] and elem in SYMTAB['__LISTS__'][t[3]]:
               if not elem in t[0]:t[0].append(elem)
        just_append=1               
    elif t[2]=='or':
        #[id1 or id2] interseccion: elementos en a o en b sin repeticion
        if not t[1] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[1])
        if not t[3] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[3])            
        for elem in SYMTAB['__LISTS__'][t[1]] + SYMTAB['__LISTS__'][t[3]]:
           if elem in SYMTAB['__LISTS__'][t[1]] or elem in SYMTAB['__LISTS__'][t[3]]:
               if not elem in t[0]: t[0].append(elem)
        just_append=1               
    elif t[2]=='not':
        #[id1 not id2]: elementos que esten en id1 y no esten en id2
        if not t[1] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[1])
        if not t[3] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[3])            
        for elem in SYMTAB['__LISTS__'][t[1]]:
           if elem in SYMTAB['__LISTS__'][t[1]] and not elem in SYMTAB['__LISTS__'][t[3]]:
               t[0].append(elem)
        just_append=1               
    elif t[2] in ['!=','<>']:
        #[id1!=id2] : elementos que esten en una u otra lista, pero no en ambas
        if not t[1] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[1])
        if not t[3] in SYMTAB['__LISTS__']:
            raise Exception('Error: la lista "%s" no esta definida.' % t[3])            
        for elem in SYMTAB['__LISTS__'][t[1]] + SYMTAB['__LISTS__'][t[3]]:
           if elem in SYMTAB['__LISTS__'][t[1]] and not elem in SYMTAB['__LISTS__'][t[3]] or not elem in SYMTAB['__LISTS__'][t[1]] and elem in SYMTAB['__LISTS__'][t[3]]:
               t[0].append(elem)
        just_append=1               


def p_item_list(t):
    '''item_list : item COMMA item_list
    | item'''
    global item_list
    #print 't[1] en item_list: %s' % t[1]
    t[0]=item_list
    #item_list=[]
    

def p_id_op(t):
    '''id_op : ARROW
    | PLUS
    | MINUS
    | AND
    | OR
    | NOT
    | NE
    | COLON'''
    t[0]=t[1]
    

def p_id_operand(t):
    '''id_operand : ID'''
    t[0]=t[1]      

def p_opt_attrs(t):
    '''opt_attrs : ATTRS ID
    | empty'''
    global html_attrs
    if len(t)==3: #Poner la global al valor del diccionario pasado
        html_attrs=SYMTAB['__DICTIONARIES__'][t[2]]
        #Asegurarse de que todas los valores son textos
        #Y cambiar * por True
        for el in html_attrs:
            if html_attrs[el]=='*':
                html_attrs[el]=True
            if type(html_attrs[el]) not in [type(''),type(u'')]:
                html_attrs[el]=str(html_attrs[el])
    t[0]=''

def p_opt_text(t):
    '''opt_text : TEXT STRING
    | empty'''
    global html_text
    if len(t)==3:
        if t[2]=='*': #Cualquier texto
            html_text=True
        else:
            html_text=re.compile(t[2])
    else:
        t[0]=''


def p_list_add_st(t): 
    '''list_add_st : SET list_add_valid PLUS expr
    | SET list_add_valid PLUS expr AS LIST
    | SET list_add_valid PLUS linqlike_st
    | SET list_add_valid PLUS linqlike_st AS LIST
    | SET list_add_valid PLUS sql_st
    | SET list_add_valid PLUS sql_st AS LIST    
    | SET list_add_valid PLUS ID AS LIST
    | SET list_add_valid PLUS ID
    | SET list_add_valid PLUS list_expr_st
    | SET list_add_valid PLUS list_expr_st AS LIST'''    
    global item_list,accesors_list2
    dest=None
    fldn=None
    is_id=0
    is_objfld=0
    #print 'Valor de t[2]: %s' % t[2]
    #print 'accesors_list2: %s' % accesor_list2
    if type(t[2])==type([]):
        dest=t[2]
        if accesor_list2!=[]: #VER SI ESTO ES SEGURO!!!!!!!!!!!!
           accesor_list=[]
    elif t[2] in SYMTAB and type(SYMTAB[t[2]])==type([]):
        dest=SYMTAB[t[2]]

    elif '.' in t[2]:
        is_objfld=1
        dest,fldn=findObjectField(t[2])
        if dest !='this' and not isinstance(dest,MiniObject):
            if not SYMTAB['__OBJECT_INSTANCES__'].has_key(dest):
               raise Exception('Error. El objeto %s no esta definido.' %dest)
            else:
                dest=SYMTAB['__OBJECT_INSTANCES__'][dest]
                                           
    elif type(t[2]) in [type(''),type(u'')] and t[2] in TYPESTAB:
        if TYPESTAB[t[2]]!='t_list':
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_list"'%(t[2],TYPESTAB[t[2]]))
        dest=SYMTAB['__LISTS__'][t[2]]
        is_id=1                     
    else:
        raise Exception('Error: "%s" no es una lista y tiene que serlo'%t[2])        
        
    if is_objfld==0 and len(t)==7: #As list (antes era un elif)
        items=[]
        if is_id==1:
            if type(t[4]) in [type(''),type(u'')] and t[4] in TYPESTAB:
                items=findId(t[4])[0]
            else: #por si es un string
                items=t[4]
        else:
            if type(t[4])==type([]):
                items=t[4]
            elif t[4] in TYPESTAB:
                if TYPESTAB[t[4]]!='t_list':
                    raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_list"'%(t[4],TYPESTAB[t[4]]))
                items=SYMTAB['__LISTS__'][t[4]]
            else:
                raise Exception('Error: "%s" no es una lista y tiene que serlo'%t[4])                 

        if t[2]==t[4]:#con copia temporal
            temp=SYMTAB['__LISTS__'][t[2]][:]
            for item in items:
                temp.append(item)
            SYMTAB['__LISTS__'][t[2]]=temp
        else:
            for item in items:
                dest.append(item)

                
    elif is_objfld==1:
        #CAMBIO PARA PERMITIR THIS------------------------------------------------------------------
        if dest=='this':
            if not SYMTAB['__INSIDE_OBJECT_MACRO__']==1:
                raise Exception('Error: solo se puede usar this dentro de una macro de objeto.')
            else:
                dest=SYMTAB['__MACRO_INSTANCE_OWNER__']
        #FIN CAMBIO PARA THIS-----------------------------------------------------------------------
        private=isPrivate(dest,fldn)
        if isinstance(dest,MiniObject):
            #print 'por aqui!!!'
            if private==0:
                old=getattr(dest,fldn)
                if len(t)==7: #as list
                    old=old + t[4]
                else:
                    old.append(t[4])
                setattr(dest,fldn,old)
            else:
                raise Exception('Error de acceso a campo de objeto. El campo "%s" se ha declarado privado'%fldn)
        else:
            if private==0 or SYMTAB['__INSIDE_OBJECT_MACRO__']==1: #public o via this
                old=getattr(SYMTAB['__OBJECT_INSTANCES__'][dest],fldn)
                if len(t)==7:
                    old=old + t[4]
                else:
                    old.append(t[4])
                setattr(SYMTAB['__OBJECT_INSTANCES__'][dest],fldn,old)
            else:
                raise Exception('Error de acceso a campo de objeto. El campo "%s" se ha declarado privado'%fldn)

            
    elif is_id==1:
        if t[2]==t[4]: #list l1 + l1, necesita una copia temporal
            temp=SYMTAB['__LISTS__'][t[2]][:]
            temp.append(findId(t[4])[0])
            SYMTAB['__LISTS__'][t[2]]=temp
        else:
            if type(t[4]) in [type(''),type(u'')] and t[4] in TYPESTAB:
                SYMTAB['__LISTS__'][t[2]].append(findId(t[4])[0])
            else:
                SYMTAB['__LISTS__'][t[2]].append(t[4])
    else: #Proceder en funcion de t[4]
        #print 't[4]: %s' % t[4]
        if type(t[4])==type([]):
            dest.append(t[4])
        elif t[4] in TYPESTAB:
            if TYPESTAB[t[4]]!='t_list':
                raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_list"'%(t[4],TYPESTAB[t[4]]))
            dest.append(SYMTAB['__LISTS__'][t[4]])
        else:
            raise Exception('Error: "%s" no es una lista y tiene que serlo'%t[4])             
    item_list=[]
    t[0]=1

def p_list_add_valid(t): 
    '''list_add_valid : assignable
    | ID'''
    t[0]=t[1]


def p_iter_definition_st(t):
    '''iter_definition_st : ITERATOR ID FOR id_expr opt_loop
    | ITERATOR ID FOR VAR opt_loop
    | ITERATOR ID FOR expr opt_loop'''
    #Definicion de iterador
    #print SYMTAB['__USED_IDS__']
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_iterator','t_null']:
        raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_iterator"'%(t[2],TYPESTAB[t[2]]))
    global item_list        
    #print t[4]
    val=None
    loop=0
    if t[5]=='loop':
        loop=1
    if type(t[4]) in [type(0),type(0L),type(0.0)]:
        raise Exception('Error: el numero "%s" no es iterable'%t[4])
    elif type(t[4])!=type([]) and t[4][0]=='@': #Variable, comprobar que tiene una list
        static=0
        if isStaticVar(t[4]) and isValidStatic(t[4]):
            static=1
        if static==0 and not SYMTAB.has_key(t[4]):
            raise Exception('Error: la variable "%s" no esta definida'%t[4])
        if static==1:
            val=SYMTAB['__STATICS__'][t[4]]
        else:
            val=SYMTAB[t[4]]
        #print 'val: %s' % val
        if type(val)!=type([]):
           raise Exception('Error: la variable "%s" no contiene una lista'%t[4])
    else:
        if type(t[4])==type([]):
            val=t[4]
        else:
            raise Exception('Error: la expresion "%s" no es una lista'%t[4])
    if loop==0:
        SYMTAB['__ITERATORS__'][t[2]]=MiniIter(val)
    else:
        SYMTAB['__ITERATORS__'][t[2]]=MiniIter(val,loop=1)
    SYMTAB['__USED_IDS__'].append((t[2]))
    TYPESTAB[t[2]]='t_iterator'                
    t[0]=t[2]

def p_opt_loop(t):
    '''opt_loop : LOOP
    | empty'''
    t[0]=t[1]

    

def p_iterator_expr(t):
    '''iterator_expr : ITERATOR ID IS LT id_list2 GT
    | ITERATOR ID IS EXTRACTOR id_list2 INSERTOR'''
##    '''iterator_expr : ITERATOR ID IS LT id_list2 GT
##    | ITERATOR ID IS IDENTIFIER LT id_list2 GT
##    | ITERATOR ID IS LT NUMBER GT imap_oper LT id_list2 GT
##    | ITERATOR ID IS EXTRACTOR id_list2 INSERTOR'''
    #if t[2] in SYMTAB['__USED_IDS__']:
    #    raise Exception('Error: El nombre "%s" ya existe'%t[2]);
    if t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_iterator','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_iterator"'%(t[2],TYPESTAB[t[2]]))
    #global item_list        
    if len(t)==7: #chain(*iterators) <a,b,c> o izip(iterators)<<a,b,c>>
        iters=[]
        for item in t[5].split(','):
            if item not in SYMTAB['__ITERATORS__']:
                raise Exception('Error: El identificador "%s" no se corresponde con un iterador definido'%item)
            if SYMTAB['__ITERATORS__'][item].getLoop()!=0:
                raise Exception('Error: El iterador "%s" se ha definido como iterador circular y no se puede usar en una expresion de iteradores'%item)            
            iters.append(SYMTAB['__ITERATORS__'][item].getIterable())
        if t[4]=='<':
            SYMTAB['__ITERATORS__'][t[2]]=MiniIter(list(itertools.chain(*iters)))
        else:
            SYMTAB['__ITERATORS__'][t[2]]=MiniIter(list([list(e) for e in itertools.izip(*iters)]))
            #print [el for el in SYMTAB['__ITERATORS__'][t[2]].getIterable()]
        SYMTAB['__USED_IDS__'].append((t[2]))
        TYPESTAB[t[2]]='t_iterator'              
##    elif len(t)==8: #imap(*iterators)
##        iters=[]
##        for item in t[6].split(','):
##            if item not in SYMTAB['__ITERATORS__']:
##                raise Exception('Error: El identificador "%s" no se corresponde con un iterador definido'%item)
##            if SYMTAB['__ITERATORS__'][item].getLoop()!=0:
##                raise Exception('Error: El iterador "%s" se ha definido como iterador circular y no se puede usar en una expresion de iteradores'%item)
##            iters.append(SYMTAB['__ITERATORS__'][item].getIterable())
##        if not SYMTAB['__FUNCTIONS__'].has_key(t[4]):
##            raise Exception('Error invocando a la funcion: %s. Esta funcion no esta definida.' %t[4])   
##        func=SYMTAB['__FUNCTIONS__'][t[4]]            
##        mapiter=itertools.imap(func,itertools.chain(*iters))
##        SYMTAB['__ITERATORS__'][t[2]]=MiniIter(list(mapiter))
##        SYMTAB['__USED_IDS__'].append((t[2]))
##        TYPESTAB[t[2]]='t_iterator'       
##    else: #operator(*iterators)
##        iters=[]
##        for item in t[9].split(','):
##            if item not in SYMTAB['__ITERATORS__']:
##                raise Exception('Error: El identificador "%s" no se corresponde con un iterador definido'%item)
##            if SYMTAB['__ITERATORS__'][item].getLoop()!=0:
##                raise Exception('Error: El iterador "%s" se ha definido como iterador circular y no se puede usar en una expresion de iteradores'%item)            
##            iters.append(SYMTAB['__ITERATORS__'][item].getIterable())
##        if not operators_map.has_key(t[7]):
##            raise Exception('Error: El operador "%s" no es uno de los permitidos. Solo se aceptan: +,-,*,/,**'%t[7])
##        func=operators_map[t[7]]
##        #Crear una lista de la misma longitud que el iterable con los argumentos
##        iters=list(itertools.chain(*iters))
##        arglist=[t[5]]*len(iters)
##        #print [el for el in arglist]
##        ziplist=itertools.izip(arglist,iters)
##        #print [el for el in ziplist]
##        zipmapiter=list(itertools.starmap(func,ziplist))
##        SYMTAB['__ITERATORS__'][t[2]]=MiniIter(list(zipmapiter))
##        SYMTAB['__USED_IDS__'].append((t[2]))
##        TYPESTAB[t[2]]='t_iterator'        
    t[0]=t [1]


##def p_imap_oper(t):
##    '''imap_oper : PLUS
##    | MINUS
##    | TIMES
##    | EXP
##    | DIV'''
##    t[0]=t[1]


def p_itertolist_st(t):
    '''itertolist_st : ID EXTRACTOR ID'''
    if not t[1] in SYMTAB['__ITERATORS__']:
        raise Exception('Error: El identificador "%s" no se corresponde con ningun iterador definido'%t[1]);
    if not t[3] in SYMTAB['__LISTS__']:
        raise Exception('Error: El identificador "%s" no se corresponde con ninguna lista definida'%t[3]);
    #Enviar contenido de iterador a la lista
    for i in range(len(SYMTAB['__ITERATORS__'][t[1]])):
        SYMTAB['__ITERATORS__'][t[1]].next()
        SYMTAB['__LISTS__'][t[3]].append(SYMTAB['__ITERATORS__'][t[1]].getNext())
    t[0]=t[2]    


def p_matrix_definition_st(t):
    '''matrix_definition_st : MATRIX ID IS LBRACK item_list RBRACK'''
    #print 'En matrix_definition!'
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_matrix','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_matrix"'%(t[2],TYPESTAB[t[2]]))
    global item_list        
    #global item_list
    SYMTAB['__MATRIXES__'][t[2]]=Matrix(t[5])
    if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
    TYPESTAB[t[2]]='t_matrix'         
    item_list=[]
    #print SYMTAB['__MATRIXES__']
    t[0]=t[2]

def p_tree_definition_st(t):
    '''tree_definition_st : TREE ID IS expr opt_parent'''
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_tree','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_tree"'%(t[2],TYPESTAB[t[2]]))
    global item_list        
##    if t[2] in SYMTAB['__USED_IDS__']:
##        raise Exception('Error: El nombre "%s" ya existe'%t[2]);       
    SYMTAB['__TREES__'][t[2]]=minitree.MiniTree(t[2],t[5],t[4],[])
    if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
    TYPESTAB[t[2]]='t_tree'      
    t[0]=t[2]


def p_graph_definition_st(t):
    '''graph_definition_st : GRAPH ID IS LBRACK nodes_list RBRACK WITH LBRACK graph_elem_list RBRACK'''
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_graph','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_graph"'%(t[2],TYPESTAB[t[2]]))       
##    if t[2] in SYMTAB['__USED_IDS__']:
##        raise Exception('Error: El nombre "%s" ya existe'%t[2]);     
    global graph_nodes_list
    #Poner los nombres en el orden que estan en el programa
    t[5].reverse()
    print 'Lista de nombres_nodo->contenidos: %s' %t[5]
    t[9].reverse()
    print 'Lista de elementos->conexiones: %s' % t[9]
    gr=grafo.Grafo()
    #Crear el grafo:
    #Por ahora no usamos el peso
    nodesids=dict([(item[0],gr.addNodo(item[1],item[0])) for item in t[5] if item[0] not in gr.getNodos(1)])
    #Crear las conexiones
    for item in t[9]:
        actual=nodesids[item[0]]
        #for el in [i.strip() for i in item[1].split(',')]:
        #print 'recorriendo: %s' %item
        for el in item[1].split(','):
            gr.addArco(actual,nodesids[el],item[2])
            #print 'Creando arco entre %s y %s'%(item[0],el)
    SYMTAB['__GRAPHS__'][t[2]]=gr
    if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
    SYMTAB['__USED_IDS__'].append((t[2]))    
    TYPESTAB[t[2]]='t_graph'      
    t[0]=t[2]

def p_nodes_list(t):
    '''nodes_list : ID COLON expr
    | ID COLON expr COMMA nodes_list'''
    global graph_list
    node=[t[1],t[3]]
    graph_list.append(node)
    t[0]=graph_list    

def p_graph_elem_list(t):
    '''graph_elem_list : ID ARROW id_list COLON expr
    | ID ARROW id_list COLON expr COMMA graph_elem_list'''
    global graph_nodes_list
    node=[t[1],t[3],t[5]]
    graph_nodes_list.append(node)
    t[0]=graph_nodes_list
    
    

def p_xml_st(t):
    '''xml_st : XML ID IS expr
    | XML ID IS expr INSERTOR expr
    | XML ID IS expr EXTRACTOR expr'''
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_xml','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_xml"'%(t[2],TYPESTAB[t[2]]))
    global item_list        
    if len(t)==5: #Crear un xml nuevo
        SYMTAB['__XMLS__'][t[2]]=minidom.parseString(t[4])
        if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
        TYPESTAB[t[2]]='t_xml'        
        #print SYMTAB['__XMLS__']
    elif len(t)==7: #Insercion o extraccion
        if t[5]=='>>': #Insertar
            if not SYMTAB['__XMLS__'].has_key(t[2]):
                raise Exception('Error: El XML %s no esta definido.' %t[2])
            if not SYMTAB['__XMLS__'].has_key(t[4]):
                raise Exception('Error: El XML %s no esta definido.' % t[4])

            source=SYMTAB['__XMLS__'][t[4]]
            dest=SYMTAB['__XMLS__'][t[2]]
            pos=xpath.find(t[6], dest)
            #Asegurarse de que pos es un nodo y no es una lista
            if type(pos)==type([]) and pos!=[]:
                pos=pos[0]
            if not isinstance(pos,minidom.Node):
                raise Exception('Error: La posicion de insercion %s no se corresponde a un nodo.' %t[6])
            el=source.firstChild
            pos.appendChild(el)
        if t[5]=='<<': #Extraer sin borrar
            if not SYMTAB['__XMLS__'].has_key(t[4]):
                raise Exception('Error: El XML %s no esta definido.' %t[4])

            source=SYMTAB['__XMLS__'][t[4]]
            pos=xpath.find(t[6], source)
            #Asegurarse de que pos es un nodo y no es una lista. Si se quiere la lista usar list ID is 'xmlname' << 'xpath'
            if type(pos)==type([]) and pos!=[]:
                pos=pos[0]
            if not isinstance(pos,minidom.Node):
                raise Exception('Error: La posicion de extraccion %s no se corresponde a un nodo.' %t[6])
            SYMTAB['__XMLS__'][t[2]]=minidom.parseString(pos.toxml())
            if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
            TYPESTAB[t[2]]='t_xml'            
    else:
        raise Exception('Error procesando el XML "%s"' %t[2])
    
    #print 'Dentro de xml_st!!'
    t[0]=t[2]
    

def p_html_st(t):
    '''html_st : HTML ID IS expr
    | HTML ID IS ID EXTRACTOR expr'''
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_html','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_html"'%(t[2],TYPESTAB[t[2]]))
    global item_list        
    if len(t)==5: #Crear un html nuevo a partir de un string o un archivo o una url
        if t[4].strip().find('http://')==0: #URL: descargarla
            #print 'descargando:%s' %t[4]
            SYMTAB['__HTMLS__'][t[2]]=BeautifulSoup(urllib.urlopen(t[4]).read())
        elif os.path.exists(t[4]):
            SYMTAB['__HTMLS__'][t[2]]=BeautifulSoup(open(t[4]).read())
        else:
            SYMTAB['__HTMLS__'][t[2]]=BeautifulSoup(t[4])
        if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
        TYPESTAB[t[2]]='t_html'            
        #print 'HTMLS:%s' %SYMTAB['__HTMLS__'].keys()
    elif len(t)==7:
        if t[5]=='<<': #Extraer
            if not SYMTAB['__HTMLS__'].has_key(t[4]):
                raise Exception('Error: El HTML %s no esta definido.' %t[4])
            #Cogemos el fragmento definido por la expresion BeautifulSoup t[6]
            #Si hay mas de un fragmento, habra comas y es necesario transformar en una lista
            parts=t[6]
            if len(parts.split(','))!=0:
                parts=parts.split(',')
            #soup.findAll devuelve una lista
            elems=SYMTAB['__HTMLS__'][t[4]].findAll(parts)
            SYMTAB['__HTMLS__'][t[2]]=BeautifulSoup(''.join([str(el) for el in elems]))
            if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
            TYPESTAB[t[2]]='t_html'            
            #print SYMTAB['__HTMLS__'][t[2]]





def p_opt_parent(t):
    '''opt_parent : WITH PARENT ID
    | empty'''
    if len(t)==2: #empty
        t[0]=0
    else:
        if not SYMTAB['__TREES__'].has_key(t[3]):
            raise Exception ('Tree definition error: the tree %s does not exists.' % t[3])
        t[0]=SYMTAB['__TREES__'][t[3]]


def p_pair(t):
    '''pair : expr COLON expr
    | expr ARROW ID'''
    if t[2]=='->':
    	t[0]=(t[1],findId(t[3])[0])
    else:
    	t[0]= (t[1],t[3])


def p_pair_list(t):
    '''pair_list : pair COMMA pair_list
    | pair
    | empty'''
    global pair_list
    for el in t:
        if type(el)==type((1,2)):
            pair_list.append(el)
    t[0]=pair_list

def p_dict_definition_st(t):
    '''dict_definition_st : DICT ID IS LBRACK pair_list RBRACK
    | DICT ID IS VAR'''
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_dict','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_dict"'%(t[2],TYPESTAB[t[2]]))
    global item_list    
    global pair_list
    if len(t)==5: #Contenido de una variable
        SYMTAB['__DICTIONARIES__'][t[2]]=SYMTAB[t[4]]
    else:
        #Convertir la lista de tuplas en un diccionario
        SYMTAB['__DICTIONARIES__'][t[2]]=dict(t[5])
    if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
    TYPESTAB[t[2]]='t_dict'    
    t[0]=t[2]
    pair_list=[]
    #print SYMTAB['__DICTIONARIES__']


def p_instance_definition_st(t):
    '''instance_definition_st : INSTANCE ID IS STRING imports'''
    #print 'Valor Python: %s' % repr(t[4])
    #print 'Valor Python2: %s' % t[4].strip("'")
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_instance','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_instance"'%(t[2],TYPESTAB[t[2]]))      
    temp={}
    if t[5] != None:
        #print repr(t[5].strip("'").split(','))
        for item in t[5].strip("'").split(','):
            imp_code='import ' + item
            #Hay que hacer el update o no se ven los nombres importados!!!!!
            exec imp_code in temp
            SYMTAB['__PY_OBJECTS__'].update(temp)
    #Evaluar la cadena sin las comillas!
    inst_code=t[2] + '=' + t[4].strip("'")
    #print 'ins_code: %s' %inst_code
    exec inst_code in SYMTAB['__PY_OBJECTS__']
    if not t[2] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[2]))
    TYPESTAB[t[2]]='t_instance'    
    #print SYMTAB['__PY_OBJECTS__']
    t[0]=t[2]


def p_imports(t):
    '''imports : IMPORTS STRING
    | empty'''
    if len(t)== 3:
        t[0]=t[2]
    else:
        t[0]=t[1] #empty devuelve None

#-------------------------------------------------------------------------------

def p_condic_expr(t):
    '''condic_expr : condic_expr OR condic_expr
    | and_exp'''
    #print 'Alcanzado condic_expr'
    #print t[0]
    if len(t)==4: #exp or exp
        t[0]=t[1] or t[3]
    else: #and_exp
        t[0]=t[1]    
        

def p_and_exp(t):
    '''and_exp : and_exp AND not_exp
    | not_exp'''
    #print 'Alcanzado and_exp'
    #print 'len(t)=%d' %len(t)
    if len(t)==4: #exp and exp
        t[0]=t[1] and t[3]
        ##print 'haciendo and entre %s y %s' %(t[1],t[3])
    else: #not_exp
        t[0]=t[1]    

def p_not_exp(t):
    '''not_exp : NOT condic_expr
    | LPAREN condic_expr RPAREN
    | bool_exp'''
    #print 'Alcanzado not_exp'
    ##print 'len de t: %s' % len(t)
    if len(t)==3: #not condic_expr
        t[0]=not t[2]
        ##print 'negando %s' % t[2]
    elif len(t)==4: #(condic_expr)
        t[0]=t[2]
    else:
        t[0]=t[1]



def p_bool_exp(t):
    '''bool_exp : expr relop expr
    | expr IN ID
    | expr IN expr
    | expr
    | ID LPAREN RPAREN
    | expr IS ID
    | expr IS REGEX expr'''
    #| LBRACK expr_list RBRACK IS ID'''
    #print 'Alcanzado bool_exp'
    ##print t[1]
    global params_list
    #if len(t)==6: #test de: "lista encaja en tipo?"
    if len(t)>2 and t[2]=='is' and t[3]=='regex':
        if type(t[1]) not in [type(''),type(u'')]:
            raise Exception('Error: para la comprobacion de expresion regular se necesita una cadena y "%s" no lo es'%t[1])
        if re.search(t[4],t[1]):
            t[0]=1
        else:
            t[0]=0
    elif len(t)>2 and t[2]=='is': #test de: "lista encaja en tipo?"        
        if not t[3] in SYMTAB['__TYPEDEFS__']:
            raise Exception('Error: el tipo "%s" no esta definido'%t[3])
        #print 'Detectado test de lista en objeto!!!'
        #print 't[1]: %s' % t[1]
        #print SYMTAB['__TYPEDEFS__'][t[5]]
        kind,template=SYMTAB['__TYPEDEFS__'][t[3]]
        #print 'plantilla:%s'% template
        #Hay que ir probando uno por uno y puede ser recursivo
        #params_list.reverse()
        #print 'params_list:%s' % params_list
        #if len(params_list)!=len(template):
##        if len(t[1])!=len(template):
##            t[0]=0
##        else:
##            #t[0]=listMatchType(params_list,template,kind)
##            t[0]=listMatchType(t[1],template,kind)
        #Si es un valor de una lista, comprobar que sea una lista y que tenga un solo elemento
        if kind==1:
            if type(t[1])!= type([]):
                raise Exception('Error: "%s" no es una lista y tiene que serlo'% t[1])
            else:
                if len(t[1])!=1:
                    raise Exception('Error: Para esta comprobacion (un valor de entre varios posibles), la lista "%s" debe tener un solo elemento'%t[1])
        t[0]=listMatchType(t[1],template,kind)
        #params_list=[]
    elif len(t)>2:
        if t[2]=='==' and t[1]==t[3]:
            t[0]=1
        elif t[2] in ['!=','<>'] and t[1]!=t[3]:
            t[0]=1
        elif t[2]=='<=' and t[1]<=t[3]:
            t[0]=1
        elif t[2]=='>=' and t[1]>=t[3]:
            t[0]=1
        elif t[2]=='>' and t[1]>t[3]:
            t[0]=1
        elif t[2]=='<' and t[1]<t[3]:
            t[0]=1
        elif t[2]=='(': #Comprobacion de un iterador
            if not t[1] in SYMTAB['__ITERATORS__']:
                raise Exception('Error: el identificador "%s" no es un iterador definido'%t[1])
            #print SYMTAB['__ITERATORS__'][t[1]].hasNext()
            if SYMTAB['__ITERATORS__'][t[1]].next():
                #SYMTAB['__ITERATORS__'][t[1]].next()
                t[0]=1
            else:
                t[0]=0
        elif t[2]=='in':
            #Solo se pude usar in con enums, listas, diccionarios y matrixes
            container=t[3]
            #Cambio para permitir usar in con listas y diccionarios no controlados por identificador
            if type(container) in [type([]),type({})]:
                if t[1] in container:
                    t[0]=1
                else:
                    t[0]=0
            #---------------------------------------------------------------------------------------
            elif SYMTAB['__LISTS__'].has_key(container):
                if t[1] in SYMTAB['__LISTS__'][container]:
                    t[0]=1
                else:
                    t[0]=0
                
            elif SYMTAB['__ENUMS__'].has_key(container):
                #if t[1] in range(len(SYMTAB['__ENUMS__'][container])):
                if t[1] in SYMTAB['__ENUMS__'][container]:
                    t[0]=1
                else:
                    t[0]=0
                    
            elif SYMTAB['__DICTIONARIES__'].has_key(container):
                if t[1] in SYMTAB['__DICTIONARIES__'][container].keys():
                    t[0]=1
                else:
                    t[0]=0

            elif SYMTAB['__MATRIXES__'].has_key(container):
                if t[1] in SYMTAB['__MATRIXES__'][container]:
                    t[0]=1
                else:
                    t[0]=0
            #Como ultima oportunidad comprobar que es una subcadena
            #(antes hay que probar que sea un identificador)
            elif type(container) in [type(''),type(u'')]:
                if t[1] in container:
                    t[0]=1
                else:
                    t[0]=0
        else:
            t[0]=0
    else:
        if t[1]:
            t[0]=t[1]
        else:
            t[0]=0
    #print 'en bool_exp t[0]:%s' %t[0]





def p_relop(t):
    '''relop : EQ
    | GT
    | GE
    | LT
    | LE
    | NE'''
    #print 'Alcanzado relop'
    t[0]=t[1]

def p_expr_list(t):
    '''expr_list : expr COMMA expr_list
    | expr
    | empty'''
    global params_list
    #print 'Alcanzado expr_list'
    #print 't[1] en expr_list_nuevo: %s'%t[1]
    #Cambio para poder procesar llamadas a funcion sin argumentos-------------------------
##    if len(t)!=0:
##        for elem in t:
##            if elem!=None and elem!=',': #Hay que aceptar ceros y '' como posibles argumentos!!!!
##                    params_list.append(elem)
    if len(t)!=0:
        if t[1]!=None:
            params_list.append(t[1])
    t[0]=None
    
    
# def p_expr_list(t):
#     '''expr_list : condic_expr COMMA expr_list
#     | condic_expr
#     | empty'''
#     global params_list
#     if len(t)!=0:
#         if t[1]!=None:
#             params_list.append(t[1])
#     t[0]=None    
    
    
    
    

def p_expr(t):
    '''expr : expr PLUS termino
    | expr MINUS termino
    | MINUS expr %prec UMINUS
    | termino    
    | list_exp_oper    
    '''
    #print 'en expr'
    #global listexp_from_expr
    try:
        if t[1]=='-': #uminus
            #t[0]=-t[2]
            t[0]=performOperation(t[2],'-')
        else:
            op=t[2]
            t[0]=performOperation(t[1],op,t[3])
            SYMTAB['_']=t[0]
        #print 't[0] en expr en el try: %s'%t[0]
    except:
        t[0]=t[1]
    #listexp_from_expr-=1#COMENTAR SI FALLA!!!!!!!!!
        #print 'ocurrio una excepcion'
        #print 't[0] en expr en el except: %s'%repr(t[0])
    #print 't[0] en expr: %s'%repr(t[0])
    
        
   
def p_termino(t):
    '''termino : termino TIMES pot_factor
    | termino DIV pot_factor
    | pot_factor'''
    global item_list
    try:
        op=t[2]
        t[0]=performOperation(t[1],op,t[3])
    except:
        t[0]=t[1]
    #print 'Alcanzado termino'
    

def p_pot_factor(t):
    '''pot_factor : factor EXP factor
    | factor'''
    #print 'en pot_factor'
    #
    if len(t)>2:
        t[0]=float(t[1]**t[3])
        ##print 'elevamos %s a %s' % (t[1],t[3])
    else:
        t[0]=t[1]


def p_factor(t):
    '''factor :  assignable
    | LPAREN expr RPAREN
    | ID accesors2
    | VAR accesors2     
    | ID accesors
    | VAR accesors   
    | NUMBER
    | funcall    
    | STRING
    | NULL
    | ID'''
    #| list_exp_oper'''
    #| list_expr_st'''No puede ser asi!!
    #print 'Alcanzado factor %s' %len(t)
    #print 'En factor: %s' % [el for el in t]
    #print 't[1] en factor: %s' %t[1]
    #print 'expr_counter: %s\n' % expr_counter
    #Ver si es una cadena o una variable
    global accesor_list,accesor_list2,item_list,expr_counter
    #print accesor_list
##    if t[1]==None:
##        t[0]=None
##        expr_counter+=1
##        print 'actualizado expr_counter: %s\n' % expr_counter
    if len(t)==3: #Asignacion tipo array []
       #print 'Asignacion tipo array'
       t[2].reverse()# El orden de los accesores esta al reves!!
       if t[1][0]=='@': #variable
            static=0
            if isStaticVar(t[1]) and isValidStatic(t[1]):
                static=1
            if static==0 and not SYMTAB.has_key(t[1]):
                raise Exception('Error: la variable "%s" no esta definida'%t[1])           
           #Proceder por cada elemento de lista de accesores obtenida
            if static==0:
               temp=SYMTAB[t[1]]
            else:
               temp=SYMTAB['__STATICS__'][t[1]]
           #print 'Valor de temp: %s' % temp
       elif SYMTAB['__LISTS__'].has_key(t[1]):
           #print 'Entrando por listas!'
           #Proceder por cada elemento de lista de accesores obtenida
           temp=SYMTAB['__LISTS__'][t[1]]
       elif SYMTAB['__DICTIONARIES__'].has_key(t[1]):
           #print 'Entrando por diccionarios'
           #Proceder por cada elemento de lista de accesores obtenida
           temp=SYMTAB['__DICTIONARIES__'][t[1]]
       elif SYMTAB['__MATRIXES__'].has_key(t[1]):
           #print 'Entrando por matrixes'
           #Proceder por cada elemento de lista de accesores obtenida
           temp=SYMTAB['__MATRIXES__'][t[1]].getList()           
       #print 'Temp: %s' % temp
       for item in t[2]:
           #Item puede ser un numero, una cadena, una lista o un dict
           #Probar que sea un dict primero
           #print 'probando item %s' % item
           try:
               #print type(temp[item])
               #if type(temp[item]) in (type(Matrix()),type({}),type(''),type(u''),type([]), type(2),type(2L),type(2.0)):
               temp=temp[item]#OJO!!!!!!!!!!!!!

           except:
                try:
                    #print 'Probando la lista!!'
                    temp=temp[int(item)]
                except:
                   raise Exception('Error: El elemento "%s" no es accesible' % temp)
       t[0]=temp
       #print 't[0] vale:%s'%t[0]
       #Resetear listas de accesores (REVISAR ESTO!!!)
       if accesor_list!=[]:
           accesor_list=[]
       elif accesor_list2!=[]:
           accesor_list2=[]
    elif len(t)==2: #no es (expr)
        #print 'valor de t[1] en factor: %s' %t[1]
        if type(t[1]) in [type(''),type(u'')] and t[1]=='null': ###OJO, REVISAR ESTE CAMBIO MUY BIEN!!!!!!!!!
            t[0]=SYMTAB['__NULL__']
            #print 'Asignando un null!!'

        elif type(t[1])==type([]) and t[1]!=[] and isinstance(t[1][0],MiniObject):
            #print 'ACCESO A CAMPO DE OBJETO CON INSTANCIA: %s'%t[1]
            #1.- Obtener el valor del campo
            t[0]=findObjectFieldFromInst(*t[1]) #Cambio para permitir cadenas de acceso a objetos

            #CAMBIO PARA PERMITIR THIS------------------------------------------------------------------
##            if objn=='this':
##                if not SYMTAB['__INSIDE_OBJECT_MACRO__']==1:
##                    raise Exception('Error: solo se puede usar this dentro de una macro de objeto.')
##                else:
##                    objn=SYMTAB['__MACRO_INSTANCE_OWNER__']
            #FIN CAMBIO PARA THIS-----------------------------------------------------------------------             
        elif type(t[1]) in [type(''),type(u'')] and t[1] in SYMTAB['__ITERATORS__']:
            itval=findId(t[1])
            t[0]=itval[0].getNext()           
        elif type(t[1])in [type(''),type(u'')] and t[1]!='(' and t[1]!=')':
            if t[1]=='' or t[1]==u'' or t[1]=='.': #Cadena vacia o un punto!!
                t[0]=t[1]
            elif t[1][0]=='@': #VAR
                static=0
                if isStaticVar(t[1]) and isValidStatic(t[1]):
                    static=1
                if static==0 and not SYMTAB.has_key(t[1]):
                    raise Exception('Error: la variable "%s" no esta definida'%t[1])
                if static==0:
                    t[0]=SYMTAB[t[1]]
                else:
                    t[0]=SYMTAB['__STATICS__'][t[1]]

                      
            #Cambio para acceder a campos de objetos---------------------
            elif '.' in t[1] and t[1][0] not in ["'",'"'] and t[1].split('.')[0] in SYMTAB['__OBJECT_INSTANCES__'].keys() + ['this']: #Acceso a campo de objeto
                #print t[1]
                #print 'ACCESO A CAMPO DE OBJETO: %s'%t[1]
                #1.- Obtener el nombre del objeto y el del campo
                #print t[1]
                #objn,fldn=t[1][1:].split('.')
                #objn,fldn=t[1].split('.')
                objn,fldn=findObjectField(t[1]) #Cambio para permitir cadenas de acceso a objetos


                #CAMBIO PARA PERMITIR THIS------------------------------------------------------------------
                if objn=='this':
                    if not SYMTAB['__INSIDE_OBJECT_MACRO__']==1:
                        raise Exception('Error: solo se puede usar this dentro de una macro de objeto.')
                    else:
                        objn=SYMTAB['__MACRO_INSTANCE_OWNER__']
                #FIN CAMBIO PARA THIS-----------------------------------------------------------------------

                
                #print objn
                #print fldn
                #2.- Asignar el valor del campo a la expresion
                private=isPrivate(objn,fldn)
                if isinstance(objn,MiniObject):
                    if private==0:
                        t[0]=getattr(objn,fldn)
                    else:
                        raise Exception('Error de acceso a campo de objeto. El campo "%s" se ha declarado privado'%fldn)
                else:
                    if private==0 or SYMTAB['__INSIDE_OBJECT_MACRO__']==1: #public o via this
                        t[0]=getattr(SYMTAB['__OBJECT_INSTANCES__'][objn],fldn)
                    else:
                        raise Exception('Error de acceso a campo de objeto. El campo "%s" se ha declarado privado'%fldn)
                #print 't[0] en acceso a campo: %s' %t[0]
            #Fin cambio----------------------------------------------------
                
            elif type(t[1]) in [type(''),type(u'')]: #Es un string
                #print 'cadena segun viene: %s' %t[1]
                #if len(t[1])>=4: print t[1][:4]
                if t[1][:4]=='''""\'\'''': #Cadena ""'' ... ''""
                    t[0]=t[1].lstrip('""\'\'')
                    t[0]=t[0].rstrip('\'\'""')                   
                elif t[1][0]=="'": #Cadena normal
                    t[0]=t[1].strip("'")
                elif t[1][0]=='"': #Cadena normal
                    t[0]=t[1].strip('"')
                else:
                    t[0]=t[1]
##                else: #Cadena ""'' ... ''""
##                    t[0]=t[1].lstrip('""\'\'')
##                    t[0]=t[0].rstrip('\'\'""')
                #print 'cadena modificada: %s' % t[0]

                #Aplicar encodings------------------------
                if t[0] and not isinstance(t[0],unicode):
                    t[0]=unicode(t[0],locale.getdefaultlocale()[1],'replace').encode(SYMTAB['__ENCODING__'],'replace')
                    #t[0]=t[0].encode(SYMTAB['__ENCODING__'],'replace')
                else:
                    t[0]=safe_unicode(t[0])
                    t[0]=t[0].encode(SYMTAB['__ENCODING__'],'replace')
                #-----------------------------------------
                   
                
        elif type(t[1])==type(3) or type(t[1])==type(3.0) or type(t[1])==type(1000000000000000):#int,long,float=>numero
            #print 'Tipo reconocido como numero!!'
            t[0]=t[1]
        else: #Asignar una lista, diccionario o cualquier instancia!!!
            #print 'asignando lo que sea'
            t[0]=t[1]             
    else: #(expr)
        t[0]=t[2]
    #print 't0 en factor: %s' %str(t[0])



def p_accesors(t):
    '''
    accesors : LBRACK expr RBRACK accesors
    | LBRACK expr RBRACK
    '''
    global accesor_list
    #print 'En accesors'
    #Hay que generar una lista con los accesores necesarios
    accesor_list.append(t[2])
    t[0]=accesor_list

def p_accesors2(t):
    '''
    accesors2 : LBRACK expr RBRACK accesors2
    | LBRACK expr RBRACK
    '''
    global accesor_list2
    #print 'En accesors2'    
    #Hay que generar una lista con los accesores necesarios
    accesor_list2.append(t[2])
    t[0]=accesor_list2    

def p_funcall(t):
    '''funcall : IDENTIFIER LPAREN expr_list RPAREN'''
    #print 'nombre de funcion: %s' % t[1]
    global params_list
    #print 'args en funcall nuevo: %s' % params_list
    if not SYMTAB['__FUNCTIONS__'].has_key(t[1]):
        raise Exception('Error invocando a la funcion: %s. Esta funcion no esta definida.' %t[1])
    func=SYMTAB['__FUNCTIONS__'][t[1]]
    #Hay que invertir la lista de parametros
    params_list.reverse()
    #Hay que hacer una copia para tener param_list vacio en las llamadas a runMiniCode!!!!!
    fargs=params_list[:]
    params_list=[]
    t[0]=func(*fargs)
    
def p_empty(t):
    '''
    empty : 
    '''
    ##print 'Regla vacia'
    pass

def p_id_list(t):
    '''id_list : ID
    | ID COMMA id_list
    | expr'''
    try:
        t[0]=t[1] + t[2] + t[3]
    except:
        t[0]=t[1]

def p_id_list2(t):
    '''id_list2 : ID
    | ID COMMA id_list2'''
    try:
        t[0]=t[1] + t[2] + t[3]
    except:
        t[0]=t[1]



def p_prolog_st(t):
    '''prolog_st : PROLOG ID IS expr'''
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_prolog','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_prolog"'%(t[2],TYPESTAB[t[2]]))          
##    if t[2] in SYMTAB['__USED_IDS__']:
##        raise Exception('Error: El nombre "%s" ya existe'%t[2]);    
    #Compilar a Python el fragmento de PROLOG pasado y almacenarlo
    #en SYMTAB['__PROLOGS__']
    SYMTAB['__PROLOGS__'][t[2]]=t[4]
    SYMTAB['__USED_IDS__'].append(t[2])
    TYPESTAB[t[2]]='t_prolog'    
    t[0]=t[1]

def p_consult_st(t):
    '''consult_st : CONSULT ID WITH expr consult_dest
    | CONSULT ID WITH expr'''
    if SYMTAB['__BASECONS__'].has_key(t[2]): #Experto mini
        results=MotorInferencia(SYMTAB['__BASECONS__'][t[2]]).query(t[4])
        #Poner a None la instancia unica del experto??
        SYMTAB['__EXPENGINE__']=None
        if len(t)==6:
             SYMTAB['__DICTIONARIES__'][t[5]]['results']=results
    else:
        #Prolog. Comprobar que el programa existe
        if not SYMTAB['__PROLOGS__'].has_key(t[2]):
            raise Exception('Error: El programa prolog "%s" no esta definido.' % t[2])
        code=SYMTAB['__PROLOGS__'][t[2]]
        code+=t[4]
        code=code.strip()
        #print 'codigo:%s' %code.split('\n')
        env = [] #??
        result_list=[]
        for sent in code.split('\n') :
            if sent == "" : continue
            #s = re.sub("#.*","",sent[:-1]) # clip comments and newline
            s=sent
            s = re.sub(" is ","*is*",s)    # protect "is" operator
            s = re.sub(" ", "" ,s)           # remove spaces
            if s == "" : continue
            #print s
            if s[-1] in '?.' : punc=s[-1]; s=s[:-1]
            else: punc='.'

            #print 'punc: %s' %punc
            if punc == '?' :
                #print 'consultando... con %s'%s
                result_list=prolog3.search(prolog3.Term(s))
            else:
                #print 'anyadiendo regla... %s'%s
                prolog3.rules.append(prolog3.Rule(s))
        #print 'result_list: %s' %result_list
        #Devolver las soluciones en un diccionario
        solutions={}
        for item in result_list:
            if type(item)==type({}):
                for k in item:
                    if not solutions.has_key(k):
                        solutions[k]=[item[k]]
                    else:
                        solutions[k].append(item[k])
            else: #Hay un Yes o similar
                solutions['default']=item
        SYMTAB['__DICTIONARIES__'][t[5]]=solutions
    t[0]='1' #t[1].strip()+'___'

def p_consult_dest(t):
    '''consult_dest : IN ID'''
    if not SYMTAB['__DICTIONARIES__'].has_key(t[2]):
        raise Exception('Error: El diccionario "%s" no esta definido' %t[2])
    t[0]=t[2]


def p_sexpr_st(t):
    '''sexpr_st : SEXPR ID IS expr'''
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_sexpr','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_sexpr"'%(t[2],TYPESTAB[t[2]]))          
    if t[2] in SYMTAB['__USED_IDS__']:
        raise Exception('Error: El nombre "%s" ya existe'%t[2]);    
    SYMTAB['__SEXPRS__'][t[2]]=t[4]
    SYMTAB['__USED_IDS__'].append(t[2])
    TYPESTAB[t[2]]='t_sexpr'    
    t[0]=t[1]

def p_pcode_st(t):
    '''pcode_st : PCODE ID IS expr'''
    if not t[2] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%t[2])
    elif t[2] in TYPESTAB and TYPESTAB[t[2]] not in ['t_pcode','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_pcode"'%(t[2],TYPESTAB[t[2]]))          
    if t[2] in SYMTAB['__USED_IDS__']:
        raise Exception('Error: El nombre "%s" ya existe'%t[2]);    
    SYMTAB['__PCODES__'][t[2]]=t[4]
    SYMTAB['__USED_IDS__'].append(t[2])
    TYPESTAB[t[2]]='t_pcode'    
    t[0]=t[1]

####----------------------------------------------------------------------------------
####                         EXTENSIONES LINQ-LIKE
####----------------------------------------------------------------------------------
def p_linqlike_st(t):
    '''linqlike_st : FROM origin SELECT attr_list where_list groupby orderby'''
    global attrs_list
    global linqresult_list
    global group_list
    global where_list
    global order_list
    global order_type
    #print TYPESTAB
    #Hay que dar la vuelta a la lista de atributos
    attrs_list.reverse()
    attr_pos={}
    #print 'lista de atributos: %s' %attrs_list
    
    #----------------------------------------------------------------------
    #Comprobar lista de atributos: No puede haber campos repetidos
    #salvo que tengan distintas funciones de agregado.
    #Si hay una o mas funciones de agregado, debe existir groupby
    #y debe estar ese campo en la lista del groupby
    has_functions=0
    func=''
    fpos=-1
    flds=[]
    for el in attrs_list:
        #print 'checking: %s' %el
        if el[0] in flds:
            raise Exception('Error: el campo "%s" ya se ha usado. No se permiten campos duplicados en los campos de seleccion'%el[0])
        flds.append(el[0])
        if el[2]!='':
            has_functions+=1
            func=el[2]
            #print 'func:%s' % func
            fpos=el[1]
            #print 'Hay funciones de agregado'
    if has_functions > 1:
        raise Exception('Error: Solo se acepta una funcion de agregado en los campos de seleccion y hay %s'%has_functions)
    if has_functions==1 and group_list==[]:
        raise Exception('Error: Si se usa una funcion de agregado en los campos de seleccion hay que usar obligatoriamente una sentencia groupby')
    #-----------------------------------------------------------------------
    
    #1.-Obtener la secuencia a iterar
    iter_type=None
    seq=None
    #print 'Valor de t[2]: %s' %t[2]
    if type(t[2])!=type([]):
        iter_type=TYPESTAB[t[2]]
        #print 'tipo del iterable: %s' %iter_type
        if iter_type not in ['t_list','t_dict','t_matrix']:
            raise Exception('Error: "%s" no es un tipo iterable valido'%iter_type)
    else:
        seq=t[2]
    flds=[]
    conds=where_list  #t[5]
    #Hay que dar la vuelta a las condiciones (usamos and y  el orden importa)
    conds.reverse()
    #print 'lista de condiciones: %s' %where_list
    if iter_type=='t_list':
       seq=SYMTAB['__LISTS__'][t[2]]
    elif iter_type=='t_dict': #resto de casos
        seq=SYMTAB['__DICTIONARIES__'][t[2]].values()
    elif iter_type=='t_matrix': #?????
        seq=SYMTAB['__MATRIXES__'][t[2]].getList()
    #print 'secuencia: %s'% seq
    for item in seq:
        #print 'Recorriendo item: %s' % item
        if isinstance(item,MiniObject):
            condsOk=1
            for at in attrs_list:
                #print 'buscando campo: %s' % at
                if not hasattr(item,at[0]):
                    raise Exception('Error: El objeto no contiene la propiedad "%s"'%at[0])                                 
                condsOk=satisfyConditions(conds,item,at[0])
                #print 'Valor de condsOk: %s' % condsOk
                if condsOk==0: #optimizacion?
                    break                
                flds.append(getattr(item,at[0]))
            if flds!=[] and condsOk==1:
                linqresult_list.append(flds)
            flds=[]
        elif type(item)==type({}):
            for at in attrs_list:
                if at[0] not in item:
                   raise Exception('Error: El diccionario no contiene la clave "%s"'%at[0])
                condsOk=satisfyConditions(conds,item,at[0])
                #print 'Valor de condsOk: %s' % condsOk
                if condsOk==0: #optimizacion?
                    break                
                flds.append(item[at[0]])
            if flds!=[] and condsOk==1:
                linqresult_list.append(flds)
            flds=[]
        elif type(item)==type([]):
            #print 'indices para las listas: %s' % attrs_list
            #print 'item: %s' % item
            #print 'attrs_list: %s' % attrs_list
            for at in attrs_list:
                #print 'probando at: %s' %at
                if at[1] >=len(item):
                      raise Exception('Error: el indice "%s" esta fuera del rango de la lista'%at[1])
                condsOk=satisfyConditions(conds,item,at)
                #print 'Valor de condsOk: %s' % condsOk
                if condsOk==0: #optimizacion?
                    break                
                flds.append(item[at[1]])
            if flds!=[] and condsOk==1:
                linqresult_list.append(flds)
            flds=[]            
        else:
            raise Exception('Error: Las sentencias Linq-like solo se pueden aplicar a instancias de objetos, listas y diccionarios')
    #print 'resultados: %s' %linqresult_list
    #Comprobar si hay que agrupar los datos
    table={}
    mtx=Matrix(linqresult_list[:])
    if group_list!=[]:
        #Dar la vuelta a la lista
        group_list.reverse()
        filt_values=[]
        #print 'group_list: %s' %group_list
        #print 'Hay que agrupar los resultados'
        #print mtx.toString()
        #Los campos del groupby deben ser menores o iguales a los atributos
        if len(group_list)>len(attrs_list):
            raise Exception('Error: El numero de campos en groupby debe ser igual o menor que el numero de campos seleccionados por el select')
        for el in group_list:
            if type(el[1]) not in [type(''),type(u''),type(0),type(0L),type(0.0)]:
                raise Exception('Error: no se puede usar groupby con elementos que no sean cadenas o numeros')
            if el[0] not in [e[0] for e in attrs_list]:
                raise Exception('Error: El campo "%s" no esta incluido en los campos de seleccion. Solo se puede usar groupby con campos incluidos en los campos de seleccion'%el[0])
            filt_values.append(list(set(mtx.getCol(el[1]))))
        #print 'filt_values: %s' % filt_values
        groupbyTable(table,filt_values,0)
        #print 'TABLE : %s' %table
        processGroupbyRows(mtx,table,group_list)
        #print 'TABLE DESPUES DE CONTAR: %s' %table
        m2=[]
        groupbyToRows(table,m2,[])
        #print 'RECONVERTIDO:'
        #pprint.pprint(m2)
        #t[0]=m2
        #RESOLVER AQUI FUNCIONES NO COUNT!!!!!!!
        numfilas=len(m2)
        #print 'numero de filas obtenidas: %s' %numfilas
        #print 'funcion a aplicar: %s' %func
        #print 'posicion afectada en las filas: %s' %fpos
        if fpos >= len(m2[0]): fpos=len(m2[0])-1
        #proceder segun funcion(PERMITIMOS FUNCIONES AGRUPADAS: MAXMIN,SUMCOUNT,SUMAVG???)
        #estadisticos??
        s=v=sp=vp=m=max=min=count=recorr=None
        #Entrar en el for SOLO SI HAY ALGO (len!=0)
        for it in m2:
            #print 'buscando funcion a aplicar...'
            #print 'func: %s' % func
            #print 'it[fpos]: %s'%it[fpos]
            if isinstance(it[fpos],GroupItem):
                if func=='count':
                    it[fpos]=it[fpos].count
                elif func=='sum':
                    it[fpos]=it[fpos].value
                elif func=='avg':
                    it[fpos]=(it[fpos].value)/(it[fpos].count)
                elif func=='var':
                    sumx=reduce(lambda x,y:x+y,it[fpos].items)
                    n=it[fpos].count
                    m=sumx/n                
                    sumx2=reduce(lambda x,y:x+y,[(i-m)**2 for i in it[fpos].items])
                    if n>1:
                        it[fpos]=sumx2/(n-1)
                    else:
                        it[fpos]=sumx2/n
                elif func=='std':
                    sumx=reduce(lambda x,y:x+y,it[fpos].items)
                    n=it[fpos].count
                    m=sumx/n                
                    sumx2=reduce(lambda x,y:x+y,[(i-m)**2 for i in it[fpos].items])
                    if n>1:
                        it[fpos]=math.sqrt(sumx2/(n-1))
                    else:
                        it[fpos]=math.sqrt(sumx2/n)                    
                elif func=='varp':
                    sumx=reduce(lambda x,y:x+y,it[fpos].items)
                    n=it[fpos].count
                    m=sumx/n              
                    sumx2=reduce(lambda x,y:x+y,[(i-m)**2 for i in it[fpos].items])
                    it[fpos]=sumx2/n
                elif func=='stdp':
                    sumx=reduce(lambda x,y:x+y,it[fpos].items)
                    n=it[fpos].count
                    m=sumx/n              
                    sumx2=reduce(lambda x,y:x+y,[(i-m)**2 for i in it[fpos].items])
                    it[fpos]=math.sqrt(sumx2/n)               
                elif func=='max':
                    it[fpos]=it[fpos].max
                elif func=='min':
                    it[fpos]=it[fpos].min
            #Cambiar el ultimo elemento si es un objeto por su campo count
            if isinstance(it[-1],GroupItem):
                it[-1]=it[-1].count
        t[0]=m2
    else:
        t[0]=linqresult_list[:]

    #Aplicar orderby si es preciso        
    #Crear un heap con el campo por el que se quiere ordenar (valido para mas de un campo??)
    #y recuperar la lista ordenada
    if order_list !=[]:
        heap=[]
        for el in t[0]:
            aux=[]
            for a in order_list:
                aux.append(el[a])
            aux.append(el)
            heapq.heappush(heap,aux)
        t[0]=[heapq.heappop(heap)[-1] for i in range(len(heap))]
        #invertir si es preciso
        if order_type=='desc':
            t[0].reverse()
    #-------------------------------------------------------
    
    #Limpieza
    attrs_list=[]
    linqresult_list=[]
    where_list=[]
    group_list=[]
    order_list=[]
    having_list=[]
    order_type=''
    

def p_origin_st(t):
    '''origin : ID
    | LPAREN linqlike_st RPAREN'''
    if len(t)==4:
        t[0]=t[2]
    else:
        t[0]=t[1]
    #print 't[0] en origin: %s' %t[0]

 
def p_attr_list_st(t):
    '''attr_list : attr COMMA attr_list
    | attr'''
    global attrs_list
    attrs_list.append(t[1])
    t[0]=t[1]
    

def p_attr_st(t):
    '''attr : ID
    | ID AS NUMBER
    | ID LPAREN ID RPAREN
    | ID LPAREN ID RPAREN AS NUMBER
    | COUNT LPAREN ID RPAREN
    | COUNT LPAREN ID RPAREN AS NUMBER'''
    global attrs_list
    funcs=['count','sum','avg','std','stdp','var','varp','max','min']
    if len(t)==7:
        if not t[1]in funcs:
            raise Exception('Error: "%s" no es una funcion de agregado permitida. Solo se aceptan "%s"'%(t[1],", ".join(funcs)))
        t[0]=[t[3],t[6],t[1]]
    elif len(t)==5:
        if not t[1]in funcs:
            raise Exception('Error: "%s" no es una funcion de agregado permitida. Solo se aceptan "%s"'%(t[1],", ".join(funcs)))        
        t[0]=[t[3],-1,t[1]]
    elif len(t)==4:
        t[0]=[t[1],t[3],'']
    else:
        t[0]=[t[1],-1,'']
    

def p_where_list_st(t):
    '''where_list : WHERE where_conds
    | empty'''
    global where_list
    t[0]=where_list[:]

def p_where_conds_st(t):
    '''where_conds : condition AND where_conds
    | condition'''
    global where_list
    where_list.append(t[1])
    t[0]=t[1]

def p_condition_st(t):
    '''condition : ID condition_op expr
    | ID IN LBRACK expr_list RBRACK
    | ID NOT IN LBRACK expr_list RBRACK
    | ID BETWEEN expr AND expr
    | ID NOT BETWEEN expr AND expr
    | ID LIKE expr
    | ID NOT LIKE expr
    | ID REGEX expr'''
    global params_list
    if len(t)==4:
        t[0]=[t[1],t[2],t[3]]
    else:
        if t[3]=='[':
            t[0]=[t[1],'in',params_list]
            params_list=[]#??
        elif t[4]=='[':
            t[0]=[t[1],'not in',params_list]
            params_list=[]#??            
        elif t[2]=='between':
            if type(t[3]) not in [type(0),type(0L),type(0.0)]:
                raise Exception('Error: "%s" no es un numero'%t[3])
            if type(t[5]) not in [type(0),type(0L),type(0.0)]:
                raise Exception('Error: "%s" no es un numero'%t[5])             
            t[0]=[t[1],'between',t[3],t[5]]
        elif t[2]=='not' and t[3]=='between':
            if type(t[4]) not in [type(0),type(0L),type(0.0)]:
                raise Exception('Error: "%s" no es un numero'%t[4])
            if type(t[6]) not in [type(0),type(0L),type(0.0)]:
                raise Exception('Error: "%s" no es un numero'%t[6])             
            t[0]=[t[1],'not between',t[4],t[6]]
        elif t[2]=='like':
            if type(t[3]) not in [type(''),type(u'')]:
                raise Exception('Error: "%s" no es un texto'%t[3])
            t[0]=[t[1],'like',t[3]]
        elif t[2]=='not' and t[3]=='like':
            if type(t[4]) not in [type(''),type(u'')]:
                raise Exception('Error: "%s" no es un texto'%t[4])            
            t[0]=[t[1],'not like',t[4]]
        elif t[2]=='regex':
            if type(t[3]) not in [type(''),type(u'')]:
                raise Exception('Error: "%s" no es un texto'%t[3])            
            t[0]=[t[1],'regex',t[3]]            
            

def p_condition_op_st(t):
    '''condition_op : EQUAL
    | GT
    | GE
    | LT
    | LE
    | NE
    | CONTAINS
    | NOT CONTAINS'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + ' ' + t[2]


def p_groupby_st(t):
    '''groupby : GROUPBY id_list3
    | empty'''
    t[0]=1


def p_id_list3(t):
    '''id_list3 : ID AS expr
    | ID AS expr COMMA id_list3'''
    global group_list
    #expr DEBE ser un entero
    if type(t[3]) not in [type(0),type(0L),type(0.0)]:
        raise Exception('Error despues de "%s": El elemento despues del "AS" tiene que ser un numero entero.'%t[3])
    #Hay que saber el orden de la columna por la que
    #filtrar con respecto a la matrix original
    ##COMPROBAR QUE LOS NUMEROS DEL AS SON DISTINTOS!!!!!
    group_list.append([t[1],t[3]])
    t[0]=1
    

def p_orderby_st(t):
    '''orderby : ORDER BY id_list5
    | ORDER BY id_list5 ASC
    | ORDER BY id_list5 DESC
    | empty'''
    global order_type
    if len(t)==5:
        order_type=t[4]
    else:
        order_type='asc'
    t[0]=1

def p_id_list5(t):
    '''id_list5 : ID AS expr
    | ID AS expr COMMA id_list5'''
    global order_list
    order_list.append(t[3])
    t[0]=1    

####----------------------------------------------------------------------------------
####                         EXTENSIONES SQL (SnakeSQL)
####----------------------------------------------------------------------------------

def p_sql_st(t):
    '''sql_st : CREATE DATABASE expr AS ID
    | CONSULT DATABASE ID WITH expr
    | CONSULT DATABASE ID WITH expr AND expr
    | CLOSE DATABASE ID'''
    global objpairs_list #ID DEBE TENER UN TIPO PARA PODER BUSCAR SI EXISTE!!!(t_bdconn)
    resul=[]
    conn=None
    if t[1]=='create':#excepcion si ya existe!!
          #if t[3] in SYMTAB['__CONNECTIONS__']:
          #    raise Exception('Error: la base de datos "%s" ya existe'%t[3])
          if not t[5] in TYPESTAB:
             raise Exception('Error: el identificador "%s" no esta definido'%t[5]) 
          if t[5] in TYPESTAB and TYPESTAB[t[5]] not in ['t_sqlconnection','t_null']:
            raise Exception('Error: El identificador "%s" se ha asociado al tipo "%s" y ya no puede asociarse al tipo "t_list"'%(t[5],TYPESTAB[t[5]]))
    
          if SQLITE_AVAILABLE==1:
              conn=sqlite3.connect(t[3], isolation_level=None)
          else:
              conn=SnakeSQL.connect(t[3],autoCreate=True)
          SYMTAB['__CONNECTIONS__'][t[5]]= conn#t[3]
          if not t[5] in SYMTAB['__USED_IDS__']: SYMTAB['__USED_IDS__'].append((t[5]))
          TYPESTAB[t[5]]='t_sqlconnection'
          #print TYPESTAB
          #print SYMTAB['__CONNECTIONS__']
          #conn.close()
    elif t[1]=='close':
          if not t[3] in  SYMTAB['__CONNECTIONS__']:
            raise Exception('Error: La base de datos "%s" no esta definida'%t[3])
          if SQLITE_AVAILABLE==0:
              SYMTAB['__CONNECTIONS__'][t[3]].close()
          del SYMTAB['__CONNECTIONS__'][t[3]]
    elif t[1]=='consult':
        #print 'consult st'
        if not t[3] in  SYMTAB['__CONNECTIONS__']:
          raise Exception('Error: La base de datos "%s" no esta definida'%t[3])
        conn=SYMTAB['__CONNECTIONS__'][t[3]]
        cursor=conn.cursor()
        res=None
        if len(t)==8: #con lista de parametros
           if SQLITE_AVAILABLE==1:
               #Si es un id que corresponda a una lista lo usamos
               params=None
               if type(t[7])!=type([]):
                  if t[7] in TYPESTAB and TYPESTAB[t[7]]=='t_list':
                     params=SYMTAB['__LISTS__'][t[7]]
                  else:
                     raise Exception('Error: "%s" no es una lista ni un odentificador que corresponda a una lista'%t[7])
               else:
                     params=t[7]
               #res=cursor.executemany(t[5],params)#Esto lleva transacciones!!!!!!
               res=cursor.execute(t[5],params)
           else:
               raise Exception('Error: La consulta con parametros solo esta disponible para bases de datos SQLite')
        else:
           res=cursor.execute(t[5])
        #print 'res: %s' %res
        data=None
        if res:
          data=cursor.fetchall()
          #print 'data: %s' %data
        conn.commit()
        #conn.close()
        if SQLITE_AVAILABLE==1:
            resul=data
        else:
            if type(data)==type((0,)):
                resul=list(data)
        cursor.close()
    #Traducir a SQL y ejecutar lo que se pida
    #Asegurarse de que son listas
    if type(resul)==type([]):
        resul=[list(i) for i in resul]
    t[0]=resul
    #print 't[0]:%s' % t[0]


####----------------------------------------------------------------------------------
####                         EXTENSIONES TQL
####----------------------------------------------------------------------------------

def p_tql_st(t):
    '''tql_st : select_st
    | create_st
    | update_st
    | delete_st
    | insert_st
    | use_st'''
    ##print 'alcanzado nivel de tql_st'
    t[0]=t[1]
    ##print 'to en order %s' % t[0]    


def p_select_st(t):
    '''select_st : select header_opts elementos from procedencia order_opt limit_opt sel_opt format_opt aslist_opt
    | SELECT kind_html expr_html FROM proc_html conds_html'''
    global html_text
    global html_attrs
    global select_as_list
    
    if t[2] in ['html','xml','xhtml']: #Cambio para que el select funcione con HTML y XML
        #print 'proc_html:%s' %t[5]
        #print 'attrs: %s' % html_attrs
        #print 'text: %s' % html_text
        #Lanzar una excepcion si usamos xpath(xml o xhtml) y se han definido attrs o text----------------------------------------------------------
        if t[2]!='html':
            if html_text!='':
                raise Exception('Error: No se puede definir un texto a buscar cuando se usa una expresion xpath (xml o xhtml).')
            if html_attrs!={}:
                raise Exception('Error: No se puede definir un diccionario de atributos buscar cuando se usa una expresion xpath (xml o xhtml).')
        #------------------------------------------------------------------------------------------------------------------------------------------
        textos=''
        for item in t[5].split(','): #Lista de IDs
            if not SYMTAB['__HTMLS__'].has_key(item):
                if not SYMTAB['__XMLS__'].has_key(item):
                    raise Exception('Error: "%s" no esta definido como un HTML o un XML.' %item)
            if t[3]=='*': #Devolvemos todo el fragmento HTML como string
                if t[2]=='html':
                    textos+=str(SYMTAB['__HTMLS__'][item])
                else:
                    textos+=SYMTAB['__XMLS__'][item].toxml()
            else:
                parts=t[3]
                if t[2]=='html' and len(parts.split(','))!=1:
                    parts=parts.split(',')
                #Ver si se han definido attrs y text
                elems=[]
                if html_text!='':
                    if t[2]=='html':
                        elems=SYMTAB['__HTMLS__'][item].findAll(parts, text=html_text)
                    #Restaurar global
                    html_text=''
                elif html_attrs != {}:#Controlar que los valores sean listas o *!!!!!
                    if t[2]=='html':
                        elems=SYMTAB['__HTMLS__'][item].findAll(parts, attrs=html_attrs)
                    #Restaurar global
                    html_attrs={}
                else:
                    if t[2]=='html':
                        elems=SYMTAB['__HTMLS__'][item].findAll(parts)
                    else: #Buscar con una expresion xpath
                        source=SYMTAB['__XMLS__'][item]
                        pos=xpath.find(parts, source)
                        #Asegurarse de que pos es un nodo y no es una lista.
                        if type(pos)==type([]) and pos!=[]:
                            elems=[p.toxml() for p in pos]
                        else:
                            elems.append(pos)
                #if t[2]=='html':       
                textos+=''.join([str(el) for el in elems])
        t[0]=textos
    else:

        global contador
        contador=0
        resultado=[]
        elementos=None
        procedencia=None
        destino=None
        #Averiguamos en cual encaja suponiendo que se cumple
        #la regla mas larga
        #destino=SYMTAB['__DEST__']
        elementos=t[3]
        procedencia=t[5]
        namesust=''
        #Si procedencia es un numero, lo convertimos a string
        if type(procedencia) in [type(0),type(0L),type(0.0)]:
            procedencia=str(procedencia)
        #if type(procedencia)==type(''):
        #    procedencia=[procedencia.strip("'")]    
        #Procedemos segun el valor de ELEMTYPE
        if SYMTAB['ELEMTYPE']==2: #LINE O LINES
            #Hay que tener en cuenta si se ha definido un nuevo separador
            #con un use separator
            #print 'elementos: %s' % str(elementos)
            start=elementos[0]
            #ver si es una tupla (start,end) o solo un numero
            try:
                end=elementos[1]
            except:
                end=None
            #Procedencia puede ser una lista o un string
            if type(procedencia) in [type(''),type(u'')]:
                procedencia=[procedencia]
            for elem in procedencia:
                if SYMTAB['__LINE_SEP__']==r'\n': #separador por defecto,cortamos lineas
                    #lines=open(elem,'r').readlines()
                    lines=getPathText(elem,1)
                else: #Definido por el usuario,hacemos un split
                    ##print 'separador al inicio %s' %SYMTAB['__LINE_SEP__']
                    if not SYMTAB['__USE_REGEX__']:
                        #lines=open(elem,'r').read().split(SYMTAB['__LINE_SEP__'])
                        lines=getPathText(elem).split(SYMTAB['__LINE_SEP__'])
                    else:
                        #--------------------------------------------------------
                        #Cambio para permitir split por expresiones regulares    |
                        #--------------------------------------------------------
                        #lines=open(elem,'r').read()
                        lines=getPathText(elem)
                        r=RegExp(SYMTAB['__LINE_SEP__'])
                        lines=r.split(lines)
                        #Restablecer
                        SYMTAB['__USE_REGEX__']=0
                        #--------------------------------------------------------
                    ##print 'lines %s' % lines
                #Lineas o usuario, seguimos por aqui
                if start >= 0 and start < len(lines):
                    namesust='sust' + str(contador)
                    if end and end <= len(lines):
                        resultado.append({namesust:lines[start:end]})
                        contador+=1
                    else:
                        resultado.append({namesust:lines[start]})
                        contador+=1
                elif start==-1 and end==-1:
                    namesust='sust' + str(contador)
                    resultado.append({namesust:lines[0:]})
                    contador+=1                
        elif SYMTAB['ELEMTYPE']==3: #*
            #Procedencia puede ser una lista o un string
            if type(procedencia) in [type(''),type(u'')]:
                procedencia=[procedencia]            
            for elem in procedencia:
                namesust='sust' + str(contador)
                #resultado.append({namesust:open(elem,'r').read()})
                resultado.append({namesust:getPathText(elem)})
                contador+=1
                        
        elif SYMTAB['ELEMTYPE'] in [0,1]:  #Expresiones regulares  
            sus=SubstitutionsTable()
            for parte in elementos:
                namesust='sust' + str(contador)
                contador+=1
                sus.addSubstitution(namesust,parte.strip("'"))   
            tex=TextExtractor([sus])
            #Procedencia puede ser una lista o un string
            if type(procedencia) in [type(''),type(u'')]:
                procedencia=[procedencia]            
            for parte in procedencia:
                tex.extractFile(parte)
                resultado.append(tex.getExtracts())
                tex.reset()
                        
        
     
        #Convertir a string antes de devolverlo
        #Usamos el separador que haya en SYMTAB
        #y formateamos si es necesario
        #print 'resultado type: %s' % type(resultado)
        #print 'len(resultado): %s'% len(resultado)
        if type(resultado)==type([]): #Puede ser un string si se ha pedido un count
            salida=[]
            for el in resultado:
                for elem in el.values():
                    if type(elem)==type([]):
                        salida+=elem
                    else:
                        salida.append(elem)



            #Comprobar si se ha pedido limite
            #No va con "*" porque se mete un solo elemento en la lista
            if SYMTAB['__LIMIT__']: #and type(resultado)==type([]):
                if SYMTAB['__LIMIT_TYPE__']==1: #ASC
                    if len(salida) > SYMTAB['__LIMIT__']:
                        salida=salida[:SYMTAB['__LIMIT__']]
                elif SYMTAB['__LIMIT_TYPE__']==2: #DESC
                    if len(salida) > SYMTAB['__LIMIT__']:
                        salida=salida[-SYMTAB['__LIMIT__']:]
                #Restablecer variables globales
                SYMTAB['__LIMIT__']=0
                SYMTAB['__LIMIT_TYPE__']=0
                        
            #Comprobar si se ha pedido distinct
            if SYMTAB['__DISTINCT__']:
                ##print 'establecido distinct'
                salida2=[]
                for el in salida:
                    if not el in salida2:
                        salida2.append(el)
                ##print 'salida2: %s' % salida2
                salida=salida2
                #Restablecer flag
                SYMTAB['__DISTINCT__']=0
                

            #Comprobar si hay que ordenarla y como
            if SYMTAB['__ORDER__']:
                salida.sort()
                ##print resultado
                if SYMTAB['__ORDER__']==2:
                    salida.reverse()
                #Restablecer flag de orden
                SYMTAB['__ORDER__']==0
                
                
            #Formateo-----------------------------------------------
            if SYMTAB['__FORMAT__'] and SYMTAB['__LINE_LENGTH__']>10: #Longitud minima para evitar problemas
                #Truquito: usamos un puntero a funcion
                #para evitar los if dentro del bucle

                format_func=None
                if SYMTAB['__FORMAT__']=='left':
                    format_func=string.ljust
                elif SYMTAB['__FORMAT__']=='right':
                    format_func=string.rjust
                elif SYMTAB['__FORMAT__']=='center':
                    format_func=string.center
                if callable(format_func):
                    for i in range(len(salida)):
                        salida[i]=format_func(salida[i],SYMTAB['__LINE_LENGTH__'])
                else:
                    counter=len(re.findall('%s',SYMTAB['__FORMAT__']))
                    if counter==0:
                        raise Exception('Error."%s" no es una expresion de formato valida'%SYMTAB['__FORMAT__'])
                    for i in range(len(salida)):
                        #print tuple([salida[i]]*counter)
                        salida[i]=SYMTAB['__FORMAT__'] %tuple([salida[i]]*counter)
                #Restablecer variables a valores por defecto
                SYMTAB['__FORMAT__']=None
                SYMTAB['__LINE_LENGTH__']=100
            #fin formateo-------------------------------------------


            #Ver si se nos ha pedido un count
            #Si es asi, devolvemos la longitud de la lista
            if SYMTAB['__COUNT__'] or SYMTAB['__STATS__']:
                ##print 'salida en count: %s' %salida
                salida=str(len(salida))
                ##print 'salida convertida en count: %s' %salida
                #Restablecer flags
                SYMTAB['__COUNT__']=0
                resultado=salida
            else:
                if select_as_list==0:                    
                    resultado=SYMTAB['__LINE_JOIN__'].join(salida)
                else:
                    resultado=salida
                    select_as_list=0
        t[0]=resultado


def p_proc_html(t):
    '''proc_html : id_list
    | expr'''
    t[0]=t[1]

def p_kind_html(t):
    '''kind_html : HTML
    | XML
    | XHTML'''
    t[0]=t[1]

def p_expr_html(t):
    '''expr_html : expr
    | TIMES'''
    t[0]=t[1]

def p_conds_html(t):
    '''conds_html : WHERE opt_text
    | WHERE opt_attrs
    | empty'''
    t[0]=t[1]

def p_select(t):
    'select : SELECT'
    #SYMTAB['CUR_ORDER']=0
    t[0]=t[1]

def p_aslist_opt(t):
    '''aslist_opt : AS LIST
    | empty'''
    global select_as_list
    if len(t)>2:
        select_as_list=1
    t[0]=1    

def p_header_opts(t):
    'header_opts : count_opt distinct_opt'
    t[0]=1

def p_count_opt(t):
    '''count_opt : empty
    | COUNT'''
    try:
        if t[1]:
            SYMTAB['__COUNT__']=1
    except:
        SYMTAB['__COUNT__']=0
    t[0]=1


def p_distinct_opt(t):
    '''distinct_opt : empty
    | DISTINCT'''
    try:
        if t[1]=='distinct':
            SYMTAB['__DISTINCT__']=1
    except:
        SYMTAB['__DISTINCT__']=0
    t[0]=1


def p_elementos(t):#REVISAR!!!!!!
    '''elementos : line_sel
    | TIMES
    | expr'''
    #print [el for el in t]
    if type(t[1])==type(''):
        if t[1]=='*':
            SYMTAB['ELEMTYPE']=3 #*
            t[0]=t[1]
        else:
            t[0]=[t[1].strip("'")]
            SYMTAB['ELEMTYPE']=0 #String(expresion regular)
    elif type(t[1]) in [type(0),type(0L)]:
        SYMTAB['ELEMTYPE']=2 #Lines_sel
        t[0]=[t[1]]
    elif type(t[1])==type((0,)):
        SYMTAB['ELEMTYPE']=2 #Lines_sel
        t[0]=t[1]
    else:
        t[0]=[el.strip("'") for el in t[1]]
        SYMTAB['ELEMTYPE']=1 #String_list(lista de regexps)


def p_line_sel(t):
    '''line_sel : LINES LBRACK expr RBRACK
    | LINES LBRACK expr COLON expr RBRACK '''
    if len(t)==5: #si len es 1 es un lines[expr]
        SYMTAB['POS_INSERT']=4
        SYMTAB['CONDIC_DEL']=3
        t[0]=t[3]
    else: #si no es un lines[expr:expr]k
        SYMTAB['POS_INSERT']=5
        SYMTAB['CONDIC_DEL']=4
        t[0]=(t[3],t[5])    


def p_from(t):
    'from : FROM'


def p_procedencia(t):
    '''procedencia : file_list
    | dir_list
    | expr'''
    #print 't[1] en procedencia: %s' % t[1]
    t[0]=t[1] #Revisar la opcion expr!!

        

def p_file_list(t):
    '''file_list : FILES LPAREN expr RPAREN'''
    #Gestionar flags para ordenes que los precisen
    if SYMTAB['CUR_ORDER']==1: #create
        SYMTAB['CREATE_FILES']=1
    elif SYMTAB['CUR_ORDER']==3: #update
        SYMTAB['UPDATE_FILE_LIST']=1
    if type(t[3])!=type([]):
        if type(t[3]) not in [type(''),type(u'')]:
            raise Exception('Error: "%s" no es una lista o un string'%t[3])        
    t[0]=t[3]

        

def p_dir_list(t):
    '''dir_list : DIRS LPAREN expr RPAREN '''
    #Poner a 1 flags para create
    if SYMTAB['CUR_ORDER']==1:
        SYMTAB['CREATE_DIRS']=1
    elif SYMTAB['CUR_ORDER']==3: #update
        SYMTAB['UPDATE_FILE_DIR']=1      
    if type(t[3])!=type([]):
        if type(t[3]) not in [type(''),type(u'')]:
            raise Exception('Error: "%s" no es una lista o un string'%t[3]) 
    dirs=t[3]
    if SYMTAB['CUR_ORDER']in [0,2,4]: #Select,insert,delete
        #Cargar los archivos:
        #Copiar directorios en symtab (para delete)
        SYMTAB['__DIRS__']=dirs
        archs=[]
        for item in dirs:
            fils=os.listdir(item)
            ###print fils
            for fil in fils:
                full_name=item + '/' + fil
                if os.path.isfile(full_name):
                    archs.append(full_name)
        t[0]=archs
    elif SYMTAB['CUR_ORDER']==1:
        ###print 't[0] vale %s' % dirs
        t[0]=dirs    


def p_order_opt(t):
    ''' order_opt : empty
    | ORDER ASC
    | ORDER DESC'''
    try:
        if t[1]:
            if t[2]=='asc':
                SYMTAB['__ORDER__']=1
            elif t[2]=='desc':
                SYMTAB['__ORDER__']=2
    except:
        SYMTAB['__ORDER__']=0


def p_limit_opt(t):
    '''limit_opt : empty
    | LIMIT expr
    | LIMIT expr limit_type'''
    #print [el for el in t]
    if t[1]!=None:
        SYMTAB['__LIMIT__']=int(t[2])
        if len(t)==4:
            if t[3]=='asc':
                SYMTAB['__LIMIT_TYPE__']=1
            else:
                SYMTAB['__LIMIT_TYPE__']=2
        else:
            SYMTAB['__LIMIT_TYPE__']=1
    t[0]=1


def p_limit_type(t):
    '''limit_type : ASC
    | DESC'''
    t[0]=t[1]
        

def p_sel_opt(t):
    '''sel_opt : empty
    | USE SEPARATOR expr regex'''
    if len(t)==5:
        SYMTAB['__LINE_SEP__']=t[3] #.strip("'")  
    t[0]=t[1]

def p_regex(t):
    '''regex : empty
    | REGEX'''
    ##print 't1:%s' %t[1]
    if t[1]:
        SYMTAB['__USE_REGEX__']=1
        ##print 'puesto regex a 1'
    t[0]=t[1]

def p_format_opt(t):
    '''format_opt : empty
    | FORMAT align length_opt'''
    if len(t)>3: #No empty
        SYMTAB['__FORMAT__']=t[2]
        if len(t)==4: #Longitud de linea
            SYMTAB['__LINE_LENGTH__']=int(t[3])


def p_align(t):
    '''align : LEFT
    | RIGHT
    | CENTER
    | expr'''#???
    t[0]=t[1]

def p_length_opt(t):
    '''length_opt : empty
    | expr'''
    t[0]=t[1]   

def p_create_st(t):
    'create_st : create procedencia'
    #if SYMTAB['__NOEXEC__']: return
    #print 'En create_st'
    #print 't[2]: %s' % t[2]
    if type(t[2])==type(''):
        t[2]=t[2].strip("'")
        #creamos el archivo con el path indicado
        try:
            f=open(t[2],'w')
            f.close()
        except:
            pass
    elif SYMTAB['CREATE_FILES']==1:
        for item in t[2]:
            item=item.strip("'").strip()
            f=open(item,'w')
            f.close()
        SYMTAB['CREATE_FILES']=0
    elif SYMTAB['CREATE_DIRS']==1:
        for item in t[2]:
            item=item.strip("'").strip()
            try:
                os.makedirs(item)
            except:
                pass
        SYMTAB['CREATE_DIRS']=0



def p_update_st(t):
    'update_st : update procedencia SET arg_el EQUAL arg_el'
    regx=RegExp(t[4])
    if type(t[2]) in [type(''),type(u'')]:
        if os.path.exists(t[2]) and os.path.isfile(t[2]):
            f=open(t[2],'r')
            text=f.read()
            f.close()
            nuevo=regx.replace(text,t[6])
            f2=open(t[2],'w')
            f2.write(nuevo)
            f2.close()
            t[0]=1
        else:
            t[2]=regx.replace(t[2],t[6])
            t[0]=t[2]
            
    else:
        for el in t[2]: #Elementos devueltos por procedencia
            if os.path.exists(el) and os.path.isfile(el):
                f=open(el,'r')
                text=f.read()
                f.close()
                nuevo=regx.replace(text,t[6])
                f2=open(el,'w')
                f2.write(nuevo)
                f2.close()
                t[0]=1
        t[0]=0


    
def p_delete_st(t):
    'delete_st : delete procedencia condic_del'
    #if SYMTAB['__NOEXEC__']: return
    proced=t[2]
    #print 'proced: %s' % str(proced)
    condic=t[3]
    #print 'condic: %s' % str(condic)
    deltype=SYMTAB['CONDIC_DEL']
    #print 'deltype: %s' % deltype
    dirs=SYMTAB['__DIRS__']
    #Si hay condic,entonces se borra o bien un rango de lineas
    #o bien una o mas expresiones regulares, segun el valor de CONDIC_DEL.
    #Si no, se borran los archivos o los directorios especificados.
    if condic ==None:
        if type(proced)==type([]): #borramos archivos
            for fil in proced:
                os.remove(fil)
        elif type(proced) in [type(''),type(u'')]:
            if os.path.isdir(proced):
                os.removedirs(proced)
            else:
                os.remove(proced)
    else:
        #Corregir que la procedencia sea un string
        if type(proced)==type(''):
            proced=[proced]
        for arch in proced:
            arch=arch.strip()
            txt=''
            if os.path.exists(arch):
                if os.path.isfile(arch):
                    f=open(arch,'r')
                    txt=f.read()
                    f.close()
                else:
                    raise Exception('Error: "%s" no es un archivo valido'%arch)
            else:
                raise Exception('Error: "%s" no es un archivo valido'%arch)
            if deltype in [3,4]: #line_sel
                lines=txt.split('\n')
                start=None
                if type(condic) in [type(0),type(0L),type(0.0)]:
                    start=condic
                else:
                    start=condic[0]
                end=None
                try:
                    end=condic[1]
                except:
                    pass
                if deltype==3:
                    if len(lines)>=start:
                        del lines[start]
                    else:
                        #lanzar excepcion
                        pass
                elif deltype==4:
                    if len(lines)>=start and end and len(lines)>=end and len(lines)>=start:
                        lines=lines[0:start] + lines[end:]
                    else:
                        #lanzar excepcion
                        pass
                txt='\n'.join(lines)
            #Reconstruir el archivo
            f=open(arch,'w')
            f.write(txt)
            f.close()
    #Restablecer flag
    SYMTAB['CONDIC_DEL']=-1
    SYMTAB['__DIRS__']=[]
    t[0]=1
            
        
        
def p_insert_st(t):
    'insert_st : insert expr INTO procedencia WHERE condic_ins'
    proced=t[4]
    #print 'procedencia: %s' %proced
    texto=t[2]
    resultados=[]
    if type(t[2]) not in [type(''),type(u'')]:
        raise Exception('Error: "%s" no es un string y deberia serlo')
    condic=t[6]
    pos=SYMTAB['POS_INSERT']
    #print 'posinsert: %d' %pos
    #Comprobar aqui varlist
    txt=''
    isvarlist=0
    if type(proced) in [type(''),type(u'')]:
        proced=[proced]
    for el in proced:
        #print 'procesando: %s' % el.strip()
        el=el.strip()
        if os.path.exists(el) and os.path.isfile(el):
            #print 'abriendo: %s' %el
            f=open(el,'r')
            txt=f.read()
            f.close()
        else:
            txt=el
        #Insertamos segun valor de pos
        if pos==1: #end
            txt+=texto
        elif pos==0: #begin
            txt=texto + txt
        elif pos==2: #string (Regexp.replace)
            regx=RegExp(condic)
            txt=regx.replace(txt,texto)
        elif pos==3: #stringlist (lista de regex.replace)
            for pat in condic:
                regx=RegExp(pat)
                txt=regx.replace(txt,texto)
        elif pos in [4,5]: #line_sel
            #Si condic tiene mas de un elemento,lanzar una excepcion
            if len(condic)>1:
                return
            else:
                #Transformar el texto en una lista de lineas
                txt=txt.split('\n')
                start=condic[0]
                #Colocar el nuevo texto en el lugar especificado
                #o al final si se pasa
                if start < len(txt):
                    txt.insert(start,texto)
                else:
                    txt.append(texto)
                txt='\n'.join(txt)
        else:
            #Lanzar una excepcion aqui
            pass
        #Poner el nuevo texto en el archivo si procede
        ##print 'guardando texto en archivo'
        if os.path.exists(el) and os.path.isfile(el):
            f=open(el,'w')
            f.write(txt)
            f.close()
        resultados.append(txt)
    t[0]=resultados
    #Restablecer POS_INSERT
    SYMTAB['POS_INSERT']=-1





def p_use_st(t):
    '''use_st : USE JOINER expr'''
    try:
        sep=t[3]#.strip("'")
        if sep==r'\n':
            sep=os.linesep
        SYMTAB['__LINE_JOIN__']=sep
    except:
        pass


def p_create(t):
    'create : CREATE'
    #print 'En create'
    SYMTAB['CUR_ORDER']=1


def p_update(t):
    'update : UPDATE'
    SYMTAB['CUR_ORDER']=3    


def p_delete(t):
    'delete : DELETE'
    SYMTAB['CUR_ORDER']=4
    t[0]=t[1]    


def p_condic_del(t):
    '''condic_del : empty
    | WHERE conds'''
    #print [el for el in t]
    if len(t)==3:
        t[0]=t[2]
    else:
        t[0]=None


def p_conds(t):
    '''conds : line_sel'''
    t[0]=t[1]


def p_insert(t):
    'insert : INSERT'
    SYMTAB['CUR_ORDER']=2
    t[0]=t[1]


def p_condic_ins(t):
    '''condic_ins : BEGIN
    | END
    | line_sel
    | expr'''
    if t[1]=='end':
        SYMTAB['POS_INSERT']=1
    elif t[1]=='begin':
        SYMTAB['POS_INSERT']=0
    elif SYMTAB['POS_INSERT']==-1:
        #Si falla todo lo demas asumimos que es un patron (string)
        SYMTAB['POS_INSERT']=2
    t[0]=t[1]


    
def p_arg_el(t):
    '''arg_el : expr'''
    t[0]=t[1]

####----------------------------------------------------------------------------------
####                         FIN DE EXTENSIONES TQL
####----------------------------------------------------------------------------------


# Error rule for syntax errors
def p_error(t):
    print 'Localizado un error'
    print 'Error evaluando Token: %s' %repr(t)
    print "Error de sintaxis en la entrada!"


# Build the parser
#parser=yacc.yacc(debug=0)

def parserFactory():
    #Generamos el parser con picklefile para evitar el parsetab.py!!
    return yacc.yacc(debug=0,picklefile='parsetab.p')#Poner a debug=0 en produccion

parser=parserFactory()


if __name__=='__main__':
    #print 'Comenzando analisis...'
    import interprete
    SYMTAB['__FUNCTIONS__'].update(interprete.exported_functions) 
    text='''
    
function saluda(%arg)
{
  _write('\nSaludos remotos %arg!!!\n');
  return %arg; 
};

&saluda('Manolo');

@retval=&saluda('Manolo');
'''

    parser.parse(text)
    print 'Terminado.'
        

