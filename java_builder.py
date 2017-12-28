#Esquema para traduccion de minimal a Java#
import re

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

def indent(code): #Ok
    indent='    '
    val=''
    for it in code.split('\n'):
        val+=indent + it + '\n'
    #val+='\n'
    return val

def vartable(vdict): #????
    indent='    '
    val=''
    #print vdict
    for it in vdict.split(','):
        val+=indent + 'Object ' +  it + ';\n'
    val+='\n'
    return val   

def process_native(t): #Ok
    '''native : NATIVE idchain
    | NATIVE idchain TIMES
    | NATIVE idchain FROM expr'''
    #return ' import ' + code + ';\n'
    if len(t)==3:
        return 'import ' + t[2] + ';\n'
    else:
        return 'import ' + t[2] + '.*;\n'

def process_run_native(code):#Ok
    raise Exception("Error: Java no admite evaluacion dinamica de codigo")

def process_return(code): #Ok
    return ' return ' +  code

def process_var_decl(ids, tp, val=''):
    code=''
    if tp=='': tp='Object'
    for item in ids.split(','):
        if val!='':
            code+=tp + ' ' + item + ' = ' + val + ';\n'
        else:
            code+=tp + ' ' + item + ';\n'
    return code

def process_annotation(t):
    '''annotation : LBRACK AMPERSAND annot_elems_list RBRACK'''
    return '@' + t[3] + '\n'

def process_idfunitem(item):#Ok?
    '''idfunitem : ID
    | THIS DOT ID
    | ID AS generic'''
    #print 'len(t) en process_idfunitem: %s' % len(item)
    if len(item)==2:
        return 'Object ' + item[1]
    elif item[2]=='as':
	    return item[3] + ' ' + item[1]
    else:
        return item[1] + ' ' + item[2] + ' ' + item[3]

def process_fundef(id,funcargs,orderlist,_type,generic,modifiers,annots=''):#Ok
    #
    #Buscar argumentos genericos en funcargs(empiezan con mayusculas)
    #No traducir el tipo "ignore": constructores y similares
    val=''
    if _type=='': _type='Object'
    if _type=='ignore': _type=''
    templatestr=''
    if generic!=0:
        generic_st=r'\b[A-Z]\b' #Restringidos nombres de genericos a UNA mayuscula!!!!
        generic_params=[x for x in re.findall(generic_st,funcargs)]
        #print 'Genericos detectados: %s' %generic_params
        if generic_params!=[]:
            templatestr='< ' + ','.join([x for x in generic_params]) + '>'
    #if annots!='':
    #    val+=annots + '\n'
    if modifiers=='':
        #print 'public static ' + _type + ' ' + id + templatestr +  ' (' + funcargs 
        #val+='public static ' + _type + ' ' + id + templatestr +  ' (' + funcargs + ')\n'
        val+= annots + 'public static ' + templatestr + ' ' + _type + ' ' + id + ' (' + funcargs + ')\n'
        #print 'valor de val aqui: %s'%repr(val)
    else:
        #val+= modifiers + ' ' + _type + ' ' + id + templatestr +  ' (' + funcargs + ')\n'
        val+= annots +  modifiers + ' ' + templatestr + ' ' + _type + ' ' + id + ' (' + funcargs + ')\n'
    if val[-1]==',':val=val[:-1]#quitar la ultima coma???
    #Permitimos funciones vacias para definir interfaces
    if orderlist=='':
        #val+=';'
        val+='{}'
    else:
        val+='\n{\n' + indent(orderlist) + '\n}\n' 
    #print 'Valor de la cadena de la funcion: %s' % val
    return indent(val)

def process_fundef_anonym(funcargs,orderlist):#Ok
    val='(' + funcargs + ')->\n'
    #if val[-1]==',':val=val[:-1]#quitar la ultima coma
    val+='{\n' + orderlist + '\n}' 
    return val

def process_fundef_anonym2(funcargs,orderlist):#Ok
    #quitar cualquier object x que pudiera haberse metido por no poner tipos
    #(esto plantea el problema de si de verdad se quiere un object x
    funcargs=funcargs.replace('Object','')
    val='(' + funcargs + ')->' + orderlist + '\n'
    return val

def process_plus(a,b):#ok
    return a + " + " + b;

def process_tolist(a,b): #Ok
    return a + ".add(" + b + ")"

def process_range(b,e,s): #Ok?
    return "JavaRuntime.genRange(" + b + "," + e + "," + s + ")"

def process_array(elems,_type):#Ok?
    if _type=='': _type='Object'
    return  'new ' + _type + ' {' + ','.join(elems) + '}'

def process_assign(assignable,expr):#Ok
    if type(expr)==type([]):
        return '\n' + expr[1] + '\n' + assignable + ' = ' + expr[0]
    else:
        return '\n' + assignable + " = " + expr

def process_map(fun,seqs):#Ok
    #return 'JavaRuntime.map(JavaRuntime.iterjoin(' + seqs + '),' + fun + ')'
    return 'JavaRuntime.map(' + fun + ',JavaRuntime.iterjoin(' + seqs + '))'

def process_filter(fun,seqs):#Ok
    #return 'JavaRuntime.filter(JavaRuntime.iterjoin(' + seqs + '),' + fun + ')'
    return 'JavaRuntime.filter(' + fun + ',JavaRuntime.iterjoin(' + seqs + '))'

def process_reduce(fun,seqs,init=None):#Ok
    if init==None:
        return 'JavaRuntime.reduce(0,' + fun + ',JavaRuntime.iterjoin(' + seqs + '))'
    else:
        return 'JavaRuntime.reduce(' + init + ',' + fun + ',JavaRuntime.iterjoin(' + seqs + '))'

def process_take(mapf,seqs,filtf=None):#Ok
    if filtf==None:
        return 'JavaRuntime.map(' + mapf + ',JavaRuntime.iterjoin(' + seqs + '))'
    else: #Primero filtramos y luego mapeamos
        return 'JavaRuntime.map(' + mapf + ',JavaRuntime.filter(' + filtf + ',JavaRuntime.iterjoin(' + seqs + ')))'

def process_slice(start,end,seqs): #Ok
    return 'JavaRuntime.slice(JavaRuntime.iterjoin(' + seqs + '),' + start + ',' + end + ')'

def process_if(cond,code,_else=None):#Ok
    if _else==None:
        return '\nif (' + cond + ')\n{\n' + indent(code) + '\n}\n'
    else:
        return '\nif (' + cond + ')\n{\n' + indent(code) + '\n}\nelse\n{\n' + indent(_else) + '\n}\n'

def process_foreach(id,expr,code):#Ok
    return '\nfor (' + id + ' : ' + expr + ' )\n{\n' + indent(code) + '\n}\n'

def process_for(id,expr,cond,incr,code):#Ok
    return '\nfor (long ' + id + ' = ' + expr + ';' + cond + ';' + incr + ')\n{\n' + indent(code) + '\n}\n'

def process_while(cond,code):#Ok
    return '\nwhile (' + cond + ' )\n{\n' + indent(code) + '\n}\n'

def process_repeat(cond,code):#Ok?
    return '\ndo\n{\n' + indent(code) + '\n}\nwhile (' + cond + ' );'

def process_let(iddict,code): #Esto debe dar una excepcion!!
    return '\n\n(function()\n{\n' + iddict + '\n' + indent(code) + '})()\n\n'

def process_ifelse(expr,cond,elsecode): #Ok
    return cond + ' ? ' + expr + ' : ' + elsecode;

def process_order(seqs, fun,reverse=0):#Ok
    if reverse:
        return 'JavaRuntime.order(' + fun + ',JavaRuntime.iterjoin(' + seqs + '),true)\n'
    else:
        return 'JavaRuntime.order(' + fun + ',JavaRuntime.iterjoin(' + seqs + '),false)\n'

def process_global_vars(inside_fun,inside_macro,idlist):#Deberia dar excepcion en Java??
    if inside_fun or inside_macro: #Ignorar globales en macros y funciones (?)
        return ''
    else:
        s=''
        for item in idlist.split(','):
            s+='var ' + item  + '=null;\n'
    return s

def process_cut(name,regx,elems):#Ok
    code= 'ArrayList<String> ' + name + ' = new ArrayList<>();\n'
    for item in elems:
        code+= name + '.addAll( JavaRuntime.resplit(' + item+ ',' + regx + '));\n'
    return [name,code]

def process_match(name,regx,elems): #Ok
    code= 'ArrayList<String> ' + name + ' = new ArrayList<>();\n'
    for item in elems:
        code+= name + '.addAll( JavaRuntime.rematches(' + item + ',' + regx + '));\n'
    return [name,code]

def process_update(name,elems,old,new): #Ok
    code= 'ArrayList<String> ' + name + ' = new ArrayList<String>();\n'
    for item in elems:
        code+= name + '.add( JavaRuntime.rereplace(' + item + ',' + old + ',' + new + '));\n'
    return [name,code]

def process_text_st(lst):#Ok
    global cont
    elems=findElements2(lst)
    code=''
    name='aux' + str(cont)
    cont+=1
    code+= 'String ' + name + '="";\n'
    for item in elems:
        code+= '\nif (new java.io.File(' + item + ').isFile())\n'
        code+= '{' + name + '+=JavaRuntime.readf(' + item + ');\n}'
        code+= 'else{\n ' + name + '+= ' + item + ';}\n'
    return [name,code]

def process_format(st,lst): #Ok
    code= 'JavaRuntime.format('+ st + ',' + lst + ')'
    return code

def process_trycatch(tr,ct,fnl):
    code= 'try {\n' + tr + '}\n' + 'catch(Exception err) {\n' + ct + '}\n'
    if fnl!='':
        code+= 'finally{\n' + fnl + '}\n'
    return code

def process_raise(expr):
    return 'throw new Exception(' + expr + ');\n'

def process_assert(condic): #Ok?
    code='if (!(' + condic + '))\n'
    code+= 'throw new Exception("assertion error: \'%s\' is false"'%condic + ');\n'
    return code

def process_cond(t,counter):
    t[3]=[el.replace('%%cond%%','cond'+ str(counter)) for el in t[3]]
    name=t[3][0]
    code=''
    code+='var ' +  name + '= ' + t[2] + ';\n'
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
                code='else if(!JavaRuntime.match(' + name + ',' + expr + ')){\n'
            else:
                code='else if(JavaRuntime.match(' + name+ ',' + expr + ')){\n'
        elif relop.strip() in ['in','not in']:
            if 'not' in relop:
                code='else if(!' + expr + '.contains(' + name + ')){\n'
            else:
                code='else if(' + expr + '.contains(' + name + ')){\n'
        else:
            code+='else if (' + name + relop + ' ' + expr + '){\n'
        code+=indent(order_list) + '}\n'
        #Hacemos esto SOLO la primera vez!!!
        #stack.push(name)
        #print 'Apilando: %s' % name
    else:
        if relop.strip() in ['match','not match']:
            if 'not' in relop:
                code='else if(!JavaRuntime.match(' + name + ',' + expr + ')){\n'
            else:
                code='else if(JavaRuntime.match(' + name + ',' + expr + ')){\n'
        elif relop.strip() in ['in','not in']:
            if 'not' in relop:
                code='else if(!' + expr + '.contains(' + name + ')){\n'
            else:
                code='else if(' + expr + '.contains(' + name + ')){\n'
        else:
            code+='else if(' + rest[0] + relop + ' ' + expr + '){\n'
        code+=indent(order_list) + '}\n'
        code+=rest[1]
    code=[name,code]
    return code

def process_incr(expr,kind):
    return expr + kind

def process_yield(expr): #Debe dar excepcion en java( o mapearlo a un stream)
    return 'yield return '  + expr

def process_next(expr):#??????
    return expr + '.next()'

def process_boolexp(tokens):#Ok
    global susts
    if len(tokens)==2: #expr
        return tokens[1]
    elif len(tokens)==4: #corregir para match e in
        if tokens[1]=='(':#LPAREN condic_expr RPAREN
            return tokens[1] + tokens[2] + tokens[3]
        else: #expr relop expr
            if tokens[2].strip() in susts:
                return tokens[1] + ' ' + susts[tokens[2]] + ' ' + tokens[3]
            else:
                if tokens[2].strip()=='in': #x IN y
                    return tokens[3] + '.contains(' + tokens[1] + ')'
                else:
                    return tokens[1] + ' ' + tokens[2] + ' ' + tokens[3]
    else: #MATCH expr IN expr
        return 'JavaRuntime.rematch(' + tokens[2] +',' + tokens[4] + ')'

def process_sequence(elems,_type):#Ok?
    print 'elems: %s' % elems
    print 'type: %s'%repr(_type)
    if _type=='':
        if elems[0]==']':
            return 'JavaRuntime.listFactory()'
        else:
            #print 'volviendo por donde debo'
            return 'JavaRuntime.listFactory(' + ','.join(elems) + ')'
    if elems[0]==']': #Lista vaciat
        return 'JavaRuntime.listFactory();'
    lstr='JavaRuntime.listFactory('
    for item in elems:
        if item[0]=='[': #listas anidadas, recursivo!
            item=process_sequence(findElements2(item[1:-1]),_type)
            #print 'Valor de item procesado: %s' % item
        #lstr+='(' + _type + ')' + item + ','
        lstr+=item + ','
    lstr=lstr[:-1]#Ecs!!
    lstr+=')'
    return lstr

def process_dict(elems,_type):#Ok
    #print 'elems: %s' % elems
    #print '_type: %s' % _type
    _type2=_type.split('<')[1:]
    _type2=''.join(_type2)
    _types_st=r'\b[A-Za-z_]+\b' #Restringidos nombres de genericos a una mayuscula!!!!
    _types=[x for x in re.findall(_types_st,_type2)]
    #print '_types: %s' % _types
    if elems[0]=='}': #Lista vacia
        if _type=='': _type='<Object,Object> '
        return 'JavaRuntime.dictFactory ();\n'
    lstr='JavaRuntime.dictFactory('
    kt=[]
    vt=[]
    for item in elems:
        k,v=item.split(':')
        kt.append(k)
        vt.append(v)
    kt=','.join(kt)
    vt=','.join(vt)
    lstr+= 'new ' + _types[0] + '[] {' + kt + '}, new ' + _types[1] + '[] {' + vt + '})\n'
    return lstr

def process_multassign2(idlist,last,expr):
    code=''
    ids=len(idlist)
    for i in range(ids):
        code+= idlist[i] + ' = ' + expr + '[' + str(i) + '];\n'
    code+= last + ' = ' + expr + '.slice(' + str(ids) + ');\n'
    return code

def process_typed_assign(id,expr,typ):
    code= typ + ' ' + id.strip() + ' = ' + expr + ';\n'
    return code

def process_new(token): #Ok?
    if len(token)==3:#NEW idlist
        if token[2][-1]==']': #inicializacion de array
            return token[1] + ' ' + token[2]
        else:
            return token[1] + ' ' + token[2] + '()'
    else:#NEW idlist LPAREN defaults_chain RPAREN
        return token[1] + ' ' + token[2] + '(' + token[4] + ')'

def process_class_section(token):#Ok?
    '''class_section : begin_class_section class_list end_class_section
    | empty'''
    #print 't en class_ssection: %s' % [el for el in token]
    if len(token)==2:
        return token[1]
    else:
        return token[2]

def process_class_list(token): #Ok?
    '''class_list : classtype classname extends_or_implements base_list inner_class_list field_list member_list END class_list
    | classtype classname extends_or_implements base_list inner_class_list field_list  member_list END'''
    code=''
    clsname=token[2]
    #code=token[1] + ' ' + clsname + ' ' + token[4] + '\n{\n'
    #Cambio: En Java, cuando se pasa mas de un elemento en la cadena de herencia,
    #Si se pone extends, hereda de la primera e implementa el resto. Si es implements, implementa todas
    if token[3]=='extends' and len(token[4].split(','))>1:
        code+=token[1] + ' ' + clsname + ' '
        bases=token[4].split(',')
        code+= ' extends ' + bases[0] + ' implements ' + ','.join(bases[1:]) + '\n{\n'
    else:
        if token[4]!='':
            code=token[1] + ' ' + clsname + ' ' + token[4] + '\n{\n'
        else:
            code=token[1] + ' ' + clsname + ' ' + '\n{\n'
    code+= indent(token[5]) + indent(token[6]) + indent(token[7])
    code+='\n}\n'
    if len(token)==10:
        code+=token[9]
    return code

def process_base_list(token): #Ok?
    '''base_list : idchain_list
    | OBJECT
    | OBJECT COMMA idchain_list'''
    code=''
    if len(token)==2:
        if token[1]!="object":
            code+=': ' + token[1]
    else:
        code=': ' + token[3]
    return code


def process_field_list(token): #Ok?
    '''field_list : field_item COLON ambit field_list 
    | field_item COLON ambit
    | empty'''
    #print 'token en fld_list: %s' % [el for el in token]
    code=''
    typ='Object'
    name=''
    if len(token)==2:
        code=token[1]
    else:
        if len(token[1].split('|'))==2:
            name,typ=token[1].split('|')
        else:
            typ='Object'
            name=token[1]
            #Cambio para que no ponga Object en las enums
            if 'enum ' in token[1]: typ=''
        code=token[3] + ' ' + typ + ' ' + name + ';\n'
    if len(token)==5:
        code+= token[4]
    #print 'code en fld_list: %s' % code
    return code

def process_field_item(token):
    '''field_item : ID
    | ID AS generic
    | enum_st'''
    #print 'token en fld_item: %s' % [el for el in token]
    code=''
    if len(token)==4:
        code=token[1] + '|' + token[3]
    else:
        code=token[1]
    #print 'code en fld_item: %s' % code
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

def process_inner_class(token):
    '''inner_class : PIPE classtype classname extends_or_implements base_list field_list member_list END PIPE'''
    #print [el for el in token]
    #print token[4][0]
    code=''
    #code+=token[2] + ' ' + token[3] + ' ' + token[4] + ' ' + token[5][1:] + '\n{\n'
    #Cambio: En Java, cuando se pasa mas de un elemento en la cadena de herencia,
    #Si se pone extends, hereda de la primera e implementa el resto. Si es implements, implementa todas
    if token[4]=='extends' and len(token[5].split(','))>1:
        code+=token[2] + ' ' + token[3] + ' '
        bases=token[5][1:].split(',')
        code+= ' extends ' + bases[0] + ' implements ' + ','.join(bases[1:]) + '\n{\n'
    else:
        if token[5][1:]!='':
            code=token[2] + ' ' + token[3] + ' ' + token[4] + ' ' + token[5] + '\n{\n'
        else:
            code=token[2] + ' ' + token[3] + ' ' + '\n{\n'
    #code+= indent(token[6][0]) + indent(token[7])
    code+= indent(token[6]) + indent(token[7])
    code+='\n};\n'
    return code

# def process_member_fun(token): #ambit fundef
    # #print 'token[2]: %s' % token[2]
    # #De fundef la cadena comienza con un "public static" que no nos interesa a no ser que tenga anotaciones
    # if '@' not in token[2]:
        # token[2]=token[2].replace('public static','',1)
        # return token[1] + ' ' + token[2] + '\n'
    # else:
        # return token[2] + '\n'


def process_member_fun(token): #Ok ambit fundef
    #print 'token[2]: %s' % token[2]
    #De fundef la cadena comienza con un "public static" que no nos interesa
    token[2]=token[2].replace('public static','',1)
    parts=token[2].split(' ')
    annots= [part for part in parts if '@' in part]
    rest= [part for part in parts if '@' not in part]
    #print 'annots: %s' % annots
    #print 'rest: %s' % rest
    #return token[1] + ' ' + token[2] + '\n'
    if annots==[]:
        return token[1] + ' ' + token[2] + '\n'
    else:
        return '\n'.join(annots) + token[1] + ' '.join(rest) + '\n'


def process_operator(token): #En Java debe dar una excepcion
    ''' operator_def : cls_mod OPERATOR oper_type LPAREN funcargs RPAREN AS generic COLON order_list END'''
    code=''
    #code+=token[1] + ' ' + token[8] + ' ' + token[2] + ' ' + token[3] + '(' + token[5] + ')\n{\n' + indent(token[10]) + '\n}\n'
    return code

def process_consult_db(db,query): 
    return "JavaRuntime.getSQLiteResults(\"" + db.strip('"') + "\",\"" + query.strip('"') + "\")\n"

def process_create(what,items): #1:bd, 2:dirs,3:files
    code=''
    if what==1: #db
        for item in items:      
           code+= "JavaRuntime.createSQLiteDB( " + item + ");\n"
    elif what==2: #dirs
        for item in items: 
           code+= "System.IO.Directory.CreateDirectory(" + item + ");\n"
    elif what==3: #files
        for item in items: 
           code+= "(System.IO.File.Create(" + item + ")).Close();\n"
    return code

def process_delete(items,what): #1:files, 2:dirs
    code=''
    if what==1:
        for item in items:      
           code+= "System.IO.File.Delete( " + item + ");\n"
    else:
        for item in items:      
           code+= "System.IO.Directory.Delete( " + item + ");\n"
    return code

def process_copy(item,dest,what): #1:files, 2:dirs
    code=''
    if what==1:   
       code+= "JavaRuntime.docopy( " + item + "," + dest + ",false);\n"
    else:    
       code+= "JavaRuntime.docopy( " + item + "," + dest + ",true);\n"
    return code

def process_selectf(paths,patrs): #Ok  
    code= "JavaRuntime._selectf( JavaRuntime.listFactory<string>(" + paths + "),JavaRuntime.listFactory<string>(" + patrs + "));\n"
    return code

def process_environ(name,instr): #Ok
    code='package ' + name + ';\n'
    code+=indent(instr) + '\n'
    return code
#Generamos enums sencillas y que empiezan en cero
def process_enum(name,elems): #Ok. Los campos de las enums TIENEN que ir en mayusculas en Java
    return 'enum ' + name + ' {' + ','.join([el.split('=')[0] for el in elems.split(',')]) + '};\n' 

def process_thread(name,fun,join,args=''):
    #No se aceptan argumentos en los threads de C#
    if args!='': raise Exception('Error: en los threads de C# no se aceptan argumentos')
    code= name+ ' = new Thread( new ThreadStart(' + fun + '));\n'
    code+= name + '.Start();\n'
    if join=='join':
        code+= name + '.Join();\n'
    return code


def process_xml_st(t):
    '''xml_st : XML expr_list
    | XML expr FROM path_elems_list
    | XML path_elems_list ARROW path_elems_list IN expr'''
    if len(t)==3: #xml expr_list
        return 'JavaRuntime.documentFactory(' + t[2] + ')'
    elif len(t)==5:#xml expr from path_elems_list
	    return 'JavaRuntime.getXpathNodes(' + t[4] + ',' + t[2] + ')'
    else: #XML path_elems_list ARROW path_elems_list IN expr
        return 'JavaRuntime.appendXmlFragment(' + t[4] + ',' + t[6] + ',JavaRuntime.xmlstring(' + t[2] + '))'



def process_html_st(t):
    '''html_st : HTML expr
    | HTML path_elems_list INSERTOR expr'''
    if len(t)==3: #HTML expr
        return 'JavaRuntime.getHTMLDocument(' + t[2] + ')'
    else: #HTML path_elems_list INSERTOR expr
        return 'JavaRuntime.htmlSelector(' + t[2] + ',' + t[4] + ')'

def process_create(kind,elems):
    #print 'valor de kind: %s' % kind
    if kind==2: 
        cad=','.join(elems)
        if cad[0]=='"':
            return 'JavaRuntime.createDirs(new ArrayList<String>(Arrays.asList(' + cad + ')));\n'
        else:
            return 'JavaRuntime.createDir(' + cad + ');\n'
    elif kind==1: #database
        cad=','.join(elems)
        return '_createSQLiteDB(' + cad + ');\n'
    else:
        cad=','.join(elems)
        if cad[0]=='"':
            return 'JavaRuntime.createFiles(new ArrayList<String>(Arrays.asList(' + cad + ')));\n'
        else:
            return 'JavaRuntime.createFile(' + cad + ');\n'