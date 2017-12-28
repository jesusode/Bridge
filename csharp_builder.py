#Esquema para traduccion de minimal a C#
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

def indent(code):
    indent='    '
    val=''
    for it in code.split('\n'):
        val+=indent + it + '\n'
    val+='\n'
    return val

def vartable(vdict):
    indent='    '
    val=''
    #print vdict
    for it in vdict.split(','):
        val+=indent + 'var ' +  it + ';\n'
    val+='\n'
    return val   

def process_native(code):
    return ' using ' + code + ';\n'

def process_run_native(code):
    return ' eval(' + code + ')'

def process_return(code):
    return ' return ' +  code

def process_var_decl(ids, tp, val=''):
    code=''
    if tp=='': tp='object'
    for item in ids.split(','):
        if val!='':
            code+=tp + ' ' + item + ' = ' + val + ';\n'
        else:
            code+=tp + ' ' + item + ';\n'
    return code

def process_annotation(t):
    '''annotation : LBRACK AMPERSAND annot_elems_list RBRACK'''
    return '[' + t[3] + ']\n'

def process_idfunitem(item):#????????????????????
    if len(item.split(' '))==1:
        return 'object ' + item
    else:
        return item

def process_fundef(id,funcargs,orderlist,_type,generic,modifiers,annots=''):#Done
    #
    #Buscar argumentos genericos en funcargs(empiezan con mayusculas)
    #No traducir el tipo "ignore": constructores y similares
    val=''
    if _type=='': _type='object'
    if _type=='ignore': _type=''
    templatestr=''
    if generic!=0:
        generic_st=r'\b[A-Z]\b' #Restringidos nombres de genericos a UNA mayuscula!!!!
        generic_params=[x for x in re.findall(generic_st,funcargs)]
        #print 'Genericos detectados: %s' %generic_params
        if generic_params!=[]:
            templatestr='< ' + ','.join([x for x in generic_params]) + '>'
    if annots!='':
        val+=annots + '\n'
    if modifiers=='':
        #print 'public static ' + _type + ' ' + id + templatestr +  ' (' + funcargs 
        val+='public static ' + _type + ' ' + id + templatestr +  ' (' + funcargs + ')\n'
        #print 'valor de val aqui: %s'%repr(val)
    else:
        val+= modifiers + ' ' + _type + ' ' + id + templatestr +  ' (' + funcargs + ')\n'
    if val[-1]==',':val=val[:-1]#quitar la ultima coma???
    #Permitimos funciones vacias para definir interfaces
    if orderlist=='':
        val+=';'
    else:
        val+='\n{\n' + indent(orderlist) + '\n}\n' 
    #print 'Valor de la cadena de la funcion: %s' % val
    return indent(val)

def process_fundef_anonym(funcargs,orderlist):#Done
    val='(' + funcargs + ')=>\n'
    #if val[-1]==',':val=val[:-1]#quitar la ultima coma
    val+='{\n' + orderlist + '\n}' 
    return val

def process_fundef_anonym2(funcargs,orderlist):#ok
    #quitar cualquier object x que pudiera haberse metido por no poner tipos
    #(esto plantea el problema de si de verdad se quiere un object x
    funcargs=funcargs.replace('object','')
    val='(' + funcargs + ')=>\n'
    val+= orderlist + '\n' 
    return val

def process_plus(a,b):#ok
    return a + " + " + b;

def process_incr(expr,kind):
    return expr + kind

def process_tolist(a,b):
    return a + ".Add(" + b + ")"

def process_range(b,e,s):
    return "minimal.runtime.genRange(" + b + "," + e + ",(long)" + s + ")"

def process_array(elems,_type):#?
    if _type=='': _type='object'
    return  'new ' + _type + '[' + str(len(elems)) + '] {' + ','.join(elems) + '}'

def process_assign(assignable,expr):
    if type(expr)==type([]):
        return '\n' + expr[1] + '\n' + assignable + ' = ' + expr[0]
    else:
        return '\n' + assignable + " = " + expr

def process_map(fun,seqs):
    return 'minimal.runtime.map(minimal.runtime.iterjoin(' + seqs + '),' + fun + ')'

def process_filter(fun,seqs):
    return 'minimal.runtime.filter(minimal.runtime.iterjoin(' + seqs + '),' + fun + ')'

def process_reduce(fun,seqs,init=None):
    if init==None:
        return 'minimal.runtime.reduce(minimal.runtime.iterjoin(' + seqs + '),' + fun + ')'
    else:
        return 'minimal.runtime.reduce(minimal.runtime.iterjoin(' + seqs + '),' + fun + ',' + init +  ')'

def process_take(mapf,seqs,filtf=None):
    if filtf==None:
        return 'minimal.runtime.map(minimal.runtime.iterjoin(' + seqs + '),' + mapf + ')'
    else: #Primero filtramos y luego mapeamos
        return 'minimal.runtime.map(minimal.runtime.filter(minimal.runtime.iterjoin(' + seqs + '),' + filtf + '),' + mapf + ')'

def process_slice(start,end,seqs):
    return 'minimal.runtime.slice(minimal.runtime.iterjoin(' + seqs + '),' + start + ',' + end + ')'

def process_if(cond,code,_else=None):#ok
    if _else==None:
        return '\nif (' + cond + ')\n{\n' + indent(code) + '\n}\n'
    else:
        return '\nif (' + cond + ')\n{\n' + indent(code) + '\n}\nelse\n{\n' + indent(_else) + '\n}\n'

def process_foreach(id,expr,code):#ok
    return '\nforeach (var ' + id + ' in ' + expr + ' )\n{\n' + indent(code) + '\n}\n'

def process_for(id,expr,cond,incr,code):#ok
    return '\nfor (var ' + id + ' = ' + expr + ';' + cond + ';' + incr + ')\n{\n' + indent(code) + '\n}\n'

def process_while(cond,code):#ok
    return '\nwhile (' + cond + ' )\n{\n' + indent(code) + '\n}\n'

def process_repeat(cond,code):#ok
    return '\ndo\n{\n' + indent(code) + '\n}\nwhile (' + cond + ' );'

def process_let(iddict,code):
    return '\n\n(function()\n{\n' + iddict + '\n' + indent(code) + '})()\n\n'

def process_ifelse(expr,cond,elsecode):
    return cond + ' ? ' + expr + ' : ' + elsecode;

def process_order(seqs, fun,reverse=0):
    if reverse:
        return 'minimal.runtime.order(minimal.runtime.iterjoin(' + seqs + '),' + fun + ',true);\n'
    else:
        return 'minimal.runtime.order(minimal.runtime.iterjoin(' + seqs + '),' + fun + ',false);\n'

def process_global_vars(inside_fun,inside_macro,idlist):
    if inside_fun or inside_macro: #Ignorar globales en macros y funciones (?)
        return ''
    else:
        s=''
        for item in idlist.split(','):
            s+='var ' + item  + '=null;\n'
    return s

def process_cut(name,regx,elems):
    code= 'System.Collections.Generic.List<string> ' + name + ' = new System.Collections.Generic.List<string>();\n'
    for item in elems:
        code+= name + '.AddRange( minimal.runtime.split(' + item+ ',' + regx + '));\n'
    return [name,code]

def process_match(name,regx,elems):#ok
    code= 'System.Collections.Generic.List<string> ' + name + ' = new System.Collections.Generic.List<string>();\n'
    for item in elems:
        code+= name + '.AddRange( minimal.runtime.getMatches(' + regx + ',' + item + '));\n'
    return [name,code]

def process_update(name,elems,old,new):
    code= 'System.Collections.Generic.List<string> ' + name + ' = new System.Collections.Generic.List<string>();\n'
    for item in elems:
        code+= name + '.Add( minimal.runtime.replace(' + item + ',' + old + ',' + new + '));\n'
    return [name,code]

def process_text_st(lst):
    global cont
    elems=findElements2(lst)
    code=''
    name='aux' + str(cont)
    cont+=1
    code+= 'string ' + name + '="";\n'
    for item in elems:
        code+= '\nif (System.IO.File.Exists(' + item + '))\n'
        code+= '{' + name + '+=System.IO.File.ReadAllText(' + item + ');\n}'
        code+= 'else{\n ' + name + '+= ' + item + ';}\n'
    return [name,code]

def process_format(st,lst):
    code= 'String.Format('+ st + ',' + lst + '.ToArray());\n'
    return code

def process_trycatch(tr,ct,fnl):
    code= 'try {\n' + tr + '}\n' + 'catch(System.Exception err) {\n' + ct + '}\n'
    if fnl!='':
        code+= 'finally{\n' + fnl + '}\n'
    return code

def process_raise(expr):
    return 'throw new System.Exception(' + expr + ');\n'

def process_assert(condic):
    code='if (!(' + condic + '))\n'
    code+= 'throw new System.Exception("assertion error: \'%s\' is false"'%condic + ');\n'
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
                code='else if(!minimal.runtime.match(' + name + ',' + expr + ')){\n'
            else:
                code='else if(minimal.runtime.match(' + name+ ',' + expr + ')){\n'
        elif relop.strip() in ['in','not in']:
            if 'not' in relop:
                code='else if(!' + expr + '.Contains(' + name + ')){\n'
            else:
                code='else if(' + expr + '.Contains(' + name + ')){\n'
        else:
            code+='else if (' + name + relop + ' ' + expr + '){\n'
        code+=indent(order_list) + '}\n'
        #Hacemos esto SOLO la primera vez!!!
        #stack.push(name)
        #print 'Apilando: %s' % name
    else:
        if relop.strip() in ['match','not match']:
            if 'not' in relop:
                code='else if(!minimal.runtime.match(' + name + ',' + expr + ')){\n'
            else:
                code='else if(minimal.runtime.match(' + name + ',' + expr + ')){\n'
        elif relop.strip() in ['in','not in']:
            if 'not' in relop:
                code='else if(!' + expr + '.Contains(' + name + ')){\n'
            else:
                code='else if(' + expr + '.Contains(' + name + ')){\n'
        else:
            code+='else if(' + rest[0] + relop + ' ' + expr + '){\n'
        code+=indent(order_list) + '}\n'
        code+=rest[1]
    code=[name,code]
    return code

def process_incr(expr,kind):
    return expr + kind

def process_yield(expr):
    return 'yield return '  + expr

def process_next(expr):#??????
    return expr + '.next()'

def process_boolexp(tokens):#ok
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
                    return tokens[3] + '.Contains(' + tokens[1] + ')'
                else:
                    return tokens[1] + ' ' + tokens[2] + ' ' + tokens[3]
    else: #MATCH expr IN expr
        return 'minimal.runtime.match(' + tokens[2] +',' + tokens[4] + ')'

def process_sequence(elems,_type):#REVISAR CAMBIO RECURSIVO!!
    #print 'elems: %s' % elems
    #print 'type: %s'%repr(_type)
    if _type=='':
        if elems[0]==']':
            return 'minimal.runtime.listObjectFactory()'
        else:
            #print 'volviendo por donde debo'
            return 'minimal.runtime.listObjectFactory(' + ','.join(elems) + ')'
    if elems[0]==']': #Lista vaciat
        return 'minimal.runtime.listFactory();'
    lstr='minimal.runtime.listFactory('
    for item in elems:
        if item[0]=='[': #listas anidadas, recursivo!
            item=process_sequence(findElements2(item[1:-1]),_type)
            #print 'Valor de item procesado: %s' % item
        #lstr+='(' + _type + ')' + item + ','
        lstr+=item + ','
    lstr=lstr[:-1]#Ecs!!
    lstr+=')'
    return lstr

def process_dict(elems,_type):
    _type2=_type.split('<')[1:]
    _type2=''.join(_type2)
    _types_st=r'\b[A-Za-z_]+\b' #Restringidos nombres de genericos a una mayuscula!!!!
    _types=[x for x in re.findall(_types_st,_type2)]
    #print '_types: %s' % _types
    if elems[0]=='}': #Lista vacia
        if _type=='': _type='<object,object> '
        return 'new minimal.runtime.dictFactory ' + _type + '();\n'
    lstr='minimal.runtime.dictFactory('
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

def process_new(token):
    if len(token)==3:#NEW idlist
        if token[2][-1]==']': #inicializacion de array
            return token[1] + ' ' + token[2]
        else:
            return token[1] + ' ' + token[2] + '()'
    else:#NEW idlist LPAREN defaults_chain RPAREN
        return token[1] + ' ' + token[2] + '(' + token[4] + ')'

def process_class_section(token):
    '''class_section : begin_class_section class_list end_class_section
    | empty'''
    if len(token)==2:
        return token[1]
    else:
        return token[2]

def process_class_list(token):
    '''class_list : CLASS ID EXTENDS base_list field_list member_list END class_list
    | CLASS ID EXTENDS base_list field_list  member_list END'''
    code=''
    clsname=token[2]
    #code='public class ' + clsname + ' ' + token[4] + '\n{\n'
    code=token[1] + ' ' + clsname + ' ' + token[4] + '\n{\n'
    code+= indent(token[5]) + indent(token[6])
    code+='\n}\n'
    if len(token)==9:
        code+=token[8]
    return code

def process_base_list(token):
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


def process_field_list(token):
    '''field_list : field_item COLON ambit field_list 
    | field_item COLON ambit
    | empty'''
    code=''
    typ='object'
    name=''
    if len(token)==2:
        code=token[1]
    else:
        if len(token[1].split('|'))==2:
            name,typ=token[1].split('|')
        else:
            typ='object'
            name=token[1]
        code=token[3] + ' ' + typ + ' ' + name + ';\n'
    if len(token)==5:
        code+= token[4]
    return code

def process_field_item(token):
    code=''
    if len(token)==4:
        code=token[1] + '|' + token[3]
    else:
        code=token[1]
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

def process_member_fun(token): #ambit fundef
    #Si se pasa un t como token, token[0] siempre es null!!
    #De fundef la cadena comienza con un "public static" que no nos interesa
    token[2]=token[2].replace('public static','',1)
    return token[1] + ' ' + token[2] + '\n'

def process_operator(token):
    ''' operator_def : cls_mod OPERATOR oper_type LPAREN funcargs RPAREN AS generic COLON order_list END'''
    code=''
    code+=token[1] + ' ' + token[8] + ' ' + token[2] + ' ' + token[3] + '(' + token[5] + ')\n{\n' + indent(token[10]) + '\n}\n'
    return code

def process_consult_db(db,query): 
    return "minimal.runtime.getSQLiteResults(\"" + db.strip('"') + "\",\"" + query.strip('"') + "\")\n"

def process_create(what,items): #1:bd, 2:dirs,3:files
    code=''
    if what==1: #db
        for item in items:      
           code+= "minimal.runtime.createSQLiteDB( " + item + ");\n"
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
       code+= "minimal.runtime.docopy( " + item + "," + dest + ",false);\n"
    else:    
       code+= "minimal.runtime.docopy( " + item + "," + dest + ",true);\n"
    return code

def process_selectf(paths,patrs):   
    code= "minimal.runtime._selectf( minimal.runtime.listFactory<string>(" + paths + "),minimal.runtime.listFactory<string>(" + patrs + "));\n"
    return code
def process_environ(name,instr):
    code='namespace ' + name + '\n{\n'
    code+=indent(instr) + '\n}\n'
    return code

def process_enum(name,elems):
    return 'enum ' + name + ' {' + elems + '};\n' 

def process_thread(name,fun,join,args=''):
    #No se aceptan argumentos en los threads de C#
    if args!='': raise Exception('Error: en los threads de C# no se aceptan argumentos')
    code= name+ ' = new Thread( new ThreadStart(' + fun + '));\n'
    code+= name + '.Start();\n'
    if join=='join':
        code+= name + '.Join();\n'
    return code

