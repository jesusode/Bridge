#!Python

#print __builtins__['open']
from RegExp2 import *
import os
import sys
from _globals import SYMTAB
import copy

import imp
import thread
import re
import pprint


class PreProcessException(Exception):
    pass


class PreProcessor:
    """
    Preprocesador de archivo/cadena de codigo.
    Gestiona los imports y las definiciones/apariciones de macros
    """
    def __init__(self,thr_id=''):
        self.__tid=thr_id
        #Expresion para detectar variables, macros y clases globales ???
        self.__globals='\s*globals\s*([\$|\@]*[a-zA-Z0-9]+)\s*;'
        
        #Definicion de templates de codigo-----------------------------------------------------------------------------------
        #self.__templates='\s*template\s*([A-Za-z][A-Za-z0-9_]*)\(((\$[A-Za-z0-9_]*)*(,\$[A-Za-z0-9_]*)*)\)\s*\{([^\}]*\}([^};][^}]*\})*);'
        #--------------------------------------------------------------------------------------------------------------------


        #Definicion de templates de codigo-----------------------------------------------------------------------------------
        self.__templates='\s*macro\s*([A-Za-z][A-Za-z0-9_]*)\(((\$[A-Za-z0-9_]*)*(,\$[A-Za-z0-9_]*)*)\)\s*syntax:\s*([A-Za-z0-9_\(\)\[\]\+\*\-\.<>,:]*(\|[A-Za-z0-9_\(\)\[\]\+\*\-\.<>,:]*)*)\s*((.|\s)+?)\s*endmacro\s*;'
        #--------------------------------------------------------------------------------------------------------------------
        
        
        #self.__classnames='\s*class\s*([A-Za-z][A-Za-z0-9_]*)\s*extends\s*([A-Za-z][A-Za-z0-9_]*(,[A-Za-z][A-Za-z0-9_]*)*)\s*:' #\s*.+endclass'
        self.__classnames='\s*endclass\s*'        
        self.__instances='\s*([A-Za-z][A-Za-z0-9_]*)\s*=\s*new\s*([A-Za-z][A-Za-z0-9_]*)\s*;'
        #Expresiones regulares para las macros y los imports

        #self.__macro='\s*(function\s+[\\.][a-zA-Z0-9]+|function) ([A-Za-z][A-Za-z0-9_]*)\(((@[A-Za-z0-9_]*)*(,@[A-Za-z0-9_]*)*)\)\s*\{([^\}]*\}([^};][^}]*\})*);'
        self.__macro='\s*(function\s+[\\.][a-zA-Z0-9]+|function) ([A-Za-z][A-Za-z0-9_]*)\(((@[A-Za-z0-9_]*)*(,@[A-Za-z0-9_]*)*)\)(([\s\S]+?)\s*endfunction\s*);'

        #self.__macro_invoke='\$([A-Za-z][A-Za-z0-9_]*)\s*\(([^\)]*)\);'
        self.__macro_invoke='\s*\$([A-Za-z][A-Za-z0-9_]*\.*[A-Za-z0-9_]*)\s*\(([^\)]*)\);'
        self.__import='[^#]?imported (.+|\s+);' #Revisarlo para que falle cuando se comente la linea!!
        #self.__include='[^#]?include (.+|\s+);' #Revisarlo para que falle cuando se comente la linea!!
        self.__comments='##[^\n]*\n?'
        self.__use_modules='[^#]?use module (.+|\s+);'
        #Exp reg para permitir return value en macros
        self.__return='\s*return\s*([^;]+);'

        #Expresiones com
        self.__com_expr='com\s+[^\n]*\n?'
        self.__com_expr2='com\s+[^;]*;'
        
        #Lista de archivos ya importados
        self.__imported=[]
        #Motor de expresiones regulares
        self.__regexp=RegExp('')
        #Cadena procesada
        self.__processed=''

    def process(self,code_string):
        '''Efectua el preprocesado y devuelve una cadena limpia de comentarios, includes, imports y definiciones y usos de macros'''
        #print '\n\nENTRANDO AL PREPROCESADOR!!\n\n'
        #Limpiar los comentarios
        self.__regexp.setPatron(self.__comments)
        code_string=self.__regexp.replace(code_string,'\n')
        #print 'CADENA SIN COMENTARIOS: %s' %code_string
        
        #Poner un ; (instruccion que no hace nada) al final de los endclass-------------------
        #porque el parser espera un valid_st despues de la definicion de clases
        last=None 
        for r in [[m.start(),m.end()] for m in re.finditer(self.__classnames,code_string)]:
            last=r
        if last!=None:
            s,e=last
            code_string=code_string[:s] + '\nendclass;\n' + code_string[e:]
            #print code_string
        #-------------------------------------------------------------------------------------
        
        #1.- Primero los imports:
        self.__regexp.setPatron(self.__import)
        results=self.__regexp.getMatches(code_string)
        #print results
        if results!=[]:
            #Guardar los nombres de los archivos ya importados
            for arch in results:
                if arch!='' and arch in self.__imported:
                    raise PreProcessException("Excepcion en el preprocesado:\nSolo se permite importar un archivo una vez y el archivo \"%s\" ya se ha importado." % arch)
                else:
                    self.__imported.append(arch)
                    #Sustituir la linea del import por el codigo del archivo
                    if not os.path.exists(arch):
                        raise PreProcessException("Excepcion en el preprocesado:\nEl archivo \"%s\" no existe." % arch)
                    code=open(arch).read()
                    code_string=code_string.replace('imported ' + arch + ';',code,1)
                    #print 'Cadena de codigo modificada:\n %s' % code_string
            #No se admiten imports anidados por ahora. Generar una excepcion si todavia quedan
            results=self.__regexp.getMatches(code_string)
            if results!=[]:
                raise PreProcessException("Excepcion en el preprocesado:\nNo se admiten sentencias 'imported' en el contenido de los archivos importados." )
        if self.__imported!=[]:
            SYMTAB['__IMPORTS__'].extend(self.__imported)

        #Hay que volver a limpiar los comentarios
        self.__regexp.setPatron(self.__comments)
        code_string=self.__regexp.replace(code_string,'\n')            
            

        #2.- Ahora las templates
        self.__regexp.setPatron(self.__templates)
        #Obtenemos una lista con tupla con varios grupos
        #print self.__regexp.getMatches(code_string)
        for elem in self.__regexp.getMatches(code_string):
            #print 'elem: %s' % str(elem)
            regex=RegExp(self.__templates)
            begin,end=regex.getMatchInterval(code_string,0)
            #print begin,end
            t_dict={}
            #print 'Reconocido template:'
            #print 'Nombre del template: %s' %elem[0]
            tname=elem[0]
            t_dict['name']=tname
            #print 'Argumentos del template: %s' %elem[1]
            targs=elem[1]
            if targs=='':
                targs=[]
            else:
                targs=targs.split(',')
            t_dict['args']=targs
            t_sint=elem[4]
            #print 'sintaxis del template: %s' %t_sint
            t_dict['syntax']=t_sint
            #PROCESAR SINTAXIS Y CREAR EXPRESION REGULAR!!!!
            #print 'Cuerpo del template: %s' %elem[6].rstrip('}')
            tbody=elem[6].rstrip('}')
            t_dict['body']=tbody
            #print t_dict
            SYMTAB['__TEMPLATES__'][tname]=t_dict
            #print SYMTAB['__TEMPLATES__']
            if tname in SYMTAB['__USED_IDS__']:
                raise Exception('Error: el identificador "%s" ya existe'%tname)
            todel=code_string[begin:end]
            code_string=code_string.replace(todel,'')
            #code_string=code_string.replace(tbody,'__macro_%s'%tname)

        #2.- Ahora las macros
        self.__regexp.setPatron(self.__macro)
        #Obtenemos una lista con tupla con varios grupos:el primero
        #de cada tupla es el tipo de macro, el segundo el nombre de la macro, el tercero la lista de argumentos
        #y el ultimo el codigo
        #pprint.pprint(self.__regexp.getMatches(code_string))
        for elem in self.__regexp.getMatches(code_string):
            #print elem
            macro_args=[]
            _type=elem[0]
            name=elem[1]
                
            ###Cambio para macros de objeto: Guardamos el tipo y el nombre como clave para permitir macros con igual nombre en distintos objetos--------------
            if '.' in _type: #Macro de objeto
                _type=_type.strip().lstrip('function').strip()
                name=_type[1:] + '.' + name
            ##Fin cambio---------------------------------------------------------------------------------------------------------------------------------------
                                
                
            arguments=elem[2]
            if arguments !='': macro_args=arguments.strip().split(',')
            if macro_args==None: macro_args=[]
            #code=elem[-2][:-1](el antiguo y que funcionaba con las llaves)
            code=elem[-2].rstrip('endfunction')            
            #print 'Nombre: %s' % str(name)
            #print 'Argumentos: %s' % str(arguments)
            #print 'Codigo: %s' % str(code)
            
            #Proteger codigo dentro de strings ??-------------------------------------------------------
            regx=RegExp('\"\"\'\'[\s\S]*?\'\'\"\"')
            scont=0
            strings={}
            strs=regx.getMatches(code)
            for el in strs:
                code=code.replace(el,'%%%%'+str(scont)+'%%%%')
                strings['%%%%'+str(scont)+'%%%%']=el
                scont+=1
            #print 'code ahora: %s' %code
            #--------------------------------------------------------------------------------------------
            
            #Procesar los returns en el codigo:----------------------------------------------------------
            regx=RegExp(self.__return)
            #print re.sub(self.__return,"\n _setVar('&" + name + "',\\1);",code)
            old_code=code
            #print regx.getMatches(code)
            #Considerar varias sentencias return:
            #code=regx.replace(code," _setVar('&" + name + "',\\1);")
            code=re.sub(self.__return,"\n _setVar('&" + name + "',\\1);",code)
            #--------------------------------------------------------------------------------------------
            
            #Recuperar el contenido de las strings-------------------------------------------------------
            for item in strings:
                code=code.replace(item,strings[item])
            #print 'code reconstruido: %s'%code          
            #--------------------------------------------------------------------------------------------
            
            #Cambio para ver si las macros aceptan valor de retorno--------------------------------------
            macro_dict={'type':_type,'args':macro_args,'code':code,'name': name,'returns':0}
            #Si se cambia algo en la cadena de codigo, es que hay al menos un return
            if code!=old_code:
                macro_dict['returns']=1
            #--------------------------------------------------------------------------------------------
                
            #Dar de alta las macros. Guardamos un diccionario con los argumentos y el codigo
            SYMTAB['__MACROS__'][name]=macro_dict
            #print SYMTAB['__MACROS__'][name]

            #Dar de alta la macro en SYMTAB porque el interprete espera-------------------------------
            #que todas las macros devuelvan un valor. Por defecto la ponemos a null
            SYMTAB['&' + name]=SYMTAB['__NULL__']
            #-----------------------------------------------------------------------------------------
            
            #Cambio para tener los nombres de las macros censados-------------------------------------
            if name not in SYMTAB['__USED_IDS__']:
                SYMTAB['__USED_IDS__'].append(name)
            #-----------------------------------------------------------------------------------------
            #print SYMTAB['__USED_IDS__']
        #Borrar las macros del codigo de entrada
        code_string=self.__regexp.replace(code_string,'')

        #print 'code_string :%s' % code_string
        #Procesar las lineas com si las hay
        self.__regexp.setPatron(self.__com_expr2)
        matches2=self.__regexp.getMatches(code_string)
        self.__regexp.setPatron(self.__com_expr)
        contador=0
        matches=[]
        matches=self.__regexp.getMatches(code_string)
        #No admitimos sentencias com multilinea
        for i in range(len(matches2)):
            #print repr(matches2[i]),' ==> ',repr(matches[i][:-1]),'\n'
            if len(matches2[i])!=len(matches[i][:-1]):
                raise Exception('Error en la sentencia com: "%s". No se admiten sentencias com que ocupen mas de una linea.'%matches2[i])
        table={}
        if matches!=[]:
            #Cambiar las lineas com por una marca
            for m in matches:
                key='%%COM_' + str(contador) +'%%'
                table[contador]=key
                code_string=code_string.replace(m,key)
                contador+=1
            #procesar coincidencias
            for i in range(len(matches)):
                linep=''
                matches[i]=matches[i].rstrip()
                #1.- Quitar el 'com ' del principio
                matches[i]=matches[i][4:]
                #print 'matches[i]: %s' %matches[i]
                linep+='com '
                #2.- Proceder segun tipo de sentencia com
                if ' is ' in matches[i]: #COM COMID IS LBRACK com_chain RBRACK o COM COMID IS expr
                    parts=matches[i].split(' is ')
                    #print 'partes:%s' %parts
                    linep+=' !' + parts[0].strip() + ' is '
                    #Mirar primer caracter de segunda parte.Si es una comilla ponerlo todo tal cual
                    parts[1]=parts[1].strip()
                    if parts[1][0]=="'":
                        linep+=parts[1] + '\n'
                        matches[i]=linep
                    elif parts[1][0]=='[':
                        parts[1]=parts[1][1:-2]
                        linep+='[!'
                        openpars=0
                        openstring=0
                        for char in parts[1]:
                            if char=='(' and openstring==0:
                                openpars+=1
                            elif char==')' and openstring==0:
                                if openpars>0:
                                    openpars-=1                                
                            elif char=="'":
                                if openstring==1:
                                    openstring=0
                                else:
                                    openstring=1
                            if char=='.': #Decorar si no estamos en un parentesis o en un string
                                if openpars%2==0:#Parentesis equilibrados
                                    linep+='.!'
                                    continue
                            linep+=char
                        linep+='];\n'
                        matches[i]=linep
                elif re.match(r'(.+|\s+)->\s*@[a-zA-Z0-9_]+;$',matches[i]): #COM com_chain ARROW VAR
                    parts=matches[i].split('->')#Asegurarse de que se parte en solo 2 partes!!!!
                    #print parts
                    openpars=0
                    openstring=0
                    linep+='!'
                    for char in parts[0]:
                        if char=='(' and openstring==0:
                            openpars+=1
                        elif char==')' and openstring==0:
                            if openpars>0:
                                openpars-=1                                
                        elif char=="'":
                            if openstring==1:
                                openstring=0
                            else:
                                openstring=1
                        if char=='.': #Decorar si no estamos en un parentesis o en un string
                            if openpars%2==0:#Parentesis equilibrados
                                linep+='.!'
                                continue
                        linep+=char
                    linep+='->' + parts[1] + '\n'
                    matches[i]=linep

                elif re.match(r'(.+|\s+):=(.+|\s+);?$',matches[i]): #COM com_chain COLON EQUAL expr
                    parts=matches[i].split(':=')#Asegurarse de que se parte en solo 2 partes!!!!
                    #print parts
                    openpars=0
                    openstring=0
                    linep+='!'
                    for char in parts[0]:
                        if char=='(' and openstring==0:
                            openpars+=1
                        elif char==')' and openstring==0:
                            if openpars>0:
                                openpars-=1                                
                        elif char=="'":
                            if openstring==1:
                                openstring=0
                            else:
                                openstring=1
                        if char=='.': #Decorar si no estamos en un parentesis o en un string
                            if openpars%2==0:#Parentesis equilibrados
                                linep+='.!'
                                continue
                        linep+=char
                    linep+=':=' + parts[1] + '\n'
                    matches[i]=linep
                elif re.match(r'(.+|\s+);$',matches[i]): #COM com_chain
                    parts=matches[i]
                    #print parts
                    openpars=0
                    openstring=0
                    linep+='!'
                    for char in parts:
                        if char=='(' and openstring==0:
                            openpars+=1
                        elif char==')' and openstring==0:
                            if openpars>0:
                                openpars-=1                                
                        elif char=="'":
                            if openstring==1:
                                openstring=0
                            else:
                                openstring=1
                        if char=='.': #Decorar si no estamos en un parentesis o en un string
                            if openpars%2==0:#Parentesis equilibrados
                                linep+='.!'
                                continue
                        linep+=char
                    linep+='\n'
                    matches[i]=linep                            
                            
            #Y sustituir marcas por las procesadas
            for el in table:
                code_string=code_string.replace(table[el],matches[el])



        #4.- Ahora resolvemos las importaciones de funciones
        self.__regexp.setPatron(self.__use_modules)
        results=self.__regexp.getMatches(code_string)
        #print repr(results[0])
        if results!=[]:
            #Guardar los nombres de los archivos ya importados
            for arch in results:
                if not os.path.exists(arch):
                    raise PreProcessException("Excepcion en el preprocesado:\nEl archivo \"%s\" no existe." % arch)
                #print 'Importando las funciones del modulo: %s' % arch
                #try:
                fname=os.path.splitext(os.path.basename(arch))[0]
                m=imp.new_module(fname)
                impcode=open(arch).read()
                
                #Cambio para que funcione en Mac (y Linux??), quitar los '\r'-------------
                impcode=impcode.replace('\r','')
                #-------------------------------------------------------------------------
                #VIGILAR ESTO!!!!!----------------------------------------
                m.__dict__.update(sys.modules)##VIGILAR ESTO!!!!!!
                #VIGILAR ESTO!!!!!----------------------------------------
                exec impcode in m.__dict__
                sys.modules[fname]=m
                SYMTAB['__FUNCTIONS__'].update(m.exported_functions)
                #except:
                 #   raise PreProcessException("Excepcion en el preprocesado:\nEl archivo \"%s\" no tiene la estructura adecuada para poder importar sus funciones en mini." % arch)
                code_string=code_string.replace('use module ' + arch + ';','',1)
                #print 'Cadena de codigo modificada:\n %s' % code_string
            #No se admiten use modules anidados por ahora. Generar una excepcion si todavia quedan
            results=self.__regexp.getMatches(code_string)
            if results!=[]:
                raise PreProcessException("Excepcion en el preprocesado:\nNo se admiten sentencias USE MODULE en el contenido de los archivos importados." )



        #5.- Por ultimo, decoramos el codigo para permitir simular multithreading si se ha pasado un thread_id ??????
        self.__regexp.setPatron(self.__globals)
        results=self.__regexp.getMatches(code_string)
        if results!=[]:
            for item in results:
                if not item in SYMTAB['__GLOBAL_VARS__']:
                    SYMTAB['__GLOBAL_VARS__'].append(item)
        #print '\n\nRESULTADOS PARA GLOBALS: %s\n\n\n' %str(results)


        #print '\n\nLISTA DE OBJETOS VIRTUALES: %s\n\n' %virtual_objects
        #print '\n\nLISTA DE INSTANCIAS VIRTUALES: %s\n\n' %virtual_instances
                    
        #CAMBIO PARA ASEGURAR CORRECTAS DEFINICIONES DE LISTAS----------------------------------------------------            
        #EXCEPCION SI HAY MAS DE UN '->list' EN LA EXPRESION (REVISAR ESTO MUY BIEN!!!!!!!)
        self.__list_def='\s*\->\s*list\s*\[.*\]\s*'    
        self.__regexp.setPatron(self.__list_def)
        matches=self.__regexp.getMatches(code_string)
        #print 'matches: %s' % matches
        for el in matches:
            l=el[6:]
            _open=0
            closed=0
            buff=''
            #print 'valor de l: %s' %l
            for char in l:
                buff+=char
                #print 'char: %s, open: %s, closed: %s' % (char,_open,closed)
                if char=='[': _open+=1
                if char==']': closed+=1
                if _open and _open==closed:
                    #print 'reconocida lista: %s'%buff
                    arrow=buff.find('->')
                    #print 'arrow: %s' % arrow
                    if arrow!=-1 and '->list' in buff[arrow+2:]:
                        #print 'LISTA NO VALIDA!!!!'
                        raise Exception('Error en la expresion de lista "%s": solo se permite un "->list" al principio de la expresion'%buff)
                    buff=''
                    _open=closed=0
                
            #print l,'->list' in l
            #if '->list' in l:
            #    raise Exception('Error en la expresion de lista "%s": solo se permite un "->list" al principio de la expresion'%el)
        #FIN CAMBIO PARA EXPRESIONES DE LISTAS---------------------------------------------------------------------
            
        #print 'codigo totalmente procesado: %s' % code_string
        #print SYMTAB['__MACROS__']
        return code_string


if __name__=='__main__':
  
    print '\n\nCODIGO DE PRUEBA\n\n'
    cadena='''
##use module stdlib/mini_list.py;
com word is 'Word.Application';
com excel is 'Excel.Application';
com excel.Save(archivo='c:/archivo excel.xls',22,'Texto a mirar'):=1;
com excel.Save(archivo='c:/archivo excel.xls',longitud=22,texto='Texto a mirar');
com word.Visible:=1;
@resul=null;
com excel.Visible->@resul;
com excel.Visible:=1;
com wb is [excel.Workbooks.Add()];
com sheet is [excel.Workbooks(1)];
list values is [1,2,3,4,5];
@values=list values;
com excel.Range('A1:A5').Value[()]:=@values;
com excel.Cells(1,1).Value:=666;
com excel.Cells(1,2).Value:=777;
com excel.Cells(1,3).Value:=888;
com excel.Cells(1,4).Value:=999;
com excel.Range('A1:D1').Value->@values;
    '''

    cadena=open('obj_list_test.mini').read()   
    proc=PreProcessor()    
    print proc.process(cadena)
 