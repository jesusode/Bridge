from _globals import SYMTAB,TYPESTAB
import sys
import os

#Cambio para poder crear y usar estructuras C---------------------------
import binstream
#-----------------------------------------------------------------------

#-----------------------------------------------------
#               Manejo de flujos binarios
#-----------------------------------------------------

def binStreamCreate(*args):
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamCreate(name,path)'''
        raise WrongNumberOfArguments(msg)
    if not args[0] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[0])      
    if args[0] in SYMTAB['__USED_IDS__']:
        raise Exception('Error: El nombre "%s" ya existe'%args[0]);        
    SYMTAB['__BINARY_STREAMS__'][args[0]]=binstream.BinaryStream(args[1])
    SYMTAB['__USED_IDS__'].append(args[0])
    TYPESTAB[args[0]]='t_binstream'        
    return 1



def binStreamOpen(*args):
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamOpen(bsname,mode)'''
        raise WrongNumberOfArguments(msg)
    if not args[0] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[0])      
    
    if not SYMTAB['__BINARY_STREAMS__'].has_key(args[0]):
        raise Exception('Error: El flujo %s no esta definido!' %args[0])
    if args[1] not in ['rb','wb']:
        raise Exception('Error: mode debe ser "rb" o "wb". %s no esta permitido' %args[1])
    SYMTAB['__BINARY_STREAMS__'][args[0]].reopen(args[1])
    return 1



def binStreamClose(*args):
    if len(args)!=1:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamClose(bsname)'''
        raise WrongNumberOfArguments(msg)
    if not args[0] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[0])      
    
    if not SYMTAB['__BINARY_STREAMS__'].has_key(args[0]):
        raise Exception('Error: El flujo %s no esta definido!' %args[0])
    SYMTAB['__BINARY_STREAMS__'][args[0]].close()
    return 1




def binStreamDefineStruct(*args):
    if len(args)!=3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamDefineStruct(bsname,struct_name,struct_format)'''
        raise WrongNumberOfArguments(msg)
    if not args[0] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[0])      
    if not args[1] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[1])      
    if not SYMTAB['__BINARY_STREAMS__'].has_key(args[0]):
        raise Exception('Error: El flujo %s no esta definido!' %args[0])
    SYMTAB['__BINARY_STREAMS__'][args[0]].addStruct(args[2],args[1])
    return 1


def binStreamWriteStruct(*args):
    if len(args)!=3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamWriteStruct(bsname,struct_name,struct_fields_list_name)'''
        raise WrongNumberOfArguments(msg)
    if not args[0] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[0])      
    if not args[1] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[1])          
    if not SYMTAB['__LISTS__'].has_key(args[2]):
        raise Exception('Error: La lista %s no esta definida!' %args[2])    
    if not SYMTAB['__BINARY_STREAMS__'].has_key(args[0]):
        raise Exception('Error: El flujo %s no esta definido!' %args[0])
    SYMTAB['__BINARY_STREAMS__'][args[0]].writeStruct(args[1],SYMTAB['__LISTS__'][args[2]])
    return 1


def binStreamReadStruct(*args):
    if len(args)!=3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamReadStruct(bsname,struct_name,struct_fields_list_name)'''
        raise WrongNumberOfArguments(msg)
    if not args[0] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[0])      
    if not args[1] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[1])     
    if not SYMTAB['__LISTS__'].has_key(args[2]):
        raise Exception('Error: La lista %s no esta definida!' %args[2])    
    if not SYMTAB['__BINARY_STREAMS__'].has_key(args[0]):
        raise Exception('Error: El flujo %s no esta definido!' %args[0])
    SYMTAB['__LISTS__'][args[2]]=SYMTAB['__BINARY_STREAMS__'][args[0]].readStruct(args[1])
    return 1


def binStreamGetStructSize(*args):
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamGetStructSize(bsname,struct_name)'''
        raise WrongNumberOfArguments(msg)
    if not args[0] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[0])      
    if not args[1] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[1])     
    if not SYMTAB['__BINARY_STREAMS__'].has_key(args[0]):
        raise Exception('Error: El flujo %s no esta definido!' %args[0])
    return SYMTAB['__BINARY_STREAMS__'][args[0]].getStructSize(args[1])


def binStreamWrite(*args):
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamWrite(bsname,bytes)'''
        raise WrongNumberOfArguments(msg)
    if not args[0] in TYPESTAB:
        raise Exception('Error: el identificador "%s" no esta definido'%args[0])          
    if not SYMTAB['__BINARY_STREAMS__'].has_key(args[0]):
        raise Exception('Error: El flujo %s no esta definido!' %args[0])
    SYMTAB['__BINARY_STREAMS__'][args[0]].write(args[1])
    return 1


exported_functions={
    '_binStreamCreate' : binStreamCreate, #Funciones para flujos binarios
    '_binStreamDefineStruct' : binStreamDefineStruct,
    '_binStreamWriteStruct' : binStreamWriteStruct,
    '_binStreamReadStruct' : binStreamReadStruct,
    '_binStreamOpen' : binStreamOpen,
    '_binStreamClose' : binStreamClose,
    '_binStreamGetStructSize' : binStreamGetStructSize,
    '_binStreamWrite' :binStreamWrite

    }