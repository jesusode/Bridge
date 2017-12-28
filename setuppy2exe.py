from distutils.core import setup
import py2exe

setup(
    version = "%%version%%",
    description = "%%description%",
    name = "%%name%%",
    data_files=[ ("modules",["inference_engine2.py","minimal_py.py","pila.py",
	     "basecon.py","prolog.py","lispy.py","RegExp.py", "matrix.py",
		 "RegExp2.py","reglas.py","stlex2.py","lex.py","yacc.py",
		 "templates.py","xmltodict.py","js_builder.py","java_builder.py"])]
    options = {"py2exe": {"compressed": 0,
                          "optimize": 0,
                          "bundle_files": 3}},
    #zipfile = None,
    # targets to build
    console=[{'script':"%%name%%.py",
                'icon_resources':[(1,'%%icon%%.ico')]
                }]
    )
