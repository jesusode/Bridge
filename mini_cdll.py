from _globals import SYMTAB,TYPESTAB
from  _globals import *
import sys
import os
#Cambio para usar funciones de DLLs C----------------------------
import ctypes
#----------------------------------------------------------------


C_INT_TYPES=['char','wchar_t','unsigned char','short','unsigned short','int','unsigned int','long','unsigned long','long long','unsigned long long']

CTYPES_CONVERSION_TABLE={
    #'char' : ctypes.c_char,
    #'wchar_t' : ctypes.c_wchar,
    'char' : ctypes.c_byte,
    'unsigned char' : ctypes.c_ubyte,
    'short' : ctypes.c_short,
    'unsigned short' : ctypes.c_ushort,
    'int' : ctypes.c_int,
    'unsigned int' : ctypes.c_uint,
    'long': ctypes.c_long,
    'unsigned long' : ctypes.c_ulong,
    'long long': ctypes.c_longlong, 
    'unsigned long long' : ctypes.c_ulonglong,
    'float' : ctypes.c_float,
    'double' : ctypes.c_double,
    'char *' : ctypes.c_char_p,
    #'wchar_t *' : ctypes.c_wchar_p,
    'void *' : ctypes.c_void_p,
    #'mem_ptr': ctypes.create_string_buffer
}


#-----------------------------------------------------
#          Funciones para llamar DLLs C via ctypes
#-----------------------------------------------------

def loadCDLL(*args):
    if len(args)!=2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _loadCDLL(cdllname,call_convention)'''
        raise WrongNumberOfArguments(msg)
    if args[1]=='cdecl':
        return ctypes.CDLL(args[0])
    else:
        return ctypes.WinDLL(args[0])



def callCDLLFunc(*args):
    if len(args)< 3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _callCDLLFunc(dll,funcname,args_list_name)'''
        raise WrongNumberOfArguments(msg)   
    cdll=args[0]
    _args=args[2]
    return getattr(cdll,args[1])(*_args)


if 'win32' in OSSYSTEM:    
    def loadWinDLL(*args):
        if len(args)!=1:
            msg='''Numero incorrecto de argumentos para la funcion.
            La sintaxis correcta es _loadWinDLL(windllname)'''
            raise WrongNumberOfArguments(msg);        
        return getattr(ctypes.windll,(args[0]))



    def callWinDLLFunc(*args):
        if len(args)< 3:
            msg='''Numero incorrecto de argumentos para la funcion.
            La sintaxis correcta es _callWinDLLFunc(wdll,funcname,args_list_name)'''
            raise WrongNumberOfArguments(msg)    
        windll=args[0]
        _args=args[2]
        f=getattr(windll,args[1])
        if len(_args)==0:
            return f(None)
        else:
            return f(*_args)


def createCFuncArguments(*args): #crear SYMTAB['__ARGS_LISTS__'][NAME] y convertir con ctypes a argumentos correctos????
    if len(args)!= 2:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es createCFuncArguments(arg_list,arg_types_list)'''           
        raise WrongNumberOfArguments(msg)
    arg_types=args[0]
    arg_values=args[1]
    ##HAY QUE INCLUIR CODIGO PARA DETECTAR STRUCT NAME Y STRUCT NAME*!!!!!!!!!!!!!!!
    ##QUE PASA CON LOS ARRAYS Y PUNTEROS A FUNCION??????????????
    #Si no tienen la misma longitud, generar una excepcion
    if len(arg_types)!=len(arg_values):
        raise Exception('Error: la lista de argumentos y la lista de valores deben tener el mismo numero de elementos')
    func_args=[]
    contador=0
    for el in arg_types:
        if el in CTYPES_CONVERSION_TABLE:
            _arg=arg_values[contador]
            #Asegurarse de que los enteros son enteros!!
            if type(_arg) in (type(0.0),type(1),type(1L)):
                if el in C_INT_TYPES:
                    _arg=long(_arg)
            func_args.append(CTYPES_CONVERSION_TABLE[el](_arg))
            contador+=1
        else:
            raise Exception('Error: el argumento "%s" no se reconoce como argumento valido' % el)
    return func_args     



exported_functions={
    '_loadCDLL' : loadCDLL, #Manejo de ctypes
    '_createCFuncArguments' : createCFuncArguments,    
    '_callCDLLFunc' : callCDLLFunc }
    
if 'win32' in OSSYSTEM:
    exported_functions.update({
    '_loadWinDLL' : loadWinDLL,
    '_callWinDLLFunc' : callWinDLLFunc})