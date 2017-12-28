from __future__ import division
#!Python

'''
class Pet
            {
                public string Name { get; set; }
                public int Age { get; set; }
            }

            // Uses method-based query syntax.
            public static void GroupByEx1()
            {
                // Create a list of pets.
                List<Pet> pets =
                    new List<Pet>{ new Pet { Name="Barley", Age=8 },
                                   new Pet { Name="Boots", Age=4 },
                                   new Pet { Name="Whiskers", Age=1 },
                                   new Pet { Name="Daisy", Age=4 } };

                // Group the pets using Age as the key value 
                // and selecting only the pet's Name for each value.
                IEnumerable<IGrouping<int, string>> query =
                    pets.GroupBy(pet => pet.Age, pet => pet.Name);

                // Iterate over each IGrouping in the collection.
                foreach (IGrouping<int, string> petGroup in query)
                {
                    // Print the key value of the IGrouping.
                    Console.WriteLine(petGroup.Key);
                    // Iterate over each value in the 
                    // IGrouping and print the value.
                    foreach (string name in petGroup)
                        Console.WriteLine("  {0}", name);
                }
            }

            /*
             This code produces the following output:

             8
               Barley
             4
               Boots
               Daisy
             1
               Whiskers
            */

'''            




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

#cadena auxiliar para definiciones auxiliares
aux_string=''


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
    for it in re.findall(r'\([^\)]*?\)',cad): #Parentesis de funciones
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
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Data;
using System.Data.SqlClient;
using System.Reflection;
using System.Runtime.InteropServices;

//user imports
%%__imports__%%


//COM
public static class ComObjectManager: Object
	{
		
		//Crear una instancia del objeto a partir del progId
		public static Object fromProgID(string progid)
		{
			Type comType = Type.GetTypeFromProgID (progid, true);
			return Activator.CreateInstance (comType);
		}
		
		//Invocar un metodo del objeto (estatico)
		public static Object InvokeMethod(Object obj,string name,Object[] args)
		{
				return obj.GetType().InvokeMember(name,
    			BindingFlags.InvokeMethod,
    			Type.DefaultBinder, obj, args);
		}	
		//Invocar el set de una propiedad Com
		public static void SetComProperty(Object obj,string name,object value)
		{
				Object[] args=new Object[] {value};
				obj.GetType().InvokeMember(name,
    			BindingFlags.SetProperty,
    			Type.DefaultBinder, obj, args);
		}
		//Obtener el valor de una propiedad
		public static Object GetComProperty(Object obj,string name)
		{
				return obj.GetType().InvokeMember(name,
    			BindingFlags.GetProperty,
    			null, obj, null);
		}
		//Obtener el valor de una propiedad con argumentos
		public static Object GetComProperty(Object obj,string name,object[] args)
		{
				return obj.GetType().InvokeMember(name,
    			BindingFlags.GetProperty,
    			null, obj, args);
		}		
	
	}

//Globals
public static class Globals
{
}

//Main class
public class Minimal%%__name__%%
{

public static T CastObject<T>(object input, T example)
{
    return (T) input;
}
   %%__functions__%%

   public static void Main(String[] args)
   {
      %%__main_code__%%
   }
}
'''

#Tabla de identificadores definidos-tipo
defined_ids={}

#Tabla de funciones de sistema
system_func={}

#Tabla de funciones definidas por el usuario
user_funcs={}

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
    #print 't[3] en program: %s' % t[3]
    if t[1]==None: t[1]=''
    t[0]=t[1] + t[2] + t[3]
    outstring+=t[0]
    #print 'outstring: %s' % outstring
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
    global importstring
    if not t[1]:
        t[0]=''
    else:
        t[0]='using' + ' ' + t[2] + t[3] if len(t)==4 else 'using' + ' ' + t[2] + t[3] + t[4]
    importstring+=t[0]


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
    '''fundef : FUNCTION ID LPAREN idfunlist RPAREN COLON order_list END
    | FUNCTION ID LPAREN idfunlist RPAREN  AS idchain COLON order_list END'''
    global user_funcs
    if len(t)==9:
        t[0]='public static Object ' + t[2] + ' ' + t[3]
        for el in t[4].split(','):
            if ' ' in el:
                t[0]+= ' ' + el + ','
            else:
                t[0]+= " Object " + el + ','
        if t[0][-1]==',':t[0]=t[0][:-1]#quitar la ultima coma
        t[0]+=t[5] + '\n{\n' +t[7] + '\n}\n'            
    else:
        t[0]='public static ' + t[7] + ' ' + t[2] + ' ' + t[3]
        for el in t[4].split(','):
            if ' ' in el:
                t[0]+= ' ' + el + ','
            else:
                t[0]+= " Object " + el + ','
        if t[0][-1]==',':t[0]=t[0][:-1]#quitar la ultima coma
        t[0]+=t[5] + '\n{\n' +t[9] + '\n}\n'
    user_funcs[t[1]]='user'
    

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
        

def p_idfunlist(t):
    '''idfunlist : idfunitem
    | idfunitem COMMA idfunlist
    | empty'''
    if t[1]==None:
        t[0]=''
    elif len(t)==2:
        t[0]= t[1]
    else:
        t[0]=t[1] + t[2] +  t[3]


def p_idfunitem(t):
    '''idfunitem : ID
    | ID AS idchain'''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[3]+ ' ' +t[1]      
    

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
        if len(t)==3 and t[1]:
            t[0]=t[1] + t[2]
        else:
            if t[1]:
                t[0]=t[1] + t[2] + t[3]
            else:
                if len(t)==4:
                    t[0]=t[3]
                else:
                    t[0]=t[1]
            


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
    | expr_list
    | verbatim_st
    | create_st
    | com_st
    '''
    t[0]=t[1]


def p_com_st(t):
    '''com_st : COM NEW idchain
    | COM idchain accesors
    | COM funcall
    | COM idchain'''
    if t[2]=='new': #com new idchain
        t[0]='ComObjectManager.fromProgID(\"' + t[3] + '\")'
    elif len(t)==4: #accesors
        t[0]= t[2] + t[3]
    elif not '(' in t[2]: #set property
        prop=t[2].split('.')[-1]
        prefix='.'.join(t[2].split('.')[:-1])
        t[0]='ComObjectManager.GetComProperty(' + prefix+ ', \"' + prop + '\")'
    else: #invoke member
        t[0]=t[2]
    

def p_verbatim_st(t):
    '''verbatim_st : VERBATIM STRING'''
    t[0] =t[2] 

def p_var_decl(t):
    '''var_decl : SET ID
    | SET ID AS idchain'''
    #t[0]="object " + t[2] + "= new Object()\n"
    global outstring
    if t[2] in defined_ids:
        raise Exception('Error: el identificador "%s" ya esta definido'%t[2])
    if len(t)==3:
        t[0]= "object " + t[2]
        defined_ids[t[2]]='object'
    else:
        t[0]=t[4] + ' ' + t[2]
        defined_ids[t[2]]=t[4]
    outstring+=t[0] + ';\n'
    t[0]=''
    
def p_assign_exp(t):
    '''assign_exp : assignable EQUAL expr_list
    | assignable EQUAL expr_list IF expr_list ELSE expr_list
    | assignable EQUAL anonym_st
    | assignable EQUAL com_st'''
    global l_name,l_counter,aux_string,outstring
    #Cambio para ver si assignable es un objeto COM
    if t[1][0]=='@':
        t[1]=t[1][1:]#quitar flag
        prop=t[1].split('.')[-1]
        prefix='.'.join(t[1].split('.')[:-1])
        t[0]='ComObjectManager.SetComProperty(' + prefix + ',\"' + prop + '\",' + t[3] + ')'
    elif 'System.Collections.Generics.List list' in t[3]:
        t[0]=t[3] + t[1] + t[2] + getSequenceName(t[3])
    elif '=>' in t[3]: #anonym_st
        t[0]=t[1] + ' ' + t[2] + t[3]
    elif '=' in t[3]: #filter-like
        epos=t[3].find('=')
        idn=t[3][:epos]
        #t[0]=t[3][:-1] + '.ToList();\n' + t[1] + t[2] + idn
        t[0]=t[3][:-1] + ';\n' + t[1] + t[2] + idn
    elif len(t)==8: #condic_assign, se transforma en in if-then-else
        t[0]= 'if (' + t[5] + ')\n{\n' + t[1] + '=' + t[3] + ';\n}\nelse\n{\n' + t[1] + '=' + t[7] + ';\n}\n'
    else:
        t[0]=t[1] + t[2] + t[3]    
    if aux_string!='':
        outstring+=aux_string
        outstring+=t[0] + ';'
        aux_string=''
    elif aux_string=='' and t[0]!='':
        outstring+=t[0] + ';'
        t[0]=''
    else:
        t[0]=''


def p_assignable(t):
    '''assignable : idchain
    | COM idchain'''
    if len(t)==3:
        if not '.' in t[2]: #nombre de variable. Comprobar que existe
            if not t[2] in defined_ids:
                raise Exception('Error: El identificador "%s" se usa sin haberse definido'%t[2])
        t[0]='@' + t[2]
    else:
        if not '.' in t[1]: #nombre de variable. Comprobar que existe
            if not t[1] in defined_ids:
                raise Exception('Error: El identificador "%s" se usa sin haberse definido'%t[1])        
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
    '''pair : expr COLON condic_expr'''
    t[0]=t[1] + t[2] + t[3]

def p_pair_list(t):
    '''pair_list : pair COMMA pair_list
    | pair
    | empty'''
    t[0]=t[1] if len(t)==2 else t[1] + t[2] + t[3]

def p_condic_expr(t):
    '''condic_expr : condic_expr OR condic_expr
    | and_exp'''
    t[0]=t[1] if len(t)==2 else t[1] + " || " + t[3]
   
def p_and_exp(t):
    '''and_exp : and_exp AND not_exp
    | not_exp'''
    t[0]=t[1] if len(t)==2 else t[1] + " && " + t[3]
   
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
    global aux_string
    if len(t)==2:
        t[0]=t[1]
    elif len(t)==3:
        t[0]=t[1]+t[2]
    else:
        t[0]=t[1] + t[2] + t[3]

def p_expr_list(t):
    '''expr_list : expr_list_item
    | expr_list_item COMMA expr_list'''
    global aux_string,outstring
    #print 'EN EXPR_LIST CON t[1]: %s' % t[1]
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[1] + t[2] + t[3]
    if aux_string!='': #REVISAR ESTO!
        outstring+=aux_string
        aux_string=''


def p_expr_list_item(t):
    '''expr_list_item : condic_expr
    | sequence
    | array
    | dict
    | dictobj
    | funcall
    | lambda_st
    | pylike_st
    | filter_st
    | map_st
    | slice_st'''
    t[0]=t[1]


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
    | LPAREN condic_expr RPAREN   
    | NUMBER  
    | STRING
    | NULL
    | expr accesors
    | cast_st
    | text_st
    | update_st
    | split_st
    | match_st'''
    #print 'EN FACTOR CON T[1]:%s y len(t):%s' % (t[1],len(t))
    if len(t)==2:
        t[0]=t[1]
    elif len(t)==3:
        t[0]=t[1] + t[2]
    else:#(expr)
        t[0]=t[1] + t[2] + t[3]



def p_funcall(t):
    '''funcall : idchain LPAREN expr_list RPAREN
    | idchain LPAREN RPAREN'''
    if len(t)==4:
        t[0]=t[1]+t[2]+t[3]
    else:
        t[0]=t[1] + t[2] + t[3] + t[4]
   


def p_cast_st(t):
    '''cast_st : LPAREN idchain RPAREN expr_list'''
    t[0]=t[1] + t[2] + t[3] + t[4]
    
    
def p_sequence(t):
    '''sequence : LBRACK RBRACK
    | LBRACK expr_list RBRACK
    | LBRACK expr_list RBRACK AS idchain'''
    global l_name,l_counter,aux_string
    elems=findElements(t[2])
    name=l_name + str(l_counter)
    l_counter+=1
    prefix=''#??
    if len(t)!=6:
        t[0]="\n\nSystem.Collections.Generic.List<object> " + name + " = new \n\nSystem.Collections.Generic.List<object>();\n"
    else:
        t[0]="\n\nSystem.Collections.Generic.List<" + t[5] + "> " + name + " = new \n\nSystem.Collections.Generic.List<" + t[5] + ">();\n"
    for item in elems:
        if '=' in item:#REVISAR ESTO MUY BIEN!!!!
            item=item.strip('(').strip(')')
            aux_string+=item
            t[0]+=name + ".Add(" + item.split('=')[0] + ");\n"
        else:
            t[0]+=name + ".Add(" + item + ");\n"
    aux_string+=t[0]
    t[0]=name

def p_array(t):
    '''array : LCURLY expr_list RCURLY
    | LCURLY expr_list RCURLY AS idchain'''
    global a_counter,a_name,aux_string
    elems=findElements(t[2])
    name=a_name + str(a_counter)
    a_counter+=1
    if len(t)==4:
        t[0]="Object[] " + name + " = {\n"
    else:
        t[0]= t[5] + "[] " + name + " = {\n"
    for item in elems:
        t[0]+=item + ",\n"
    t[0]+="};\n"
    aux_string+=t[0]
    t[0]=name


def p_dict(t):
    '''dict : LCURLY pair_list RCURLY'''
    global d_name,d_counter,aux_string
    elems=findElements(t[2])
    name=d_name + str(l_counter)
    d_counter+=1
    prefix=''
    t[0]="System.Collections.Generic.Dictionary<object,object> " + name + " = new System.Collections.Generic.Dictionary<object,object>();\n"
    for item in elems:
        parts=item.split(':')
        t[0]+=name + ".Add(" + parts[0] + ',' + parts[1] +  ");\n"
    aux_string+=t[0]
    t[0]=name       


def p_accesors(t):
    '''
    accesors : LBRACK expr RBRACK accesors
    | LBRACK expr RBRACK
    '''
    t[0]=t[1] + t[2] + t[3] if len(t)==4 else t[1]+t[2]+t[3]+t[4]


def p_dictobj(t):
    '''dictobj : LCURLY objpair_list RCURLY'''
    global o_name,o_counter,aux_string
    name=o_name + str(o_counter)
    o_counter+=1
    aux_string+= '\nvar ' + name + '= new ' + t[1] + t[2] + t[3] + ';\n'
    t[0]=name


def p_objpair(t):
    '''objpair : ID EQUAL condic_expr'''
    t[0]=t[1] + t[2] + t[3]

def p_objpair_list(t):
    '''objpair_list : objpair COMMA objpair_list
    | objpair
    | empty'''
    t[0]=t[1] if len(t)==2 else t[1] + t[2] + t[3]


def p_anonym_st(t):
    '''anonym_st : FUNCTION LPAREN idlist RPAREN COLON order_list END'''
    t[0]=t[2] + t[3] + t[4] + ' => {' + t[6] + '}\n'  

    
def p_lambda_st(t): #?
    '''lambda_st : LPAREN idlist RPAREN COLON order_list'''
    t[0]=t[1] + t[2] + t[3] + ' => ' + t[5].strip(';')


def p_filter_st(t):
    '''filter_st : FILTER lambda_st IN expr_list
    | FILTER lambda_st IN expr_list ARROW idchain'''
    global l_name,l_counter,aux_string
    elems=findElements(t[4])
    name=l_name + str(l_counter)
    l_counter+=1
    if len(t)==5:
        t[0]="\n\nSystem.Collections.Generic.List<object> " + name + " = new System.Collections.Generic.List<object>();\n"
    else:
         t[0]="\n\nSystem.Collections.Generic.List<" + t[6] + "> " + name + " = new System.Collections.Generic.List<" + t[6] + ">();\n"
    for item in elems:
        if "list" in item:
            #t[0]+=item
            t[0]+=name + '.AddRange(' + item + ');\n'
        elif "Object[] " in item:
            t[0]+=item
            t[0]+=name + '.AddRange(' + getSequenceName(item) + ');\n'
        else:
            t[0]+=name + ".Add(" + item + ");\n"
    t[0]+= name + '= ' + name + '.Where(' + t[2] + ').ToList();'
    aux_string+=t[0]    
    t[0]=name

def p_map_st(t):
    '''map_st : MAP lambda_st IN expr_list
    | MAP lambda_st IN expr_list ARROW idchain'''
    global l_name,l_counter,aux_string
    elems=findElements(t[4])
    name=l_name + str(l_counter)
    l_counter+=1
    if len(t)==5:
        t[0]="\n\nSystem.Collections.Generic.List<object> " + name + " = new System.Collections.Generic.List<object>();\n"
    else:
         t[0]="\n\nSystem.Collections.Generic.List<" + t[6] + "> " + name + " = new System.Collections.Generic.List<" + t[6] + ">();\n"    
    for item in elems:
        if "list" in item:
            #t[0]+=item
            t[0]+=name + '.AddRange(' + item + ');\n'
        elif "Object[] " in item:
            t[0]+=item
            t[0]+=name + '.AddRange(' + getSequenceName(item) + ');\n'
        else:
            t[0]+=name + ".Add(" + item + ");\n"
    t[0]+= name + '= ' + name + '.Select(' + t[2] + ').ToList();'
    aux_string+=t[0]    
    t[0]=name
    


def p_pylike_st(t):
    '''
    pylike_st : ID IN expr_list IF condic_expr'''
    global l_name,l_counter,aux_string
    elems=findElements(t[3])
    name=l_name + str(l_counter)
    l_counter+=1
    t[0]="\n\nSystem.Collections.Generic.List<object> " + name + " = new System.Collections.Generic.List<object>();\n"
    for item in elems:
        if "new System.Collections.Generic.List<;" in item:
            t[0]+=item
            t[0]+=name + '.AddRange(' + getSequenceName(item) + ');\n'
        elif "Object[] " in item:
            t[0]+=item
            t[0]+=name + '.AddRange(' + getSequenceName(item) + ');\n'
        else:
            t[0]+=name + ".Add(" + item + ");\n"
    t[0]+= name + '= ' + name + '.Where(' + t[1] + '=>' +  t[5] + ').ToList();'            
    aux_string+=t[0]
    t[0]=name



def p_slice_st(t):
    '''
    slice_st : LBRACK expr COLON expr RBRACK IN expr_list'''
    global l_name,l_counter,aux_string
    elems=findElements(t[7])
    name=l_name + str(l_counter)
    l_counter+=1
    t[0]="\n\nSystem.Collections.Generic.List<object> " + name + " = new System.Collections.Generic.List<object>();\n"
    for item in elems:
        if "new System.Collections.Generic.List<;" in item:
            t[0]+=item
            t[0]+=name + '.AddRange(' + getSequenceName(item) + ');\n'
        elif "Object[] " in item:
            t[0]+=item
            t[0]+=name + '.AddRange(' + getSequenceName(item) + ');\n'
        else:
            t[0]+=name + ".Add(" + item + ");\n"
    aux_string+=t[0]
    t[0]=''
    t[0]+= name + '= ' + name + '.GetRange(' + t[2] + ',' + t[4] + ');'

    
def p_create_st(t):
    '''create_st : CREATE FILES expr_list
    | CREATE DIRS expr_list'''
    global outstring
    t[0]=''
    elems=findElements(t[3])
    if t[2]=="dirs":
        for item in elems:
            outstring+='System.IO.Directory.CreateDirectory(' + item + ');\n'
    else:
        for item in elems:
            outstring+='System.IO.File.Create(' + item + ');\n'


def p_text_st(t):
    '''text_st : TEXT FROM expr_list'''
    global aux_string,t_name,t_counter
    elems=findElements(t[3])
    name=t_name + str(t_counter)
    t_counter+=1
    aux_string+= 'string ' + name + '="";\n'
    for item in elems:
        aux_string+= '\nif (System.IO.File.Exists(' + item + '))\n'
        aux_string+= '{' + name + '+=System.IO.File.ReadAllText(' + item + ');\n}'
        aux_string+= 'else{\n ' + name + '+= ' + item + ';}\n'
    t[0]=name


def p_update_st(t):
    '''update_st : UPDATE expr_list SET expr EQUAL expr'''
    global aux_string,u_counter,u_name,re_name,re_counter
    elems=findElements(t[2])
    name=u_name + str(u_counter)
    re=re_name + str(re_counter)
    u_counter+=1
    re_counter+=1
    old_pat=t[4]
    new_pat=t[6]
    aux_string+= 'string ' + name + '="";\n'
    aux_string+='Regex ' + re + ' =new Regex(' + new_pat + ');\n'
    for item in elems:
        aux_string+= '\nif (System.IO.File.Exists(' + item + '))\n'
        aux_string+= '{' + name + '+=System.IO.File.ReadAllText(' + item + ');\n'
        aux_string+= name + '= ' + re_name + '.Replace(' + name + ',' + old_pat + ');\n'
        aux_string+= 'System.IO.File.WriteAllText(' + item + ',' + name + ');}\n'
        aux_string+= 'else{\n' + name + '= ' + re_name + '.Replace(' + name + ',' + old_pat + ');}\n'
    t[0]=name


def p_split_st(t):
    '''split_st : SPLIT expr IN expr'''
    global aux_string,s_counter,s_name
    name=s_name + str(s_counter)
    s_counter+=1
    pat=t[2]
    aux_string+= 'string[] ' + name + ';\n'
    aux_string+= '\nif (System.IO.File.Exists(' + t[24] + '))\n'
    aux_string+= '{' + name + ' = Regex.Split(System.IO.File.ReadAllText(' + t[4] + '),' + pat + ');}\n'
    aux_string+= 'else{\n' + name + '=Regex.Split(' + t[4] + ',' + pat + ');}\n'
    t[0]=name

def p_match_st(t):
    '''match_st : MATCH expr IN expr'''
    global aux_string,m_counter,m_name,aux_counter,aux_name
    name=m_name + str(m_counter)
    m_counter+=1
    aux=aux_name + str(aux_counter)
    aux_counter+=1
    pat=t[2]
    aux_string+= 'System.Collections.Generic.List<string> ' + name + '=new System.Collections.Generic.List<string>();\n'
    aux_string+= '\nif (System.IO.File.Exists(' + t[4] + '))\n'
    aux_string+= '{Match ' + aux + ' = Regex.Match(System.IO.File.ReadAllText(' + t[4] + '),' + pat + ');\n'
    aux_string+= 'while(' + aux + '.Success){\nfor(int i=0;i<' + aux + '.Groups.Count;i++)\n{'
    aux_string+= name + '.Add(' + aux + '.Groups[i].Value);}\n' + aux + '= ' + aux + '.NextMatch();}}\n'
    aux_string+= 'else\n'
    aux_string+= '{Match ' + aux + ' = Regex.Match(' + t[4] + ',' + pat + ');\n'
    aux_string+= 'while(' + aux + '.Success){\nfor(int i=0;i<' + aux + '.Groups.Count;i++)\n{'
    aux_string+= name + '.Add(' + aux + '.Groups[i].Value);}\n' + aux + '= ' + aux + '.NextMatch();}\n}\n'    
    t[0]=name     
    
    
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


#Regex.Replace(name, pattern, String.Empty)

if __name__=='__main__':
    program='''
    set f as System.Collections.Generic.Dictionary<object,object>;
    set g as System.Collections.Generic.List<object>;
    set d;
    f={"x":"asd","y":"tenga","w":"ose","z":"binga"};
    foreach i in f do
      System.Console.WriteLine(i.ToString());
    end;    
    System.Console.ReadKey();
    set gg as System.Collections.Generic.List<object>;
    d={id=45,txt="dfg"};
    gg=[{id=1,txt="xxx"},{id=2,txt="yyy"},{id=3,txt="zzz"}];
    foreach i in gg do
      System.Console.WriteLine(i,{id=0,txt=""},{id=0,txt=""});
    end;      
    System.Console.ReadKey();
    func(i,[9]);
    '''
    program='''
    function saluda(m as string,k,l,v as int) as System.IO.File:
      print("hola " + m);
    end
    d=[y,78,"w",fun(i,{1,2,3},[4,5],{f:3,g:h},b[y][z])];
    {{d="tres",a=4},{d="dos",a=0}, (x,y) : x++};
    l= x in [2,3,4,5,6,7,8],9,10 if x>4 and x<9;
    m= filter (x):x>5 or x==0; in [1,2,3,4],5,6;
    n= [0:3] in [1,2,3,4],5,6;
    p=function (g): print(g);g++; end; 
    '''
    program='''
    set f as string;
    set f2;
    set t as string;
    f="dir3";
    f2="dir3/file3.txt";
    create dirs "dir1","dir2",f;
    create files "dir1/file1.txt","dir2/file2.txt",(string)f2;
    t=text from "Hola ","a todos:","file1.txt";
    t=update "file1.txt" set "perro"="gato";
    t=split " " in "file1.txt";
    t= match "perr" in "perro de roque";
    System.Console.WriteLine(t);
    System.Console.ReadKey();
    '''
    program='''
    set t as System.Collections.Generic.List<string>;
    t= match "perro de roque perrete y perraco" with "p[a-z]+";
    foreach item in t do
      System.Console.WriteLine(item);
    end;
    System.Console.ReadKey();
    '''
    program='''
    set t as System.Collections.Generic.List<int>;
    set q as System.Collections.Generic.List<string>;
    t=map (x):x*x; in filter (z):z<6; in filter (y):y<7; in [1,2,3,4,5,6] as int,[6,7,8] as int ->int ->int ->int;
    q=match "perr" in "perro de roque";
    foreach item in t do
       System.Console.WriteLine(item);
    end;
    foreach i in q do
       System.Console.WriteLine(i);
    end;    
    '''
    program='''
    set a;
    set b;
    set c;
    set d;
    a= com new Excel.Application;
    b= com a.worksheets.ActiveWorksheet;
    c= com a.WorkBooks[2];
    d= com a.Visible;
    com a.Visible=1;
	MessageBox.Show("Hi world from minimal#!!");
    '''
    parser.parse(program)
    print 'Trabajo terminado!'
        

