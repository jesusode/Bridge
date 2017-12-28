from _globals import TYPESTAB
from _globals import SYMTAB
import _globals
import sys
import os

#Excepcion si la plataforma es Java, linux o MacOS
if 'java' in _globals.OSSYSTEM or 'linux2' in _globals.OSSYSTEM or 'darwin' in _globals.OSSYSTEM:
    raise Exception('Error: el modulo mini_dotnet no esta disponible en plataformas Java, Linux o MacOSX')

import preprocessor
from tokenizer import *
from interprete import runMiniCode

#Aplicaciones .NET via Python.NET(.NET 2.0 y superior------
import clr
#print dir(clr)
clr.AddReference('System')
import System
r=clr.AddReference('dyncompiler2')
import dyncompiler2
#print r
#----------------------------------------------------------

#Plantilla para wrappers de eventos .NET-------------
DOTNET_WRAPPER_TEMPLATE="""
def eventWrapper_%%wname%%_%%wevent%%(source,args):
    evt_code='''%%codename%%'''
    runMiniCode(evt_code)
    """

DOTNET_MENU_TEMPLATE="""
def eventWrapper_%%wname%%_%%label%%():
    evt_code='''%%codename%%'''
    runMiniCode(evt_code)
    """
    
#-----------------------------------------------------
#          Uso de objetos .NET
#-----------------------------------------------------

def compileDotNetCode(*args): #OK
    args=list(args)    
    if len(args) !=4: 
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _compileDotNetCode(code_or_string,type,name,target)'''
        raise Exception(msg)
    code=None
    if SYMTAB['__CODES__'].has_key(args[0]):
        code=SYMTAB['__CODES__'][args[0]]
    else:
        code=args[0]
    engine=None
    if args[1] in ['vbnet','VBNET','VB']:
        #print 'codigo a compilar: \n%s' % code
        engine=dyncompiler2.CompileEngine(code,dyncompiler2.LanguageType.VB,'')
    else:
        engine=dyncompiler2.CompileEngine(code,dyncompiler2.LanguageType.CSharp,'')
    return engine.Compile(args[2],args[3])


def addDotNetReferences(*args): #OK
    args=list(args)    
    if len(args) !=1: 
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _addDotNetReferences(list_of_elements)'''
        raise Exception(msg)
    arguments=None
    args_type=0
    reflist=None
    if type(args[0])==type([]):
       reflist=args[0]
    else:
        if not SYMTAB['__LISTS__'].has_key(args[0]):
            raise Exception('Error: la lista "%s" no esta definida' % args[0])
        reflist=SYMTAB['__LISTS__'][args[0]]
    #Hay que hacer un AddReference para cada elemento de la lista
    for el in reflist:
        clr.AddReference(el)
    return 1

def importDotNetPackages(*args): #OK
    args=list(args)    
    if len(args) !=1: 
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _importDotNetPackages(list_of_packages)'''
        raise Exception(msg)
    arguments=None
    args_type=0
    reflist=None
    if type(args[0])==type([]):
       reflist=args[0]
    else:
        if not SYMTAB['__LISTS__'].has_key(args[0]):
            raise Exception('Error: la lista "%s" no esta definida' % args[0])
        reflist=SYMTAB['__LISTS__'][args[0]]
    #Hay que hacer un import para cada elemento de la lista
    for el in reflist:
        #print 'importando: %s' %el
        impstr='import ' + el 
        exec impstr in globals(),locals()
    return 1

def createDotNetObject(*args): #OK
    args=list(args)    
    if len(args) !=2: 
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _createDotNetObject(class_string,options_list_or_dict_name)'''
        raise Exception(msg)
    arguments=None
    args_type=0
    if type(args[1]) in [type([]),type({})]:
        arguments=args[1]
    elif SYMTAB['__LISTS__'].has_key(args[1]):
        arguments=SYMTAB['__LISTS__'][args[1]]
    elif SYMTAB['__DICTIONARIES__'].has_key(args[1]):
        arguments=SYMTAB['__DICTIONARIES__'][args[1]]
    else:
        raise Exception('Error: "%s" no esta definido como lista ni como diccionario' % args[1])
    args[0]+= '(' 
    if type(arguments)==type({}):
        args[0]+='**arguments)'
    else:
        args[0]+='*arguments)'
    return eval(args[0])


def callDotNetFunc(*args): #OK
    args=list(args)    
    if len(args) !=2: 
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _callDotNetFunc(func_string,options_list_or_dict_name)'''
        raise Exception(msg)
    arguments=None
    if type(args[1]) in [type([]),type({})]:
        arguments=args[1]    
    elif SYMTAB['__LISTS__'].has_key(args[1]):
        arguments=SYMTAB['__LISTS__'][args[1]]
    elif SYMTAB['__DICTIONARIES__'].has_key(args[1]):
        arguments=SYMTAB['__DICTIONARIES__'][args[1]]
    else:
        raise Exception('Error: "%s" no esta definido como lista ni como diccionario' % args[1])
    args[0]+= '(' 
    #if args_type==1:
    if type(args)==type({}):
        args[0]+='**arguments)'
    else:
        args[0]+='*arguments)'
    retval=eval(args[0])
    return retval


def callDotNetObjectFunc(*args): #OK
    args=list(args)    
    if len(args) !=3: 
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _callDotNetObjectFunc(obj,func_string,options_list_or_dict_name)'''
        raise Exception(msg)
    arguments=None
    if type(args[2]) in [type([]),type({})]:
        arguments=args[2]        
    elif SYMTAB['__LISTS__'].has_key(args[2]):
        arguments=SYMTAB['__LISTS__'][args[2]]
    elif SYMTAB['__DICTIONARIES__'].has_key(args[2]):
        arguments=SYMTAB['__DICTIONARIES__'][args[2]]
    else:
        raise Exception('Error: "%s" no esta definido como lista ni como diccionario' % args[2])
    if not hasattr(args[0],args[1]):
        raise Exception('Error: el objeto "%s" no tiene definido la funcion "%s"' %(args[0],args[1]))
    f=getattr(args[0],args[1])
    if type(arguments)==type({}):
        return f(**arguments)
    else:
        return f(*arguments)


def setDotNetObjectProp(*args): #OK
    args=list(args)    
    if len(args) !=3: 
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _setDotNetObjectProp(obj,prop_string,value)'''
        raise Exception(msg)
    if not hasattr(args[0],args[1]):
        raise Exception('Error: el objeto .NET "%s" no tiene definida la propiedad "%s"' % (args[0],args[1]))
    setattr(args[0],args[1],args[2])
    return 1


def getDotNetObjectProp(*args): #OK
    args=list(args)    
    if len(args) !=2: 
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _getDotNetObjectProp(obj,prop_string)'''
        raise Exception(msg)
    if not hasattr(args[0],args[1]):
        raise Exception('Error: el objeto .NET "%s" no tiene definida la propiedad "%s"' % (args[0],args[1]))              
    return getattr(args[0],args[1])
    

def bindDotNetEvent(*args): #OK
    args=list(args)    
    if len(args)!=3: 
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _bindDotNetEvent(dotnet_object,event_name,code_name)'''
        raise Exception(msg)
    key=args[1]
    code=args[2]
    ftemplate=DOTNET_WRAPPER_TEMPLATE
    ftemplate=ftemplate.replace('%%wname%%',str(args[0].GetHashCode()))
    ftemplate=ftemplate.replace('%%wevent%%',key)
    ftemplate=ftemplate.replace('%%codename%%',code)
    #print ftemplate
    #Compilarla y asignarla al widget
    fname='eventWrapper_' + str(args[0].GetHashCode()) + '_' + key
    #print fname
    exec ftemplate in globals(),locals()
    #print eval(fname)
    if not hasattr(args[0],key):
        raise Exception('Error: el objeto .NET "%s" no tiene definido el evento "%s"'%(args[0],key))
    delegate=getattr(args[0],key)
    delegate+=eval(fname)    
    return 1



exported_functions={
    '_addDotNetReferences' : addDotNetReferences,
    '_importDotNetPackages': importDotNetPackages,
    '_createDotNetObject' : createDotNetObject,
    '_callDotNetFunc' : callDotNetFunc,
    '_setDotNetObjectProp' : setDotNetObjectProp,
    '_getDotNetObjectProp' : getDotNetObjectProp,
    '_callDotNetObjectFunc' : callDotNetObjectFunc,
    '_bindDotNetEvent' : bindDotNetEvent,
    '_compileDotNetCode' : compileDotNetCode
    }

