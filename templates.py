#Templates

#Plantilla para codigo c++
cpp_template='''
/* Bridge generated code */

//User code
 %%__main_code__%%

'''

cpp_header_template='''
/* Bridge generated code */

#include <iostream>
#include <sstream>
#include <algorithm>
#include <string>
#include <vector>
#include <list>
#include <thread>
#include <chrono>
#include <cstdarg>
#include <cstdlib>
#include <fstream>
#include <cerrno>
#include <map>
#include <regex>
#include <iterator>
#include <array>
#include "sqlite3.h"
//necesario para que reconozca std::accumulate en mac
#include <numeric>
//CppLinq
# include "cpplinq.hpp"
//xml
#include "pugixml.hpp"

//User code
 %%__main_code__%%

'''

#Plantilla para codigo csharp
cs_template='''
/* Bridge generated code */

//preprocessor flags
%%__preflags__%%

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Reflection;
using System.Threading;
//Runtime minimal para C#
using minimal;

//user imports
%%__imports__%%


//user classes
%%__classes__%%

//Main class
public class %%__name__%%
{

%%__main_code__%%

}
'''

java_template='''
/* Bridge generated code */
//java imports
import bridgeJavaRuntime.JavaRuntime;
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
import java.util.Arrays;
import java.util.function.*;
import java.util.stream.*;
import java.util.Collections;
import java.util.Comparator;
import java.nio.file.*;
import java.io.*;
import java.util.regex.*;

import java.net.*;
//JAXP
import javax.xml.parsers.FactoryConfigurationError;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
//DOM
import org.w3c.dom.Document;
import org.w3c.dom.DocumentType;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;
import org.xml.sax.InputSource;
import javax.xml.transform.*;
import javax.xml.transform.dom.*;
import javax.xml.transform.stream.*;

%%__imports__%%

%%__main_code__%%

'''

__embed_ply="""
if not 'java' in sys.platform:
    if not 'minimal_py' in sys.modules:
         minimal_py=__import__('minimal_py')
    else:
         minimal_py=sys.modules['minimal_py']"""


#Plantilla para codigo python
py_template='''
%%__encoding__%%
from __future__ import division
#Bridge generated code 
import sys
sys.path.append('.')#Para py2exe
sys.path.append('./modules')#Para py2exe
sys.path.append('library.zip')#Para py2exe
#Para evitar el error de desbordamiento que da el parser actual con jython
%%__reflective__%%
if not 'python_runtime' in sys.modules:
     python_runtime=__import__('python_runtime')
else:
     python_runtime=sys.modules['python_runtime']
from python_runtime import *
if not 'itertools' in sys.modules:
     itertools=__import__('itertools')
else:
     itertools=sys.modules['itertools']
if not 'shutil' in sys.modules:
     shutil=__import__('shutil')
else:
     shutil=sys.modules['shutil']
if not 'prologpy' in sys.modules: 
     prologpy=__import__('prologpy')
else:
     prologpy=sys.modules['prologpy']
if not 'os' in sys.modules:
     os=__import__('os')
else:
     os=sys.modules['os']
if not 'os.path' in sys.modules:
     os.path=__import__('os.path')
else:
     os.path=sys.modules['os.path']
import xml.dom.minidom as minidom
#Esto tiene que estar asi para que sea procesado por pyinstaller-----------------------------------
try:
   import sqlite3
except:
   pass
import shutil
import BeautifulSoup
import BSXPath
import sgmllib
import cgi, Cookie, pprint, urlparse, urllib
import xpath
import web
import SimpleHTTPServer
from python_runtime import _print,_input,_exec,_eval,_getSystem,_mod,_check_py_bases,_type,_tostring,_append,_car,_cdr,_cons,_last,_butlast,_curry,_closure,_compose,_fcopy,_decorate,_itermix,_trampoline
from python_runtime import _getWebVar,_getWebEnviron,_getWebPath,SESSION,_killSession,_setSessionVar,_getSessionVar,_getCookie,_setCookie,_getWebFile,_setHeader,_webRedirect
from python_runtime import _toMatrix,_invert,_toDict,_mcopy,_appendRow,_getList,_insertRow,_appendCol,_insertCol,_getCol,_getRow,_getDimensions,_size,_toint,_tofloat,_abs,_strip,_count,_indexof,_histogram
from python_runtime import _chain,_zip,_cartessian, _combinations,_combinations_with_r, _permutations,_enumerate, _starmap, _list,_cycle,_split,_join,_readf,_readflines,_system,_lisp,_scheme,_lispModule,_clojure
from python_runtime import _xmltod,_dtoxml,_transaction,_rollback,_isclass,_cmdline,_toUnicode,_slice,_checkType,_xmlstr,_applyXSLT,_geturl,_open,_C,_getC,_copy
from python_runtime import _urlencode,_urldecode,_linqlike,_append2,_reverse,_queryADO,_getDBADOinfo,_sublist,_insert,_rematch,_resplit,_rereplace,_fromjson,_tojson
from python_runtime import _formbox,_getFormItemValue,_setFormItemValue,_getFormItem,_callFormItem,_setFormItemFont,_tcl,_keys,_values,_pairs, _socket_server,_socket_client,_apply,_del,_format,_replace,_getchar
from python_runtime import _find,_strinsert,_regroups,_writef,_writeflines,_foreach,_setencoding,_divmod,_fact,_sqrt,_index,_exp,_ln,_log,_sin,_asin,_cos,_acos,_tan,_atan
from python_runtime import _profilepy,_pause,_close,_setWinConsoleCodePage,_getStdin,_getStdout,_getStderr,_floor,_ceil
#---------------------------------------------------------------------------------------------------------------

%%__sealed__%%

class EnumMetaClass(type):
    def __setattr__(self, name, value):
        raise Exception('Error: You cannot set an enum value. Enum values are inmutable')

class Enum:
    __metaclass__= EnumMetaClass

__typedefs={'numeric':[],'chain':[]}
__type_instances={}
__basecons={}
__pyBases=[]

%%__main_code__%%
'''

py_template2='''
#Bridge generated code
%%__main_code__%%
'''

webpy_template='''
#Bridge generated code
class %%servname%%:
    def GET(self):
%%servgetcode%%
    def POST(self):
%%servpostcode%%
'''

#Plantilla para codigo javascript
js_template2='''
/* Bridge generated code */
//support functions
//js_doAddition
function minimaljs_doAddition(a,b)
{
  if ((typeof a==="number" && typeof b==="number") || 
      (a instanceof String && typeof b==="number") || 
      (b instanceof String && typeof a==="number") ||
      (a instanceof String && b instanceof String) )
    {
        return a + b;
    }
  else if (a instanceof Array && !(b instanceof Array))
    {
        a.push(b);
        return b;
    }  
  else if (b instanceof Array && !(a instanceof Array))
    {
        b.push(a);
        return a;
    }
  else if (b instanceof Array && a instanceof Array)
    {
        return a.concat(b);
    }
  else
     try
        {
          return a + b;
        }
     catch(err)
        {
          throw "Error: El operador '+' no esta definido para estos dos tipos de operando";
        }
}
function minimal_js_genRange(start,end,step)
{
  resul=[];
  if (step==0)
    {step=1;}
  if (end<start)
  {
     if (step>0) {step=-step;}
     while (end<start)
     {
        resul.push(start);
        start+=step;
     }
  }
  else 
  {
     if (step<0) {step=-step;}
      while (start<end)
      {
         resul.push(start);
         start+=step;
      }
  }
  return resul;
}
function minimal_js_histogram(seq)
{
    var hist = {};
    seq.map( function (a) { if (a in hist) hist[a]++; else hist[a] = 1; } );
    return hist;
}
function minimal_js_groupby(seq,f)
{
    var hist = {};
    seq.map( function (a) { if (f(a) in hist) hist[f(a)].push(a); else hist[f(a)] = [a]; } );
    return hist;
}
// This is the function.
String.prototype.format = function (args) {
    var str = this;
    return str.replace(String.prototype.format.regex, function(item) {
        var intVal = parseInt(item.substring(1, item.length - 1));
        var replace;
        if (intVal >= 0) {
            replace = args[intVal];
        } else if (intVal === -1) {
            replace = "{";
        } else if (intVal === -2) {
            replace = "}";
        } else {
            replace = "";
        }
        return replace;
    });
};
String.prototype.format.regex = new RegExp("{-?[0-9]+}", "g");

//Funcion para implementar la herencia por extension de prototipo

function _inherit(destination, source) {
  for (var k in source) {
      //console.log("Recorriendo: " + k);
      //Hay que usar constructor.prototype
      destination.constructor.prototype[k] = source[k];
      //console.log("Extendiendo con " + k);
  }
  return destination; 
}

//

function _type2(elem,tp) //???
{
    return typeof(elem) === 'string' || elem instanceof tp;
}

function _checkType(resul,type)
{
   console.log(resul instanceof type); 
   if (!(resul instanceof type)) throw ("Typr error: expected " + type)
}

//stdlib
function _print(elem)
{
    console.log(elem);
}

function _tostring(elem)
{
    return elem.toString();
}

function _toint(elem)
{
    return parseInt(elem);
}

function _tofloat(elem)
{
    return parseFloat(elem);
}

function _tojson(elem)
{
    return JSON.parse(elem);
}

//Esto aparentemente no funciona bien
function _fromjson(elem)
{
    return eval(elem);
}

function _input(prompt)
{
    throw("Error: _input is not allowed in JavaScript");
}

function _size(elem)
{
    return elem.length;
}

function _eval(code)
{
    return eval(code);
}

function _abs(num)
{
    return Math.abs(num);
}

function _mod(num,div)
{
    return num % div;
}

function _type(elem)
{
    return typeof elem;
}

function _copy(arr)
{
    return arr.slice();
}

function _list(elems)
{
    var l=[];
    for(i=0;i<arguments.length;i++)
    {
        l.push(arguments[i]);
    }
    return l;
}

function _car(arr)
{
    return arr[0];
}

function _cdr(arr)
{
    return arr.slice(1);
}

function _cons(arr,elem)
{
    return arr.push(elem);
}

function _append(arr,elem)
{
    arr.push(elem);
}

function _insert(arr,elem,index)
{
   arr.splice(index,0,elem);
}

function _histogram(seq)
{
    return minimal_js_histogram(seq);
}

function _sublist(arr,beg,end)
{
    return arr.slice(beg,end+1);
}

function _reverse(arr)
{
    return arr.slice().reverse();
}

function _split(string,cad)
{
    return string.split(cad);
}

function _join(arr,cad)
{
    return arr.join(cad);
}

//Si no se pasa una expresion regular, solo elimina la primera ocurrencia de cad
function _strip(cad)
{
    return cad.trim();
}

//Si no se pasa una expresion regular, solo elimina la primera ocurrencia de cad
function _replace(arr,old,_new)
{
    var re= new RegExp(old,"g");
    return arr.replace(re,_new);
}

function _rereplace(cad,re,_new)
{
    return _replace(cad,re,_new);
}

function _resplit(cad,re)
{
    var regex= new RegExp(re,"g");
    return cad.split(regex);
}

function _rematch(cad,re)
{
    var regex= new RegExp(re,"g");
    return cad.match(regex);
}

function _keys(dic) {
  var ks=[];
  for (var k in dic) {
      ks.push(k);
  }
  return ks;
}

function _values(dic) {
  var vs=[];
  for (var k in dic) {
      vs.push(dic[k]);
  }
  return vs;
}

function _pairs(dic) {
  var ps=[];
  for (var k in dic) {
      ps.push([k,dic[k]]);
  }
  return ps;
}

function _indexof(elem,array)
{
    return array.indexOf(elem);
}

//Soporte para el === de JavaScript
function eq(a,b)
{
    return a===b;
}



//end support functions
//code
%%__jscode__%%
'''

js_template='''
/* Bridge generated code */
//code
try
{
    var jsruntime=require('./jsruntime');
    minimaljs_doAddition=jsruntime.minimaljs_doAddition;
	minimal_js_genRange=jsruntime.minimal_js_genRange;
	minimal_js_histogram=jsruntime.minimal_js_histogram;
	minimal_js_groupby=jsruntime.minimal_js_groupby;
    _inherit=jsruntime._inherit;
}
catch(err){}


%%__jscode__%%
'''

exe_setup='''
from distutils.core import setup
import py2exe

setup(
    version = "%%version%%",
    description = "%%description%%",
    name = "%%name%%",
    data_files=[ ("modules",%%modules_list%%)],
    options = {"py2exe": {"compressed": 0,
                          "optimize": 0,
                          "bundle_files": 3,
                          "dist_dir": "%%outdir%%"}},
    #zipfile = None,
    # targets to build
    console=[{'script':"%%scriptname%%.py",
                'icon_resources':[(1,'%%icon%%')]
                }]
    )
'''

cmd_compile='''
%%precompile%%
%%pythonpath%% setup.py py2exe %%dllexcludes%% %%dllincludes%% %%includes%% %%excludes%%
%%postcompile%%
'''
