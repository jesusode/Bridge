
from distutils.core import setup
import py2exe

setup(
    version = "1.0",
    description = "Minimal generated program",
    name = "minibot",
    data_files=[ ("modules",['RegExp.py', 'RegExp2.py', 'xmltodict.py', 'pila.py', 'prologpy.py', 'matrix.py', 'lispy.py'])],
    options = {"py2exe": {"compressed": 0,
                          "optimize": 0,
                          "bundle_files": 3,
                          "dist_dir": "minibot"}},
    #zipfile = None,
    # targets to build
    console=[{'script':"minibot/minibot.py",
                'icon_resources':[(1,'icono.ico')]
                }]
    )
