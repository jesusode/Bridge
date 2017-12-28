#Esquema para traduccion de minimal a C++
import re

tempname='cpptemp_'
tempcont=0


def findElements2(cad):
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

susts={'and':'&&', 'or':'||', 'not':'!'}
#Contador auxiliar para nombres
cont=0

def indent(code):
    indent='    '
    val=''
    for it in code.split('\n'):
        val+=indent + it + '\n'
    #val+='\n'
    return val


#Funcion de utilidad para detectar prefijos de interes en los tipos de funciones o variables.
#Reglas: se acepta static y const en cualquier orden
#        aunque solo es correcto en C++ static const
def process_prefix(var,pref='_',target=['static','const']):
    parts=var.split(pref)
    prefs=''
    if len(parts)==1:
        return var
    else:
        for item in target:
            if parts[0]==item: 
                prefs+= item + ' '
                parts=parts[1:]
    if prefs!='':
        return prefs + ' ' + pref.join(parts)
    else:
        return pref.join(parts)


def vartable(vdict):#??
    indent='    '
    val=''
    print vdict
    for it in vdict.split(','):
        val+=indent + 'var ' +  it + ';\n'
    val+='\n'
    return val   

def process_native(code):#Done
    if '.h' in code:
        return '#include "' + code + '"\n'
    else:
        return "#include<" + code + ">\n"

def process_run_native(code):#Done
    raise Exception("Error: C++ no soporta evaluacion del codigo en runtime!")

def process_return(code):#Done
    return ' return ' +  code

def process_var_decl(ids, tp, val=''):
    #print 'en var_decl: ids=%s tp=%s val=%s'%(ids,tp,val)
    code=''
    if tp=='': val='null'
    #Cambio para soportar const y definicion de arrays como C
    tp=process_prefix(tp)
    array_str=''
    if tp[-2:]=='[]':
        array_str='[]'
        tp=tp[:-2]
    for item in ids.split(','):
        if tp=='ignore':
            continue
        elif val!='':
            code+=tp + ' ' + item + array_str +  ' = ' + val + ';\n'
        else:
            code+=tp + ' ' + item + array_str +  ';\n'
    #print 'code: %s' % code
    return code

def process_array(elems,_typ,id=''):#REVISAR!!!!!!
    _typ= process_prefix(_typ)
    if id!='':
        return 'std::array<' + _typ + ',' + str(len(elems)) + '> ' + id +  ' = {' + ','.join(elems) + '}'
    else:
        return 'std::array<' + _typ + ',' + str(len(elems)) + '>{' + ','.join(elems) + '}'

#Revisar el cast de los elementos. Si no se pone no deduce bien el tipo
#Si se pone ver si da problemas con los elementos y las listas anidadas
def process_sequence(elems,_type='void* '):
    #print 'elems: %s' % elems
    is_any_list=0
    if _type=="any":
        is_any_list=1
    _type=process_prefix(_type)
    if elems[0]==']': #Lista vacia
        return 'listFactory(std::initializer_list<' + _type + '>())'
    lstr='listFactory({'
    for item in elems:
        if is_any_list:
            lstr+= 'any(' + item + '),'
        else:
            lstr+= item + ','
    lstr=lstr[:-1]#Ecs!!
    lstr+='})'
    #print 'cadena de la lista: %s' % lstr
    return lstr

def process_dict(elems,_type):#No funciona dictFactoty!!
    #Tal y como esta, se pueden definir diccionarios en assign_st, 
    #pero no soporta diccionarios anidados ni su uso en una expresion.
    global tempname,tempcont
    #print 'elems: %s' % elems
    _type=process_prefix(_type)
    name=tempname+str(tempcont)
    tempcont+=1
    #quitar < y > de los que empiecen por <
    if _type[0]=='<':
        _type=_type[1:-1]
    if elems[0]=='}': #Lista vacia
    #std::map<std::string,int> dict3();
        return 'map <' + _type + '>();'
    lstr='map<' + _type + '>  ' + name + ' = {'
    kt=vt=''
    if ',' in _type and len(_type.split(','))==2:#que estas haciendo????
        kt,vt=_type.split(',')
        #Quitar restos
        if '<' in kt:
            kt=kt[(kt.find('<')+1):]
            vt=vt[:vt.find('>')]
    for item in elems:
        k,v=item.split(':')
        #lstr+='{' + item.replace(':',',') + '},'
        lstr+='{' + ('(' + kt + ')' + k if kt else k) + ',' + ('(' + vt + ')' + v if vt else v) + '},'
    lstr=lstr[:-1]#Ecs!!
    lstr+='};'
    return [name,lstr]

def process_idfunitem(tok): #Que pasa con this dot id????
    '''idfunitem : ID
    | THIS DOT ID
    | ID AS generic'''
    if len(tok)==2:
        return tok[1]
    else:
        array_str=''
        if tok[3][-2:]=='[]':
            array_str='[]'
            tok[3]=tok[3][:-2]
    return tok[3] + ' ' + tok[1].strip('%') + array_str
        

def process_annotation(t):
    '''annotation : LBRACK ^ annot_elems_list RBRACK'''
    #return '[' + t[3] + ']\n'
    return t[3] + '|'

def process_fundef(id,funcargs,orderlist,_type,generic,modifiers='',annots=''):#Done
    #flag para indicar que la funcion es decabecera (.h) y solo queremos la definicion
    isheader=0
    #quitar el ultimo | de annots
    #print 'id en cpp-builder: %s' % id
    #print 'funcargs en cpp-builder: %s' % funcargs
    #print 'orderlist en cpp-builder: %s' % orderlist
    #print 'type en cpp-builder: %s' % _type
    #print 'modifiers en cpp-builder: %s' % modifiers
    #print 'annots en cpp-builder: %s' % annots
    if annots!='' and annots!='generic' and annots[-1]=='|': annots=annots[:-1]
    #print "anotaciones: %s" % annots
    annots=annots.split('|')
    if 'header' in annots:
        isheader=1
        del annots[annots.index('header')]
    annots=' '.join(annots)
    #print "anotaciones ahora: %s" % annots
    #Cambio: Procesar funcargs para tener en cuenta los const_xxx---------------------
    funcargs= ','.join([process_prefix(el) for el in funcargs.split(',')])
    #---------------------------------------------------------------------------------
    #print 'funcargs: %s' % funcargs
    val=''
    init_cons_items=[]
    #Usamos las anotaciones para ponerle los valores al constructor si el tipo es ignore
    if annots=='generic': annots=''
    if annots!='':
        #if _type!='ignore': raise Exception('Error: En C++ solo se admite como anotacion cppinit para inicializar constructores')
        annots=annots.strip()
        init_cons_items=annots.split(',')
        #if init_cons_items[0]!='cppinit': raise Exception('Error: En C++ solo se admite como anotacion cppinit para inicializar constructores')
        if init_cons_items[0]=='cppinit': #Esto hay que hacerlo mejor. Ecs!
            init_cons_items=init_cons_items[1:]
        else:
            init_cons_items=[]
    generic_st=r'variadic_[A-Z][a-zA-Z_0-9]*|template_[A-Z][a-zA-Z_0-9]*|[A-Z][a-zA-Z_0-9]*'
    #generic_params=[x for x in re.findall(generic_st,funcargs)]
    #REVISAR: Cambio para tener en cuenta los genericos no solo en los argumentos sino tb en el tipo de retorno
    generic_params=[x for x in re.findall(generic_st,funcargs + ' ' + _type)]
    generic_params=list(set(generic_params)) #Eliminar repetidos
    #Convertir variadic_xx en xx...  ------------------------------------
    for i in range(len(generic_params)):
        if 'variadic_' in generic_params[i]:
            #print 'generic_params[i]: %s' % generic_params[i]
            #print 'funcargs aqui: %s' % funcargs
            #sustituir primero en funcargs
            funcargs=funcargs.replace(generic_params[i],generic_params[i][9:] + '...')
            generic_params[i]=generic_params[i][9:] + '...'
        elif 'template_' in generic_params[i]:
            #print 'generic_params[i]: %s' % generic_params[i]
            #print 'funcargs aqui: %s' % funcargs
            #sustituir primero en funcargs
            funcargs=funcargs.replace(generic_params[i],'template<typename ' + generic_params[i][9:] + '>')
            generic_params[i]='template<typename ' +generic_params[i][9:] + '>'
    #--------------------------------------------------------------------
    #print 'Genericos detectados en fundef: %s' %generic_params
    #print 'valor de generic: %s' % generic
    if generic!=0:
        if generic_params!=[]:
            val+='template< ' + ','.join(['typename ' + x for x in generic_params]) + '>\n'
    #Si se pasan modificadores, ponerlos antes del tipo
    if modifiers!='': _type=modifiers + ' ' + _type
    #Con ignore se ignora el tipo para los constructores y con destructor se genera un destructor
    if _type=='ignore':_type=''
    if _type=='destructor':_type='~'
    #Procesar tipo de retorno para const y posible virtual
    conststr=''
    typeparts=_type.split('_')
    if len(typeparts)>1 and typeparts[0].strip()=='const': 
        conststr=' const '
        typeparts=typeparts[1:]
    if len(typeparts)>1 and typeparts[-1].strip()=='virtual': #Const aqui????
        return '\n' + '_'.join(typeparts[0:-1]) + ' ' + id + ' (' + funcargs + ')=0;\n'
    #val+='\n' + _type + ' ' + id + ' (' + funcargs + ')' 
    val+='\n' + '_'.join(typeparts) + ' ' + id + ' (' + funcargs + ')' + conststr
    if val[-1]==',':val=val[:-1]#quitar la ultima coma???
    if init_cons_items!=[]: val+= ': ' +  ','.join(init_cons_items)
    if isheader==0:
        val+='\n{\n' + indent(orderlist) + '\n}\n' 
    else:
        val+=';\n'
    return val

def process_fundef_anonym(funcargs,orderlist):#Done
    val='[](' + funcargs + ')\n'
    #if val[-1]==',':val=val[:-1]#quitar la ultima coma
    val+='{\n' + orderlist + '\n}' 
    return val

def process_fundef_anonym2(funcargs,orderlist):#Done
    #orderlist puede ser una lista [nemobre,codigo]!!
    val='[](' + funcargs + ')\n'
    if type(orderlist)==type([]): 
        temp=orderlist[1]
        val+='{ ' + temp + ' return ' + orderlist[0] + ';}\n' 
    else:
        val+='{return ' + orderlist + ';}\n' 
    return val

def process_plus(a,b):#Done
    return a + " + " + b;

def process_incr(expr,kind):
    return expr + kind

def process_tolist(a,b):#Done
    return a + ".push_back(" + b + ")"

def process_insertor(a,op,b):#Done
    return a + " " + op + " " + b

def process_range(b,e,s):
    return "_genRange(" + b + "," + e + "," + s + ")"

def process_enum(name,elems):
    return 'enum ' + name + ' {' + elems + '};\n' 

def process_environ(name,instr):
    code='namespace ' + name + '\n{\n'
    code+=indent(instr) + '\n}\n'
    return code

def process_assign(assignable,expr):#Done
    if type(expr)==type([]):
        a,b=expr
        expr= b + ';\n'
        expr+= assignable + '=' + a + ';\n'
        return expr
    elif expr[0:10]=='std::array': #Parche para que los array se asignen como auto
        return '\n auto ' + assignable + " = " + expr
    else:
        return '\n' + assignable + " = " + expr

def process_map(fun,seqs):#Done
    #return '_map(' + seqs + "," + fun + ')'
    return '_map(_iterjoin({' + seqs + "})," + fun + ')'

def process_filter(fun,seqs):#Done
    #return '_filter(' + seqs + "," + fun + ')'
    return '_filter(_iterjoin({' + seqs + "})," + fun + ')'

def process_reduce(fun,seqs,init=None):#Done
    if init==None:
        return '_reduce(_iterjoin({' + seqs + '}), 0,' + fun + ')'
    else:
        return '_reduce(_iterjoin({' + seqs + '}),' + init +  ',' + fun +  ')'

def process_take(mapf,seqs,filtf=None):
    if filtf==None:
        return '_map(_iterjoin({' + seqs + '}),' + mapf + ')'
    else: #Primero filtramos y luego mapeamos
        return '_map(_filter(_iterjoin({' + seqs + '}),' + filtf + '),' + mapf + ')'

def process_slice(start,end,seqs):#Done
    return '_slice(_iterjoin({' + seqs + '}),' + start + ',' + end + ')'

def process_if(cond,code,_else=None):#Done
    if _else==None:
        return '\nif (' + cond + ')\n{\n' + indent(code) + '\n}\n'
    else:
        return '\nif (' + cond + ')\n{\n' + indent(code) + '\n}\nelse\n{\n' + indent(_else) + '\n}\n'

def process_trycatch(tr,ct,fnl):
    code= 'try {\n' + indent(tr) + '}\n' + 'catch(minimal_exception _exception) {\n' + indent(ct) + '}\n'
    if fnl!='':
        #code+= 'finally{\n' + fnl + '}\n'
        raise Exception('Error: C++ no permite usar finally')
    return code

def process_raise(expr):
    return 'minimal_exception __e( ' + expr + ');throw __e\n'

def process_assert(condic):
    code='if (!(' + condic + '))\n'
    code+= 'throw minimal_exception("assertion error: \'%s\' is false"'%condic + ');\n'
    return code

def process_cond(t,counter): #No tenemos cond implementado
    t[3]=[el.replace('%%cond%%','cond'+ str(counter)) for el in t[3]]
    name=t[3][0]
    code=''
    code+='auto ' +  name + '= ' + t[2] + ';\n'
    #Quitar los dos primeros caracteres
    t[3]=t[3][1][4:]
    code+=t[3] + '\n'
    code+='else{\n'
    code+=indent(t[6]) + '}\n'
    return code

def process_caselist(counter,relop,expr,order_list,rest=''):
    #print "en process case list con %s y %s" %(order_list,rest)
    name='%%cond%%'
    code=''
    if rest=='':
        if relop.strip() in ['match','not match']:
            if 'not' in relop:
                code='else if(!_rematch(' + name + ',' + expr + ')){\n'
            else:
                code='else if(_rematch(' + name+ ',' + expr + ')){\n'
        elif relop.strip() in ['in','not in']:
            if 'not' in relop:
                code='else if(!_in(' + expr + ',' + name + ')){\n'
            else:
                code='else if(_in(' + expr + ',' + name + ')){\n'
        else:
            code+='else if (' + name + relop + ' ' + expr + '){\n'
        code+=indent(order_list) + '}\n'
        #Hacemos esto SOLO la primera vez!!!
        #stack.push(name)
        #print 'Apilando: %s' % name
    else:
        if relop.strip() in ['match','not match']:
            if 'not' in relop:
                code='else if(!_rematch(' + name + ',' + expr + ')){\n'
            else:
                code='else if(_rematch(' + name + ',' + expr + ')){\n'
        elif relop.strip() in ['in','not in']:
            if 'not' in relop:
                code='else if(!_in' + expr + ',' + name + ')){\n'
            else:
                code='else if(_in' + expr + ',' + name + ')){\n'
        else:
            code+='else if(' + rest[0] + relop + ' ' + expr + '){\n'
        code+=indent(order_list) + '}\n'
        code+=rest[1]
    code=[name,code]
    return code

def process_foreach(id,expr,code): #Done
    return 'for (auto ' + id + ' : ' + expr + ' )\n{\n' + indent(code) + '\n}\n'

def process_for(id,expr,cond,incr,code): #Done
    return '\nfor (long ' + id + ' = ' + expr + ';' + cond + ';' + incr + ')\n{\n' + indent(code) + '\n}\n'

def process_while(cond,code):#Done
    return 'while (' + cond + ' )\n{\n' + indent(code) + '\n}\n'

def process_repeat(cond,code):#Revisar logica
    #return 'do\n{\n' + indent(code) + '\n};\nwhile (!(' + cond + ') )'
    return 'while (!(' + cond + ' ))\n{\n' + indent(code) + '\n}\n'

def process_let(iddict,code): #no implementado
    return '\n\n(function()\n{\n' + iddict + '\n' + indent(code) + '})()\n\n'

def process_boolexp(tokens):#CAMBIARLO PARA C++!!!!!
    global susts
    #print 'process_boolexp: %s'%[el for el in tokens]
    if len(tokens)==2: #expr
        return tokens[1]
    elif len(tokens)==4: #corregir para match e in
        if tokens[1]=='(':#LPAREN condic_expr RPAREN
            return tokens[1] + tokens[2] + tokens[3]
        else: #expr relop expr
            if tokens[2].strip() in susts:
                return tokens[1] + ' ' + susts[tokens[2]] + ' ' + tokens[3]
            else:
                #print 'valor de tokens[2]: %s'% tokens[2]
                if tokens[2].strip()=='in': #x IN y
                    return' _in(' + tokens[3] + ', ' + tokens[1] + ')'
                if tokens[2].strip()=='not in': #x NOT IN y
                    return' !_in(' + tokens[3] + ', ' + tokens[1] + ')'
                else:
                    return tokens[1] + ' ' + tokens[2] + ' ' + tokens[3]
    else: #MATCH expr IN expr
        return '_rematch(' + tokens[2] +',' + tokens[4] + ')'

def process_ifelse(expr,cond,elsecode):#Done
    return cond + ' ? ' + expr + ' : ' + elsecode;

def process_order(seqs, fun,reverse=0):#Done
    #Collection sort(Collection col,F fun,int reverse)
    if reverse:
        return '_sort(_iterjoin({' + seqs + '}),' + fun + ',0)'
    else:
        return '_sort(_iterjoin({' + seqs + '}),' + fun + ',1)'

#Funciones para clases a partir del csharp builder
def process_new(token):
    if len(token)==3:#NEW idlist
        if token[2][-1]==']': #inicializacion de array
            return token[1] + ' ' + token[2]
        else:
            return token[1] + ' ' + token[2] + '()'
    else:#NEW idlist LPAREN defaults_chain RPAREN
        args=','.join([item.split('=')[1] for item in findElements2(token[4])])
        return token[1] + ' ' + token[2] + '(' + args + ')'

def process_delete(item):
    return "delete " + item
        
def process_class_section(token):
    '''class_section : begin_class_section class_list end_class_section
    | empty'''
    if len(token)==2:
        return token[1]
    else:
        return token[2]

def process_class_list(token): #Revisar bien esto!!!!
    '''class_list : classtype classname EXTENDS base_list inner_class_list field_list member_list END class_list
    | classtype classname EXTENDS base_list inner_class_list field_list  member_list END'''
    code=''
    generics=0
    #print 'token[1] en class_list: %s' % token[1]
    if 'generic' in token[1]:
        generics=1
        token[1]=token[1].replace('generic','')
    clsname=token[2]
    templs2=[]
    all_tpls=''
    if generics==1:
        temp2=re.findall("template<\s*([^>]+)\s*>",token[6][1])
        for item in temp2:
            for el in item.split(','):
                if not el in templs2: templs2.append(el)
        print 'templates definidos en los campos: %s' % templs2

        if templs2!=[]:
            all_tpls='template< ' + ','.join([el for el in templs2]) + '>\n'
            print 'Todos los templates arregladitos: %s' %all_tpls
    #code='public class ' + clsname + ' ' + token[4] + '\n{\n'
    if all_tpls!='':
        code+= all_tpls
    code+=token[1] + ' ' + clsname + ' ' + token[4] + '\n{\n'
    code+= indent(token[5]) + indent(token[6][0]) + indent(token[7])
    code+='\n};\n'
    if len(token)==10:
        code+=token[9]
    return code


def process_base_list(token):
    '''base_list : idchain_list
    | OBJECT
    | OBJECT COMMA idchain_list'''
    code=''
    #de momento todas herencia publica: despues habilitar private y protected
    if len(token)==2:
        if token[1]!="object":
            code+=': '
            for item in token[1].split(','):
                code+=' public ' + item + ','
            code=code[:-1]
    else:
        code+=': '
        for item in token[3].split(','):
            code=' public ' + item + ','
        code=code[:-1]
    return code


def process_field_list(token):
    '''field_list : field_item COLON ambit field_list 
    | field_item COLON ambit
    | empty'''
    code=''
    typ='void* '
    name=''
    if len(token)==2:
        code=token[1]
    else:
        if len(token[1].split('|'))==2:
            name,typ=token[1].split('|')
        else:
            if 'enum ' in token[1]: #Cambio para enums como miembro
                typ=' '
            name=token[1]
        if token[3]!='static':
            code=token[3] + ':\n ' + typ + ' ' + name + ';\n'
        else:
            code='public:\nstatic ' + typ + ' ' + name + ';\n'
    if len(token)==5:
        code+= token[4][0]
    #Buscar genericos si los hay
    generic_st=r'[A-Z][a-zA-Z_0-9]*'
    generic_params=[x for x in re.findall(generic_st,code)]
    #print 'Genericos detectados en field_list: %s' %generic_params
    val=''
    if generic_params!=[]:
        val+='template< ' + ','.join(['typename ' + x for x in generic_params]) + '>\n'
        #print val
    return [code,val]

def process_field_item(token):
    code=''
    if len(token)==4:
        code=token[1] + '|' + token[3]
    else:
        code=token[1]
    return code

def process_inner_class(token):
    '''inner_class : PIPE classtype classname field_list member_list END PIPE'''
    #print [el for el in token]
    #print token[4][0]
    code=''
    code+=token[2] + ' ' + token[3] + '\n{\n'
    code+= indent(token[4][0]) + indent(token[5])
    code+='\n};\n'
    return code

def process_member_list(token):

    return token[1]

def process_member_fun_list(token):
    code=''
    if len(token)==3:
        code=token[1] + token[2]
    else:
        code=token[1]
    return code

# def process_member_fun(token): #ambit fundef
    # #Si se pasa un t como token, token[0] siempre es null!!
    # #De fundef la cadena comienza con un "public static" que no nos interesa
    # '''member_fun : cls_mod fundef'''
    # print 'valor de token[1]: %s' %token[1]
    # print 'valor de token[2]: %s' %token[2]
    # token[2]=token[2].replace('public static','',1)#??
    # if token[1]!='static':
        # return token[1] + ':\n ' + token[2] + '\n'
    # else:
        # return 'public:\nstatic ' + token[2] + '\n'    

def process_member_fun(token): #ambit fundef
    #Si se pasa un t como token, token[0] siempre es null!!
    #De fundef la cadena comienza con un "public static" que no nos interesa
    '''member_fun : cls_mod fundef'''
    #print 'valor de token[1](cls_mod): %s' %token[1]
    #print 'valor de token[2]: %s' %token[2]
    token[2]=token[2].replace('public static','',1)#??
    if token[1] in [None,'']:
        return token[2]
    modifiers=[el.strip() for el in token[1].split(' ')]
    #print 'modifiers: %s' % modifiers
    if 'public' in modifiers:
        del modifiers[modifiers.index('public')]
        return 'public: \n' + ' '.join(modifiers) + ' ' + token[2] +  '\n'
    if 'static' in modifiers:
        del modifiers[modifiers.index('static')]
        return 'public: \nstatic' + ' '.join(modifiers) + ' ' + token[2] +  '\n'
    else: #No deberia pasar nunca por aqui
        return ''

def process_operator(token):#falta operator Id(para los casts)
    ''' operator_def : cls_mod OPERATOR oper_type LPAREN funcargs RPAREN AS generic COLON order_list END'''
    global susts
    code=''
    params=''
    #Cambiar si es and, or o not por el equivalente C++
    if token[3] in susts: 
        token[3]= susts[token[3]]
    if token[3] in ['++','--','+++','--']:
        if token[5]!='': raise Exception('Error: Los operadores "++" y "--" en C++ no admiten argumentos')
        if token[3] in ['---','+++']:
            params= 'int'
            token[3]=token[3][:-1]#Quitar el ultimo + o -
    else:
        params= token[5]
    #Procesar para const y posible virtual
    conststr=''
    typeparts=token[8].split('_')
    if len(typeparts)>1 and typeparts[0].strip()=='const': 
        conststr=' const '
        typeparts=typeparts[1:]
    code+=token[1] + ':\n ' + '_'.join(typeparts) + ' ' + token[2] +  token[3] + ' (' + params + ') ' + conststr + '\n{\n' + indent(token[10]) + '\n}\n'
    return code
    # code+=token[1] + ':\n ' + token[8] + ' ' + token[2] +  token[3] + ' (' + params + ')\n{\n' + indent(token[10]) + '\n}\n'
    # return code
def process_cut(name,regx,elems):
    return  '_relistsplit(vector<string>({' + ','.join(elems) + '}),' + regx + ')'

def process_match(name,regx,elems):#ok
    return  '_relistmatches(vector<string>({' + ','.join(elems) + '}),' + regx + ')'

def process_update(name,elems,old,new):
    return  '_relistreplace(vector<string>({' + ','.join(elems) + '}),' + old + ',' + new + ')'

def process_text_st(lst):
    elems=findElements2(lst)
    return  '_readflist(vector<string>({' + ','.join(elems) + '}))'

def process_lines(regx,elems):
    return  '_resplit(_readflist(vector<string>({' + ','.join(elems) + '})),' + regx + ')'

def process_format(st,lst):
    if st[0]=='"':
        return '_format(string('+ st + '),' + lst + ');\n'
    else:
        return '_format(' + st + ',' + lst + ');\n'

def process_create(kind,elems):
    #print 'valor de kind: %s' % kind
    if kind==2: 
        raise Exception("Error: no se permite create dirs en C++ por ahora")
    elif kind==1: #database
        cad=','.join(elems)
        return '_createSQLiteDB(' + cad + ');\n'
    else:
        cad=','.join(elems)
        if cad[0]=='"':
            return '_create_files(vector<string>{' + cad + '});\n'
        else:
            return '_create_files(' + cad + ');\n'

def process_textwrite(cont,files,apnd):
    if apnd==True:
        if files[0]=='"':
            return '_writeflist(vector<string>{' + files + '},' + cont + ',true);\n'
        else:
            return '_writeflist(' + files + ',' + cont + ',true);\n'
    else:
        if files[0]=='"':
            return '_writeflist(vector<string>{' + files + '},' + cont + ',false);\n'
        else:
            return '_writeflist(' + files + ',' + cont + ',false);\n'

def process_ctypedef(old, new):
    return 'typedef ' + old + ' ' + new


def process_thread(name,fun,join,args=''):
    #No se aceptan argumentos en los threads de C#
    #if args!='': raise Exception('Error: en los threads de C# no se aceptan argumentos')
    code=''
    if args=='':
        code= 'std::thread ' +  name+ '(' + fun + ');\n'
    else:
        code= 'std::thread ' +  name+ '(' + fun + ',' + args +  ');\n'
    if join=='join':
        code+= name + '.join();\n'
    return code

def process_consult_db(db,query): 
    return "_querySQLiteDB(" + db + "," + query + ")\n"
