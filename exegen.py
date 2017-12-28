#Exegen : envoltorio sobre py2exe
import sys
import shutil
import os

__version__='1.0'

#Templates-------------------------------------------------------------------------------------------
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
    %%exe_type%%=[{'script':"%%scriptname%%.py",
                'icon_resources':[(1,'%%icon%%')]
                }]
    )
'''

cmd_compile='''
%%precompile%%
%%pythonpath%% setup.py py2exe %%dllexcludes%% %%dllincludes%% %%includes%% %%excludes%%
%%postcompile%%
'''
#---------------------------------------------------------------------------------------------------------

def generateExe(outputfile,outputdir='.',exe_type='console',
                dependencies=[],extra_files=[],precompile='echo Generando ejecutable para el script...',
                postcompile='echo Ejecutable generado',exe_props='',
                includes=[],excludes=[],dllincludes=[],dllexcludes=[],
                version='1.0',icon='microscope.ico',description='Py2exe generated program'):
    #global outputfile,exe_props,outputdir,__dependencies,exe_type
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
        config['name']=outputfile.split('.')[0]
        config['type']= exe_type
        config['icon']=icon
        config['version']=version
        config['description']='GUI parser generated program'
        config['modules_list']=str(dependencies)
        config['pythonpath']= sys.executable
        config['precompile']=precompile
        config['postcompile']=postcompile
        config['includes']=','.join(includes)
        config['excludes']=','.join(excludes)
        config['dllincludes']=','.join(dllincludes)
        config['dllexcludes']=','.join(dllexcludes)
        config["outdir"]=outputdir if outputdir != '.' else 'dist'
    #Crear cadena para setup.py
    setup= exe_setup
    setup=setup.replace('%%name%%',config['name'])
    #setup=setup.replace('%%scriptname%%',outputdir + '/' + config['name'])
    setup=setup.replace('%%scriptname%%',config['name'])
    setup=setup.replace('%%exe_type%%',config['type'])      
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
        copyExtraFiles(outputdir,outputdir,extra_files)
    else:
        copyExtraFiles('dist',outputdir,extra_files)
    #TODO: copiar modulos que necesita por defecto.??


def copyExtraFiles(dest,outputdir,extra_files):
    #global extra_files,outputdir
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
