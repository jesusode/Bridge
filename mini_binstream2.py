from _globals import SYMTAB,TYPESTAB
import sys
import os

#Cambio para poder crear y usar estructuras C---------------------------
import binstream
#-----------------------------------------------------------------------

#-----------------------------------------------------
#               Manejo de flujos binarios
#-----------------------------------------------------

def binStreamCreate(*args):  #OK
    if len(args)!=1:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamCreate(path)'''
        raise WrongNumberOfArguments(msg)        
    return binstream.BinaryStream(args[0])



def binStreamOpen(*args):  #OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamOpen(bs,mode)'''
        raise WrongNumberOfArguments(msg)
    if args[1] not in ['rb','wb']:
        raise Exception('Error: mode debe ser "rb" o "wb". %s no esta permitido' %args[1])
    args[0].reopen(args[1])
    return 1



def binStreamClose(*args):  #OK
    if len(args)!=1:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamClose(bs)'''
        raise WrongNumberOfArguments(msg)
    args[0].close()
    return 1


def binStreamDefineStruct(*args):  #OK
    if len(args)!=3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamDefineStruct(bs,struct_name,struct_format)'''
        raise WrongNumberOfArguments(msg)
    args[0].addStruct(args[2],args[1])
    return 1


def binStreamWriteStruct(*args):  #OK
    if len(args)!=3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamWriteStruct(bs,struct_name,struct_fields_list)'''
        raise WrongNumberOfArguments(msg)
    args[0].writeStruct(args[1],args[2])
    return 1


def binStreamReadStruct(*args): #OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamReadStruct(bsname,struct_name)'''
        raise WrongNumberOfArguments(msg)
    return args[0].readStruct(args[1])


def binStreamGetStructSize(*args):  #OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamGetStructSize(bs,struct_name)'''
        raise WrongNumberOfArguments(msg)
    return args[0].getStructSize(args[1])


def binStreamWrite(*args): #OK
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binStreamWrite(bs,bytes)'''
        raise WrongNumberOfArguments(msg)
    args[0].write(args[1])
    return len(args[1])


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