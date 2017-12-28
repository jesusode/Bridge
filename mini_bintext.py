from _globals import SYMTAB,TYPESTAB
import sys
import os
#Cambio para poder codificar cadenas binarias como texto----------------
import uu
import binascii
import base64
#-----------------------------------------------------------------------

#-----------------------------------------------------
#    Codificacion de archivos binarios como texto
#-----------------------------------------------------
def binaryToTextEncode(*args):
    if len(args) != 3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _binaryToTextEncode(binfile,method,outfile)
        Donde method es uno de:  uu, hex, base64'''
        raise WrongNumberOfArguments(msg)

    binfile=args[0]
    method=args[1]
    outfile=args[2]
    if method.lower()=='uu':
        uu.encode(binfile,outfile)
        return  1
    elif method.lower()=='hex':
        bytes=binascii.hexlify(open(binfile,'rb').read())
        f=open(outfile,'w')
        f.write(bytes)
        f.close()
        return  1
    elif method.lower()=='base64':
        bytes=base64.b64encode(open(binfile,'rb').read())
        f=open(outfile,'w')
        f.write(bytes)
        f.close()        
        return  1
    else:
        return 0

def textToBinaryDecode(*args):
    if len(args) != 3:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _textToBinaryDecode(textfile,method,outfile)
        Donde method es uno de:  uu, hex, base64'''
        raise WrongNumberOfArguments(msg)
    textfile=args[0]
    method=args[1]
    outfile=args[2]
    if method.lower()=='uu':
        uu.decode(textfile,outfile)
        return  1
    elif method.lower()=='hex':   
        bytes=binascii.unhexlify(open(textfile,'r').read())
        f=open(outfile,'wb')
        f.write(bytes)
        f.close()             
        return  1
    elif method.lower()=='base64':
        bytes=base64.b64decode(open(textfile,'r').read())
        f=open(outfile,'wb')
        f.write(bytes)
        f.close()             
        return  1
    else:
        return 0

def crc32(*args):
    if len(args) != 1:
        msg='''Numero incorrecto de argumentos para la funcion.
        La sintaxis correcta es _crc32(text)'''
        raise WrongNumberOfArguments(msg)
    return  binascii.crc32(args[0])



exported_functions={
    '_binaryToTextEncode' : binaryToTextEncode, #Conversion de archivos binarios a texto
    '_textToBinaryDecode' : textToBinaryDecode,
    '_crc32' : crc32
    }