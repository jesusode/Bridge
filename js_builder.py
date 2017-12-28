#Esquema para traduccion de minimal a JavaScript

susts={'and':'&&', 'or':'||', 'not':'!'}

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

def findFirstEq(cad):
    f=''
    for car in cad:
        if car=='=':
            return [f,cad[len(f)+1:]]
        else:
            f+=car
    return cad


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
    return 'try{\n var ' + str(code) + '= require("' + code + '")\n}\ncatch(err){}\n'

def process_run_native(code):
    return ' eval(' + code + ')'

def process_return(code):
    #print 'return para js: %s' % code
    return ' return ' +  code

def process_var_decl(code,value=None):
    val=''
    if type(value)!=type([]):
        for item in code.split(','):
            if value==None:
                val+= 'var ' + item + ' = null;\n'
            else:
                val+= 'var ' + item + ' = ' + value + ';\n'
    else:
        val='var ' + code + '=' + value[0]
        for item in value[1:]:
            if item!='':
                #print 'procesando item: %s' % item
                #item puede ser val o k=val?????
                parts=item.split('=')
                val+=code + '.' + parts[0] + '=' + parts[1]
    return val

def process_fundef(id,funcargs,orderlist,isgenerator,namespace):
    #print 'valor de funcargs: %s' % funcargs
    #print 'valor de orderlist: %s' % orderlist
    ftoken='function'
    if isgenerator==1: ftoken+='* '
    if namespace=='':
        val='\n' + ftoken + ' ' + id + ' (' + funcargs + ')\n'
    else:
        val='\n' + id + ' = '  + ftoken +  ' (' + funcargs + ')\n'
    if val[-1]==',':val=val[:-1]#quitar la ultima coma
    val+='\n{\n' + indent(orderlist) + '\n}\n' 
    return val

def process_fundef_anonym(funcargs,orderlist):
    val='\nfunction(' + funcargs + ')\n'
    if val[-1]==',':val=val[:-1]#quitar la ultima coma
    val+='\n{\n' + indent(orderlist)    + '\n}\n' 
    #print 'val en anonym: %s' %val
    return val

def process_fundef_anonym2(funcargs,orderlist):
    val='\nfunction(' + funcargs + ')\n'
    val+='\n{\nreturn ' + indent(orderlist) + ';\n}\n' 
    #print 'val en anonym2: %s' %val
    return val

def process_plus(a,b):
    return "minimaljs_doAddition(" + a + ","+ b + ")"

def process_tolist(a,b):
    return a + ".push(" + b + ")"

def process_range(b,e,s):
    return "minimal_js_genRange(" + b + "," + e + "," + s + ")"

def process_assign(assignable,expr):
    #print 'expr en assign:%s' % expr
    if type(expr)==type([]):
        if len(expr)==2:
            return '\n' + expr[1] + '\n' + assignable + ' = ' + expr[0]
        else: #CAMBIO PARA PODER PASAR VALORES AL CREAR UNA CLASE
            s=assignable + '=' + expr[0]
            for item in expr[1:]:
                if item!='':
                    #print 'procesando item: %s' % item
                    #item puede ser val o k=val?????
                    #parts=item.split('=')
                    parts=findFirstEq(item)
                    #print 'findFirstEq: %s' %findFirstEq(item)
                    s+=assignable + '.' + parts[0] + '=' + parts[1]
            #print 'valor de s: %s' % s
            return s
    else:
        return '\n' + assignable + " = " + expr

def process_map(fun,seqs):
    return '\n[].concat(' + seqs + ').map(' + fun + ')'

def process_groupby(t):
    return 'minimal_js_groupby(' + '+'.join(t[4].split('{{{{____}}}}')) + ',' + t[2] + ')'

def process_filter(fun,seqs):
    #print 'valor en filter:%s' %'\n[].concat(' + seqs + ').filter(' + fun + ')'
    return '\n[].concat(' + seqs + ').filter(' + fun + ')'

def process_reduce(fun,seqs,init=None):
    if init==None:
        return '\n[].concat(' + seqs + ').reduce(' + fun + ')'
    else:
        return '\n[].concat(' + seqs + ').reduce(' + fun + ',' + init +  ')'

def process_take(mapf,seqs,filtf=None):
    if filtf==None:
        return '\n[].concat(' + seqs + ').map(' + mapf + ')'
    else:
        return '\n[].concat(' + seqs + ').filter(' + filtf + ').map(' + mapf + ')'

def process_slice(start,end,seqs):
    #print 'end en slice: %s' % end
    if start=='null': start=0
    if end!='null':
        return '\n[].concat(' + seqs + ').slice(' + start + ',' + end + ')'
    else:
        return '\n[].concat(' + seqs + ').slice(' + start + ')'

def process_if(cond,code,_else=None):
    if _else==None:
        return '\nif (' + cond + ')\n{\n' + indent(code) + '\n}\n'
    else:
        return '\nif (' + cond + ')\n{\n' + indent(code) + '\n}\nelse\n{\n' + indent(_else) + '\n}\n'
    
def process_cond(t,counter):
    t[3]=[el.replace('%%cond%%','cond'+ str(counter)) for el in t[3]]
    name=t[3][0]
    code=''
    code+=name + '= ' + t[2] + ';\n'
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
                code='else if(!' + expr + '.match(' + name + ')){\n'
            else:
                code='else if(' + expr + '.match(' + name + ')){\n'
        elif relop.strip() in ['in','not in']:
            if 'not' in relop:
                code='else if(!((' + expr + '.indexOf(' + name + '))!=-1)){\n'
            else:
                code='else if((' + expr + '.indexOf(' + name + '))!=-1){\n'
        else:
            code+='else if (' + name + relop + ' ' + expr + '){\n'
        code+=indent(order_list) + '}\n'
        #Hacemos esto SOLO la primera vez!!!
        #stack.push(name)
        #print 'Apilando: %s' % name
    else:
        if relop.strip() in ['match','not match']:
            if 'not' in relop:
                code='else if(!'+ expr + '.match(' + name + ')){\n'
            else:
                code='else if(' + expr + '.match(' + name + ')){\n'
        elif relop.strip() in ['in','not in']:
            if 'not' in relop:
                code='else if(!((' + expr + '.indexOf(' + name + '))!=-1)){\n'
            else:
                code='else if((' + expr + '.indexOf(' + name + '))!=-1){\n'
        else:
            code+='else if(' + rest[0] + relop + ' ' + expr + '){\n'
        code+=indent(order_list) + '}\n'
        code+=rest[1]
    code=[name,code]
    return code

def process_foreach(id,expr,code):
    return 'for (var ' + id + ' in ' + expr + ' )\n{\n' + indent(code) + '\n}\n'

def process_for(id,expr,cond,incr,code):
    return '\nfor (var ' + id + ' = ' + expr + ';' + cond + ';' + incr + ')\n{\n' + indent(code) + '\n}\n'

def process_while(cond,code):
    return 'while (' + cond + ' )\n{\n' + indent(code) + '\n}\n'

def process_repeat(cond,code):
    return 'do\n{\n' + indent(code) + '\n}\nwhile (' + cond + ' )'

def process_let(iddict,code):
    return '\n\n(function()\n{\n' + iddict + '\n' + indent(code) + '})()\n\n'

def process_ifelse(expr,cond,elsecode):
    return cond + ' ? ' + expr + ' : ' + elsecode;

def process_order(seqs, fun,reverse=0):
    if reverse:
        return '\n[].concat(' + seqs + ').sort(' + fun + ').reverse()'
    else:
        return '\n[].concat(' + seqs + ').sort(' + fun + ')'

def process_global_vars(inside_fun,inside_macro,idlist):
    if inside_fun or inside_macro: #Ignorar globales en macros y funciones (?)
        return ''
    else:
        s=''
        for item in idlist.split(','):
            s+='var ' + item  + '=null;\n'
    return s

def process_cut(name,regx,elems):
    regx='/' + regx.strip('"') + '/g' #Convertir a sintaxis de js
    code= name + '=[];\n'
    for item in elems:
        code+= name+'_temp=' + item + '.split(' + regx + ');\n'
        code+= name + ' = ' + name + '.concat(' + name + '_temp);\n'
    return [name,code]

def process_match(name,regx,elems):
    regx='/' + regx.strip('"') + '/g' #Convertir a sintaxis de js
    code= name + '=[];\n'
    for item in elems:
        code+= name+'_temp=' + item + '.match(' + regx + ');\n'
        code+= name + ' = ' + name + '.concat(' + name + '_temp);\n'
    return [name,code]

def process_update(name,elems,old,new):
    old='/' + old.strip('"') + '/g' #Convertir a sintaxis de js
    code= name + '=[];\n'
    for item in elems:
        code+= name+'_temp=' + item + '.replace(' + old + ',' + new + ');\n'
        code+= name + ' = ' + name + '.concat(' + name + '_temp);\n'
    return [name,code]

def process_idtotext(name,el,lst):
    code=name + '=""\n'
    #code=name+'_aux = ' + el + ' instanceof Array;\n'
    code+='if (!(' + el + ' instanceof Array)) throw "Error: Debe ser una lista";\n'
    if len(lst)==2: raise Exception('Error: Solo se acepta un separador en idtowords en JavaScript')
    code+=name + ' = ' + el + ';\n'
    code+=name + ' = ' + name + '.join(' + lst[0] + ');\n'
    return [name,code]

def process_format(st,lst):
    code= st + '.format(' + lst + ');\n'
    return code

def process_trycatch(tr,ct,fnl):
    code= 'try {\n' + tr + '}\n' + 'catch(err) {\n' + ct + '}\n'
    if fnl!='':
        code+= 'finally{\n' + fnl + '}\n'
    return code

def process_raise(expr):
    return 'throw ' + expr

def process_assert(condic):
    code='if (!(' + condic + '))\n'
    code+= 'throw "assertion error: \'%s\' is false"'%condic + ';\n'
    return code

def process_incr(expr,kind):
    return expr + kind

def process_yield(expr):
    return 'yield '  + expr

def process_next(expr):
    return expr + '.next()'

def process_boolexp(tokens):
    global susts
    #print [tok for tok in tokens]
    #print len(tokens)
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
                    return tokens[3] + '.indexOf(' + tokens[1] + ')!= -1'
                elif tokens[2].strip()=='not in': #OJITO: not in y no not x in y!!
                    #print 'por not in: %s' %'(' + tokens[3] + '.indexOf(' + tokens[1] + ')== -1)'
                    return '(' + tokens[3] + '.indexOf(' + tokens[1] + ')== -1)'
                else:
                    return tokens[1] + ' ' + tokens[2] + ' ' + tokens[3]
    else: #MATCH expr IN expr
        return tokens[4] + '.match(/' + tokens[2].strip('"') + '/g)'

def process_multassign2(idlist,last,expr):
    code=''
    ids=len(idlist)
    for i in range(ids):
        code+= idlist[i] + ' = ' + expr + '[' + str(i) + '];\n'
    code+= last + ' = ' + expr + '.slice(' + str(ids) + ');\n'
    return code

def process_typed_assign(id,expr,typ):
    code= expr + ';\n'
    code+= '_checkType(' + id.strip() + ',' + typ + ');\n'
    return code

def process_new(token):
    if len(token)==3:#NEW idlist
        return token[1] + ' ' + token[2] + '()'
    else:#NEW idlist LPAREN defaults_chain RPAREN
        #print [el for el in token]
        #raise Exception('Error: En JavaScript no se permite la asignacion de valores al crear una clase')
        s=[token[1] + ' ' + token[2] + '();\n']
        for item in findElements2(token[4]):
            s.append(item + ';\n')
        #necesitamos que la lista tenga al menos 3 valores para que se procese correctamente en process_assign
        while len(s)<3:
            s.append("")
        return s

def process_class_section(token):
    '''class_section : begin_class_section class_list end_class_section
    | empty'''
    if len(token)==2:
        return token[1]
    else:
        return token[2]

def process_class_list(token): #REVISAR por cambio en inner_class_list!!!!!
    '''class_list : classtype classname EXTENDS base_list inner_class_list field_list member_list END class_list
    | classtype classname EXTENDS base_list inner_class_list field_list  member_list END'''
    _bases=[];
    if token[4].strip()!='object':
        raise Exception("Error: en JavaScript solo se permite heredar de object")
        #_bases=[el for el in token[4].strip().split(',') if el !='object']
        #print 'Bases: %s' % _bases
    code=''
    clsname=token[2]
    code='function ' + clsname + '()\n{\n'
    code+= indent(token[6]) + indent(token[7])
    code+='\n}\n'
    #Reemplazar campos estaticos y metodos
    code= code.replace('%%_static_fld%%',clsname)
    code= code.replace('%%clsname%%',clsname)
    #Generar cadena de herencia
    #for item in _bases:
    #    code+='_inherit(' + clsname + ',' + item + ');\n'
    if len(token)==10:
        code+=token[9]
    return code

def process_base_list(token):
    code=''
    if len(token)==2:
        code=token[1]
    else:
        code='MiniObject' + token[2] + token[3]
    #print 'en js_base_list: %s' % code
    return code

def process_field_list(token):
    '''field_list : field_item COLON ambit field_list 
    | field_item COLON ambit
    | empty'''
    #print 'valor de member: %s' % token[1]
    code=''
    if len(token)==2:
        code=token[1]
    else:
        name=token[1]
        if token[3]=='private':
            name='__' + name
            code='this.' + name + ' = null;\n'
        elif token[3]=='static':
            #raise Exception('Error: no se permite definir campos estaticos en JavaScript')
            code+='\n%%_static_fld%%.' + name + ' = null;\n'
        else: 
            code='this.' + name + ' = null;\n'
    if len(token)==5:
        code+= token[4]
    #print 'en js_field_list: %s' % code
    return code

def process_field_item(token):
    code=''
    if len(token)==4:
        code=token[1] + '|' + token[3]
    else:
        code=token[1]
    return code

def process_member_list(token):
    #print 'en js_member_list: %s' % token[1]
    return token[1]

def process_member_fun_list(token):
    code=''
    if len(token)==3:
        code=token[1] + token[2]
    else:
        code=token[1]
    return code


#Gestion de ambit: public: tal cual, private: __nombre, static: de la funcion (?)
def process_member_fun(token): #ambit fundef
    global staticsusts#?
    fname=token[2].split('(')[0].strip()[9:]
    #print 'fname: %s' % fname
    ambit=token[1]
    if ambit=='static':
        #raise Exception('Error: No se permite definir funciones estaticas en JavaScript')
        return '%%clsname%%.' + fname + ' = ' + token[2].replace(fname,'',1) + ';\n'
    elif ambit=='private':
        return '%%clsname%%.prototype.__' + fname + ' = ' + token[2].replace(fname,'',1) + ';\n'
    else:
        return '%%clsname%%.prototype.' + fname + ' = ' + token[2].replace(fname,'',1) + ';\n'

def process_environ(name,instr):
    code='var ' + name + '=(function()\n{\n'
    code+=indent(instr) + '\nreturn this;\n})();\n'
    return code

