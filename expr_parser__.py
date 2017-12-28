from __future__ import division
#!Python

#Para medir eficiencia------------------------------------------------
import time
#print 'Comenzando carga de modulos: %s' % time.strftime('%H:%M:%S')
#---------------------------------------------------------------------

import yacc
import os
import os.path
import sys
import math
import re
import random

#Esto para que no molesten los warnings------------------------
import warnings
warnings.filterwarnings('ignore')
#--------------------------------------------------------------
#print 'Antes de llegar a las que dependen del sistema operativo: %s' % time.strftime('%H:%M:%S')

import stlex2

#Nombre generico para listas,arrays y dicts
l_name='list'
l_counter=0
a_counter=0
a_name='array'
d_counter=0
d_name='dict'


#FALLA CON "," EN LOS STRINGS!!!!
def findElements(cad):
    instr=0
    elems=[]
    #Proteger cadenas, listas y arrays interiores
    noms='%%%'
    ncont=0
    sust={}
    for it in re.findall(r'\"[^\"]*?\"',cad):
        t=noms+str(ncont)
        sust[t]=it
        cad=cad.replace(it,t)
        ncont+=1
    for it in re.findall(r'{[^}]*?\}',cad):
        t=noms+str(ncont)
        sust[t]=it
        cad=cad.replace(it,t)
        ncont+=1
    for it in re.findall(r'\[[^\]]*?\]',cad):
        t=noms+str(ncont)
        sust[t]=it
        cad=cad.replace(it,t)
        ncont+=1
    item=''
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
    if item!='':
        while '%%%' in item:
            for el in sust:
                item=item.replace(el,sust[el])          
        elems.append(item)
    return elems


def getSequenceName(item):
    lines=item.split(';')
    return lines[0].split('=')[0].split()[1]

# Get the token map from the lexer.  This is required.
tokens=stlex2.tokens

#Plantilla para codigo csharp
cs_template='''
/* Minimal# generated code */

using System;
using System.Collections;
using System.IO;
using System.Linq;
//user imports
%%__imports__%%

//Main class
public class Minimal%%__name__%%
{
   %%__functions__%%

   public static void Main(String[] args)
   {
      %%__main_code__%%
   }
}
'''

#Lista de identificadores definidos
defined_ids=[]

#Cadena que contiene las importaciones a realizar
importstring=''

#Cadena que contiene las funciones definidas
funcstring=''

#Cadena de salida para compilar
outstring=""

#Flag para saber si un return_st es correcto
INSIDE_FUNC=0

#Reglas de precedencia de operadores
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIV'),
    ('right','UMINUS'),
    )

def p_program(t):
    '''program : import_section fundef_section order_list'''
    global outstring,cs_template
    if t[1]==None: t[1]=''
    t[0]=t[1] + t[2] + t[3]
    outstring=t[0]
    outstring+='System.Console.WriteLine("Adios");'
    t[0]=outstring
    #sustituir secciones
    cs_template=cs_template.replace("%%__name__%%",str(int(random.random()*1000000000)))
    cs_template=cs_template.replace("%%__imports__%%",importstring)
    cs_template=cs_template.replace("%%__functions__%%",funcstring)
    cs_template=cs_template.replace("%%__main_code__%%",outstring)
    print cs_template
    #escribirlo en un archivo
    f=open('salida.cs','w')
    f.write(cs_template)
    f.close()

def p_import_section(t):
    '''import_section : import_list
    | empty'''
    global INSIDE_FUNC,importstring
    t[0]=t[1] + '\n\n'
    #Establecer flag de entrada a definiciones de funciones
    INSIDE_FUNC=1
    importstring=t[0]
    t[0]=''

def p_import_list(t):
    '''import_list : IMPORTS idchain SEMI
    | IMPORTS idchain SEMI import_list'''
    global outstring
    if not t[1]:
        t[0]=''
    else:
        t[0]='using' + ' ' + t[2] + t[3] if len(t)==4 else 'using' + ' ' + t[2] + t[3] + t[4]
    #outstring+=t[0]


def p_idchain(t):
    '''idchain : ID DOT idchain
    | ID'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2] + t[3]


def p_fundef_section(t):
    '''fundef_section : funlist
    | empty'''
    global funcstring,INSIDE_FUNC
    if t[1]==None:
        t[0]=''
    else:
        t[0]=t[1]
    #outstring+=t[0]
    #Restablecer flag de definicion de funciones
    INSIDE_FUNC=0
    funcstring=t[0]
    t[0]=''

def p_funlist(t):
    '''funlist : fundef
    | fundef funlist'''
    t[0]= t[1] if len(t)==2 else t[1] + ' ' + t[2]

def p_fundef(t):
    '''fundef : FUNCTION ID LPAREN idlist RPAREN order_list END'''
    t[0]='public static Object ' + t[2] + ' ' + t[3]
    for el in t[4].split(','):
        t[0]+= "Object " + el + ','
    if t[0][-1]==',':t[0]=t[0][:-1]#quitar la ultima coma
    t[0]+=t[5] + '\n{\n' +t[6] + '\n}\n'
    

def p_idlist(t):
    '''idlist : ID
    | ID COMMA idlist
    | empty'''
    if t[1]==None:
        t[0]=''
    elif len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1]+t[2]+t[3]
    

def p_order_list(t):
    '''order_list : valid_st SEMI
    | valid_st SEMI order_list'''
    #Eliminar ";" de los bloques
    if len(t[1].strip())>=9 and t[1].strip()[:7]=='foreach':
        t[0]=t[1] if len(t)==3 else t[1] + t[3]    
    elif t[1].strip()[:2]=='if':
        t[0]=t[1] if len(t)==3 else t[1] + t[3]
    elif t[1].strip()[:2]=='do':
        t[0]=t[1] if len(t)==3 else t[1] + t[3]
    elif t[1].strip()[:3]=='for':
        t[0]=t[1] if len(t)==3 else t[1] + t[3]        
    elif t[1].strip()[:5]=='while':
        t[0]=t[1] if len(t)==3 else t[1] + t[3]
    elif t[1].strip()[:6]=='switch':
        t[0]=t[1] if len(t)==3 else t[1] + t[3]        
    else:
        t[0]=t[1] + t[2] if len(t)==3 else t[1] + t[2] + t[3]


def p_valid_st(t):
    '''valid_st : var_decl
    | assign_exp
    | incr_st
    | return_st
    | if_st
    | cond_st
    | while_st
    | loopwhen_st
    | foreach_st
    | for_st
    | empty
    | expr
    '''
    t[0]=t[1]


def p_var_decl(t):
    '''var_decl : SET ID
    | SET ID AS idchain'''
    #t[0]="object " + t[2] + "= new Object()\n"
    if t[2] in defined_ids:
        raise Exception('Error: el identificador "%s" ya esta definido'%t[2])
    defined_ids.append(t[2])
    if len(t)==3:
        t[0]= "object " + t[2]
    else:
        t[0]=t[4] + ' ' + t[2]
    
def p_assign_exp(t):
    '''assign_exp : assignable EQUAL condic_expr
    | assignable EQUAL condic_expr IF condic_expr ELSE condic_expr
    | assignable EQUAL LBRACK expr FOR ID IN ID RBRACK
    | assignable EQUAL LBRACK expr FOR ID IN ID RBRACK QUESTION condic_expr'''
    global l_name,l_counter
    if 'ArrayList list' in t[3]:
        t[0]=t[3] + t[1] + t[2] + getSequenceName(t[3])
    elif len(t)==8: #condic_assign, se transforma en in if-then-else
        t[0]= 'if (' + t[5] + ')\n{\n' + t[1] + '=' + t[3] + ';\n}\nelse\n{\n' + t[1] + '=' + t[7] + ';\n}\n'
    elif len(t)==10: #lista por comprension
        name=l_name + str(l_counter)
        l_counter+=1
        t[0]='ArrayList ' + name + '= new ArrayList();foreach(var ' + t[6] + ' in ' + t[8] + ')\n{\n'
        t[0]+='\n' + name + '.Add(' + t[6] + ');\n}\n'
        t[0]+= t[1] + '=' + name + ';\n'
    elif len(t)==12: #lista por comprension con condicional
        name=l_name + str(l_counter)
        l_counter+=1
        t[0]='ArrayList ' + name + '= new ArrayList();foreach(var ' + t[6] + ' in ' + t[8] + ')\n{\n'
        t[0]+='\nif(' + t[11] + ')\n{\n' + name + '.Add(' + t[6] + ');\n}\n\n}\n'
        t[0]+= t[1] + '=' + name + ';\n'        
    else:
        t[0]=t[1] + t[2] + t[3]

def p_assignable(t):
    '''assignable : idchain'''
    t[0]=t[1]

def p_return_st(t):
    '''return_st : RETURN expr'''
    global INSIDE_FUNC
    if INSIDE_FUNC==0:
        raise Exception('Error: Sentencia "return" fuera de una definicion de funcion')
    t[0]=t[1] + ' ' + t[2]

def p_incr_st(t):
    '''incr_st : idchain INCR'''
    t[0]=t[1] + t[2]    


def p_if_st(t):
    '''if_st : IF condic_expr THEN order_list END
    | IF condic_expr THEN order_list ELSE order_list END'''
    if len(t)==6:
        t[0]='\n' + t[1] + '(' + t[2] + ')' + t[3] + '\n{\n' + t[4] + '\n}\n'
    else:
        t[0]='\n' + t[1] + '(' + t[2] + ')' + t[3] + '\n{\n' + t[4] + '\n}\n' + t[5] + '\n{\n' + t[6] + '\n}\n'


def p_cond_st(t):
    '''cond_st : COND expr case_list ELSE DO order_list END'''
    t[0]= '\nswitch(' + t[2] + ')\n{\n' +  t[3]  + '\ndefault:\n{\n' + t[6] + '\nbreak;\n}\n}\n'


def p_case_list(t):
    '''case_list : CASE expr DO order_list
    | CASE expr DO order_list case_list'''
    t[0]=t[1] + ' ' + t[2] + ' :\n{\n' + t[3] + t[4] + '\nbreak;\n}\n' if len(t)==5 else t[1] + ' ' + t[2] + ' :\n{\n' + t[3] + t[4] + '\nbreak;\n}\n' + t[5]


def p_while_st(t):
    '''while_st : WHILE condic_expr DO order_list END'''
    t[0]='\n' + t[1] + '(' + t[2] + ')' + t[3] + '\n{\n' + t[4] + '\n}\n'

def p_loopwhen_st(t):
    '''loopwhen_st : LOOP order_list WHEN condic_expr'''
    t[0]='do\n{\n' + t[2] + '\n}\nwhile(' + t[4] + ')\n'

def p_for(t):
    '''for_st : FOR ID EQUAL expr COMMA condic_expr COMMA incr_st DO order_list END'''
    t[0]= t[1] + '(' + t[2] + '=' + t[4] + ';' + t[6] + ';' + t[8] + ')\n{\n' + t[10] + '\n}\n' 


def p_foreach_st(t):
    '''foreach_st : FOREACH ID IN ID DO order_list END'''
    t[0]= t[1] + '(var ' + t[2] + ' ' + t[3] + ' ' + t[4] + ')\n{\n' + t[6] + '\n}\n'

 
def p_pair(t):
    '''pair : expr COLON expr'''
    t[0]=t[1] + t[2] + t[3]

def p_pair_list(t):
    '''pair_list : pair COMMA pair_list
    | pair
    | empty'''
    t[0]=t[1] if len(t)==2 else t[1] + t[2] + t[3]

def p_condic_expr(t):
    '''condic_expr : condic_expr OR condic_expr
    | and_exp'''
    t[0]=t[1] if len(t)==2 else t[1] + "||" + t[3]
   
def p_and_exp(t):
    '''and_exp : and_exp AND not_exp
    | not_exp'''
    t[0]=t[1] if len(t)==2 else t[1] + "&&" + t[3]
   
def p_not_exp(t):
    '''not_exp : NOT condic_expr
    | LPAREN condic_expr RPAREN
    | bool_exp'''
    if len(t)==2:
        t[0]=t[1]
    elif len(t)==3:
        t[0]="!" +t[2]
    else:
        t[0]=t[2]

def p_bool_exp(t):
    '''bool_exp : expr relop expr
    | expr'''
    #| expr IS REGEX expr'''
    t[0]=t[1] if len(t)==2 else t[1] + t[2] + t[3]

def p_relop(t):
    '''relop : EQ
    | GT
    | GE
    | LT
    | LE
    | NE
    | IN'''
    t[0]=t[1]


def p_expr(t):
    '''expr : expr PLUS termino
    | expr MINUS termino
    | MINUS expr %prec UMINUS
    | termino      
    '''
    if len(t)==2:
        t[0]=t[1]
    elif len(t)==3:
        t[0]=t[1]+t[2]
    else:
        t[0]=t[1] + t[2] + t[3]    

def p_expr_list(t):
    '''expr_list : expr
    | expr COMMA expr_list'''
    t[0]=t[1] if len(t)==2 else t[1] + t[2] + t[3]

def p_termino(t):
    '''termino : termino TIMES pot_factor
    | termino DIV pot_factor
    | pot_factor'''
    t[0]=t[1] if len(t)==2 else t[1] + t[2] + t[3]
      
    
def p_pot_factor(t):
    '''pot_factor : factor EXP factor
    | factor'''
    t[0]=t[1] if len(t)==2 else t[1] + t[2] + t[3]
    

def p_factor(t):
    '''factor :  assignable
    | LPAREN expr RPAREN   
    | NUMBER  
    | STRING
    | NULL
    | ID
    | funcall
    | sequence
    | array
    | dict
    | expr accesors
    | ID accesors'''
    t[0]=t[1] if len(t)==2 else t[1] + t[2]


def p_sequence(t):
    '''sequence : LBRACK RBRACK
    | LBRACK expr_list RBRACK'''
    global l_name,l_counter
    elems=findElements(t[2])
    name=l_name + str(l_counter)
    l_counter+=1
    t[0]="ArrayList " + name + " = new ArrayList();\n"
    for item in elems:
        if "new ArrayList();" in item:
            t[0]+=item
            t[0]+=name + '.Add(' + getSequenceName(item) + ');\n'
        elif "Object[] " in item:
            t[0]+=item
            t[0]+=name + '.Add(' + getSequenceName(item) + ');\n'
        else:
            t[0]+=name + ".Add((object)" + item + ");\n"

def p_array(t):
    '''array : LCURLY expr_list RCURLY'''
    global a_counter,a_name
    elems=findElements(t[2])
    name=a_name + str(a_counter)
    a_counter+=1
    t[0]="Object[] " + name + " = {\n"
    for item in elems:
        t[0]+="(object)" + item + ",\n"
    t[0]+="};\n"


def p_dict(t):
    '''dict : LCURLY pair_list RCURLY'''
    t[0]=t[1] + t[2] + t[3]
    print 'valor de t[0] en dict: %s' %t[0]     


def p_accesors(t):
    '''
    accesors : LBRACK expr RBRACK accesors
    | LBRACK expr RBRACK
    '''
    t[0]=t[1] + t[2] + t[3] if len(t)==4 else t[1]+t[2]+t[3]+t[4]

    
def p_funcall(t):
    '''funcall : idchain LPAREN expr_list RPAREN
    | idchain LPAREN RPAREN'''
    if len(t)==4:
        t[0]=t[1]+t[2]+t[3]
    else:
        t[0]=t[1] + t[2] + t[3] + t[4]

    
def p_empty(t):
    '''
    empty : 
    '''
    t[0]=''


# Error rule for syntax errors
def p_error(t):
    print 'Localizado un error'
    print 'Error evaluando Token: %s' %repr(t)
    print "Error de sintaxis en la entrada!"


# Build the parser
#parser=yacc.yacc(debug=0)

def parserFactory():
    #Generamos el parser con picklefile para evitar el parsetab.py!!
    return yacc.yacc(debug=1,picklefile='parsetab.p')#Poner a debug=0 en produccion

parser=parserFactory()


if __name__=='__main__':
    program='''
    imports System;
    imports System.Windows.Forms;
    imports System.Runtime.InteropServices;
    function factorial(numero)
      set r;
      set f;
      return r;
    end
    function userfunc(x,y,z,otras)
      set k;
      set l;
      return r;
    end    
    set a;
    set b;
    set c;
    set y as System.Windows.File;
    b=[2,3,4,"tres,cuatro",[[6,6],{"A","B"}]];
    c=["[]dfg",b];
    while (c==9) do 
    if b<3 then a=0; b=9; end;
    c=0;
    end;
    a=b if b<5 else c;
    c++;
    a--;
    foreach a in b do
    c++;
    c=45;
    end;
    loop
    c=3;b=0;
    when a<c;
    for x=0,x<7,x++ do
    a=b;
    b--;
    end;
    cond b
    case 1 do c=1;
    case 2 do c=2;
    case 3 do c=3;
    else do c=null;
    end;
    l=[x for x in b];
    m=[g for g in b ? g<67 and c>8];
    '''
    program='''
    set l as ArrayList;
    l=[1,2,3,4];
    foreach i in l do
       System.Console.WriteLine(i);
    end;
    System.Console.WriteLine("Terminado!");
    '''
    parser.parse(program)
    print 'Trabajo terminado!'
        

