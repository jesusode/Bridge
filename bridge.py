from __future__ import division
#!Python
import sys
import shutil

#Plantillas para los lenguajes a generar------
from templates import *
#---------------------------------------------

#Soporte JavaScript----
import js_builder
#----------------------

#Soporte C++-----------
import cpp_builder
#----------------------

#Soporte Java----------
import java_builder
#----------------------

#Soporte CSharp----------
import csharp_builder
#----------------------

#Para medir eficiencia------------------------------------------------
if not 'time' in sys.modules: 
    time=__import__('time')
else:
    time=sys.modules['time']
#print 'Comenzando carga de modulos: %s' % time.strftime('%H:%M:%S')
#---------------------------------------------------------------------
if not 'urllib' in sys.modules:
    urllib=__import__('urllib')
else:
    urllib=sys.modules['urllib']

#Patch para la ultima version de ply(no va con jython)
if 'java' in sys.platform:
    #if not 'lex' in sys.modules:
        #lex=__import__('lex')
        #from ply import lex
    import lex
    #else:
    #    lex=sys.modules['lex']
    #if not 'yacc' in sys.modules:
        #yacc=__import__('yacc')
        #from ply import yacc
    import yacc
    #else:
    #    yacc=sys.modules['yacc']
else:
    from ply import lex
    from ply import yacc
if not 'os' in sys.modules:
    os=__import__('os')
else:
    os=sys.modules['os']
if not 'os.path' in sys.modules:
    os.path=__import__('os.path')
else:
    os.path=sys.modules['os.path']
if not 'math' in sys.modules:
    math=__import__('math')
else:
    math=sys.modules['math']
if not 're' in sys.modules:
    re=__import__('re')
else:
    re=sys.modules['re']
if not 'random' in sys.modules:
    random=__import__('random')
else:
    random=sys.modules['random']
if not 'pila' in sys.modules:
    pila=__import__('pila')
else:
    pila=sys.modules['pila']
condstack=pila.Pila()

#print sys.modules

#Esto para que no molesten los warnings------------------------
if not 'warnings' in sys.modules:
    warnings=__import__('warnings')
else:
    warnings=sys.modules['warnings']
sys.modules['warnings'].filterwarnings('ignore')
#--------------------------------------------------------------
#print 'Antes de llegar a las que dependen del sistema operativo: %s' % time.strftime('%H:%M:%S')

if not 'stlex2' in sys.modules:
    stlex2=__import__('stlex2')
else:
    stlex2=sys.modules['stlex2']

#Lenguajes permitidos--------------------------------
allowed_langs=['python','csharp','java','js','c++','cython','python3']
#----------------------------------------------------

#Flag global para permitir crear generadores en JavaScript(necesitan marcar la funcion como function*)-------
JS_GENERATOR=0
#------------------------------------------------------------------------------------------------------------

#Variables globales controlables por directivas de linea de comandos
active_lang='python' #Por defecto traducimos a python
create_exe=0 #Crear o no un ejecutable
print_script=0 #Imprimir codigo generado en consola
exec_script=0 #Ejecutar script despues de generarlo
exe_props='' #Archivo de propiedades para generar el ejecutable
outputfile='bridge_output.py' #Nombre del archivo de salida
outputdir='.' #Directorio de salida donde se pondra el archivo generado y/o el ejecutable
extra_files=[] #Archivos de usuario a copiar el el dir del ejecutable
#Archivos de los que depende para compilar con py2exe
__dependencies=['bridge.py','RegExp.py',
                'RegExp2.py','stlex2.py','templates.py',
                'xmltodict.py','lex.py','yacc.py','js_builder.py','csharp_builder.py','cpp_builder.py',
                'java_builder.py','pila.py','prologpy.py',
                'matrix.py','lispy.py']
__dependencies=['RegExp.py','RegExp2.py','xmltodict.py','pila.py','prologpy.py','matrix.py','lispy.py']
prolog_mode=0
minimal_mode=0
repl_mode=0
scheme_mode=0 
clojure_mode=0 
lisp_mode=0 
tk_mode=0
#Flag que controla que se importe el interprete (bridge)
embed_ply=0
#-------------------------------------------------------------------

#Flag que controla el encoding para el codigo fuente(solo Python)
_encoding=""
#-------------------------------------------------------------------

#Global que contiene el programa en ejecucion
__program=''

#Bases de datos soportadas------------------------------------
allowed_databases=['ado','mysql']
#-------------------------------------------------------------

#Flags para traduccion condicional----------------------------
__flags=[]
#-------------------------------------------------------------

#Indentacion para Python---------------------
indent='    '
indent_level=0
#--------------------------------------------

#Nombre generico para listas,arrays y dicts
l_name='list'
l_counter=0
a_counter=0
a_name='array'
d_counter=0
d_name='dict'
o_counter=0
o_name='objdict'
t_name='text'
t_counter=0
u_name='update'
u_counter=0
re_name='regex'
re_counter=0
s_name='split'
s_counter=0
m_name='match'
m_counter=0
aux_name='aux'
aux_counter=0
x_name='xml'
x_counter=0
pl_name='prolog'
pl_counter=0
db_name='dbase'
db_counter=0
f_name='file'
f_counter=0
srv_name='servlet'
srv_counter=0
cnd_name='cond'
cnd_counter=0
g_name='groupby'
g_counter=0
rule_name='rule'
rule_counter=0
let_name='let'
let_counter=0
lazy_name='lazy'
lazy_counter=0
deconstruct_name='deconstruct'
deconstruct_counter=0
tr_name='thread'
tr_counter=0
pr_name='process'
pr_counter=0
enum_counter=0

#Lista de valores para atributos de linq like
attrs_list=[]
att_counter=0
linqresult_list=[]
where_list=[]
group_list=[]
order_list=[]
order_type=''

#Flag para permitir usar el parser en el codigo generado----
__reflected=0
#-----------------------------------------------------------

#Contador de funciones para python
fun_counter=0

#cadena auxiliar para definiciones auxiliares
aux_string=''

#tabla de sustituciones y contador de sustituciones
table_sust={}
cont_sus=0

#Lista de modulos importados--------
imported=[]
#-----------------------------------

#Lista de clases definidas----------
__classes=[]
#Clases a comprobar en runtime
__pyBases=[]
#-----------------------------------


#Funciones globales definidas----------
__functions=[]
#--------------------------------------

#Tipos basados en listas---------------
__typedefs={'numeric':[],'chain':[]}
__type_instances={}
#--------------------------------------

#Bases de conocimiento definidas----------??????
__basecons=[]
#-----------------------------------------

#Directorio base para los environs-----------
__ENVIRON_PATH='.'
__current_namespace=''
__namespaces=[]
#--------------------------------------------
#Archivo que esta siendo procesado-----------
__program_file=''
#--------------------------------------------
#Macros--------------------------------------
__macros={}
macro_name='macro'
macro_counter=0
__quotedefs={}
IN_MACRODEF=0
to_reeval=''

# Get the token map from the lexer.  This is required.
tokens=stlex2.tokens

#Lista de urls a manejar
urls=[]

#Tabla de identificadores definidos-tipo
defined_ids={}

#Tabla de funciones de sistema
system_func={}

#Tabla de funciones definidas por el usuario
user_funcs={}

#Cadena que contiene las importaciones nativas a realizar
nativestring=''

#Cadena que contiene las importaciones a realizar
importstring=''

#Cadena que contiene las funciones definidas
funcstring=''

#Cadena de salida para compilar
outstring=""

#Cadena para las clases de usuario en C# y Java
class_string=''

#Cadena con flags de compilacion condicional para C#
csflags=''

#Cadena con flags de compilacion condicional para C++
cppflags=''

#Flag para generar o no un archivo .h C++ (opcion -h de linea de comandos)
cppheader=0

#Flag para saber si estamos dentro de bucles
INSIDE_LOOP=0

#Flag para saber si un return_st es correcto
INSIDE_FUNC=0

#Flag para saber si estamos definiendo clases
__inclass=0

#Flag para saber si estamos definiendo una funcion lambda
__inlambda=0

#Flags para tipos-lista-----------------------
type_choice=0
options_list=[]
#---------------------------------------------

#Para python con soporte de tipos--------------------------------
py_checks=[] #Comprobaciones para funciones y funciones miembro
py_typeclass=[] #Comprobaciones para variables miembro
py_statictypeclass=[]#Comprobaciones para miembros estaticos
_ftype=''#Tipo del campo si se ha definido
#----------------------------------------------------------------

#Tabla de definiciones a sustituir en codigo final---------------
__definitions={}
#----------------------------------------------------------------

#Flag para controlar excepciones al traducir a diversos lenguajes---------------------
#Si es 1, generamos las excepciones y no se pude usar onflag con lenguajes mezclados
#Si es cero, permite generar codigo que puede contener errores
__strict_mode=0
#--------------------------------------------------------------------------------------

#Clases selladas
__sealed=[]

#Path de busqueda para los imports-------------------------------
MINIMAL_PATH=['.']
#----------------------------------------------------------------

#Flag que indica que estamos dentro de un servidor web----------
IN_WEBSERVER=0
#----------------------------------------------------------------

#Soporte de operadores-------------------------------------------
py_opers={
    '+' : '__add__',
    '-' : '__sub__',
    '*' : '__mul__',
    '/' : '__truediv__',
    '=' : '__equal__',
    '!=' : '__ne__',
    '<' : '__lt__',
    '>' : '__gt__',
    '<=' : '__le__',
    '>=' : '__ge__'
}
#-----------------------------------------------------------------

def flatDeconstructor(dstring,pat):
    cont=0
    cad=''
    #parts=dstring.split(',')
    parts=findElements(dstring)
    #print 'parts:%s' % parts
    for item in parts:
        #print 'procesando item %s,cont=%s' % (item,cont)
        if item=='None':
            cont+=1
            continue
        elif item and item[0]=='[':
            it=item[1:-1]
            #print 'Valor de it:%s' %it
            cad+= flatDeconstructor(it,pat + '[' + str(cont) + ']')
        else:
            cad+= item + ' = ' + pat + '[' + str(cont) + ']\n'
        cont+=1
    #print 'cad en flatDec: %s' % cad
    return cad

#def checkType(elem,_type): #Esto se usa????
#    if not type(elem)==_type:
#        raise Exception("Error: '%s' tiene que tener el tipo %s"%(elem,_type))

#Asignar opciones de linea de comando si las hay-----------
#Disponibles:
# -o <file> Nombre del archivo de salida
# -l <lang> Lenguaje al que se traducira
# -e Crear ejecutable
# -r Ejecutar despues de traducir
# -d Imprimir en consola el codigo generado
# -p <file> Archivo de propiedades para generar ejecutable
#-----------------------------------------------------------
def setCommandLineOptions(opts):
    global create_exe,print_script,exec_script,outputfile,active_lang,extra_files,outputdir,outstring,active_lang,prolog_mode,minimal_mode,scheme_mode,clojure_mode,lisp_mode,repl_mode,__flags,allowed_langs,csflags,cppflags,__strict_mode,MINIMAL_PATH,cppheader,embed_ply,_encoding
    #print 'opts: %s' % opts
    if '-e' in opts: #exe
        create_exe=1
        del opts[opts.index('-e')]
    if '-r' in opts: #run
        exec_script=1
        del opts[opts.index('-r')]
    if '-d' in opts: #dir de salida
        i=opts.index('-d')
        outputdir=opts[i+1]
        del opts[opts.index('-d')]
    if '-p' in opts: #debug print
        print_script=1
        del opts[opts.index('-p')]
    if '-o' in opts: #output file
        i=opts.index('-o')
        outputfile=opts[i+1]
        del opts[i]
        del opts[i]
    if '-s' in opts: #self-reflective
        embed_ply=1
        del opts[opts.index('-s')]
    if '-encoding' in opts: #codec para codigo fuente
        i=opts.index('-encoding')
        _encoding=opts[i+1]
        del opts[i]
        del opts[i]
    if '-strict' in opts: #codigo estricto(restringido al lenguaje especificado)
        i=opts.index('-strict')
        del opts[i]
        __strict_mode=1
    while '-i' in opts: #extra files
        i=opts.index('-i')
        extra_files.append(opts[i+1])
        del opts[i]
        del opts[i]
    while '-flag' in opts: #opciones para trad. condic.
        i=opts.index('-flag')
        if opts[i+1] not in __flags and opts[i+1] not in allowed_langs:  __flags.append(opts[i+1])
        del opts[i]
        del opts[i]
    while '-csflag' in opts: #opciones para trad. condic. en C#
        i=opts.index('-csflag')
        csflags+='#define ' + opts[i+1]
        del opts[i]
        del opts[i]
    while '-cppflag' in opts: #opciones para trad. condic. en C#
        i=opts.index('-cppflag')
        cppflags+='#define ' + opts[i+1]
        del opts[i]
        del opts[i]
    while '-path' in opts: #Busqueda para imports
        i=opts.index('-path')
        if not opts[i+1] in MINIMAL_PATH:
            MINIMAL_PATH.append(opts[i+1])
        del opts[i]
        del opts[i]
    if not '-l' in opts: #establecer flag de python
        __flags.append('python')
    if '-l' in opts: #language
        i=opts.index('-l')
        if opts[i+1] not in allowed_langs:
            raise Exception('Error: "%s" no es un lenguaje soportado'%opts[i+1])
        active_lang=opts[i+1]
        #Para c++ ponemos cpp pq c++ no es un identificador para minimal
        __flags.append(active_lang) if active_lang!="c++" else __flags.append("cpp")
        del opts[i]
        del opts[i]
    if '-h' in opts: #generar archivo .h
        if active_lang!='c++': raise Exception('Error: solo se permite generar archivos de cabecera cuando el lenguaje activo es C++')
        cppheader=1
        del opts[opts.index('-h')]
    if '-lisp' in opts: #incorporar Hy(lento en cargar, retrasa el arranque)
        i=opts.index('-lisp')
        hypath='''if 'win32' in sys.platform or 'darwin' in sys.platform or 'linux' in sys.platform:\n    import hy\n    import hy.cmdline\n'''
        if active_lang=='python':
            outstring+=hypath
        del opts[opts.index('-lisp')]
        lisp_mode=1
    if '-clojure' in opts: #incorporar clojure.py(lento en cargar, retrasa el arranque)
        i=opts.index('-clojure')
        cljpath='import clojure\n'
        if active_lang=='python':
            outstring+=cljpath
        del opts[opts.index('-clojure')]
        clojure_mode=1
    if '-tk' in opts: #incorporar Tkinter(para permitir _formbox)
        i=opts.index('-tk')
        tkpath='import mini_tkbasic\n'
        if active_lang=='python':
            outstring+=tkpath
        del opts[opts.index('-tk')]
        tk_mode=1
    if '-scheme' in opts:
        i=opts.index('-scheme')
        del opts[opts.index('-scheme')]
        scheme_mode=1
    if '-repl' in opts: #-repl arranca en modo repl minimal, prolog, hy, scheme o clojure
        i=opts.index('-repl')
        if active_lang!='python':
            raise Exception('Error: No se puede arancar en modo -repl si el lenguaje no es Python')
        del opts[opts.index('-repl')]
        repl_mode=1
    #Comprobar que no haya opciones incompatibles
    if active_lang!='python' and create_exe==1:
        raise Exception('Error: Solo se pueden generar ejecutables cuando el lenguaje es Python')
    if exec_script==1 and active_lang!='python':
        raise Exception('Error: Solo se permite ejecutar el codigo generado cuando el lenguaje es Python')
    if '-prolog' in opts: #Mejor como opcion de -repl
        i=opts.index('-prolog')
        if active_lang!='python': raise Exception('Error: Solo se puede arrancar minimal en modo Prolog cuando el lenguaje objetivo es Python')
        prolog_mode=1
        del opts[i]
    sys.argv=opts[:] #Ver que pasa con primer y segundo componenente y cuando es un exe!!!
    #print sys.argv

def findInLines(pat,text):
    matches={}
    lines=[x for x in text.split('\n') if x!='']
    #print 'lines in find: %s' % lines
    for i in range(len(lines)):
        #print 'Valor de i: %s' % i
        #print 'Buscando %s en %s'%(pat,lines[i])
        #print lines[i].find(pat)
        if lines[i].find(pat)!=-1:
            if len(lines[i])>len(lines[i].strip()):
                matches[i]=len(lines[i])-len(lines[i].strip())
            else:
                matches[i]=0
    #print 'matches: %s' % matches
    return matches

def replaceWithFormat(text,pat,new,spaces_dict,macro):
    global active_lang
    #print 'TEXT:%s' % text
    lines=[x for x in text.split('\n') if x!='']
    #print 'lines: %s' % lines
    #print 'spaces_dict:%s' % spaces_dict
    for item in spaces_dict:
        codelines=[x for x in new.split('\n') if x!='']
        #print codelines,len(codelines)
        #print 'Sustituyendo patron: %s' % pat
        #Si solo hay una linea y el patron tiene mas texto, no poner retorno de linea
        #si hay mas y hay mas texto hay que generar una excepcion
        pos=lines[item].find(pat)
        #print pos+len(pat),len(lines[item])
        #print 'linea: %s' % lines[item]
        if pos+len(pat)<len(lines[item]):
            if len(codelines)==1:
                lines[item]= lines[item].replace(pat,codelines[0])
            elif active_lang!='python': #CAMBIO PARA MACROS EN JS
                lines[item]= lines[item].replace(pat,codelines[0])
            else:
                raise Exception('Error: La posicion del argumento "%s" en la macro "%s" no es terminal, y no se admite sustituirlo por codigo de multiples lineas "%s"'%(pat,macro,new))
        else:
            first=new.split('\n')[0] + '\n'
            newlines=[((' '*spaces_dict[item]) + x) for x in new.split('\n')[1:]]
            lines[item]=lines[item].replace(pat,first+('\n').join(newlines))
    return ('\n').join(lines)
    

def expand_macro(macro,args):
    #Rescatar template y nombre de argumentos esperados
    global __macros
    if not macro in __macros: raise Exception('Error: La macro "%s" no esta definida'%macro)
    template,arglist=__macros[macro]
    if len(arglist)!=len(args):
        raise Exception('Error: La macro "%s" espera como argumentos "%s" y se le ha pasado "%s"'%(macro,arglist,args))
    #Sustituir cada ocurrencia de los argumentos por los que se han pasado
    for i in range(len(arglist)):
        #print findInLines(arglist[i],template)
        #template=template.replace(arglist[i],args[i].lstrip())
        template=replaceWithFormat(template,arglist[i],args[i].lstrip(),findInLines(arglist[i],template),macro)
        #print 'template ahora: %s' % template
    return template

# def _macroexpand(macro,*args):
    # global __macros
    # return expand_macro(__macros[macro.strip('"')[1:]],[x.strip('"') for x in args])

#--------------------------------------------
def findElements(cad):
    elems=[]
    inbrack=0
    inparen=0
    instring=0
    cont=0
    buff=''
    chars=list(cad)
    while cont<len(cad):
        c=chars[cont]
        #print 'procesando char: %s' % c
        if c=='[':
            inbrack+=1
            buff+=c
        elif c==']':
            inbrack-=1
            buff+=c
        elif c=='"':
            if instring>0:
                instring-=1
                buff+=c
            else:
                instring+=1
                buff+=c
        elif c=='(':
            inparen+=1
            buff+=c
        elif c==')':
            inparen-=1
            buff+=c
        elif c==',':
            if inbrack==0 and inparen==0 and instring==0:
                elems.append(buff)#; print 'metiendo: %s' % buff
                buff=''
            else:
                buff+=c
            cont+=1
            continue
        else:
            buff+=c
        cont+=1
        #print 'valor de buff: %s' % buff
    #coger ultimo trozo si lo hay
    if buff!='': elems.append(buff) #;print 'metiendo al final: %s' % buff
    return elems

#FALLA CON "," EN LOS STRINGS!!!! (recuperar si va mal)
def findElements2(cad):
    instr=0
    elems=[]
    #Proteger cadenas, listas y arrays interiores
    noms='%%%'
    ncont=0
    sust={}
    #print 'cad al principio:%s' % cad
    for it in sys.modules['re'].findall(r'\"[^\"]*?\"',cad):
        t=noms+str(ncont)
        sust[t]=it
        cad=cad.replace(it,t)
        ncont+=1
    for it in sys.modules['re'].findall(r'{[^}]*?\}',cad):
        t=noms+str(ncont)
        sust[t]=it
        cad=cad.replace(it,t)
        ncont+=1
    #print 'cad antes: %s' % cad
    for it in sys.modules['re'].findall(r'\[[^\]]*?\]',cad):#??
        t=noms+str(ncont)
        sust[t]=it
        cad=cad.replace(it,t)
        print 'cad aqui: %s' % cad
        ncont+=1
    for it in sys.modules['re'].findall(r'\([^\)]*?\)',cad): #Parentesis de funciones
        t=noms+str(ncont)
        sust[t]=it
        cad=cad.replace(it,t)
        ncont+=1        
    item=''
    #print 'cad en findElements2: %s' % cad
    if cad[-1]!=')': #secuencia de llamadas a funcion de runtime. REVISAR!!!!!!!!
        for el in list(cad):
            if el!=',':
                item+=el
            else:
                #Recuperar listas, arrays y strings
                while '%%%' in item:
                    for el in sust:
                        item=item.replace(el,sust[el])
                    old2=item
                elems.append(item)
                item=''
    else:
        item=cad
    if item!='':
        while '%%%' in item:
            for el in sust:
                item=item.replace(el,sust[el])          
        elems.append(item)
    return elems


def getSequenceName(item):
    lines=item.split(';')
    return lines[0].split('=')[0].split()[1]


def findInPath(name): #Tambien deberiamos admitir zips como posibles paths
    global MINIMAL_PATH
    #print 'MINIMAL_PATH: %s' %MINIMAL_PATH
    exts=['.mini','.txt','.bridge']
    #print os.getcwd()
    for item in MINIMAL_PATH:
        if item=='.': item=''
        #Probar como archivo y como directorio
        for i in exts:
            #print 'buscando: %s' %repr(item + name + i )
            #print os.path.exists(item + name + i )
            if os.path.isdir(item):
                if os.path.exists(item + '/' + name + i):
                    return item + '/' + name + i
            if os.path.exists(item + name + i):
                return item + name + i
    return ''


def preprocess2(prog): #Cambiado para importacion multiple. REVISAR!!!!
    #Quitar comentarios
    global imported,MINIMAL_PATH
    #return prog;
    #imports='\n\s*?\s*imports\s+(.+|\s+)'
    imports='\n\s*?(\s*imports\s+.+)'
    #Primero normalizar a un espacio de separacion
    prog=sys.modules['re'].sub('imports\s+','imports ',prog)
    #print 'prog normalizado: %s' % prog
    #Cambio para evitar que modifique los imports que estan dentro de los strings-------------
    #Proteger strings
    noms='%%%'
    ncont=0
    sust={}
    sust2={}
    #print 'cad al principio:%s' % cad
    for it in sys.modules['re'].findall(r'\"\"\"[\s\S]*?\"\"\"',prog):
        t=noms+str(ncont) + noms
        sust[t]=it
        prog=prog.replace(it,t)
        ncont+=1
    #print 'prog tras las sustituciones1: %s' %prog
    #raise Exception("Parada temporal!:)")
    #Cambio: nueva expresion regular para los strings de una sola comilla (la otra fallaba)
    for it in sys.modules['re'].findall(r'"(?:[^"\\]|\\.)*"',prog):
        t=noms+str(ncont) + noms
        sust2[t]=it
        prog=prog.replace(it,t)
        ncont+=1
    #print 'prog tras las sustituciones2: %s' %prog
    #open("zzzzzzzz.py","w").write(prog)
    #raise Exception("Parada temporal!:)")
    #print 'prog tras las sustituciones2: %s' %prog
    #raise Exception("Parada temporal!:)")
    results=sys.modules['re'].findall(imports,prog)
    #print 'results: %s' % results
    results=[x.strip().strip('imports').strip() for x in results if not '#' in x]
    while results!=[]:
        #print 'results para imports: %s' % results
        #Guardar los nombres de los archivos ya importados
        for arch in results:
            if arch[-1]==';': arch=arch[:-1]#Quitar el ; final ???
            if arch!='' and arch in imported:
                prog=prog.replace('imports ' + arch,"",1)
            else:
                #Sustituir la linea del import por el codigo del archivo
                item=findInPath(arch)
                #print 'valor de item: %s' % item
                if item=='':
                    raise Exception("Error en la importacion:\n\tEl modulo \"%s\" no existe en el path de minimal." % arch)
                code=open(item).read()
                #print 'reemplazando: %s' % arch
                prog=prog.replace('imports ' + arch,code,1)
                #print 'prog hasta ahora: %s' % prog
                imported.append(arch)
        #print 'prog antes de BUSCAR: %s' % prog
        results=sys.modules['re'].findall(imports,prog)
        #print results,[x.strip()[0] for x in results]
        results=[x.strip().strip('imports').strip() for x in results if not '#' in x]
        #print 'prog ahora: %s' % prog
        #print 'results2: %s' % results
        #open("zzzzzzzz.py","w").write(prog)
        #raw_input("seguimos...")
    #print 'prog despues de preprocess: %s' %prog
    #open("zzzzzzzz.py","w").write(prog)
    #raise Exception("Parada temporal")
    #Recuperar strings
    #print "tabla de sustituciones: %s" % sust
    #for el in sust:
    #    prog=prog.replace(el,sust[el]) 
    #Aqui el orden de recuperacion tiene que ser inverso al de sustitucion
    #probablemente para evitar solapamientos(<--REVISAR ESTOOOOOO!)
    for el in sust2:
        prog=prog.replace(el,sust2[el])
    for el in sust:
        prog=prog.replace(el,sust[el])  
    #print 'prog despues de preprocess: %s' %prog
    #open("zzzzzzzz.py","w").write(prog)
    #raise Exception("Parada temporal")
    #----------------------------------------------------------------------------------------------
    return prog

def preprocess(prog): #Cambiado para importacion multiple. REVISAR!!!!
    #Quitar comentarios
    global imported,MINIMAL_PATH
    exp="""\"[\s\S]*?\s*imports\s*[a-zA-Z_0-9]+\s*?;[\s\S]*?\"|(imports\s*?[a-zA-Z_0-9]+\s*?;)"""
    results=[[x.group(1),x.start(1),x.end(1)] for x in sys.modules['re'].finditer(exp,prog,flags=0)]
    results=[y for y in results if y[0]!=None]
    #print 'IMPORTS results: %s' % results
    cont=0;
    susts={}
    while results!=[]:
        #Guardar los nombres de los archivos ya importados
        for elem in results:
            arch=''.join(elem[0].strip(";").split()[1:])
            #Sustituir el import por una cadena DE LA MISMA LONGITUD!!!
            _len=elem[2]-elem[1]
            #print "_len: %s" % _len
            sstr="__" + str(cont)
            while len(sstr)<_len-2:
                sstr+="%"
            sstr+="_&"
            #print "sstr: %s" % sstr
            #print "arch: %s" % arch
            if arch!='' and arch in imported:
                #prog=prog[:elem[1]] + sstr + prog[elem[2]:]
                prog=prog[:elem[1]] + "\n" + prog[elem[2]:]
                #print "prog: " + prog
                #raise Exception("Parada temporal")
            else:
                #Sustituir la linea del import por el codigo del archivo
                item=findInPath(arch)
                if item=='':
                    raise Exception("Error en la importacion:\n\tEl modulo \"%s\" no existe en el path de bridge." % arch)
                #code=open(item).read()
                code=preprocess(open(item).read())
                prog=prog[:elem[1]] + sstr + prog[elem[2]:]
                imported.append(arch)
                susts[sstr]=code
                cont+=1
                #print "prog: " + prog
                #raise Exception("Parada temporal")
        results=[[x.group(1),x.start(1),x.end(1)] for x in sys.modules['re'].finditer(exp,prog,flags=0)]
        results=[y for y in results if y[0]!=None]
        #print 'results ahora: %s' % results
    #Aplicar las sustituciones
    for item in susts:
        prog=prog.replace(item,susts[item])
    #print prog
    #raise Exception("Temporally stopped!")
    return prog

def checkBaseList(idobj,bases):
    global __classes
    if __classes==[]: return 
    #print 'Clases registradas: %s'%__classes
    for item in bases.split(','):
        if item in ['MiniObject']: continue
        if '.' in item: continue
        if not item in [el[0] for el in __classes]:
                raise Exception('Error: el tipo "%s" en la cadena de herencia de "%s" no esta definido como clase minimal'%(item,idobj))

def build_enum(name,fields):
    code='class '
    code+= name + ' (Enum):\n'
    #code+='    def __init__(self):\n'
    for item in fields.split(','):  
        code+= '    ' + item + '\n'
    return code

#Funcion auxiliar para permitir python 2.7 tipado
def buildCheckType(generic):
    if not '<' in generic:
        return generic
    else:
        its= generic.split('<')
        if len(its)<3:
            return its[0] + ',' + its[1].strip('>') + ' '
        else:
            return its[0] + ',' + its[1] + ',' + its[2].strip('>') + ' '

def applyDefinitions(cad,defs):
    #Proteger strings
    noms='%%%'
    ncont=0
    sust={}
    #print 'cad al principio:%s' % cad
    for it in sys.modules['re'].findall(r'\"[^\"]*?\"',cad):
        t=noms+str(ncont) + noms
        sust[t]=it
        cad=cad.replace(it,t)
        ncont+=1
    #print 'defs: %s' %defs
    #print 'cad con las strings protegidas: %s' % cad
    #print 'sust: %s'%sust
    for item in defs:
        cad=re.sub('\\b'+ item + '\\b',defs[item].strip('"'),cad)
        #print 'Buscando: %s' % item
        #cad=re.sub(item ,defs[item].strip('"'),cad)
    #Recuperar strings
    for el in sust:
        cad=cad.replace(el,sust[el]) 
    #print 'cad al salir de applySust: %s' % cad
    return cad


def cleanupCode(code): #REVISAR!!!!!!!!! Chapucero, pero funciona
    #Limpiar un poco el codigo no Python
    #1.-:quitar grupos de retornos de linea
    code=sys.modules['re'].sub(r'[\n\s]{4,50}','\n',code)#Revisar esto!!!
    #Esta chapucilla arregla los ; que se meten entre las funciones con los onflag????
    code=sys.modules['re'].sub(r'}\s*}\s*;','}\n}\n',code)
    code=sys.modules['re'].sub(r';\s*}\s*;',';\n}\n',code)
    #code=sys.modules['re'].sub(r'{\s*;','{\n',code)
    code=sys.modules['re'].sub(r'^[\)]\s*;\s*(public|static|private|function)\s*','\\1  ',code)
    code=sys.modules['re'].sub(r'\s*;\s*(public|static|private|function)\s*','\\1  ',code) ###REVISAR ESTA!!!
    return code


def cleanupJavaCode(code): #REVISAR!!!!!!!!! Chapucero, pero funciona
    #Limpiar un poco el codigo no Python
    #1.-:quitar grupos de retornos de linea
    code=sys.modules['re'].sub(r'[\n\s]{4,50}','\n',code)#Revisar esto!!!
    #Esta chapucilla arregla los ; que se meten entre las funciones con los onflag????
    code=sys.modules['re'].sub(r'}\s*}\s*;','}\n}\n',code)
    code=sys.modules['re'].sub(r';\s*}\s*;',';\n}\n',code)
    #code=sys.modules['re'].sub(r'{\s*;','{\n',code)
    code=sys.modules['re'].sub(r'^[\)]\s*;\s*(public|static|private|function)\s*','\\1  ',code)
    #code=sys.modules['re'].sub(r'\s*;\s*(public|static|private|function)\s*','\\1  ',code) ###REVISAR ESTA!!!
    return code


#Reglas de precedencia de operadores
# precedence = (
    # ('left','PLUS','MINUS'),
    # ('left','TIMES','DIV'),
    # ('right','UMINUS'),
    # )

precedence = (
    ('right','UMINUS'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIV'),
    )


def p_program(t): #js
    '''program : definitions_section program_elems_list'''
    global outstring,py_template,py_template2,cs_template,js_template,importstring,funcstring,__macros,outputfile,outputdir,class_string,csflags,cppflags,__definitions,__sealed,cppheader,embed_ply,__embed_ply
    if t[2]==None: t[2]=''
    t[0]=t[2]
    #print 'funcstring: %s' % funcstring
    #print 'outstring antes: %s' % outstring
    #print 'class_string antes: %s' % class_string
    #print 'definitions: %s' % __definitions
    outstring+=t[0]
    #print 'outstring despues: %s' % outstring + '\n-------------------------'
    t[0]=outstring
    #Efectuar las sustituciones definidas en __definitions:(revisar como y donde sustituye)
    #if __definitions!={}:
    outstring=applyDefinitions(outstring,__definitions)
    template=''
    if active_lang=='python':
        if __reflected==0:
            template=py_template
        else:
            template=py_template2
        #Cambio para permitir clases selladas------------------------------
        ss=''
        for item in __sealed:
            ss+='python_runtime.__sealed__.append(' + item + ')\n'
        template= template.replace("%%__sealed__%%", ss)
        #------------------------------------------------------------------
        template=template.replace("%%__main_code__%%",outstring)#!!!!!!!!!!!!
        #Cambio para permitir la importacion condicional de ply y bridge.py----------
        if embed_ply==1:
            template=template.replace("%%__reflective__%%",__embed_ply)
        else:
            template=template.replace("%%__reflective__%%","")
        #--------------------------------------------------------------------------------
        #Cambio para permitir definir un encoding para el codigo fuente
        _enc_str="# -*- coding: %s -*-"
        if _encoding!="":
            template=template.replace("%%__encoding__%%",_enc_str%_encoding)
        else:
            template=template.replace("%%__encoding__%%","")  
        #print template
    elif active_lang=='cython':
        template=py_template2
        template=template.replace("%%__main_code__%%",outstring)#!!!!!!!!!!!!
    elif active_lang=='java':
        #print 'outstring aqui: %s' % repr(outstring)
        outstring=outstring.strip().strip('\n')
        outstring=cleanupJavaCode(outstring)
        #print 'outstring para java: %s' % outstring
        template=java_template
        template=template.replace("%%__main_code__%%",outstring)
        template=template.replace("%%__imports__%%",importstring)
        #template=template.replace("%%__functions__%%",funcstring)
        #template=template.replace("%%__name__%%",outputfile.split('.')[0])
    elif active_lang=='csharp':
        #Quitar el ultimo ; (de donde sale???)
        #print 'outstring aqui: %s' % repr(outstring)
        #print outstring!=''
        #Crear una copia personalizada del runtime
        runtime=open('cs_runtime.cs','r').read()
        outstring=outstring.strip().strip('\n')
        outstring=cleanupCode(outstring)
        if outstring not in ['',u'']:
            if outstring[-1]==';': outstring=outstring[:-1]
        template=cs_template
        template=template.replace("%%__main_code__%%",outstring)
        template=template.replace("%%__imports__%%",importstring)
        template=template.replace("%%__classes__%%",class_string)
        template=template.replace("%%__preflags__%%",csflags)
        runtime=runtime.replace("//%%__preflags__%%",csflags)
        template=template.replace("%%__name__%%",outputfile.split('.')[0])
        #Crear nuevo archivo de runtime
        f=open('cs_runtime_minimal.cs','w')
        f.write(runtime)
        f.close()
    elif active_lang=='c++':
        runtime=open('cpp_runtime.cpp','r').read()
        outstring=outstring.strip().strip('\n')
        #outstring=cleanupCode(outstring)
        if outstring not in ['',u'']:
            if outstring[-1]==';': outstring=outstring[:-1]
        template=cpp_header_template
        if cppheader==0:
            template=cpp_template
            template= runtime + template
        template=template.replace("%%__preflags__%%",cppflags)
        template=template.replace("%%__main_code__%%",outstring)
        template=template.replace("%%__imports__%%",importstring)
    else:
        template=js_template
        template=template.replace("%%__jscode__%%",outstring)
    #escribirlo en un archivo
    #Asegurarse de que existe outputdir
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    #print 'Escribiendo en : %s' % outputfile
    f=open(outputdir + '/' + outputfile,'w')
    f.write(template)
    f.close()
    t[0]=template
    class_string=''#?de verdad hay que resetearlo?
    outstring=''#?????????Esto se corrige para el run . Comprobar el resto!!!!!

#Seccion de definiciones------------------------------------------------
def p_definitions_section(t):
    '''definitions_section : definitions_list
    | empty'''
    t[0]=''

def p_definitions_list(t):
    '''definitions_list : definition
    | definition definitions_list'''
    t[0]=''

def p_definition(t):
    '''definition : DEFINE path_elem AS path_elem
    | DEFINE STRING AS path_elem
    | DEFINE path_elem AS path_elem IF idlist
    | DEFINE STRING AS path_elem IF idlist'''
    global __definitions,__flags
    #print 'FLAGS: %s' % str(__flags)
    t[4]=t[4].strip('%')
    if len(t)==7:
        #print t[6].split(',')
        for item in t[6].split(','):
            if item in __flags:
                __definitions[t[4]]=t[2]
    else:
        __definitions[t[4]]=t[2]
    t[0]=''
    #print 'DEFINITIONS: %s' %str(__definitions)

def p_program_elems_list(t):
    '''program_elems_list : program_elem program_elems_list
    | program_elem'''
    if len(t)==3:
        t[0]=t[1] + t[2]
    else:
        t[0]=t[1]


def p_program_elem(t):
    '''program_elem : order_list
    | webserver_section
    | extern_section'''
    t[0]=t[1] + '\n'


def p_native(t): #REVISAR CAMBIOS!!!
    '''native : NATIVE idchain
    | NATIVE idchain TIMES
    | NATIVE idchain FROM expr'''
    global active_lang,importstring,csharp_builder,js_builder,cpp_builder,__strict_mode
    if active_lang=='python':
        if len(t)==3:
            t[0]='import ' + t[2] + '\n'
        else:
            if t[3]=='from':
                t[0]='from ' + t[4] + ' import ' + t[2] + '\n'
    elif active_lang=='cython':
        if len(t)==3:
            t[0]='import ' + t[2] + '\n'
        else:
            if t[3]=='from':
                t[0]='from ' + t[4] + ' cimport ' + t[2] + '\n'
    elif active_lang=='java':
        importstring+=java_builder.process_native(t)
        t[0]=''
    elif active_lang=='csharp':
        importstring+= csharp_builder.process_native(t[2])
        t[0]=''
    elif active_lang=='c++':
        importstring+=cpp_builder.process_native(t[2])
        t[0]=''
    else:
        t[0]=js_builder.process_native(t[2])

def p_idchain(t): #ok
    '''idchain : ID DOT idchain
    | ID'''
    #print 'en idchain'
    t[1]=t[1].strip('%')
    if len(t)==2:
        #Parche para que no se tome null por un ID (aunque no deberia pasar)
        if t[1]=='null':
            t[0]='None'
        else:
            t[0]=t[1]
    else:
        t[0]=t[1] + t[2] + t[3]
    #print 't[0] en idchain: %s' % t[0]

def p_set_environ(t): #ok
    '''set_environ : ENVIRON idchain'''
    global __current_namespace
    __current_namespace=t[2]
    #print 'Establecido NAMESPACE a %s' % __current_namespace
    t[0]=t[2]

def p_namespace(t):#jsp
    '''namespace : set_environ namespace_item_list END idchain'''
    global py_template,__current_namespace,__namespaces,cpp_builder,csharp_builder,js_builder,active_lang,class_string
    #print 'PATH: %s' % t[2]
    #print 'Texto en namespace item: %s' % t[3]
    if t[1] in __namespaces: raise Exception('Error: el environ "%s" ya se ha definido' % t[1])
    if t[1]!=t[4]:
        raise Exception('Error: el nombre de un environ debe ser igual al principio que al final de su definicion')
    if active_lang=='python':
        #Crear arbol de directorios y en cada uno un __init__.py
        curdir=__ENVIRON_PATH
        parts=t[1].split('.')
        if len(parts)>1:
            for item in parts[:-1]:
                curdir+='/' + item
                os.makedirs(curdir)
                open(curdir + '/' + '__init__.py','w').close()
        #y poner el codigo del nuevo modulo
        #print 'Escribimos el codigo en : %s' % parts[-1]
        code=py_template.replace('%%__main_code__%%',t[2])
        f=open(curdir + '/' + parts[-1] + '.py','w')
        f.write(code)
        f.close()
        #Poner en namespaces
        __namespaces.append(t[1])
        #Restablecer __current_namespace
        __current_namespace=''
        t[0]=''
    elif active_lang=='csharp':
        class_string+=csharp_builder.process_environ(__current_namespace,t[2])
        #Poner en namespaces
        __namespaces.append(t[1])
        #Restablecer __current_namespace
        __current_namespace=''
        t[0]=''
    elif active_lang=='java':
        class_string+=java_builder.process_environ(__current_namespace,t[2])
        #Poner en namespaces
        __namespaces.append(t[1])
        #Restablecer __current_namespace
        __current_namespace=''
        t[0]=''
    elif active_lang=='js':
        t[0]=js_builder.process_environ(__current_namespace,t[2])
        #Poner en namespaces
        __namespaces.append(t[1])
        #Restablecer __current_namespace
        __current_namespace=''

def p_namespace_item_list(t):#jsp
    '''namespace_item_list : namespace_item namespace_item_list
    | namespace_item'''
    if len(t)==3:
        t[0]=t[1] + t[2]
    else:
        t[0]=t[1]
      
def p_namespace_item(t):#jsp
    '''namespace_item : class_section
    | fundef_section'''
    t[0]=t[1]

#---Cambios para soportar definiciones extern "C" en C++---------------
def p_extern_section(t):
    '''extern_section : EXTERN COLON extern_item_list END'''
    t[0]='extern "C" {\n' + t[3] + '}\n'

def p_extern_item_list(t):#jsp
    '''extern_item_list : extern_item extern_item_list
    | extern_item'''
    if len(t)==3:
        t[0]=t[1] + t[2]
    else:
        t[0]=t[1]

def p_extern_item(t):#jsp
    '''extern_item : class_section
    | fundef_section'''
    t[0]=t[1]
#-----Fin cambios para extern-------------------------------------------
    
def p_class_section(t):#js,csharp,cpp
    '''class_section : begin_class_section class_list end_class_section
    | empty'''
    global __classes,__pyBases,active_lang,js_builder,class_string,__current_namespace
    #print 'valor de class_string al entrar: %s' % class_string
    #print 'current namespace en class: %s' % __current_namespace
    if active_lang=='js':
        t[0]=js_builder.process_class_section(t)
    elif active_lang=='csharp':
        if __current_namespace=='':
            class_string+=csharp_builder.process_class_section(t)
            t[0]=''
        else:
            t[0]=csharp_builder.process_class_section(t)
    elif active_lang=='java':
        t[0]=java_builder.process_class_section(t)
    elif active_lang=='c++':
        t[0]=cpp_builder.process_class_section(t)
    else:
        __classes.reverse()
        for item in __classes:
            checkBaseList(item[0],item[1])
            for el in item[1].split(','):
                if el and el!='MiniObject' and el not in [x[0] for x in __classes]:
                    __pyBases.append(el)
        if len(t)==4:
            #Cambio para comprobar las bases Python en runtime
            t[0]='python_runtime._check_py_bases([' + ','.join(__pyBases) + '])\n'
            t[0]+=t[2]
            #print '__pyBases: %s' % __pyBases
        else:
            t[0]=t[1]

def p_begin_class_section(t): #js,csharp,cpp
    '''begin_class_section : BEGIN'''
    global __inclass,INSIDE_FUNC
    #Poner a 1 el flag de funciones para permitir la definicion de funciones miembro
    INSIDE_FUNC=1
    __inclass=1
    t[0]='' 

def p_end_class_section(t): #js,csharp,cpp
    '''end_class_section : ENDSEC'''
    global __inclass,INSIDE_FUNC,__pyBases
    #restablecer flag de funciones
    INSIDE_FUNC=0
    __inclass=0
    t[0]=''

def p_class_list(t):#js,csharp,cpp
    '''class_list : classtype classname class_or_interface base_list inner_class_list field_list member_list END class_list
    | classtype classname class_or_interface base_list inner_class_list field_list  member_list END'''
    global __classes,indent,__pyBases,__current_namespace,active_lang,js_builder,__strict_mode,__sealed
    #Excepciones para structs-interfaces
    py_typeclass=[]
    if active_lang=='js':
        #Excepciones para structs-interfaces
        if t[1] in ['struct','interface'] and __strict_mode==1: raise Exception('Error: JavaScript no permite la definicion de estructuras o interfaces')
        t[0]=js_builder.process_class_list(t)
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_class_list(t)
    elif active_lang=='java':
        t[0]=java_builder.process_class_list(t)
    elif active_lang=='c++':
        t[0]=cpp_builder.process_class_list(t)
    else:
        #Excepciones para structs-interfaces
        #print 'Valor de t[1]: %s'%repr(t[1])
        if t[1].strip() in ['struct','interface','final struct','final interface'] and __strict_mode==1: raise Exception('Error: Python no permite la definicion de estructuras o interfaces')
        #Excepcion para decoradores en python:
        if t[1].strip() not in ['class','final class'] and __strict_mode==1:
            raise Exception('Error: Python no permite decoradores para las clases')
            
        #Poner en la lista de clases selladas si t[1] es final---------------------------------
        if t[1]=='final class':
            __sealed.append(repr(t[2]))
        #---------------------------------------------------------------------------------------
        
        if t[4]=='object': t[4]='MiniObject'
        bases=t[4].split(',')
        bases.reverse()#Revisar esto: parece que asi es mas correcto el MRO para herencia multiple
        #print 'bases: %s' % bases
        #print 'field_list: \n%s' % repr(t[5])
        #print 'NAMESPACE: %s' % __current_namespace
        #print 'creando clase %s' % t[2] 
        if t[2] and t[2] in [el[0] for el in __classes] and __current_namespace=='':
            raise Exception('Error: la clase "%s" ya esta definida'%t[2])
        
        if len(t)==10:
            t[0]='class ' + t[2] + '(' + t[4] + '):\n%%static_str%%'
            #Control de herencia multiple (new style classes):------------------------------------------------------
            t[0]+=indent + 'def __init__(self,*k,**kw):\n'
            #-------------------------------------------------------------------------------------------------------
            static_str=''
            if t[6].strip()!='':
                #t[0]+=2*indent + 'super(' + t[2] + ',self)\n'
                for item in [i.split(':') for i in t[6].split(',')]:
                    k=item[0].split('|')
                    f=k[0] if len(k)>1 else item[0] 
                    if len(k)>1: #Campo con restricciones
                        #py_typeclass.append('"' + k[0] + '" :' + k[1])
                        py_typeclass.append('"' + k[0] + '" : [' + buildCheckType(k[1]) + ']')
                        #print 'actualizada!!!:%s' % py_typeclass
                    if item[1]=='private':
                        t[0]+=2*indent + 'self.__' + f + '=None\n'
                    elif item[1]=='static':
                        static_str+=indent + f + '=None\n'
                    else: #Public por defecto
                        t[0]+=2*indent + 'self.' + f + '=None\n'
                if py_typeclass: t[0]+= 2*indent + 'self.pyTypeConstraints={' + ','.join(py_typeclass) + '}\n'
            #Control de herencia multiple (new style classes):------------------------------------------------------
            for b in bases:
                t[0]+= 2*indent + b +  '.__init__(self,*k,**kw)\n'
            #-------------------------------------------------------------------------------------------------------
            #Poner funciones miembro
            for item in t[7].split('\n'):
                t[0]+=indent + item + '\n'
            t[0]=t[0].replace('%%static_str%%',static_str)
            t[0]+=t[9] + '\n'
            if __current_namespace=='':
                __classes.append((t[2],t[4],t[6]))
            else:
                __classes.append((__current_namespace + '.' + t[2],t[4],t[6]))
        else:
            t[0]='class ' + t[2] + '(' + t[4] + '):\n%%static_str%%'
            #Control de herencia multiple (new style classes):------------------------------------------------------
            t[0]+=indent + 'def __init__(self,*k,**kw):\n'
            #-------------------------------------------------------------------------------------------------------
            static_str=''
            if t[6].strip()!='':
                #t[0]+=2*indent + 'super(' + t[2] + ',self)\n'
                for item in [i.split(':') for i in t[6].split(',')]:
                    k=item[0].split('|')
                    f=k[0] if len(k)>1 else item[0] 
                    if len(k)>1: #Campo con restricciones
                        #py_typeclass.append('"' + k[0] + '" :' + k[1])
                        py_typeclass.append('"' + k[0] + '" : [' + buildCheckType(k[1]) + ']')
                        #print 'actualizada2!!!:%s' % py_typeclass
                    if item[1]=='private':
                        t[0]+=2*indent + 'self.__' + f + '=None\n'
                    elif item[1]=='static':
                        static_str+=indent + f + '=None\n'
                    else: #Public por defecto
                        t[0]+=2*indent + 'self.' + f + '=None\n'
                if py_typeclass: t[0]+= 2*indent + 'self.pyTypeConstraints={' + ','.join(py_typeclass) + '}\n'
            #Control de herencia multiple (new style classes):------------------------------------------------------
            for b in bases:
                t[0]+= 2*indent + b +  '.__init__(self,*k,**kw)\n'
            #-------------------------------------------------------------------------------------------------------
            #Poner funciones miembro
            for item in t[7].split('\n'):
                t[0]+=indent + item + '\n'
            t[0]=t[0].replace('%%static_str%%',static_str)
            if __current_namespace=='':
                __classes.append((t[2],t[4],t[6]))
            else:
                __classes.append((__current_namespace + '.' + t[2],t[4],t[6]))
        #print 'valor de __classess: %s '% __classes
        #print 'valor de t[0] en class_list: %s' %t[0] 
    #print 'valor de t[0] en class_list: %s' %t[0]


def p_class_or_interface(t):
    '''class_or_interface : EXTENDS
    | IMPLEMENTS'''
    t[0]=t[1]


def p_classname(t):
    '''classname : generic'''
    t[0]=t[1]


# def p_classtype(t):
    # '''classtype : cls_mod CLASS
    # | cls_mod STRUCT
    # | cls_mod INTERFACE
    # | cls_mod generic'''
    # t[0]=t[1] + ' ' + t[2]


def p_classtype(t):
    '''classtype : cls_mod CLASS
    | cls_mod STRUCT
    | cls_mod INTERFACE
    | cls_mod generic
    | cls_mod CLASS GENERIC
    | cls_mod STRUCT GENERIC
    | cls_mod INTERFACE GENERIC
    | cls_mod generic GENERIC'''
    if len(t)==3:
        t[0]=t[1] + ' ' + t[2]
    else:
        t[0]=t[1] + ' ' + t[2] + ' ' + t[3]

# def p_cls_mod(t):
    # '''cls_mod : id_space
    # | empty'''
    # t[0]=t[1]

def p_cls_mod(t):
    '''cls_mod : AMPERSAND id_space
    | empty'''
    if len(t)==3:
        t[0]=t[2]
    else:
        t[0]=t[1]


# def p_cls_mod2(t):
    # '''cls_mod2 : AMPERSAND id_space2
    # | empty'''
    # if len(t)==3:
        # t[0]=t[2]
    # else:
        # t[0]=t[1]


def p_id_space(t):
    '''id_space : ids_elem
    | ids_elem id_space'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]= t[1] + ' ' + t[2]

# def p_id_space2(t):
    # '''id_space2 : ambit'''
    # t[0]=t[1]


def p_ids_elem(t):
    '''ids_elem : ID
    | ambit'''
    t[0]=t[1].strip('%')

def p_base_list(t): #jsp
    '''base_list : generic_list
    | OBJECT
    | OBJECT COMMA generic_list'''
    global active_lang,js_builder
    if active_lang=='js':
        t[0]=js_builder.process_base_list(t)
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_base_list(t)
        #print 't[0] en base_list: %s' % t[0]
    elif active_lang=='java':
        t[0]=java_builder.process_base_list(t)
    elif active_lang=='c++':
        t[0]=cpp_builder.process_base_list(t)
    else:
        if len(t)==2:
            t[0]=t[1]
        else:
            t[0]='MiniObject' + t[2] + t[3]

#Clases anidadas(solo C++ y Java)
def p_inner_class(t):
    '''inner_class : PIPE classtype classname class_or_interface base_list field_list member_list END PIPE'''
    global active_lang, __strict_mode
    if active_lang in ['c++','java']:
        if active_lang=='c++':
            t[0]=cpp_builder.process_inner_class(t)
        else:
            t[0]=java_builder.process_inner_class(t)
    else:
        if __strict_mode==1:
            raise Exception('Error: Solo se permiten clases anidadas cuando el lenguaje objetivo es C++ o Java')
        else:
            t[0]=''
    #print 'valor de t[0] en inner_class_list: %s' %t[0]

def p_inner_class_list(t):#js,csharp,cpp
    '''inner_class_list : inner_class
    | inner_class inner_class_list
    | empty'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2]
    #Por que t[0] puede ser None?????
    #if t[0] ==None: t[0] =''
    #print 'valor de t[0] en inner_class: %s' %t[0]

def p_field_list(t): #js,csharp,cpp
    '''field_list : field_item COLON ambit field_list 
    | field_item COLON ambit
    | empty'''
    global active_lang,js_builder
    if active_lang=='js':
        t[0]=js_builder.process_field_list(t)
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_field_list(t)
    elif active_lang=='java':
        t[0]=java_builder.process_field_list(t)
    elif active_lang=='c++':
        t[0]=cpp_builder.process_field_list(t)
    else:
        if len(t)==2:
            t[0]=t[1]
        elif len(t)==4:
            t[0]=t[1] + t[2] + t[3]
        else:
            t[0]= t[1] + t[2] + t[3] + ',' + t[4]


def p_field_item(t):#js,csharp,cpp
    '''field_item : ID
    | ID AS generic
    | enum_st'''
    global active_lang,js_builder,cpp_builder
    #print 't[1] en p_field_item: %s' % t[1]
    if t[1]: t[1]=t[1].strip('%')
    if active_lang=='js':
        t[0]=js_builder.process_field_item(t)
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_field_item(t)
    elif active_lang=='java':
        t[0]=java_builder.process_field_item(t)
    elif active_lang=='c++':
        t[0]=cpp_builder.process_field_item(t)
    else:
        if len(t)==4:
            t[0]=t[1] + '|' + t[3]
        else:
            t[0]=t[1]

        
def p_ambit(t): #REVISAR CAMBIO!!!
    '''ambit : PUBLIC
    | PRIVATE
    | STATIC
    | PUBLIC STATIC
    | PRIVATE STATIC'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + ' ' + t[2]

    
def p_member_list(t): #jsp
    '''member_list : member_fun_list
    | empty'''
    global INSIDE_FUNC,active_lang,js_builder
    #print 'Valor de INSIDE_FUNC aqui: %s' % INSIDE_FUNC
    if active_lang=='js':
        t[0]=js_builder.process_member_list(t)
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_member_list(t)
    elif active_lang=='java':
        t[0]=java_builder.process_member_list(t)
    elif active_lang=='c++':
        t[0]=cpp_builder.process_member_list(t)
    else:
        t[0]=t[1]
    #print 'valor de t[0] en member_list: %s' % t[0]

    
def p_member_fun(t): #PARA RECUPERAR SI VA MAL!!!!
    '''member_fun : ambit fundef'''
    #print 'en member_fun cls_mod: %s' % t[1]
    #print 'en member_fun fundef: %s' % t[2]
    global active_lang,js_builder
    if active_lang=='js':
        t[0]=js_builder.process_member_fun(t)
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_member_fun(t)
    elif active_lang=='java':
        t[0]=java_builder.process_member_fun(t)
    elif active_lang=='c++':
        t[0]=cpp_builder.process_member_fun(t)
    else:
        fname=t[2].split('(')[0].strip()[4:]
        if t[1]=='private':
            t[0]=t[2].replace(fname,'__'+fname,1)
        elif t[1]=='static':
            t[0]='@staticmethod\n' + t[2].replace('self,','',1)
        else:
            t[0]=t[2]
    #print 'valor de t[0] en member_fun: %s' % t[0]

def p_member_fun_list(t): #jsp
    '''member_fun_list : member_fun_ext  member_fun_list
    | member_fun_ext'''
    global active_lang,js_builder
    if active_lang=='js':
        t[0]=js_builder.process_member_fun_list(t)
        #print 't[0] en member_fun_list: %s' % t[0]
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_member_fun_list(t)
    elif active_lang=='java':
        t[0]=java_builder.process_member_fun_list(t)
    elif active_lang=='c++':
        t[0]=cpp_builder.process_member_fun_list(t)
    else:
        if len(t)==3:
            t[0]=t[1] + t[2]
        else:
            t[0]=t[1]
        
def p_member_fun_ext(t):
    '''member_fun_ext : member_fun
    | operator_def'''
    t[0]=t[1]

def p_operator_def(t):
    ''' operator_def : OPERATOR oper_type LPAREN funcargs RPAREN COLON order_list END
    | cls_mod OPERATOR oper_type LPAREN funcargs RPAREN AS generic COLON order_list END'''
    global py_opers,active_lang,indent,py_checks,csharp_builder,cpp_builder,__strict_mode
    if active_lang=='python': #COMPROBAR QUE EL PRIMER ARGUMENTO ES self!!!!!!!
        if len(t)==12  and __strict_mode==1: raise Exception('Error: en python no se permite declarar el tipo de retorno de una funcion u operador')
        fname=py_opers[t[2]]
        #Actualizar indent
        indent+='    '
        t[0]='\ndef ' + fname + ' ' + t[3] + t[4] + t[5] + t[6] + '\n'
        #poner checks de tipos si se han definido------------------------------------------
        for x in py_checks:
            #t[0]+=indent + 'python_runtime._checkType(' + x[0] + ',' + x[1] + ')\n'
            t[0]+=indent + 'python_runtime._checkType(' + x[0] + ',' + buildCheckType(x[1]) + ')\n'
        py_checks=[]
        #-----------------------------------------------------------------------------------
        for it in t[7].split('\n'):
            t[0]+=indent + it + '\n'
        #Actualizar indent(quitar 4 espacios)
        indent=indent[-4]
        #print 'resultado de operator: %s' % t[0]
    elif active_lang=='js'  and __strict_mode==1: raise Exception('Error: JavaScript no permite la definicion de operadores')
    elif active_lang=='java'  and __strict_mode==1: raise Exception('Error: Java no permite la definicion de operadores')
    elif active_lang=='csharp'  and __strict_mode==1:
        if len(t)!=12: raise Exception('Error: en C# hay que declarar el tipo de retorno de una funcion u operador')
        t[0]=csharp_builder.process_operator(t)
    elif active_lang=='csharp':#Parece que si es como esta escrito
        t[0]=csharp_builder.process_operator(t)
    elif active_lang=='c++'  and __strict_mode==1:
        if len(t)!=12: raise Exception('Error: en C++ hay que declarar el tipo de retorno de una funcion u operador')
        t[0]=cpp_builder.process_operator(t)
    elif active_lang=='c++':#Parece que si es como esta escrito
        t[0]=cpp_builder.process_operator(t)
    else:
        t[0]=''

def p_oper_type(t):
    ''' oper_type : PLUS
    | MINUS
    | TIMES
    | DIV
    | EQ
    | EQUAL
    | GE
    | NE
    | GT
    | LT
    | LE
    | EXTRACTOR
    | INSERTOR
    | INSERTOREQ
    | EXTRACTOREQ
    | AMPERSANDEQ
    | PTR
    | PTREQ
    | PLUSEQ
    | MINUSEQ
    | TIMESEQ
    | DIVEQ
    | ARROW
    | ARROW TIMES
    | AMPERSAND
    | LPAREN RPAREN
    | LBRACK RBRACK
    | DOTDOT
    | INCR
    | INCR PLUS
    | INCR MINUS
    | AND
    | OR
    | NOT
    | DESTR
    | COMMA
    | DOT
    | PIPE
    | PIPE EQUAL
    | ID'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2]
#---------------------------------------------------------------------------------------------------------        

def p_fundef_section(t): #ok
    '''fundef_section : begin_fun_section funlist end_fun_section'''
    #global funcstring,INSIDE_FUNC
    if t[2]==None:
        t[0]=''
    else:
        t[0]=t[2]
    #Restablecer flag de definicion de funciones
    #INSIDE_FUNC=0
    #t[0]=t[2]

def p_begin_fun_section(t): #ok
    '''begin_fun_section : BEGIN'''
    global INSIDE_FUNC
    #Poner a 1 el flag de funciones para permitir la definicion de funciones miembro
    INSIDE_FUNC+=1
    t[0]=t[1] 

def p_end_fun_section(t): #ok
    '''end_fun_section : ENDSEC'''
    global INSIDE_FUNC
    #restablecer flag de funciones
    INSIDE_FUNC-=1
    t[0]=t[1]
    
def p_funlist(t): #ok
    '''funlist : funlist_elem
    | funlist_elem funlist'''
    t[0]= t[1] if len(t)==2 else t[1] + t[2]
    #print "t[0] en funlist: %s"%t[0]
    
def p_fundef(t): #VIGILAR CAMBIO PARA FUNCIONES VACIAS PARA INTERFACES|CYTHON!!
    '''fundef : annotation_list cls_mod funtype generic LPAREN funcargs RPAREN COLON order_list END
    | annotation_list cls_mod funtype generic LPAREN funcargs RPAREN COLON empty END
    | annotation_list cls_mod funtype generic LPAREN funcargs RPAREN  AS generic COLON order_list END
    | annotation_list cls_mod funtype generic LPAREN funcargs RPAREN  AS generic COLON empty END'''
    global user_funcs,indent,__functions,__inclass,__current_namespace,py_checks,JS_GENERATOR,funcstring,__strict_mode
    langs={'c++':'C++','java':'Java','csharp': 'C#','python':'Python','cython':'Cython'}
    #Python y Js no admiten modificadores en las funciones
    #if active_lang in ['python','js']  and __strict_mode==1:
    #    raise Exception('Error: "%s" no admite modificadores en las funciones'%langs[active_lang])
    #print 'en fundef len(t): %s' % len(t)
    #print [el for el in t]
    #print 'annotations en fundef: %s' % t[1]
    #print 'cls_mod2 en fundef: %s' % t[2]
    if len(t)==11:
        if active_lang in ['python','cython']:
            #Excepcion si la funcion ya esta definida
            if not __inclass and t[4] in __functions and __current_namespace==''  and __strict_mode==1: raise Exception('Error: la funcion "%s" ya esta definida'%t[4])
            #Actualizar indent
            indent+='    '
            if t[3]=='cfunction':
                t[0]=t[1] + '\ncdef ' + t[4] + ' ' + t[5]
            else:
                t[0]=t[1] + '\ndef ' + t[4] + ' ' + t[5]
            #print t[4]
            for el in t[6].split(','):
                t[0]+= ' ' + el + ','
            if t[0][-1]==',':t[0]=t[0][:-1]#quitar la ultima coma
            t[0]+=t[7] + t[8] + '\n' #+t[7] + '\n'  
            #poner checks de tipos si se han definido------------------------------------------
            for x in py_checks:
                #t[0]+=indent + 'python_runtime._checkType(' + x[0] + ',' + x[1] + ')\n'
                t[0]+=indent + 'python_runtime._checkType(' + x[0] + ',' + buildCheckType(x[1]) + ')\n'
            py_checks=[]
            #-----------------------------------------------------------------------------------
            #print 'valor de t[9]: %s' % t[9]
            for it in t[9].split('\n'):
                t[0]+=indent + it + '\n'
            #Actualizar indent(quitar 4 espacios)
            indent=indent[-4]
            #Registrar la funcion
            if __inclass==0:
                if __current_namespace=='':
                    __functions.append(t[4])
                else:
                    __functions.append(__current_namespace + '.' + t[4])
            #print 'funciones registradas: %s' % __functions
            #print "t[0] en fundef: %s" % t[0]
        elif active_lang in ['c++', 'java','csharp']  and __strict_mode==1:
            raise Exception("Error: En %s las funciones deben especificar el tipo de retorno" % langs[active_lang])
        elif active_lang in ['c++', 'java','csharp']:
            modifiers=t[2]
            annots=t[1]
            #if t[1]=='generic':
            if 'generic' in t[1].split('|'): #Ver si esto funciona para todos los lenguajes
                if active_lang=='csharp':
                    t[0]=csharp_builder.process_fundef(t[4],t[6],'',t[9],1,modifiers,annots)
                elif active_lang=='java':
                    t[0]=java_builder.process_fundef(t[4],t[6],'',t[9],1,modifiers,annots)
                elif active_lang=='c++':
                    #print 'entrando a c++ (1)'
                    t[0]=cpp_builder.process_fundef(t[4],t[6],'',t[9],1,modifiers,annots)
            else:
                #process_fundef(id,funcargs,orderlist,_type,generic,modifiers,annots=''):
                if active_lang=='csharp':
                    t[0]=csharp_builder.process_fundef(t[4],t[6],t[9],'',0,modifiers,annots)
                elif active_lang=='java':
                    t[0]=java_builder.process_fundef(t[4],t[6],t[9],'',0,modifiers,annots)
                elif active_lang=='c++':
                    #print 'entrando a c++ (2)'
                    t[0]=csharp_builder.process_fundef(t[4],t[6],t[9],'',0,modifiers,annots)
        else: #js   
            t[0]=js_builder.process_fundef(t[4],t[6],t[9],JS_GENERATOR,__current_namespace)  
            #Resetear flag de generador
            if JS_GENERATOR==1: JS_GENERATOR=0
    elif active_lang=='csharp':
        if __current_namespace!='' and __inclass==0  and __strict_mode==1: #No dejamos definir funciones fuera de clases en los environs!!
            raise Exception('Error: en C# solo se acepta definir funciones fuera de un environ. Usar una clase estatica en su lugar')
        modifiers=t[2]
        annots=t[1]
        if t[1]=='generic':
            t[0]=csharp_builder.process_fundef(t[4],t[6],t[11],t[9],1,modifiers)
        else:
            t[0]=csharp_builder.process_fundef(t[4],t[6],t[11],t[9],0,modifiers,annots)
    elif active_lang=='java':
        if __current_namespace!='' and __inclass==0  and __strict_mode==1: #No dejamos definir funciones fuera de clases en los environs!!
            raise Exception('Error: en Java solo se acepta definir funciones fuera de un environ. Usar una clase estatica en su lugar')
        modifiers=t[2]
        annots=t[1]
        if t[1]=='generic':
            t[0]=java_builder.process_fundef(t[4],t[6],t[11],t[9],1,modifiers)
        else:
            t[0]=java_builder.process_fundef(t[4],t[6],t[11],t[9],0,modifiers,annots)
    elif active_lang=='c++': 
        modifiers=t[2]
        annots=t[1]
        #if t[1]=='generic': 
        #print 'entrando a c++ (3)'
        if 'generic' in t[1].split('|'): #Ver si esto funciona para todos los lenguajes
            t[0]=cpp_builder.process_fundef(t[4],t[6],t[11],t[9],1,modifiers,annots)
        else:
            t[0]=cpp_builder.process_fundef(t[4],t[6],t[11],t[9],0,modifiers,annots)
    elif active_lang=='cython':
            #Excepcion si la funcion ya esta definida
            if not __inclass and t[4] in __functions and __current_namespace==''  and __strict_mode==1: raise Exception('Error: la funcion "%s" ya esta definida'%t[4])
            #Actualizar indent
            indent+='    '
            if t[3]=='cfunction':
                t[0]=t[1] + '\ncdef ' + t[9] + ' ' + t[4] + ' ' + t[5]
            else:
                raise Exception("En Cython hay que definir las funciones con tipo con cfunction")
            for el in t[6].split(','):
                t[0]+= ' ' + el + ','
            if t[0][-1]==',':t[0]=t[0][:-1]#quitar la ultima coma
            t[0]+=t[7] + t[10] + '\n'
            #print 'Valor de t11: %s'%repr(t[11])
            for it in t[11].split('\n'):
                t[0]+=indent + it + '\n'
            #Actualizar indent(quitar 4 espacios)
            indent=indent[-4]
    else: #?????????????
        #print "Me voy por el else!!!!!!!!"
        #if active_lang in ['python','js']  and __strict_mode==1:
        #    raise Exception('Error definiendo la funcion "%s" como "%s" : %s no acepta declarar funciones con tipo de retorno explicito.'%(t[4],t[9],langs[active_lang]))
        #PRUEBAS-------------------------------------------------------------------------------
        if active_lang in ['python','js']: 
            #print "ENTRANDO AL CODIGO EN PRUEBAS"		
            #Excepcion si la funcion ya esta definida
            if not __inclass and t[4] in __functions and __current_namespace==''  and __strict_mode==1: raise Exception('Error: la funcion "%s" ya esta definida'%t[4])
            #Actualizar indent
            indent+='    '
            if t[3]=='cfunction':
                t[0]=t[1] + '\ncdef ' + t[4] + ' ' + t[5]
            else:
                t[0]=t[1] + '\ndef ' + t[4] + ' ' + t[5]
            #print t[4]
            for el in t[6].split(','):
                t[0]+= ' ' + el + ','
            if t[0][-1]==',':t[0]=t[0][:-1]#quitar la ultima coma
            t[0]+=t[7] + t[10] + '\n' #+t[7] + '\n'  
            #poner checks de tipos si se han definido------------------------------------------
            for x in py_checks:
                #t[0]+=indent + 'python_runtime._checkType(' + x[0] + ',' + x[1] + ')\n'
                t[0]+=indent + 'python_runtime._checkType(' + x[0] + ',' + buildCheckType(x[1]) + ')\n'
            py_checks=[]
            #-----------------------------------------------------------------------------------
            #print 'valor de t[9]: %s' % t[9]
            if t[11]!="":
                for it in t[11].split('\n'):
                    t[0]+=indent + it + '\n'
            mch1= sys.modules['re'].findall('return\s+(.*)\n',t[0])
            mch= sys.modules['re'].findall('return\s+.*\n',t[0])
            #print mch1
            #print mch
            for i in range(len(mch1)):
                #typestr='python_runtime._checkType(' + mch1[i] + ',' + buildCheckType(t[9]) + ')\n'
                #typestr += indent + 'return ' +  mch1[i] + '\n'
                typestr='python_runtime._checkType(' + mch1[i] + ',' + buildCheckType(t[9]) + '); return ' +  mch1[i] + '\n'
                #print typestr
                #print "T[0]: %s"%t[0]
                #print "mch1[i]: %s"%mch1[i]
                #t[0]=sys.modules['re'].sub('return\s+'+item+'\n',typestr,t[0])
                t[0]=t[0].replace(mch[i],typestr)
                #print "T[0] AHORA: %s"%t[0]
            #raise Exception("PARADA TEMPORAL")
            #Actualizar indent(quitar 4 espacios)
            indent=indent[-4]
            #Registrar la funcion
            if __inclass==0:
                if __current_namespace=='':
                    __functions.append(t[4])
                else:
                    __functions.append(__current_namespace + '.' + t[4])
        #FIN PRUEBAS---------------------------------------------------------------------------------


        #ESto sirve para algo????????----------------------------
		
        # t[0]='public static ' + t[9] + ' ' + t[4] + ' ' + t[5]
        # for el in t[6].split(','): #Que hace esto??????
            # if ' ' in el:
                # t[0]+= ' ' + el + ','
            # else:
                # t[0]+= " Object " + el + ','
        # if t[0][-1]==',':t[0]=t[0][:-1]#quitar la ultima coma
        # t[0]+=t[7] + '\n{\n' +t[11] + '\n}\n'
		
        #--------------------------------------------------------
    user_funcs[t[3]]='user' #?


#Solo para Cython
def p_funtype(t):
    '''funtype : FUNCTION
    | CFUNCTION'''
    t[0]=t[1]

def p_funlist_elem(t):
    '''funlist_elem : fundef
    | enum_st'''
    t[0]=t[1]


def p_annotation_list(t):#cy
    '''annotation_list : annotation annotation_list
    | annotation
    | GENERIC
    | empty'''
    global active_lang,__strict_mode
    if active_lang=='js' and t[1]!='' and __strict_mode==1: raise Exception('Error: JavaScript no permite anotaciones en las funciones')
    #if active_lang=='c++'  and __strict_mode==1: raise Exception('Error: C++ no permite anotaciones en las funciones')    
    if active_lang=='cython'  and __strict_mode==1: raise Exception('Error: Cython no permite anotaciones en las funciones') 
    if len(t)==3:
        #Trampa para no meter generic en la cadena de annots
        #if t[1]=='generic' and active_lang=='c++': t[1]=''
        #if t[2]=='generic' and active_lang=='c++': t[2]=''
        t[0]=t[1] + t[2]
    else:
        t[0]=t[1]

def p_annotation(t):
    '''annotation : LBRACK PTR annot_elems_list RBRACK'''
    global active_lang,csharp_builder
    #Esto depende del lenguaje final!!!!!
    if active_lang=='c++': #C++ acepta anotaciones???
        t[0]=cpp_builder.process_annotation(t)
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_annotation(t)
    elif active_lang=='java':
        t[0]=java_builder.process_annotation(t)
    else:#Python
        t[0]='@' + t[3] + '\n'

def p_annot_elems_list(t):
    '''annot_elems_list : annot_elem
    | annot_elem annot_elems_list'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + ',' + t[2]

def p_annot_elem(t):
    '''annot_elem : funcall
    | ID'''
    t[0]=t[1].strip('%')

def p_funcargs(t): #ok
    '''funcargs : idfunlist optional_args
    | optional_args'''
    #print 't en funcargs:%s' % [el for el in t]
    global __inclass,active_lang,cpp_builder
    if __inclass==1 and active_lang=='python': #Para funciones miembro
        #print 'paso por aqui en funcargs y no debo!!!!!!!'
        t[0]='self,'
    else:
        t[0]=''
    if len(t)==3:
        if t[1]!='' and t[2]:
            t[2]=',' + t[2]
        elif t[1]=='' and t[2]:
            t[2]=t[2]
        t[0]+=t[1] + t[2]
    else:
        t[0]+=t[1]
    if t[0] and  t[0][-1]==',': t[0]=t[0][:-1] #OJITO con ESTO!!!

def p_funcargs2(t): #chapuza para permitir definir lambdas dentro de clases
    '''funcargs2 : idfunlist optional_args
    | optional_args'''
    #print 't[1] en funcargs2:%s' % t[1]
    #print 't[2] en funcargs2:%s' % t[2]
    t[0]=''
    if len(t)==3:
        if t[1]!='' and t[2]:
            t[2]=',' + t[2]
        elif t[1]=='' and t[2]:
            t[2]=t[2]
        t[0]+=t[1] + t[2]
    else:
        t[0]+=t[1]
    if t[0] and  t[0][-1]==',': t[0]=t[0][:-1] #OJITO con ESTO!!!

def p_optional_args(t): #js
    '''optional_args : PIPE TIMES defaults_item COMMA EXP defaults_item
    | PIPE EXP defaults_item
    | PIPE TIMES defaults_item
    | PIPE defaults_chain
    | empty'''
    global active_lang,__strict_mode
    #print 't en optional_args:%s' % [el for el in t]
    #print 'len(t) optional_args:%s' % len(t)
    if len(t)>2 and t[2] in ['*','**'] and active_lang in ['js'] and __strict_mode==1:
       raise Exception('Error: JavaScript no admite argumentos opcionales excepto por nombre=valor')
    if len(t)==7:
        t[0]='*' + t[3] + ',' + '**' +  t[6]
    elif len(t)==3:
        t[0]=t[2]
    elif len(t)==4:
        t[0]=t[2] + t[3]
    else:
        t[0]=t[1]
    #t[0]=t[0].lstrip('|')
    #print 't[0] en optional_args:%s'%t[0]

def p_defaults_chain(t): #jsp
    '''defaults_chain : defaults_ex COMMA defaults_chain
    | defaults_ex'''
    global active_lang
    #print 't en p_defaults_chain: %s' % [x for x in t]
    if len(t)==4:
        t[0]=t[1] + t[2] + t[3]
    else:
        t[0]=t[1]

def p_defaults_ex(t):#jsp
    '''defaults_ex : QUESTION ID EQUAL defaults_item
    | QUESTION defaults_item'''
    global active_lang
    if len(t)==5:
        t[0]=t[2].strip('%') + t[3] + t[4]
    else:
        t[0]=t[2]

def p_defaults_item(t):#jsp
    '''defaults_item : expr
    | path_elem'''
    #print 't en p_defaults_item: %s' % [x for x in t]
    t[0]=t[1]

def p_idlist(t): #ok
    '''idlist : idel
    | idel COMMA idlist
    | empty'''
    if t[1]==None:
        t[0]=''
    elif len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1]+t[2]+t[3]

def p_idlist2(t): #ok
    '''idlist2 : ID idop ID
    | ID idop idlist2'''
    t[0]=t[1].strip('%')+t[2]+t[3].strip('%')

def p_idop(t):
    '''idop : COMMA
    | SEMI'''
    t[0]=t[1]

def p_idel(t): #Cambio para macros. REVISAR!!!
    '''idel : ID
    | MACROID'''
    t[0]=t[1].strip('%')

# def p_idfunlist(t): #RECUPERAR ESTE CAMBIO SI VA MAL
    # '''idfunlist : idfunitem
    # | idfunitem COMMA idfunlist'''
    # global active_lang,csharp_builder
    # #print 't en idfunlist: %s' %[el for el in t]
    # if len(t)==2:
            # t[0]= t[1]
    # else:
        # if active_lang=='csharp':
            # t[0]=csharp_builder.process_idfunitem(t[1]) + t[2] +  t[3]
        # elif active_lang=='java':
            # t[0]=java_builder.process_idfunitem(t[1]) + t[2] +  t[3]
        # else:
            # t[0]=t[1] + t[2] +  t[3]
    # #print 't[0] en idfunlist: %s' % t[0]


def p_idfunlist(t): #ok
    '''idfunlist : idfunitem
    | idfunitem COMMA idfunlist'''
    global active_lang,csharp_builder
    #print 't en idfunlist: %s' %[el for el in t]
    if len(t)==2:
        t[0]= t[1]
    else:
        t[0]=t[1] + t[2] +  t[3]
    #print 't[0] en idfunlist: %s' % t[0]


def p_idfunitem(t): #%%%%%REVISARLOOOOO%%%%%%%quien usa this dot id?????
    '''idfunitem : ID
    | THIS DOT ID
    | ID AS generic'''
    global active_lang,py_checks,__strict_mode,cpp_builder
    #print 't en idfunlist: %s' %[el for el in t]
    if len(t)==2:
        t[0]=t[1].strip('%')
    else:
        if active_lang in ['python','cython']:
            py_checks.append([t[1],t[3].strip('%')])
            t[0]=t[1].strip('%')
        elif active_lang=='c++':
            t[0]=cpp_builder.process_idfunitem(t)
        elif active_lang=='csharp':
            t[0]=csharp_builder.process_idfunitem(t)
        elif active_lang=='java':
            t[0]=java_builder.process_idfunitem(t)
        elif active_lang in ['js']  and __strict_mode==1:
            raise Exception('Error: en el parametro de funcion al definir "%s" como "%s": %s no acepta variables con tipo explicito'%(t[1],t[3],active_lang))
        else: #????
            if t[1]=='.':
                #print 'paso por idfunitem con el .'
                t[0]=t[1].strip('%')+ t[2] +t[3].strip('%') 
            else:
                t[0]=t[3].strip('%')+ ' ' +t[1].strip('%')      


#Enums------------------------------------------------
def p_enum_st(t):#cy
    ''' enum_st : ENUM ID COLON enum_item_list END'''
    global active_lang,csharp_builder,cpp_builder,js_builder,__strict_mode
    t[2]=t[2].strip('%')
    if active_lang=='js'  and __strict_mode==1:
        raise Exception('Error: No se permiten enums en JavaScript')
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_enum(t[2],t[4])
    elif active_lang=='java':
        t[0]=java_builder.process_enum(t[2],t[4])
    elif active_lang=='c++':
        t[0]=cpp_builder.process_enum(t[2],t[4])
    elif active_lang=='cython':
        t[0]='cdef enum ' + t[2] + ':\n\t' + t[4] + '\n'
    else:
        t[0]=build_enum(t[2],t[4])

def p_enum_item_list(t):
    ''' enum_item_list : enum_item
    | enum_item COMMA enum_item_list'''
    global enum_counter

    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2] + t[3]
    #poner a cero el contador
    enum_counter=0


def p_enum_item(t):
    ''' enum_item :  ID
    | ID EQUAL NUMBER'''
    global enum_counter
    t[1]=t[1].strip('%')
    #enum_counter se incrementa en una unidad para cada campo. Si
    #se especifica un valor, se actualiza a partir de ese valor
    if len(t)==2:
        t[0]=t[1] + '=' + str(enum_counter)
    else:
        t[0]=t[1] + t[2] + t[3]
        enum_counter=int(t[3])
    enum_counter+=1

def p_webserver_section(t):#jsp #cambiado para sesiones. Revisar
    '''webserver_section : WEBSERVER NUMBER COLON global_sect servlet_list END'''
    global outstring,py_template,cs_template,active_lang,urls
    if active_lang=='python':
        t[0]=t[4] + t[5] + '\n'
        t[0]+='app = Application(' + str(tuple(urls)) + ',globals())\n'
        t[0]+="python_runtime.SESSION = web.session.Session(app, web.session.DiskStore('sessions'))\n"
        t[0]+='app.run( port= ' + str(int(t[2])) + ')\n'
    else: #C#
        pass


def p_servlet_list(t):#jsp
    '''servlet_list : FOR STRING WEBGET COLON servlet_item_list WEBPOST COLON servlet_item_list END
    | FOR STRING WEBGET COLON servlet_item_list WEBPOST COLON servlet_item_list END servlet_list'''
    global outstring, py_template,cs_template,webpy_template,srv_name,srv_counter,active_lang,urls
    if active_lang=='python':
        if len(t)==10:
            #Ajustar espacios del codigo y cambiar response por return
            out1=''
            for i in t[5].split('\n'):
                if 'response' in i and  i.index('response')==0:
                    i=i.replace('response','return')
                out1+=' '*8 + i + '\n'
            out2=''
            for i in t[8].split('\n'):
                if 'response' in i  and i.index('response')==0:
                    i=i.replace('response','return')
                out2+=' '*8 + i + '\n'
            t[0]=webpy_template
            t[0]=t[0].replace('%%servname%%',srv_name + str(srv_counter))
            t[0]=t[0].replace('%%servgetcode%%',out1)
            t[0]=t[0].replace('%%servpostcode%%',out2)
            urls.append(t[2].strip('"'))
            urls.append(srv_name + str(srv_counter))
            srv_counter+=1
        else:
            #Ajustar espacios del codigo
            out1=''
            for i in t[5].split('\n'):
                if 'response' in i  and i.index('response')==0:
                    i=i.replace('response','return')
                out1+=' '*8 + i + '\n'
            out2=''
            for i in t[8].split('\n'):
                if 'response' in i  and  i.index('response')==0:
                    i=i.replace('response','return')
                out2+=' '*8 + i + '\n'
            t[0]=webpy_template
            t[0]=t[0].replace('%%servname%%',srv_name + str(srv_counter))
            t[0]=t[0].replace('%%servgetcode%%',out1)
            t[0]=t[0].replace('%%servpostcode%%',out2)
            t[0]+=t[10]
            urls.append(t[2].strip('"'))
            urls.append(srv_name + str(srv_counter))
            srv_counter+=1
        #print urls
    else: #C#
        pass
        

def p_servlet_item(t):#jsp
    '''servlet_item : valid_st SEMI
    | RESPONSE expr SEMI
    | empty'''
    if not t[1]:
        t[0]=''
    elif len(t)==4:
        t[0]=t[1] + ' ' + t[2] + '\n'
    else:
        t[0]=t[1] + '\n'


def p_servlet_item_list(t):#jsp
    '''servlet_item_list : servlet_item
    | servlet_item servlet_item_list'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2]


def p_global_sect(t):#jsp
    '''global_sect : GLOBAL order_list END'''
    t[0]=t[2]

#Para permitir variables globales en las funciones(ahora las implementa como privadas todas)
def p_global_vars(t):#revisar jsp. REVISAR CAMBIO PARA MACROS!!
    '''global_vars : GLOBAL idlist'''
    global active_lang,defined_ids,INSIDE_FUNC,IN_MACRODEF,__strict_mode
    #if INSIDE_FUNC==0 and IN_MACRODEF==0:
    #    raise Exception('Error: Las referencias a variables globales solo se permiten dentro del ambito de una funcion')
    if active_lang in ['python']:
        if INSIDE_FUNC==0 and IN_MACRODEF==0 and __strict_mode==1:
            raise Exception('Error: Las referencias a variables globales en Python solo se permiten dentro del ambito de una funcion')
        else:
            t[0]=t[1] + ' ' + t[2]
    elif active_lang=='js':
        t[0]=js_builder.process_global_vars(INSIDE_FUNC,IN_MACRODEF,t[2])
    elif active_lang in ['java', 'csharp'] and __strict_mode==1:
        raise Exception('Error definiendo %s: No se admite la definicion de  variables globales en CSharp o Java' % t[2])
    else:
        t[0]=t[2]
    
def p_order_list(t): #cy
    '''order_list : valid_st SEMI
    | valid_st SEMI order_list'''
    #Eliminar ";" de los bloques
    global active_lang
    #print 'Len(t) en order_list: %s' % len(t)
    #print 'Valor de t en order_list: %s' % [el for el in t]
    if t[1]==None: t[1]=''
    #NO TOCAR EL ESPACIO EN PYTHON!!!!!!!!! Y EN LOS DEMAS?????
    if active_lang not in ['python','cython','java']:
        #t[1]=t[1].strip(" ").strip('\n')
        t[1]=t[1].strip()
    #print '---------------------------------------'
    #print 't[1][:7]: %s'%t[1][:7]
    #print 'Valor de t[1] en order_list: %s' % repr(t[1])
    if t[1]=='^': t[1]=''
    if t[1] and t[1][-1]=='^': t[1]=t[1][:-1]
    #if len(t)==4:
    #    print 'valor de t[3]: %s' % t[3]
    #print 'Valor de t[2]: %s' % t[2]
    if t[1] and type(t[1])==type([]):
        t[1]=t[1][1] #Es un "text id to..."
    if t[1] and len(t[1])>=9 and t[1][:7]=='foreach':
        #print 'arreglando un foreach????'
        t[0]=t[1] if len(t)==3 else t[1] + t[3] + '\n'   
    elif t[1] and t[1][:2]=='if':
        t[0]=t[1] if len(t)==3 else t[1] + t[3]
    elif t[1] and t[1][:2]=='do':
        t[0]=t[1] if len(t)==3 else t[1] + t[3]
    elif t[1] and t[1][:3]=='for':
        t[0]=t[1] if len(t)==3 else t[1] + t[3]        
    elif t[1] and t[1][:5]=='while':
        t[0]=t[1] if len(t)==3 else t[1] + t[3]
    elif t[1] and t[1][:6]=='switch':#?????
        t[0]=t[1] if len(t)==3 else t[1] + t[3]        
    else: #ESTO HAY QUE REVISARLO(sobran caminos 3 y 4 aparentemente)(no, no sobran) 
        if active_lang in ['python','cython']:
            if len(t)==3 and t[1]:
                #print 'camino 1'
                t[0]=t[1] + '\n'
            else:
                if t[1]:
                    #print 'camino 2'
                    t[0]=t[1] + '\n' + t[3] + '\n'
                    #print 'Valor de t[0]: %s' % t[0]
                else:
                    if len(t)==4:
                        #print 'camino 3'
                        t[0]=t[3] + '\n'
                    else:
                        #print 'camino 4'
                        t[0]=t[1] + '\n'
        else:
            #print 'recortando lo de onflag en: %s'%t[1]
            if len(t)==3 and t[1]:#Cambio para evitar el ; en onflag
                #print 'valor de t[1] aqui: %s' % t[1]
                if t[1] in ['','\n']:
                    t[0]=''
                elif t[1].strip('\n')[-1]=='^':
                    t[0]=t[1][:-1]
                    #print 'recortando cadena!!!!'
                else:
                    t[0]=t[1] + t[2] + '\n'
            else:
                if t[1]=='':
                    if len(t)>=4: #OJO: CAMBIO PARA USAR MACROS EN JS
                        t[0]=t[3] + '\n' #ANTES TODO ERA ESTA LINEA!!!
                    else:
                        t[0]=t[1]
                elif t[1]:
                    if t[1].strip() and  t[1].strip()[-1]=='^':
                        t[0]=t[1][:-1] + t[3] + '\n'
                        #print 'recortando cadena2!!!!'
                    else:
                        t[0]=t[1] + t[2] + t[3] + '\n'
                else:
                    if len(t)==4:
                        t[0]=t[3] + '\n'
                    else:
                        t[0]=t[1] + '\n'
    if t[0]==None: t[0]=''
    #print '-----------------------------------------'
    #print 'valor de t[0] en order_list:%s' %t[0] # repr(t[0])


#Gestion de threads-----------------------------------------------------------
def p_valid_st(t): #ok #VIGILAR ADICION DE SEQUENCE Y CAST_ST!!!
    '''valid_st : var_decl
    | assign_exp
    | condic_expr
    | incr_st
    | return_st
    | break_st
    | continue_st
    | yield_st
    | if_st
    | cond_st
    | while_st
    | loopwhen_st
    | foreach_st
    | for_st
    | empty
    | create_st
    | textwrite_st
    | binarywrite_st
    | copy_st
    | delete_st
    | try_st
    | assert_st
    | raise_st
    | run_st
    | run_native_st
    | multassign_st
    | multassign2_st
    | typedef_st
    | typeinst_st
    | serialize_st
    | native
    | namespace
    | fundef_section
    | class_section
    | let2_st
    | quote_st
    | quotedef_st
    | macrodef_st
    | macroid_st
    | macrocall
    | quote_sum
    | quote_expr
    | pipeline_st
    | free_st
    | global_vars
    | typed_assign
    | thread_st
    | array
    | cast_st
    | setflag_st
    | unsetflag_st
    | onflag_st
    | apply_code_st
    | c_static_call
    | assign_generic
    | with_block'''
    global active_lang
    if t[1]==None: t[1]=''
    if type(t[1])==type([]):
        t[0]=t[1]
    else:
        if active_lang in ['python','cython']:
            t[0]=t[1] + '\n'#REVISAR ESTE RETORNO DE LINEA(puesto por fallo en condic_expr como valid_st,se pega a la siguiente linea)
        else:
            t[0]=t[1] + '\n' ##Revisarlo: facilita lectura: alguna contraindicacion?????
    #print 't[0] en valid_st: %s' % t[0]


#Nuevo: Bloque with
def p_with_block(t):
    '''with_block : WITH idlist COLON order_list END'''
    global active_lang,indent,js_builder,csharp_builder,cpp_builder,__strict_mode
    if active_lang in ['python','cython']:
        t[0]= 'with ' + t[2] + ':\n'
        #Actualizar indent
        indent+='    '
        for it in t[4].split('\n'):
            t[0]+=indent + it + '\n'
        t[0]+='\n'
        #Actualizar indent(quitar 4 espacios)
        indent=indent[-4]
        indent+='    '
    elif active_lang=='js':
        raise Exception("No implementado bloque with en JavaScript")
    elif active_lang=='java':
        raise Exception("No implementado bloque with en Java")
    elif active_lang=='csharp':
        raise Exception("No implementado bloque with en C#")
    else:
        if __strict_mode==1:
            raise Exception('Error: Los bloques with solo se permiten en Python y JavaScript')

#Traduccion condicional-----------------------------------------------------
def p_setflag_st(t):
    '''setflag_st : SETFLAG ID'''
    global __flags
    t[2]=t[2].strip('%')
    if not t[2] in __flags: __flags.append(t[2])
    t[0]=''

def p_unsetflag_st(t):
    '''unsetflag_st : UNSETFLAG ID'''
    global __flags
    t[2]=t[2].strip('%')
    if t[2] in __flags: del __flags[__flags.index(t[2])]
    t[0]=''

def p_onflag_st(t):
    '''onflag_st : ONFLAG flag_id COLON flag_elem END
    | ONFLAG ID COLON flag_elem END
    | ONFLAG flag_id COLON flag_elem ELSE COLON flag_elem END
    | ONFLAG ID COLON flag_elem ELSE COLON flag_elem END'''
    global __flags
    #print 'valor de FLAGS: %s' % __flags
    #Quitar espacios y posibles ; terminales
    t[0]=''
    elems=t[2].strip('%').split(';') #Primero los or
    if len(t)==6:
        for item in elems: #y luego los and
            if not ',' in item:
                if item in __flags:
                    t[0]=t[4]
                    break
            else:
                ands=item.split(',')
                for p in ands:
                    if not p in __flags:
                        abort=1
                if abort==1:
                    t[0]=''
                else:
                    t[0]=t[4]
    else:
         for item in elems:
             if not ',' in item:
                 if item in __flags:
                     t[0]=t[4]
                 else:
                     t[0]=t[7]
             else:
                 ands=item.split(',')
                 abort=0 #????????
                 for p in ands:
                     if not p in __flags:
                         abort=1
                 if abort==1:
                     t[0]=t[7]
                 else:
                     t[0]=t[4]
    if active_lang!='python':
        #print 't[0] antes del strip: %s' % t[0]
        #print '} in t[0]:%s' % ('}' in t[0])
        #Aqui hay un problema: para funciones y clases mete un ; donde no va y hay que quitarlo
        #y para sentencias individuales
        t[0]=t[0].strip().strip('\n').strip(';')
        if t[0] and t[0]!='' and  '}' in t[0]:
            t[0]+= '^' #Para que se usa esto?????????
        else:
            t[0]+= ';^'#Para que se usa esto?????????
    #print 'valor de t[0] en onflag: %s' %repr(t[0])
    #print 'saliendo de onflag!!'
                
    
def p_flag_elem(t):
    '''flag_elem :  order_list'''
    t[0]=t[1]

def p_flag_id(t):
    '''flag_id : idlist2'''
    t[0]=t[1]

def p_c_pointer_st(t):
    '''c_pointer_st : PIPE path_elems_list ARROW funcall PIPE
    | PIPE path_elems_list ARROW path_elems_list PIPE'''
    global active_lang,__strict_mode
    if active_lang!='c++' and __strict_mode==1:
        raise Exception("Error: El uso de punteros solo se permite en C++")
    t[0]=t[2] + t[3] + t[4]


def p_thread_st(t):#nuevo
    '''thread_st : THREAD ID IS ID opt_ptcargs opt_join'''
    global active_lang,csharp_builder,cpp_builder,js_builder
    t[2]=t[2].strip('%')
    t[4]=t[4].strip('%')
    #global tr_counter,tr_name
    #tname=tr_name + '_' + str(tr_counter)
    if active_lang in ['python','cython']:
        if t[5]=='':
            t[0]= t[2] + '= threading.Thread(target=' + t[4] + ',args=())\n'
        else:
            t[0]= t[2] + '= threading.Thread(target=' + t[4] + ',args=(' + t[5] + '))\n'
        t[0]+=t[2] + '.start()\n'
        if t[6]=='join':
            t[0]+= t[2]+ '.join()\n'
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_thread(t[2],t[4],t[6],t[5])
    elif active_lang=='java':
        t[0]=java_builder.process_thread(t[2],t[4],t[6],t[5])
    elif active_lang=='c++':
        t[0]=cpp_builder.process_thread(t[2],t[4],t[6],t[5])
    else:
        t[0]=''

def p_opt_join(t):
    '''opt_join : JOIN
    | empty'''
    t[0]=t[1]

def p_opt_ptcargs(t):
    '''opt_ptcargs : WITH expr_list
    | empty'''
    if len(t)==3:
        t[0]=t[2]
    else:
        t[0]=t[1]

def p_free_st(t):#jsp
    '''free_st : LCURLY free_idlist RCURLY'''
    t[0]=t[2]

def p_free_idlist(t):#jsp
    '''free_idlist : free_id_item free_idlist
    | free_id_item'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2]

def p_free_id_item(t):#jsp
    '''free_id_item :
    | condic_expr
    | assign_exp
    | DOT
    | COLON
    | BEGIN
    | END'''
    global __quotedefs
    decorative=['.',':','begin','end']
    if '@' + t[1] in __quotedefs:
        t[0]=__quotedefs['@' + t[1]]
    elif t[1] not in decorative:
        t[0]=t[1] + '\n'
    else:
        t[0]=''

def p_let_st(t):#jsp
    '''let_st : LET id_dict IN order_list END'''
    global active_lang,indent,let_name,let_counter
    if active_lang in ['python','cython']:
        #Actualizar indent
        indent+='    '
        name= let_name + 'func' + str(let_counter)
        t[0]='def ' + name + '(' + t[2] + '):\n'
        ords=t[4].strip().split('\n')
        for it in ords[:-1]:
            t[0]+=indent + it + '\n'
        t[0]+=indent + 'return ' + ords[-1]
        t[0]+='\n'
        #Actualizar indent(quitar 4 espacios)
        indent=indent[-4]
        #t[0]+=name + '()\n'
        t[0]=[name + '()\n',t[0]]
        #Actualizar contador
        let_counter+=1
    elif active_lang=='js':
        t[0]=js_builder.process_let(t[2],t[4])
    else:
        if __strict_mode==1:
            raise Exception('Error: Solo se permite el uso de let en python y JavaScript')
        
def p_let2_st(t):#jsp
    '''let2_st : LET id_dict IN order_list END'''
    global active_lang,indent,let_name,let_counter
    if active_lang in ['python','cython']:
        #Actualizar indent
        indent+='    '
        name= let_name + 'func' + str(let_counter)
        t[0]='def ' + name + '(' + t[2] + '):\n'
        for it in t[4].strip().split('\n'):
            t[0]+=indent + it + '\n'
        t[0]+='\n'
        #Actualizar indent(quitar 4 espacios)
        indent=indent[-4]
        t[0]+=name + '()\n'
        #Actualizar contador
        let_counter+=1
    elif active_lang=='js':
        t[0]=js_builder.process_let(t[2],t[4])
    else:
        if __strict_mode==1:
            raise Exception('Error: Solo se permite el uso de let en python y JavaScript')

def p_id_dict(t): #jsp
    '''id_dict : PIPE id_pair_list PIPE'''
    global d_name,d_counter,aux_string,active_lang
    if active_lang in ['python','cython']:
        t[0]=t[2]
    else:
        t[0]=t[2]

def p_id_pair(t): #jsp
    '''id_pair : ID COLON condic_expr'''
    global active_lang
    if active_lang in ['python','cython']:
        t[0]=t[1].strip('%') + '=' + t[3]
    else:
        t[0]='var ' + t[1].strip('%') + '=' + t[3] + ';'

def p_id_pair_list(t): #jsp
    '''id_pair_list : id_pair COMMA id_pair_list
    | id_pair
    | empty'''
    global active_lang
    if active_lang in ['python','cython']:
        t[0]=t[1] if len(t)==2 else t[1] + t[2] + t[3]
    else:
        t[0]=t[1] + '\n' if len(t)==2 else t[1] + '\n' + t[3]    

def p_new_st(t): #Revisar esto!!!!!
    '''new_st : NEW generic
    | NEW generic LPAREN defaults_chain RPAREN
    '''
    global active_lang,js_builder
    if active_lang=='js':
        t[0]=js_builder.process_new(t)
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_new(t)
    elif active_lang=='java':
        t[0]=java_builder.process_new(t)
    elif active_lang=='c++':
        t[0]=cpp_builder.process_new(t)
    elif len(t)==3:
        t[0]=t[2] + '()'
    else:
        t[0]=t[2] + t[3] + t[4] + t[5]
    #print 't[0] en new_st: %s' %t[0]

def p_typedef_st(t): #cy
    '''typedef_st : TYPEDEF ID AS types_list
    | TYPEDEF ID SELECT options_list
    | TYPEDEF ID AS ARRAY LBRACK expr_list RBRACK
    | TYPEDEF ID AS ARRAY FROM ID
    | CTYPEDEF generic AS generic 
    | CTYPEDEF generic
    '''
    global __inclass,INSIDE_FUNC,__typedefs,__classes,type_choice,options_list,__strict_mode,cpp_builder,csharp_builder
    #Solo permitimos definirlos fuera de clases y funciones
    t[2]=t[2].strip('%')
    if t[1]!='ctypedef' and active_lang=='c++' and __strict_mode==1: raise Exception('Error: Para el lenguaje objetivo C++ solo se acepta ctypedef')
    if t[1]=='ctypedef' and active_lang=='c++' and len(t)==3 and  __strict_mode==1: raise Exception('Error: Para el lenguaje objetivo C++ solo se acepta ctypedef generic as generic')
    if t[1]=='ctypedef' and active_lang!='cython' and __strict_mode==1: raise Exception('Error: solo se permite ctypedef cuando el lenguaje objetivo es Cython')
    if t[1]=='ctypedef':
        if active_lang=='cython':
            if len(t)==3:
                t[0]= t[1] + ' ' + t[2] + '\n'
            else:
                t[0]= t[1] + ' ' + t[2] + ' ' + t[4] + '\n'
        elif active_lang=='c++':
            t[0]=cpp_builder.process_ctypedef(t[2],t[4])
    else:
        if __inclass==1 or INSIDE_FUNC==1:
            raise Exception('Error: solo se permite definir tipos basados en listas fuera de funciones y clases')
        #Comprobar que no esta repetido
        if t[2] in __typedefs or t[2] in [i[0] for i in __classes] and __strict_mode==1:
            raise Exception('Error: el tipo "%s" ya esta definido'%t[2])
        if len(t)==8:
            __typedefs[t[2]]=(1,t[6])
            t[0]='__typedefs["' + t[2] + '"]=(1,' + t[6] + ')\n'
            #print __typedefs
        elif len(t)==7:
            t[6]=t[6].strip('%')
            if t[2]==t[6]:
                raise Exception('Error: No se admiten definiciones recursivas ("%s" en terminos de "%s"'%(t[2],t[6]))
            if t[6] not in __typedefs:
                if t[6] not in [i[0] for i in __classes]:
                    raise Exception('Error: El tipo "%s" no esta definido.' %t[6])
            __typedefs[t[2]]=(3,[t[6]])
            t[0]='__typedefs["' + t[2] + '"]=(3,"' + t[6] + '")\n'
            #print __typedefs
        else:
            if type_choice==1:
                #Comprobar que todos son tipos validos
                for el in options_list[:]: #?????
                    if el not in __typedefs:
                        if el not in [i[0] for i in __classes]:
                            raise Exception('Error: El tipo "%s" no esta definido.' %el)
                __typedefs[t[2]]=(2,t[4].strip('"') if t[4][0]=='"' else t[4])
                t[0]='__typedefs["' + t[2] + '"]=(2,' + str(t[4]) + ')\n'
                type_choice=0
                options_list=[]
            else:
                #Comprobar que todos son tipos validos
                for el in t[4].split(','):
                    if el not in __typedefs:
                        if el not in [i[0] for i in __classes]:
                            raise Exception('Error: El tipo "%s" no esta definido.' %el)        
                __typedefs[t[2]]=(0,t[4])
                t[0]='__typedefs["' + t[2] + '"]=(0,"' + t[4] + '")\n'
    #print __typedefs
    #'__type_instancest[0]=t[1]

def p_types_list(t):#jsp
    '''types_list : basic_type COMMA types_list
    | basic_type COMMA basic_type
    | basic_type'''
    if len(t)==4:
        t[0]=t[1] + ',' + t[3]
    else:
        t[0]=t[1]


def p_basic_type(t):#jsp
    '''basic_type : ID
    | NUMERIC
    | CHAIN'''
    #Si es numeric o chain , debe ser tipo 1, y no 0 como es por defecto
    global type_choice
    if t[1] in ['numeric','chain']: 
        type_choice=1
        t[0]='"' + t[1].strip('%') + '"'
    else:
        t[0]=t[1].strip('%')

def p_options_list(t):#jsp
    '''options_list : type_expr_elem COMMA options_list
    | type_expr_elem'''
    global options_list
    global type_choice
    type_choice=1
    if len(t)==3:
        if type(t[3])!=type([]):
            if t[1]==t[3]:
                raise Exception('Error: los tipos opcionales deben ser distintos')
            options_list.append(t[3])
            options_list.append(t[1])
    else:
        options_list.append(t[1])
    t[0]=options_list  


def p_type_expr_elem(t):#jsp
    '''type_expr_elem : expr
    | NUMERIC
    | CHAIN'''
    t[0]=t[1]

def p_typeinst_st(t):#jsp
    '''typeinst_st : ID IS NEW ID expr'''
    t[1]=t[1].strip('%')
    t[4]=t[4].strip('%')
    if not t[1] in defined_ids:
        raise Exception('Error: el identificador "%s" no esta definido'%t[1])
    if not t[4] in __typedefs:
         if not t[4] in [i[0] for i in __classes]:
            raise Exception('Error: el tipo "%s" no esta definido'%t[4])
    kind,tplist=__typedefs[t[4]]
    #print tplist
    if type(tplist)==type([]):
        if kind==0:
            if len(t[5])!=len(tplist):
                raise Exception('Error: Los argumentos de la definicion de la instancia "%s" no coinciden con los de la definicion del tipo "%s"' % (type_exprs,tplist))
    #Cambio:Comprobamos igual que en los condicionales
    #if not python_runtime.listMatchType(t[5],tplist,kind):
    #    raise Exception('Error: Los argumentos no coinciden con los de la plantilla del tipo-lista')
    if type(tplist)==type([]):
        t[0]='if not python_runtime.listMatchType(' + t[5] + ',' +  str(tplist) + ',' + str(kind) + ',__typedefs):\n'
    else:
        #print "Valor de tplist:%s" % tplist
        if not tplist[0] in ['"',"'"]:
            t[0]='if not python_runtime.listMatchType(' + t[5] + ',"' +  tplist + '",' + str(kind) + ',__typedefs):\n'
        else:
            t[0]='if not python_runtime.listMatchType(' + t[5] + "," + tplist + "," + str(kind) + ',__typedefs):\n' #REVISARLOOOO
    t[0]+='    raise Exception(\'Error: Los argumentos no coinciden con los de la plantilla del tipo-lista\')\n'
    #Todo bien, dar de alta la instancia----------
    #t[0]+='__type_instances["' + t[1] + '"]=' + t[5] + '\n'
    t[0]+=t[1] + '=' + t[5] + '\n'
    __type_instances[t[1]]=t[5]
    #---------------------------------------------
    #print __type_instances
    #print __typedefs

def p_macrodef_st(t):#jsp
    '''macrodef_st : start_macrodef MACRO ID LPAREN macroid_list RPAREN COLON order_list END end_macrodef'''
    global __macros,__strict_mode
    t[3]=t[3].strip('%')
    if t[3] in __macros and __strict_mode==1:
        raise Exception('Error: la macro "%s" ya esta definida'%t[2])
    args=t[5]
    #print 'Argumentos de la macro: %s' % t[5]
    __macros[t[3]]=[t[8],[x.strip() for x in t[5].split(',')]]
    #print "Macros definidas: %s" % __macros
    t[0]=''

def p_start_macrodef(t):#jsp
    '''start_macrodef : empty'''
    global IN_MACRODEF
    IN_MACRODEF=1
    t[0]=''

def p_end_macrodef(t):#jsp
    '''end_macrodef : empty'''
    global IN_MACRODEF
    IN_MACRODEF=0
    t[0]=''

def p_macroid_st(t):#jsp
    '''macroid_st : MACROID'''
    global IN_MACRODEF
    if IN_MACRODEF==0: raise Exception("Error: Solo se permite usar un MACROID dentro de la definicion de una macro")
    t[0]=t[1]

def p_macroid_list(t):#jsp
    '''macroid_list : macroid_st COMMA macroid_list
    | macroid_st'''
    if len(t)==4:
        t[0]=t[1] + ',' + t[3]
    else:
        t[0]=t[1]

def p_macrocall(t):#jsp #asumimos que todas las macros llevan argumentos??? 
    '''macrocall : CODEID LPAREN quote_list RPAREN'''
    global __macros, macro_name,macro_counter,indent
    code=expand_macro(t[1][1:],findElements(t[3]))
    macro_counter+=1
    t[0]=''
    for line in code.split('\n'):
        t[0]+=line + '\n'

def p_macrocall2(t):#jsp #asumimos que todas las macros llevan argumentos???
    '''macrocall2 : CODEID LPAREN quote_list RPAREN'''
    #print 'EN MACROCALL!!!!!!!'
    global __macros, macro_name,macro_counter,indent,parser,__program,outstring,to_reeval
    #print 'resultado de findElements: %s' %findElements(t[3])
    code=expand_macro(t[1][1:],findElements(t[3]))
    #print 'codigo de la macro expandido:%s' % code
    name=macro_name + str(macro_counter)
    macro_counter+=1
    t[0]='def ' + name + '():\n'
    indent+='    '
    for line in code.split('\n'):
        t[0]+=indent + line + '\n'
    t[0]+='\n'
    indent=indent[:4]
    t[0]=[name + '()',t[0]]

def p_quote_st(t):#jsp#REVISAR ESTE CAMBIO!!!!!!!
    '''quote_st : ARROBA LPAREN order_list RPAREN'''
    #t[0]='@' + t[3] + ';'
    t[0]=t[3]

def p_quotedef_st(t):#jsp#REVISAR ESTE CAMBIO!!!!!!!
    '''quotedef_st : ARROBA LPAREN order_list RPAREN AS CODEID'''
    global __quotedefs #dar de alta el quotedef
    __quotedefs[t[6]]=t[3]
    t[0]=''

def p_quote_list(t):#jsp
    '''quote_list : quote_item COMMA quote_list
    | quote_item'''
    if len(t)==4:
        t[0]=t[1] + ',' + t[3]
    else:
        t[0]=t[1]

def p_quote_item(t):#jsp #REVISAR ESTE CAMBIO!!!!!!!
    '''quote_item : valid_st ARROBA'''
    t[0]=t[1]

def p_quote_expr(t):#jsp
    '''quote_expr : CODEID'''
    global __quotedefs
    if not  t[1] in __quotedefs:
        raise Exception('Error: No se ha definido el quotedef "%s"'%t[1])
    t[0]=__quotedefs[t[1]]

def p_quote_sum(t):#Pendiente implementar el resto de las operaciones
    '''quote_sum : quote_op_item quote_op quote_op_item
    | quote_op_item quote_op quote_op_item AS CODEID'''
    global __quotedefs
    t[0]=''
    if len(t)==4:
        t[0]=t[1] +'\n' +  t[3]
    else:
        __quotedefs[t[5]]=t[1] + t[3]

def p_quote_op_item(t):
    '''quote_op_item : quote_item
        | quote_expr'''
    t[0]=t[1]
    
    
def p_quote_op(t):
    '''quote_op : PLUS
        | MINUS
        | TIMES
        | IN'''
    t[0]=t[1]

def p_apply_code_st(t):
     '''apply_code_st : APPLY sust_list TO CODEID AS CODEID
        | APPLY quote_list IN ID TO CODEID AS CODEID'''
     global __quotedefs
     if len(t)==7:
         if not t[6] in __quotedefs: __quotedefs[t[6]]=""
         t[0]=__quotedefs[t[4]]
         #print "sust_list: %s" % t[2]
         for item in t[2].split('____%%%%____'):
             new,old=item.split("||____||")
             t[0]=replaceWithFormat(t[0],old,new.lstrip(),findInLines(old,t[0]),t[0])
     else:
         if not t[8] in __quotedefs: __quotedefs[t[8]]=""
         temp=__quotedefs[t[6]]
         #print 'valor de temp: %s'%temp
         t[0]=''
         #print "sust_list: %s" % t[2]
         for item in t[2].split(','):
             t[0]+=replaceWithFormat(temp,t[4],item.lstrip(),findInLines(t[4],temp),temp) + '\n'
             #print 't[0] aqui: %s'%t[0]
         #print 't[0] al salir: %s'%t[0]

def p_sust_list(t):
    '''sust_list : quote_op_item ARROW ID
    | quote_op_item ARROW ID COMMA sust_list'''
    if len(t)==4:
        t[0]=t[1] + "||____||" + t[3]
    else:
        t[0]=t[1] +  "||____||" + t[3] + "____%%%%____" + t[5]



def p_list_compr(t):#python,C#,js
    '''list_compr : TAKE take_var ARROW expr FROM PIPE expr_list PIPE
    | TAKE take_var ARROW expr FROM PIPE list_compr PIPE
    | TAKE take_var ARROW expr FROM PIPE expr_list PIPE WHERE condic_expr
    | TAKE take_var ARROW expr FROM PIPE list_compr PIPE WHERE condic_expr
    | TAKE LAZY take_var ARROW expr FROM PIPE expr_list PIPE
    | TAKE LAZY take_var ARROW expr FROM PIPE list_compr PIPE
    | TAKE LAZY take_var ARROW expr FROM PIPE expr_list PIPE WHERE condic_expr
    | TAKE LAZY take_var ARROW expr FROM PIPE list_compr PIPE WHERE condic_expr'''
    global active_lang,csharp_builder,cpp_builder,js_builder,__strict_mode
    vars=t[2].split(',')
    nvars=len(vars)
    if active_lang in ['python','cython']:
        #vars=t[2].split(',')
        #nvars=len(vars)
        #print vars
        if t[2]=='lazy':
           if nvars==1:
               if len(t)==10:
                   t[0]='(' + t[5] + ' for ' + t[3] + ' in list(itertools.chain('+ t[8] + ')))'
               else:
                   t[0]='(' + t[5] + ' for ' + t[3] + ' in list(itertools.chain('+ t[8] + ')) if ' + t[11] + ')'
           else:
               if len(t)==10:
                    t[0]='[' + t[5]
                    lists=findElements(t[8])
                    if len(vars)!=len(lists): raise Exception('Error: En una comprension sobre varias listas, debe coincidir el numero de variables con el numero de listas')
                    for i in range(len(vars)):
                        t[0]+= ' for ' + vars[i] + ' in ' + lists[i] + ' '
                    t[0]+=']'
               else:
                    t[0]='[' + t[5]
                    lists=findElements(t[8])
                    if len(vars)!=len(lists): raise Exception('Error: En una comprension sobre varias listas, debe coincidir el numero de variables con el numero de listas')
                    for i in range(len(vars)):
                        t[0]+= ' for ' + vars[i] + ' in ' + lists[i] + ' '
                    t[0]+=' if ' + t[11] + ']'
        elif len(t)==9:
            if nvars==1:
                t[0]='[' + t[4] + ' for ' + t[2] + ' in list(itertools.chain('+ t[7] + '))]'
            else:
                t[0]='[' + t[4]
                lists=findElements(t[7])
                if len(vars)!=len(lists): raise Exception('Error: En una comprension sobre varias listas, debe coincidir el numero de variables con el numero de listas')
                for i in range(len(vars)):
                    t[0]+= ' for ' + vars[i] + ' in ' + lists[i] + ' '
                t[0]+=']'
        else:
            if nvars==1:
                t[0]='[' + t[4] + ' for ' + t[2] + ' in list(itertools.chain('+ t[7] + ')) if ' + t[10] + ']'
            else:
                t[0]='[' + t[4]
                lists=findElements(t[7])
                if len(vars)!=len(lists): raise Exception('Error: En una comprension sobre varias listas, debe coincidir el numero de variables con el numero de listas')
                for i in range(len(vars)):
                    t[0]+= ' for ' + vars[i] + ' in ' + lists[i] + ' '
                t[0]+=' if ' + t[10] + ']'
    elif active_lang=='csharp':
        if t[2]=='lazy' and __strict_mode==1: raise Exception('Error: No se permite el uso de "lazy" en C#')
        if nvars>1  and __strict_mode==1: raise Exception('Error: No se permite el uso de mas de una variable en las comprensiones en C#')
        mapf='(' + t[2] + ')=> ' + t[4] 
        if len(t)==9:
            t[0]=csharp_builder.process_take(mapf,t[7])
        else:
            filtf='(' + t[2] + ')=>' + t[10] 
            t[0]=csharp_builder.process_take(mapf,t[7],filtf)
    elif active_lang=='java':
        if nvars>1  and __strict_mode==1: raise Exception('Error: No se permite el uso de mas de una variable en las comprensiones en Java')
        mapf='(' + t[2] + ')-> ' + t[4] 
        if len(t)==9:
            t[0]=java_builder.process_take(mapf,t[7])
        else:
            filtf='(' + t[2] + ')->' + t[10] 
            t[0]=java_builder.process_take(mapf,t[7],filtf)
    elif active_lang=='c++':
        if t[2]=='lazy' and __strict_mode==1: raise Exception('Error: No se permite el uso de "lazy" en C++')
        #if nvars>1  and __strict_mode==1: raise Exception('Error: No se permite el uso de mas de una variable en las comprensiones en C#')
        mapf='[](' + t[2] + '){ return ' + t[4] + ';}' 
        if len(t)==9:
            t[0]=cpp_builder.process_take(mapf,t[7])
        else:
            filtf='[](' + t[2] + '){ return ' + t[10]  + ';}'
            t[0]=cpp_builder.process_take(mapf,t[7],filtf)
    else:
        if t[2]=='lazy' and __strict_mode==1: raise Exception('Error: No se permite el uso de "lazy" en JS')
        if nvars>1 and __strict_mode==1: raise Exception('Error: No se permite el uso de mas de una variable en las comprensiones en JS')
        mapf='function(' + t[2] + '){ return ' + t[4] + ';}' 
        if len(t)==9:
            t[0]=js_builder.process_take(mapf,t[7])
        else:
            filtf='function(' + t[2] + '){ if(' + t[10] + '){ return ' + t[2] + ';}}' 
            t[0]=js_builder.process_take(mapf,t[7],filtf)

def p_take_var(t):
    '''take_var : idlist
       | ID AS generic'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]= t[3] + ' '  + t[1]

def p_functional_st(t): #ok
    '''functional_st :
    | filter_st
    | map_st
    | reduce_st
    | slice_st
    | group_st
    | order_st
    | linqlike_st
    | list_compr
    '''
    #####OJO####: puesto para return_st: cuando hay opciones de functional_st y algun empty, se mete por aqui
    #es una chapuza, pero lo soluciona por ahora.
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=''

def p_run_st(t):#Revisar esto: Una opcion no se utiliza
    '''run_st : RUN expr
    | RUN expr AS ID'''
    global active_lang,__strict_mode
    if active_lang=='python':
        t[0]='bridge.__reflected=1\n'
        t[0]+='exec bridge.parser.parse(' + t[2] + ')\n'
        t[0]+='bridge.__reflected=0\n'
    else:
        if __strict_mode==1:
            raise Exception('Error: La evaluacion de codigo con "run" solo se permite en python')

def p_run_native_st(t):
    '''run_native_st : RUN NATIVE expr'''
    global active_lang,__strict_mode
    if active_lang in ['python','cython']:
        t[0]='exec ' + t[3] + '\n'
    elif active_lang=='js':
        t[0]=js_builder.process_run_native(code)
    else:
        if __strict_mode==1:
            raise Exception('Error: La evaluacion de codigo nativo con "run native" solo se permite en Python y JavaScript')


def p_serialize_st(t):#jsp
    '''serialize_st : SERIALIZE path_elems_list IN expr
    | SERIALIZE path_elems_list'''
    if len(t)==5:
        t[0]='python_runtime.doSerialize(' + t[2] + ',' + t[4] + ')\n'
    else:
        t[0]='python_runtime.doSerialize(' + t[2] +')\n'


def p_deserialize_st(t):#jsp
    '''deserialize_st : DESERIALIZE FROM expr'''
    t[0]='python_runtime.doDeserialize(' + t[3] + ')\n'
    

def p_multassign_st(t): #jsp
    '''multassign_st : LBRACK multassign_elems_list RBRACK  EQUAL expr'''
    global deconstruct_name,deconstruct_counter
    name=deconstruct_name + str(deconstruct_counter)
    deconstruct_counter+=1
    head= name + '= ' + t[5] + '\n'
    toflat=t[2]
    #print 'en multassign_st con t=%s' % str([el for el in t])

    #print 'head= %s'% head
    #print 'toflat=%s'%toflat
    t[0]= head + flatDeconstructor(toflat,name)+ '\n'
    #print 't[0]:%s' % t[0]

def p_multassign_elems_list(t):
    '''multassign_elems_list : multassign_elem COMMA multassign_elems_list
    | multassign_elem'''
    #print 'en multassign_elems_list con t=%s' % str([el for el in t])
    if len(t)==4:
         t[0]=t[1]+t[2]+t[3]
    else:
         t[0]=t[1]

def p_multassign_elem(t):
    '''multassign_elem : path_elems_list
    | LBRACK multassign_elems_list RBRACK
    | NULL'''
    #print 'en multassign_elem con t=%s' % str([el for el in t])
    global active_lang
    if len(t)==4:
         t[0]=t[1]+t[2]+t[3]
    else:
        if t[1]=='null':
            t[0]='None' if active_lang in ['python','cython'] else 'null'
        else:
            t[0]=t[1]

def p_multassign2_st(t): #RECUPERAR ESTO SI NO VA EL CAMBIO!!!!!
    '''multassign2_st : path_elems_list_list  EQUAL expr
    | path_elems_list_list PIPE path_elems_list EQUAL expr'''
    global active_lang,js_builder,__strict_mode
    if active_lang=='js' and __strict_mode==1:
        if len(t)==4: raise Exception('Error: en JavaScript no se permiten asignaciones a,b=[x,y], usar [a,b]=[x,y]')
        t[0]=js_builder.process_multassign2(findElements(t[1]),t[3],t[5])
    else:
        if len(t)==4:
            t[0] =t[1] + t[2] + t[3]
        else:
            elems=findElements(t[1])
            t[0]=t[1] + ' = ' + t[5] + '[:' + str(len(elems)) + ']\n'
            t[0]+=t[3] + ' = ' + t[5] + '[' + str(len(elems)) + ':]\n'
    
def p_pipeline_st(t): #jsp
     '''pipeline_st : PIPE GT expr_list pipeline_list'''
     #t[0]=t[1]+t[2]
     t[0]=''
     funcs=[ el for el in t[4].split('|>') if el!='']
     #print 'funcs: %s' % funcs
     #root=''
     for i in range(len(funcs)):
         if i==0:
             t[0]=funcs[0] + '(' + t[3] + ')'
         else:
             t[0]=funcs[i] + '(' + t[0] + ')'
     #print 't[0] en pipeline_st: %s'%t[0]


def p_pipeline_list(t): #jsp
     '''pipeline_list : PIPE GT pipeline_item pipeline_list
     | PIPE GT pipeline_item'''
     if len(t)==5:
         t[0]=t[1]+t[2]+t[3] + t[4]
     else:
         t[0]=t[1]+t[2]+t[3]


def p_pipeline_item(t): #jsp
     '''pipeline_item : path_elems_list
     | PUT IN path_elems_list'''
     if len(t)==2:
        t[0]=t[1]
     else:
        t[0]=t[3] + '.send'

def p_var_decl(t): #REVISAR!!!!!!
    '''var_decl : SETVAR idlist
    | SETVAR idlist EQUAL init_item
    | SETVAR idlist AS generic
    | SETCVAR idlist AS generic
    | SETVAR idlist AS generic EQUAL init_item
    | SETVAR idlist AS generic ARROW funcall_generic
    | SETVAR idlist LBRACK expr RBRACK AS generic
    | SETVAR idlist LBRACK expr RBRACK AS generic EQUAL init_item'''
    global outstring,active_lang,defined_ids,INSIDE_FUNC,__strict_mode
    #print 'len(t) en setvar: %s' % len(t)
    #print 'active_lang: %s' % active_lang
    defids=t[2].split(',')
    for it in defids:
        if it in defined_ids:
            if INSIDE_FUNC==0 and __strict_mode==1:
                raise Exception('Error: el identificador "%s" ya esta definido'%it)
    if t[1]=='setcvar' and active_lang!='cython' and __strict_mode==1:
        raise Exception("Error: solo se permite usar setcvar cuando el lenguaje objetivo es cython")
    if len(t) in [3,5]:
        if active_lang=='python':
            t[0]=''
            for it in t[2].split(','):
                if len(t)==3:
                    t[0]+=it + ' = None\n'
                else:
                    if t[3]!='=' and __strict_mode==1: raise Exception('Error: python no permite definir tipos ni genericos')
                    t[0]+=it + ' = ' + t[4] + '\n'
                #Ignorar definiciones de funciones
                if INSIDE_FUNC==0:
                    defined_ids[it]='object'
        elif active_lang=='cython':
            t[0]=''
            for it in t[2].split(','):
                if len(t)==3:
                    t[0]+=it + ' = None\n'
                else:
                    if t[3]=='as' and t[1]=='setvar':
                        raise Exception("Error: Para definir una variable con tipo en Cython hay que usar setcvar")
                    if t[3]=='=':
                        t[0]+=it + ' = ' + t[4] + '\n'
                    else:
                        t[0]+='cdef ' +t[4] + ' ' + it + '\n'
        elif active_lang=='c++':
            if len(t)==3  and __strict_mode==1:
                raise Exception("Error: C++ no acepta definicion de variables sin tipo")
            elif len(t)==3:
                t[0]=cpp_builder.process_var_decl(t[2],'')
            else:
                if t[3]!='=':
                    t[0]= cpp_builder.process_var_decl(t[2],t[4])
                else:
                    t[0]= cpp_builder.process_var_decl(t[2],'',t[4])
        elif active_lang=='csharp':
            if len(t)==3  and __strict_mode==1:
                raise Exception("Error: C# no acepta definicion de variables sin tipo")
            elif len(t)==3:
                t[0]=csharp_builder.process_var_decl(t[2],'')
            else:
                if t[3]!='=':
                    t[0]= csharp_builder.process_var_decl(t[2],t[4])
                else:
                    t[0]= csharp_builder.process_var_decl(t[2],'',t[4])
        elif active_lang=='java':
            if len(t)==3  and __strict_mode==1:
                raise Exception("Error: Java no acepta definicion de variables sin tipo")
            elif len(t)==3:
                t[0]=java_builder.process_var_decl(t[2],'')
            else:
                if t[3]!='=':
                    t[0]= java_builder.process_var_decl(t[2],t[4])
                else:
                    t[0]= java_builder.process_var_decl(t[2],'',t[4])
        else:
            if len(t)==3:
                t[0]=js_builder.process_var_decl(t[2])
            else:
                t[0]=js_builder.process_var_decl(t[2],t[4])
            for it in t[2].split(','):
                defined_ids[it]='NaN'#???????
    elif len(t) in [7,8,10]: #arrays e inicializacion de listas
        if active_lang=='c++':
            if t[3]=='[':
                t[0]= cpp_builder.process_var_decl(t[2] + t[3] + t[4] + t[5],t[7])
            else:
                #print 'valor de t[6] aqui: %s' % t[6]
                t[0]= cpp_builder.process_var_decl(t[2],t[4],t[6])
        elif active_lang=='csharp':
            if len(t)==7:
                t[0]= csharp_builder.process_var_decl(t[2],t[4],t[6])
            else: #Tiene sentido el resto de las opciones?Si, si se quiere a[]=[1,2,3]
                pass
        elif active_lang=='java':
            if len(t)==7:
                t[0]= java_builder.process_var_decl(t[2],t[4],t[6])
            else: #Tiene sentido el resto de las opciones?Si, si se quiere a[]=[1,2,3]
                pass
    else: #Cambiar para python
        if active_lang=='python' and __strict_mode==1:
            raise Exception('Error definiendo "%s" como "%s": Python no acepta definir variables con tipo explicito.' % (t[2],t[4]))
        elif active_lang=='c++':
            t[0]=cpp_builder.process_var_decl(t[2],t[4])
            defined_ids[it]='cppvar'
        else:
            t[0]=t[4] + ' ' + t[2]
        for item in defids:
            defined_ids[item]=t[4]
        #print 'defined ids: %s' % defined_ids
    if active_lang in ['python','cython']:
        if t[0]:
            t[0] += '\n'
        else:
            t[0]=''
    #print 't[0] en setvar: %s' % t[0]


def p_init_item(t):
    ''' init_item : expr
    | new_st'''
    t[0]=t[1] 
    #print 'en init_item t[0]:%s' % t[0]

def p_fptr(t): #cy
    '''fptr : ARROW generic PIPE ID COLON generic_list PIPE'''
    global active_lang
    t[0]=t[2] + ' (*' + t[4] + ') (' + t[6] + ')'

def p_c_adrress(t): #Vigilar!!
    '''c_address : AMPERSAND path_elems_list
    | TIMES path_elems_list'''
    global active_lang, __strict_mode
    if active_lang in ['c++','csharp']:
        t[0]=t[1] + t[2]
    else:
        if __strict_mode==1:
            raise Exception('Error: Solo se permite el uso del operador de direccion en C++ y C#')
        else: #ignorar el statement
            t[0]=''


def p_generic(t):#Vigilar generic LBRACK NUMBER RBRACK#cy
    '''generic : idchain
    | fptr
    | LT generic_list GT
    | generic LBRACK RBRACK
    | generic LBRACK NUMBER RBRACK
    | idchain LT generic_list GT
    | generic sufix_list
    | generic DOTDOT generic'''
    global active_lang
    if len(t)==2:
        t[0]=t[1]
    elif len(t)==3:
        t[0]=t[1] + t[2]
    elif len(t)==4:
        if t[2]=='..': t[2]='::'
        t[0]=t[1]+t[2]+t[3]
    else: 
        t[0]=t[1]+t[2]+t[3]+t[4]
    #Parche para map en c++(es palabra clave en minimal)
    #if active_lang=='c++':
    #    t[0]=t[0].replace('map_','map')
    #print 't[0] en generic: %s'%t[0]        
def p_sufix_list(t): #Vigilar
    '''sufix_list : sufix_elem
    | sufix_elem sufix_list'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2]

def p_sufix_elem(t): #Vigilar
    '''sufix_elem : AMPERSAND
    | TIMES'''
    t[0]=t[1]

# def p_generic_list(t):#jsp
    # '''generic_list : generic
    # | generic COMMA generic_list'''
    # if len(t)==2:
        # t[0]=t[1]
    # else: 
        # t[0]=t[1]+t[2]+t[3]
    # #print 't[0] en generic_list: %s'%t[0]

def p_generic_list(t):#jsp
    '''generic_list : generic
    | generic COMMA generic_list
    | generic DOTDOT generic_list'''
    if len(t)==2:
        t[0]=t[1]
    else: 
        t[0]=t[1]+t[2]+t[3]
    #print 't[0] en generic_list: %s'%t[0]

#-----------------------------------------------------------------------------------------------|
#No se puede poner condic_expr en el lado derecho, porque no interpreta bien la expresion!!!!!!!|
#-----------------------------------------------------------------------------------------------|
def p_assign_exp(t):
    '''assign_exp : assignable EQUAL expr
    | assignable EQUAL functional_st
    | assignable EQUAL text_st
    | assignable EQUAL lines_st
    | assignable EQUAL binary_st
    | assignable EQUAL select_files_st
    | assignable EQUAL update_st
    | assignable EQUAL match_st
    | assignable EQUAL cut_st
    | assignable EQUAL idtotext_st
    | assignable EQUAL anonym_st
    | assignable EQUAL lambda_st
    | assignable EQUAL xml_st
    | assignable EQUAL html_st
    | assignable EQUAL consult_st
    | assignable EQUAL consult_db_st
    | assignable EQUAL new_st
    | assignable EQUAL pipeline_st
    | assignable EQUAL let_st
    | assignable EQUAL YIELD expr
    | assignable EQUAL PIPE YIELD PIPE
    | assignable EQUAL macrocall2
    | assignable EQUAL lazy_expr
    | assignable EQUAL THREAD IS ID opt_ptcargs opt_join
    | assignable EQUAL ASYNC PIPE ID expr_list PIPE
    | assignable EQUAL AWAIT ID
    | assignable EQUAL AWAIT ID THEN ID'''
    global l_name,l_counter,aux_string,outstring,active_lang,indent,INSIDE_FUNC,as_counter,as_name,__strict_mode
    #Excepciones para lenguaje no python con async y await
    if active_lang not in ['python','cython'] and t[3] in ['async','await','|'] and __strict_mode==1:
        raise Exception('Error: solo se permiten los comandos "async" y "await" y corrutinas en Python')
    if active_lang in ['python','cython']:
        #print 'en assign_exp con t[1] y t[3]: %s,%s'%(t[1],t[3])
        if t[3]=='yield': #Corrutina
            if INSIDE_FUNC==0:
                  raise Exception('Error: Expresion "yield" fuera de una definicion de funcion/corrutina')
            t[0]=t[1] + ' ' + t[2] + '(yield ' + t[4] + ')\n'
        elif t[3]=='|': #Corrutina
            if INSIDE_FUNC==0:
                  raise Exception('Error: Expresion "yield" fuera de una definicion de funcion/corrutina')
            t[0]=t[1] + ' ' + t[2] + '(yield)\n'
        elif t[3]=='async': #llamada asincrona
            t[0]= t[1] + t[2] + 'python_runtime.asynfun(' + t[5].strip('%') + ',' + t[6] + ')\n'
        elif t[3]=='await': #Espera por funcion sincrona
            if len(t)==7:
                t[0]= t[1] + t[2] + t[6].strip('%') + '(' +  t[4].strip('%') + '.result()) if not ' + t[4].strip('%') + '.running() else None\n'
            else:
                t[0]= t[1] + t[2] + t[4].strip('%') + '.result() if not ' + t[4].strip('%') + '.running() else None\n'
        elif t[3]=='thread': #Asignar un thread'''thread_st : THREAD ID IS ID opt_ptcargs opt_join'''
            if t[6]=='':
                t[0]= t[1] + '= threading.Thread(target=' + t[5] + ',args=())\n'
            else:
                t[0]= t[1] + '= threading.Thread(target=' + t[5] + ',args=(' + t[6] + '))\n'
            t[0]+=t[1] + '.start()\n'
            if t[7]=='join':
                t[0]+= t[1]+ '.join()\n' 
        elif type(t[3])==type([]):
            t[0]=t[3][1] + '\n'
            t[0]+=t[1] + ' ' + t[2] + ' ' + t[3][0] + '\n'
        else:
            t[0]=t[1] + ' ' + t[2] + ' ' + t[3] + '\n' #Ojo considerar funciones anonimas!
        if aux_string!='':#????
            outstring+=aux_string
            aux_string=''
    elif active_lang=='c++':
        t[0]=cpp_builder.process_assign(t[1],t[3])
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_assign(t[1],t[3])
    elif active_lang=='java':
        t[0]=java_builder.process_assign(t[1],t[3])
    else: #(pendiente yield)
        t[0]=js_builder.process_assign(t[1],t[3])


def p_typed_assign(t): #js,csharp. NUEVO, REVISARRRRRRRRRRRRRR!!!!!!!!!!!
    '''typed_assign : assign_exp AS generic'''
    #print 'en typed_assign'
    #print [el for el in t]
    global active_lang,js_builder 
    id,rest=t[1].split('=')
    if active_lang=='js':
        t[0]=js_builder.process_typed_assign(id,t[1],t[3])
    elif active_lang in ['python','cython']:
        #print 'valor de t[1] en typed:%s' % t[1]
        #print 'valor de t[3] en typed:%s' % t[3]
        t[0]=t[1] + 'python_runtime._checkType(' + id + ',' + buildCheckType(t[3]) + ')\n'
    else:
        t[0]=t[3].strip('\n') + ' ' + id.strip('\n') + ' = ' + rest 
    #print "t[0] en typed_assign:<-- %s  -->"%t[0]

def p_next_expr(t): #CAMBIADO NEXT POR GET!!!!!!!!!VIGILARLO!!!!!
    '''next_expr : GET expr'''
    global active_lang,js_builder
    #t[0]='next(' + t[2] + ')'
    if active_lang=='js':
        t[0]=js_builder.process_next(t[2])
    else:
        t[0]= t[2] + '.next()'

def p_send_expr(t): #python,resto error
    '''send_expr : PUT expr IN expr_list'''
    global active_lang,__strict_mode
    if active_lang not in ['python','cython'] and __strict_mode==1: raise Exception('Error: Solo se permite "put" en Python')
    t[0]=''
    funcs=[ el for el in t[4].split(',') if el!='']
    for fun in funcs:
       t[0]+= fun + '.send(' + t[2] + ')\n'

def p_lazy_expr(t): #python,resto error
    '''lazy_expr : LAZY iterable_expr'''
    global lazy_counter,lazy_name,active_lang,__strict_mode
    if active_lang not in ['python','cython'] and __strict_mode==1: raise Exception('Error: Solo se permite "lazy" en Python')
    name=lazy_name + str(lazy_counter)
    t[0]=name + ' = ' + t[2]
    t[0]=[name,t[0]]
    lazy_counter+=1
            
def p_iterable_expr(t):#jsp
    '''iterable_expr : expr'''
    #print 'Valor de t[1]:%s|"%s"' %(t[1],t[1][-2])
    if t[1][:4]=='list' and t[1][-2]!=']': t[1]=t[1].strip('list')[1:-1]
    #print 'Valor de itertools despues: %s' % t[1]
    t[0]='iter(' + t[1] + ')'

def p_ifelse(t): #Faltan resto de lenguajes!!!!!
    '''ifelse_st : expr IF condic_expr ELSE expr'''
    global active_lang
    if active_lang in ['python','cython']:
        t[0]=t[1] + ' if ' + t[3] + ' else ' + t[5] + '\n'
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_ifelse(t[1],t[3],t[5])
    elif active_lang=='c++':
        t[0]=cpp_builder.process_ifelse(t[1],t[3],t[5])
    elif active_lang=='java':
        t[0]=java_builder.process_ifelse(t[1],t[3],t[5])
    else:
        t[0]=js_builder.process_ifelse(t[1],t[3],t[5])

def p_assignable(t): #jsp
    '''assignable : path_elems_list
    | MACROID
    | c_pointer_st
    | c_address
    | c_static_call'''
    global active_lang,INSIDE_FUNC,defined_ids
    if not '.' in t[1] and not '[' in t[1] and not('(') in t[1]: #nombre de variable. Comprobar que existe
        if not t[1] in defined_ids:
            if active_lang in ['python','cython','js']:
                if INSIDE_FUNC==0:
                    if t[1][0]!='$': #No protestamos por un MACROID
                        raise Exception('Error: El identificador "%s" se usa sin haberse definido'%t[1])  
            else:
                if t[1][0]!='$': #No protestamos por un MACROID
                    if active_lang not in ['csharp','c++','java']:#Permitimos esto en C# para usar dynamic y linq
                        raise Exception('Error: El identificador "%s" se usa sin haberse definido'%t[1])        
    t[0]=t[1]


def p_return_st(t): #jsp
    '''return_st : RETURN ret_item'''
    global INSIDE_FUNC,IN_MACRODEF,active_lang
    if INSIDE_FUNC==0 and IN_MACRODEF==0:
        raise Exception('Error: Sentencia "return" fuera de una definicion de funcion')
    if active_lang in ['python','cython']:
        if type(t[2])==type([]):
            #t[0]=[name,tmp]
            t[0]=t[2][1] + '\n'
            t[0]+=t[1] + ' ' + t[2][0] + '\n'
        else:
            t[0]=t[1] + ' ' + t[2]
    elif active_lang=='c++':
        t[0]=cpp_builder.process_return(t[2])
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_return(t[2])
    elif active_lang=='java':
        t[0]=java_builder.process_return(t[2])
    else:
        t[0]=js_builder.process_return(t[2])

def p_ret_item(t):
    '''ret_item : condic_expr
    | anonym_st
    | empty'''
    t[0]=t[1]


def p_yield_st(t): #jsp
    '''yield_st : YIELD condic_expr'''
    global INSIDE_FUNC,active_lang,js_builder,JS_GENERATOR
    if INSIDE_FUNC==0:
        raise Exception('Error: Sentencia "yield" fuera de una definicion de funcion')
    if active_lang=='js':
        t[0]=js_builder.process_yield(t[2]);
        #poner a 1 el flag de generador
        JS_GENERATOR=1
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_yield(t[2]);
    elif active_lang=='java':
        t[0]=java_builder.process_yield(t[2]);
    else:
        t[0]=t[1] + ' ' + t[2]

def p_incr_st(t): #Cambiar por path_elems_list cuando funcione bien
    '''incr_st : path_elems_list INCR
       | c_pointer_st INCR
       | c_address INCR
       | INCR path_elems_list
       | INCR c_pointer_st
       | INCR c_address'''
    global active_lang,INSIDE_FUNC,js_builder, __strict_mode
    if active_lang in ['python','cython']:
        if t[1] in ['++', '--'] and __strict_mode==1 : raise Exception("Error: en Python no se admite el operador incremento prefijo")
        if t[2]=='++':
            t[0]=t[1] + '+=1'
        else:
            t[0]=t[1] + '-=1'
    elif active_lang=='js':
        t[0]=js_builder.process_incr(t[1],t[2]);
    elif active_lang=='c++':
        t[0]=cpp_builder.process_incr(t[1],t[2]);
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_incr(t[1],t[2]);
    elif active_lang=='java':
        t[0]=java_builder.process_incr(t[1],t[2]);
    else:
        t[0]=t[1] + t[2] 
        


def p_try_st(t): #revisar
    '''try_st : TRY order_list CATCH order_list FINALLY order_list END
       | TRY order_list CATCH order_list END'''
    global active_lang,indent,js_builder,csharp_builder,cpp_builder
    #print t[2],t[1]
    if active_lang in ['python','cython']:
        #Actualizar indent
        indent+='    '
        t[0]='\n' + t[1] + ' : \n'
        for it in t[2].split('\n'):
            t[0]+=indent + it + '\n'
        t[0]+='\n\n'
        #Actualizar indent(quitar 4 espacios)
        indent=indent[-4]
        indent+='    '
        t[0]+='\nexcept Exception as exception: \n'
        for it in t[4].split('\n'):
            t[0]+=indent + it + '\n'
        t[0]+='\n\n'
        #Actualizar indent(quitar 4 espacios)
        indent=indent[-4]
        if len(t)==8:
            #print 'Escribiendo el finally'
            indent+='    '
            t[0]+='\n' + t[5] + ' : \n'
            for it in t[6].split('\n'):
                t[0]+=indent + it + '\n'
            t[0]+='\n\n'
            #Actualizar indent(quitar 4 espacios)
            indent=indent[-4]
    elif active_lang=='js':
        _finally=''
        if len(t)==8: _finally=t[6]
        t[0]=js_builder.process_trycatch(t[2],t[4],_finally) + '\n\n'
    elif active_lang=='csharp':
        _finally=''
        if len(t)==8: _finally=t[6]
        t[0]=csharp_builder.process_trycatch(t[2],t[4],_finally) + '\n\n'
    elif active_lang=='java':
        _finally=''
        if len(t)==8: _finally=t[6]
        t[0]=java_builder.process_trycatch(t[2],t[4],_finally) + '\n\n'
    elif active_lang=='c++':
        _finally=''
        if len(t)==8: _finally=t[6]
        t[0]=cpp_builder.process_trycatch(t[2],t[4],_finally) + '\n\n'
    else: #C#
        pass



def p_assert_st(t): #python,js,c#
    '''assert_st : ASSERT condic_expr'''
    global active_lang,indent,js_builder,csharp_builder
    if active_lang in ['python','cython']:
        t[0]='if not ' + t[2] + ':\n'
        t[0]+= indent + 'raise Exception("""assertion error: \'%s\' is false"""'%t[2] + ')\n'
    elif active_lang=='js':
        t[0]=js_builder.process_assert(t[2])
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_assert(t[2])
    elif active_lang=='csharp':
        t[0]=java_builder.process_assert(t[2])
    elif active_lang=='c++':
        t[0]=cpp_builder.process_assert(t[2])
    else:#C#
        pass


def p_raise_st(t): #python,js,c#
    '''raise_st : RAISE expr'''
    global active_lang,indent,js_builder,csharp_builder
    if active_lang in ['python','cython']:
        t[0]='raise Exception(' + t[2] + ')\n'
    elif active_lang=='js':
        t[0]=js_builder.process_raise(t[2])
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_raise(t[2])
    elif active_lang=='java':
        t[0]=java_builder.process_raise(t[2])
    elif active_lang=='c++':
        t[0]=cpp_builder.process_raise(t[2])
    else:#C#
        pass



def p_if_st(t): #jsp,c++,csharp
    '''if_st : IF condic_expr THEN order_list END
    | IF condic_expr THEN order_list ELSE order_list END'''
    global active_lang,indent
    if active_lang in ['python','cython']:
        if len(t)==6: #Ojo, terminar esto y controlar indent!!
            t[0]='\n' + t[1] + ' ' + t[2] + ' :\n'
            #Actualizar indent
            indent+='    '
            t[0]='\n' + t[1] + ' ' + t[2] + ' : \n'
            for it in t[4].split('\n'):
                t[0]+=indent + it + '\n'
            t[0]+='\n\n'
            #Actualizar indent(quitar 4 espacios)
            indent=indent[-4]
        else:
            t[0]='\n' + t[1] + ' ' + t[2] + ' :\n'
            #Actualizar indent
            indent+='    '
            t[0]='\n' + t[1] + ' ' + t[2] + ' : \n'
            for it in t[4].split('\n'):
                t[0]+=indent + it + '\n'
            t[0]+='else:\n'
            for it in t[6].split('\n'):
                t[0]+=indent + it + '\n'
            #Actualizar indent(quitar 4 espacios)
            indent=indent[-4]
            t[0]+='\n\n'
    else:
        if len(t)==6:
            if active_lang=='c++':
                t[0]= cpp_builder.process_if(t[2],t[4])
            elif active_lang=='csharp':
                t[0]= csharp_builder.process_if(t[2],t[4])
            elif active_lang=='java':
                t[0]= java_builder.process_if(t[2],t[4])
            else:
                t[0]= js_builder.process_if(t[2],t[4])
        else:
            if active_lang=='c++':
                t[0]= cpp_builder.process_if(t[2],t[4],t[6])
            elif active_lang=='csharp':
                t[0]= csharp_builder.process_if(t[2],t[4],t[6])
            elif active_lang=='java':
                t[0]= java_builder.process_if(t[2],t[4],t[6])
            else:
                t[0]= js_builder.process_if(t[2],t[4],t[6])


def p_cond_st(t): #python,jsp,c++,csharp
    '''cond_st : COND expr case_list ELSE DO order_list END'''
    global active_lang,indent,cnd_name,cnd_counter,condstack,csharp_builder,cpp_builder,js_builder
    #print 'valor de la pila: %s' %condstack.toString()
    if active_lang in ['python','cython']:
        #print 'en cond_st'
        #print 'cnd_counter: %s' % cnd_counter
        #name=condstack.pop()
        t[3]=[el.replace('%%cond%%','cond'+ str(cnd_counter)) for el in t[3]]
        name=t[3][0]
        #print 'valor de t[3]: %s' % t[3]
        cnd_counter+=1
        indent+='    '
        t[0]=''
        t[0]+= name + '= ' + t[2] + '\n'
        #Quitar los dos primeros caracteres
        t[3]=t[3][1][2:]
        t[0]+=t[3] + '\n'
        t[0]+='else:\n'
        for it in t[6].split('\n'):
            t[0] += indent + it + '\n' 
        #cnd_counter+=1#Recuperar
        #t[0]=[name,t[0]]
        #condstack.push(name)
        #print condstack.toString()
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_cond(t,cnd_counter)
        cnd_counter+=1
    elif active_lang=='java':
        t[0]=java_builder.process_cond(t,cnd_counter)
        cnd_counter+=1
    elif active_lang=='c++':
        t[0]=cpp_builder.process_cond(t,cnd_counter)
        cnd_counter+=1
    elif active_lang=='js':
        t[0]=js_builder.process_cond(t,cnd_counter)
        cnd_counter+=1
    else:#????idem para java
        t[0]= '\nswitch(' + t[2] + ')\n{\n' +  t[3]  + '\ndefault:\n{\n' + t[6] + '\nbreak;\n}\n}\n'

def p_case_list(t): #Cambiar
    '''case_list : CASE relop_plus expr DO order_list
    | CASE relop_plus expr DO order_list case_list'''
    global active_lang,indent,cnd_name,cnd_counter,condstack
#    print 'en case_list'
#    print 'len(t): %s' % len(t)
#    print 'cnd_counter: %s' % cnd_counter
#    print [el for el in t] 
    name='%%cond%%' #cnd_name+str(cnd_counter)
    #cnd_counter+=1
    #print "valor de t[2]:%s,%s" % (t[2],repr(t[2]))
    if active_lang in ['python','cython']:
        if len(t)==6:
            indent+='    '
            t[0]=''
            if t[2].strip() in ['match','not match']:
                if 'not' in t[2]:
                    t[0]='elif not re.search(' + t[3] + ',' + name + ',):\n'
                else:
                    t[0]='elif re.search(' + t[3] + ',' + name + ',):\n'
            elif t[2].strip()=='is':
                if not t[3] in __typedefs: raise Exception('Error: "%s" no es un tipo definido'%t[3])
                if type(__typedefs[t[3]][1])==type([]):
                    t[0]='elif python_runtime.listMatchType(' + name + ',' + __typedefs[t[3]][1] + ',' + str( __typedefs[t[3]][0]) +  ',__typedefs):\n'
                else:
                    t[0]='elif python_runtime.listMatchType(' + name + ",'" + __typedefs[t[3]][1] + "'," + str( __typedefs[t[3]][0]) +  ',__typedefs):\n'
            else:
                t[0]+='elif ' + name + t[2] + ' ' + t[3] + ':\n'
            for it in t[5].split('\n'):
                t[0]+= indent + it + '\n'
            indent=indent[-4]
            #Hacemos esto SOLO la primera vez!!!
            #condstack.push(name)
            #cnd_counter+=1##REcuperar
        else:
            indent+='    '
            t[0]=''
            if t[2].strip() in ['match','not match']:
                if 'not' in t[2]:
                    t[0]='elif not re.search(' + t[3] + ',' + name + ',):\n'
                else:
                    t[0]='elif re.search(' + t[3] + ',' + name + ',):\n'
            elif t[2].strip()=='is':
                if not t[3] in __typedefs: raise Exception('Error: "%s" no es un tipo definido'%t[3])
                if type(__typedefs[t[3]][1])==type([]):
                    t[0]='elif python_runtime.listMatchType(' + name + ',' + __typedefs[t[3]][1] + ',' + str( __typedefs[t[3]][0]) +  ',__typedefs):\n'
                else:
                    t[0]='elif python_runtime.listMatchType(' + name + ",'" + __typedefs[t[3]][1] + "'," + str( __typedefs[t[3]][0]) +  ',__typedefs):\n'
            else:
                t[0]+='elif ' + t[6][0] + t[2] + ' ' + t[3] + ':\n'
            for it in t[5].split('\n'):
                t[0]+= indent + it + '\n'
            t[0]+=t[6][1]
            indent=indent[-4]
        #condstack.push(name)
        t[0]=[name,t[0]]
    elif active_lang=='csharp':
        #print 'len(t): %s' % len(t)
        #print [el for el in t]
        if len(t)==6:
            t[0]=csharp_builder.process_caselist(cnd_counter,t[2],t[3],t[5])
        else:
            #print 'Yendo por el else con t6: %s' % t[6]
            t[0]=csharp_builder.process_caselist(cnd_counter,t[2],t[3],t[5],t[6])
    elif active_lang=='java':
        #print 'len(t): %s' % len(t)
        #print [el for el in t]
        if len(t)==6:
            t[0]=java_builder.process_caselist(cnd_counter,t[2],t[3],t[5])
        else:
            #print 'Yendo por el else con t6: %s' % t[6]
            t[0]=java_builder.process_caselist(cnd_counter,t[2],t[3],t[5],t[6])
    elif active_lang=='c++':
        #print 'len(t): %s' % len(t)
        #print [el for el in t]
        if len(t)==6:
            t[0]=cpp_builder.process_caselist(cnd_counter,t[2],t[3],t[5])
        else:
            #print 'Yendo por el else con t6: %s' % t[6]
            t[0]=cpp_builder.process_caselist(cnd_counter,t[2],t[3],t[5],t[6])
    elif active_lang=='js':
        if len(t)==6:
            t[0]=js_builder.process_caselist(cnd_counter,t[2],t[3],t[5])
        else:
            t[0]=js_builder.process_caselist(cnd_counter,t[2],t[3],t[5],t[6])

def p_while_st(t): #jsp,c++.csharp
    '''while_st : start_while condic_expr DO order_list END end_loop'''
    global active_lang,indent
    #print t[2],t[1]
    if active_lang in ['python','cython']:
        #Actualizar indent
        indent+='    '
        t[0]='\n' + t[1] + ' ' + t[2] + ' : \n'
        for it in t[4].split('\n'):
            t[0]+=indent + it + '\n'
        t[0]+='\n'
        #Actualizar indent(quitar 4 espacios)
        indent=indent[-4]
    else: #C#
        if active_lang=='c++':
            t[0]= cpp_builder.process_while(t[2],t[4])
        elif active_lang=='csharp':
            t[0]= csharp_builder.process_while(t[2],t[4])
        elif active_lang=='java':
            t[0]= java_builder.process_while(t[2],t[4])
        else:
            t[0]= js_builder.process_while(t[2],t[4])

def p_start_while(t):
    '''start_while : WHILE'''
    global INSIDE_LOOP
    INSIDE_LOOP+=1
    t[0]=t[1]

def p_loopwhen_st(t): #jsp,c++,csharp
    '''loopwhen_st : start_loop order_list UNTIL condic_expr END'''
    global active_lang,indent
    if active_lang in ['python','cython']:
        t[0]='while True: \n'
        #Actualizar indent
        indent+='    '
        for it in t[2].split('\n'):
            t[0]+=indent + it + '\n'
        t[0]+=indent + 'if ' + t[4] + ' : break \n'
        t[0]+='\n'
        #Actualizar indent(quitar 4 espacios)
        indent=indent[-4]
    else:
        if active_lang=='c++':
            t[0]= cpp_builder.process_repeat(t[4],t[2])
        elif active_lang=='csharp':
            t[0]= csharp_builder.process_repeat(t[4],t[2])
        elif active_lang=='java':
            t[0]= java_builder.process_repeat(t[4],t[2])
        else:
            t[0]= js_builder.process_repeat(t[4],t[2])

def p_start_loop(t):
    '''start_loop : REPEAT'''
    global INSIDE_LOOP
    INSIDE_LOOP+=1
    t[0]=t[1]

def p_for(t): #jsp,c++,csharp
    '''for_st : start_for ID EQUAL expr COMMA condic_expr COMMA for_option DO order_list END end_loop'''
    global active_lang,indent
    t[2]=t[2].strip('%')
    if active_lang in ['python','cython']:
        t[0]=t[2] + ' = ' + t[4]
        t[0]+='\nwhile ' + t[6] + ' :\n'
        #Actualizar indent
        indent+='    '
        for it in t[10].split('\n'):
            t[0]+=indent + it + '\n'
        t[0]+=indent + t[8]
        t[0]+='\n'
        #Actualizar indent(quitar 4 espacios)
        indent=indent[-4]
        
    else:
        if active_lang=='c++':
            t[0]= cpp_builder.process_for(t[2],t[4],t[6],t[8],t[10])
        elif active_lang=='csharp':
            t[0]= csharp_builder.process_for(t[2],t[4],t[6],t[8],t[10])
        elif active_lang=='java':
            t[0]= java_builder.process_for(t[2],t[4],t[6],t[8],t[10])
        else:
            t[0]= js_builder.process_for(t[2],t[4],t[6],t[8],t[10])

def p_for_option(t):
    '''for_option : incr_st
    | ID EQUAL expr''' 
    if len(t)==4:
        t[0]=t[1]+t[2]+t[3]
    else:
        t[0]=t[1]

def p_start_for(t):#ok
    '''start_for : FOR'''
    global INSIDE_LOOP
    INSIDE_LOOP+=1
    t[0]=t[1]

def p_foreach_st(t): #js,c++,csharp
    '''foreach_st : start_foreach foreach_var IN expr DO order_list END end_loop
    | start_foreach foreach_var IN ID DO order_list END end_loop'''
    global active_lang,indent
    t[2]=t[2].strip('%')
    t[4]=t[4].strip('%')
    if active_lang in ['python','cython']:
        t[0]='for ' + t[2] + ' ' + t[3] + ' ' + t[4] + ': \n'
        #Actualizar indent
        indent+='    '
        for it in t[6].split('\n'):
            t[0]+=indent + it + '\n'
        t[0]+='\n'
        #Actualizar indent(quitar 4 espacios)
        indent=indent[-4]
    else:
        if active_lang=='c++':
            t[0]= cpp_builder.process_foreach(t[2],t[4],t[6])
        elif active_lang=='csharp':
            t[0]= csharp_builder.process_foreach(t[2],t[4],t[6])
        elif active_lang=='java':
            t[0]= java_builder.process_foreach(t[2],t[4],t[6])
        else:
            t[0]= js_builder.process_foreach(t[2],t[4],t[6])

def p_foreach_var(t):
    '''foreach_var : ID
       | ID AS generic'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]= t[3] + ' ' + t[1]

def p_start_foreach(t):#ok
    '''start_foreach : FOREACH'''
    global INSIDE_LOOP
    INSIDE_LOOP+=1
    t[0]=t[1]

def p_break_st(t):#ok
    '''break_st : BREAK'''
    global INSIDE_LOOP
    if INSIDE_LOOP==0: raise Exception('Error: solo se puede usar la sentencia "break" dentro de un bucle')
    t[0]=t[1]

def p_continue_st(t):#ok
    '''continue_st : CONTINUE'''
    global INSIDE_LOOP
    if INSIDE_LOOP==0: raise Exception('Error: solo se puede usar la sentencia "continue" dentro de un bucle')
    t[0]=t[1]

def p_end_loop(t):#ok
    '''end_loop : empty'''
    global INSIDE_LOOP
    INSIDE_LOOP-=1
    if INSIDE_LOOP<0: INSIDE_LOOP=0
    t[0]=t[1]
 
def p_pair(t): #Recuperar si va mal
    '''pair : expr COLON condic_expr'''
    t[0]=t[1] + t[2] + t[3]

def p_pair_list(t): #ok
    '''pair_list : pair COMMA pair_list
    | pair
    | empty'''
    t[0]=t[1] if len(t)==2 else t[1] + t[2] + t[3]

def p_condic_expr(t): #ok
    '''condic_expr : condic_expr OR condic_expr
    | and_exp'''
    global active_lang
    if active_lang in ['python','cython']:
        t[0]=t[1] if len(t)==2 else t[1] + ' ' +  t[2] + ' ' + t[3]
    else:
        t[0]=t[1] if len(t)==2 else t[1] + " || " + t[3]
    #print 't[0] en condic_expr: %s' %t[0]
   
def p_and_exp(t): #ok
    '''and_exp : and_exp AND not_exp
    | not_exp'''
    global active_lang
    if active_lang in ['python','cython']:
        t[0]=t[1] if len(t)==2 else t[1] + ' ' +  t[2] + ' ' + t[3]
    else:
        t[0]=t[1] if len(t)==2 else t[1] + " && " + t[3]
   
def p_not_exp(t): #ok
    '''not_exp : NOT condic_expr
    | bool_exp'''
    global active_lang
    if len(t)==2:
        t[0]=t[1]
    elif len(t)==3:
        if active_lang in ['python','cython']:
            t[0]=t[1]+' ' + t[2]
        else:
            t[0]="!" +t[2]
    else:
        t[0]=t[2]

def p_bool_exp(t): #REVISAR!!!!!!!!!! jsp
    '''bool_exp : expr relop expr
    | LPAREN condic_expr RPAREN
    | MATCH expr IN expr
    | expr'''
    global __type_instances,__typedefs,active_lang,js_builder
    if active_lang=='js':
        t[0]=js_builder.process_boolexp(t)
        #print 't[0] en bool_exp para js: %s' %t[0]
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_boolexp(t)
    elif active_lang=='java':
        t[0]=java_builder.process_boolexp(t)
    elif active_lang=='c++':
        t[0]=cpp_builder.process_boolexp(t)
    elif active_lang in ['python','cython']:
        if len(t)==2:
            t[0]=t[1]
        elif len(t)==4:
            if t[2]==' is ': #match list-type
                #listMatchType(lst,template,kind,__tdefs)
                #print __typedefs
                #print 't[1]: %s' %t[1]
                #print 't[3]: %s' %t[3]
                if not t[3] in __typedefs: raise Exception('Error: "%s" no es un tipo basado en listas definido'%t[3])
                if type(__typedefs[t[3]][1])==type([]):
                    #print 'valor de __typedefs[t[3]][1]: %s' % __typedefs[t[3]][1]
                    #t[0]='python_runtime.listMatchType(' + t[1] + ',' + __typedefs[t[3]][1] + ',' + str( __typedefs[t[3]][0]) +  ',__typedefs)'
                    t[0]='python_runtime.listMatchType(' + t[1] + "," + str(__typedefs[t[3]][1]) + ',' + str( __typedefs[t[3]][0]) +  ',__typedefs)'
                else:
                    t[0]='python_runtime.listMatchType(' + t[1] + ",'" + __typedefs[t[3]][1] + "'," + str( __typedefs[t[3]][0]) +  ',__typedefs)'
            else:
                t[0]=t[1] + t[2] + t[3]
        else:
            t[0]='re.search(' + t[2] + ',' + t[4] + ')'         

def p_relop(t): #ok
    '''relop : EQ
    | GT
    | GE
    | LT
    | LE
    | NE
    | IN
    | IS
    | NOT IN'''
    if len(t)==2:
        t[0]=' ' + t[1] + ' '
    else:
        t[0]=' ' + t[1] + ' '+t[2] + ' '

def p_relop_plus(t): #ok
    '''relop_plus : EQ
    | GT
    | GE
    | LT
    | LE
    | NE
    | IN
    | IS
    | NOT IN
    | MATCH
    | NOT MATCH'''
    if len(t)==2:
        t[0]=' ' + t[1] + ' '
    else:
        t[0]=' ' + t[1] + ' '+t[2] + ' '

def p_binor_st(t):
    '''binor_st : PIPE bo_list PIPE'''
    t[0]=t[2]

def p_bo_list(t): #REVISARLO!!!!!!!
    '''bo_list : path_elems_list BO path_elems_list
    | path_elems_list BO bo_list'''
    t[0]=t[1] + '|' + t[3]

#ESTE CAMBIO DA ERROR en math CON COSAS COMO: _print(a.transform(|(x): math.log(x)|).data);
# def p_bo_list(t):
    # '''bo_list : expr BO expr
    # | expr BO bo_list'''
    # t[0]=t[1] + '|' + t[3]
#quitado de aqui c_pointer_st
def p_expr(t): #COPIA DE SEGURIDAD!!(REVISAR EL CAST!!!!)
    '''expr : expr PLUS termino
    | expr MINUS termino
    | expr COLON COLON termino
    | expr INSERTOR termino
    | expr EXTRACTOR termino
    | MINUS expr %prec UMINUS  
    | PLUS expr %prec UMINUS 
    | termino
    | annotation  
    | binor_st
    | cast_st
    '''
    global active_lang
    #print 'en expr: len(t):%s' % len(t)
    if len(t)==2:
        t[0]=t[1]
    elif len(t)==3: #???????????????????????y el -termino?????????
        t[0]=t[1]+t[2]
        
    else:
        #t[0]=t[1] + t[2] + t[3]#Revisar este cambio!!
        if active_lang in ['python','cython']:
            if t[2]=='+':
                t[0]='python_runtime.doAddition(' + t[1] + ',' + t[3] + ')'
            elif t[2]==':':
                t[0]='python_runtime._append2(' + t[4] + ',' + t[1] + ')'
            else:
                t[0]=t[1] + t[2] + t[3]
        else:
            if t[2]=='+':
                if active_lang=='c++':
                    t[0]=cpp_builder.process_plus(t[1],t[3])
                elif active_lang=='csharp':
                    t[0]=csharp_builder.process_plus(t[1],t[3])
                elif active_lang=='java':
                    t[0]=java_builder.process_plus(t[1],t[3])
                else:
                    t[0]=js_builder.process_plus(t[1],t[3])
            elif t[2]==':':
                if active_lang=='c++':
                    t[0]=cpp_builder.process_tolist(t[1],t[4])
                elif active_lang=='csharp':
                    t[0]=csharp_builder.process_tolist(t[1],t[4])
                elif active_lang=='java':
                    t[0]=java_builder.process_tolist(t[1],t[4])
                else:
                    t[0]=js_builder.process_tolist(t[1],t[4])
            elif t[2] in ['<<','>>']:
                if active_lang=='c++':
                    t[0]=cpp_builder.process_insertor(t[1],t[2],t[3])
                elif active_lang=='csharp':
                    t[0]=csharp_builder.process_insertor(t[1],t[2],t[3])
                elif active_lang=='java':
                    t[0]=java_builder.process_insertor(t[1],t[2],t[3])
                else:
                    t[0]=js_builder.process_insertor(t[1],t[2],t[3])
            else:
                t[0]=t[1] + t[2] + t[3]
    #print 't[0] en expr: %s' % t[0]

def p_expr_list(t): #jsp
    '''expr_list : expr
    | expr COMMA expr_list'''
    global aux_string,outstring,active_lang
    #print 'EN EXPR_LIST CON t[1]: %s' % t[1]
    if active_lang in ['python','cython']:
        if len(t)==2:
            t[0]=t[1]
        else:
            if t[1]:
                if not t[1]: t[1]=''
                if not t[2]: t[2]=''
                if not t[3]: t[3]=''
                t[0]=t[1] + t[2] + t[3]
            else:
                t[0]=''
        #print 't[0] en expr_list: %s' % t[0]
    else:
        if len(t)==2:
            t[0]=t[1]
        else:
            if not t[1]: t[1]=''
            if not t[2]: t[2]=''
            if not t[3]: t[3]=''
            t[0]=t[1] + t[2] + t[3]
        if aux_string!='': #REVISAR ESTO!
            outstring+=aux_string
            aux_string=''


def p_path_elems_list(t): #ok
    '''path_elems_list : path_elem path_elem_sep path_elems_list
    | path_elem'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2] + t[3]
    #print 'en path_elems_list: %s' %t[0]

#No se puede poner sequence aqui porque nos metemos en recursividad no permitida!!!!!

#Cambio para poder tener resolutor de ambito
# def p_path_elem_sep(t):
    # '''path_elem_sep : DOT 
    # | COLON COLON'''
    # if len(t)==2:
        # t[0]=t[1]
    # else:
        # t[0]=t[1] + t[2]

def p_path_elem_sep(t):
    '''path_elem_sep : DOT
    | DOTDOT'''
    global active_lang
    if t[1]=='.':
        t[0]=t[1]
    else:
        if active_lang in ['python','cython']:
            t[0]='.'
        else:
            t[0]='::'


def p_path_elem(t): #jsp #Se ha puesto string y this_st aqui, REVISARLOOOO!
    '''path_elem : idchain
    | accesors
    | funcall
    | this_st
    | idchain accesors
    | funcall accesors'''
    if len(t)==3:
        t[0]=t[1] + t[2]
    else:
        t[0]=t[1]  
    #print 'en path_elem: %s' % t[0]

def p_c_static_call(t):
    '''c_static_call : PIPE PIPE static_list PIPE PIPE'''
    t[0]=t[3]

def p_static_list(t): #ok
    '''static_list : static_elem COLON COLON static_list
    | static_elem'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2] + t[3] + t[4]

def p_static_elem(t):
    '''static_elem : generic
    | funcall'''
    t[0]=t[1]


def p_path_elems_list_list(t): #ok
    '''path_elems_list_list : path_elems_list COMMA path_elems_list_list
    | path_elems_list'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2] + t[3]


def p_expr_list_item(t): #ok?
    '''expr_list_item : sequence
    | array
    | dict
    | lambda_st
    | functional_st
    | new_st
    | range_st
    | next_expr
    | send_expr
    | quote_st
    | macroid_st
    | select_files_st
    '''
    t[0]=t[1]
    #print 't[0] en expr_list_item: %s'% t[0]


def p_range_st(t): 
    '''range_st : expr TO expr
    | expr TO expr IN expr'''
    global active_lang
    #print 'en range t[1]: %s' % t[1]
    #print 'en range t[3]: %s' % t[3]
    if active_lang=='csharp':
        if len(t)==4:
            t[0]=csharp_builder.process_range(t[1],t[3],"1")
        else:
            t[0]=csharp_builder.process_range(t[1],t[3],t[5])
    elif active_lang=='java':
        if len(t)==4:
            t[0]=java_builder.process_range(t[1],t[3],"1")
        else:
            t[0]=java_builder.process_range(t[1],t[3],t[5])
    elif active_lang=='c++':
        if len(t)==4:
            raise Exception('Error: C++ es un lenguaje fuertemente tipoado y se debe indicar el incremento de un rango')
        else:
            t[0]=cpp_builder.process_range(t[1],t[3],t[5])
    elif active_lang in ['python','cython']:
        if len(t)==4:
            t[0]='python_runtime.genRange(' + t[1] + ',' + t[3] + ')'
        else:
            t[0]='python_runtime.genRange(' + t[1] + ',' + t[3] + ',' + t[5] +  ')'
    else:
        if len(t)==4:
            t[0]=js_builder.process_range(t[1],t[3],"1")
        else:
            t[0]=js_builder.process_range(t[1],t[3],t[5])


def p_this_st(t): #ok
    '''this_st : THIS'''
    global __inclass,active_lang
    if __inclass==0:
        raise Exception('Error: no se puede usar la palabra clave "this" fuera de una definicion de clase')
    if active_lang in ['python','cython']:
        t[0]='self'
    else: #En el resto de lenguajes es "this"
        t[0]=t[1]


def p_termino(t): #COPIA DE SEGURIDAD!!
    '''termino : termino TIMES pot_factor
    | termino DIV pot_factor
    | pot_factor'''
    t[0]=t[1] if len(t)==2 else t[1] + t[2] + t[3]
      

def p_pot_factor(t): #Revisar para usar Math.pow, que tiene mucho mejor renidimiento
    '''pot_factor : factor EXP factor
    | factor'''
    t[0]=t[1] if len(t)==2 else t[1] + t[2] + t[3]
    

def p_factor(t): #En revision jsp
    '''factor : LPAREN expr RPAREN  
    | NUMBER
    | NULL
    | expr_list_item path_elems_list
    | expr_list_item DOT funcall
    | path_elems_list
    | expr_list_item
    | ifelse_st
    | format_st
    | serialize_st
    | deserialize_st
    | TRUE
    | FALSE
    | STRING
    | c_address
    | c_pointer_st
    | c_static_call
    | funcall_generic
    '''
    global active_lang
    #print 'EN FACTOR CON T[1]:%s y len(t):%s' % (t[1],len(t))
    if len(t)==2:
        if t[1] in ['null','None']:
            #print 'PROCESANDO NULL!!'
            t[0]='None' if active_lang in ['python','cython'] else 'null'
        elif t[1]=='true':
            t[0]='True' if active_lang in ['python','cython'] else 'true'
        elif t[1]=='false':
            t[0]='False' if active_lang in ['python','cython'] else 'false'
        else:
            t[0]=t[1]
    elif len(t)==3:
        t[0]=t[1] + t[2]
    else:#(expr)
        if t[2]==None: t[2]=''
        if t[3]==None: t[3]=''
        t[0]=t[1] + t[2] + t[3]
    #print 't[0] en factor: %s' %t[0]


def p_funcall(t): #ok
    '''funcall : path_elems_list LPAREN funcall_chain RPAREN
    | path_elems_list LPAREN RPAREN'''
    global indent
    if len(t)==5:
        t[0]=t[1]+t[2]+t[3] + t[4]
    else:
        t[0]=t[1] + '()'
    # print 'en funcall con t[0]:%s' % t[0]


def p_funcall_generic(t): #Esto habra que separarlo segun lenguajes!!!!
    '''funcall_generic : PIPE generic LPAREN funcall_chain RPAREN PIPE
    | PIPE generic LPAREN RPAREN PIPE'''
    global indent
    if len(t)==7:
        t[0]=t[2]+t[3]+t[4] + t[5]
    else:
        t[0]=t[2] + '()'
    #print 'en funcall_generic con t[0]:%s' % t[0]

def p_assign_generic(t):
    '''assign_generic : assignable ARROW funcall_generic'''
    t[0]=t[1] + '=' + t[3]


def p_funcall_chain(t): #ok
    '''funcall_chain : expr_list
    | expr_list optional_args
    | optional_args'''
    if len(t)==2:
        #print 't[1] en funcall_chain:%s' % t[1]
        t[0]=t[1]
    else:
        #print 't[2] en funcall_chain:%s' % t[2]
        t[0]=t[1] + ',' + t[2]
        #t[0]=t[1] + t[2]
    #print 't[0] en funcall_chain: %s' % t[0]

def p_cast_st(t): #jsp
    '''cast_st : PIPE generic PIPE expr'''
    global active_lang,__strict_mode
    if active_lang in ['python','js'] and __strict_mode==1:
        raise Exception('Error: %s es un lenguaje sin declaracion explicita de tipos. No acepta conversiones axplicitas tampoco.'%active_lang)
    if active_lang=='cython':
        t[0]='<' + t[2] + '>' + t[4]
    else:
        t[0]='(' + t[2] + ')' + t[4]
    


def p_sequence(t): #jsp?
    '''sequence : LBRACK RBRACK
    | LBRACK RBRACK AS generic
    | LBRACK expr_list RBRACK
    | LBRACK expr_list COMMA RBRACK
    | LBRACK expr_list RBRACK AS generic'''
    global l_name,l_counter,aux_string,active_lang,__strict_mode
    if active_lang in ['python','js','cython']:
        if len(t)==3:
            t[0]=t[1] + t[2]
        elif len(t)==4:
            t[0]=t[1] + t[2] + t[3]
        else:
            if __strict_mode==1:
                raise Exception('Error: %s no admite declaracion explicita de tipos'%active_lang)
    else:
        #elems=None
        elems=' '
        if active_lang=='c++':
            if len(t)not in [5,6] and __strict_mode==1: raise Exception('Error: en C++ se debe especificar el tipo de los elementos de una lista')
            if len(t)==3:
                t[0]=cpp_builder.process_sequence(']','void*')
            elif len(t)==4:
                elems=findElements(t[2])
                t[0]=cpp_builder.process_sequence(elems,'void*')
            elif len(t)==5:
                t[0]=cpp_builder.process_sequence(']',t[4])
            else:
                elems=findElements(t[2])
                t[0]=cpp_builder.process_sequence(elems,t[5])
        elif active_lang=='csharp': #Esto parece estar mal: REVISARLO
            if len(t)not in [5,6] and __strict_mode==1: raise Exception('Error: en C# se debe especificar el tipo de los elementos de una lista')
            elif len(t) in [5,6]:
                typ=t[4] if len(t)==5 else t[5]
            else:
                typ=''
            #print 'typ en sequence: %s'% repr(typ)
            t[0]=csharp_builder.process_sequence(elems,typ)
        elif active_lang=='java':
            if len(t)not in [5,6] and __strict_mode==1: raise Exception('Error: en Java se debe especificar el tipo de los elementos de una lista')
            if len(t)==3:
                t[0]=java_builder.process_sequence(']','Object')
            elif len(t)==4:
                elems=findElements(t[2])
                t[0]=java_builder.process_sequence(elems,'Object')
            elif len(t)==5:
                #print 'Por lista vacia con tipo: %s' % t[4]
                t[0]=java_builder.process_sequence(']',t[4])
            else:
                elems=findElements(t[2])
                t[0]=java_builder.process_sequence(elems,t[5])
        else:
            t[0]='' #implementar para java y c#

def p_array(t): #Revisar
    '''array : LCURLY expr_list RCURLY AS generic
    | LCURLY expr_list RCURLY'''
    global a_counter,a_name,aux_string,active_lang,__strict_mode
    if active_lang in ['python','js','cython'] and __strict_mode==1:
        raise Exception('Error: En %s no existe el tipo array, utilizar listas.'%active_lang)
    elems=findElements(t[2])
    if active_lang=='c++':
        t[0]=cpp_builder.process_array(elems,t[5])
    elif active_lang=='csharp':
        if len(t)==4:
            t[0]=csharp_builder.process_array(elems,'')
        else:
            t[0]=csharp_builder.process_array(elems,t[5])
    elif active_lang=='java':
        if len(t)==4:
            t[0]=java_builder.process_array(elems,'')
        else:
            t[0]=java_builder.process_array(elems,t[5])

def p_dict(t): #REVISAR!!!
    '''dict : LCURLY pair_list RCURLY
    | LCURLY pair_list RCURLY AS generic
    | LCURLY RCURLY
    | LCURLY RCURLY AS generic'''
    global d_name,d_counter,aux_string,active_lang,__strict_mode
    if active_lang in ['python','js','cython']:
        if len(t)==3:
            t[0]='{}'
        else:
            t[0]=t[1] + t[2] + t[3]
    else: 
        if len(t) in [3,4] and __strict_mode==1: raise Exception('Error: en %s no se permite definir diccionarios sin tipo'%active_lang)
        elems=findElements(t[2])
        #print 'elems: %s' % elems
        typ=''
        if len(t)==5:
            typ=t[4]
        elif len(t)==6:
            typ=t[5]
        if active_lang=='c++':
            if len(t)not in [5,6] and __strict_mode==1: raise Exception('Error: en C++ se debe especificar el tipo de los elementos de un diccionario')
            t[0]=cpp_builder.process_dict(elems,typ)   
        elif active_lang=='csharp':
            t[0]=csharp_builder.process_dict(elems,typ) 
        elif active_lang=='java':
            t[0]=java_builder.process_dict(elems,typ) 
        else: #ignoramos resto por ahora
            pass


def p_accesors(t):#ok,jsp,c++
    '''
    accesors : LBRACK expr RBRACK accesors
    | LBRACK expr RBRACK
    '''
    #print 'Yendo por accesors'
    t[0]=t[1] + t[2] + t[3] if len(t)==4 else t[1]+t[2]+t[3]+t[4]


def p_anonym_st(t): #jsp,c++,csharp
    '''anonym_st : set_an_flags FUNCTION LPAREN funcargs RPAREN COLON order_list END reset_an_flags
    | annotation_list set_an_flags FUNCTION LPAREN funcargs RPAREN COLON order_list END reset_an_flags'''
    global active_lang,indent,fun_counter,aux_string
    #print 'En anonym_st: %s'%active_lang
    if active_lang in ['python','cython'] :
        name='function' + str(fun_counter)
        #tmp='def ' + name  + '(' + t[4] + ') :\n'
        tmp=''
        #Actualizar indent
        indent+='    '
        #for it in t[6].split('\n'):
        if len(t)==10:
            tmp='def ' + name  + '(' + t[4] + ') :\n'
            for it in t[7].split('\n'):
                tmp+=indent + it + '\n'
        else:
            tmp= t[1] + '\ndef ' + name  + '(' + t[5] + ') :\n'
            for it in t[8].split('\n'):
                tmp+=indent + it + '\n'
        tmp+='\n\n'
        #Actualizar indent(quitar 4 espacios)
        indent=indent[-4]
        #Actualizar fun_counter
        fun_counter+=1
        #aux_string+=tmp
        #t[0]=name
        t[0]=[name,tmp]
    else:
        if active_lang=='c++':
            t[0]=cpp_builder.process_fundef_anonym(t[4],t[7])
        elif active_lang=='csharp':
            t[0]=csharp_builder.process_fundef_anonym(t[4],t[7])
        elif active_lang=='java':
            t[0]=java_builder.process_fundef_anonym(t[4],t[7])
        else:
            if len(t)==10:
                t[0]=js_builder.process_fundef_anonym(t[4],t[7])
            else:
                t[0]=js_builder.process_fundef_anonym(t[5],t[8])

#Esto es un muy buen truco para establecer/restablecer globales
def p_set_an_flags(t): #ok
    '''set_an_flags : empty'''
    global INSIDE_FUNC
    #if INSIDE_FUNC==1:
    #    raise Exception("Error: No se permiten definiciones anidadas de funciones")
    INSIDE_FUNC+=1
    t[0]=''

def p_reset_an_flags(t): #ok
    '''reset_an_flags : empty'''
    global INSIDE_FUNC
    INSIDE_FUNC-=1
    t[0]=''

def p_lambda_st(t): #jsp,c++,csharp
    '''lambda_st : PIPE  LPAREN funcargs2 RPAREN  COLON condic_expr PIPE'''
    global active_lang,indent,fun_counter
    #print 'valor de funcargs en lambda: %s' % t[3]
    if active_lang in ['python','cython']:
        t[0]='lambda ' + t[3] + ': ' +t[6].strip()
        #print 't[3] en lambda: %s' % t[3]
    elif active_lang=='c++':
        #t[0]=t[1] + t[2] + t[3] + ' => ' + t[5].strip(';')
        t[0]=cpp_builder.process_fundef_anonym2(t[3],t[6])
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_fundef_anonym2(t[3],t[6])
    elif active_lang=='java':
        t[0]=java_builder.process_fundef_anonym2(t[3],t[6])
    else:
        #t[0]=t[1] + t[2] + t[3] + ' => ' + t[5].strip(';')
        t[0]=js_builder.process_fundef_anonym2(t[3],t[6])

def p_functional_fun(t): #ok
    '''functional_fun : lambda_st
    | ID'''
    t[0]=t[1].strip('%')

def p_filter_st(t): #js,c++,csharp
    '''filter_st : FILTER functional_fun IN expr_list'''
    global l_name,l_counter,aux_string,active_lang
    if active_lang in ['python','cython']:
        if '{{{{____}}}}' in t[4]:
            t[4]='+'.join(t[4].split('{{{{____}}}}'))
        t[0]='filter(' + t[2] + ',list(itertools.chain(' + t[4] + ')))'
    else: #Revisar para idlist!!
        if active_lang=='c++':
            t[0]=cpp_builder.process_filter(t[2],t[4])
        elif active_lang=='csharp':
            t[0]=csharp_builder.process_filter(t[2],t[4])
        elif active_lang=='java':
            t[0]=java_builder.process_filter(t[2],t[4])
        else:
            t[0]=js_builder.process_filter(t[2],t[4])

def p_map_st(t): #jsp,c++,csharp
    '''map_st : MAP functional_fun IN fun_item_list'''
    global l_name,l_counter,active_lang
    #print 't[4] en map:%s' % t[4]
    if active_lang in ['python','cython']:
        if '{{{{____}}}}' in t[4]:
            t[4]='+'.join(t[4].split('{{{{____}}}}'))
        t[0]='list(itertools.imap(' + t[2] + ',list(itertools.chain(' + t[4] + '))))'
    else:
        if active_lang=='c++':
            t[0]=cpp_builder.process_map(t[2],t[4])
        elif active_lang=='csharp':
            t[0]=csharp_builder.process_map(t[2],t[4])
        elif active_lang=='java':
            t[0]=java_builder.process_map(t[2],t[4])
        else:
            t[0]=js_builder.process_map(t[2],t[4])

def p_reduce_st(t): #js,c++,csharp
    '''reduce_st : REDUCE functional_fun IN fun_item_list
    | REDUCE functional_fun IN fun_item_list WITH expr'''
    global l_name,l_counter,aux_string,active_lang
    if active_lang in ['python','cython']:
        if '{{{{____}}}}' in t[4]:
            t[4]='+'.join(t[4].split('{{{{____}}}}'))
        if len(t)==5:
            t[0]='reduce(' + t[2] + ',itertools.chain(' + t[4] + '))'
            #t[0]='list(ireduce(' + t[2] + ',itertools.chain(' + t[4] + ')))'
        else:
            t[0]='reduce(' + t[2] + ',itertools.chain(' + t[4] + '),' + t[6] + ')'
            #t[0]='list(ireduce(' + t[2] + ',itertools.chain(' + t[4] + ')))'
    else: #Resto
        if active_lang=='c++':
            if len(t)==5:
                t[0]=cpp_builder.process_reduce(t[2],t[4])  
            else:
                t[0]=cpp_builder.process_reduce(t[2],t[4],t[6])
        elif active_lang=='csharp':
            if len(t)==5:
                t[0]=csharp_builder.process_reduce(t[2],t[4])  
            else:
                t[0]=csharp_builder.process_reduce(t[2],t[4],t[6])
        elif active_lang=='java':
            if len(t)==5:
                t[0]=java_builder.process_reduce(t[2],t[4],'0')  
            else:
                t[0]=java_builder.process_reduce(t[2],t[4],t[6])
        else:
            if len(t)==5:
                t[0]=js_builder.process_reduce(t[2],t[4])  
            else:
                t[0]=js_builder.process_reduce(t[2],t[4],t[6])
    
def p_slice_st(t): #Cambiar
    '''
    slice_st : LBRACK expr COLON expr RBRACK IN fun_item_list'''
    global l_name,l_counter,aux_string,active_lang
    if active_lang in ['python','cython']:
        if '{{{{____}}}}' in t[7]:
            t[7]='+'.join(t[7].split('{{{{____}}}}'))
        t[0]='list(itertools.chain(' + t[7] + '))[ ' + (t[2] if t[2]!='null' else '') + ': ' + (t[4] if t[4]!='null' else '') +  ']\n'
    else: #Revisar para idlist!!
        if active_lang=='c++':
             t[0]=cpp_builder.process_slice(t[2],t[4],t[7])
        elif active_lang=='csharp':
             t[0]=csharp_builder.process_slice(t[2],t[4],t[7])
        elif active_lang=='java':
             t[0]=java_builder.process_slice(t[2],t[4],t[7])
        else:
             t[0]=js_builder.process_slice(t[2],t[4],t[7])

def p_group_st(t): #Revisar para resto de lenguajes
    '''group_st : GROUPBY functional_fun IN fun_item_list'''
    global g_name,g_counter,aux_string,active_lang,__strict_mode
    if active_lang in ['python','cython']:
        t[0]='python_runtime.doGroup(' + '+'.join(t[4].split('{{{{____}}}}')) + ',' + t[2] + ')'
    elif active_lang=='js':
        t[0]=js_builder.process_groupby(t)
    else: #Resto
        if __strict_mode==1:
            raise Exception('Error: "groupby" solo esta disponible en Python y JavaScript')
        else:
            t[0]=''


def p_fun_list_item(t):
    '''fun_list_item : expr
    | path_elems_list'''
    t[0]=t[1]

def p_fun_item_list(t):
    '''fun_item_list : fun_list_item COMMA fun_item_list
    | fun_list_item'''
    if len(t)==2:
        t[0]=t[1]
    else:
        if active_lang in ['python','cython']:
            t[0]=t[1] + '{{{{____}}}}' + t[3]
        else:
            t[0] = t[1] + t[2] + t[3]

def p_order_st(t): #ok
    '''order_st :  ORDER fun_item_list BY functional_fun opt_reverse'''
    global g_name,g_counter,aux_string,active_lang
    #print 'len(t) en order: %s' % len(t)
    if active_lang in ['python','cython']:
        name=g_name + str(g_counter)
        t[0]= ''
        if '{{{{____}}}}' in t[2]:
            t[2]='+'.join(t[2].split('{{{{____}}}}'))
        if t[5]=='reverse':
            t[0]+='python_runtime.doSort(itertools.chain(' + t[2] + '),' + t[4] + ',1)'
        else:
            t[0]+='python_runtime.doSort(itertools.chain(' + t[2] + '),' + t[4] + ')'
    else: #
        if active_lang=='c++':
            if len(t)==7:
                if t[6]=='reverse':
                    t[0]=cpp_builder.process_order(t[3],t[5],1)
                else:
                    t[0]=cpp_builder.process_order(t[3],t[5])
            elif len(t)==6:
                if t[5]=='reverse':
                    t[0]=cpp_builder.process_order(t[2],t[4],1)
                else:
                    t[0]=cpp_builder.process_order(t[2],t[4])
        elif active_lang=='csharp':
            if len(t)==7:
                if t[6]=='reverse':
                    t[0]=csharp_builder.process_order(t[3],t[5],1)
                else:
                    t[0]=csharp_builder.process_order(t[3],t[5])
            elif len(t)==6:
                if t[5]=='reverse':
                    t[0]=csharp_builder.process_order(t[2],t[4],1)
                else:
                    t[0]=csharp_builder.process_order(t[2],t[4])
        elif active_lang=='java':
            if len(t)==7:
                if t[6]=='reverse':
                    t[0]=java_builder.process_order(t[3],t[5],1)
                else:
                    t[0]=java_builder.process_order(t[3],t[5])
            elif len(t)==6:
                if t[5]=='reverse':
                    t[0]=java_builder.process_order(t[2],t[4],1)
                else:
                    t[0]=java_builder.process_order(t[2],t[4])
        else:
            if len(t)==7:
                if t[6]=='reverse':
                    t[0]=js_builder.process_order(t[3],t[5],1)
                else:
                    t[0]=js_builder.process_order(t[3],t[6])
            elif len(t)==6:
                if t[5]=='reverse':
                    t[0]=js_builder.process_order(t[2],t[4],1)
                else:
                    t[0]=js_builder.process_order(t[2],t[4])

def p_opt_reverse(t):
    '''opt_reverse : REVERSE
       | empty'''
    t[0]=t[1]


def p_fsysitem(t):
    '''fsysitem : expr_list
    | path_elems_list_list'''
    t[0]=t[1]

def p_create_st(t): #python,js,c#
    '''create_st : CREATE FILES fsysitem
    | CREATE DIRS fsysitem
    | CREATE DATABASE fsysitem'''
    global outstring,active_lang,__strict_mode
    if active_lang=='js' and __strict_mode==1: raise Exception('Error: JavaScript no soporta de forma nativa acceso a archivos o directorios ni creacion de bases de datos')
    elif active_lang in ['python','cython']:
        t[0]=''
        #print 't[3]:%s' % t[3]
        elems=findElements(t[3])
        #print 'elems:%s' % elems
        if t[2]=="dirs":
            for item in elems:
                t[0]+='os.makedirs(' + item + ')\n'
        elif t[2]=="files":
            for item in elems:
                #print 'item: %s' % item
                t[0]+='open(' + item + ',"w").close()\n'
                #print 't[0]:%s' %t[0]
        else: #databases
            for item in elems:
                t[0]+='sqlite3.connect(' + item + ',isolation_level=None).close()\n'
    elif active_lang=='csharp':
        kind=1
        if t[2]=="dirs":
           kind=2
        elif t[2]=="files":
           kind=3
        t[0]=csharp_builder.process_create(kind,findElements(t[3]))
    elif active_lang=='java':
        kind=1
        if t[2]=="dirs":
           kind=2
        elif t[2]=="files":
           kind=3
        t[0]=java_builder.process_create(kind,findElements(t[3]))
    elif active_lang=='c++':
        kind=1
        if t[2]=="dirs":
           kind=2
        elif t[2]=="files":
           kind=3
        t[0]=cpp_builder.process_create(kind,findElements(t[3]))
    else: #Ya no vale, reescribir para java 
        pass
                
                     
def p_copy_st(t): #Revisar c#
    '''copy_st : COPY FILES expr TO expr
    | COPY DIRS expr TO expr'''
    global active_lang,csharp_builder,__strict_mode
    if active_lang=='js' and __strict_mode==1: raise Exception('Error en copy: JavaScript no permite de manera nativa el acceso a archivos')
    if active_lang in ['python','cython']:
        elems=findElements(t[3])
        if t[2]=='files':
            t[0]='python_runtime.doCopy(' + t[3] + ',' + t[5] + ',0)\n'
        else:
            t[0]='python_runtime.doCopy(' + t[3] + ',' + t[5] + ',1)\n'
    elif active_lang=='csharp': #C#
        if t[2]=='files':
            t[0]=csharp_builder.process_copy(t[3],t[5],1)
        else:
            t[0]=csharp_builder.process_copy(t[3],t[5],2)
    elif active_lang=='java': #Java#
        if t[2]=='files':
            t[0]=java_builder.process_copy(t[3],t[5],1)
        else:
            t[0]=java_builder.process_copy(t[3],t[5],2)


def p_delete_st(t): #c#,#ESTA MAL EN PYTHON!!!!
    '''delete_st : DEL FILES fsysitem
    | DEL DIRS fsysitem
    | DEL path_elems_list'''
    global active_lang,csharp_builder,cpp_builder,js_builder,java_builder,__strict_mode
    if active_lang=='js' and __strict_mode==1: raise Exception('Error en del: JavaScript no permite de manera nativa el acceso a archivos')
    if len(t)==3: #Solo deberia funcionar en Python,Cython y C++
        if active_lang in ['python','cython']: 
            t[0]= "del " + t[2] + '\n'
        elif active_lang=='c++':
            t[0]=cpp_builder.process_delete(t[2])
        else: #?????????
            t[0]=''
    elif active_lang in ['python','cython']: #Esto esta mal!!!!!
        elems=findElements(t[3])
        if t[2]=='files':
            t[0]='python_runtime.doDelete(' + t[3] + ',0)\n'
        else:
            t[0]='python_runtime.doDelete(' + t[3] + ',1)\n'
    elif active_lang=='csharp': #C#
        if t[2]=='files':
            t[0]=csharp_builder.process_delete(findElements(t[3]),1)
        else:
            t[0]=csharp_builder.process_delete(findElements(t[3]),2)
    elif active_lang=='java': #Java#
        if t[2]=='files':
            t[0]=java_builder.process_delete(findElements(t[3]),1)
        else:
            t[0]=java_builder.process_delete(findElements(t[3]),2)


def p_select_files_st(t): #ok
    '''select_files_st : SELECT FILES expr_list FROM expr_list'''
    global active_lang,csharp_builder,__strict_mode
    if active_lang=='js' and __strict_mode==1: raise Exception('Error en select: JavaScript no permite de manera nativa el acceso a archivos')
    if active_lang in ['python','cython']:
        t[0]=''
        t[0]='python_runtime._get_files([' + t[3] + '],[' + t[5] + '])\n'
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_selectf(t[5],t[3])
    elif active_lang=='java':
        t[0]=java_builder.process_selectf(t[5],t[3])

def p_text_st(t): #ok
    '''text_st : WORDS FROM expr_list'''
    global t_name,t_counter,active_lang,__strict_mode,csharp_builder,cpp_builder
    if active_lang=='js' and __strict_mode==1: raise Exception('Error en text: JavaScript no permite de manera nativa el acceso a archivos')
    if active_lang in ['python','cython']:
        t[0]=''
        elems=findElements(t[3])
        name=t_name + str(t_counter)
        t_counter+=1
        t[0]+= name + '=""\n'
        for item in elems:
            t[0]+=name + '+=python_runtime.getPathText(' + item + ')\n'
        t[0]=[name,t[0]]
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_text_st(t[3])
    elif active_lang=='java':
        t[0]=java_builder.process_text_st(t[3])
    elif active_lang=='c++':
        t[0]=cpp_builder.process_text_st(t[3])
    else:
        pass
        
def p_lines_st(t): #ok
    '''lines_st : LINES BY expr FROM expr_list'''
    global t_name,t_counter,active_lang,__strict_mode
    if active_lang not in ['python','cython','c++'] and __strict_mode==1: raise Exception('Error en lines: solo se permite en Python, Cython y C++')
    t[0]=''
    if active_lang=='python':
        elems=findElements(t[5])
        name=t_name + str(t_counter)
        t_counter+=1
        t[0]+= name + '=[]\n'
        for item in elems:
            t[0]+=name + '+=python_runtime.getPathText(' + item + ').split(' + t[3] + ')\n'
        t[0]=[name,t[0]]
    elif active_lang=='c++':
        elems=findElements(t[5])
        t[0]=cpp_builder.process_lines(t[3],elems)
    elif active_lang=='csharp':
        elems=findElements(t[5])
        t[0]=csharp_builder.process_lines(t[3],elems)
    elif active_lang=='java':
        elems=findElements(t[5])
        t[0]=java_builder.process_lines(t[3],elems)
    else:#??
        t[0]=''

def p_idtotext_st(t): #ok
    '''idtotext_st : expr BY expr TO WORDS
    | expr BY expr COMMA expr TO WORDS'''
    global t_name,t_counter,active_lang
    name=t_name + str(t_counter)
    t_counter+=1
    if active_lang in ['python','cython']:
        t[0]=name + '=""\n'
        t[0]+='if type(' + t[1] + ')!= type([]): raise Exception("Error: Debe ser una lista")\n'
        if len(t)==6:
            t[0]+=name + '=' + t[3] + '.join(' + t[1] + ')\n'
        else:
            t[0]+=name + '=' + t[5] + '.join([' + t[3] + '.join(el) for el in ' + t[1] + '])\n' 
        t[0]=[name,t[0]]
    elif active_lang=='js':
        name=t_name + str(t_counter)
        t_counter+=1
        if len(t)==6:
            t[0]=js_builder.process_idtotext(name,t[1],[t[3]])
        else:
            t[0]=js_builder.process_idtotext(name,t[1],[t[3],t[5]])
    else:
        if __strict_mode==1:
            raise Exception('Error: La construccion "expr by expr to words" solo se permite en Python,Cython y JavaScript')

def p_format_st(t): #ok
    '''format_st : FORMAT expr WITH expr'''
    global active_lang,js_builder,csharp_builder,cpp_builder
    if active_lang in ['python','cython']:
        t[0]='python_runtime.doFormat(' + t[2] + ',' + t[4] + ')'
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_format(t[2],t[4]);
    elif active_lang=='java':
        t[0]=java_builder.process_format(t[2],t[4]);
    elif active_lang=='c++':
        t[0]=cpp_builder.process_format(t[2],t[4]);
    elif active_lang=='js':
        t[0]=js_builder.process_format(t[2],t[4]);
    else: #C#
        pass

def p_binary_st(t): #ok
    '''binary_st : BINARY expr_list
    | BINARY expr_list FROM expr TO expr'''
    global t_name,t_counter,active_lang,__strict_mode
    if active_lang not in ['python','cython'] and __strict_mode==1: raise Exception('Error: en binary: Solo se permite para Python')
    t[0]=''
    elems=findElements(t[2])
    name=t_name + str(t_counter)
    t_counter+=1
    t[0]+= name + '=""\n'
    for item in elems:
        if len(t)==3:
            t[0]+=name + '+=python_runtime.getPathTextBinary(' + item + ')\n'
        else:
            t[0]+=name + '+=python_runtime.getBinaryChunk(' + item + ',' +  str(int(t[4])) + ',' + str(int(t[6])) +  ')\n'
    t[0]=[name,t[0]]


def p_textwrite_st(t): #ok
    '''textwrite_st : WORDS expr TO expr_list
    | ADD WORDS expr TO expr_list'''
    global t_name,t_counter,active_lang,__strict_mode,cpp_builder
    if active_lang not in ['python','cython'] and __strict_mode==1: raise Exception('Error en words o add words: Esta construccion solo se permite en Python')
    if active_lang in ['python','cython']:
        t[0]=''
        elems=''
        if len(t)==6:
           #elems=findElements(t[5])
           elems=t[5]
        else:
           #elems=findElements(t[4])
           elems=t[4]
        name=t_name + str(t_counter)
        t_counter+=1
        t[0]+= name + '=""\n'
        for item in elems.split(','):
            t[0]+='if os.path.exists(' + item + ') and os.path.isfile(' + item + '):\n'
            if len(t)==6:
                t[0]+= '    ' + name + '=open(' + item + ',"a")\n'
                t[0]+= '    ' + name + '.write(' + t[3] + ')\n'
            else:
                t[0]+= '    ' + name + '=open(' + item + ',"w")\n'
                t[0]+= '    ' + name + '.write(' + t[2] + ')\n'
            t[0]+= '    ' + name + '.close()\n'
            t[0]+= 'else:\n     raise Exception(\'Error: "%s" debe ser un archivo valido\'%' + item + ')\n' #%item
        t[0]=[name,t[0]]
    elif active_lang=='c++':
        if t[1]=='words':
            t[0]=cpp_builder.process_textwrite(t[2],t[4],False)
        else:
            t[0]=cpp_builder.process_textwrite(t[3],t[5],True)
    elif active_lang=='csharp':
        if t[1]=='words':
            t[0]=csharp_builder.process_textwrite(t[2],t[4],False)
        else:
            t[0]=csharp_builder.process_textwrite(t[3],t[5],True)
    elif active_lang=='java':
        if t[1]=='words':
            t[0]=java_builder.process_textwrite(t[2],t[4],False)
        else:
            t[0]=java_builder.process_textwrite(t[3],t[5],True)
    else:
        t[0]=""



def p_binarywrite_st(t): #ok
    '''binarywrite_st : BINARY expr TO expr_list
    | ADD BINARY expr TO expr_list'''
    global t_name,t_counter,active_lang,__strict_mode
    if active_lang not in ['python','cython'] and __strict_mode==1: raise Exception('Error en binary: Solo se permite para Python')
    t[0]=''
    elems=''
    if len(t)==5:
        elems=findElements(t[4])
    else:
        elems=findElements(t[5])
    name=t_name + str(t_counter)
    t_counter+=1
    t[0]+= name + '=""\n'
    for item in elems:
        t[0]+='if os.path.exists(' + item + ') and os.path.isfile(' + item + '):\n'
        if len(t)==5:
            t[0]+= '    ' + name + '=open(' + item + ',"wb")\n'
            t[0]+= '    ' + name + '.write(' + t[2] + ')\n'
            t[0]+= '    ' + name + '.close()\n'
        else:
            t[0]+= '    ' + 'python_runtime.appendBinaryChunk(' + item + ',' + t[3] + ')\n'
        t[0]+= 'else:\n     raise Exception("Error: "%s" debe ser un archivo valido")\n'%item
    t[0]=[name,t[0]]


def p_update_st(t): #Revisar
    '''update_st : UPDATE expr_list LET expr EQUAL expr'''
    global aux_string,u_counter,u_name,re_name,re_counter,cpp_builder,js_builder,csharp_builder,active_lang
    if active_lang in ['python','cython']:
        elems=findElements(t[2])
        name=u_name + str(u_counter)
        u_counter+=1
        re_counter+=1
        old_pat=t[4]
        new_pat=t[6]
        aux=''
        aux+= name + '=""\n'
        for item in elems:
            aux+='if os.path.exists(' + item + ') and os.path.isfile(' + item + '):\n'
            aux+= '    f_' + name + ' = open(' + item + ',"r")\n'
            aux+= '    ' + name + ' += re.sub(' + old_pat + ',' + new_pat + ',' + 'f_' + name +  '.read())\n'
            aux+= '    f_' + name + '.close()\n'
            aux+= '    f_' + name + ' = open(' + item + ',"w")\n'
            aux+= '    f_' + name + '.write(' + name + ')\n'
            aux+= '    f_' + name + '.close()\n'
            aux+= 'else:\n' + '    ' +  name + '+=re.sub(' + old_pat + ',' + new_pat + ',' + item + ')\n'
        t[0]=[name,aux]
    elif active_lang=='js':
        elems=findElements(t[2])
        name=u_name + str(u_counter)
        u_counter+=1
        t[0]=js_builder.process_update(name,elems,t[4],t[6])
    elif active_lang=='csharp':
        elems=findElements(t[2])
        name=u_name + str(u_counter)
        u_counter+=1
        t[0]=csharp_builder.process_update(name,elems,t[4],t[6])
    elif active_lang=='java':
        elems=findElements(t[2])
        name=u_name + str(u_counter)
        u_counter+=1
        t[0]=java_builder.process_update(name,elems,t[4],t[6])
    elif active_lang=='c++':
        elems=findElements(t[2])
        name=u_name + str(u_counter)
        u_counter+=1
        t[0]=cpp_builder.process_update(name,elems,t[4],t[6])

def p_cut_st(t): #Revisar
    '''cut_st : CUT expr_list BY expr'''
    global aux_string,s_counter,s_name,active_lang,csharp_builder,cpp_builder
    if active_lang in ['python','cython']:
        elems=findElements(t[2])
        name=s_name + str(s_counter)
        s_counter+=1
        pat=t[4]
        aux= name + '=[]\n'
        for item in elems:
            aux+='if os.path.exists(' + item + ') and os.path.isfile(' + item + '):\n'
            aux+= '    ' + name + ' += re.split(open(' + item + ').read(),' + pat + ')\n'
            aux+= 'else:\n' + '    ' +  name + '+=re.split(' + pat + ',' + item + ')\n'
        t[0]=[name,aux]
    elif active_lang=='js':
        elems=findElements(t[2])
        name=s_name + str(s_counter)
        s_counter+=1
        t[0]=js_builder.process_cut(name,t[4],elems)
    elif active_lang=='csharp':
        elems=findElements(t[2])
        name=s_name + str(s_counter)
        s_counter+=1
        t[0]=csharp_builder.process_cut(name,t[4],elems)
    elif active_lang=='java':
        elems=findElements(t[2])
        name=s_name + str(s_counter)
        s_counter+=1
        t[0]=java_builder.process_cut(name,t[4],elems)
    elif active_lang=='c++':
        elems=findElements(t[2])
        name=s_name + str(s_counter)
        s_counter+=1
        t[0]=cpp_builder.process_cut(name,t[4],elems)
        
def p_match_st(t): #Revisar
    '''match_st : MATCH expr IN expr_list'''
    global aux_string,m_counter,m_name,aux_counter,aux_name,active_lang,js_builder,csharp_builder,cpp_builder
    if active_lang in ['python','cython']:
        elems=findElements(t[4])
        name=m_name + str(m_counter)
        m_counter+=1
        pat=t[2]
        aux= name + '=[]\n'
        for item in elems:
            aux+='if os.path.exists(' + item + ') and os.path.isfile(' + item + '):\n'
            aux+= '    ' + name + ' += re.findall(open(' + item + ').read(),' + pat + ')\n'
            aux+= 'else:\n' + '    ' +  name + '+=re.findall(' + pat + ',' + item + ')\n'
        t[0]=[name,aux]
    elif active_lang=='js':
        elems=findElements(t[4])
        name=m_name + str(m_counter)
        m_counter+=1
        t[0]=js_builder.process_match(name,t[2],elems)
    elif active_lang=='csharp':
        elems=findElements(t[4])
        name=m_name + str(m_counter)
        m_counter+=1  
        t[0]=csharp_builder.process_match(name,t[2],elems)
    elif active_lang=='java':
        elems=findElements(t[4])
        name=m_name + str(m_counter)
        m_counter+=1  
        t[0]=java_builder.process_match(name,t[2],elems)
    elif active_lang=='c++':
        elems=findElements(t[4])
        name=m_name + str(m_counter)
        m_counter+=1  
        t[0]=cpp_builder.process_match(name,t[2],elems)
    

def p_xml_st(t): #Revisar
    '''xml_st : XML expr_list
    | XML expr FROM path_elems_list
    | XML path_elems_list ARROW path_elems_list IN expr'''
    global active_lang,x_name,x_counter
    if active_lang in ['python','cython']:
        t[0]=''
        if len(t)==3:
            elems=findElements(t[2])
            name=x_name + str(x_counter)
            x_counter+=1
            t[0]=name + '=[]\n'
            for item in elems:
                t[0]+='if os.path.exists(' + item + ') and os.path.isfile(' + item + '):\n'
                t[0]+= '    ' + name + '.append(minidom.parseString(open(' + item + ',"r").read()))\n'
                t[0]+= 'else:\n ' + '    ' +  name + '.append(minidom.parseString(' + item + '))\n'
        elif len(t)==7:#????????????????????
            name=x_name + str(x_counter)
            x_counter+=1
            t[0]=name + '=xpath.find(' + t[6] + ',' + t[4] + ')\n'
            t[0]+=name + '__=' + t[2] + '.firstChild\n'
            t[0]+=name + '[0].appendChild(' + name + '__)\n'
            t[0]+=name + '=' + name + '[0]\n'
        else:
            name=x_name + str(x_counter)
            x_counter+=1
            t[0]=name + '=None\n'
            t[0]+='if type(' + t[4] + ') in [type(""),type(u"")]: ' + t[4] + '=minidom.parseString(' + t[4] + ')\n'
            t[0]+= name + '=xpath.find(' + t[2] + ',' + t[4] + ')\n'
        t[0]=[name,t[0]]
    else:
        if active_lang=='java':
            t[0]=java_builder.process_xml_st(t)
        elif active_lang=='js':
            t[0]=js_builder.process_xml_st(t)
        elif active_lang=='csharp':
            t[0]=csharp_builder.process_xml_st(t)
        elif active_lang=='c++':
            t[0]=cpp_builder.process_xml_st(t)


def p_html_st(t):
    '''html_st : HTML expr
    | HTML path_elems_list INSERTOR expr'''
    global active_lang,x_name,x_counter
    #if active_lang not in ['python','cython'] and __strict_mode==1:
    #    raise Exception("Error: solo se admiten sentencias html en Python") 
    if active_lang in ["python","cython"]:
        name=x_name + str(x_counter)
        x_counter+=1    
        if len(t)==3: #Crear un html nuevo a partir de un string o un archivo o una url
            t[0]=name + '=""\n'
            t[0]+='if ' + t[2] + '.strip().find("http://")==0:\n' #URL: descargarla
            t[0]+='    ' +  name + '=BeautifulSoup.BeautifulSoup(urllib.urlopen(' + t[2] + ').read())\n'
            t[0]+='elif os.path.exists(' + t[2] + '):\n'
            t[0]+='    ' + name + '=BeautifulSoup.BeautifulSoup(open(' + t[2] + ').read())\n'
            t[0]+='else:\n'
            t[0]+='    ' + name + '=BeautifulSoup.BeautifulSoup(' + t[2] + ')\n'
            t[0]=[name,t[0]]
        else:
            #Cogemos el fragmento definido por la expresion BeautifulSoup t[4]
            #Si hay mas de un fragmento, habra comas y es necesario transformar en una lista
            t[0]=name + '=""\n'
            t[0]+='parts=' + t[4] + '\n'
            t[0]+="if len(parts.split(','))!=0:\n"
            t[0]+='   ' + "parts=parts.split(',')\n"
            #soup.findAll devuelve una lista
            t[0]+='__elems=' + t[2] + '.findAll(parts)\n'
            t[0]+= name + "=BeautifulSoup.BeautifulSoup(''.join([str(el) for el in __elems]))\n"
            t[0]=[name,t[0]]
    else:
        if active_lang=='java':
            t[0]=java_builder.process_html_st(t)
        elif active_lang=='js':
            t[0]=js_builder.process_html_st(t)
        elif active_lang=='csharp':
            t[0]=csharp_builder.process_html_st(t)
        elif active_lang=='c++':
            t[0]=cpp_builder.process_html_st(t)


def p_consult_st(t): #Revisar. Podemos querer meter mas reglas o consultar????
    '''consult_st : CONSULT PROLOG expr WITH expr opt_addto'''
    global active_lang,pl_name,pl_counter,defined_id,__strict_mode
    if active_lang not in ['python','cython'] and __strict_mode==1: raise Exception('Error: Las extensiones prolog solo estan disponibles para Python')
    name=pl_name + str(pl_counter)
    pl_counter+=1    
    #Resetear reglas o se duplican en cada llamada a consult
    #a no ser que se quiera aumentar las reglas con add
    t[0]=''
    if t[6]=='add':
            t[0]+=name + '={}\n'
            t[0]+='prologpy.procString(' + t[5] + ')\n'
    else:
        if t[6]!='lazy':
            t[0]+='prologpy.rules=[]\n'
            t[0]+='prologpy.procString(' + t[3] + ')\n'
        t[0]+='result_list=prologpy.search(prologpy.Term(' + t[5] + '))\n'
        t[0]+=name + '={}\n'
        #t[0]+='print prologpy.rules\n'
        #t[0]+='print result_list\n'
        t[0]+='for item in result_list:\n'
        t[0]+='        if type(item)==type({}):\n'
        t[0]+='            for k in item:\n'
        t[0]+='                if not ' + name + '.has_key(k):\n'
        t[0]+='                    ' + name + '[k]=[item[k]]\n'
        t[0]+='                else:\n'
        t[0]+='                    ' + name + '[k].append(item[k])\n'
        t[0]+='        else: #Hay un Yes o similar\n'
        t[0]+='            ' + name + '["default"]=item\n'
    t[0]=[name,t[0]]


def p_opt_addto(t):
    '''opt_addto : ADD
    | LAZY
    | empty'''
    t[0]=t[1]

def p_consult_db_st(t): #Revisar (cambiar expr por ID???)
    '''consult_db_st : CONSULT DATABASE expr WITH expr_list
    | CONSULT DATABASE expr AS expr WITH expr_list'''
    global active_lang,db_name,db_counter,csharp_builder,__strict_mode
    name=db_name + str(db_counter)
    db_counter+=1
    t[0]=""
    aux=name + '=[]\n'
    if active_lang=='js' and __strict_mode==1: raise Exception('Error: JavaScript no permite de forma nativa el acceso a bases de datos')
    if active_lang in ['python','cython']:
        if len(t)==6: #sqlite
            elems=findElements(t[5])
            aux+=name + '_conn=sqlite3.connect(' + t[3] + ',isolation_level=None)\n'
            aux+=name + '_cursor=' + name + '_conn.cursor()\n'
            #Ejecutar las consultas secuencialmente
            for item in elems:
                aux+=name + '_cursor.execute(' + item + ')\n'
                aux+='for i in ' + name + '_cursor:\n'
                aux+='    if type(i)==type((0,)):\n'
                aux+='        ' + name + '.append(list(i))\n'
                aux+='    else:\n'
                aux+='        ' + name + '.append(i)\n'
            aux+='names = [description[0] for description in ' + name + '_cursor.description] if ' + name + '_cursor.description else []\n'
            #aux+=name + '_conn.commit()\n' #recuperar si va mal!!!
            aux+= name + '_conn.commit()\n'
            aux+= name + '= {"data":' + name + ' ,' + '"names": names,"affected":' + name + '_cursor.rowcount}\n' 
            t[0]=[name,aux]
        else: #ado
            elems=findElements(t[5])
            aux+=name + '= python_runtime._queryADO(' + t[5] + ',' + t[7] + ')\n'
            t[0]=[name,aux]
    elif active_lang=='csharp':
        t[0]=csharp_builder.process_consult_db(t[3],t[5])
    elif active_lang=='java':
        t[0]=java_builder.process_consult_db(t[3],t[5])
    elif active_lang=='c++':
        t[0]=cpp_builder.process_consult_db(t[3],t[5])
    else: #C#
        pass
   
def p_empty(t):
    '''
    empty : 
    '''
    t[0]=''



####----------------------------------------------------------------------------------
####                         EXTENSIONES LINQ-LIKE
####----------------------------------------------------------------------------------
def p_linqlike_st(t):
    '''linqlike_st : FROM origin SELECT attr_list where_list groupby orderby'''
    global active_lang
    if active_lang not in ['python','cython']:
        raise Exception("Error: Solo se aceptan sentencias from-select en Python")
    attrs_list=t[4]
    
    linqresult_list=[]
    group_list=t[6]
    #print 'group_list: %s' % group_list
    where_list=t[5]
    #print 'where_list:%s' % where_list
    #print type(where_list)
    order_list=t[7][0] if len(t[7])==2 else t[7]
    #print 'order_list:%s' % order_list
    order_type=t[7][1] if len(t[7])==2 else 'asc'
    #print TYPESTAB
    #Hay que dar la vuelta a la lista de atributos
    #attrs_list.reverse()
    #print 'attrs_list en linqlike: %s' % attrs_list
    attr_pos={}
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
        #OJO: ESTO SE HA QUITADO PARA PERMITIR GROUPBY DE UN SOLO CAMPO CONSIGO MISMO. REVISARLO--------------------------------------
        #if el[0] in flds:
        #    raise Exception('Error: el campo "%s" ya se ha usado. No se permiten campos duplicados en los campos de seleccion'%el[0])
        #-----------------------------------------------------------------------------------------------------------------------------
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
    flds=[]
    conds=where_list  #t5
    #Hay que dar la vuelta a las condiciones (usamos and y  el orden importa)
    conds.reverse()
    #print 'correcto hasta aqui'
    #ENTRADA A PLANTILLA??
    #_linqlike(conds_list,where_list,group_list,attrs_list,_list)
    #def _linqlike(where_list,group_list,attrs_list,order_list,_list,order_type)
    t[0]='python_runtime._linqlike(' + str(conds) + ',' + str(group_list) + ',' + str(attrs_list) + ',' + str(order_list) + ',' + t[2] + ',"' + order_type + '")\n'
    

def p_origin_st(t): #Anteriormente linqlike_st!!!!
    '''origin : path_elems_list
    | LPAREN functional_st RPAREN'''
    if len(t)==4:
        t[0]=t[2]
    else:
        t[0]=t[1]
    #print 't[0] en origin: %s' %t[0]

 
def p_attr_list_st(t):
    '''attr_list : attr COMMA attr_list
    | attr'''
    global attrs_list
    if len(t)==2:
        t[0]=[t[1]]
    else:
        t[0]=[t[1]] + t[3]
    #cleanup
    attrs_list=[]
    

#Revisar llamadas a check_attr!!!!
#Revisar las opciones no AS NUMBER (en principio no se deberian permitir)
def p_attr_st(t): 
    '''attr : attr_elem
    | attr_elem AS NUMBER
    | attr_elem LPAREN attr_elem RPAREN
    | attr_elem LPAREN attr_elem RPAREN AS NUMBER
    | COUNT LPAREN attr_elem RPAREN
    | COUNT LPAREN attr_elem RPAREN AS NUMBER'''
    funcs=['count','sum','avg','std','stdp','var','varp','max','min']
    t[1]=t[1].strip('%')
    if len(t)==7:
        t[3]=t[3].strip('%')
        t[3]=check_attr(t[3])
        if not t[1]in funcs:
            raise Exception('Error: "%s" no es una funcion de agregado permitida. Solo se aceptan "%s"'%(t[1],", ".join(funcs)))
        t[0]=[t[3],t[6],t[1]]
    elif len(t)==5:
        t[3]=t[3].strip('%')
        t[3]=check_attr(t[3])
        if not t[1]in funcs:
            raise Exception('Error: "%s" no es una funcion de agregado permitida. Solo se aceptan "%s" '%(t[1],", ".join(funcs)))        
        t[0]=[t[3],-1,t[1]]
    elif len(t)==4:
        t[3]=t[3].strip('%')
        t[1]=check_attr(t[1])
        t[0]=[t[1],t[3],'']
    else:
        t[1]=check_attr(t[1])
        t[0]=[t[1],-1,'']
#Ojito: esto es para poder coger claves de diccionarios que sean strings
def p_attr_elem(t): 
    '''attr_elem : ID
    | STRING'''
    t[0]=t[1]   

def check_attr(at):
    global attrs_list,att_counter
    if not at in attrs_list:
        attrs_list.append(at)
    else:
        at=at + str(att_counter)
        att_counter+=1
    return at
    
def p_where_list_st(t):
    '''where_list : WHERE where_conds
    | empty'''
    #global where_list
    #t[0]=where_list[:]
    if len(t)==2:
        t[0]=[]
    else:
        t[0]=t[2]



def p_where_conds_st(t):
    '''where_conds : condition AND where_conds
    | condition'''
    #global where_list
    #where_list.append(t[1])
    #t[0]=t[1]
    if len(t)==2:
        t[0]=[t[1]]
    else:
        t[0]=[t[1]] + t[3]


def p_condition_st(t):
    '''condition : PIPE ID condition_op expr PIPE
    | PIPE ID IN LBRACK expr_list RBRACK PIPE
    | PIPE ID NOT IN LBRACK expr_list RBRACK PIPE
    | PIPE ID BETWEEN expr AND expr PIPE
    | PIPE ID NOT BETWEEN expr AND expr PIPE
    | PIPE ID LIKE expr PIPE
    | PIPE ID NOT LIKE expr PIPE
    | PIPE ID MATCH expr PIPE'''
    t[2]=t[2].strip('%')
    if len(t)==6:
        if type(t[4]) in [type(''),type(u'')]: t[4]=t[4].strip('"')
        t[0]=[t[2],t[3],t[4]]
    else:
        if t[3]=='match':
            if type(t[4]) not in [type(''),type(u'')]:
                raise Exception('Error: "%s" no es un texto'%t[4])            
            t[0]=[t[2],'match',t[4].strip('"')]
        elif t[4]=='[':
            t[0]=[t[2],'in',t[5]]
        elif t[5]=='[':
            t[0]=[t[2],'not in',t[6]]          
        elif t[3]=='between':
            if type(t[4]) not in [type(0),type(0L),type(0.0)]:
                raise Exception('Error: "%s" no es un numero'%t[4])
            if type(t[6]) not in [type(0),type(0L),type(0.0)]:
                raise Exception('Error: "%s" no es un numero'%t[6])             
            t[0]=[t[2],'between',t[4],t[6]]
        elif t[3]=='not' and t[4]=='between':
            if type(t[5]) not in [type(0),type(0L),type(0.0)]:
                raise Exception('Error: "%s" no es un numero'%t[5])
            if type(t[7]) not in [type(0),type(0L),type(0.0)]:
                raise Exception('Error: "%s" no es un numero'%t[7])             
            t[0]=[t[2],'not between',t[5],t[7]]
        elif t[3]=='like':
            if type(t[4]) not in [type(''),type(u'')]:
                raise Exception('Error: "%s" no es un texto'%t[4])
            t[0]=[t[2],'like',t[4].strip('"')]
        elif t[3]=='not' and t[4]=='like':
            if type(t[5]) not in [type(''),type(u'')]:
                raise Exception('Error: "%s" no es un texto'%t[5])            
            t[0]=[t[2],'not like',t[5].strip('"')]

            
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
    #t[0]=1
    if len(t)==2:
        t[0]=[]
    else:
        t[0]=t[2] #[t[2]]


def p_id_list3(t):
    '''id_list3 : ID AS NUMBER
    | ID AS NUMBER COMMA id_list3'''
    #global group_list
    #Hay que saber el orden de la columna por la que
    #filtrar con respecto a la matrix original
    ##COMPROBAR QUE LOS NUMEROS DEL AS SON DISTINTOS!!!!!
    #group_list.append([t[1],t[3]])
    #t[0]=1
    # if len(t)==4: #REcuperar si no va el cambio!!!
        # t[0]= [t[1],t[3]]
    # else:
        # t[0]=[t[1],t[3]] + t[5]
    t[1]=t[1].strip('%')
    if len(t)==4: #Revisar cambio!!!
        t[0]= [[t[1],t[3]]]
    else:
        t[0]=[[t[1],t[3]]] + t[5] 
    #print 't[0]hasta ahora: %s' % t[0]
    

def p_orderby_st(t):
    '''orderby : ORDER BY id_list5
    | ORDER BY id_list5 ASC
    | ORDER BY id_list5 DESC
    | empty'''
    #global order_type
    #if len(t)==5:
    #    order_type=t[4]
    #else:
    #    order_type='asc'
    #t[0]=1
    if len(t)==2:
        t[0]=[]
    elif len(t)==4:
        t[0]=[t[3],'asc']
    else:
        t[0]=[t[3],t[4]]


def p_id_list5(t):
    '''id_list5 : ID AS NUMBER
    | ID AS NUMBER COMMA id_list5'''
    #global order_list
    #order_list.append(t[3])
    t[1]=t[1].strip('%')
    t[0]=1
    if len(t)==4:
        t[0]=[t[3]]
    else:
        t[0]=[t[3]] + t[5]


# Error rule for syntax errors
def p_error(t):
    #print dir(t)
    global __program,__program_file
    #print 'Localizado un error'
    print '\nError de sintaxis (token no permitido) evaluando token "%s" en:\n'%t.value
    #print 'Error evaluando Token: %s en:' %repr(t)
    #print "en la linea %s y en posicion %s" % (t.lineno,t.lexpos)
    print " ==> %s,...,etc.\n" %__program[t.lexpos:t.lexpos + 75]
    if __program_file:
        print 'procesando archivo: %s en la linea %s\n' %(__program_file,t.lexer.lineno)
    raise Exception(">>> Minimal language: Programa terminado con errores.")                                                                



def parserFactory():
    #Generamos el parser con picklefile para evitar el parsetab.py!!
    #Si se usa tabmodule, primero hay que generarlo sin write_tables y despues usar write_tables!!!!!!!!!!!
    # if 'java' in sys.platform: #Version recortada para java
        # return yacc.yacc(debug=1,tabmodule='minimal_java_parsetab',write_tables=False)#Poner a debug=0 en produccion
    # else:
        # return yacc.yacc(debug=1,tabmodule='minimal_parsetab',write_tables=False)#Poner a debug=0 en produccion
    return yacc.yacc(debug=1)#,tabmodule='minimal_parsetab',write_tables=False)#Poner a debug=0 en produccion

parser=parserFactory()

def generateExe():
    global create_exe,print_script,exec_script,outputfile,active_lang,exe_props,__program_file,outputdir,__dependencies,has_tix
    config={}
    required=["version","name"]
    #Si existe el archivo de propiedades, usarlo
    if exe_props and os.path.exists(exe_props):
        #permitimos comentarios y lineas vacias(?)
        valids = [l for l in open(exe_props,'r').readlines() if len(l) and l.strip()[0]!='#']
        for line in valids:
            parts=lins.split('=')
            config[parts[0].strip()]=parts[1].strip()
    else:
        config['name']=outputfile.split('.')[0]#os.path.basename(__program_file).split('.')[0]
        config['icon']='icono.ico'
        config['version']='1.0'
        config['description']='Minimal generated program'
        config['modules_list']=str(__dependencies)
        config['pythonpath']= sys.executable
        config['precompile']='echo Generando ejecutable para el script...'
        config['postcompile']='echo Ejecutable generado'
        config['includes']=''
        config['excludes']=''
        config['dllincludes']=''
        config['dllexcludes']=''
        config["outdir"]=outputdir if outputdir != '.' else 'dist'
    #Crear cadena para setup.py
    setup= exe_setup
    setup=setup.replace('%%name%%',config['name'])
    setup=setup.replace('%%scriptname%%',outputdir + '/' + config['name'])
    setup=setup.replace('%%description%%',config['description'])
    setup=setup.replace('%%version%%',config['version'])
    setup=setup.replace('%%icon%%',config['icon'])
    setup=setup.replace('%%modules_list%%',config['modules_list'])
    setup=setup.replace('%%outdir%%',config['outdir'])
    cmdorder=cmd_compile
    cmdorder=cmdorder.replace('%%precompile%%',config['precompile'])
    cmdorder=cmdorder.replace('%%postcompile%%',config['postcompile'])
    cmdorder=cmdorder.replace('%%pythonpath%%',config['pythonpath'])
    cmdorder=cmdorder.replace('%%includes%%',config['includes']) #No es asi, es una lista!!!!
    cmdorder=cmdorder.replace('%%excludes%%',config['excludes'])
    cmdorder=cmdorder.replace('%%dllincludes%%',config['dllincludes'])
    cmdorder=cmdorder.replace('%%dllexcludes%%',config['dllexcludes'])
    #Generar setup.py
    f=open('setup.py','w')
    f.write(setup)
    f.close()
    #y ejecutar la linea de comandos
    for order in cmdorder.split('\n'):
        os.system(order)
    #Rematar la faena: copiar parsetab.p en el directorio dist
    shutil.rmtree('build')
    if outputdir!='.':
        shutil.copyfile('parsetab.p',outputdir + '/parsetab.p')
        copyExtraFiles(outputdir)
    else:
        shutil.copyfile('parsetab.p','dist/parsetab.p')
    #TODO: copiar modulos que necesita por defecto y permitir renombrar el directorio de salida. La opcion type no la estamos usando????
    #copyExtraFiles(outputdir)
    #Cambiar el nombre del directorio dist si se ha especificado

def copyExtraFiles(dest):
    global extra_files,outputdir
    outdir=''
    if outputdir!=dest:
        outdir=outputdir + '/' + dest
    else:
        outdir=outputdir
    #asegurarse de que el directorio base existe
    if outputdir!=dest:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
    #Copiar todos los archivos extra especificados
    for item in extra_files:
        if os.path.isfile(item):
            shutil.copyfile(item,outdir + '/' + os.path.basename(item))
        elif os.path.isdir(item):
            shutil.copytree(item,outdir + '/' + os.path.basename(item))

if __name__=='__main__':
    if not 'bridge' in sys.modules:
         bridge=__import__('bridge')
    else:
         bridge=sys.modules['bridge']
    if not 'python_runtime' in sys.modules:
         python_runtime=__import__('python_runtime')
    #Establecer opciones de linea de comandos
    setCommandLineOptions(sys.argv)
    #Permitimos arrancar en modo repl minimal, prolog y los lisps
    if repl_mode==1:
        if prolog_mode==1:
            if not 'prologpy' in sys.modules: 
                 prologpy=__import__('prologpy')
            else:
                 prologpy=sys.modules['prologpy']
            prologpy.main()
            sys.exit(0)
        elif clojure_mode==1:
            if not 'clojure' in sys.modules: 
                 clojure=__import__('clojure')
            else:
                 clojure=sys.modules['clojure']
            clojure.main.main()
            sys.exit(0)
        elif lisp_mode==1:
            import hy
            import hy.cmdline
            hy.cmdline.run_repl()
            sys.exit(0)
        elif scheme_mode==1:
            if not 'lispy' in sys.modules: 
                 lispy=__import__('lispy')
            else:
                 lispy=sys.modules['lispy']
            lispy.repl()
            sys.exit(0)
        else: #repl minimal
            code=''
            if not 'mini_tkbasic' in sys.modules:
                mini_tkbasic=sys.modules['mini_tkbasic']
            while 1:
                code=raw_input('minimal>')
                if code=='quit': break
                bridge.__reflected=1
                code=preprocess(code)
                code=parser.parse(code)
                exec code
    program=open(sys.argv[1]).read()
    __program_file=sys.argv[1]
    #program=program.replace('\r\n','\n')
    #program=program.replace('\r','\n')
    #Preprocesador
    program=preprocess(program)
    __program=program
    #print program
    code=parser.parse(program,tracking=True)
    if print_script==1:
        print code
    #Esto obtiene la gramatica----
    #print help(bridge)
    #-----------------------------
    if exec_script==1:
        exec code
    if create_exe==1:
        generateExe()
    if create_exe==0 and extra_files!=[]:
        if outputdir and outputdir!='.':
            copyExtraFiles(outputdir)
        else:
            copyExtraFiles('extras')
    print '>Interprete Bridge finalizado sin errores.'