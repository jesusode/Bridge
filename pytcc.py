# pytcc.py  wraps 'libtcc.dll' to allow Python to compile and execute the C language.# If 'libtcc.dll' is not found it will be created.
# License: Public Domain.
# Last edit on: Tue Oct 26 2010.




from ctypes import *
from win32api import LoadLibrary, FreeLibrary, GetProcAddress
from zlib import decompress
from hashlib import md5
import os



# edit include path.
TCC_INCLUDE_PATH = "./tcc/include"
TCC_DLL_PATH ="./tcc/libtcc.dll"# os.getenv ("SYSTEMROOT") + "\\system32\\libtcc2.dll"


TCC_OUTPUT_MEMORY  = 0 # output will be ran in memory (no output file) (default) 
TCC_OUTPUT_EXE  = 1 # executable file 
TCC_OUTPUT_DLL = 2 # dynamic library 
TCC_OUTPUT_OBJ  = 3 # object file 
TCC_OUTPUT_PREPROCESS = 4 # preprocessed file (used internally)
TCC_OUTPUT_FORMAT_ELF = 0 # default output format: ELF 
TCC_OUTPUT_FORMAT_BINARY = 1 # binary image output 
TCC_OUTPUT_FORMAT_COFF = 2 # COFF


pycast = lambda obj, ctype:    cast (pointer (obj), POINTER (ctype)).contents




class pytcc:
    
    """pytcc (code=None): -> pytcc object."""

    state = None
    output_type = TCC_OUTPUT_MEMORY
    
    def __init__ (self, code=None):

        # initialize a new compilation context.
        self.new ()
        if code:    self.compile (code)

    def __call__ (self, code=None):
        if code:
            self.new ()
            self.compile (code)
        return self.relocate ()     

    def new (self):
        """create a new TCC compilation context."""
        self.delete ()
        new_state = tcc.tcc_new ()
        assert new_state, "tcc_new failed."
        self.state = new_state
        self.set_output_type (self.output_type)
        self.add_include_path (TCC_INCLUDE_PATH)
        self.add_include_path (TCC_INCLUDE_PATH + "\\winapi")
        self.add_lib_proc ("msvcrt.dll", "printf")

    def add_file (self, filename):
        """add a file (either a C file, dll, an object, a library or an ldscript)"""
        success = tcc.tcc_add_file (self.state, filename)
        if success == -1: raise Exception("tcc_add_file failed.")
      
    def add_include_path (self, pathname):
        """add include path."""
        failure = tcc.tcc_add_include_path (self.state, pathname)
        if failure: raise Exception("tcc_add_include_path failed.")
        
    def add_library (self, libraryname):
        return tcc.tcc_add_library (self.state, libraryname)
    
    def add_library_path (self, pathname):
        return tcc.tcc_add_library_path (self.state, pathname)
    
    def add_symbol (self, name, value=0):
        return tcc.tcc_add_symbol (self.state, name, value)
    
    def add_sysinclude_path (self, pathname):
        """add a system include path."""
        return tcc.tcc_add_sysinclude_path (self.state, pathname)
    
    def compile (self, string):
        """compile a string containing C source."""
        failure = tcc.tcc_compile_string (self.state, string)
        if failure: raise Exception("tcc_compile_string failed.")

    def define_symbol (self, symbol, value):
        """define preprocessor symbol 'symbol'. Can put optional value."""
        return tcc.tcc_define_symbol (self.state, symbol, value)
    
    def delete (self):
        """free a TCC compilation context."""
        if self.state:    return tcc.tcc_delete (self.state)
    
    def output_file (self, filename):
        """output an executable, library or object file. DO NOT call tcc_relocate() before."""
        return tcc.tcc_output_file (self.state, filename)
    
    def relocate (self, pointer=0):
        """ all relocations (needed before using tcc_get_symbol()). Return non zero if link error."""
        failure = tcc.tcc_relocate (self.state, pointer)
        if failure: raise Exception("tcc_relocate failed.")
        
    def run (self, pointer=0):
        return tcc.tcc_run (self.state, pointer)
    
    def set_output_type (self, output_type):
        return tcc.tcc_set_output_type (self.state, output_type)
    
    def set_warning (self, warning_name, value):
        return tcc.tcc_set_warning (self.state, warning_name, value)
    
    def undefine_symbol (self, symbol):
        """undefine preprocess symbol 'symbol'."""
        return tcc.tcc_undefine_symbol (self.state, symbol)

    def get_symbol (self, name):
        """get_symbol (self, symbol_name): -> symbol address."""
        assert self.state, "Not initialized."
        symbol_pointer = c_long (0)
        success = tcc.tcc_get_symbol (self.state, byref (symbol_pointer), name)
        if success == -1: raise Exception("Symbol not found.")
        assert symbol_pointer.value,  "tcc_get_symbol failed."
        return symbol_pointer.value

    def get_function (self, funcname, restype=c_int, argtypes=None):
        """get_function (self, funcname, restype=c_int, argtypes=None): -> function."""
        assert self.state, "Not initialized."
        func_pointer = self.get_symbol (funcname)
        prototype = CFUNCTYPE (restype) if not argtypes else CFUNCTYPE (restype, *argtypes)
        function = prototype (func_pointer)
        return function

    def get_void_p (self, name):
        """returns a void pointer of symbol name."""
        return c_void_p (self.get_symbol (name))

    def get_type (self, name, ctype=c_int):
        """get_type (self, name ,ctype): -> return a ctype of symbol name."""
        void_p = self.get_void_p (name)
        return cast (void_p, POINTER (ctype)).contents

    def add_lib_proc (self, libraryname, procname):

        dllhandle = LoadLibrary (libraryname)
        prochandle = GetProcAddress (dllhandle, procname)
        self.add_symbol (procname, prochandle)
        

        



    
# upx'd libtcc.dll, compressed with zlib and then encoded with base64.
# if we cant find libtcc.dll we create it.

____binary ='eNqsundQU133P5pOSCGhB0IJHaT3jhQpSjH0XkINEIqQEKRICSAhRIIN7CLq'+\
'Y0NApIlKAKUoKHYg\nNBUFDQgiAoqSy/O+3/nOnd+dufefu2bO2eustj9rnbX'+\
'P7D1zPEM4ADAAAIDsXAIBANAB+C/ZA/6/\nqXDnElG8JwK4Kzyi1AH0GFHyIy'+\
'dmEtIz0hIySCmEGFJqahqVEB1HyKClEhJTCXv2+xJS0mLj9NBo\nhOr/xCA6A'+\
'wAeQDDgS5W8CwAFAtzdATILgCkjgSALABYIAGB3jAggwKz+DkoD0A6wf9EuR'+\
'P1HDvov\nbuD/4P9vQPB/fXYI/J874X+esf8r/3cY3IkTCwf8J97g/0uOOnvB'+\
'ABTg/3/yJwYZ/Bce6H9x/ZvP\n/1Hf2R07w/+CBv43fxDw/2Fn/187o/9N7t8'+\
'aIf4tCvD/tOMa6xkY/zu5EloYJAxzl/zp3Bb++zYI\nDOjeefkeeSCAOhQQuC'+\
'0QCPyZnxiLOCbtD4uGYoZvMraB1P1MqiqE5Yxl7lGF81K3ZmBwJkR1AQq8\n6'+\
'qGOkmf2yZV2twoE6zRkHQC4Aijl0rCGPOYYy8LuD3MxvHcpeIOHAmgDAGf5f'+\
'NkxxIsB++nn062F\ncBzw+XC9GVV6AADYmmjfEsHi/vGIXjRVvY/XrfobjzLk'+\
'8v9hrl+AM8MlaYKZKquX1F0seVMGH2L5\nKgPNAifuCl/srkJl/mBK3Hh+y/A'+\
'lU/cg4Pn2BOFs/cU+wagbf7hz/tk0uw0vGPjq922K1/IOASGs\nP6+MwJzgWm'+\
'LWS+9stHHd+qr0YzkAxcW2UP3wL9LXbDD6MfpUgVPbYkwMgABNTKUCstISYw'+\
'HrNQJB\nDJmUAUiMB8RRMuMAdHIiJTojjpQMgCx1pQmotIxUQHyaQlw2NQ6RS'+\
'SVRE31beTPbtNTMxITUOKuE\nNGoaIBYUk+Zxlvekez8tDpBJT6RiSPsk+CG9'+\
'0/qAyEghGJXifA/w9mwcEkGgTN7q4mkm5CUkZlIB\nSUptneGDcE0S7RCdAmr'+\
'o5DxwgCs6OSw1LLZmNOYhKkAh/NO5YyMH0PHZxcmhv5ae0aKrHdPyyH/E\nls'+\
'KNw61o6xoA6sH0vNSUzNI4PXABRdKOlpISbrx8OScuLd4+NLombmSyuQiZSK'+\
'K0qXAenz8jLOku\nBv+LQDYbYKKPfspMWbI0XzSBiuZ8AT+f9VqPodBihSJTh'+\
'wfPvhNZSoGmwna/Q0Blj3QaG8c+wmVk\nvKHvLq6T3HyZbJ6eQUpIyVsf6yLF'+\
'eOz1ci502esB3+PgN7cedcFvr6esv5cTar/XbFtzQYBDpIOP\nqy8yPjIGHl/'+\
'mVLetr3NLuCvKaXOAwhUWTydV01vGYpLF4KK0VFrm5xB+PFw0pmkGK3Tn3bZ'+\
'YDDU2\nZq+osAhyiaMCFUl/gP8cL5E0qIC4AXGtx55Kbc043dMck3kuJb3wN6'+\
'ujX+ap3F3SlITOGCmzWimj\nVLg7PHlZEZASlxKTfhDWlHoobTIFeTjGlZYFM'+\
'obvfKomYo+do4nRxDPdXsUe7YGTKQ9fZKeJPM2J\nT6cd9ngbNDbMkRQtvXFX'+\
'KaHKBh7rrJ58xq4qMbshM94bFXsidM4++zM5ue3LbMdQ9MGOc1+TE1cp\nNgp'+\
'TmTNx22q5MZITUsmfoIYJH7VKq1xYUN3H9Fibtqb6lLXoRNe4rBUafD3A4G7'+\
'U0XSLAzRSxXjI\n+D2NGFCsOZIcF3wyjkwmZ2ff7vx8Mjs7FUqNOGY28vZeHC'+\
'5ORig2OjP9y7eziel4xZQUA7Dh1cTT\nV42MTUzNnv+gLpsDsgkQw53He+0/b'+\
'EzNNGIydix2DBL/Y+H5yuSMIvVfmtphd4bY6B21yQ7/P2rq\nM8XdsTv01uOV'+\
'yc7wPH44PqgNlBlriEyY/5Uq4SGfFQ2hU87OJyM1Yj13uC8er0xDo8F0ilJM'+\
'JO/8\nfExMzL5oAITev2/JhiIlgNB/2PAOUtRoNNq5f3Kf0rJDd1xo59OuX1H'+\
'8N8y81fON7H+ZeLG0Vwet\ndpgCajTk4ZWs83QK2H5H8cts4iDlY8sONyidPE'+\
'/ZLw6lv5KRaxGVk4PQq/XfPqNI70js3pGrKW1x\nCVD6c9oeF0pjZjX04dXqa'+\
'joF4LHj+Epm8iAFDIPQz8+PP6Oo7QCM6bR5vgH+l8skn/9mc25nWrGM\njIPn'+\
'Px3MyCCRSM52Toski9NQyr642EUNbEbG7x9SMjwYHUqBpKXT0y1wzyglR6t/'+\
'UFM/cqRpX3ec\n1WPKqjxz+DDKubN5A1A6RTYzM/PLs/bXEpQKOoQCzuSSTsf'+\
'HZsY3/+23cslLwlKEKYiktHmz0HZQ\nKjhaOIYUB0FuhG2EpaKQoBy0pFDmud'+\
'z90SQluFAmAvxpMvecc7qM0L6YjYnMxjIMXKgCi1lMvtgJ\nF8pLg6RCm5fPp'+\
'UVDYnJh0VAp/JlzMaKQHEmlscVYCjKaZIzKi2luRmZioeka6ZRFyzPINAo2Q'+\
'Vrn\nc/w8BXkeJ90v2zaGQsaEp0FThz37n8GixWIuCgU3jQdLpEpKQAd3uBwZ'+\
'DXR0lhnSjGQjgs4U1xlb\npMDSoXpoZFaWVBlFPAEv0nQKaYbuksPP87jBIgn'+\
'r8Tv5nub9oKIzMjLAVDrlWx46AeQFoaDP/3Pw\n/I5sp+Sgf4wtwywhFCnb8v'+\
'zGRUg6NDgi1eglikIRlz3TKb21I1CFiaku1jLHxT9BIg1hZjL8CDUY\nBUVRe'+\
'yhNyUqHwjREKPRZTy+KlA7E6OWDsXSoxo7z9PgiRTUDqp6h0Whu+UuEQpFqU'+\
'5li5UP+qz0z\n8kz9X+3+vJYhaRGKllT2HpeHOLOdV2U0BhG5j4fTb/0sk6MI'+\
'gaFumbGxO32TGf3swbPBnU7VgeR9\no+00Y9JOm82frqikTMZKQas/Dw7+x6g'+\
'5+N8uY0JVRv7TbZnR9At8ZRVKBUkXSnc5raLyH9FUp7ML\nRZea9n8TceE7bZ'+\
'pESrx38gvJ6zM4NjEFOXCd6nPndbzWsuWrXIgWYhcUlXKVH40MjwHHmpHirc'+\
'Rv\nA8BrQrEwz/nVqVhwCiAmmk6PDYvNfbZ27wCWKmoPyYAcefKuWtwYkvbMt'+\
'+EmLE2GLD3imvLeO3Gx\nMptVVsq67UC/5Rub6/qNeIuMrEOeO7ecDJhIB8dB'+\
'ctpcvmW6QXMCL+lHX6/m9cNiHiSivgxMnuKd\ntl+IgSLTv9u9Y7BHjESrSin'+\
'JDrt+Qv6aaKMKkFfLkigahhCKETVmwC4BFpeeiEowgqXyEVPKOfFG\n1ToHVW'+\
'POXY/LTqdBSbBsywx2iFK5feitzs8flPwj4y4LeSw9m5YyT5fPPLD27g3sHV'+\
'RuJD7jbyqG\nur+5bCNOqi8TQu7VLRwnRYMTlUx6GfzeuGyHePd4++SqZ3BMZ'+\
'k/UpghSRHMvxz5Nz+CMcz8sB4XU\nXzfLmGjNGeVBhqS0fRDXkQcev6c1S5Oi'+\
'1bWXR85/K4VkpkMNZPviY1oS+UqJ0qKPphcfpHuJiRNl\n65vNrcugGlMU3LD'+\
'c+vQwDJr5U274zSRuKgdGifVIwHyTnI6HZsCCzbs6s4Ti4qCh2bImYazxbHz'+\
'3\n2byc8w2mygmTkERKysHzCbmLVOmdpZ9pU57yOdMpA2Ke0bS2K8frZXrgMc'+\
'nc14b1sEsWZmbC4HR9\nWBzaYxiGFKLBLHpJfc+E4jBwmnRm86mYQihqCCYfp'+\
'WOuRD0wHjt3SnszC06Ppp2rXub6Qemx6Cyp\n3DcwcZoI7dtEEAvzcOcD8Cju'+\
'QHQmhdMjRI+VTqAu0xweCtGlU+KEDKbqYA9/wiiVeY2kZFVhaOwB\no1X2ZAa'+\
'JHoukUFwe+qbJf9oJuB6/7HwFJn5XKCv5OzlKepkcLfxMzsmLHvtInhKYcHQ'+\
'vhaJfsFHw\nEcC292ehAcCfs8xPdTB7X3Yw0Drow98rm3C6JIv4E14OEWXKK4'+\
'zXfKgxGOrj+BIfa98NCjHutn3c\nbMh/I+SrBC/l0aBD2/QYTV918ZUePjyYt'+\
'sZfUpy+rbPu27MFl4Ez5RmPUIa86S2bLyI1xgF+gq6x\n0EqqHIdyAjjBXGEh'+\
'tMYYC3+zvgkgpUNMEPMp7VNoxBl9gekJAW33/PSWj0S5uBPGQcyEtU1v7pYk'+\
'\nsEMgHvPBdDmWPYRpAmJx2y48tuKz4zZDYyKW18ebx/Ns+c+erzsLm9rVJk8'+\
'538GGPbgn4ZcEfLDU\n/6yMCLO31+VMYPm8irRn514Fvjbo9YerCb61d81k9H'+\
'wA264IsfKxjhJUT9tVVIPphoBmh3nYZ9lH\nxRc9KRWJMNDLNW9LObm2EBk77'+\
'M544uzzWp50Ch+Rj7cW7l3PuDOlz/+6s30JwjLznacSMIM0SVVO\nFWPRZBAT'+\
'voUsbReJwGLafmz0dXAs2ju70py4mJLxgqLt71DkZdaVEYpgkzGLYWzC0VVw'+\
'YWEeLy0N\ngqBGSqsVbAoESCDVAyJquPH0KdUeRDURo2qSWVpl6MNdpcEsbpI'+\
'gnXBCVrKrlXEq7GgfuViD/xYW\nn3gyvvt52+DDrrcWiz1kntPACZhYC3l7Q4'+\
'YzBbhIbuDz2c6PiClpzz9HSj2KFxpeBQ6/HqEsbKYt\nRvgEaUgpjlU3N1evv'+\
'JtbRV6vakXW/hhml918lbXLGl+2dI+26oMmM7N62SXvZ4SnVrkixNiQwAzG\n'+\
'R+D7xf0bLvyi/g6ZgGEyH2pssCWjwPgBBCM6fPFzXVptAJxZShIAakwcztPP'+\
'SsIY6K6zkgwWB9tM\nJMjsSoRT9rFgcn+45x0b1V/mHQX+GbJDmw8VVJ3SaoR'+\
'mxr4z3zuvXGQF6PsvshRepQeThxe32g6t\nfHY5Wb20JQx/jKgFrbRhg4t/Z0'+\
'GQ1AMXlvpqlIOKBCRqgNCqV7z72oHkINKoWlT8LwWV4G08dlGQ\nRcC09xJXW'+\
'lt0/nCs81eoq/Er707zGqkEiMlhT/59ITJ7avFw+QY7KZ4qj7NE1gq5NHFLr'+\
'FeE4rn3\nVK7hvMynZEBQ/qt8ac/945857VbFHzUqxXzJRcSzwaFPZd/2z5Nv'+\
'LYCywC37iugqoHrCyjTJ6rm3\nYEGGllL0YerQ33cygpdUuyRQyKz99gHC7QY'+\
'6yaDO9ix2vvFkJZt4eEE654JuMi7sXLvB7pRpHMsG\nWqgMNLHhd2XdytpQAZ'+\
'rl+DFvpX6GNN53yiT5KIyG+O5vkTBS90E6LBb19vEsYRh2TWE/Hvq5N+hC\nL'+\
'Qgm9NsNGGRsPrEAR8IOr1WnHdq81fIQoBPcBfmLMeSZnE3tMsCcuCd3rpm4m'+\
'P0DzwiyQIVgSv5h\nM96ECbUQ+xpbVP2vCrZbkmDA8MXQSIZuhKYXpjTl6CFG'+\
'S4zMwbMZ2e2BELbj9jZSZ5Yzpc0XGK5b\nTucrc/Qpk2PPFtMPyT4pU55NZ8S'+\
'kXVjjBhFd9qUsQghBeTPOMkfY7WN7gjRvMgogz4UvxOB6Dkmi\nIg6cVikmHm'+\
'nm5enLlsc0Y3rFZZkDcqhgqvTm1Ob0ItuV+KzL6MqKI+LNIdytYskuZBB/3P'+\
'VkhNn9\njhWiz+1Tlxl94Lw/PtZSWOXYg5CIiCyrvZHsw7MTRc/9HvHGLAcCw'+\
'aXiWSVgTSHCo+Fvj/IueeR+\nfJlCMsayggyc/J0XEh5vLvUuDID2tYNluEq9'+\
'AWcnnzdfQoDOD0AxTwJyc9PA/nP1eAjo8kVLLcus\n5W++WMy6QR1kw1Ag9Se'+\
'K5Htg3eT52HioROtYt3sfdTePnYkKmA5Kadd/MDn7J2RmLjjvUPYiMM5n\ny/'+\
'R+ckd3AAus9mLmlSXcij5Tet0VEdjDyF8AloAuc3Xar9tRrTdmITJilN5k67'+\
'7f5AVtJLPxO3Qo\nndnYVN67+/D757NNGC6/g+Ppduys0tS0rFOCCuhIipveY'+\
'eFK51vE04CVXE/Gr/dy2WLr9nAVVDfq\n/AqtGyDrHUke0mrjbZ4xpZSuRza2'+\
'ipP7cIeraIqhD8EI7QOMz3/qfEvK8JQziAIBxsI2odm8Ywpy\nyL/qrT2ZBrS'+\
'aa3FZpKkGvNdY/kNeIOWfEJktNff1sSrDWuswifpCZJR6zOdr5fEmJ9ZtUbl'+\
'+ZM4l\no37t3pHfzhVygsombs+ikUToLBHdI5BPPVu2NFtE/nJUH1anLuJuqF'+\
'28HZL1BeIneX2LqCn3Em4R\nHMhfC66NxQkHBsZbSdRFngqBF239sJp95PBh0'+\
'gYBbKbHPEr6O33Ycotq8FxhT6f8wDDYXRHb3bGH\n8RWdUDemyYT/WJNimbxc'+\
'Zzumcdn7sKeZEHt4XvIMgY2SZQElsbSfTEPAwOm7BhlSPQt/stKkjkHb\n4i3'+\
'h82DBgaN6RfTS2yW87immWu/Mq6INhYDA0oQX0dtX0Arz+qldwD+GXEYOFpB'+\
'quTnh99ru7Rhp\nMJTAuU1NJ5/Iejwsbl2NOnVM0XIrLj0+MsAVa7hJjGfsnC'+\
'VRyM9/Jtu4xRGJJ7jwKoD4/FCVOqaE\nD6qKX7pp0z7uBRflAIEySlKqk+6RG'+\
'SJHiLBY+zhsPtVyLPWxnCB7FpweY3M/NFRtFjEIrCVsBNfK\nB33Ejr5KXSuB'+\
'Mm7EoxvoIsE2oZqvKT/IzCCD6MNY7cXsAXSRud7w9jpzNb3Xsv9olllsjMpX'+\
'wCHh\nAO1m0h3asAy//J0y6p8TaCVC4F/F9NLgxcmeuBVwkecKd7E6r2jDLAl'+\
'LfhXWHHzXQnj65yInBQ4j\n1RDuDkaFIq3JPXZmiifbW1vT26rU4jLtBQeX+0'+\
'l7ISkgzXrkP0etxS7Rw77av8HtHnxJDTYj2pAN\nX27chn5Tty5bWYsIiKTiJ'+\
'o/kr1MMm0X4zGx4YzdouSnrcjb5lJX1pmjw0b7JXjLWc9YG0c9bH7BH\nmAX5'+\
'hPDvWFC6dnfxlAy2tKnJkIJ9I7uaIGWdV/7ufuFy7O4btcaY7V3tRdXIad29'+\
'utTsl/nyH/Rj\n+tKgBKcyat+zdoAIEvJ8dXF8sW9WqMDkjlJKmaJOE559Kt4'+\
'n731mzBsjoDX4moVN4Mh5XbMkp8ds\noYNtq692gSrH/sj24xBPh9NGxEsfnB'+\
'JGfRH5UgHmoGA0532gdpGDs8+WyDKkxpK+WEkfjdCjcLGz\ns7ljZoueYgR0X'+\
'pjiUKWkrLG4Rb7j4JRJDqbMUGb7lNArf9Df25KT9NxUbAtg100ucFwI3lTEU'+\
'wxi\nWTHm9QQIE2rmx/bIi+0dhVvfqbZYYaoheYygaFCEYZqo1stzxZTqCNmN'+\
'gMOjA5NBI+g+Mhg4vejL\npL1e6uYK7RdaHD7VNf00u0i1hQd50/PO7If3bCT'+\
'/vDZe7rv7iETtAt/w+ueuumR8GwMES1f1ww5B\nLo9Nzf0qMRBwZX2SwMliHS'+\
'/alYMwx7l9bStlcDMluqpx7hHVqjEl+bsHz3lJuCgcoSAvdAJSKaAE\n1nppy'+\
'caoUr+/0VGnwsNvJr6MzMyGfQr+/XrreC81pv+EE33VkRMTuP4I2qWKRGn1B'+\
'ofo2dqjp/QJ\n12s4Bs6B5Cy44mLhnDO5cM0eoMqVFo4oFPpjL0ceH3ozf5oH'+\
'tVc7eX37L+pQVfPkkY27D2GRWI5w\nTHXLSxAyQiPcrNZS5Y9spORkfPrQCeO'+\
'goa6PHCO5IO8i9DnwaQ0FUeZo7SPUsaP3UvI+KDJ+Zxud\ndYBTkW9v+D0Mea'+\
'5hdasvGvIVdQoeJcnzzk5OSpI+OFdIacbvsZ/R2YU26ITTO12j3E9+cLDCvh'+\
'Dp\nxNaob8O3DlUdyZo05EWJ9XwoFVjq2QPtpcd1dSYW1iLOObZgUzyjHhngG'+\
'QTRHImLA9mPPzS/BwWE\nbP6FCBv8ai7sSJyxyTsKzk0lpSanyr68pSsVe5Ux'+\
'EG/uYB+0mQynSthDKxGQvqpF9yCy6G10VRB/\nQq3nqNxJtz7ZCzDyShAiJNi'+\
'+Sk4Tyg0muCST4VZc1/dbxhrAKVK5ZI8nPqrtLhKB/uH/Z2kT3ppc\n8OUP2h'+\
'ZTaN+zoEhQZHniyaJpt0uHfP/6HZKb0A0RsKkyAssfzImefXB7nHrH3/bpco'+\
'Sj5WrG9/5E\n5tjRjdDDIu17HZgzfzoFAP5sW+7q7Y0XMWwHy9G8qk3N9p8Np'+\
'/gfsFq9PpW4kcdpy3wt+I3ZTB3f\nClAJN0XgmBx4SB3NsQDSpBxFHdbXoB1i'+\
'tDVXEBPZ4Re6ZxohVSH+azQt46DzMEACZr/RkK6ZFQEP\niNDW73g9uRhERVL'+\
'PKdZTvwuvTQV0p9zJ0J+M4M8lhJPe033L7vu2E2/ZvXif7XSxEhZY1Tw0If+'+\
'a\nufGHNuZtlJGQ2xZg0Echr01bRJE4/+SHKpKWgrbcXzoJSsdoKkfuUcE/R2'+\
'fpdXh/EPHqizyy/OO+\nBm4GVeqwQSIE/7Ts+3knpqLkbfTUw8mYzEAMIZuOy'+\
'LX7foT9akjPoeiXYI0oEbCIv3JJkZC1zMRD\n7/TNlMyzwlF/TnSNpeBzGT3u'+\
'D1dyfI3ciD0CRWR3votEscTlTSQzAEfPE6h+M6D7XtSW40DAHsgY\nJTynxAM'+\
'vNBA01fbKhZDkIzF7EBEZ8E4P5Y91tIg/F4DOzsLNWhD/Ae7aMzYF9AhMNgd'+\
'mIgkViuo2\n9/65KsiE9KCBdm9CcKi0Dc+7aNFIfWcUDdq1J9t9ctuyLxP24i'+\
'M047c33byyeTIvJSJEieU6UWjg\nyHMxWF1hKjN3Z+9fPxkQ8bIgxpz5IxnZX'+\
'gr2st5Fx/wDNuFd3tyj7xuoHxxkPaHICNYHW9Mt8pU4\nVJ3H/WqFck1otyUU'+\
'NbTS5k/YhK0LIW8l+Tas1VPGedfovs+I508q1IMK9BAW83e83kv0mmx2MNBf'+\
'\nu74LfFgD/eJUlWC4lOq1wmjdKcctCNgRIplIhErAz/ccpumKzLB8UGqbsM6'+\
'NXlQHzKXoQ7hr1Dht\nVFSgv1luwgkyC2y2nH9Q2BkZvB3QfGKzEJeo4ePbMw'+\
'/R8piC+UPsRiVeFNwPT8cYE51fyDE5fLaP\nO3XNN4dd+lOP+HLN5r4KDRa5x'+\
'j6B3GwFyUxb6/9xBnE3D+2x0ql1f8ByGlfQ0RIJ3YarwBeFH8bn\nCP9TAfRt'+\
'V4c7ZupmvzDP7nJNfMt8Vw3d9t6rZRXWvPAU+CTkqOuLp2BeNruRWKw7utdb'+\
'R7IhNWqd\n8Gy7+9yjWHRGWgpBLdNKLdYKARAisKD1ZEQDGlLyGVEqBK3pCmH'+\
'BauGqwMAni5dMOjyFNzZQQFud\nP2PnF9UjIJxVnQf1Rea/8SwwCgWVHyQeMf'+\
'7+t0tPmmwfyOiD1P5J1L84c609Y8JbBlX6EnOkzFOP\nX+1jaKpn9h4EG22jR'+\
'TvIUgw6IkdZZWfNDV+bB7qE/DZb7Dlua3vBXtYjJjkddymzELGrEpKPe6BI\n'+\
'hQnK5q7VBAraSvJC/+YJRoOev8p1UJ27U/qBedJ9Nb9l/5re5HdEuzKxV2dc'+\
'R8JJ81X+/R5CByfz\nAyfMpPdjD7gPJbj81MlE+DpHz88p936kOd5XjiUvqyN'+\
'f3++0yWJcBFBFylwj8cZ+X3/boGE6NzUl\nkc8JNzVNlfY5b84c05IaVzLA06'+\
'mqpObQuWKOEhWaWZlKKlgE+iTyv2qoxWi4D4JmfPosoY+iRol+\nccsT/bsPh'+\
'NzPKKRkkWhxXQ+D1YTDW6JBHidHmv8xOGGg+j1wwCWwojDddglT1LTV5I+tu'+\
'Xm9CYDd\n6IepfEeLURPZroTs+/ct3u56oDdXY8Z04oEVeXgoPBc34NQDgMHz'+\
'VTQ0UFgwNPCx65iRxjM5Lbn+\nPYr27h/qio/jhIusqR2vIK1DCvFZy2I13/t'+\
'OMeXF5gzmYTw06jPstDQ69JXqyuPjyuPggPsZitng\ndcvxe0H5CtJmtIY3g/'+\
'wgCDhAa5TOb2/vkDB0UGRLgPI+vRQobiW+v54KOeF6MYH18eVqFlK2YIVq\nY'+\
'BmCezTDX/rDEOA33zL65W5Y8pjjP65ianoxR0852c+m9Lqv0GYmH6PaSoWMD'+\
'LL76zmZ56urwfD8\nPFQtWkT1vWgUqhCsKhc/+YFtJ4lV3P3Q7ms6cPMxVWc3'+\
'zulGgdTtdKbKDASo8rvcU/oLnFvqQuaP\n1xtp0nLgatdnWEIsBcBk4ydtFes'+\
'AyKU+ltSEteMXhZUzUcdjSvdZBwcdLvExvMQUbDKD5+bsd7px\nj5CMJSqI35'+\
'eqIl3ji1of0MiP5UmEjmEVBcpwIfPNS3Fh2yKz1Ah6bt+ztl3nnM64vD7d2/'+\
'/S3ezM\nOz+Y3lhl4I0avadGmw3hxcR+ez8TKp252ZMSijfpHxZqMuCsTKvMt'+\
'O1a3ACF+lT4L4a17EykAtZR\nWwBP2poNEhaKGfNC8owBg1zCooF1tnGKxhtO'+\
'jbRlrn49R4MscsR9nRSZapRnEMmf13dPHYv6dOUn\n1qC7racmXyY65pMazc4'+\
'D/MwU981DD55AVrjLfasBHDKWC7pUEFrx8NBXzwFLEypB2EhfV1IPch5z\nWJ'+\
'Zq3ifaaTJ2BmBmCHaMa0R0mi+YeYXexiPmzGKw4CRM45P4Yxikr/nTyTVkLl'+\
'jaIl1gVmdymIzS\nyLYKH0IppS639xlczZC1sbEFdMAndz1HLGHt7AK6bMRW8'+\
's2zOeXyov3SSoMGFpsLXXajXw+NPhru\nfycMs3hVGMTIbY4R02DK58OWn5z/'+\
'u2URzDJFhrIjgMYFDvoZQ4RQPEgK0FfbHBNtRnB+OAPsbOKJ\nNEUG6R+co9S'+\
'Ps+xoZ02vnnh+ru78StHWUJQy05S6iJfcDmIJ9SyA2ManLH/kGVquh2eM38Y'+\
'qh91N\nHTuTE6L+Hg8RmNRK6P7kjTmtBrmE5H3ht6V58a4VbvnkNyiNvySqwN'+\
'ZrgMFBefP8owFPROZKliPM\nCYIsyIMK7GvFVlEhzn1OwZ5CZDYyBTt78R506'+\
'mvokDfrQrQjyHJsOZKRFtILLrQCgAyJFaBLztP0\nkuUKR6CQ0ogyQNZ8Blr5'+\
'CF2XL+HMEv/Guyv25yRXDq+WUByu9ZZcIJQp0kJbyY5XeEg8cSRKfDIP\nfa/'+\
'3UA9W6gHnyxisAT6K2ZDsX0ldKWJR9cQl6kWTrgHNZpigHkcZibTIF6ezB3B'+\
'5YCSOKe4fc1NM\nJUe1Ge41uxpylj+0XCq1nETCrKpYYqnCYTzw0vW3P2/z6+'+\
'JzHkSiTo9yq5MonWKZJ6YUbc18vd0s\nLvZHvHVAh+diwzbUCCLoBb3vEJqea'+\
'9H7re7a0m9wDFBBvuijor1KWxLvQjlViu3mD9RVEQ1RnRVO\nGn0leXHl1JX2'+\
'hWTueHLx3seZnMtkyfcaHWM5aRHMngKdPLDEVzCbiP0mvxLPMxMFoeRey60N'+\
'OMhB\non+CHyKYg7qBRWmgPtBVrOVv6v4zsXOCLsRGTy8rA0fTYT4t+riVMDc'+\
'XK/e+VkOMopjFBdYVWm4P\nSxxME8Pkr9JahC2qXp27rsZ8p9L3jRaIXxCTP3'+\
'7jSH9IenB2f/HeFW8yQX2icy+MmG6uLw9r7r5Q\nlEW5udGPDgu0e08s0TwnC'+\
'7JqeBT6shb4ot1o3VMKuTqGCUhcjAd8MypnsUyKm0FUryhv+SC22h57\norRd'+\
'SgO53fpQhrO+x/dg2MPIlnxCS0UA0WJSPJdSh4zMtkzBEdPZxXIf2ptnWoz7'+\
'EWGOLF+I5agq\nK2DU9GWuSCqYUt1xhP/t5EZFUOJbmP9KvXRFW6LnmjVct4B'+\
'08NE6coWgEaZR/J/fS0RSIny79ncx\nbNWIYcIQ37YD4FpZBILtEAiivH3Z1Q'+\
'q9E1avNFl6b99rexSxYfezqGNo04J861rXvCzEFvUhv8OJ\naqGGoPVr3RoFH'+\
'xBIactzYmZotztLkPxL9zk6cFoN6oswj743WCVg29oRkoFXfite9yLpPePXb'+\
'pB7\n6wBkM/pCLMBa+dbmnXfu9vVw/qx05ZumlrbQe1KzUdCE2mNzdvq1V77u'+\
'N5xehjtUAHnBbavO45Vw\nAeNz9IBCGO1jGhNuik3/sZKsSBt1ME6huoeJv7t'+\
'nSaF1iKnSbgiOBfMohFAbp0vd91mdhx/vO44h\n8p/WN73sqxa/DOS/AnijQT'+\
'a0VFeCH0rsvgMhLf4fwv5+0N1dKQjAslMFWPe3SdrYKOP319+7vjMq\nKe2/L'+\
'0g7SYm/giYwzprStLh6rbiGeJ5wba+Y4J49+s71biGdy/y6IdumE03LS2eSL'+\
'X5C9Kk0lWLH\n/GVk226Zl0UVVqSraSOZVRA0pnS/jFRq+pERUdrblACHK/zW'+\
'l77rg878KdG7HCcBBedya/7mqu07\nMtJOdXdKYmbmbQKgIA1thEglUZFqMQR'+\
'364voFFKMqwYig2RVqdcZL5yH1mARE66nneG5cM4pWIej\nJmpXe+tPb53aEt'+\
'gztr6bpn9zclGUMhbTZZzIvfieMwwbxrYKPuhgMWimLL/ZP+XoMG47MtzTxG'+\
'Zw\ndX6IesLC1TpbbLM8yCOA7n7NanS3euDfj8fEvdKNYwyQfVG83ocGGkSZY'+\
'wK5eKnT5c1hafrNCZzy\n1MHb08z2x1mhWvH6VM8jEqBdWeEpNkdDBo66HrXO'+\
'4bqhx0+rvrBq7+LfmLIH4TBH3PQDfW5Zy8mt\nNgX6vHhmZLci1/tOeU1B00h'+\
'e7Lz7CvbdbtHQXtjE4OT3aXd3alR23Ko9DANwqQCkwx6oRAshXqqq\nHFSNEf'+\
'ZlGL65qbmRsLQ6meRrYQg64YDVPjjOT4U6poCjhMBOFvcO6wLcHRfA1HN1lE'+\
'H8gvWmUi+x\nBGyTRZX6O4odcbiyxnF4/fhWDXe/ZOzk97LN5IuiQZ7SUbaQ5'+\
'uX5+WULWzuYoe3uXbZggq0N/taL\nY/MytrZicI5PKJQJKvDir7vwf7hlNjlo'+\
'VHgEfveO8vTOit0td2r0UJRNLCMMaNOh3F0jxDTeRcXq\n066a2Wx2rYfuuno'+\
'GYTsaud+BX1hX2sPmyOFjscj1vyjnI7ePwICMXvr8sPLooD0vqNHtCqhTthL'+\
'Q\n6iv32CwHQwY9eHPwZMIvoXQsVSI7vrQ+AZfnCU4mtynp7IO4XwZlPF89sX'+\
'BRQSgKm67zfFVHgorL\nlrPAItbznJCBjilJJUQXw274I3Y63tAm4AGC1+bNL'+\
'Td7V32o/UiJxWMF8Ke5B0rqSmciTrGk8sXE\nQ4r2d0BON2Kv3QxTdmqk75F4'+\
'4xLaTuHkKjoZuzTxWhl2UpgqRdPDnhFMG9tjsy8dU/D3iwA/7/Wk\nPt4zXOp'+\
'sA85GOoPHYt2lncFkc50SKp7opHIVhRoiZyuMKJrVkwayxVkOEONRsWYnWBm'+\
'/W/p8nRh4\nsR2TLhS2S4cr7miDs/Y3vvTAvsCYrXhY97ToDFKcJcbEMofMIp'+\
'r/spA+ggMQA2zOwNb9Hs/sUnNb\nq4JV/oMK+JSq6xehhldJR+JxP8snvMhXQ'+\
'kx5f7Ugpyra2UZsEJF87yS+3nXDlEMkq5RHiWvMKRsS\nu7VZ+VzrWdGi366H'+\
'8NaSYHGHCuOgMo7TOcm9FUBrfflqbdHwvtnT+wtbG7JeszIp+2bcqz81IeKc'+\
'\n5NGDuh9+0B68AuUQOYlt36/DLRv+EbJvZNg5Fn011YXI3Tv3wLo3ExkJAbn'+\
'Bg42O18XX2FHALoUN\nXwNme7y53MLiq1PX/cd0D27TVtiHpUIy7gaHKsjFuN'+\
'5XHAR15OV+4U9wviPcogB2nkDd1BC1zDg3\nAmgiFFhOSE0Dg+BBTXDFHGAy6'+\
'cYJFQO0EOg+eAAXsLtO9Ljcfg2HoJmQB5xcN2pAXvVLmjnLW9cI\n7nNcWS4K'+\
'0HPGu6+dy94XcPh4psS1oWtuvKCWG1d8l5IFxgo/iNqh5ZParunZNXjTWx8a'+\
'OTMW/A90\nXKgza/hS+Jwq0KttypngloteXJFhyZZ3s/PnqC721AsLQv2bZ4u'+\
'Q9nRbbQnmww2t71EtxsLpR/P5\nTVM6zpNRof/Y07hJY/FLTo57omqEPsyRl6'+\
'JFMYGQJ4VtFQf626rn9lx0qqNA2QYIHhom/xIdEqv5\nIrrjGnfvum9U1E11g'+\
'xDI1SFb/a3SRsa2JlWygSn/JSKA8PYH10cqmH+z6PeMfsd9jbJoUizlIOGu\n'+\
'ZU4SKWaQ9Cm9tvNa1b53VRQ6u61tD4MEl0ppYER39GekScrqsEpFujE4lq1P'+\
'kUCv4hNqui8bGDYb\nzMLO3/FngbbnwohAcI/kXU247sl++6DBfWLgn0+Mnva'+\
'G1+to6SicTQ7W3KfNnMDLOksV+YLTAgI/\n7HX/h3w/fTY5SKKa8ePA1qV7W7'+\
'wgigzKC8LuZSajbYXfa1FJgr7Hss1jGIWireEzOUUbSGjaQHnw\n4qE9OQFFT'+\
'8dOy/dO7cmQn2RPORwPjuVKMIx0bs2CecE0zEctWt3jDGFN0f0SezklY770R'+\
'sIs/7zi\n4J+F2q2jXe4oLL/sm026qyzJt2rvlkKgREQIcNPrIdG1KVRhRkW0'+\
'AQX5+kmehe9ILeFqsU8KzZX3\nhBQKOX7UGpV9QQxNLp3SUsfTquuRzz5qmNZ'+\
'Q7iP/vMX7G7FcD4Zx/mAeRlpeEm2fXaFC8/kLTrMX\nIGF2wkRacAhzgjafhL'+\
'ugGmX4kr/qydUpLttDSFL5XAjDBIilK6OVwqDS1lKqD8UToq8I3ZcePEex\nS'+\
'tK8Y5DuduIv9nop72Jys4Gt8/hK4pDYuC2SikS5b+u/wJiYprNdxjD0eWKt3'+\
'XrpCu2jF4tRiTB9\nIOPdiYVrNZE61syqFNiMctYx1YIMxbpn6l3pHmIS7J/n'+\
'KV1BjsYelmhIkg5q/XH/lYirsslelOtR\n7wvpvV9U6MP98YVwJECUaKEjuZe'+\
'spHnb6qKft41KtDoQ84VNVe/WUDEqKxa6uZJJUG7OGgvY9HLw\ndFYO9LBB29'+\
'3yqiaMAbT7BpKvJkHm44PT5MwlJ0UynGkZKAI1TczU33019n1qXIOSThPghW'+\
'lyYWZP\nAk3EY+jynWSR02HRl94lxoN1OK6J8Q5mx0ub8AXprbpik+WtMXEpz'+\
'kjNdvojamJWXIBapnGza481\nAflDuAekAF02d1rBHse+ApRX834eyWeWzm0o'+\
'nViA3smQVDwD2L3b/F79dhS7+O+2oiPzrbQYXG/q\nM8FrjqgFrgz4hlpTdtu'+\
'/Irr3nclzsH/I8rYiFTRy7FugNTg3yPy27wusuMLeRyaFon0XuNZp0lgE\nbZ'+\
'VVGtcLLOqrj610C2M0zvOGV+TnoGxoYfQZMnEFsosln8VKY1afkGEkQzZEAY'+\
'rZBFnazgl5e+PO\n76tePYqsB9qhrEA4n1ujMNcbCKTqrj8F0boSPvFEWVDGC'+\
'phZwq/f44lb192tURrCIo5L7gpBAu3A\nwQ84zDo2KAZDBOkSlilVXwOuuUDG'+\
'4LaDRncqkSYobQyu6ClaGZIotGtkpPIvv5vxy2Zgyk79EviX\nc21cmzK8qif'+\
'SW8UA/7F147vB9V0++zNMHdw1CdZm5fnE4U9an2xcWBuEs3tPPmWfkKsb/ez'+\
'm8Jb5\njh18/OkGvgp4CF34INrmDehvBNca4uRJToeYh66eDX8QeDkmAXO29f'+\
'gz5YvoNlroiFxp+3F8Vn4r\nMys+VxE6Z+OeDTtyNOk7Vds3FRJ662OZaGnlX'+\
'/EH0Zdz5EjCmKnShR+WDrUrlyQRJzpPXpM2e4nt\nwgF7R96mgFNOri9i2HWW'+\
'/UJyWfgmSTVUTBNxemMkGsOAg/Ikv+GducWPRO8EMroXYkeswopCqFKz\ndI2'+\
'7ltY0s24rpIt165jf80NF+SI3WA6BPo3lxDyH25RDpPHtv9PvIytOfGKzZct'+\
'95bzPgKKagu46\nyXe1BUJWpI5dZ7lCINFrxMGwy/uHNB37p0rN8AyxNQ64nV'+\
'hlv0gliv0gFwN4YY9rJIAmg2V2qxcf\nPm+y1eq9JJF3pe/86bGYGdVUTLVfk'+\
'j7U2p9Eyh1dbI14ElmTJqoUFsbOYNfOPawpQ91xB2dBu2C+\nLvMRrC/GvBhv'+\
'rw8GdlFHAh9sYEUeiayUyM9n34TDp5A+iTUl7ZIhlNSU35GpoY6d1cp92xk3'+\
'Gram\nFumVCD/5wvvyP1LtNPKf93bJm7Md/hLzf/r0/knbK/SOuop2rnXKgzd'+\
'XEsY+E61L66vsVOrPUa1v\nmr2emdqfbcwca9UatN3+Rodf1C5XqFQY39nUUe'+\
'HTI/3gBOmKEf/EV/eANG8gknFsF6C+rAFXtVqg\nwVL26jglTq5cbqNBYR3Oo'+\
'wrX/bTi9TRHs3L7fUQHRAyIWLyxYqEJtcT7t70c5Q4eeJxoUO8f1cJ1\ngh9w'+\
'Y/nEnQC3nFvbV6DfAnS3ht41AoE/seyUHi7D193+kEIerfw2JuAtHlV6gYK2'+\
'quReXgLCrYm4\nrEDGVwjrF6XFbFqyGxv460i+dBhh1etXtAR+wF6imHt9XUq'+\
'62isE12UB0Wr5eya/QL7y4CnGNsJX\nWLQj2AyuBCjabulOQ8k+WtvU/AnHzM'+\
'deHi6d4wZEYuNpQ17E/YdYlhAhOfZpGVZfYIeDem21j4Os\nklaWi2rQ7glrl'+\
'EgT6tixaj9XkVUWoBhAzUcNxI0OZTOHmAOxl8dxer3aJ0YnzXBa995sOd6MN'+\
'CBb\nctdwH6n0l98gnXWBBihvySYr3EwhVnuGX4RwUFCXfJFYYYCrxIil72tA'+\
'JWBQ8qakizER0X2EWNN/\nzFTJQc0e53fla2g7Gu3xIFQduHIyRKbAMtnRjxV'+\
'1nb4rLtiFPX3jEDfuAO1RGU8ZwbXaVwJQJAD/\nELLVsjWQhVKt5NllXfKLMg'+\
'ka6pr0xeOsyZILR5seRwnjwMboays39tQeiXgUUue1Kt6OYfmv8Hvu\nOkPBJ'+\
'upO5iFj3J8i02UB/3QAOaEbhOBKDsQCHGozxKK0iYNDFihmg1LWkeApSFt5p'+\
'ri7vNNeY4JG\nBJmBMovFZAjllQFU/hA4Lmzf0axR86h2/E26pIjfKwxU5M+5'+\
'9t8uzFdfAoNNu4RNuuA1SaplF+Fn\nkF2vapaa8OIcm5lwupivWUyzS2zQKFR'+\
'WdEX1mOc6f7ELtQ8hjNaVNxoSRroIOMvF3ZU1F6B0UQY/\nEAphS4A/jXu8ce'+\
'F34brh0fX5y+b8TxiucOfe5ApDPZKEH3+0lmZfu1fKeWWlJcmNjZcdPcTl6R'+\
'K/\nzGgPON+QMhHzSXtd/1UYgAl4SKCFYxciv5RYaotHSxyu8JzW+6vm/2pWe'+\
'IzlqQ2pqmB+F1zyrp/B\nveIz8ldOFqSoSbT4Jktlc5GS9dFxGW+7/FeuhYvF'+\
'JWDbosRKpw9nbRtE89DxsvT12MSERKrIbKg2\n2kCDppG5nq6cG2sM4ACo5BJ'+\
'Og5+yDSWYm+V9NjUOfsDg8M/FTABgxUHRhkwYI/wjsJ2VmnQMjEKK\nwWdF2H'+\
'pSqcR2w7HyE1kXd71GHr+yAKsLRfSW/S4ePw8zgG/rjTG+kPRmetuNoUxP7o'+\
'NuUeeFQDB9\nZnu/55ylR75+Uf7unIsZ4W+nFebC8v1fV2iUgxxVc0rbW1qRD'+\
'GF3fiPnQMb4s7djepcKhePCYM+G\nh4ycfdLlic8mtsLdQAde92Mu3LjYSJQf'+\
'lxKdO+X3XTpFAy89+ogyOHDjZpBdhthrn1mKmsL4aGnU\nodCeTv+H32FNtO+'+\
'PNj5rDGIapxsOFI2ZdjDyR3MwE+28mkczbDmw/OwpjVFm+H25tmzexC7/bX+'+\
'o\n533RDcugvPYZdfqlDKilfeaZb2wns+0GwyPWF2btD8EYKbOrFxh5+xegBg'+\
'p5x9T/KYN2SKS4jy69\nEB4pmphkKQ3GYF++QzoURYiPfoR63/TtHLqF9okm9'+\
'TWuBHJlMulgGkEqOzY42uOIP83n6yEFwzrR\nzFa27krmG5WuMmeq9Omm6p5D'+\
'uaUXDrmUOdZbFSk+XD9re+CJ6hRy8IVjxtQvHQeC7WDO8BWDr8x/\nTjAVqE7'+\
'CC8294th0/tKB6jOpuQVuLlBQujOATSxMUT7p7E+K2Ax6BlscFKe9ZTxBDo3'+\
'CDmY/1F+5\n+edO11jHGF2YNNxSkIW5+VEpYcZ/VaSl0FYOeJjf31H6IfaZdN'+\
'dHZP+koqgDloqAjmfXNoCUr3mT\nlDeTdVRT2A9VMcf7+qP+wPLCYtlheFBmk'+\
'K+6oq7U4/3S1NdjauGzvgZyS28RpcYk5Me4p9+z+403\nLIAfqaIze0ULY0LD'+\
'MXEXOmPtWkvO/9aungQ63GPLbwJMdIXfAgrXSzbqDLIOt4t8gJzZ7ZKB5401'+\
'\nOhIH5T8ITynL4r9nzUa0+hB1/RqIb4Vf+CxNP7hrtxDYGD6JHR/S+iE2iTb'+\
'lFrwo0fSa7pmSU9U6\ne4Etzo4lEfL9vxKivDdSTrj8MpjyMP28SHjKnYosl+'+\
'gJfYke4tl2ao1vSndMzeEwJItFvXXLAdRu\nyx5p4en16sVkqyVE6Hrd+8HfU'+\
'fG2R+U51vPndfcDp42GA/kDtgx5N85bVwektXDXyMJn84/8ttis\na2UKq7fK'+\
'rra6AU8BWl1KnKoYu2WLw8TKqg32iqZmG+8CmLlQXW103nsXq+D8nFAa6jbU'+\
'+27nCKdX\nYnuVe+5RApIGSyQf2XcexoBcf5AeVWMYSb+9yUeegio84faRgqU'+\
'x6nBflC7Vj0zdj469c4xPN7E0\n0Ks37TM7eyvUP7qGEvRiKPpsBGYeNjiUv/'+\
'jLwmH81SkKv0L9caGeamM0F/elDPwFPhd7vvpX+afO\nkufypZcNRA59E2kB8'+\
'tRw4dWUYJ0br5d6w48oZFO1fwftbSh0wfm60j5l3gQouo1FjzkehT7t5GHy\n'+\
'1e6deO7XeehzcBbnm+pJBdaYApZfJP2Iv/di8IRQfP2n2L19oNSY5y4oWPQo'+\
'CKWrB4gEDPW64Jl0\njvtj47NsQJwmWIrzbW9tvBjytrQbPS5NHLyBf1N6dsT'+\
'RSWUDFXamNbDtNEcpOwrScfHAvU8yLQR7\nSHycfnGUSNbP2BV7m4vnjol/h8'+\
'C9y2Uqw92a6wjYeCgCVhpdaG+WLNl8UtY7S7ZYOr2w9rqKxVhp\nNxAaH3djl'+\
'3yZaBPbo+Zw47FjIwDY2ORsTlm5DFDcWhnS0GrhShF6fB6bD+8pB7THcwqpQ'+\
'rkJ4OQP\nSBHTxsUmvAg4ebhpvIZShHdSGTbn9exBf/CLPTYHCzGTjSgTGK44'+\
'AIb7BSq6Q65j/pjXV4C/sI4L\nzFMN/vD6fYS8vye3p3YXWbVNRsCp6s5cJFX'+\
'er64oaY81W3zkUcPv2PTLacz8xo9J0QGnyM4vXeZc\nmmD2WNMLPwCzcNdNcX'+\
'axQh9EqRCQ2vTUWCWhiUwAU5AAs/GjmtKaYDRSaSoM7+IkM+m0qhJGYYFL\n5'+\
'dLUo7Ttz1teQhB92Hq4HrEmH8PX5/1nJxI4asq+TnB82/eKythhSRSp7k242'+\
'AL//k1oePwumSMh\n2Ehis96fiebLur+BsRBBjvPrsN+MPM6mzvb6trGdL7A3'+\
'eWKMHNfXBhtHCDgtgYfFH/YuRoUEy1tf\nCKQfNpqIuxCnnZuIUptqUUnMAyd'+\
'XIStGtHNbpMXByQfD19VCo3aqdtA8KkzGqSq3NR58PEe+ptXv\nNq8XPbAZr2'+\
'A4dCQIN5VzHZ3efBRPfeRiPStUWGOOqQrTHASulL7YJ/FFWdLN+T7kA/OdXu'+\
'If0Etb\nHj+JAk4WQ1K/3F4c2ZlDgP/MaQmGO6kIyg0r2wLdnaqi3/8TEBxB7'+\
'Hukkkd2epEX9CSks4bZO7P8\nRHdbpd3UyTp8uMDo9Rj4A91g2pDcetKpZF0U'+\
'wFTlK2PtbK5pfo/2NewC9i9pxvC5F9ST0otEQ3GX\nxK7EOqdRZANu6e2zrlh'+\
'KHMHMzZNHl3W0XI1YPYMJsXPGswcdHXuzj6WMJzLweb2S7Gut786L4+lv\ntC'+\
'hmpOJeM5/So0KDCUIJQjDs9WsEeLdkt9+BfWMucdEAT37qFF7fIT1D6KA4LR'+\
'VMwVSgL9JoCW/z\n94c6LF1Z80rL4rvoKDhwUy3uqu+uSQc8RcxYF4vMaszGx'+\
'9GPZ7ZLtLld2I1LPejvuZ5gr2ZgFGsF\nATQ+aW27qgYDC4fOwtNhVWHSLsCR'+\
'MWhOYC3c1hWRpyv6wNSFsnmg7AEo/ET0K1usc+039xwLgdB3\nFJAaIuGPFRg'+\
'JaCgP0CZgd60y3uyhyIv9OAtcIBNUrmeF9X2zjtbexAbQEIZOD782ci3Dg/l'+\
'8+sUX\nfp36Sz8YtbSA19jmyXBd7R7mMcn7mGrqq3sqL2ShLKHdoHKpDkqKBL'+\
'9LV1PtqMSfvbRzyjGnv66f\nOzuS7eZ5NiOhR2jzU0yAD7CYNhfgKOL2KWUTA'+\
'xeZqJg98sBqEmFVMaqrQFUL8xnFdsvxAxj3gEeP\nD3HcnxJ8tLKd+FMpAOVU'+\
'/yufYSwhqGib6Bt2DdERwKMnSOO8WAUSVFkhHXMp4O/LFPtV4peai36h\n/i8'+\
'hJm81LZrBtSxTbR30uWQxLU8cvtbZwONajUMyhWj8+eEZnctnMfE2rPyz542'+\
'wpK2ycSqBFYk7\nBi9lBmWzbn2NYLq62wJFfEa/zrxaThGTjOhRvQCzOL+Zt0'+\
'JlVH4LREElac3kBK1UyQNqcQRcPOu0\n6inzS8fuX/5J4aR8Oqz6wnFtlcIMO'+\
'bEgTNX82vfZ8tKRqwoyilCvSK0oMb6Sc7P8T8aew7Ps8Iu+\nf4djXBqioVcI'+\
'MwGXenlaodQDGt4gvDJvBl7WkkTQvdyO65Y8CAY7BtAeBURZGPhU5KWbHFE/'+\
'aZO5\nyzNwA34FBCZT//zsLOcGkN+wAyr0PQMUn+6VgFKEqDMX7ylmqGPZkNK'+\
'D2LWb28qwzrR51nRRX4vz\npgcP+xN7CZX7WWRwuPvZBVLa7+WHAXI+7+SKCG'+\
'e54ccv1gpHUEElh06i2r0CjNll5lMtI8LpCweC\nwBnxyKidVa+2syR3lvxIh'+\
'q8V3snD0Wldxdc83nx9CEe70ah00lrBzVTQkA3hUQMApyzwE6g/uuKP\nJoJo'+\
'Mbr5eHzpkDNlO8bz9JvW1klREOJoIAfVUjh/QN3DJcjw3aV6Y8ndmSqQDrsF'+\
'hA1KQ3HimuUN\nxdG+7YCl+yURb/TTuZptqV+ueBKA/HeuY2eElceUDG9V20W'+\
'88ZXI2CdyIOxAmP4H7w7Z5/daKZeC\ngIlrFxNtLSpwxgOwFR/Dt7DXuMKmb3'+\
'bX3Ama/HNcharKx18lV5qKfjt1F/cRrq6bgKj76D3XVpJc\nw3WC9kRl2QNOH'+\
'3qiPufuNQbpuVPBs+wxGa2oLVdpPVvUfs/CLnl2nrYQEDgPOSmXSYxYw0LUJ'+\
'UqL\nIP2I8qv5cuYrj2UN7XohTZD8lsgbGeWnEWOFJxGMj741IbJc19YXHr9k'+\
'Zjj7wnV9NORGLg3xG53O\nEDCM+UlChnRSwlZLOhEu/COC8WEbsWZIkLrkK8S'+\
'VDWByvb/oGR5DyP1x0GR664zGk53KyWZ3B4mn\nnb1ff32NTPrw64ejhCMQVY'+\
'jdpUBUFQ+Vov4IquOf50DFnA3HscuZ78IlrlSUh6uQwUlZGA2yEnGB\nm3bjh'+\
'T1qe1TmTwou6AfQv65ehAVD33hpaMXabcnZUrqUUlsZNnA09iZOrMi9bbjMD'+\
'wvb/+zUkn9Z\n2oI2USt4UbiRBqBZlzTb1kXLe1KPhxA6cc3FNgWiFlXFGYSB'+\
'oXVF7lEE7dl9ZpeSxNUnqSk9Quh+\nu/EwTmdAb9HTMteV8m83PJghkBPXhor'+\
'vOSWmrhIK7UQPg3sy4pxI5b8JiXfPuQdwlQgbBePjqqFH\nawKO0TjPbtP3P6'+\
'VazrAdUMToM6qjqnvUiu5yVnuuw7VPtNM2tJKi3kzuLnrWmKOPmQpwCMyFF7'+\
'mh\nXjxB14HlOyPnfxamN7SoamWU7CX3pvlSslJwThYqTelh4riWYhR2HDMVD'+\
'93nLKm4SbxVzNBx3cwq\naXyd0m+mZH9FafDP6dRr+FtvO+k/rrBt3+nCRXuQ'+\
'kgljxa1X7t8ZVJV6ZC9UXkoFuwNbSTPrmTh2\ntq6t1J/9bbT+EtFPkatvESN'+\
'wn4HdEOw/GGNznEUX+0JDUdCtrafd9+mKWdchNF787Sur1sm8K+tL\nVJyQE8'+\
'LaGd7bp6mWpXVJrWguRf/8efTFY+/cgUx3d/oLgy4xlvhbjOomyyVc4ihC1s'+\
'o5+AMV2u3e\nxnWorPDNeSTbPBMiKroxptTLFDkCMbWve6Ua0AS0IuhKr8lug'+\
'+0CnJNZii+ofixbyJrHhn4T8OYn\nHq1mRLWy4OiT73jmCMI0VNeJ6f81WlBs'+\
'tko/IdOqiV5VWU/2v2u+mY1p3zUtyvtAZIRB6AknyVPj\nzt+NlKOyJcEezSd'+\
'v6iT8hrvTqDZs8SiDe970KcIzeeUJ+hdHuGU78tS3QaqBEMK9V1Mq60vomxs'+\
'C\nr0PiDoxf4EP9jTPBOO9XmP18TEjt4G5Jt4A1F/6bzE8DiL/nOrtjS00u1C'+\
'RYPlm1WY2KHKPKjVEl\nnijVoApp7nbe35tSthIHjYw4M28lKluW14Q9z/nRZ'+\
'hfd7qlIIEQ8nx/aIwdWbvD9yK8vRjoDzF0L\nAxS2cOpfg321+rsif9DFf39s'+\
'j9pvu/eQqOGPrG9JwGZ3X6JTRqsw5On/xWB5B0LhOFD89nLcHYez\nz15nlRm'+\
'yR0addQ7ZMxHlDmVvZ2QVZZRZEmUTsneEUtkr35IjWiTF7/fX+/zx/nrv/fF'+\
'OyZJnVCbN\n3rtLkwst0liTfxfRp3suNhHJ5haueg0/0SxxbgknCFhvSjxC61'+\
'vK8mv9RVxW6zqQm7mTJxJvq1bC\n8+zx2mG/LqUBWedGDpDrNtCrF+16oXaEZ'+\
'J/9HXcqqBuACCdcoat2QF7yZWSK/CkCFrMFpilKBt9E\neP/GoVTc40SS5Gwi'+\
'6n1bNgoMb0JSeRgL0dRU+Twxgdf6cdkSDsNvLoy6m/EE5QQ5cGCVaeod/97r'+\
'\n5+0aI6R018frXqcFv+HatVfUJAiveSmP/73Vdb5sgyuIqDDd33EG0gI/6Mw'+\
'+w3xToZjg4a4o7N4q\nVgLA7HKlpMRl4vHF+iNlInCGRVP4GleMrRYuUwxHC/'+\
'bXRDxPk1UaMkXYDsKErJgJGpDOoX7YkenF\ndTYi2anJYHATsuFsgbs9GnOHL'+\
'SJPqffruwhrq1vcG239BYJgX+bDdAdhUPp1Sn9VIl5cIea+AyZS\nnmJ99Mvq'+\
'ef0TjQlW5bgGYD9BN0zu5WnrMENp0czy1ysiidB3DKJh1wTQg3KjURyaKzLL'+\
'K7x9QZAc\nfXzk3pl7kyJW9teUY41uhufMPoKYTRI98maJOtTSafk+Sm+mU1H'+\
'n5d+rF/p+Y/tOuBI+6WT1nHYS\nJUfYcKdrOgwccN92XPpHDgcv2wMfmxAQ+l'+\
'EaT/y7GwS8wR/r3ixR/irhcO0fLvQ3maWIZcqJdkXl\nKwnGRrSmDYqCqu4O1'+\
'ifHGuw5hiFc6631DDxQbbbuvqKyymZOmo6NwOO1vdAhEQdNnF8cFT0iwU6Q\n'+\
'S0TovWdu6LGxEIRQG25cQ/0JHxmEa8lQLPJuwdn5bJkPFggCix91g4T9Ylpg'+\
'ux/qqRzDZda7I2sX\nEriam9ceV4XoxWcqAwselxp+yYwaFC++It4dYfRQKFM'+\
'LmBn2MpGrrmKeqc+7+6GvnqXvOnPD1ILL\nvN62F/YXruxBbUSMh0mQ7c3fj3'+\
'uLp5uqhi9THM/CO/DKpvonuwdBF4Cr1+YYMwlMKdNavObmx56R\n0OJ1aH1gD'+\
'+go8pCfgrqleONBhrNhVpsNjSTHWchGC6DqDsqeXu/VLoJunGWuc7iwq3UUH'+\
'0zSX9kw\nVxESUDRcAaqMwCuZOiFgKalv4WwlDd8WqN31dqNESmRweThuXpmS'+\
'UivOJ+fMEoxokh2DaWJNovGj\navpDO8tgbDHLAf15CYsN1I8gFD8XQWokoIA'+\
'C1ktNzNrVyJO/d2NeymESlRFZryHimMQXnLAtvSwE\nOBSrvOk0CsSkZHc61S'+\
'U2R5vSvCAxZHUxxyfmz5+Ot0tvJT5hNUjwr/RcjTUsiMG/4x0bSPXCfjxE\nA'+\
'LYIuo82/mO29IQJAT/S69qvmjFb2/1hz9M303nirTtmdvGQeAieea2pyow8f'+\
'R/6C3YcfXAiFO2K\nPyHG6NdJ3HJNF2kdIrYg4K6JAvj1XvmiOLRrjyGYKcRA'+\
'vco0XiM3JXt4ctiwhz7NeN4QGyVP4eFs\n/7yZrBsnfe/JfT7OPdxnIgnMuTx'+\
'/tludKugYMOf+XPZQJJLlLlJyJfClJvM/ITikXJjTnKWUUmNE\nvirdhrlUzS'+\
'pN5AInfLVOEH9C7lAk70uc5wLdKn6xss7TCSn9HbjBkmuJ5+GZKABQolSfWN'+\
'/Nq4s7\nuet3LLaCotJY/W8IFju4unzhEgRG09iT/MMIAEFKMOcFo+s0ahNtb'+\
'170wQUa/FxJK1fAjizF3t7S\nQr9LUWAvp8Xe7xdto3JqFWPS0Z1HfN1dABvp'+\
'zu/F+wOnunNfPDAObZC0G2QmSp9NgArnFQ+JI0se\neH2xns5+TUOj30vgOT0'+\
'SDusgVGJ7TrIpXy6SZzA1XM+r73JgvfAgl5rspd4WWe4z+vUS4Pu5QZXa\nI8'+\
'V04D+eH8cyLjRrD+N6H2XgI5EsgXVf91YORexo91DfvhpoTmIXSGbOdg8EVC'+\
'Z/O7fqwI1mTb6O\nUPDrP+qe3RF1kj5rCbvodPOXgmA82CQHwBpcX18AVUyc8'+\
'JfJ6fZOgeJlYSOE8xyBRjHtTSz8W/NN\nVhr1XvAYxdKS9bg6w05EDId7QY1C'+\
'1wvldp8ziyUOrcRIUdb48GydxuayB9qr8PYrgAzZ7MVa0Mx9\nGeYfuRph5zC'+\
'/cu7tnuorgR43ibe8M65cgyWI4y/rICy5fqPnM6/PXTRm8c9A3e66kyrikxe'+\
'4j9dj\nz+eTco8sbGAY/Zzx8blaatoLv8tg7c3MPMXeAUHSSyImd38AAMn30r'+\
'LBjI0vLOD+DmFAXNY+h9MZ\n6g/Gr2lJwPM7luQ5MDRsBCtsgMLImr5VtuQVk'+\
'TlzzvKtMljfzNrRY9jpjnIomCVuS8gwHQmkYLN1\naKcI1pjUmbc+WCYTFm3O'+\
'Qu7cFBbaMw56Ph94zfyxMWZWekoJMo58PvOlcUgDk/vMEJXve7M1D/7j\nDvP'+\
'ux5v/5/zFgrfF/xffVyUDDzr9DHoLHjalu2BtaNkxMbOZjRntrUnpFznG6Pv'+\
'y9qQZ5vaq0iN2\nE/UzvXS+kdYvxc4kQzWYjbrQvmRbLC99MJl9wSABDeLRFv'+\
'm6V3UZ+eSd+P3DI3mWqN36QzQjCTOd\n0eBk+Ex7Ec+z9y2Z2siVjFIUkuENb'+\
'7omU31VlsdB9QOmDiGR5JKf4+0VGRki429/dZJoM98yEuDp\n+TXxXDuPkYgC'+\
'QktUdHHiCYtio1hjBsnTRRYjB8tv6BP8Bwj+iQAyrWeF3dpWE4dQWR7NZ8vT'+\
'0qLW\nXOw6T6KPYOuXY44bZY35H4C/fhi0RwYmZbM+aajyMF3riiI+qMtPkzP'+\
'44s4KHFW5Pf025nAB9Fke\n+gx4nSqWmjS9HJM4r2DZoDvzh34cxvgL9zvQw9'+\
'IEb9HmzOM+qpwmv9QUuDFwIS2jE4iE16sQ7fRN\nIpSbqY1BAZiEnfeoCXbZd'+\
'P4r5YoVk2+Z89tX2TcILct3QqoD9GAJB+mGag9JWtTGPoe5NIMCWwya\nv6ww'+\
'YaMVq4nu/EYzfKtLhGzD381tswJjYKePNo6uX8UuXsHOjy3P1+x+bYOk2/20'+\
'To9ajJoALQlk\nnDrUSi0GTtBFl+d6aJhTuJtwopJoJZW5t+y8H89X766nuXT'+\
'+AzmUZSrx5EEEJEbqc2tb6xDMCsis\nWaGD8+12q9QAotDFiCely04QdYWgya'+\
'L5fJIczUiBhmSfCQuCZ1rMf61dX11bnh8YjuB7F3tRmLdI\n9LaztYb96SXqm'+\
'ZWjpEsHqxdXvjALVvqYeSbLBtjlaUWIQzRKcn7eU80b4B/z9+N/hW6MUUCKV'+\
'Bvz\nH7dc98sbujretDBvb9sW4Q54cJDPDaI+PrHaP3gKpfdBMCgYzR2yAXFq'+\
'fq+A1wgRN5Dj8xJxhZm1\nkp28EDQlmmfhU/9EpQD+ILRii1yru6DQ2SMPYx4'+\
'C27OxjnHuWaPUjICHAeB5PmOCpg3DWTltZX+N\nQV+KX8Okn//wxGMMUk9KZt'+\
'5/Jvv9N3qEwH0aNuGvWYNAB43yJUSpt5UnYcs5xW+TU+UIa299dSBp\nxj/Fo'+\
'n/DiAq9el7rkjozxpoPXW+HyamugaZvWSeCaf6jW8aKc0B0E8EaspYMpIZuh'+\
'U1aQZIvq5Qt\nFGWUvab8jvPe3Pu8D9v5M+Urz7oTflqYUb9rqSOCzqJlnUJo'+\
'LBC3xMkqWHjAaQLliwNgOJr1JvGx\nDZvTp26DpULmu/uczh/Qz+qBFkYGMNP'+\
'yAdj0Gh2eflOfR/Zfb/JaUu0FCv7hB+QI13VqE6b4hbLA\nBd/s/+rP2rxxVc'+\
'/Wy7cxuAQx4wHL9lAhTTyPtB04OFALYIAnLxnVGkjQkPKDePMNxo7pEHyr52'+\
'r4\naOsMy52fjHFVxrHKQlIy3x+XqH08rkmbW+ovQwMEQSiOgCaI6j6/hX5EW'+\
'X1KGf3ehDiuEX1FrcEh\n85Hd1nEeWgGxjN/RIZPL4lA5mpDMH5wCjSPdKHge'+\
'TT6yYr0EDFgG6+wdDmNnbIkgLYXJG40lCkge\ncXDcRRybVO5fHg2eI/TDmQf'+\
'tuGZujRIhpx7jRKmV8H3E3Z+HnV88WMUmXWm0ENo1qBC7QASQ5mdD\nZHyfdg'+\
'o17X3wzipGjZBM6rSqR99yCOO8ryEonXuVS5G5q3nnYctD1dha5gg3S8YEsx'+\
'M99wBylpmF\nQOzFok0Pc9Es+QWjsejR3Ib6MVgyehKePW1ebKidU999J0ewu'+\
'3V/oR6FSvhQcgxZcEv4TUxYF5I4\n+oROqXJYQAoJY0+6c1NvDXjqJniv9a7x'+\
'd6Nvtk6GqrAtLfFLGPGXgvtY9xaSlYbn1oFOtGgQji10\nENXNUnxw3ptmLi6'+\
'olT5ktfRIaXq+t9LqR+JtxasC+ZE0mXh2MUe+cge1R0CGYLZP9u/DGxf2d16'+\
'O\n5h8zH2b7EG4mY8ovFMQ6YRPl5pcgJpnGc7fXEA23e5NvD9z8uu8hhmLzw+'+\
'8kzvF85U/4QTGTiU/P\nNqwiAoTszoZYCZXplsn/+80/ny4a3NVlCDNK+KPhd'+\
'/2/b6n5lQ+6/9sWIJqXAsEOe48IDHAwY8gv\nCLZTSinvXrUPkqgdC82pCQqg'+\
'e0dJ7nxmYG5Z6vnRQhyoQ7VUMfyPv9oRuGi/kIiXfjdao95tmhpJ\nJm71byw'+\
'qqJKVFn/dHYjCZvIvb+T8EY4WS50//3bNlP3+7Zws6oiEAlnU6GYOun7uRZz'+\
'R15ciWbEX\niOfHlRInLpWzUe2aABDFV4tnea+AEQdAXQtH7kRR4sv3tnYsze'+\
'W3wEIteEzHec90N4TDjWfJhliu\nF2Sxy1VdrCK6wiy3r+X3I1XPFSj2858Ht'+\
'aetcLkY/vC6DEHStGsU111QNMKrZ7yUgesmjW1nuPm2\nYi9wnaOv33811BC2'+\
'eBMr2c+cfmgS6Ad2FWINoL9oXHYI+XS+DbfOBZ9X5ik8WQuxnB/Rg/csSQ1S'+\
'\nBR2qBbKKk0exNGyFuZ0jf4LYCfpV1DKs3lRYd+6JD19Q93LbIiTGm4dmb0+'+\
'CxJhGiISafBGp1a87\nAAlZxuFEllRZ2K0Voo5l8R6hUZ98LD81o31YW1vUeu'+\
'YDNxeToZ9GX7Y5RU9Wpt+5i95OYt73EuxV\nnUJJ0Iv0V6OWXibDrvPCWvRdc'+\
'YpQeEkXeUvEJsiYhXa2VZdYmEqyC2eWuNzpu27qVXHnwgipZpka\nmYoqgNMX'+\
'SWl1Iud0ErvS9e7ZihdjaZh0uwZo2/3EVrxUWknsbciIXiHOe3o5w4rkQpN6'+\
'3Ffd5Dfq\nxLvtpheacg+pyVzsxr0+EI2wyDeOsLohhNmBxJg8VjOTgSBeTVo'+\
'VO2w+/7e4F9QY0BDPgSrCto0G\n1XfAN47u3DPmZ97hufmgTZ3g12lYYn6oh9'+\
'1g1pmNe4jykbltcV6cEI8N0ea7G/rT+UUbp3e41gkt\nW1ZLp4qRIjQUBcz9I'+\
'bWPkFn/aHwG3pEDdoYkqNBsXblG3k8PmO0YnVNCQAtaq6uA8pIgOxgly0M7\n'+\
'US+m4IC6S29n5eHYaYeg5Y+tFKCy7QjMVA1Q/ia6p2CdElTjGPRK1gBNIQN5'+\
'ACQtzHMDbKUrTjLu\nKywdXWCTrluTYOfUhYb7n5ZeBa4hMRZEOrcx4IgDHgt'+\
'/PZ4A4G44xyETI6crP39ocyPYvbb3ZYAx\nmhzc7+jGZwi2LUZBNYSr7/opBb'+\
'DZ2yy+B6ab3z060nq/tigLKBTQ6KOv9HMhWtOELWdN4QCMIUtf\nWxrf9L/0U'+\
'Dx91f5AillveCY+x/eJEKo0yl6WJZ2LMVrXwjrE/CcOmaDLsXMVzopiIXQ8S'+\
'X840Bw6\nDHdVHXpFgINc7FQFf8OAcbGUsabLlRDHAWRhsZbGNAlwXib8N/M9'+\
'KxElyHmPj2MtlEn6K1MPIHFK\nAxRQxtVQ4n5fJm8gVGtu5WagsG297tZ59ep'+\
'SJNGVGNw9p2uIgwCs+txttYlkzGwyEnlAHKQ4m6Zg\nVVYyS1l5r6Mw/+y54g'+\
'VEhuFzymysKqx62E3sR8JenPypSfYJa5j9qVhLcfCHN8qWh8VfwPuH1SfK\ny'+\
'02fSsZN4Q84wAKSim2Wb5U0jdp1isrR+nEJhG60GPO2LZeAH99jbsV7O4ajo'+\
'gS1oanVVd0nzF5Y\nHfNFI7OxejXIvt8RotPut5zZclOmW6KEoolQRo+4e17D'+\
'WQlQwihqBvDr9V7FxNP73FGvLlciSbwO\nHecuq+dmuhzFnJebvzrhe2LiKI/'+\
'Z6WykyHDod/1kjrIsx0Wy93zRWvaDl4pHxrzro0FhY1IS1UaQ\nx6NZx+d1X/'+\
'TIiUWjjKY0Lk6LbtexXpS4v3PMVnt+Ebm+peWVe+Hnn2JIleh8ZnZRMdL5x9'+\
'hYTiQ3\nh63ARzw7v+mpe8gj9r/cg/OB7le9Q44c9uN5S10cFEmpDaCUDcvYr'+\
'ywaXin90EA9V1iAnOllpRv6\nU0C1tet0a58rYt5973OhAQIBtMYLVhEhF2AP'+\
'78rx5edqPKS2ZqTq6HwBYeVX973kEqsJ07SAm9We\nHWsbzZXcvt7W+yJm/0r'+\
'kaY43etVKC57kn58Vqo92K0aHxVAe7kwWFiyBy6VKvYjw3iK5I5ayJbAk\nTy'+\
'LV9CxPwBsufl5x/m82W/F5r1XR3Ga5D24oAYfJrq+O5uJxBmlqSjAzURYe3q'+\
'D/IFxV2bNSsckc\n/hv3r3LIc5b89LLhfLqnF0K0oXj9VzxNPLD9ZW9rDBUZh'+\
'ClP87zRruDYcE2HidmZ3d16d1m038AM\nyjtcWAcUQe1kQsnXVRfnYZti+3FV'+\
'konhGI0qAa1Esv7pvsEGx2G/Px12YAy8+/liaR8XO4CFD+dR\nOUdEA688bHV'+\
'I+ONUup7B/cXtucHWqj3c6YMjYyogicj/S8GtVi+1nxt56SPXUUzId0ds0mK'+\
'EPjbd\nGs94ixzAJF3FOXMqlKp5IuZzJXfYfsLT7XeL9nP5T5FsFjs+4e1lid'+\
'kPkfXe8idvUnCum2RktsZD\nApLt6ZK97lz/t/x4Lvzc3TOHZxZDygq2M0EgR'+\
'CKB5lS2aP0bfUnL66xQn+6tZinS08DRQDhfEfDW\n8Q7C5HBbJezcOabkhqnh'+\
'lYowqMswsSfe+iNj+Bt4zYrWG11M8cJIfRMJOTkugIEAgsbNPoO9iDUk\nGWE'+\
'HaMCZXpB7b9jre6g/R/5CvpaN+E3kyRsUv4fvzW9AA86lzZ7Yd/Mf49H6jD+'+\
'icePZnshbX2PX\nPhDltUw1yteyTRkLgT9hMymhfX+4IDpafXpdpu1xHzOv2n'+\
'XpQcp1tauwWrE6ZX8zo+cYen8Ne0g/\nqtIsu8LffjQHwYqLSyTapSV3Wodey'+\
'bZLHL6V9I8cz1lzFyq36KlArcuwgWEBQex//di9UX6e0qCL\nZNRHWZKYxcUo'+\
'8mWBc31u6QywV7KAsdtxw52UUa0lgXDsw3qq7D2TLAfD+2V2LTzPACYM/5Km'+\
'fKfZ\ncObMeaeQf5PrRdMZVzcE7pmv31/BXTmbmeCMcz0pbXDuh1P5HfuD2JV'+\
'qP+vmw9kVn2a/O3KwQJQD\n3cI4CFp27YDVALyABew8vc4jDcbmmKDCwcYfIK'+\
'mFCNPiFoGxQAGA0fiOAcQEUTUoIU1uURyA83yV\n+eLZbzs5efX/dtZCubAy+'+\
'U2dsI6fnKxOGm4y0lQRc8Btf8ixpK26yLB809O1S/greEyKRQ9xqgP+\nyCIb'+\
'Ugp+LAv+vjl25dHmY3q0G1iVmCKaDfYg973+lffhR/p2aaOjclWQngo6VWWz'+\
'djblgGTK2J2V\npmwp2uhPkQp5qC+ySatHwqdSqYpcJJi1m+J5KzU/ecfFhZO'+\
'9qh+uUKixFIyLYSgG3hJkPrbwqasJ\nm4qGZ+r+fDibYpmqZcucHnm/rVc6U/'+\
'hobfgWokYiwQLI+sr94dnQVLp2jZRWCgB/NhjG2TCqsKNL\nY8eBdelfzbsSa'+\
'wAuElUdelQZj+/5NbZqpRd0YQ3U6FrntT3+TvCNxWiYDTA1v11fT1rV1MKk5'+\
'jnn\nL1PhgQLTGUa3g1hEEZFERzcioSgAZQph2Kyg0KQ/zS2n/t9N4EdDMJ/5'+\
'y61ks7xpVw8k42clO/Sl\nkJ97LdZrlOuRVGReuf5umIaj8OKSJWe8p7e3rHK'+\
'IYESTieK0qKPltWcOtXIXvUzifN2N3/vkXBXL\nEB0fHp3lKmYFvCo38HjzHm'+\
'wI7qNBeo1Gbzw+G60SG8F322j6Nnq85KfddNwfdz6uUPHtpDJ0JcO5\nuSvP8'+\
'28Z+N+ohg36erWxEZwV8BX2msFH0KpYrI+gvb/maejbY9mccBNxqhzcHQco1'+\
'voWNUoCRvVu\n9QkDtbmbRaNam+ivnwo11ou2y3StQNYuJnDDMi1nrR5Eymq6'+\
'PYNozKbbzZ3r5PUeLv07rf3uazdK\nWcHFH5SJlwcuC5ZrL1kXNgVw3FP3eqE'+\
'qZSvnoYfA7BAYLm9w09W57C5z0a16l84lLVtOWF1aqi4z\nIjGAyM1Z9kmfGj'+\
'6GhmdULN87p/wJpVNSqrmt3Ozx6JL//5PfTHwdch1qUp+Jf81//DpG/S0mSw'+\
'oI\nT8SfX2hN+5w0B2gHQF+3F1LjBX2nVy5CJJcMd3lM5WQ/aNJ7HyEWiBLRE'+\
'cl1hsqHE5p2gyjI8Syu\nnCX6MG7s1Argo0hYsKyvueEFXHzD1cCqeV83kZQZ'+\
'3F97qYbsrzl3n+qfU8fRPBjlOaLws45nMNMQ\n93X8cEF4GtGyKhcragY592S'+\
'9Rc95aDdJEHQ6M/0soEiWggUBqxnCx7A/y0/9PwDnNKYxD59khp+K\nRq0NxK'+\
'T7L5isYfs2uJDTLCpuf89Hjupm8muOO7ef0c1mP1+NbEA/NXIy4SwKqJ4WsA'+\
'9T5bfbGrs0\nMaUMhDKZ2T8i081gh8CHlOkGjP7aZ5CL6Fa2f7ji6kG4gsm0N'+\
'CIXoMeWIXmRLLYHuekVqTOi/wT7\npgFgliulDszmfIjVjPb0c9KmGa+Lp8tY'+\
'l+hX3yvhmz0EACWl0Ahl++TTi96uWJeWKPqz7IPNLlQ3\nW6rE0xil6YFA3Pu'+\
'//m0tHj3S4z99LEetGZZLPu76iYuyzR6k7imVhL1Jda3fyuyYWdZ3t8vwmWT'+\
'g\n7DRiLu1G31Yte/2QgYKHu4YnHmIhI9JgNIjdSGJezlN5ujfehNDxr8uuwW'+\
'XkxbI56ykdHN4gFsi5\nPEIow0EvlCd3n9mCn58xvlJv6275A/Q8OCZFCD0ay'+\
'5oBvlP8Bm36NnwyfMHyLBEcLrWxo2r6lm4P\nBWN41IJG3RJY9eHGYNuDbMKZ'+\
'33bPlJENpiUiA5c4ZMNJ7FqEw2GM784YrBuCXGEuutW9Y+6REDw1\nThxxr8+'+\
'Etf4x0WS+ZLvA/JbwWvrRSOGzL2jEJhy7JMrYZ3GrcHkUwY0NnJEth2uzfcp'+\
'pYG3gei37\nXB2F+r/N46428QEckt/j7UqqEzS5ZDbS6Y6JqEcSLDpZRDpByL'+\
'vOXUP+k1E79jpPyDL+tua4neqT\n2vShYqXLICmaP5T5LvWucfVe1afkpDMyv'+\
'AjDErmVML3PQul66CcmY7I5i7Pip/HIYXdFL+aHZRit\nRhw7rg2h6Yg/CgFo'+\
'6UYO8wjltbRVm8Z8Ol3VmMWcqYEDrd+CN9wN+Jk7lz8UIZ4F36jbbo5ZYsuN'+\
'\nj+5Zby1uqxfRBKPAdhFaeHFGNSAquLRKONOamOuGszS2FxMqn61MZXO0Daa'+\
'Y3pBwbnOPKhdB09Aj\nmHBTfwGR9/7OkiNzHMmUhubHl9gFLFJ3G9QRswCJuN'+\
'2aD4yPGD7RV2Lcpbb7TELZbWYWPkMvdPX/\nK3aFl/8wVJ1OFpwZY29euz2qa'+\
'5JYIeQoYYxlmP+0se8iAExeSEkPX97BaeSB9Z8Ncl9I3Wud20ov\n7Cxd/fwM'+\
'kQNrA+uJmWrK2LOiLydENZLr0u+9WVo05e/Hr5JUp2nOd+ZAg4gUH6i/cIFi'+\
'RThmH2A2\no0rhRnNw5BpluZ4jsIXKsXEcfdfHn60VTRtraJ+B36y8JBnMzN2'+\
'eKE3ubmTPUixmJsC13Ah3seca\nL1r+J712aQZMoCn5g1nlj0TiSc/nwEVa91'+\
'gTd5OFzL9py66pitGHWRMVTTkLziJwMqCcVIHgKPzx\nJU0txNIbg8InAj5KL'+\
'G5S5uSDwyZAOeJwBDQQmvB5sdK9sderHitGuRZWYNfnaOYQquq6k5T7hKem\n'+\
'w/zm8HVw74yDPpT+o7XljSnQKhhttPM6Tznj6z6DDdYxy+xTkU/oaXC6EvwK'+\
'SwzV18iAKQFzAOdD\nhexN3BHB4fYSqfkcuc4HTSOU9yh0rIptlOB97kXKC8/'+\
'9URwuzONyc7OQl67Le9hfcAsEjQsffdqc\nH/cqiP329c3cuFdpFDBSsHA7JE'+\
'D3NLioIM3dmhUJjrm58LcuUAzCMpDwB9QOEEa2t32z3P9sk7CO\npR2e6Np4g'+\
'OhO+3gcbPc3ZbDG2NemCa23YRAM8Wrxfc/KIxsr8N0gjkAqt7c2pKmlYbFPj'+\
'Wwga5a9\n7iZPfjjQhciFzsdAH0cfpPbZNQjLuycSoo8QZEqpj2+MkyYZYHSH'+\
'pH/O8LpIvG4hCIK5oRNlIGFT\n4v/a9rY4WG2apu6ikPRm6h5HL3tvunXf7zI'+\
'wmSm++jfOe/J5ZZlPakFEWGu8eHnfvvyMJFAL60Zf\nfY9EbyMVpSaeU+6CHu'+\
'D9pdzOkBscM8xwtbcPazIfCL8x4ggA6SpapAfBb+m+sLAZmwbFul0NTbA5\n2'+\
'PJlzaWfO0oxt+km4nMonW27yKa88ucreWClGynx+K8iwhOg8O7n8hYyhH7iA'+\
'aC3EiVs2z8Ddrma\nhcMEBmOoxshxBL+YnmKc25WWJJTR3+9Xzo35QIrl3BUD'+\
'4HE7Rod6v/xcQzrl3YON/R+5n4VIDCPu\nBMB1uALurH976e7p6R3cxvGtg2b'+\
'ksxBvSA8xj3cgfzS91ytu+9mtogaoJLPlPLss84kDzVIDQ4nu\nlrz7/92LfM'+\
'dKkOSL+5T1EtIn9gyVFeSzeaT1ItGlV48U98RTO+7423ViSr16St5TxutjCS'+\
'lcU7Ax\nWhwDvQhYXWmCQZ3ZXU5DETbIX4jgi5lKf8a+eSxWDmEYNzx9wU89P'+\
'1XegX57d64TTC4HWOzK5+Ts\nkjU5XrE/gNhVO0nWJ81SgAmbiL8cM1D+dIL3'+\
'hsKm/r06Npaomja7yzuEQbXrkOPBRS4IsaULP/eJ\nd5pUAuigNM/4mRqCld8'+\
'QaGWqJd37KTVP3BQTFrpqWud+m45s0OSvDi+dbSWZUN0+1ag5OdLAPcRd\nqO'+\
'6ZLoyAIfgIL9Tmk6gmFT/LlonvkcyuBtL7Nn49aJMz1pWPyrxPtiZAFk29fC'+\
'q7Hwv+pKqgVF/Q\n7IV+8sazlk+DWZ5dg3V7VnTID4GSTSrJOpZAjmou1r50o'+\
'1QOj4LKPgYb3Ko8qB+MZDX+XleGvfmx\ncl5yEPrE2yEfP0qY4L/V6zvKGRl0'+\
'XcW9f/TOU1Zg7QR1jRCc5LLwYqvYM3HGHmGD2lCuyFsqDRyr\nbwmQLqXWQol'+\
'M9sShiz8fCZ/xumd5uw9ObUvktdJmG6LfY9nhjvfkDsWjWTRgNAKKtehdGP2'+\
'X8p0W\n5dtgpVaI4h9lxu58YqwhUkkmmNCV6pLvwGUu7lng0vF2zctTkVxShe'+\
't8Bu+zSerY69Rztco6L6Ln\nXIj1wG5lU9bvc2/yQJq+9bVVjpNL3p1r7yT+F'+\
'vlcJF5gg5p3myjXltUi8eohpi3/jV5Lr78Vh6xq\nU6wy7p1zaff/Bv8zR9Dl'+\
'kYLFsGuPel7ty2q6fXy/YvI45snZVu1xXGRDpz+a2ZZtnQj87Y9iNmqr\n/PW'+\
'0jSKhYqK15T7KmTRrWTWay6mTPgnKdGmz3vrFr5N/Tn+s9mgcvXK1ck4KZg8'+\
'Y2Uism3U53xv3\no7Kh80+S89OXWsBwsD1zT6EdewhcIe7rIZhdj1cffppzyZ'+\
'oBuFzRtgC+6AeY4e78sWFcwO1cu1Vv\nn5940TymlsJ4dfhWvBakbwZQ80jvs'+\
'6ydqElCCe79WlRUIEIiY2ibfSykwfIbxpMJUlSv4ZWuGG1X\nP4f7yhFTKKER'+\
'KNTbTx/QzxfhKKjCNaPiMcCdkTbUSmWcPX/ezYlkTLZrKqbmBjrVNp84K5Ck'+\
'nZrj\n32HuvuktTiU+LD09d+c0LVh/5r0F4Y8R97dK8BpCo6xNTst4pVsuuya'+\
'ara5g7AxIB5HF2y+l1G6l\n1YarBgiP/5bYzb5cdk3tZ7sRiHAGNI+1qBHner'+\
'ARxunUIGJ4zvXbBCB2wG2euakZZRZDADx78590\n7NEPWs3H+hq+caf1n5y3s'+\
'bU0roQb9n1NsamvE+70Li/WG99dTZClXYDE1MZdbhWslen6nYKe76BK\n/5AT'+\
'eOAhUGT4XMxfTiZhNmfI/zMAxsJi1OmjSGG+udqOYkVIhD1DwGgTa1WURx5o'+\
'mHMyXW8Vx5aQ\nysPR/FHwmc9z1a/ywLQoKdWxiV5iw241OZTav23zyB5bhRv'+\
'0ULbPoLz/+MGP7z+BA6Lf6nEtRjuz\nmO8fHfkfcsAxaBBdLQC0obTNi2/COf'+\
't8bDdmCz1nWnpU1JobkMAmyaJNBVzmV8AEKqsVZeOpXWqg\nTpG6sZhhLCKLZ'+\
'tnmNs+ei45yArjgMcYTpkIVG9zkaAiIZhAikumCphrK+FXdaxHGVsbn3BoJa'+\
'f7a\n0Sc8IqsnTDMOfOkRd/GX3Mi4RI1DBLP5P29nKA3Sve//25JZJMqFeRHf'+\
'Tut7t6UBY4PfiD+wubNb\nUttA4DQNrlLTrgiPwRPR2m0wgFYcR3373qfx+kQ'+\
'GdLu3DaaCeKLS3xaZ6VxrU/soOAqEdXkskTOe\nmuolGqvVv4flx0yEOxT7n2'+\
'as9jakitd4ySa3/dRxM/UiatMUM+OdHuweY4CoUPG4Pyu1AvC/nOTi\n/xziW'+\
'ONF7CpNJes1SLq7kMFjQ+sYW4st4FVThDYwzWu23MK1ryZBm/k1O2ZAitP2C'+\
'jeg/FhBQ43h\n4XwCc5EUA/ga1psUyVBXFtirPsJIKwm/54V9z0pJXqpGFFZX'+\
'fUL/hV8e9eJ4bl4ty0+pKZZLMPg9\nZoy6dy2U2fdawlfntwhVNDHh5c46cyF'+\
'hUEsnwf9igAkiHBnKVU1jg+fx1CbtrCracDb0wzXj1Rhv\nQ5eCNXb0gjdn4/'+\
'5MMKd8R5c0NiMDku3nc+V2Ip9KMt/Xzjg8FN4UkvhPLd4SwbYpyZ+3vCNO/4'+\
'+5\ntnp2SMotMz/bhdPlbHYei4aLw+VI7hu63Zf9IyOp2avs3TlxpYeQAR4/N'+\
'yeuCPw5Ue3VYjQl7ZLm\nYBmR+/vdQb+yMhCHcahN+D8SicW610aDT1m+U3eP'+\
'js5j7taWeUH++Q9fGk0q1hrWKgPkfs7hLxvW\n+ulrJaRob/GXhlSmvrwm9VL'+\
'nsT44jhjjMp87BD5HkwsQohqlBeBI5wrY9LFBSa60DntmPfJWduzi\nOONHDH'+\
'WHuBqYQc+lkmYSHqcW0/6tGcyyaS/pDBicFcWVVTy+qZEr5aSyttlzYchM7/'+\
'edK0FZes2f\nF+zq/xJqGSvf5Bwgjx5nhswx8MX7Pmr1OoY7nNPV3wUi+mCp8'+\
'/rOtT28d+JY99MVGd+O1jGje5uj\nhEm9KUAHYrIpsvCo4Q+y+CgvPtoTwIOI'+\
'tesiXv4wvJeOsKfa6ir+cKjp9Ozcto7lO+uTb/9eC9RX\n0XDvr+fBNCmUj7O'+\
'LYn5GKe637F+lm5tlHWIerzmfzmosCk3z7Q//BdFLOp/mmx6SbuQyR+1YUNP'+\
'v\nz7lJ+LZDPBQUgiwNLJAQmgmcpg+nadNeQOTAOkfgj0K39mO57C/eeVZXLg'+\
'05WeHh9RiNpTliwWmo\n3k9S9+rtzAv3BB5fNeBHV3uJFvC/O+FXQy31o/3M2'+\
'XhEOuL2jQ5ERxLscIVXs19Eo5tkwnlamJ90\ngnsRTwSU8jIF3NIJgKfqjLjJ'+\
'0lRZc00eDcTN9kQAgJyjpPZYDOAP9EcsuN3QQhc+FcCAx0113MTx\npYPjwbF'+\
'jppKcSY6lTipPdifowSPRiQnWz656X7JPF+qYQfBSXsedYmxijG0bq1EhOXj'+\
'XezCnyTKE\nv6LpzV6z5bmjScHBn/vIUvB0OZnew1CZ7oTMrvZ1wCtcX5lmQw'+\
'bAEU3ibe0sEwhuDjD0TYA03+lv\nRS/XRgPRU+52UcMclu7x/jemMUNBhtEa4'+\
'1H47ryDdEh8UcVGvj4jgSPyh44xoeIFg13p9vgnkfOG\nPe3szLFTZr+H57tn'+\
'Ecwuod9Cc8EI6VUv71ZP9xmUDT1AW4aAbTadxGUZ2LeLyLQSP6cJYZUlcr3o'+\
'\nt4wUP99hJSVwoM6hr0g2dUIrSiUfKwfTuLas/3NUcB3w9fbBK0N6pojWegM'+\
'YjCorCbj6cS09yuou\nF+AL//i6Z4KH5h2N2+Qtu2/aN2IQv9ZkscGeaqVjlZ'+\
'cN41QCuCs2jjWCuexVdNFoclrbz/j0R3Ia\nnq8kwxvBfHfhUJSI6aG04lttG'+\
'Ad8kydiKEcE5ckmOpnjS0RoQVjr+W8aF4IxolgsyO6xxhvZl0D0\nB/z6+XE5'+\
'VZQ2ts1eDuwmV2pOkaK9t5zep8vxap4HipCrgj+IUXcqCZrpr9gIASpuv5jb'+\
'ZAkaETJg\nC1mxOQ3FX9rRkoXi1qlCMlQurOv5KJoEnc/GvtvXJJ57opd7std'+\
'xRdhYHn91QjHthUcX2kM1e8K7\nJ8fOfhnNzPu4b6SGQgxmnt2O0laEq1LmfG'+\
'o1+46tvVH314A0rsb4qIavplVUzVQm57B/dl0bs71r\ncpqC13/E9GN5yu7aZ'+\
'9TforxvXvCGLuDvrptbOuCR48o+Hic1K8cnyks6S22ShAHSpuvTCfo4e7c2\n'+\
'qN1cNkjutRwuUlLteOLWBjoT3E68J2P+tewV4vJut9UwGARMMaJhIQh2H3OJ'+\
'8n33e9hNnPK0sfcW\n+T9BDsRLMit+8rJfyZqA7Zhb4D/QKHXWnUQBP3Dno5I'+\
'uSpmI9fs61d93+zLjOH0ny4fg5uSvkvxw\nfdd9VGNuHJNp5vzzjviOB65Wd2'+\
'oBkhGLW6VimnjeCedDhlT/KALjk3a2ek2S0kGjDmuQiRp7jQfl\nwMF7mDb1k'+\
'gaycmII4ovRPCxEL+JN6sLOZUU0d/PSmt03F8V/VhcDRcEeVi5OfizAJ+HSH'+\
'nJEArZJ\nuNecWn9Pk0IOvzF0c65R7Uq7eqzFXO75K9tONNRbeWHNOVIOkUEv'+\
'kk+fpwRxRLnt0NywmRYu0gGI\nlAZPGcMBgs8c1riD4mDD15SMkBYmQC7q3hv'+\
'ykDuedYd+ZtflmJERURPeeoAI9Zv0gbt9vfdlY5Ni\nCOyZqJq5BrzEZg/AqJ'+\
'6ekXB90qeGOBFrmRNWlBbjVh7sHtcb8ut7UEb5ZfoTqeZIU5vCGlafD5P1\nR'+\
'9Q1+GIlJuxOe72xAcsvK5BZb575q74t27KfMDGVO1D+oDeU83XrTOGB7gYet'+\
'7EXpPpO70L5k+FC\nNHrIXSBCKlAPzLOt8kVy2vgqa/kR5b6+ba8+NnzHL3VQ'+\
'NLQe+oZhKEof4yC6hO0t+VEJJvWU70Ag\n9/H41o3IRqSW12BLtrmKP0jGHYL'+\
'ViAAUOgcQtEi0CWqr5VutFWDcYz1mt039PVy2T/YLpWRRnrG4\nc2na6Le6vB'+\
'fKQ8658Q/rU3RnAcJ35cBT7tJrHkpqvtQ2Z4vNcMObH5UtC7Un3Hm/UxDYZN'+\
'1XhCdm\n9KZyIJxICZuApfjojQaYoLU8lSSjNdzKOYMhIicT30G86WKn+0SFC'+\
'rDbF/2Fm95P1dmBr7xuej2K\nNTOcXQCYV5e582mbwijfPNQ0C4FpRoAm/sul'+\
'nNNqYl6uGok+z7cEDfghKnGfEQiB8YC0/BkfTFJr\no52B1p0phHxW/AFVpuZ'+\
'MQn9Aip2QNroMR9uur0k8Yxal2Pdd+fLScJtmzTRWJeJCQpRXtMELESnD\nGO'+\
'HlmqMg8BLmudEc2AiryRF2ZvlkueUOlgAOh0gyTqJ5pJfMra5O6rmKgbrtDL'+\
'Z8L6DN6bvs0ADE\nltxr5gBslWg++q4S3We9gNW89D5oC5l2AJ8JnFVdPBdiy'+\
'Jssdh9wy3afdxsVCt2Ci19Btur9Qn1/\nAywadItqUL444Ds1Q4T9WlDMyGnx'+\
'x20PZr8yT8V5PPv5QEkzb5v0BmvugoKXGnfnvWSp+OD42jbI\nrukXPu71i7x'+\
'u13dtrD80ztLYn9F/vfpS3yZqEUOHwggMQlufjHGyjZ3rOwQ52em/GzTY5nm'+\
'TjiLD\nUxfOZybTgOIBatot4q3h8KXNscOHabRwjMZwJEvUXqoCMD7ekvFDaj'+\
'VQcc4yd4yah99B/DbjlP5h\nwPp82DNUStmMMfky54r7dXTNs6gPv1bznKlDN'+\
'VD2NEh9GwyXAP4RlXZ7LzeI+9wcBfOPZwTH/6Jk\n2iX35P0ZGuqWr24P1JNS'+\
'JTcqIkVU7I7mvCJNCkmfo9O4AK/rdgO8L3u9EpEqOHclMIaMRnjr/PEb\nigW'+\
'kExxv2+qkqnmBVm4bEM04fiHw8vpxr2ilbFXdUlL34s332ZO57GZ0hB2Cset'+\
'unbKrVv9sfcTB\nZhDgmi7DctO5mYQbSXlR2W0U/8H2aQ9EX5G0xoGcP6oESp'+\
'K5y84U8OgaQAX88dmY7VATAxOUB3fC\n0TZ7drhaUUDTPNZYCJPyCPBM9lJa2'+\
'wIZtgNexh4UJj5lAQ+yzP4uiJVcVCAL76dZbr1dY6/bBlmB\n3EyS9Iw+IsAf'+\
'4cnbmHoJHySYOQcWiC3z34M9YI5Twd2jGDMQu00vv9WSmTlC4WtqB/CAznvR'+\
'Mm3U\nLlxjpKSnNNNHD1G492z5VNL2Wh/jrfA34WPGa8aqHsamq+2w6vDtJ0P'+\
'/Q6WDsCyPEWQ4ch/554/n\nwj1ZK71ywx7t/pctTrI6DFV43xEMxb85p+CodG'+\
'p00JcwnOgUTsr48KAqO7MxXGn9YF9LDTuVNtho\ns/DQ50nL3tUzhQPrOt3UD'+\
'BT8IYk78aagyEMiUQ6Yqh3GwF96suQOZEToZ/ix073mmS9ErULIwZXl\nl7MR'+\
'gvrOfl48Yh6cmjYNmihlhA+nfqywlfxFdJFcah9wjRcAyZXCNgBYJMDWCFkv'+\
'VzlDEXYjICcX\n4BHPmJ+5lLwswUZLFf/Y3wNWdyUpNqsGUezh5SllcQk2GUH'+\
'zzFnhqlbw0UKScKc0wVRj8gpEisY1\nMhf755Uqc82cuf9jJ4ilZaAoW7j4O4'+\
'REH4cVsfQymQZRaF3ylgffGt/f+QDmpLEZSXaanYUHFG43\nES/3UTUdonRyE'+\
'JizBml5kYg1n2yN1XYQGBQBvhDgCCxY+c12UdOyiwG4gIdPoPINW6RH0+qtQ'+\
'lh/\nVnCZRkqz7QQCJmKK3n8QmfvnNvFdD5GQ9OaPblARB1JDF5NR/GrNulN7'+\
'X0S1AczrqMmje9XQWdjh\nFUL/6jRw2PRbvqob0L+d9nKOd07MrV4MR8FwwhS'+\
'1HOkpbp6/NFuvYpwjpVVphL2GkyQ+fvY0c4Vf\nX7haxUVGlzVDZeXIdMQ1MA'+\
'0MUyaFySdqK3cTXuutCPsjfaE5Ec0OijP6iG6nMQNmOoLazyICq1B3\nsCqbt'+\
'R5/Ydsnvfx0dCmJEt4PMyB/Y9Y9nW3UY5/QrJwpmS7lilwuzW7nz0M0Tt+hP'+\
'JnmR2Nu9Bq1\nV70OPJ/YVNrfe5A4Dwrw2TGI+9OOe8HS4o6cyKj7ThpGsI5G'+\
'8HVEEW+M1LHRQrqXsgn+AJuD8AwO\nu2l2TOpHY9JAVFu5QOYkyo5T3NOYA7K'+\
'hy4n/ONqvOquxAqeLsYX16yP+yzm9JB9VESBeYXmgHc6q\nYak1YN58jgvEeP'+\
'BX2+JZ5ozf2wKsLC+WtLPFJW/Zy9tr9QtLuNS/TjqcZg6qDvFPabkyH0sJw3'+\
'+y\niMQqTK+ZBCRYhgospbGrmbUj2vd1zUzb3p+81l6vbzK+QDt/pTacLHcPy'+\
'aZS2/5cbnPY8PSKdsR1\nSv+CrGkIlA7Fn/cLnbesCmbsS/UD1S3MZ9/PBphG'+\
'DdvLLkyviD/YjwYx3vtQNX5lVUkMS7xDElNy\nrpsBskRk92aT/Xo5bJ9B7iU'+\
'JlKPYh49bZgLnDJJVI1/ljdYkX4+f4xXVTVnfO2MFWvfXLktVrWA+\nWfmbdC'+\
'XhDIN+Qx9CMS3htb0SEzOWmkpjEi4ZDXzoW68LgyPSbQ4EvozWbdo8P1nd53'+\
'L9h1dEFLNO\nOW+zzTwlVhWmUrAG1aenesAEPA+43LyAw9SinoyRu/tF+dKCm'+\
'AMUW0nkD98aLvNiimzpgLPeR9Fv\nPRdEauq97WtqflcfG/U9JihKfY19X/x0'+\
'IYq/6KqRNkvU49BqlGrqNd8AuXSuF7eG+zF2MxDhEdla\nBVbiyWkm5BwNqJs'+\
'QjUcwYDTk/KfWeX0deQUWojdEImQ5jhi+TnEeuWW1JT0et9EloXvfuAjxOGm'+\
'p\nFas+iIzB1u5L4PREOHxFRjmfDV/rbaHoKr2T0IFojOPCjQYv7rrZRbEbPj'+\
'cYlN3S7NUVeup2qmhD\n3tPCmkD9EV1uOcqHfWGtlrUMU0jzvWhQOeD/LcYJw'+\
'Ax1y7NPyyx+rrN9X/84beGqO+XxEF3VlEG7\nIw+z5fjQLMuOruYBIuRis7Bd'+\
'VGLVx7dkSh/ip+UsazyZ8/0MLsqB2BLjpOR2Vd1YMVMu3O3pf0Qv\nfyhW4VL'+\
'Vmh2lmPHKnoP9TohpmiKFyNUxGBuxeFN3DX3NlXxHIXujyABdi1qbk/s3GJx'+\
'15ckKpWOP\nVUYv2b56IkgXm7qSlj+WHDFo8rnlaNQ4/tbGx48ZhCjX+JRA/a'+\
'xszkkl6yuJz/eSQxGGfAJJhwPR\nD/dNK6Ba+rKeznxDzrWjAzoCHKuCHzVLa'+\
'ZUHACL9jB2N26Z+qkFRSypyiUvfK93KiQP9VVg1/inm\nW7D7AWU2uNdu6LoM'+\
'90hHfl0UMzlEVge0Xbc6Wg88/4vz247kaqJlLh4Qb0d7ffqzhgLe2iY9qMA+'+\
'\n7VVZVs86Jwb4JjL4KsLBdIbD3UEqClA5Sq59UjiNSzLYGHckpQNTKdyDmou'+\
'H/dcJwm9imQHYMQCA\nAKzXR48hfgtFTsrn7Ndb8ym5Whu+mHZ8s32MaYtz3d'+\
'zI/8SZ/T3DHFXDHXD1U02IAVysYSqqyQiX\nsQOfaI7Q9YTOsc0SYJ9Lk0HfE'+\
'GDd3mGf41iqrLhrwCLl4Tps3cApX3iBPOSa5qlUkFFt01c+Xw6t\nt4o7IMtU'+\
'x7E097Skky+/8SFf1frca3dFRLHC/Let5Tn2K6eh8yoQRk1nBp9Yxn3fX/wq'+\
'0m4AJBnI\nlbjFDTjHWV8aeg9hI87Q/dnIp8Qy/t7Tj1cUxNV3+j47rlWTaBQ'+\
'SIrlNcgA4i3gh3Mov6qJxSk88\nzFIiureGzhy4QBCk4zKAOh546Q0YyjYpxe'+\
'T+7NWJBuCgKoDDvGpv+KEUfdofJKQ/tChiMK2dllhh\nMEtR5LC79Q5ejJd0u'+\
'2dHhrMfTGfhyu92M8u/XmlKfVU992drqUVY1W74sL+QHvRCYhwItOxPtC1L\n'+\
'NaQeO6rZWIpZkCRnGU64BEi773dUimVpQsMX8Vt/nZxk7HG3fyf8Emlq0HPX'+\
'dWWTodwhffioJekq\nJxI857glMfM5OZeSLL19FbCg+/dmoUgD0tYVDRKEVzy'+\
'qlo/WtUkHXbE+QojAXGXXwMKArAFcxS2X\n2QJg9+O105MFWEm1g8L43ZU8Ip'+\
't6aT7fJt+rUqEBYMyvXuQx2aCclGIkYJjx64HeTDkDa3tmtM90\nziT/m3gN3'+\
'lUwFopw2fYGoPo2bhviEGtLHH1FZySC2ogmZ8j3wIpgNxDu8681bmAGK/riY'+\
'7HzRcPb\nloU2jz8PbkezB2NL9271Xp1JCBsci6UJpFMMnrC6ES7Wh4KdMyN3'+\
'tiSSxugfuGXR8bQzbuJs20kI\nXbH8l5DOx7iZ65rMNQUXRHpjcGZ1JoXhVSb'+\
'gVy9YTCVslGHVMJIGz3S31W0EodzWKOoFWty0pAeT\nQQOMlfJSbIqeul3gdG'+\
'gEqNduBYSHvNusHPNUj51AcPWafDH5+q26ffaENgbO1yb02lDYvmKSB40+\nU'+\
'0u4vo88B5PEy0QHKsD9AxOK8hr32HrorIPgGvxxIh3MP3Ru4N1EztN4wi5Oc'+\
'dR6dLCXhzmfHKko\nq0I+GVz/9gh8YDQJavoXnRpEOZFu6T4cILodH8nAbBgj'+\
'jqrawFneFpByQU/y3LUr4TEK4sHaEJpj\nVw8Fzw23jJv6j3BgqvxaM3+UYn+'+\
'PbnauooCwv7MVl6qAuIq+Lvu1Xx/qycLPbDanqqsnlmvdn42e\nsH5xeDPL3s'+\
'aths71C1btlGa0n+g6DJpdSD8t24O87G00eVowIPMgSZSLqS69WzLSeo095m'+\
'/3oSQM\nvQqM+EfFsA/u0PDZh+ATrhFVkG87YNezd3uoJtwnFgL5znFGnIUxe'+\
'hAsVRJossD4IacNJWLuG1w/\nVhx1tPIlDM8wJvo2r3xQZBEHuAIqsAN43u8X'+\
'T89VyHCxaNmUycsbwp5/A9Adu+/GJs8MXsaW9QmM\nxFqA7G6YWnjhtrtELgQ'+\
'or0fNtocbvl8UMC/fIFNpUtAo29ukE/riqWUX/X1Tekemiv2F/MBTK2YT\n+/'+\
'SYnNuO+HNNAqA5tgqrSGpOot1CIsHdaihCVGum8VOX/RM/7APRry29b7PrfK'+\
'2OSYMu6V8XpAxr\n401G6EUZW4RnX8N/UDF5e417l2O1MEbZZBNLtUiM+klCB'+\
'EJwFKHI89DZhrDVu8vTet2fcMn4EVBh\nohOspZWwmr2jnKqZVn5X1MX2Kbht'+\
'SoBhRuANQIWDn68t93L/HonFTMm6zSxlZyAv4Tw7HbSVEQjj\nqP1IblBTPJV'+\
'75teCLEvntAF2RPTfxQ5QWrZsH5Am/4Kj9Rs3hz+kY0MYelMpeFMx9TXbUDZ'+\
'roSLS\nQG/gmMb62fTDAzE9IaIuTHCr9CJ5ynB9DUjPISb9g16DqCNuTdfeNs'+\
'YDwy9d+1wKOG2RDE0t3iml\nTjK9el9s6PZE3tskK59VNvIL8npt6mfUWwTl2'+\
'bz06HtCEi5++Wf2GuK52dNmv/0/VpJo/1Nq3v5A\n7DouDjVtZwXhDvh28Z+J'+\
'enzeF1+KkxDHWqKm9jNcl1mT/btvuebEZX1DU15n8H87HiNSlTYMW66a\nCUt'+\
'QOc51xn5OdoNAumFDNJ5zuy4lIkj1EgN4PUBr3UPzJtie12knvXtZXZEQSUV'+\
'vCYdVKC7N79ke\nCqdekNq3Sr6ZbmQ0InRKbRctNf5JuwwSt62/KgTRvJwJ7v'+\
'mBDTu8FjH/Yc4gM+nbYjHj5Sx6N/bD\neS0EDvUvae2G0Oc+RG3F0ESZXRPAs'+\
'd0+STiCRrihdPr4gGp757Tp5bdVI0Oc7Ix9tTOB3WhHgsA/\n1L8IgrfcGMhu'+\
'dOi1yOa/u3MQazUNybRg64rMEDj4/5cYHWa5nG6nehDlPzHGUGkdXgNMpGav'+\
'O1ZG\n6nmKyd5O1o3mYSPwZ3cqZv5EJL7HTXxEfUihozzALy9Y5SsVx6qfoR7'+\
'hLzjEg+pzMepfjoUdc6Oo\nxmLZyAGOU9fWXRAYBABDIFAoDAaHI5Ao1Hm3d6'+\
'csLGg0KysbGwYjxAJ+BEjQuvB5B4nhAAdwiyVo\njYKv8YFrhUbz0N9FwZWSs'+\
'uBnY8RLZxTOgmvUfhBPdbpBXRg8AJTPBegDvRwEVdQXFHziyu+IBaFG\nQE85'+\
'fLMf+o6UjoOaxh/+H3snQZ2Ta++AS5EdnaWBIHY2ZDkbeyqA69Xk4xecd9Pu'+\
'ctYD2PCyv75r\nDwvg3wMzkpEBqg99EbfvIogYKOiH1tRbYbgYTMSoMOcTCCo'+\
'KlxhvC+iJoIC6MVjJWDsk8Nilm/uR\nPaiHI84K1CoZG1EOgkfYgto4DEC3l3'+\
'mftZSxI2n/AfNvdnt/QTIhLEg/VnpTwWcYwhhEVUJmnX34\nYqpJyThJgBeUf'+\
'RQfORDAhmTlBPCAkusxOhNI1gugTVkUG1Jr6pMb8A7HDm7n0HjuF64T9MkGh'+\
'eTo\ncROdQn3FISWpoAPk6komYNHBCTQIAF8GDSEFN/MwzqBGjAuo2RXUshuQ'+\
'pDcv9hCEnPxvsgT0kAMC\ngOHZYhcp19TrFoAJSJYRgZd79WOgRCQnR/VdrGD'+\
'ipBLyYPUPUFfWTcEp4gh4woG8ewI05Zg61J76\nRwQq6SKhbjpTP7SQsaylbK'+\
'DnP/77xNYXhrwKALPkc039UO7kYOG6wn2F+2rTDzmcZi9S8+FJUUkQ\nJ8cak'+\
'kMY1AvIv//5C2/WXeQb7PTU/zgu73gq/O+P3725F9de1ybrmpl1bWVd+xrZK'+\
'9nuNcq4Vu51\nXYmSSkKUUNkpiUtGE0VdIZSiLqVhlOL3+f7+Ou9z3s/zx3m8'+\
'zuO83+c192+qOagejNpBNuBE1m7I\noUmgFmmkyUO58Vs46SBvXPzs9PysEAC'+\
'5aggURAYLXcqquEoPBvEgIaBLbaB46Jsuc+S+RopQKOiL\nh+k4IbRG6w13h2'+\
'gLzw3G9qlc+6b54yJ4DE8FD0pj3v7gYrvBT5BhoASARegl8CIsvawNebkKvH'+\
'TF\nQmb5SDX4/VXwh+X+4dWPoJl7yFegAS4CAUS2Z8QfAiGxnHcAhPTUu2ecd'+\
'zFIaSQW2do/O6QyDXLG\nIfpeg94iM0vh6W9Ac1zQuxrwwEzAqfY7RJdaZB14'+\
'Rvp3eimcJzSPvAaerQcvhMaXRdY0XJcWuvH4\nxZ4ZvRE8Me9yE1m9cuphkw+'+\
'pOTToJim9+ttvZEtQ6C3S7ZXf1StBd0jI1qD2Fcm1NjDXp11lsQNp\nZhYa36'+\
'ki1DXwtOKQn1jLx+5r88i74NVP9AKLnjOzulef/zQfv1dzH7nYS5zzi1O4YL'+\
'oA4Ed2pIsc\nHxF6QEACAHxeYmvzOn0/fR7+B/50GegfGBCi/yfsAsdlYNB0Q'+\
'GiI3h2pbvbo2k36MHLhWz6f88g1\n7MVR5P2pO1cJY+DQy8CcIjAoQyXjd2Hu'+\
'EzAQe/gpMqj644lfzyhC558PVMeX9kMnQOAX0kHjv/8r\nRQcwgSRMSgNm31F'+\
'WXjq8EpLOQW5khEZOCU0ja15Havp1nMKC+sDYN/DxhYNccCvyjc1iHxccAgp'+\
'K\nXY9FzSCJ+Lfg0dTYq8eZh0gXJmdt3v4IWr/pApzzQc6DJ1RmCdh3YO6Cyu'+\
'xiUnuVxuzS7Pv/ZGgV\n+gBeXQZvOFeUh39c+LSwcngeoenqDkZmgXMBP0Kfr'+\
'6yC4/PA2UJ5gM/gE6VwdcyXM0geOPI/mdLX\nwH/Xwf++gvfg/3nfwGsb4PXv'+\
'4P/ipXM/wPM/wbP/Y36BFzbB1C0w7X/MNjhlBxz2+/+Z8D/giF3w\n5v+Yv+C'+\
'P/8DTe2CeaHgZfB/8PbH/v/uDQgDIDwAkCQhp/c/7CYQkgyBLpnpjLv9ZOhj'+\
'yHqzHtWwT\n+j2pAhnXG1v4b0uAvISSYMttemOQVzAhOGRHZpkjg4D8RiIhf1'+\
'CQ1f9a1gIN+YyBcJf/O/JBZvgh\nUVjI8f+iMjhItAAkSBAS/D9GCBKCh3yDC'+\
'Y2FA0qDbvQIowrOxxf0YzdhfBL6QrIGmmxUQRv496mz\nifuvGycBh6+wuqZR'+\
'U5URFyMOdKXmVZ4FVELRHAn/Go+GK97YX8nL13unjlkBIoERG4Cf//ZHIn4g'+\
'\nsJ11WCJWB6uL1cOisY/3+yejXcFX3i7PfJxZnfk882WGN7OfrfBlbWa9ZmP'+\
'm+8yPmZ8zv2Y2Z7Zm\nmm/t7W/P7Mz8nvkzszvzd+bfzB5xRr97/kDC0ozc44'+\
'mZ2Md8dOWi9YVUF91iwgh9CJDneUFpED9V\nc0ilyQtLKW25KGfiJtzaP5bDa'+\
'6uzy02Ep775GKXK3ePy3upoEHRB+qlGl4GKzKqT4Y1KJI0OOENw\nuP9Cp4u1'+\
'HQnVcEtJp84UsIlQvNx914Qcv2cF2QdD9RVUwxxF8PD3rn6jkE0vaotM0hrT'+\
'SoyjpCs4\n40MxDSMvHJKMyDtlQsUgTTvaBM9+yEGvXuvrzlGPVNWwtmNE7hY'+\
'vtuJQNQG8B6r5QaVIBJRecwcw\nlZZNX8gEUbx9vaiiqGxRnZf2C/KPhqh8R3'+\
'a/YBnuMN5W1sG6prf3QUrf78/w5zNkphGzSsDoaeXP\nZPWV29EUkUUkobXIk'+\
'ta/9sEB8ck34ZtqUH1q0eagMYeq5SrXqHbjrPHg5RP4iQIhuCww5WuL3g+c\n'+\
'VyUqmrck/6KW56wIH591evS8I//k3uHUADdwGrgudOLV+83tQTh58jQ/TUiO'+\
'KgY9JdnmhP9Awh0+\nHV1T5OcD1Ku4e2sDRPtCT4Uuh4MAoDlSOOUrH5C2AsS'+\
'9tQ1LBkeZWAvhZ//VFPbXyAyYBPJuS19t\nORWmC03FXQdK6/IWc2KUiBN/pt'+\
'b/xgt8NkS46Uf/UgFJUyzsVACmwlDxexNpAPC/f3Qu6QLk/Iu5\n9toLKCF6r'+\
'/nOKpHgXZP933A/CdwsafWCQIA63yZEhxL6AbaPXA+vgk6TRdX4xcni8t2vA'+\
'vnV3WcO\nur+kHmaJatk84CN0G1uGK0Z3B3M7QAfdXHUDVyG+SigovNTkHAWc'+\
'1qh+lLejazqgGj3OiW8sgE47\nnLQH30y/E59gU95EGQzDPAJP8vJVDcL5mi7'+\
'YmCcnSHbymQqfV5SMQAIOtSybJ9Mi6CaNXH9tvqQ2\ngvCmhnxtfMQ3idbTZG'+\
'wMlH3s0WhjAizX5ploH7DIql0rWC0vs9FFGm1NvJrrjgGiYMd3CXlDuH31\nw'+\
'HOU94LU1tGxCPlNYvl6DPvckRZYvXWv24NW0UBL5mgNJo/2oVUiYmuR7HrpN'+\
'oIIoGl2KZqMlqk5\ney5ov9BOFb4PO8sF+fmsggxvFgMOo6CS1GQrM6MI3TZp'+\
'm8q4I5qm40Panc1OAt53q6R+n0TwdeH0\n9tPdY0oZl1pyub+OWA2/Prb8CXP'+\
'L47IZEML51REnqf7v1QDkVz3TqebIq6S0O9y40vAdYJFsdIRj\n/OOYu2mtFJ'+\
'mTrQSpWPXv7wq8zPT8y7gvDBl8jccXq29BCEFlTYCNr1tf02f+VKCLbMbMUk'+\
'roqMsJ\nOw58A+yqoZPYwxcoG/u36xCLKjpbprTGTPy2dVdnP++SLzPYQttWK'+\
'GMtIiezet4osreVIgUmguqP\n1VeIzv3EkPCNISCWE2e8T7K7O+ciDDj0qkLW'+\
'9u1Uo+ERfoFaPlLETkyCTP0KMK7/xIOzKwwQLwnN\nV6/co5nrxfTExXN9PVZ'+\
'/0zXyxIH4BRRtSilxkPMH1F3bxx80myuZDvFee9rxHEcNmVbcukuiSb/g\nlq'+\
'zE/PyMk1WkwUQ0V2NycjbEpA5j43HrIyx/KbsP+0CUxzGbjFLgJ7bTowQIfE'+\
'OtCOFdNyGgnCRq\nkmApaH7pvvqGzqsY5JdNFyz7zb/OhG3RobxRhDkzs3Ln3'+\
'Hyj1PjdYEce1WLF2fPab3UjffTBDj0X\nIlMWA9g6xyJnaAzbY+o0nabXZeeU'+\
'M233E3shNRRb/9TMXjZuoBJ8DnejbhAmvf82b6slQZC3MKY5\nsdez9LrF3g3'+\
'DHOR12WyTIAb6+MlDMS31iD1DQ670flLf075KLyLvxlB7X44reId3lVDT+zw'+\
'Owt9d\nGZl5PbNGcvVSXY6DzwZzCPArYOAsAZFhatCxPmAZP2Hi9KyeL2MgpH'+\
'yA95Hz6apHadb1Ba0xI/77\nY5bwO0KDy0O434FC66fLv0kqdcsg1Dbvf1dwW'+\
'ALea25qOiCz/bklRjZQlMH0LLaUPVis7xbjJxFR\nzKc+wdf2G7aLRhf2fs7K'+\
'qPsIOYSTDMSetXlWds6lcodN3juTb/nPYFZZ+HXEM1UPcuPN7LqS+gbd\nLYN'+\
'wuCB2yZov4I95Jj84WwoFe3Mfmi3EMbR7EF5xDSTKU024/+41Dv772NHHjw0'+\
'r/9BmRza05kzm\nN7hMHm+w5BlY6+7QjBaMhtrd7X1m69G0/TJGv1k03Kcbyl'+\
'2dSwrVdPZeBIEz0qK8TSLvXcbQnKxF\nUqv9hspXQeunduuFWQ0nXxYc0GGHg'+\
'BwqJHDN1IPOTqi+rBMV+3SgV33eIM72x2gHtuMQ34WX/Ht/\ndG/sAqIyMZvi'+\
'CHv56mVRAOQPzGs7ofT27Gk1sZU0kFfpi2ev9750W8BMH9jZM13Rf5KDwJLW'+\
'OnBr\n59TDD2Xzfgv3ulFFkNmHekMU6wSnkOWfZUH3BwrTYQASM/kp26moQGL'+\
'm92/bzpvdepd5nYeCHFKg\n245k89mfIr2wx3ZE0QlOWMbViVqNYOM3uQN9z7'+\
'HFndaaaNJowid2o2h33vtWX5rfbL0jOnIk6oxU\nSrqAfrYU77GruHEMzlXaJ'+\
'Uwm/WGlOMVCGSQx+9eW3xyMPqPDK0y4/OljLETuJVX5jbGnJNtyNqXy\nLAh7'+\
'Sm1i16acsnP0oJ0pb+mP+ePTW1d8RXY+nIcKq6a1mECDy4tw9KD0dL9FIYgy'+\
'lV+dilRaMZZk\nipIkdn6KwBnVXz+fMUKjQMO03ol4LVVfSKwgNYFWrkrxuju'+\
'BYyfZkI7Da0QsDx+g6diTKgjXCORO\nI9JePmRTg1BGTgZoRtDosrFPW7ZqY0'+\
'/4JytpqwqqESoZ0Bo/h2TNZL7ac+Lelgd0ycGNV0XEiYQc\ncQI58JAGUvPkI'+\
'WrqcavGiV1oFDXVdjNEjDz0YmLWBHjNox3VmvfFYupuQVTQnSghJxKhE4NeD'+\
'VuT\n2oepEi98Plwtri8nbeRCG9YpNJqv9bPMjKyy6yqI2FVTBPLhPMN8+zeK'+\
'5f2Xyk7zSEPWBj/obMf9\nU9uYEwT1eiLrvBvTUpFil3dnt+P5iFFGhw8f80E'+\
'fVcJOKOXu2/s/HxwRNS5jBwllxt3VjG18kgoM\nxKT747a58a9cOs51abOqDJ'+\
'nnydATbbcQ79QRh6+/fr+fCpkfUuOyPCYVTT04itfGlUMi+yWZ+TpV\nh6ttd'+\
'v+l5LH6vEz7YjPOp7+L2ceV4+lmogCO0Ei+ecypM5k8CXDnPjzrY9tIQYIA7'+\
'KzmVmRiphGr\n0ytl03cgv20jl5NIYTdGCinusXzzPc7VcNOiv6QfpQ3WbjvB'+\
'pdffVjRef6qahYSJ2Yr4+n9FfN9T\nH1ypYx6p6SLKrzbjNgKci/KlK29WRN2'+\
'H+KlYsbLW0vl4bjpomwqmhHRuztc01lECmmEEFuGa96G1\ni2/jSBXv3kZCNN'+\
'Gbjg/jgAVzFau4R6UMKFjo5JrrzJrADhyMq9G+s6ykLUgQvCQ4ZhgeH44VUv'+\
'l8\n5v71UxaCG+Bfu3ogOfEwkjTy5WnxdmlshS3bDR1jZmShr0bBmbFxDJmKP'+\
'bfS0rbJIdjs7oWYgq4C\n+Gf/az/NCfxxIXuJtiePVGoAi1SXZk7ccSBCVcJZ'+\
'rq8ax0bDX979lzw9BviF7nFVdd55wT+brqqs\ngdVIl995HqUzE2+Q8P0f1+7'+\
'L0PlRS40ZX1VEsYyO6ugar0Ls9IBYRlwp+KSwc9Ws60bmB96dQl5z\nLxhVD7'+\
'Cf+c3iXSF1NxhKNYhmIFNjT+lVxo6UCXwWJJjIFFOnzzFuvUF3zIzafknMew'+\
'JiSC8MckKW\nmD6q8cRAQV9TW4/mqN7RdhH0DyDfhKT3jki93uwQ3BssJZ4ed'+\
'P2n7MoePKlNlv/x+BWOBZ86gZLN\nEUzBTkd/mITAwe1AtXrjF74O2rChZGgP'+\
'7qSM98n202vn+HG1zACpXwiNsM2xYaq1BGGBWP/mL/rA\n8ECGOGHU1vUhZ0Y'+\
'RuoLVUlJSSr4ZveEpEudnq4FI2DgeM7dOGpAPkDYorU8grWXEkugn4g4FqQE'+\
'G\n6NbjJBBdNKIX/DNnDyBj7XhkedAGA5zU+3VmXTHEWeib+s9sg2i3RC2IVg'+\
'WQiQP+wQLxIdEk9rFO\nJOuLOKBON+MgkLilqXB8LoAco5Os7hQwdEBkQnwch'+\
'7kl8Ej1owya3NhcAzK31s+EFElVueyHUE/0\nnuh6AImiOqV+FmVXn760pTH7'+\
'VQSVpYwFlcDgXUGuD6oLs3JnDxbX5Njg90i099JFQCDjbEHHYk9D\nZqhnQjZ'+\
'cs0XltE5EJO74mtjcTevl9nIxSnhF/9PqjR5IlXDgPAVrVDq2DQSo41KvNsX'+\
'O5GKACvdD\nL+WKiKD3H4lf1FWGbvKxkhDZ1OrrS7fl4xSZugkgiufzLqt+a9'+\
'HRotMbuQSvG3WCPVUS5y0qUu9U\nHToqYWXqKwME8F3iqsMPhCx/fVMAiHnmP'+\
'lS5ZkHjvfFC5WC1/M8XUBliqiZWJD0BMe83XFRCcGnW\nkJcq8RXIZo7zrQE6'+\
'Yg0tBl5xoH1Lcj3Hn8hZJJ1STzueN5ZMz5DhNzSGJws5gLLa8u6u3zU1zTzC'+\
'\npOUH5DvTWeTPDrd8sl6mabMSsnylNVCHLNpiuun6TzPp2UVvRebFQKqPWS4'+\
'aAdYnpAFbgg5mEglj\n7bhj99mfC4xcJ1R/TLsSttZ/NpDl6iHRIENq161Z/8'+\
'ghoutV1UeyjF7VSpXEZ8QBkfuGSAuUBFmB\nDtBsDFDljQb+k+8pXvYRxSlmG'+\
'Qj2urV2M7YdPBl1wpsxx+8m9QR7xWT7sapUxe0bAmlauQxMPkJf\n9BUKG9qe'+\
'qW3nkP7NKyKcYnfignEe6NFlct/QV8X7XE9O+49mhTml8q6/iv1VVRJe2UIm'+\
'eKkD4mgb\nqXdNSPS3c26S9gwbTGMK/HCGGOjHlNywl1Lo49Bz9Y5t5iGV7k6'+\
'ApyfLFXTfvdjLu9s/ItZwz+bv\nz+tUHK5FHOen4YmlYaFP6dFKU9/Xqe7uy3'+\
'j26eh6n6ukWbRPYAoak/QXzRwpup9td30EAgPyet2j\n3O+soL5YNK06ag3kj'+\
'WuB71wPCRZ37mkHTypH2Z+wfgEwJ+GfF3cpMgT3xH92a2vqpicEpxH85o79\n'+\
'8VBi0YfLbOhpNq5SpGhD9TsH6yw6wPrn9DdTHnslhBFOhZ5IdT1S47oRqexJ'+\
'szfKis/V3K5h8O8B\nfUdg4PtfBNSvMeRNQTd2VdFN3xTpAe9sz9u+f3NYM+c'+\
'U5Pv+1iisL6AoDJ/XoPodEwU0gQ3zPgKi\n6kSF5gqbGzMK4XY7Be45eVYPz1'+\
'570BJVB3AvED9TzeDKMZt8s2VwMUeaugzKAj/VyezMEyRwFPhw\nIPSnL03oX'+\
'5p2yva2yGd81rYMzMupaGtAxmJRn1f5kdnUoX0FD8+e+mZdEtm5p1pFitJt7'+\
'2LeEH3x\nqQpQc6Vz4bf2jirkmWjVbcBOwcJG0YxZSKlZBFUqX6du5ZTyWj5z'+\
'VPfzCVwGNj03X/x3skWUxXro\nYXN5q4luutEhnTDwPcHE6TfJLT8WRSxX7dU'+\
'cgL7yXx+6JBAFWQ5ytAg9T8S9780U3OWMhHCPjVU1\nknwYWfrCIGR0VMHrgG'+\
'zZ9YsaRdfFhCJqruXyWyCDQuQw1+YCMrUYCC1CKvyZUgai5xzaYlMEeKf3\n/'+\
'OgJoNQDmPQYuBgOMMQFgSuFRvjAYxlT89g7sF8XnsQUUMYpyq+UwbnwEMzdN'+\
'dcEncbbUV+I8QJn\nEIbybbDeOO6drqdwNJIpom06WFpdqvWSN+h77d3DZZwU'+\
'SZmKgmRQoWercAEBNPfzUqSpq7PmAVQB\nSJaQOWENCXu5XnE7CKZT70n7hZY'+\
'bb4ziVhaFNlDBTXKAhP6ISwWmO5dV2xIT8itWbP5Cd3Jl0rvG\nqiERX0sB36'+\
'PyYAYaIQG6jWUC0SHSuTb63mjFEv2gWn49qqLleq6bK4/tBc0jJIVlA18oRs'+\
'9c0oSK\n4bFf6JMiRC8fmQnR5zCFkFfx4ijfZ41f5hCIWV2DA7+u3Xj7S+bEV'+\
'eo5SmmYSYKQzWvFnD/mt9Wa\n9KJgXpCEudwvTm+T8WT3dY3KZcvGMStEyDbd'+\
'rGDr5mhhiuyfzqDu+tjs503HbIE7THULqcazc8DX\nUaFxyKH7VHvejRcNoFG'+\
'mjeykYK5HSeEAsxy3q6JVP6AU7Na1j28X2nhTCAUY6i+IZwHBpB0UgWhK\n0L'+\
'I9fw3U9V7wNEJMHvjetatd/G+rQYG6mYIWLlICNhD2MvkwwZPEykDphrhNE4'+\
'pbfl3SiAo77F8l\n/yTMNS/DqRVaCD9dCT+Tcfk6Y67mJDsY5eT+vPBv/kXgm'+\
'acA0Td5K5/fGcIE6gGK7xqCbfjKVurE\nBh8TyAFnFderfz0o6mpMLvWScYND'+\
'9vOy8QhfqouQZdWwYZDqoLfUvqoBZVKU5WPUKhHNpYQPSmq+\nN7A0L3Ub9gI'+\
'9P/QFXlNWNmKuIkgR3n18W60XJFdlnrIYY29mKosqNrKpONUjIFCU0yeVKpM'+\
'H/Vtx\n+ieVrLNF11vleyhOvkt9IerurdMooQ7yOn2UPCxzT/YW13JrGJ54xq'+\
'+xt0kSP/8oDa5WsKF5ia8+\n1ERvd9+SVC+yLzek9so4lZCZx4TIp+Qes5X3+'+\
'TRosg1UdzEdKehsmrxsJ/y7KQh1wLbp3SumyBUZ\nehLahNjoA8wGaCRDoa5l'+\
'9GOvtqwOWdJGWxgjOVxLvciQ15T6MUl3vt1Dj+jTUILGNbb5DKfpzwfe\nwBv'+\
'eGYZSKPADb6XYlX8kn5tnSsxqdrHpM0i7TKTqR0ktxQQHNRR1H34RqhOAECu'+\
'dMCVbCRfwubvG\nSbwM4/5O/JA15ow3z53NL0cNtTv9PNMGyMoKcn0f6pBm8l'+\
'sY1ywbCK1dyfU6cbZu0bum14fc05n7\nGsYg5/8YK0+dxAAJGn/4KwQ6Oeg+7'+\
'0VYRE6QlqMkJEKAoVSj1ADlE4MqPI9UZmj65Y94o4qNR67e\nKCsoQJmHgiXk'+\
'hZEWYOUEUhgHGaG21tpX7BB6OgTSgyefaK2trFVpxmQIZYspbInov6aNu6xL'+\
'ezAy\ni6Q9vKDgJr4LubhjIn+nGXmawZ0nkxDGa1+54HcxaVW+WMbrawaQrwr'+\
'E/r8pjCs1UiOoCHU+RG0u\nqk4y4tS4kGmXMf+1D/UflsNMYQ3Xb+xAS2yl2e'+\
'faCDofZmzjbPUzvgtpF36X8gsW3V3jzRacUQ2u\n/ZR2R/kUZHMfkQWVehM4p'+\
'FXZLjzkq9RqJRgY87KqLQLbOf6u+lyr+hPjCb2AJKTg+O2pN4/V5KNf\nOB4H'+\
'fY8h8JbfmmrLTz5SlvU0D+GTCRUkOZyTbqzOOOtB2uBNTQXin3NiVUxUCgT4'+\
'RLDki7Xr+bmP\nzsMG9BbPQZoQSq1KQQinCtO5m7nfWMrCfOKQMxp+ijUKKgi'+\
'tFcUBzhNgfr7k9Cz8pf15E6ovxJym\nlGdhUxmIynIPHXcM5f8lHserFYBivM'+\
'g3iaUw04WOkklUg/IPgTwl1u4NLifln4qelWzYMdFlH+Xm\nrgLUr1+M6slp6'+\
'1+PaMpedIrxYKjfYUi5Kmg+krhTcknlRvKe/XMXxO1vchiKWE+5Ioq2IczPz'+\
'hR9\neJShGwwEAzD6LBs55PRGxjnG8Hv19yF/FjNAIPpMjQrgg1VRSP4DyieL'+\
'rjLgXRGPElX+l44cKAUW\nEpq5lhWNNsxmIEHNZAngTxtAg+qpssbLNT5lI2D'+\
'/Pfkwi1/MiQKDXWizmJElhi8PVPw9s4YGKOqz\nEQS8xR+xjmmze3NPbxXTwX'+\
'22pqqv/qYUDmEkA8dbxDaBHmJCjf/2PkU19+EZk6nm931SJSK/7ner\nWElx2'+\
'PiyIjTbgzyBVk1ZnAfRV2ug9ydwgEW2DIgp677IJ2HwOTD6mBXnKuJhSTHfh'+\
'g910qutRlin\nyAMazZn1OeSXKVj2lDWXxTJ257PM4xi5ZvwqR4GOZG5Y8Rqz'+\
'o5Ca+dl+4oDxpmQlJbijNDikSnfH\nVpJ07VqqDe7gAF+UZ+xjsQmNiTFhIPt'+\
'vA2ji0OnJIlwoKdat6+JDRGg41se2++yVOMS5EFbzyTDx\n1NwoauYLa0WMxM'+\
'BGp6Nb5hNPkOegcxGoTUBs/NKCao8AdLTbXjWmSNN3mV9INZV+0gk+60bC2z'+\
'5o\nw+PVHO3qGtsOFO9eWifwSfOWnh7gVT97eFu9CHjcAjqgurAovNTtDEIpS'+\
'EfdDEhJQGTb4K25JvLR\no+q63383ykHETt4WbORvVuBetLGHJSbHsh0aPSOh'+\
'Su5DnpFsvQqi6MwPT4c5w2NmEz/2pDmShQKb\nBwN22dlGo3Zj+bYsIVlXv0f'+\
'CTVQQUCGAaDl6/9Khr8LYJEh301lrnZgTwjS8mhA7EZIXHXT6Mfv5\ntHZ/Ny'+\
'fC/PtD6DdOxAPAokh07NtCR8a4Yb6OPtNdrFVGsNBaFfVTfbm+SG5tjkmU3i'+\
'4BTE8OliL6\nSrcQkHzlCHEm+Ppmjk3isatADQRMys9rCc+bfhPV9vCx+on1y'+\
'wv+YhCxf3kUMEtHTtFrSBpmzGpS\n/i4IAOgXN+WEWq0qqn8oXRbMEJwMD73u'+\
'Y+sXCP/R/ueuiqlK+SOYZpFYPh0v9jeRkrGDWT6nKaZh\n0j7cpFVr9HsGSWy'+\
'/kudoxu7CkrZn61BfhG37rHHloSqQbFPfdc2rybVIsi9E//exDZRBBSxClf9'+\
'D\nPZ1LZUXN1hQ9fd0ksWwAXeWu5xQF7tnM5S3qL9KNT5rLHhLpYdKvNwza3+'+\
'Q+C/noJrylOvY9uKDj\nOZFqtmU4ep/CkjdKNMVlSk8uevxjB0JK9/WUxIHPS'+\
'vDSQ0ZSCl6kW+VB8iR+rinGAH/6QAJkXHUL\nr8TWSqpK6PbRzTSS9+as6ap4'+\
'AOHqD1Iv+pjAWVdG7hrPWBqOAbzVFMrpiQXTByhyNpjjP4Biz4RV\nmnea9MU'+\
'Gnmo+eith6fptZK21SKwjQggBZkIsJ5JLI+UEj59e2yBqyAnQKBDczTE5U5j'+\
'MmLg6hvnU\nXQwXxNt+xTrvxpNSCWiX3zn4B01CMop+mKgKk3IWS5lPTgv8o8'+\
'2mYHAoq5ynG1R4zayk3/7qNGf7\npYrcpE4p1xc/4+rHq2BYeA8YHQoGgwFXu'+\
'Qcgn9xJciKk9RwUmL8gjrN2rY7MeM9EUE5qbEQXjpTX\nsV/3HaszGEHc43wG'+\
'cZi/D8h3sST9IDG1RQsB7RTTTAuqLsQ3s/lRze2+IivMQOhpieEDJncFJCGK'+\
'\nChlH/z7Mb14Fg9eJac61e05zcRvb9yFnmTCm2VmfBboins7zuHwzVfecogE'+\
'ha9Pju1i3POFtgpFd\nj9euNcn90eN4lqbIWxyU6AR3WH4b19snxrDig0pFCP'+\
'JrqlP+kDnrSlc4mRtKaaR7FopcVjQkPG6t\nqPt9/LEu325WKsSHJqoxqqzXt'+\
'TUf+bf0rsyrr9hPqd3bP1nWFQhVJrC9S/LvPbS6nT6JIsmEQanf\nHOoCsobd'+\
'+rQ6v+cVSrh/01nSqav7knsZe3YugdR92zN8VczUyB8jAem32sb5l15HaSq8'+\
'Y/PpDOQ9\nDgYBjQxHHj4lAFLdjODGvx53s33u4+im5rQJHgdBGLR80u+eKyK'+\
'BK9Z9OJiqSC9Q8GEK14qc7Ikp\n+O5JdoM44NxcJZu+KyWfaio5BDtDNnJnNk'+\
'VefzKr+4j3SMwBz9xZc/eOIc7M6/5L/RxQQ7FoPfyF\nGPOeKEvmMiZSyHqQi'+\
'UnZFs8NcttDQu/FWzXzzz4FXB/xGdv8luUlzvzOWapCgO0hEXnp/O7J0n2o\n'+\
'o0UWMVJWT0WtJ3HQl8vEhQ16GnjmgCmZTMUaRBkCW/QOD1CyBEE12QP2tDe8'+\
'762Tq7kzT4ESH9hb\nQ7RihquuBb+Z69uDFWddLTwdXPl4I6adfYKLlUvqCLE'+\
'oeEuPkQT5hk7C7SicKSimWuthqTWgofVa\nSrQoPcvbrKnMbKIeWkRCJBaI+n'+\
'oTcP38nE+IPgNkA113ccNOu2bu9vFefUOIuV+o8Lm9c8ldSAix\nJQjHoH1+F'+\
'Sg3SlJ8xqT8tMPN+Ol5Hk0sI/DKWVyx68w7GHhNxkuu0+kAf6qel1AruR1//'+\
'BATTPFl\nWEMBG6TneNhzhE1+XdhBQ0iYUbPoDQIu+kJ3/vrdsUSxUbOn+hZU'+\
'h9bNHIUQ/NtK/+QZzSgK+c+k\naZuG2A1rJ9vocM2KcbQI5wD9iDqu+/o6rG7'+\
'tmS7na/iG8lYctJk8cwrS1YJFeIPF+mbbPG++htIf\nvf8T1PrQQzbzcJFlr8'+\
'r6lqWfpbru7VXOji3kamd77DnH5Ug4BIooOqj6FIGp5+Cs2mZs9dVIo0f1\n8'+\
'9TpJ7z1AB6n5I2fJfzJtFTxpno90hQZ21z2Jq0y8tFoDqO3sUfAzi/JqCpT9'+\
'Gt/XnXoxi6+Mu8k\nHkkVt7KNUySdsPpq5SvJGdw1tjSiLWSPmixwjGT03yW/'+\
'PPyDXLNukyepCTkd+jdr2zKZjUhsuKj+\nO2k+hMpo/Z5qxEv0HPz7K/azZew'+\
'rMP/RrplkbGnz4vN/VT+ofGP8ST/84PRbH/mJ/p1H7WMyr95M\n3xTGRyTicM'+\
'OY+GOu/GAAbtMWH7P1SD0wKrXucAssxjQ5PTYkXtTBcvh2c3aGqmHMYQ+2b+'+\
'zQbnL4\npjNtfsydH1fQIV8UkdQKF9rPVLpZuKilvkbLcvJgAA/SbzmurG0dT'+\
'PXXE1ODy3CcdXHiRUZFv+F5\na2YHs0qfHttIqooSBGJwBK/tplPq5M4M6wdh'+\
'DEYA9dqiBz2qEOkdpf5iqdpctJtkJHwn3ixH8FPe\nIjbbPRwfJDpZ9HOQ96Q'+\
'NugiV/bO/dzjfuRM2afOGRXbglBYZPjbCzM7PY2RNzADpLNRXIMdYwNhE\nNb'+\
'N6ZI2zUufbtSEv000PgWqL2qonSUrucL6l/rl6bdDmzQYdXO1WNge6FVXIF6'+\
'O0q35/JUsgXnAx\n1dbJGN8Po7zSP0YGk64/vy3U+wltuAhGr+905BlrxfWg7'+\
'bRYnn+AOHtlzHCBqTI2N/HP5Ej++paF\nmBSyRMAI+lSE4+r5ybFHCmpYI3Ra'+\
'op9+F4HrKu8U5D2YddePO7g6au7JEXD6opyrWRd+ZlHNSSTo\nNT3psNvXhzD'+\
'9FStzay8jRG+NyIyPdZGlsWPHSyGL0eVCDLEXl1Fotsm7h6KUxz2Oal0kAK+'+\
'uC+Fu\nH088KiXTulSIZksxZjhgVNxgcsvIsd6DVho+jcZPkghXH5jjzgHtlE'+\
'fABzec571cN1TlThhF1YkU\nhfsgwvQYDTu7SXLmP5Le3+VPYA3qeee5KHmo+'+\
'pJ2lfGdGaSW4C1241X+l1a88dD5r5QFzjdL+wxn\ne+EMVGhDjQ0gteEgBFjz'+\
'ex24n2i9QLcB5Bo5pdX2n9+xZ86o/T4WnmDNNnv497OWUV3+PtDY135D\nAS5'+\
'r4GqNFIcUnXLxgdwM5PWu0F+EpJozQOYMSyAUDb41nyAEt/voCgRLaij4bb9'+\
'HICfQIAQOLFbQ\nP3xLWSsyDhBo5+hiOXCucXE/0MXW1t3GI9DDwnKik0y0d3'+\
'DHArmcem6paZzQDysz6HqkyU+IaDKL\nn3TsB8JIIBqil6ckEXNTY9fQbFOLT'+\
'wD3ashU8XGYw+3Mo2QUoikcx3rqN9yez/zUMyBm8vYMdMI0\nwD6TX/BopXpK'+\
'A/BJEWGfKJDlObdo8jHL4wI1TPq1oJYKaO0G8NPglOY6CyS4+xmH9jAhbny4'+\
'5QC/\nW9Xs1Eh18JbnWPIfEnEhSeIDVvdTPJ6P8Nt8iSILVHa9tgETVzDTd68'+\
'Si8zyDoGw5zq8SID96+ig\nHZfveSu5LImc0Wv0MXcFkxP+y5TaWNUo4EisgJ'+\
'+mZ3kBBFQZJTd7lajWQZhcJYvCWUdSl9Gft7l4\nTFiFs+ilhLkCU+5nVtf8R'+\
'cqXj4HH1faj3bR8ewjD4a/cYm+VdQE7I9awcHDuxMSJ/czobN/cP1my\nZq9L'+\
'vfgZFIygdiSu9dS2/dNMvI9ynn3zT76nstZilpCTnz+LHz1GTAcOXjx5LgcQ'+\
'9zt55g1zVqlu\n/WeGLASSJWv46C3VdjsvVVBxjeoFa7g1I/Av5fGo109qTtL'+\
'XpImURJQLJKzWc7D1KWXOJtb6Nr8r\n9iLmAPnbUY4XGXt+8IoVDUd5Dntjut'+\
'NqL7AR0+46yastRFcCqXiXlKTKktGX47g1q5ZlUGE9Pmii\n+DpoqacnlFTEr'+\
'Q8w2vMiSP0DCkcQoqENlqVx40eZtqoJRoRCkWbECFnlTEdMjdsZrQc/QYCCI'+\
'w5P\nJOLPQM7pneytxygVadoaSwV6r140pAfmJ91CiYhAOvVeZXU1A9oCgHyH'+\
'RaSUII2+D6D1dSMicgJF\nEi0skSWvOPt3N391xJJYet4dL8DKaMPSF0ZSXqu'+\
'KAwOS2jpbs/sO5hmAHm1acpJ2zPEQ7dCuOPps\nUa6WIQDzplvbukRHKxgwqA'+\
'36livxue9hxXf/p6stuwwYFI5B7X5LAmZxnnjNM8xWSrE//j08+3YZ\nNcdex'+\
'O99Oj1Tn35lx/1gs50wXgJiUphvJ9wJY9ofE1AK0qJrBcJfO1t08qMjMEKwZ'+\
'Aw6kJ51JDdt\nFBWfgFyoALYlJ2eSgo5mAGuXwfPKspG/u6E/CDVGlnHbxerL'+\
'xOR3h1UnTmdYHcLmYkqsdTsJ9oCu\nPwYk2QQjjz7BTAVoTb9F/3k+ln7pv0W'+\
'fNUGU6L62fMZ8oii2+eeWLfED27mxp7SXwF4T5z0UWL9e\nZFrCtrx6UDxFFr'+\
'nhBnjQD9cPpArCXbHWGEugTo1dQuodi8ip5fSMbyv7XeY1l07vjhAsDF6kpC'+\
'Rd\nzAPamDa8gC577BvuHJqSW0/afW5B03Ytyt0E1G+Mg0FaHgeEM+3tzKx5+'+\
'Ymv+vX3RiVURBAl+3Km\nWcQkTVaAan1jzjXwmb4TV4JTx9fsgQvetvtku4VP'+\
'Za0Z9w6qse2U5/oyr/VSzH2TvhZpRQUnc7TC\n0ht/PhPug6fHnoBIwy0KYzL'+\
'l8Pgif6np74KNbscepCblGoBryh3hpaju+qbD7VofwJe03iVcfQY6\n4EFE7F'+\
'hTLa4OFFjfzd0+00BgJ7oZrFLy+sTWL9aNgM2nxZHKF8PKMjzIjh3WpUfs26'+\
'kZi+KmzgfF\nikktH9LDbkWrH61RlAwTnqNHhJW85O/NlMSkvbWcg7xHR6MR3'+\
'MGNtS9GhyjseI+Q7GOV/YUw8R/u\nzKQcbiokhtWFYrJpKbkLeWt96FG7cp0k'+\
'ihSr13K3h6TYLIZxF3wuyZHSGJ5UO7eif3QyIRl26SOa\nCOgPaxTiox0sB3C'+\
'+gIZtHR3Pn3wO3Ik5kCwpfaqDrhqQrM5CFNmrjQ0/WwfS193QwpjxrELNPkz'+\
'S\n9KI5o9xPcQ+mSyYav/bLFEMNQTSn3KdbWYmr27bREaa9Yhmrl0ACD3/NvF'+\
'7MuW5omGv/jfSds83s\nsofCvflWGFEb652+T/+dI6bFWwGi959znsWEvjK6l'+\
'7bE8LEm3uBN1/sgvLxTPoQBjbijoVQpbYJU\nNt+DeO6RZzCU3OGHxMxakGOw'+\
'J7Y4DhlSvPHtrgTnE9TLiRn8nm/xjv2IPmUuPQ3QW/ScPmXJ6EqI\noj/HMkr'+\
'2QBbUmn9dfoDDqz4Jdj+UxOO+S+HSocGZ0JAutbeuuGFgwcoMI1anMd7frs4'+\
's2SpBmWTX\nRdkf23pow8wdJTD7MFJRdy4/MmYVdFT2iUYtCaddJopSoc+/v2'+\
'NEjlpKJQoeTDi8VRrkbPTL+EWm\nRunvtZACLVGzJ959BTrjUO99O7G8RXDKP'+\
'Ar+ovZNCDsDZREJFbWmrsU8iGA9VrdMtu40Z3PhiPdF\nDwRjBBYJnorSFof9'+\
'qTqJaeHlAH5+OuwBdmn44a2Coar99P7qs9d+bpQoiV9hD8I3Y4X9l8GvurRv'+\
'\nxigZ2RKJUI3kP2Ovz26pQnH4USux79wnKYYYQhI76TA///ur3rcsoOBNiQb'+\
'EeJCD2usglujRz4uR\nHpadGk/tLO3sCtLfyc/+l+hhJwazZEV0Uu2kBDTg/r'+\
'OcItdSBtA3QnsOiq2EnvfYngQjup5bWt16\nAlRNNnjw3GpgCx5xmb9l1msSc'+\
'QyIwOSSXlpE3xI9hc0zZmfaO1brPzVkFWBf53XfDiNlaNSnzUj0\nvd356OuC'+\
'gwqVxxvmyMEyib0cjezkaJRgln4lLQeN7IiOFsBuxTw+gDMTVEVECzWFY5W/'+\
'utAdIFLw\ni+8IT1xjRXszFxETTrtxmONZD/2iS+9cURuU5pv8MhuaBdtyjKt'+\
'a2ALRHDrDXl/JyLBg+pqhx7F2\nhDMJHpWokEJGAl/HQdGvfExvYuAVsIsq8I'+\
'moCOZQ1qqD0cULGHn81elnFjc6DpZSWnOMHMZY8MO9\nYnj0V3C5tyMfv/FaF'+\
'4+O9g8kcw4iMeiAR8mfygSN5486DfafvJRtZIcXMD1l9qSeszfg3WZUFUi5\n'+\
'+DaKzX/ERCYSSGx31qJNIX07QO8vdxIs44oELgYDpFogeG7PPqewCCF4DJin'+\
'cPC9RTuu6S/D6wG2\nx1DMEkUWHmHVfB+inzya5vdPLytEJA4kHWtqUJUXlDH'+\
'a+DqvAfZ34GPSvX+gEZvObHCXTbfjXdtn\nmfpPe4D37s+156iZzilKZfHFnx'+\
'WGPQIZpM2lnKVHv7uSZnZ5VVgLstPp9TFIYD3Ov9RpSuHY8n+f\nPWD/1WQjX'+\
'b05feh7VdEcH/2/n66n2S8JvgWesj67ZrYY/bqdHeBylz8fq8N1dWRBvPGtv'+\
'rQP2JDS\ng9qmgeq5S43+2/gCVUdyybvTyMyi/VQ+CfAVXGtmfqHA0eudpsem'+\
'9EpUN77iL/imsY/lkwUlIOgX\ntb2z3ZoW96yQmNZ8KF7jabsGQ6xYsZH8fKR'+\
'dqgZjBOs+rXag5ewEtP5TRbiPRinxXBn0EWpgqFJd\ntbhkvi7Zo4NpKpLBgu'+\
'v/GRPTzGjnGo9Zxh3pxFZZHZtqWYs6/UvF4ZUMfyAP5rNJkRG7Wlr8+Kew\nC'+\
'goDXjvGKZ/TlbakTJRwk9Wl7Ees+AJpa6Yiv+70dL87SpWQ157SHvuuhyh5e'+\
'jRk13FeJd8E49Pr\nty5sc2Yyu8BK5ZpVfoT5/p4a4aVl3e51d5WNIvcDV2FA'+\
'a9XVItsGexvuGMnhQ8LNypE3t69SGjWO\n5nX/gWSB4gUhsD1Ta5a7GfjCVey'+\
'MUKeglqJo3ghOLhJ71tu2y4I6c9ZYvlEj8IAg38MCfS5TqKix\nhS6qJoF8IE'+\
'DTfqmAVLRj61imZpv2eaT8DcKHq8t6BC8jwD62FWdnoS+RvSaCkeKI6ybg0j'+\
'AIv39Z\ny8405Lz1QfPdXBIT600w95fYt653aEO/yuAAbSQUU6oimNaBGmlH3'+\
'fTbFFKQzHRf9v06bqMFfkTZ\nxhtvGgIc6hMI4RypDDtn++VG6h7lGSqmYIAG'+\
'Y14xECmcaRPkDTZcVXmBOtuBBi3wAa002m1IQRhR\n31/8aCI4YF0PbtGqDu+'+\
'NOzPBR6bvbvOzq8TQEMQ1Z50dNdIrv5etR9tq3AeCz62SOwe6zB9x/ntx\nlJ'+\
'RpVGl++Uq2tehzrV9abjkjLsNkm9cseOZiG0pgz4j3OYLWV70RXKx9t8vMJ1'+\
'CI92RQ32JR+W7Y\nop6kvx0AVEi1Hc4kznz5JpJD/oVRRHVtisiEDiQ5Iyp5l'+\
'Ga/wECVtj6+lYkDl4ia8CsAtMWXtX5d\nsKMrnXju5iDCl4x6ea2eeF79WsoI'+\
'hJ+wxeSonzX+IyJ5GSTryMTgFp0PtXIdrced7FlXHHg8avCS\nSkNUpkWFRZP'+\
'IOwp3TEh07BWgR66nttpzat+IRDaye8uFnYwfPafvsvmTASInxDr5mXi1TG2'+\
'GW8VZ\nL++U3xTAkutHZIE/3TV0JfVOeBttxUwIP6TJFHHPmO09EOa8UdeRCl'+\
'DrXkXmaTYq20NS3OmVwkof\nPvtUFOh0JKkkHUuWi7lCFCQndAWi9FN0YZyDQ'+\
'yjDYKgEBbKld1uTtHYh7laaHnDPi1kEBdYGGNTj\nnpWQ25hv5gm5s169YO0i'+\
'71iLWAv4IGW+6ZnJF4sL/WITkut3rdAnB8l5Q9hU5AdnLmhww32+AipJ\nnNW'+\
'A5tQ3Ix4Rrf2JFdJMsavA5xqUxBXHI9FwV1VFw+B8L9CSpUuzbZ/oAME9tzM'+\
'6ojuQOfLzugT0\nCtZIhHjHJhqUqr7ouWxl51pi8v48X6HjPyF+kTzulQ+Kiy'+\
'm9Obkc+nOC1VdRn4HWy3MdNsbrOK8b\nXAS/dH3h21EFI8v+shYv8aa5YUahj'+\
'eJGSHSEizU/UeyIUJq1HoEe2mo7TU/kaAAIYpPpE91F2Sf/\n2/BoWiUncJrt'+\
'dSKHFiBmRZURf2cxuS7Y4ONykHCRngHo2cd5A5BNPsa+vucNUIjW1N2pQkL7'+\
'kj5V\n3MrdQk6bKi4QmXnIxtE2tv/RS9o7pcxM2ht65j3oJHyRO4j5RXsWBWl'+\
'SUp0CJ724L3Zi6rO7fasE\nyaKDD/lAMP/TLXKP5QzRF/s7Fs9u8XRrMbLAWa'+\
'DtoJecfAtDLWnf54wx5eXP57DFABi99EQs+mpl\npuLlepduJQpEmn171DNv3'+\
'OhEuOkbTK+x5eGMOdejrkm9/JmRGuu12m43Cqcx/NtXtUD4JJnj7g6d\nQcy4'+\
'W+fAU4y4MQstyT1gO+gmaOQFv2kNKDLPKc9U9dtH9G/anUDWsSHVhwm6Dq21'+\
'rOMQYmiBrV+2\nGp9nPj1DF1Gg5ip+qaabZnUZa+7bHNGpkBtzoCMC9mr+bTb'+\
'kFESFVrukuUT+jYm1r4zt4XQDi2Pp\n2RRxYOMdwEie1e0YV0AU/8+RvdfvtM'+\
'f27w5GZUNR/Nb/culpSIAxq8t3aBq9s5iATp6lWDpF9p3i\nQi6UnzW2zjQ7u'+\
'A8+2C3bx+VbbWZ5ECFUsvmBxLD2l87i7cUxgWd8EKW+xVJJY7qU/HOtc7DAK'+\
'uas\nhx04LhdxZq/PuhBS4dh/5iK2NSYXDAef5zMeTKDfQp5YTunR0piGbYy1'+\
'mEokH0BG9UzYaEIKkwm/\n75w80DSGr5p+9SKTbno2aeJnohdFuS1zfMyzNxB'+\
'/QqN0qj0X9C46dskAZjnSS2SNW7kuWFaXqOJe\nyIkEGYreBhcFvwb4t3BJzE'+\
'dvxugi7RBMNzAn18ox86hn0BfpqPsbTpVfgsw+dCuRcaquUiXz0k7T\n55n2Z'+\
'qqedcbSO25TrFQkDT5qBw6iQPRNarYLq9fhlkaZlofS2F0SA+s2GIvMGuNWA'+\
'bSQQTpjjSwS\na29zZ/i+6JeKM6I1NZqmBzKeLPmLJ0RMsjUqINpiP8wBG+/u'+\
'iPgQPCwVYyMvZXr2KFrzJ7b2qXIK\nGOzZFjXaye2thbgKtj3xCVh0e1Luial'+\
'FCphpi9t4a98lonUYMHCMW+hh9FXfyGCgICX2tGcjOS89\nl6o5h9FobqDcKG'+\
'30On3pHuIHQjBTx0+C/7WcdqNP77pM3Gce70OciLesBeM+RgZ/pS7v1amf7E'+\
'n+\ntALX7ox+zx+0zkwQEsi7q0ZPDj1t+ftA7AaH83mJqfPW8j1flNL1fjY+R'+\
'cAvyrGx58kFbfFliC9N\niEPrBmHEbcOaxMwYGS4eo1daL99GVQJDeYthRDo4'+\
'DChQTp7ChKrja9UPGw25kymrCLqYNpTLpYpN\naj0WxZ+SpQgCJ+SjdRNjrtd'+\
'8L1uFrY+UcqA1Hl2hfjqxIKCLz0h5EKAhYmk5gw+z8WnupKKAU7l7\nLlXQQl'+\
'9eDAn5WU761f7mpARzYcR2WjQXvQF8qpfxiNfFlkUf610Ub0/3adQny3szzF'+\
'rurV+sfsSa\nRre6T4js28730dK7P6tuaWvLa7n7OFnb2AKAd8OReAs3waKov'+\
'Bh3zDykyJYWGsUeZUwU3c/gLdqQ\nWAlK8pJjfKaTz81MBHFpcYugGPQgwOxW'+\
'leecmCZwsb4RMdQeA29ci3j9Ct+HjhyxuQ3wjOHGGFp0\nnrDpsXlgM0BqabR'+\
'bwfRg9+uyWG5x/2hg+/Qtyxhoz8XmAilfExhfi74V27zfMjBcFfj4b3kvAc/'+\
'Z\n67YxGjRw7KfTVhJitkz1pVJYRBsgt69F2U+VMQE4jfG5VaOkGOUtJ4pJ+e'+\
'E7fA88IDBmtLxscR93\n5+U9dHVagbPM/D0+dljSDj3cshpzP58JBAOkzow6I'+\
'bI7Ony/iJX/Cgk+q/LbzYBaTEsKBxDCpstK\n6DHXkmX+688FbibGe+29qFUT'+\
'VXTGnw40Zp3nvOeXLI+7OeV987XON1nXTsLRhRZpe7xCY1EVyXQW\nPjKEqCl'+\
'R8DMjx8PE8WhDIlnjOenroFzc/TCZjMWX0dpkxQmPYTvQ2hvqzeky9Xv8A42'+\
'rhqe9WNE1\nrRe3H9oUvc8z5bc6iHCmfQd+RVcFBCQQM9Ul1bGuG+4ahyBHwZ'+\
'G7AyWBvrGHnkIv03eSiBncssxK\nxxsVAivhm7bjseZpV8DGpC0Ph+vy518S/'+\
'YpVd5oGNArY9Ty0lhAvWb4FmCV25rsluslZUnRrcIPB\nnatdhkpf+noPHbtd'+\
'cC+TvyPS0LbVWLGai8v4MVU1WJ+ybMlfE+g/d2NqbZtb9R58CvJRofSDSh6/'+\
'\nam6pdwK1JlJjM98WkfFu3tuDIS/6/iw1vcD7i//ZuXlc2/C3AFKpP9jUWxH'+\
'GhFdSBr0rPbF4TfJi\nUC3fVecAgoQpmHpINerrbiBY4BDrsKjq2iW7Sv5jBU'+\
'szgxxXEKryS1eB7gHqJfW129NDYc9JD0ES\nVVb6eRn8juZHwI37Dktl/X68W'+\
'W0tzUB1c8Wco27fTfw1sqwWHyngB2bJ7KMkDY/7ir+zqzveJPX2\nZa6w8YEt'+\
'pZDgt+CQU4Q7y57BLSGnQBfboQ7NkqB6yebCz83gmbMFhIXmbFKpBukUrPGR'+\
'uA/7h3Nx\nAyEKeoCplSs05XZ9WMVe8gghQqtYXMZVk/ma1CiTgxA6QFPiCHn'+\
'mn64xT9El1PCF4/xcMULZMRbM\nn1YjMO3y8oEjohuWV+nyEl3o95TUFEG9QB'+\
'q0zhk0IlmKKwZFffnBtsvNzIDct1bhdRv3As4/zmmh\nBc9WT1jt/9u/jdb+C'+\
'QtRPuJM9vQA2Lm5eJIBF7hZd8EemEBbFzcnCyGPb3Y2ZKByFCwXCM37ItZ5\n'+\
'Ub2IfmNqXZtlfOBT4PFoEm7mEdzL/UcgHQGUtcZ23FsivCBMFoR2O73TONgZ'+\
'0n4PpnRB+OEyy78H\nn/vwHv9ZuKRiiIDys3tw0QHDdloqTVUvF2aeBLh8n93'+\
'VmTcAfn3lwoCXyj4VVWdIdW1bkQzFOIQc\neaAcvGzIOhYWEOgZ6jecSxS9HZ'+\
'QQPFqyR5OXYZidxtvUP4F2aUH7n0PV37xij2uRvuPN/mj91sLd\nfiSdr5WU/'+\
'AX6DFowIJLeDBUowFhUdwcJdHrdh7hoFyfoJLhMDAUkKaCGaQcKpcOYdwtiX'+\
'WgGeUIw\nze2hQEoxCeLMV8EpK+Hg9im+AuTLBVJ6jQX5gZ3kiRY1WbavXYPy'+\
'qcI89r0USoxAUQmt9EDeDoEh\nhnGc9NJXUrAygZCU3wb2e+D4+Lq/pG5rOkD'+\
'0XmpRD3pXvJRyrVmtfTlC68094JHsV7+RvXAkA7LI\nEEbV4tnUXIMtC6hFFU'+\
'kjQUDDMLCft/vjO5RLvyR7OkNm3xA/WqQcwRqFh2g/UJIpF9SvtJIDTuAm\nt'+\
'Gcnlh4dq+Lp5GCMZ06JTo+gbVZBpsQyi1rBW55MoXHDtGwgXmqMt5M8KKxZx'+\
'QhIzgULCRTrPb5z\noaah/FfbUL5PyizuSzsq1XtNzNfkFH4g5fsNO2ih+eht'+\
'gBLAWUUIm9N8wWzDE/Pp5nvNmC4FBYjQ\nflEc3U/w8ecXZpqaDEkBTYJ7DM2'+\
'SvnhGLVkNld0ez4rRBEQZxqQRIMDWx3OOpP7Dc2pv76J0Uo4n\nUaGrMISbGe'+\
'LaeBdCS50UmmjiE9dSrWQSlm0EPBO50/J+tOARLKnz9v3xEuLShGPBMxG/iH'+\
'8yyQAl\nhb/3bKv7pkS/3RlEd7ByJ3A5Vvdkvw6nufhEhIlZP9uSIEH+WNqPd'+\
'fxj/hHX2F4sBvl6+ps/sDJM\nnzgfuFC6hfBddeX7NypicvJuH8HfzY3tP6jK'+\
'Y9kCYI2uq1G9lt/ODxDdxdWToG4Rl++99BV7wH8v\n5vvYDCzVqKMgKsg/5Wt'+\
'7VEZ0DRwd/e8EvsEJ8A0MX/KwWJid93xsibmGIZeWnSrjLgyeGI6eHt7y\ntm'+\
'SKog8F1l8rgZgx/Skn4kNTNQpOoUvyMxViFvY90yx0RaS80iSXmjDsygXKzA'+\
'tbIoAF9fyb+3fx\nmXQx1DQromBJOXI3xLqclAFHLHeHvPKvqZowkwDZyQx/9'+\
'QMiI0ahovnga8KRWKH0JxqoqJj6Q2Oc\nqkXcmoiQgPFWNERoiZA0217eJoJX'+\
'PGCxGA9ZlFsibfXVViZ6e8bsZxEJmnnDLySY40dUvX37PlX7\nj6r+lpfcm6o'+\
'belqTUXsX6PnxgHXOsbpFnaBbXUYP78Sn2tMi7miaseb4J3LGSzKl/Mx5I/8'+\
'M+RW+\nTa3daT1uY2bM9MZHUCoNklx/d2YDIx9VDp/xv1Oj/jiCvWiH960TrR'+\
'6zxeRGIBU2klxlcwFp+Kl0\nSpDcP5LpxrnGpGe4SLy7wHuA9KbHghQc4q7o2'+\
'uLjfMhKTI9Qo5i/Uvyt3r+YyGz9sXx5OaZTpGBM\n49nSWrGbaJlbs5fU0IrY'+\
'8ga+XNFF3mrHMywSVx75zbYDETIQ6VzGQpVBJ6NhLtCIqWb328FewnMc\nzqJ'+\
'FBojPbyZ/5gkXOnU2fA1bvW74lOqhOyU10EV5LKxfQpBg2ERNyFt+HTuuOeN'+\
'ZtTOvtmFDvwN8\nCUb8NfAwEHj1ohwTr06E2Ru9kDp90itxJhkWoXzWBXjz/7'+\
'h676gmnyd8NL2HJJBAIJTQe0d6CR0U\nJPReDdVQhARQEELThKIREbGgCBbER'+\
'i+KdCkqClYQFFT8iFKMDRCQXL/33j9+987Zc95nZp6Zs3vO\nvHtm958NWAS4'+\
'xuocnSc8cqgov3atRqAisRuhPvpG26WV3t3sJFg/+GEG8RBAK/flN5l8bSFA'+\
'im35\nZt95IjolnIHsLx9u4H8c7oZLNgaIlsacfbsToI/u4O3Gl2HaQWVEDFE'+\
'9p3038coEJnmmtsuaVHQg\nCnioST3BT/rvZ6INp92JfKHXSTrXtu1mzdm9Fp'+\
'VTDSZeBA6wjvPEKcAwL6HtZqMk6aiYYl5zK4kk\n/o7wq7jsaKgDwJzy+yLzS'+\
'k1MidbZSaRqCUGay9tGPM8X9IH1aK2DloZgNsjW9cJWcT7CPo6DLgO8\ngIFS'+\
'OySpHkPt4piTcY4p02GeH9IhSS/ymZO8Ts7y8eUQjcfiFliVV8cmreL0hhG2'+\
'L7k+Bu1fixzx\nxbfeNCAnQ0RH1/EyQ8CHQsbD3x9+Y11ebu5tu8l79Usm6JX'+\
'WSExNTM3fvIBhEZIFmJwA+hTIhVTD\nGe4MJfvypkPoeak0Xds7HJ70arD0hy'+\
'byCye/1wX9kIkZ5lr9F6oW7hgxUocsruKCXIkvLVsoECNS\n651QzBbEMLQ6b'+\
'MOUB5VdDv8jBoW6N/18sIZ4YXiT6Xwu5upxudYxpp6m2nQpqL3Z977x5RMqJ'+\
'2ph\n7dFPptTg/nGn+cdn8EFJfuWkSf+HsCOfDViOIwolCGbYyRubjTcITqai'+\
'RpJ9CmoVuWUYGBgixbO2\nL7Y7b6UrdrKutVA6taiSWzrYkOC4ULSsDPybyMS'+\
'G2bpk4sFAsxHRiaINnTTNb87YMxrWeBtRXIe/\nyF0LejDIutK3Th+oCTbcYz'+\
'6RaK+b+nrl8mH2EJaQzE24sLyGgVxTVG4VP7GBfk03olq2OwDUBFA3\nUOk81'+\
'cjhXvtztac6B7za8LVN0Y9uCIhQcnJR7VuS7wI82wpTzAtvD213cfIlniAoh'+\
'bovgGXtVNpR\nkhiJvaX1LsPgI+jc5ugXuVYak6KCcDP2fNvi6UaCgh5A045a'+\
'zzC2/Dp8cT3FaDjgkH+P+3yJpRLp\n1+eNqMCAQyfs5NoCrqRYLq0t2oJd2ta'+\
'OceZQDueMmnnsqWWS9N5DYd5GfmoiwDJzsGvCI+PXUbq1\nJwoWnmW03zo8QZ'+\
'rdM+XcVlT0i2jrrc4W7ts4RXnS39cZJry+6S3oK+ck3MJAVT6eW6RQ5YglTj'+\
'Rj\nqSTcgswuh/494RIW2kv1nX6pqW/Uu4Md7tG1iWc6lfgx0FBt+/Hpr4AjR'+\
'2qE41mlJNt70abrAVXt\n73elk0VnEcvK17Q7b52L17RdBmkLkdj0ftkG3oG0'+\
'nJ/0Np1WJyU5fy1mTTuozdYlwPnA+1cTjvFJ\n5gJ10bzDQF27pd782+nQglX'+\
'EEm8vmWHKvSu5m/qwqx0dp2uEDxCaUFIxXKlTeUFZen4afk81HRcP\nJJ0ykG'+\
'ytvX4ApORWqeXl5G3fYH13Qk+NYwUBIhWSVIwdALTuRo2BoeBsz7yI4GmEfP'+\
'i3ZuqUmhsw\nfBSWO97k8Ym/gJsAdkEsdpuKb3WgN7NJKaMFh0dhOQvl+802U'+\
'jgeh3wnGKdMX3YKRoUV3F7YzTCv\nanYikSauUbloA5Id4NXficoK8ivK/GxP'+\
'WHwX1zacJZbjwkpShsR9l7rrCg6V1zd+8sq3c0ATDCEq\nzN8HFgCHhXm+TMq'+\
'vpus8n6IXA4/rJvZtlSKWKRMWLl0DxfnKHxj+aduPjx+jwbxaDsybzRy+zKu'+\
'6\ny/PiHR4SZxrJXpKRN00eSNt8YwlZBdrqOmonTjmiR3GWvDRNQx3ISGfkEM'+\
'/MFrPMkpe9wwqEMdJe\nc74JzEy3j/Hy2pz2RiKJR/AFPw8q6gUe/1xOAtsBJ'+\
'uq1AoQajmd6fCfD0yyX0iHdpWXnrTZS4jYL\nIMxuojQLxdmDBXZaYN0CRAct'+\
'H6aOXAnfg7KXMgTL+NZE+f5uR4eVip/3odNkOZn91knCitJ5CbaD\nB0vcbyL'+\
'iUoSX6mpVBUAWnDWt6ZIBkGog2sZx6q+k4W33sxSSGXLX4wJ740zLnEFUh30'+\
'YC9Zl4ZOY\nHaUo9H1lrTp7EV4WxGfoBioZknIpmmJ+eIETDJ17Llb4jOV0WH'+\
'/s7NUv1POM8CDfYB9eHL1jtoyZ\njN09EYcTySBpP5MI+u6nxNtxlvPOAHOdH'+\
'IVlu+e5IvZLrVQ37FhmwkJzVKBNnV4dqFTh81/hcSPE\n0nXHALqHl483wM3V'+\
'zsvWK/A7/oDk/lZ0me9shFdYQqYf5lpUs+XT6eQ99HlNrtm8K6319IaEdH+6'+\
'\nDEdAzZUI/+32ymGfQByW47QlkzDYIlos/j1efGWmLIKzqSVd5gfU/TUTLGz'+\
'SmCjzAhbvFhZ+hHL+\n6H9xTLy3WgwoTMqSsrSAp+mmD3qsAtm6D9JPloV+ro'+\
'6SgDwLDj9CK1YE+hW5nrBpKJo1vHTpBvtA\nxEJRtsW5oEBWZYy8X5g4D79pH'+\
'RZ3vGYLwjMq2IylBITpFmxq5CJp00sH2k/WPEWreTiYin4H3rXf\nSG+1rc13'+\
'36dogev8DVzU80wQffB3rZKubnAdxH5adqrUACpw286NG6yPAO6P7at3AZon'+\
'1ij2Ue5J\nvs34+aa2RznrGWL/nSQBvl/tdWBsHKIPVJtUx0F4FJ9K0Hl3G1h'+\
'/FRS0nnh2KFl5kBXo6gwBszU7\nwSDtc2ff5mQe7Y8nJos8lzi3Hj5MA9Xfxg'+\
'YsjZQrFeeCVYHpurNhghGgTnRm9MMu9JXhKcVnfHMz\nk9LbbUUWuIGQw1dA3'+\
'00Mlgr945PcD9+kP3iylspOykAnQmrQL8fTkGnpRwH7M17v3PoZzTQ0ALDT\n'+\
'kLBYRjz08Xh9SLh3qBmSgvXr641TO9h/M+Wk+a+NrwVYbJ5I1zA0AFQgaXuk'+\
'pafMMxsKZQVcKqkd\nP29lR/Ueo4e6vngrvWL/suyLm6LDNUNEiDSF5p9vbAo'+\
'pPgxEK1gU7w2bKqSHe7stTSJeBoN+D6r+\nnJdXmVtABWi43FsIjjthOXdCIT'+\
'wOxY1100kmHPz1LfDr3oh7kmyGAQjzFFBdmau8e0wNeHXx0sQ5\n2BRostB5g'+\
'Xzk9wOQxqJSC1rWxatlZ3vhq25Exn2IY5f5PcTPG/uuvE6I8aaLWUFDK6aNI'+\
'biDXCx+\nErC91/si60U6S2EwOfAjKU0J/45VKnupt9nbNNrs9WESJRP+65xa'+\
'Z4mLpRLOGdooSCJmr+rvBL+m\n2rXuoYdu6k+1z+QufdTLVNYzZWaWU20AKKg'+\
'aFwTnht5+uerCyQKA1dQLgRmBR6vY31JGY0ndwKz8\n4RmGuqzeFyaSYajYQZ'+\
'X6tRMHeETVm0FGDKhvPBQjYx4NTgCwxaHSaUZiC+saLAGj6DHiuBMu4mCO\nE'+\
'q6QD3SgDT+ImP6Gsag2TB1Pe3R+g0NySyMV28k17YuFFqkQU5fGeD8Vc4YSo'+\
'D+ySoIvnd6tldye\n+gwc+SDgRig87aFXE99vWd1NJ75s5julSScCf/+rfFEw'+\
'8RtksGw2Zqu6FlC3gxO2zn9TOom3O1FS\nLSeysCbTU7AEyqSqVrPOTERnuMb'+\
'uOTjfpa6YOh0wEkxAHaepoNuza2qcbo7fgczJf7pz/lQceKhz\npt3+s+835D'+\
'IuX7cuNm/UphXXYQ/jsVnh/DzGWuZWNrEdmHhfLN7QTb7SYPYDXtG0oQud+L'+\
'WxKcG8\n4VSIZC/F3WvK2lqzTbRgpz+LdT23oCc3NK/qHS5rmiM9XLhLFBApX'+\
'mKVzwsNVLrmsC0PZwmXXvGt\n8lUSFoLDWYpWtX8d0OnpTxk7tzDCslcV+s+h'+\
'eicbsRaFlFhtufLcv69LyI/cpGV5FUVtkrZX85g4\nsugvxh2KQ0vkejjhtdl'+\
'eJ2BM2QETVFRuS4k8J1tcqMs+tovqq1oyN3L09XUpzVf+Vib+PMbNOx/8\nQ3'+\
'vk/D9hKw6+OqzoIN24Zu+9x7MOl/6Nkfu1PuT6FaX8+RcWdHjvVjAzAoLbwE'+\
'545Wu7mniQ7C1T\noUPB59G2jPljbPVgb//9wQEaHS5NQHHDTwmBS5sgXv7x3'+\
'ih2rI7nPJeTz05Vyg9DcVnMg4+tuFMR\n6TPM7WKLFIeebUZyhqb59WG4NyXX'+\
'IBxzwbE1U8GcaGibX0OYy20wrpsPYhPeV30NA0KfFahxinP1\nQEc+hId7+zj'+\
'Y31cVNszGG5oa7w0UpSaQCS02a+mxCDXXIEdKIN1Rie7j5eA6KHV42skJ72/'+\
'vYi7C\n0QwC/L07/qQBLpKWCp8GzwN0CZQ94mCqNkp+uUFZL+1jHJ9meYlGdh'+\
'kOoNkCU+Y/NTy40RdydaIa\ngDlRerLVArjqYSOJO8KkmqFjtvAVpzfDd/lLK'+\
'wHgcgOgFpBD8h7EWfu6CLtFS9uh9J6Q3qGu/wpR\nqC0OP/YcD9bxG8MX5Ths'+\
'ZwGqcCwF3nMV6StizsuwEWdOBE+dQ1fgvVHr9CzgRB5nv3P1mb+Q5KQv\nerJ'+\
'+3mqERvTlKXNJk+XkmUtF0kr7NJ2lU+XhYy5U19+IUVslBXhqu+Zx5Z99mMq'+\
'LcwSQyjnOddF2\ng/8AKnO4oVIOw/6lwYPaovOWnIVfBfgZiYIyJ1M62ChIaf'+\
'mnJOA/RohfAlgElVk7H+WGN/jB6n8k\njoij7sp+qpMH4CxBfsFA3yB6a4htB'+\
'T0OchD1op5DyNZWHImay4NA8CJ6eRT+ofpNRZ4TfcSJWSfI\nVyDpzX1uiDs5'+\
'+zzvMCKltDgnW6/Ealfet1DCbYffW0HBqAlwFeE2feDN2x+/OTRdzaqSqH+V'+\
'6cgw\nNRem0zFvptp55mGmzm/FjHwZjHsPnET1AsSatC4yLp9RK1KiBmZHln8'+\
'6ycRJ4wP+tdGO45XRZEni\neUB7MlIHx68gMvYfHlvUWP0jhoEzDsLwd6SpQa'+\
'fAzUYlSmrhqvCb096FGVoSegH7+s+fMzL69V3C\nrhk86cHP0PeGSme2k1fgc'+\
'hPQDa41kCiPp7eAuJOK3m7XXVzSohXJxD6gloa8NwBsAarnGKdGybDy\noAqM'+\
'ZLn4Qw/kJrN0NYPkLSPtWhvRwdYoubnaaECT4m2t4lkVOWocBH0D3Al3S9Ct'+\
'PJCfH/HNHH6H\nlqBDF1VPuSIVxTqu6NnVTRyK5jk2mof8ztuh1JEC2Ubrjs/'+\
'YEhpR2n5dimQ3a59HB7qL6utvhwGD\nLxLqyQ/gTTZvBPliagG7KROPZb1sjW'+\
'Ba5vMju/HYh980i7qfnM+TD04l9sCyyvcY9nVBfOVRPiUb\nWUO/Y59y1xrSv'+\
'3Sn1wAmvD3vVqiFIaYe0RALCUb+s6/rAp7Vpwzy7opfQwxjb+5ROLAmNjH2y'+\
'4il\nRosa/bwa1H0Dx9u7/mHEq1VxIBgue6Q1yUnQlcvS5W10ISzPvnv+OJCu'+\
'172EgbVn/RfrFbRhclSK\nchsYpW4eE2oKFcv78g3Mgsd+XqpcfXNSjfnr5GT'+\
'iQDTn4BrqA8M55KZZ4YnPDO1Rce8JjELv+mGX\nv4n7qdlq2cXk/R3flr6xlH'+\
'TmXR+UDq4fwbumRZMpP9WUbGnlZA8FItOcnX3Y1GFMgfvLojLsZhcC\n6j9oF'+\
'OMDG6VFlBWRllHJJtlPVnTzjXkC6B9z2eZrOgr85JIwRiT9R9/eJ+nG/Azuy'+\
'8vBr0DCdBYJ\nTCtkTHqc8BRgxrjzhOOHiS22A9KdI0sF+fYTWSf1PrsEkA6E'+\
'7h0e8KSrc0d9gS0bRXtcnfc6Ojx+\nlw88R0bpOkWmxDvKTGld+2+vb2u+Xuo'+\
'4+zuh8XqlZzY5wx1hjjjORh05aZhJvPfikHkLDx5+Ugkj\nBdaXJ2Vz/K7VrQ'+\
'OP0DyONF4y5GKvz/PobcpxoYLiEfWKc1+cy0808mi870s0Wae8PbymcYXT1U'+\
'Uc\nhW7pHHqjV4icE++rQqcWBw2gxdIODCim8RXOOgTJ5PcDorRPacvZatVZH'+\
'uHm/Fj28AQWPymEvyld\nrAAAjTf5h1Z/Ejk2R8NelMVxxPBV2fhoUm/huedp'+\
'kPGE34gJtDY+e3EVAxBXmwW9WQzRWMQkHiZv\n6tLkgVUdYiXuZB4G1AENO3u'+\
'vhZMLrDkPBWkDfzW/ZVeqj4C1loqsDGoxz76VdAV3TDJeGWfexeOT\n7OKerx'+\
'kBseGgihFIqG9e5nvAt11/7ndil8Hpsx2XvRNSZLxsrps9K9Fams/SHuoLo3'+\
'PQpnEpNJYZ\n0yxhKcIw5loSLY2Yml6oqDWS7VGqDJ+dPvkUZBhhw5FwevqKv'+\
'6/lemFpij8mbBe5PPFk5nTTBRaM\ntjchRIy9HIGYqRf9kpuIwDdNfF/SXh3U'+\
'CEqnItPvMMVpOWRVnaFoNE/VRTGk5hFXZ8gg01vrfbEp\nOls06QI1iT7arpf'+\
'LrvVsBbhB7q/+1NxfxjlBBSPgUyD+afC5yx4t02dnzOHl81zc+XK1hbWFwEy'+\
'x\n89STAnQFjXZ3fK2iXvHUaTK40LDjqLbz6Qpwlel+CuIPFHxmr5ZmbC90Gr'+\
'z/eAD8HKj5+X0fMfhl\n8M2oqamM9vV9twf+2m1Z0CFpEvD50DENLghyqyzAz'+\
'qHVV+xb13zHnOqLEhTPXW83BJf/cLQbkUPY\nu96PBFDm4UG4opKyI4B7tQZd'+\
'1EKJkjjMG+X3QMrapXyN85sQtsO7mU4soqtMqUS3jM4NRbQH+L3c\nrjtH2Lj'+\
'bwAg/GnFz1+mH+OzGXYXDNbcU4o5outa2tyvPvSifuCezm10He0Y74eknJKo'+\
'CqVvsioWS\nSts1PNo+MdRhdKQy1U+FFP7vzMulN5XRkPQ8oI72i+A+HJbq75'+\
't1I4QhnRRRbCvjh9c9dS9vAD6e\nJMPtP2V2igYsrEyKUYt7roV5vqZA6z/+t'+\
'KcqmF/cVJSNEuHLPkF44utR3ADrqqNWvwESZF+81kGn\nwEK7kjdKijp/qTbx'+\
'U0v1QseCnRCWeppfxDkSyupFoLwM8MlsgZLIqWP8d+k/bTcElik/h0tQ/04P'+\
'\nfHdoA1Is85EaZ3omthLIthZXZKli5wJeo2AaLi4by+vMZtXYKMUTOqx2Qv9'+\
'6lX5ZEZK/BXr1NMdq\nb+lll83zU6/ZYNKwRDCt/KJ87OlQrRXcO+UeHqNZcG'+\
'XIwxdrvhBvYK+CqnAfi/ZRuRozD0wdrfG6\nxccnvtSafuEfYF5jejV51ua2L'+\
'Xx5ZsG+PVRnShFf9uL4C9fF23GLhBfpjhwedSFdYgt0ZVEUF4jx\nJ1l8F1H7'+\
'vaPKUhqI2qZo+uQcT1EuK6S1OSL8iPE5U3seS8UoRoQEA2s3lGs3OGZvcrgU'+\
's4Fc6ytH\nTzS0Sp8pZEmNIvcZp/S2cuThr1SlOl5ynpRllwo6OpW7AOplYjF'+\
'L5yiyDrcBKSMnkWMV0soaDQbI\nMT+PEU1vY2UxzRsxl5EUMhU/HDxSjTvTGB'+\
'ukzbKarpB+xrTWfpRjN1rhdqsWe3PonsVw4FLl61zF\nQzWA80edhMAv/JXsL'+\
'B2dvKHBDMm3DvLos1q73pT42MgEgMwWmO1SpLiCx56XtUfAoMALtV5nikdK\n'+\
'74QvXa04Fid9EBTK4QY+mdKPsiTsmtDhyaZaRN7+rMpbV3sOONcF3cv7cV14'+\
'Xqs2sVzx3Kr+aUAv\n/Gmo542LfYjDZU7swQ6HZIVwVorv5c8Xtw9ueQ1Cz7B'+\
'lhdEsPsSRVTKNzDqYwjpCZ+Xl5GpcUtWK\nTwU4eD5piJiS9/56uQFl2aR72i'+\
'CgKoXH18Rdev5231hSgG6l8iYBKD1wSOnU1Mop40+JA3qqyY4Q\nDZahnrV/n'+\
'W6p1fGOd8rnRMm6GXcIY2B4g3ZkyLpyJzbo55X9D9bcyXOBOctWWfGMJDFQ6'+\
'qjl+Tp9\nZQmXh8C8Z5fiOREPQbsecvQXtCIvsEbnf8mHnr6Aw+Xx1c9YVUBS'+\
'RyN/Wl+0p3obgPKrTf1ElKvK\nDx4EMo/Aa19WhyFUdR8bNFcolOx/ZEobcp8'+\
'asjWiGkxyep6PnWonB4yPwV7UxkF+DfkMKtVmKjVp\nhk61jisSHjSOslSgPD'+\
'UdfMvSyh0rUU/Lqe1G9teSB2BsvZzwhf/VYi3C1akDv+5Fs7Q/euabOU4F\np'+\
'hkbuL3JP2g8lZ3Q8h8wcPvBd67LlF6d8nvXstSHJ+espopYUw9NR4LsjSUHg'+\
'2hySiYSZdU49qhw\nF7TwtPczxa7bZWfa6GOBwQS+2+c2ydOyY8jLXqtnNc7s'+\
'5IhX6dX4HlVVYNnoLMlDDAJyxUvdOHdP\nuAdyZtrL35aebyr/SC0vufy60oI'+\
'SVvdV4cw7PxlXpfjUMj0Y222sMCQ7e1vBebTiUniti/jTR7xd\now9pRNinTX'+\
'q3HUoYmWZVswn2VlBOU9iPEnE8jmAkRydE04bSX4lTFT33cOPu1ZxVk6X8/V'+\
'lfg/80\naB3sTDx/tn/9BGTypA/kNfB8n/LblmDnaj1wbQfadFwzq0VCDFx7u'+\
'WRNOTiCYq942YSukWDfcVzQ\n5oPz9Oj+8+zBdUVofJ51vDoqCjB4vWTSC3Ow'+\
'GwSPPVgZu5CyyFqGEW/PZ5ptRezBTfaSlLNxBa26\n4JZiKhL+9u1PdNi0c/X'+\
'ohboLJsHPrFLQNAkx6KvuZnBtqAPl/3k1MNQkpRjl4vkIjfCh4w68dkwp\njs'+\
'PZJV9bDOzu4w2h+HmmzTXzOBVeP8vPPbVAY9pMmzFLbaclOlTDaah3rziidn'+\
'XI6w+x6vMGJxTk\nHfuZCbQmlTmI2jt9lF4FXQeOflTFJCGcLUsvsGfkLw6tQ'+\
'VngWur0Oe0v6KP/lszMmw2rRVAufbEn\nYabPIcAm1KLDCLsL1naQmX2jHK4E'+\
'3eNKIF4kO550qTLmBkNiZEjpca3K01tDMNCoWlxiOZSnQLHE\neTI/Wz25s2e'+\
'03HTB3+C8jqJB/9TccDK2Ms+sXa/WJXUNYX0hlW9o0Jf/H2Yl7xE2mtCQWfB'+\
'nu/vN\nf1pqAenEGJ0pfsK3e9p6CvfeoEeXztNpDCllbHJiozOH67lZQ/TOPV'+\
'K7MenJ7SJM0rUc4MBZl0nl\nCPsD7RMuZgMdctx34/3gpc9veuyBePa3We6DJ'+\
'LQtKMH59eFuRfy8dXQuFvHl4ocIZ7X9rAQxlpqb\nC4TZyHv91+u97FC+W+de'+\
'kBNIw+HnUz7nwhuSbapge7PyvwVxEeRL/TCt/5xAPwVP1mermuSPBC5c\nfML'+\
'qKMNoWHhiZItjfPtz8AQSR8qUvt+PpJXGlcBqLNbcNebVLNAbi24iFQtwY2I'+\
'BSOAFy3/jxDe0\nvDbMyakt8uIJp+FqIzLOrvJTgVO10b8dzIkD8WUOS+1DXZ'+\
'kvu7AGk6s5IZ7/FZQdAxTeyCzUmC32\ng8wc8mWG7qPh3u6psV8BAIsaFDk99'+\
'bJBF62h1Q6N46bKx6/lsN50+t7peUO8B8TT9zlzIZt3qNwi\nVcwWpNJu3lri'+\
'3TqNpbEm4OA4aQIRdP2Na2XTSZHhsB7wRgnBuVYkPyncD5olvr+jTJwE04ZF'+\
'TYCv\n79P8pWMkdvHuwY+ftSGTQarm1hjWSPrTuv3udVr32SuitHIth6P8JWh'+\
'PS8cDMa+/ot4Boky9qeDv\nHkqFG31KeXn5VOijHTVpotaFQ6GQB9cWEYZrLT'+\
'S0XZwSvde+/T+D5iH9i79OXY4YfUd9e0UN7GYJ\nB7dU3GI64MQs5LtQFmDLc'+\
'Xo6I8PheESc21BR6Js1szPHMEeeGj+zibtsye/M+AKHvHeBsoNr435I\nUynX'+\
'Ae26gYYgxesaFz49AN+PBLtAMMdlqD608oU6ZUIEx/iYDnS+RylAZrtEJLKh'+\
'4JyopvvyVxF+\n7o3OGzzDfrOJ7wEQiyAI29ffn1ZGDNZ01Yi4pLyCCOKo8jj'+\
'VPcFLfAJHlveMt/R16IAzoR7+LnQZ\nCJN6V5L6zkrsYyRj2/H7puBKKX/CEy'+\
'LRDHgtToOm4VG4yaugfaMfTkexIUHjlvhCPCE7WCBVw69D\n2XzB5nFln39DL'+\
'iKmDF7q5avbY4NsG9kSu83yuFLnr2Y8Wp9z33VHSKxW28NeW3rrMyrIWXxpV'+\
'Ml6\ndJeUC33hOzsekv96nb2yhVrX9S1mMH5Bhhvyb9kmh6ZgGwhlf0lL+Xf8'+\
'9sbla1R5nlmlZpzAa1wM\n5v0AFs1I1A4I+xFAkFzqKkyPu8jmpct54D2v87W'+\
'SuKP3I6S7YeJG8ibUaxjtT11CodDZ3t7f0EDb\n0UXbe7fbbm1nHxcvbXfXvc'+\
'5E50zn7x503St6QrrFEha1GIBIrvrU52s67O/vNHmdehZ5fmD/u+gt\nhilwc'+\
'gKGuFbjkkm+NLmMzylEcWy33uXb8mzJZDx8OauRVKN1QZKrtNx+P7GUoPSao'+\
'qduFJ57VC3z\nFjrjvSAus+6gyAdR43pgoonrNY5c5UxtMnBPJ7bQfhbxKfDC'+\
'Chc+X7rAv/APLlYsVwnOLzDSOjo7\nbQGw7r6FfzI0+nhiF5T5+YXNLytLzqw'+\
'rPd/oSIGp3Uv76QbpsE89ImevtMl01UE4MnMgXwSc9qF+\nr8K90FKSYYKp7t'+\
'PHq+IXvzhp2V47K60k6T2x/Pg6M5zd4r1zapbHDcsMAzvRJH48DvftOTQ02C'+\
'nn\n/ql3kYZIFiY32Rb9YIOaIrlu0E5jl4PfdjnJOyAM9AUL9z790e2k/3Vjo'+\
'3OPeuApvIlzgYN5H5O7\nFHFob96bwXfsmaX9k7cKZ+Yuu+R6XIDYtybQxuye'+\
'hdx9QfXaehQYYi8d3qC2Hc7JJt1sGdt98FeO\nKH2lwMI0/Qry0dKSOy6QgNH'+\
'15L13tcoZdLe1ScXnZd49XoAEaPt+0xHgAtX70bx53mPgm7dquBHh\nvK5Q2W'+\
'IsoDGRBQcAcEzMGB+Tkh0HShnjZ/rev9gQFd/psOWjpN3K6qWheXiCS+ah7O'+\
'+vaxvgnjCl\nHAmRyUBIoXyxAckcYKsVrrT/b+MZK99SXIEZMM9eWqvRQUWMt'+\
'gbOyabfJ/QSFSZnqbWz4+oJMKFD\nFO9V5X0W1HVD3NgfOZWl/XVLXPox86l2'+\
'2Q2wpn1t8RnVmTU2Aa/nE+eCevTf47UKvKhqRtob6Fvq\nUypE2o3fDpmfzyM'+\
'8975wO349KiqHwN21Y+GRjs5YxZVpIg9Tz/AgSvZkwLOVd7EWl5ppBab7Hl6'+\
'w\nhS1sADEhYp4zx7NtgGVxE0Ur4edOA9fZy8zwE0hyMqZ19f6kLSo3yXKOu7'+\
'mYiolivi54BjCL7Xmb\nkZcqmQEzO5ZOKAE2v0+cO6Z/U8u6ZEvJvJ6QuLpKt'+\
'SauM9C3iPthI7dnSbg7W+NSWWunNxOpmEng\nRpkR+mv/phwwRDcgv95KicAC'+\
'ZzMXz16N31gJcZMMkN4ZfYs4mJIXIZZKyJiyg0j/VUVwX+P5ka3l\nVL0fhPk'+\
'w6ZzY7JXQ0rer61O962+u3ditHSitwGV233UxVhh0npdKGlS3uwtS3c5q0kr'+\
'GpF5aOnWg\nJ42KO/eQxUoAsiwt7UbE7UUfmvAekOKPxzaSv5k9U83mPifwQe'+\
'8xX2W26mz9l0bylvoMb911mDy1\nCqGrWz2KTob1Lb0SdQHyD8cMxLwkQw4F/'+\
'3Qby7uTFiK20NfjijaA1muXnPkMxJWwYLo3dl9lipvd\nnnBT7Vo+UR9wY93u'+\
'r4eaRPbEtoMT0DKAhbDMZB+JbhHrLnAAPSXjHz/PWNN+0WWvhE9DfDS8+Eer'+\
'\nEIdXGzszVYidMm2sRWSbVH5SSMwQEdoIbThED7exs6epxSCviCFltvu/fUd'+\
'4bSHU6kGoRcmF8iBs\ntASGnXeEnT7m4h79ePiEyNXbNZL/43ysc+p+W/buT/'+\
'XWUk6Dp33y8FzpF86Y892T9ba9li+vPs1d\n/kdylcsceE6jCqrbUjTrbz2oj'+\
'qdlQXrHKMeMxnB/YtEAALW7RxJAO4+5olZpCRiFSu1qLJYN/9YG\nPRSHv7WN'+\
'mvuzSKDlJnGLgnPbvksAy6WXy1L29zE2aU3m85PZZbbBjVzPM7omEgugY2Qk'+\
'TO8OkjuS\nfhOFFO51Xnq2rODY4VYWQoaatQnmyjcOKyd7wJ25QNs++LL4XhG'+\
'hUvbnYeB8NUnQtNZw37G2hDix\nYC4x1qKJLxmbvFcd4dd3E1WayQdOZp3KFL'+\
'WcUL/QAnsRM9EWruOFerbjMmEJClH7ekiN+1wpjhrD\nLWA8lFzoGa6lixrVk'+\
'bX3tkd7KDCsVS8LOxo4ZSacJT3OFpL3JwM3t5Ph6MjS0rNEpq+5csz0ZriF\n'+\
'01alx6YPJQOt5gNyCj23aPa9odwiN7Yv5xqMo2bphS1zn4KI71I5T9l17uo+'+\
'uu2Icpnww5NQoPcN\n4G1fnkjM1q3ZGR7BuOAhEO5pXPAFtEe72ao2S3BwfKk'+\
'zfU9ndFYtAv0YetPDobV4Quxca4AxNetO\nuN/HJFqMuM0Z33qeMygv64j9vc'+\
'ci9xNhDjpScbBz1SdP1t9snN7LMoalu7dbHU5RzY6ZGmgK73BF\nljGvvTdWy'+\
'Y7z8V+a9og5hBBKy1Wx1qH6E+angisowYn3Jx5pvvdAM/cnPS0GlrXwwa0zv'+\
'+HLpMhr\nE+BOviIiS1m3K6NLkPt8rL+kxUw8o3mLc/KKeTb+BE/EUe0NvqBl'+\
'15w2VQG49vx6HdcF8cpObSHv\nu44JamqmZ9QlQD15Ll6FH/1oirI3n/mD8c9'+\
'oE6ss+2n0fXidDz/RUOrGfwF8j/FOBgIIYZuNqBVX\nt72vf1QiIu3bduHbza'+\
'u/BM4PXu1AJ968yEHX1LpcNC4c2/HJ3Adyxjy+efojPcc/BX9TVPvH82WW\nw'+\
'gTT4dBKn2joqMuIxanvVy74VNSbT8WpT1yKgF+LlyXSrWRL++fiO/fS9PHXb'+\
'lmJkSWORmjKmSKO\ntDADMSryfcyZRoT1mTixv2yHuOW6h42XzhROqxKHIilc'+\
'8p0t6X/lkN+oB8cUwhXJx2JvctEMb6iD\n1tQudPh94TGvySvogiVM3n3Euxx'+\
'wFf/WdBX37ozMSnpkYXBmENexWDKd+5fZkXW9ETgs25t9M291\nxyZSZ630E7'+\
'FETHvtTXPkCo/1cT14KeNglsWf9qOBfqM8N/XhXI/0Vdi+vGHh3vD70kuX73'+\
'ZYiXVV\nZSFyrQaPYk7kdOxbN5HK6gupYo5lrh37+M/T+/FOjQ/7Sd+xtoinV'+\
'WkjabF5t1I2YwbNs0PUHU8q\ni5dnVDlbsvrqRgFIDtRmygpwHcGd+JGh86u9'+\
'zgVn5FwWWuZjR4Wg28tPGconQbVr/jsg9iynZXwa\nRmOIOuRS0SCjmrfHlw3'+\
'LPqc9Aa2lJJzWicaZvrxl0At9eM9j/k5EjJr/UoXz786muxZaCENcPQJu\nmV'+\
'R6psw8Ya/VB1zMTO7oM6dn8SyIpSv7CMrZKPlbI1Az/R0OZBnvOvYsuzkGbM'+\
'ny8bsnt+cnxPJg\noBN7BJrWpVwZoyWaGxdpG8/dddKdGxjzOeHORqiH78Mng'+\
'L4ZVCj1rvpGwQAInPOjMKmJ+77RoHlT\nSk8qz745kP9FOUAc13jraXBcwvVj'+\
'ZfU8VyV3vVWrs19vqh0y6paFZ6vs4xPJfdKNlitlqNC/0M86\nsBkmrbSyr7r'+\
'E8sDgCSlXGXLfps2HG05IytIC3ijvHoBSFohCv/8Wv/Zf//Q6eGYJpNwTa7L'+\
'usArC\nitntiFhZadjth8YCf8luPS6jgLVUXQ9+pwSHDU6BQtYiDJym+kxjnC'+\
'NSwXNgW8tfxWGye/+sLg1d\nzGxsihDq2lJ+LNXXtNW2/dHfr5cEqLnOchr9t'+\
'nTlWga5ILPmqa4NU39j7B7AX1/oB10PuQdUgwln\n+vH88NbuLL3wfOAEcAOY'+\
'BwKM73Ed3kzoNzl/Eti+eXCuV6VPBB5wxwMob0cNF1OfUA+/YXeu6R4U\nYTr'+\
'qoKyGPecXsyoS73kjYtghBpnyNin36HH4pmnBqtc3kIzTzvfi+ntiew4Keo2'+\
'pH14J4kLeuhyG\nBAXgB+gdHgU2DuNvD4gX4u48sEK873krBfInorTE+7/ivX'+\
'rcjTv24qkEENRvZ+lSfebJcdM7vX+R\nIcsnViuUCr10PvWKGjkr0L5gFPhNy'+\
'WREb4/Hwd8lpToTHIToTMckx8WITT5+clSlXbmM8Iw/+XVB\nKcoSmffw0sl+'+\
'8Ev/1bE9ub3LSzr6U4VHXLv7YNnEAFOs+E3p3Lr76Hpsis6xy8te9UuA104b'+\
'j6WR\n6mL02YagVLScvPV68jpLYZGnpeQbWTanTVQL2bte0nOuzXY+8XH33/v'+\
'lDS8eHhUO2gvbJ1LI619O\nZ37s5Sbil3PirkGElpVKF/bL0sLc0ndf4IuNSg'+\
'8AZEoqYMqZ9rZuj8nJ+cG2weLu8keYRX9D3bYP\nGEiERV5mZsfRWZQn55gm3'+\
'ynk+QL0HknEVTtM53hyRBtyeaxXqBuHQgwi+3tboEfzauF79Gk48/yJ\nHjkH'+\
'H0baoaXvze/d0r4yeaNsiMLu7ys7T+x3cKeH0MvOx+AHesrFUxz02pz9cOrh'+\
'v6r7N0ZYIXiE\n6KX4IMRxOZaTClyh98tPvRT9lR4wYG6ee8BF13f1ssfxiYm'+\
'n1CIFZeQD/tmvfY9eAsjA/Htpp+aX\nU/YOYRPDD1KWLnBnU8VXZkN4i2Gm3h'+\
'Iueu7BlL5zhWvKSi+ZMr9aIdwZzfrXhDopsjAwb5W9Jybi\nkJboA+b63gvYZ'+\
'mkEHE4FKKWsVduq3dGD6Rw/dqLuTHuM+kgURCAQXRbu5L5wE4kFPPQbhn+fI'+\
'Czm\npSzPyrJo1U+sNUVlj50HinqQ9sM7Ol/5OOLVae9zFe/c0GgHxsg7bm6x'+\
'VypUWCiAQs6i4WGaxhQ+\nnBKTt1nnVFiPPn74wZYKq6gEgkq94hlUv4t82Jl'+\
'FgYzuDuiXTJYTk1Y54nxLHPi9ATubo4t9nZtl\nt6/xlM0Q3Gb624z2gNvrs5'+\
'kw+mHQ0qqpON6SZfifBH3hBvikdj0++SL0jT4V3J+kcLa7upIhxfno\n4AuQy'+\
'SY0AORjwuMKsK9oqBd4v4LAJKQH4Txe18xLSfoN0sHdWJfqkb4c0bcVIg0nw'+\
'3oED8d0tBTk\nhXdylWjAcIIYD3TtYzJH7OYfXvYvLcXeDyMPQ5IL/4oygH0j'+\
'HsN5sxeF2SXnlfibK/Jf17uVKmA3\nla68ORf5nstJm3HoD6hqd3o64yKZN2+'+\
'JZQAgofpTsP3ZB5wNN09YyhlEmLLwJXBnkTONx50RSw/C\npeUOdAF1vbctnY'+\
'WgRtWoAvlvpNySsHH5gvvNIBM7+1OSxtlKLEUeYVTaGwqrHMU92u237OLtfq'+\
'hP\nCzXYzj962UJVFXRA5iOw2R6ssk/D8C4hYXBXYUXujAmuVm5lXkqACTs1W'+\
'PVBdFNk8zT9eZNEGh4c\nrq46Q60FV57XOH0jb/sNsW3s2ZDuq5hWFFYW0a4O'+\
'LYC5a7yw3td85inukm3Bn3N3KZUKyypwtMXQ\nsCyICdtAjiZw6QYKcvO75wi'+\
'WuTPge6eVDMa8IG+udwjYuwbkCmlp2Q50AJua8sPxSRWTD6hxbHLF\nl1wLO+'+\
'5+Mrp5VX04RqjooIdgTg2+W+rK0VIfLLWLOTnf25tdVmEI6qvTkoZBkPkcH9'+\
'gquPxgieo2\nRQrTbS+aELN/fcr0Y7Rck17yk5uYTb2BBZohab2C9GTxfa3hj'+\
'Z3ljTKswSmNcn1swL/emhNipk/d\np6c5CgAej8QdzPs+ODX4Rh7mdxJz8dLT'+\
'PG23bl3qBNOEv8dA4A/KFpN7NA//WdT/0rnMw89KkQ6S\nm+Vt7Ts3gzmPkwh'+\
'kNriDd70KacFq50rJOFMWynUg7rDwODHJIInI6Rs6BdRAqR9mU60cChzgUBJ'+\
'd\n+dr2ifXARB0fR+0tG29TgGqLTDQPLxG3N8Hpi0vPPBt7MvBJcSJLhXftR+'+\
'kmg4w+a7iBMpqJcLVk\njNwf6ZVbrCkQuxhSmtLMshUJkCu3R13cBkg2RudRM'+\
'px+SHVpqBEh9b+IhguBxhPvmVSv50aSIcxv\nr42uQ7QVwD8NXUzK5CysWLpd'+\
'FW4UgE64KByPsr0Kz8XqBPFuVyKsiBWECFMnu6Xzg20k4nvjMCPj\n606KRpp'+\
'ip+B4P+fi2i021rV8bG3pQ1KBRerjI8476WKCv06PHYbG/HYhTjEsF6Bje8b'+\
'c59SrGGhV\nPQNdjTgI8mJEva/YtSegvsa9vpoyD4Ko8/mvi9wBHWD0nV+JCj'+\
'm2iW0EvWsdr2SiE4ZH2wCpeKW5\nEiVS3W2nr4+nl409Fe3o3/C03De3Y2R8t'+\
'wx1Sae0zjpa5a7tu0dcQw6b6dPb1yyL3qbPfDVBGOQ+\n4+X49TZhgXdtqP1F'+\
'awWXwAyhR1Hxo7NV2RY/WYhNYD/m5d9s5/W533ZlqaIwSOFMSuzzyQ+RSPVp'+\
'\nxevKNr1OP9Y04wYMH/j4IPx+j19w3RpGcFT6Kt4jR236o0jtiQFyfQOSQ7j'+\
'8wDgHDzd9thSj/3fe\nf4BDEh/aC/lm1vfMbYMlpuzfTnmB8IgzE2Hyjq8inX'+\
'INj3s3fzl/8RFDX+hh09fnf1iaOF/w4K+F\n0zVIkMcuIGs3jPeyBxm831UCN'+\
'npTChFn8CgGMYZ8K50J+fjeX44u96Gyq893xPP48MJH8NHvsaxR\niJD45FkK'+\
'24EkjUf5DTczmMLkhazp/xx9EPasYQ/O2Ikrf6JKfAaIMz0wrQGX3NoqpvrX'+\
'iNwrAON6\nnSP7KxBZOYdLLh9qxsaNG5Xo8r4kv7Y40STXu2FYjg7R+8i66ZH'+\
'2PVFRVGdN2NIo2nv0/mVcqW84\n++rlH3yR+fSJFPx9YhXvj34eVXFfdSvwzO'+\
'2CjlCJsrDGvIM7J1WwBfZ4KezctAchmh8LXoIopAz0\nXW1iOT8iy+S3Fwhe9'+\
'12eKXVzcloakYNsq1C0NZyOLl3lXw6QvNaHOtJUEj71ZGJOshn95yK3E/dY\n'+\
'XrJcnr/M//cZnerGTvO7ByAA3Qk+ZoyP2+4b42OnX3ioybVi/yG8rlbNP52P'+\
'W9DVkxv7x7hM/YWZ\n5mMwAlwj/x9Y9Bj6p00TcWSEzf/4G7jZ+v/ZbZR0b/5'+\
'zjFVJz+P+d6fjExDyv/RuLsp5EWN0ubb6\nELrVJaWaFEAs5ZIfqA0d3xBIA7'+\
'aDEggvjpzYlDhtfCZ2K9Mm9PDjEjaoj1SbElxs17oS+dzNd/mz\ndhIkpF+S5'+\
'7g+/Z/fihRwVAToctufcKmePlBzevVSzTD13brvcuUdx6L2aMXZqfpDr2q34'+\
'5aqDSuW\nKr9MK07njqia57fHzrt6L8iEPgo7V/vzWXf43Nqp8LTZ6TlH/Mm4'+\
'7iwfNHol0vldjnfwhTmjg2ZT\n6R681Dfra86lif3r0lON5ND9wY2hJRjfedN'+\
'QsnjWOxdiiu8Ci/1yxcF25vSidsGBgKP5DvD65LTb\nwTUra4kbrxBaszb/hb'+\
'yHhy9dMAudTVeMobFiRWMnWFdNEUPOXxe+4e5v9PrSpRR+yrEdLQ7PZkDN\nA'+\
'LffhuqnarmqCygilqDBMAuIiKvdeYspw8Fwg3tLrRFLbz2+yQL075xQn+JO7'+\
'0jEAXzcn38odn/8\nfBE5cDvPcBb3/D8pLCIiMSP27fOv+M+UEc2NdTb3dWTH'+\
'3Lt76/89jw7qN9vMsASzDA9utVcf/LRT\nPSqpsWn5IWZGjv1tKrzs+b0X8hb'+\
'49JzWZMCrF+rfKclyS3cX0Oq1vQBgiL9RzeDfoPMQYmQTGiA/\nImsCBMPsgS'+\
'n/u/+wtLpgbVUtb3VKRaUmO/uSpuZlbe1aK6sKS0ugtTVI838UqxvaVrc0rB'+\
'p0re4o\nW11RsboaZvUu22pb2/qRjk69omL79nP2OABKAMvTUaB/ieE7M+G0a'+\
'0yGNiyJnamTlqxjwPmqeNnJ\nPYhfcw3z/cS+xE4sx6fxdAbHIXxnDiIid1cE'+\
'0Iocl+8EuvnExadd5ebT3EN4cV4OIv3AtwTP/xw8\nvKMtpnL/6GCxKCV7umO'+\
'zWyBQIdL/If6+Dt8KDYTlXcH/7BNZONcrCwHBKpkRb9XwcBj4uVG4D5AR\nEh'+\
'UXM2Pknph2iEN9H2HctTTbxwHDaWA7EMIG5qIc8rLBmU4vBHiIgoobAbUMCJ'+\
'6ed1OtBiQJpUEN\nUBwUg+iJn1YT2713DDzxAtT48lPhreUNVTnTZ2euxt91A'+\
'NMjWFz350ZH5aouN3aPssY5RhNTi+CN\n+LMx05DnGLKS3tX4s1ct3XxC4s7+'+\
'Q6zsQn5VzT9LfH1j99CLFubZq/PLG5AX+H8p3KXV9Ewd6Eb/\nYEgci1P6UMT'+\
'9+b+k8J8OpIAasAkDvTABAhDFHhdC9cCKaoE0xAAYu1vBlwQEiDfUIIVz0tA'+\
'Ql34Q\nAGjLYNiykhNtJ9YjdZ3ik1DO0Szk3g82mjR3rHsyg82MdhmK0Km9TK'+\
'DTKzQd+y1M8hPSmnBuz93i\nSR4tf6NSI1MP2gbHc8M7NEZtBTWZ8a/yi3tZm'+\
'MSo8GDYPRpxNTITW5WUDJd1/H4vPjkKmravc+0n\nbgaZgkiLZiUkpiSlpJ59'+\
'/Ld5lRWDSkdHRiWn+gbvmmtbi9kXowuPYbLT4mJ7zxzssEyDJadEJxki\n2Kx'+\
'vSXe69sFaNfWi9yuyopnM1MQOowwWicnwZEXMqBbrRO+7l46eqVbjfEclxVb'+\
'UDnSJD07tBmi8\nu8mEm9zsWv+L6ISnHsC+irLgHki7mWGclgVUOCIbvi8uFX'+\
'7C+YJlYkrKQWZ0EqOxiEHlM+DME2IX\nKGxEVWqc8XkrBDI8hrEdjtqX8V9+9'+\
'YpZOFMQLlFK+lfqcwCglQlOC6VEEUcrowXNonAyCZqoJI8Q\nhZH/9yvA1OAC'+\
'AEQFjVVDwPaphBNVTZSOOOIxUDRUxA+jDsfP7QjHRTCacggcFKmGFXFGGdrv'+\
'wiOd\nzxLTZP4Xri2KVWTKKMiaY1ytLPGCHUBqCKlZ5AgCnScuK0eTthA2C4W'+\
'p8Gi4jgrFWAAE3qFIu0Eh\ngAf36eqJbf+LN6FImEGtKYq7KXZ4K4SUhJguAu'+\
'knhhJBu5wSaIAokBlZyA8YAQ6BQ/uRv5LC23vx\ncDQGjkGBkGgcjigiKr7it'+\
'zGHIpCUiOJQaZgSQkZDHJ2+XygU9RUzNxCXYEijb3i6qeDENLTFELXC\n3vt/'+\
'xTAYrKgsCkdq0cAbYQjEIgJeQcRJFLS1tibabC6CzZdDW6pRYRBAW/rWHagk'+\
'Fu0uhepSF++J\np62ldYwgACQUwjsFarYjXFtpVHsNV5GDD6EUxHXwbaJoWVl'+\
'pkhHx36LC5UnKongyStybbCMGw8sR\nNGRlxPFErLbImKzKTsOCEOOoJ7gKhJ'+\
'JwZCheTCTIcXjNRHwvKkYGpqqPlkPnmAlX7N6r7vJORllk\nJuFxXlpYa9LMO'+\
'4EQDsOKIaHieVg5cenbaGsRCazcj28rRUl+eMkOmIi4nuA3gN/7HRAJcJQRv'+\
'Q2C\n0+AMpkl7R8lZdbRWtWSROhEm8y5nPVmVZBdSZIxCA1GHjsBwIiAkTMJ2'+\
'bc1EXlTVKFNB7jyWgA00\n0drVvgDzd8C2oBBIBs7AWCTg7UHj9/wDfJkv5jm'+\
'HhMI9uYJUEFOkVYRFhFmS5KkGGHE1RQIK6kmx\nGd0RPwRD4xGBLJI4VVUeen'+\
'pH4k0z6j4OCqMgCCII8VBvZfhO7pdnOEUbEfUNBTFcvCQ1Vc4sPJhK\n9fsj7'+\
'LAgorEkWAwep2ccBId5Q9P3LQ0INRFpGE0PNdFAB1l7F9ms4dysLBkUxURSi'+\
'pKDQeCjLSxV\nSR+vJAs7pKlYVRuUqjVKn+og53/ByJvuMyO0EqCAeDxBYAxs'+\
'I0MZd3o79GQF3wH+VMAGZTYT1Zgk\nSKObkjJQ5djcJWF4A9AoVkAECjyBpLx'+\
'qgqnpHRGyvaK8eeSuHaGkPLrWtGRMgAR+IIkIHt9WmrvS\nmyLNh2OD7MUkBZ'+\
'IoAFqIrhOQyQIn42PG0deeoyQDVXQbfwsVEJKyBHklUSXCfpF5EUHY8q6dIm'+\
'Sp\nPgz7GymDl5FSs9RuFJx+KKrgihHI85W/SgQJKUxVcw3PEoVaVS9ZEdIe2'+\
'4Er2N1m/SniwNkdoY2Z\nYBsgbmkTIr9Pyt7pEFzVkiAZ5GtP3O4Ak5GyEbfF'+\
'pKSQkmn4+m3hHq1dPjriZpIYO3mMt7ykGBZL\noQnbJ5MqLKLlL0iAYVQ0BWl'+\
'FkDLZAHUSqCJVNzQIBcIOYYczNcFDQuWGlGqALJesYwolGKoeodE0\nO4TfhM'+\
'qqMooyJvqq0jISQCWykqS0kbQh7idWNm57+ApqAarWonhS6YV2Y9GcbHApHo'+\
'xTI3rIi0Bx\nKN8yMSQzCdpLef+r5/fcBhomCoUu3aYjdchi4iFvCRI4g97DW'+\
'x2WKqgH+GTzDP9domXKTJScCEo0\n8fqpkCzfArxy2Ny8cEYMn1PlT4CdU1HE'+\
'FGI9bPcZu2AC8FLZPM1MAtACg5Lasz13ocSWWwkla3Zo\nJVGr8LxQot+8UCj'+\
'mpV2AL88wJ1q5mb1gORK0d6ss0LeDZ3eK8RIwomu+oTpWm6qoTNYi1/ymaCG'+\
'l\nVFC1V60lqQmNbX5ZazfaqQo3bPdP3E3t+jMqKlw5V6CqGoxCHw6wLnwrrq'+\
'/lPyWu81feEmd1oDoS\n14egSia+XXmVrkRCN9tYIyRNSTMdnY1UggtU1pe9a'+\
'w9TBt/5N3dLVFtC8O6l5B4LZXUC2ehGrqxo\nNtokKiuvI1ker/oBdleNeMBk'+\
'Z23O5CdASmAL7K/T1ACaCIqBBw6BhaqgPNqGtIANPKXZpXRYTVgk\nTP4gcSR'+\
'OgAeOEHzkeg+P+5uQjQ9a24qjtz0DItSiDFNagsO/6/4SjVOCIYI2Aei9WB/'+\
'pur5k3VAk\nFTGt7SWFJhieSNnSPSwi72VUrbIbSdiDU639RSLdavStCfBbUz'+\
'aG9sv0fscZahM6ZXcraEF7oIEy\nBWUzzfEwKYhgasFk54OEDguvkW9KKYVTM'+\
'aIGa+nv51rlXJHJHRqi7iQLCyhcBCyc2xAK6kASe46K\ndCsaEMNlB4GaJIKu'+\
'oiLV86TyjrhNxLhgDniI3CXIAkbtb5buFhQdlSb74t9Bc6CYyLq5XSVQPPaS'+\
'\nupi6FnDjdJw2S8po6NaxNGO52Z3eCYHUaUERqF/rgZqImY6HXocN5dsmLIh'+\
'2VqAKlva9h/W2bibm\nfLlNSgwQJdCjBQvA2e1WUx+kL5QYygxuRZlpCmSR3o'+\
'IOcY3Y56QeA21/xgi0JEL3peaHZnuyZF3W\n5umgbB2KiHEEU5EoIeGlhLsCc'+\
'5/9Hil+R2qpuPdX8h4J0vQP4JzgD0DtjGK4isbX5JTrwjuCYKBC\niAAMRFt7'+\
'zcriBLv3XNkJBFpmTCmfDugnuULN1SqsKp+IHQ//agee2qI5BjgoO0MV618I'+\
'k8tFpaGV\nV70EHkARymOHZPaD9qkDSBcpYLfI9bbd41XAPjZ75AWlKH+7DAW'+\
'zllhBn7l7Tx8YCxeVoBBK3w6v\nCXGxyhhpimt+piWNQcGroFMkurOc3WNicD'+\
'UE81AYvlcW/nsAqswm0TBKSGardk/UJ5woToBDTJHY\n1zuMj5JFX+PEFVJJs'+\
'm/Kdm7BIE5iChAMWQIsAgeFvm/ERipLyNVB9X2uD9ySv0AiFl3ziZt8dwOL\n'+\
'D4YjZglv36KTr4iSLQZF1WV0xEiKULVbrZOxKDctp+cikdrQNwPiOQQT6Xjb'+\
'9CIpphWi65IcnrpL\nmrEdJF55wtBIRQ1TvlvzQ8KlKyiiIaaAHPesaJi6+7i'+\
'jovdFDa1fknj1eNRIHUUP9eXVsLtLIfkl\nFUSEofb0ajhEpX0S3zRxqvv+St'+\
'wr2MoKLqmisP3UN2/PSwADijiCRqzo5Bybx/tptDiYG4npEREm\nO4bmYmKHB'+\
'drWG6AvoN6gLEHU+AEwBHSnAx5ZxAAInhnMo1xpelMCTIVahU/dHyEM8OW4j'+\
'BMAAwK0\nQmC6jK63PadMAa+AGAQI3A7AK1PVSLdLp/Iwo4sRQDDmICh/5S0E'+\
'Di6lNjxOBPVZMhD0jKIQbjd0\nXlUGUOtDTYhOTs+gwx1eAvlLQyD8mSZQROq'+\
'U7qj2Fh+k+AaoKsMZdaeNV/QgF6bTUtpAHNVoo3Pv\nx+lbYA/UO2mVuSKAaj'+\
'yltTzGUDEDtrhaKEkDKs57PH2z+6zs6r2TmB8AgB4L3nZWCQAACAH/h3Cy\nl'+\
'RBAXFEXEACI6CHpfY0o61ma+yv0X8Lz/28phjlx4c7AGTa8RLZgdZswk7rS+'+\
'Y8L+D8shD7gTNo3\nNvL/VdMW9McKFsGp2P55xL/oAoGQxeI9+D/5Y/8fhU21'+\
'/f85/z/JCvpBeX8BP4XCgklgGVG34O92\nOq4YZPdvUq7s9S/7/rVS/BJQwQC'+\
'EBy8YgRR8gWR8Bz794vbPHMZb7zLFAADFcGetRUtgxjrHBsr+\nUQL/v7r7Gv'+\
'A6ivPcOZIMpggjgmzJxoAoThHENpItGwcECCyDCcYoWAQncbI6OmePdPCes8'+\
'vZPZLs\nukEtqpGxSNXGUJP4NiI1RSF+QCkm/MSXCFCDmzipQk2uaX1zdf34N'+\
'k5wU6W4N07qxvf9ZvZn5oz8\n03OB+zxXj8e78+438858M/PN357ZR4yy1GtH'+\
'pr82WrF57Orjve8eiU1S2Gn9Bw698+irbLKEbT33\nvFGvcatR9mhfHasrZbH'+\
'3Wh56c/rJxxtx/xiimz7qHdzy6/tW/uuz9558vAkgxM/dUvrQG2Xv/s94\n/e'+\
'jr5QxJefTzJ+pHIYxnv9v4L90Xxd7YWrp5jLOCsPTdQ/MufG2iIrUV1CXvHt'+\
'r6bDPiIfqTJ7/N\nKhhrab2/bM19J99+9OGvQt29NQ/2ttU+uLaltYXAtfFHm'+\
'+f13s8+Ppb/zUNHe392309OKIX6Af2t\naypljXDyXxr+1gIs+POA/xHcn8F9'+\
'DW7El3vVv9654p7VK1YtXrSwedUqlnG7EjlvYdKy8GSVHU+u\nSou5GWOY0LX'+\
'k7ATmeTnTdRn7VDrn5eMWMM9MeKH/FsuyE6HvtpxpIiYDk7YgPbyt4u9QM8o'+\
'UV9N3\nk0hP362lrBp4Deg74SZuZmztTYyN4VrbhBQ1MjbwFGPHroT/Ecb2Lm'+\
'Os/zrGKoCNLGVsx07Io3VV\nPMnY8GLIXYsW9zhj4zvwfJCx6VsYG+pnbFszY'+\
'2XXMLZyAWNHPsbYAcSzciF0C7cH4QfghnC/Fhw9\njyJtf8LYUciUv8CY9UXG'+\
'quEmP4qwiG//9Ywtg3xdBuG2xNjQZIzN+yWu/TG2c3OM1eC+Ce5wC9L7\nKzR'+\
'wPK/Ox9jeNYz1wbU9DK4tVE6MHb+KsV0PMda0PcbaHouxI7i2wm16Isb64D/'+\
'8CcbmlsbYGNzh\nLyGOW2OsfHmM1f4p5PGsZU2MTTwSY41/As7BGBuG3gZ3xN'+\
'g4wo9+Bf4ypG0X5MA5gHRsR768PuiL\n0kD5gr9/M/SNNAzj2vLXSDOujUjbP'+\
'6NcfgV3Em7ailJWDjcH7gq4hXDL4VbA3QX3GbgOuDzcH8EN\nwj0BNwQ3DDcC'+\
'9zLc63Dfg3sL7r/D/QzuGFzstlI2A64SbjbclXC1cIvgroO7Hu4muBVwn4S7'+\
'F24d\nXBIuDZeD+wJcL9yjcDvgnoZ7Hm4M7m24n8D9DO7XcNNvBxdcDVwD3Aq'+\
'41XBr4T4Hl4DrhMvDPQL3\nZbjn4F6F+zHcBNx7cNNWlrIKuMvhFsFdD7ccbg'+\
'1cHC4L1wW3Be5xuGfgXoH7Idw/wP0PuJ/CHYV7\nD+43cOyOUnYO3PlwF8FVw'+\
'V0GN+8Oar8xVsJKWRmbxs5h57Lp7DyG6Q0rZxewGexCmLCL2EfYxayS\nzWSz'+\
'WBWrZrPZHHYJm8suZZexy1kNu4L9LruSzWMfZb/HrmK17Gp2DfsYm88WsIXs'+\
'WlbH6tkitpg1\nsCVsKbuOLWMfZ9ezG1gju5HdxG5mTewWditbzprZCnYbu52'+\
'tZHewT7A72Sp2F1vN7mYt7JPsHraG\ntbJ72afYfWwt+zT7DPssW8c+xz7PDN'+\
'aGKXA7S7Aks9LtXiLBDU971rDcznTKo7uNZs5mZi5n58T/\n9eJiZG1a5vGY2'+\
'eOQ9Umls0nDxV3azrKUnUuYRqIznnM7IWMk4q7HOlhHHKbLTrEOM2skujwj5'+\
'ame\ntOKpD31pWY484pFlLl7Eb2zHv6T8azq4JoKb4ImFq2fkzI7gapg9/Naz'+\
'1xuul2MdqXw2gQRDDeLW\ndNKW3eF7nJzNPR22Z7OO+zMO/8+gfLEOd0OG/+d'+\
'7PcpzF/4hkV1GMu+wtGmaBhSV9kyWziaY1Z5P\nW9A8VBjP4gprzzJ2l8nTlz'+\
'W7Q33azIEqTSObz7SbOeaYRGHk8lkvnTHJm7RdozPJn6TSlhncd+TR\nURh23'+\
'iOQAKIwkmbKCIBMvANKwo3teCJUzkQmExTOXZ92mJNHaVDWk2Z7voORxhJW3'+\
'HVNF/eubSG1\nlG/ce3bONEQ6XS+OLLrxrikAyltw4zLOwYMytzvuMFRBnjee'+\
'vsADXVn5JMXldYagJfrFQr8qxL+b\nY0leV4srYdmuoErYGYeUh2qQznZwCKp'+\
'KZ005mqRpmZ6Qp2ojPYm8BloIh1CG/EqLnuIm73GFBrnz\n/Y7w5Uz03HE/dp'+\
'Quv7qIVrQ4KoYQSlnxjtDjR+Nt8CMirDueywbZyGcLMgJB1Hhe4buoZnaZuX'+\
'ZS\nQ5eDttTl5NH6xaWLdWF40c7/91gXIub/Jfj/kBFF18XLLmBkNeibYBn/+'+\
'Wb2/83fQl5kDBadsd9i\nkNkRg6HEQK1+YUKRK/OvGHWwktjUcc3xr6W+w0gK'+\
'rkJBlsAN+fGUMgOVoiftkVfEzAzDzhJUFyIL\nIeKF7Igndi8ulWouknEv7t+'+\
'XcJkpctpOY0sphbGaU2pjdqgNqML18qmUqg4MWllb7NTaCNIsZIjr\nPD/1xa'+\
'W5JkzzqUvwuViQZuruEprcJ2UufvdZv1wFYnRk8+g0vOkRQk0MSLkSyvLLNE'+\
'I2MFEeEfKw\nn+YIwVCZDfraOAdcIi3HLj61DmEdk3SdmCbXHwzDWVOIGLaQX'+\
'VYZ1Bb6+xbcWgUZhRsIEYP3aBiP\nRwj1UPgbrwxqJv19n2rwTBn5b1SmIcJ7'+\
'HZpfzAzjEWaDHa+KuLh9dipmy/EcglsZIkaXB+sEjT0v\n53SSZu9K3kl5jqL'+\
'VC4GUzZFzegmQI5eE7HzGhLiUeK6GzNDuUIe8F+zy6s6RZW6EzOhuGbmT2JV'+\
'4\n1gEZKYwn0aTEY0Nm5aVyCv8ASFOYU4MPNiBzmSwzAJl1l0U6pCEH0iwhYv'+\
'Rz7PICJDV8pRzPn1MK\nf09GngLSf5WMPA9kb20UDx8CsQO1ssxrkDkayTjoX'+\
'xLOhvKrwxLkSNxrulou5R/SzF5BDpBWFeQw\nkGMKggkdq75GRv6DdKgg5yNZ'+\
'QwoyG0jFVqWUgey/Rs7FUlx2fEwO1QzkJQW5F8jc+TKSArJqvhyP\nR/EoMn8'+\
'MZFCpLYNANi0I9dPBhwBs2wI51BClUEFGiGBhGMofl69dGGret3VNZTLXdxB'+\
'q+Fo5hX+P\ny1iIGP5QvrYuRPwuvTFC+IANeYsQjJwprjaF6xDlvU5O878Ql4'+\
'L8Fkiv0grOw2VQQWbhMlQvh7qC\nEEVmAS7zF8kyN+DSqyCY0rK9CvJJXE4oy'+\
'GdxqVmslCkujSFitOdTC+ukXobLOLjUKXnfhMvOZXI8\nD5eK1YsI+TNcyj8u'+\
'IztwGX9EjufruIwqyIu4bAtD0WjOwIDtqBLP3+HSdr1cyu8AOawgh0lGqYe/'+\
'\npPTcIMcTQ54cRWYGkH5FZg6QkRDBhI+jLYo2auHzGkOZTDpL9WdPoxzPdZA'+\
'5oSB3Atl/o4x8BkjN\nzTKyHsjhJjlfm4D0LZeRLwIZCtNDdZUMvaOk8An49i'+\
'qhngVS3ixz7QFSrSA/AJJUkH8oE+taEXIE\nyMQKGfk1kNrbZORc9BXrFGQmk'+\
'Aml3K8EMq7IXAvkhILcAGRSCXU3kN23KzoE0rZS0SGQvXfIyAYg\nm+6UkUEg'+\
'81bJyF8AGVwtI88AYUqv9yLJKHp+HUjFp5VxApCadaEl8VcbOtfJZXEIMnWf'+\
'kxHqpYc2\nyzH/O2ksKcd8HixEU0qpq0AqrGBkxS0/LuOWLHM9kGEnrKtZMTr'+\
'ty8kyt0NmUsnX54CMKEgOyGhU\n6/jsiLFdbphTMYdiYzLixRPrWY3SN21BPC'+\
'3KaOdLQLZ7Su9AuVA0/wyQI4rMC0Bq8zLyPSB7FOQA\nkJVd0ViLz+/YcFeUQ'+\
'jEfrOiOEJo6IoXdcun8HPEM9cjI/6b0bFBGejk7VbtRlmHnoiZE41V/SaT6\n'+\
'C9EIzV8riRAxMWVDKoJ8Vz8oxzwDMVecE42jxFLM5IMFIyJrpFcOdSlC1W2W'+\
'kavOFRVHmqMBGR+Q\nZW4G0vBFWat3ATmsIBkgO7YpVotS+JiMbAUyoCBPAjn'+\
'+mBzPN4AMPyEj3wKS/LKMjAHxFGQcyJCC\nHAZS+xXFRgGZt0NmPweTnd1fDe'+\
'sGrV3hr/wpWaYKMhNPyfHUAmn9uowsATL9WRm5FUjjNxWNAXGe\nl5G1QOa/I'+\
'LEn02iRzguyjAmZum/JSA+QIQXZAuSYgjwGpOHFMOZ8lhaUWP9LssyTFLPSB'+\
'ncDqVBa\n3OtARhTbuw9ITVTr8lnzAdzNf0OO+R3I7FKQw0BOKMgvgDSNychv'+\
'gPQqSBkmzUcUpALI/L9RrB+Q\ntr+JRow9Ts6wc9sUmXmQ2asgS4CUfVcZRwF'+\
'pUpAWIIPfVWM2H5iIkA6CoLW/VXoihNqvICaQiu/J\nyANAVinIF4D0KcgjFI'+\
'+CbAMyHtnedoynMT4d2yfLDEOmRWnLLwJxFOQ10lhUgjkxFx5Vyv37tFyh\nW'+\
'OyfAJn+Y2XcC8R7RylBIHUHZWTa7zB2UEGqgBw4pPT4QNoU9puB1CnIKiB7f'+\
'yq3ynVAxo7I8VhA\nGn8uIxuBdL4bllfSTNDahXVUGQNApndSaRdAxhXkWSBz'+\
'35PZXyd2BXkbyPAxpb8AEvs3uV/+FZBz\nFKTkfORUQWYAmTwpI7OB7IFfsj9'+\
'A5sVk5DogJ0plZDmQhjIZuRvITgX5NMlMkxETSOUFMtILpGeG\njDwBZFeljO'+\
'wC4irrEi9TmmfJMm8CGa+Wkf1AWmfLyC+IfY6M/BZI81wZuaAcNuFSGbkUiH'+\
'OZjFwF\npE9BlgA5riArgHReLiOtQAYUxARSXiMjLpA6BekFUnGFjDwGpEWpv'+\
'cNAyq6SZb4DpLdWRn4AZJ+C\nHAKy7WoZeQ+Id42MnHsBWu7HZOQSIHMXyMg1'+\
'QHYqyBIg49fKyO1AmusUbQDZpCCfB/KSglhAvHoZ\n2QCkdZGMPHwBzU9j8po'+\
'MkPLFMvINCrVYDvUSkKYGpf4A2acgbwEZUvQ8AWREQX4JZN4SpUYBcRTk\nvB'+\
'noGRWkEsiQglwOZO51ig6BbFOQ5hliRhGxt1I8y2SZFJCK62XEA9KkIFuA7A'+\
'wRw8l7izGbr70h\nFvU7HFl5g9IqEWpAQXYCOaEgz5PMjTLyXSDrbpK5jKTHT'+\
'tyk6Bky82+WkZ8DOaog/w5kpElGLr6Q\nsS7FJlwOZN2tsswiIC3L5ZqwHEjF'+\
'GllmNZD9CpIEsuvTMpIlGQX5QyAnPiMjXwIysi7MqZXkk6A+\nQ5Z5EjJH2mV'+\
'kN5CaEjkXrwNpVJB9QLYl5VAHgUxG66KOaaQzDptQ1hx+Srkw5VC/olAhYuQ'+\
'z8R5a\nE05FpWMaKSeerEspFqACdkxBZgHZpCC1QAYV5HoK1SHHTDtn40oKb4'+\
'dMz3o51KeALLNi8ipNIuP0\n27JMJ2TGFGQjkMMPyMgjQGpdGfkqkAOejHwTS'+\
'FmXjLwKZGeXXFvGK2hGJiOHgAxskJF/BTKxUUZi\nF6Fcf1+O+UIgjQ/GwnU/'+\
'sUnZ1KsgWbO79g/leC5FqDZl/DwfyOGHZJllJPPHMrIaSJ+CdACp3Cyn\n5wt'+\
'AevplZCuQTVvkUF8BMq4gIxfRCnBMGjm8CqRuqxzPXiCjW+VQ7wBxBuRQh4E'+\
'MDig6BLJrICx3\nWmtyvVyvsjLAPoIeTak/lUBaHpXZr/yIeGcoQhqA7P+ajN'+\
'wMpGGn0hMB6XlKRtqBtPbLKewB0qQg\nm4EcUZA/B1JtxqJZP99z2a7MqXdCZ'+\
'ltDtG7M3w5hE8ra8jch0xatFdBrEJSCPyiYd7OKP1VXGNLM\n8+R4vo14hjbI'+\
'6yS0ddTyNQnhyyt7u5TVFYTs75K4+Mse06VViC4xt9xYuH/qhHuR49Dv+TNO'+\
'vxe5\nFpfpZ9iLJIs29V7kyzFpNzkTT2cL9iO/S3Xjr2Jn3D8VMsRVrsv4aW4'+\
'rOYs93xfOvH/6ZpjmjkSi\nIM2GQ+vjEpfoGakmnCYX9Pe/qM7/lVwPjwNJhv'+\
'EYhkFcbDKUCfeOw7w/Szs+Z8j7dH1/+T+R97fC\nvDuumU/aC/h2TaSAaRfDt'+\
'jztt8FT5HQWZFqeLsyFCEXsqchWFOTCeZ9K8MqSIBeE1l88VY3qDdPD\nTlmj'+\
'ovSUFJUePr+4OOISdvVTQIbOoMONF0sxi3V+ikepdV+mslBkhoH0KzK7gYw+'+\
'LdvMcSBNw3I9\nPArE+bosE6tE634mQHSN/RIBPzqlxsIUxirOQmP6exdOzm6'+\
'nEtz8TKCxpJ0lgP2XEAnT80yQngWn\nLMHBs6hRNaerUT7XyDNnri3vO5cesx'+\
'4PW5gmoXnXHS3j2xMRsgTDKBVp6GUFyNI9JSHis48WxX5Y\nY7c09h6NfafGP'+\
'l4U+xGN3dHYN2nsIxr7RFHsxzT2TRp7v8Y+rrFPFsU+obF3auyexr5dY2ffK'+\
'IZ9\nUmPv0dj7NPa9EbtvsReHFjsVX2+q7aIzG88QFOUi5XXms+vxJFaYi4pv'+\
'fAjtVORiUWWQHjKXhT2a\nr41kkMJY2aniaXDYaWR8/dxyGv38P8h7wwA7Y76'+\
'W9J4579cdD+pP7PxT5v0TYd4x2fDsNObDyihy\nVmWQd2W8EWrDop3tD0Ybfg'+\
'rXqim0kvKI0TBM6sJ6nwv6L0I8M+sOPSePCq5ALppGTj2GNPyonVfC\nmUs2n'+\
'l3asLBu7BWtZ3wuyHsL1Lr+A807vdXhvyFpOp2ma5iZuNcpFEA5zdhd6YlXT'+\
'pMvyMSTycz4\nt8N8AXHz7ZmaPRKSqV+aYc6ecO4JmWS6K1PzX+VQmbyV6f2O'+\
'PLZZAK06owUyzHmjUIfb3pRKx7PN\npQ1Db8qhEhnM4/5Wicfuskd+qMzxwdX'+\
'2PRm5FcjIvsKaOfFKUDrDlR/0WGLw74qx6mXTCq16v2bV\nt2lW/YDWpwwVxd'+\
'6gsb+ksY9p7J2lhewjRbGv1Nj3aewH9P5UYx8tir1cYx/U2Hdo7Mf1cVRR7J'+\
'0a\n+1GN/bjGflTL+0RR7BUa+zaNfUhjL3uf2Js19r0a+36NfVBjnyyKvVVjP'+\
'6CxH9ZHsBo7Gy+GfZnG\nvkdj36uxexp7RVHsvRp7WUkhe0VhepbWlRWy1xTF'+\
'vkljZxp7ucZeq7HXFcW+SmMf1zR/UNP8kKb5\npqLYezT2Exr7dC3vc7W8txT'+\
'F3qixj2rs+7S8b9Ly3lYUe4vGvl9jn9DYhzV2pyj2nRp7rVbrGjTN\nb9c031'+\
'sUe53GvlvL+6iW93Va3geLYh/Q2Cu0vM/V8t6i5X2oKPZhjX2+xr5MY9+psY'+\
'8UxT5XYx/S\nNL9L0/w8fXRRFHubxn5YY5/U2Pdr7ONFse/S2Os0zTdqmh/RN'+\
'D9RFHuNxr5Ty/uIlvc6vX8vin2H\nxl6j5X2+lvdeLe/sR8WwOxr7MS3vTGMv'+\
'09grimLv19jLtbxXa+zNev9eFLulsU9qeT+hj6i1cq8r\nin2+xj6ise/R2Fv'+\
'1/r0o9qTGfkRjP6axT2jsLUWxN2nsYxr7uMbep/fvRbEPauyVWq2r0WrdOq3'+\
'W\nOUWxb9PYqzX2eRp7p96/F8Xep7FP19grNfZlGvtgUeyexn5cK/cyjb1C79'+\
'+LYl+rsR/U2I/o+yD6\n6kFR7PM09mGNfbfG3qj370WxD2ns87Ryr9M0P6Bpf'+\
'rwo9lqNfZeW95e0vK/S5+9FsU/X2Ac09u0a\n+5GS94e9WmPfobEPa+zV71Pe'+\
'KzX27Rr7To29XB/bFMW+XWOfq9W6Wq3WefrY5q1i2Ndp7BNa3o9q\neR8rLdy'+\
'B2lV65h2obdoOVL++A/XWh7cDVXsWO1B9Z7EDNXgWO1CHS89iB+rDy3tD05n'+\
'ztaSh5Mw7\nUCPTTrMDVZiv/1TNHNP2Rlu1mtmm1cw2zSLVFMW+V2Nfq7En9T'+\
'U9jb2uKPZ9Gvs6jb1TY+/X2JuK\nYt+jsa/S2Ndq7M0ae0tR7C9p7Cs19laNf'+\
'ZnG3lYU+6jG3qKxr9PYW7Qd+WNnYQ9bNXu4UrOHzodo\nD9lZ2MPms7CHLWdh'+\
'D88vO7M9/BDz3mCdxY5821nsyI+HO/IXTPlm2l2VQb5O/a7jfZBp+fvC98ci'+\
'\nbTxd8oFpwy+dqrLTn9tj0htub5/6HbzQ9r4dO+O5Pf/XaU54dg5SDSFXmcZ'+\
'Ff92V0dlHQoGPAwne\nNaKTK5xcOuulxCpNsAf9tcrobV7/vWUgjT4XnaQhzs'+\
'8Uu6X+2TU52u9uU+IZrYxyIZB/BBLMLwTy\nM5KJyVzvAbGiFFp2lo55aVJij'+\
's0Uv9aJ4pkJZFUUil6/ztr+jmoQis7j2RWTQy2ZKQ4kOnkyQFbP\nFO8pR0jn'+\
'THHSUYT0AZlQ4nkcSJuisb+cGfUFAnluZvT+oUBenilOq/HT7OQ9N9yTCtL8'+\
'A8jsULgO\nAulRkCNAtinIsZnRCEQg02cxNl/RfBWQ4F0aKlPQJ4Kd0PBdCMh'+\
'sV2K+cVZ0CpZA7gSyV5FZO6uw\n1v3+rEI9f2mWONMpCvUkkLUK8vKsaCRDb7'+\
'CL89gGFD1/HzI7Ix2mkvxYudFnwprJ/cG7auJNDPF1\njpHxCElalmHw+KIUH'+\
'pwlSCQ9+/kSMkaqO0eHFk4qGvsPyHhKLn6nSpxlFiGXVvHY2iKu+VXBPC48\n'+\
'bwfIiBLPrVWFOlxbFY21/LoK5JgSqruKb/AG+smYmYSzwV8XDbj6qsQZXFGo'+\
'J6rkEqRQ9OuBwTCU\nKY7XKijlFxGqTNHYWFVk6wTyI0qzYhMOEfK2nItJIOU'+\
'lUZnyb6X4b4Zwdt/SNiuhTlaJ37+XBvWZ\nW7aWH0WlHKdDgONRGzQs1zTXB2'+\
'/PBnbMsy1/hy7Qz/nVGFUqNqoKyB5Fz/OAVCh5X1RdmK9bqsUv\nKSKZu4G0S'+\
'LVXVNaWqGbysyyD3ZMgPanqaBYpkA1AJhXkYSCVSnoeqxa3Uf0ZphQqMrurx'+\
'W/W/PTk\nTK6yXqW2vAGZowrXj6oLLeQ/AZleIlnjbNJvX77muZ6T/ppV2IN0'+\
'5vz9wYDr3xBPq8J14ezgDaVA\nZi6Qg4rM1bPpN85BeRkZngn//Zawfc1WezR'+\
'x4mWvwt4MmTGpr+QHd/mru4HMGsgcV9jjQHZLZSrq\nWJ0Ssz07ehPVP+9iNj'+\
'+jQNLhY7NFXY6QvwQyVymvbwJ5SYnnO0BqFZkfAKlWkH+cHewGcs2LI2v9\nF'+\
'bwghf8EmSalnZbMESeOBf1y0uxxghXXINTFkBlVNIbWZEVvWvK+dU6wbhP8C'+\
'inRnfTf4hbndNGn\nj4I9+iDUfITap+R02ZxgXy/8BegcUb98+ywZqagNfnYO'+\
'K7DzFpATSswbgexXckFVc3JctRJ5a0hh\nf3hONJfxrajPFSHPzglWiUVOkXk'+\
'3eAMniOcVLYU/VhBit2AmJhXN/2KOOBuzJGy5yfDt9BrfhtMx\nuixiF6dn+r'+\
'tUQTy/mRPNoAVy7iXitL5glMLNqv/2SPh7RsgMKXmff0k0G/VHDpcUloVxiT'+\
'iVwo/5\nAZfXwwol5jxkjigx9wEZjtIjGq7/JnwQ6vFLxHl5QmYnfEazZd0VT'+\
'2eX39O6xovnvLzTVL+IzoTL\nuV5wkij/WW/oEaOC8N423Put+w06qJiRTxz9'+\
'S3ftdj6bdI1Ep5lYz+g4Yn5SsonxOf/xp5VuFwfr\n8uOUvW5bnAEtHq43N3T'+\
'buSR8iXzOoH4tPN/YCI9zNqIDlDlIdxzGfcZO5jK4JUrDzhl0IiL9utaL\nt0'+\
'cxpeKuxwX48cKGdJyzoRzhLI5hdPMI6hh2KkWdvsBydI5vvp2OHBK5jeKmxx'+\
'wMQyhnRAsB20qK\nk3iN6GxoQznK2lDOvDaU47AN+ZBoqv8uFaHQoG/dpfuNw'+\
'gMxOtTISG7IxnO5+AYipZIkXQaB6J4m\nM6IeUAXolnJGD0KffxP0iRHgeDkR'+\
'tXLaN/89PIrTzGWJZVGQJjrJuOCZ6FnintHlt63AH3inOPHY\nUM8bR81BNba'+\
'64lbeFPWMJ5Kftcy96aSZJbF4u2WGnkCMGZ1xtzOA6fe5US65D4nx77oT0T2'+\
'PnN/x\n+SA/TJqqtg/SwYD1/nl8GL8t8rUNJS2KUH7KaNwyxEFfRodlt2s+nq'+\
'50Km3m/CDh6dFGdFY1cuNB\n1kpnTb9pOeh3oTfL7g4etm/w6GFnPJuEFky7P'+\
'bxHeuMbVB+SLo7ppijpGOwM147ACryOE5yPbRQe\nFW5oB36j8iVyNlUbMtP6'+\
'CeHBqeu+VgNfWCIBwOuc5Fmk+PgJlMFR3fyoa79CC8gNn/m6tuLtpsVL\nJ7g'+\
'XuvbLQECKLP0GWpxsFOU5UIiIm9pIHF0n6g+MY3hkOSkp3pGJC1k2RXA6x9s'+\
'V2fFvBW66ibgT\nnkVuREfyG8pR8BQQ5gMV0DfpWZvrPFB9PNdBxowaPKxkxs'+\
'56nQZfnvSf82dCgRJAB1bRT6YRbQpV\n0cxSW0pKxenPLzwChSiVfVIub7Tnw'+\
'AyKg9FRrEhkPGv7loD/2luAwkBA90GjoOchKEnLz6UD/I3w\n1HyDVp0iy5S1'+\
'E3bSNLrjWZ7U8KsAqNVZ1yvEkRLHThNkuOmNJhP9HD8XPp5Lu2QA+eMcz5ir'+\
'WvV6\n1azX0xRniq8gCCF+x09hF0QBrVBYZn1ABDW6gt9LkzkTBlHF/LTIZ7q'+\
'LrtN10x0Bl6g0cQ/VqT3v\n9yz5hCcOe/Kftgt2x3aDkuNxChFhcIMSFT1pPB'+\
'fPcCQZ1lpqI340HBD3ovD44ZtcH4oeWcFYgOIW\nVdQvbX5+WND8MJMSt24+E'+\
'9yJdsHvaWUuvDMf8O/p6wrirscOorIAimoQAOhkFH8UygpDiQTzg+L8\ne0FG'+\
'4eplDy8lbj3UFiKaFBkW6sXIKmUpI1yhvkXCA3HHuwvFHFFZ4D8q2Lhn81aW'+\
'9qiP7YpuN/pi\n5E/HLdSvnI4EvWHhEKfdddV+Xfr2Q3CfoL4nqMqERWO4dJZ'+\
'nKQBdpZMQ40npSwuKJzR1+ncXjKm+\nYcDbPtV33oD4oKA9jSkG6n0GVDRyoh'+\
'WxOoMsgA+LOsnthLhF15rjxUyJp8ILxprJtOsE95ZZv1SE\ntx2KTByCLIo5F'+\
'yc7h5Ep77R9GsoRGpkkgQfC0opYfFLKAa8VCxeJgNw2cAYeDao/t/HikadUC'+\
'NFC\n6Amvc+LowsgvGkroxeiUrF7gD5TkST4aD/Ko6wv8wss7VO5HXvJuOFqs'+\
'V3yympPpHIGYh4k6rbZy\n/kkO1zUzfJSWFaZehTUhi3e0fOwZqXYKzYad6Kk'+\
'wbiPDeuIr2B+BCYQPW62UkKQbGjZSifFjSH1f\nKETdEU9W6Cv4PogxxQdC+N'+\
'AlDBDEJQ4A5160+XaqOMr8hoPogJVGykEjF3kkHNWAJpvE4rLwEyN8\nWCd6Y'+\
'hkVXprzy5zRYw3JUf2gNh7H0I6mH5l0wgfB32F74UxJKA5I9AjDSqq04RMOp'+\
'Kmx8skJn9kx\n/wswsG1iahMO6oKPugSfwTGiL8Fk18PCCVW7ovh4DXP88bT4'+\
'Wkp7WrSZwu+y+B/Jod0rMaklr91+\nP/LuC/ChEZ+ths/jVjyBeZopQxgO8to'+\
'fIvRtpchnJd1ELu14/FwpaJY3aVecX+WPBE1Rq9IZh898\nsu3BIVnRTA/Dat'+\
'JuNPNzXV5//A8Bwdp3ZLm3S3wPTkL4nVSRME6iVX6D997iE0MBM7yilATgSg'+\
'gs\nSAESVGEzGILExRfr/MyJQVVYOjRqIeOdyCS5R/1EkaF9xcgo+PqRoX5Hx'+\
'8j5k0lhLJTP6qBLTidp\n0YLPDYOehn/Px5jyW0PGqT4cZMjfKSo0X0mppKWP'+\
'EBlTfa0nOGGfckwtL/iyj1H4GR8O+1LKN4C4\nrz3umqJHQPbFCoWYNWfcDnV'+\
'iUB+M4r1u28VQzPH7LH9xRerUoEUb9UHuVfiYa8oPLikK0WT47C/8\nVpQhf2'+\
'/LCD8KZURfhQpWsPi6FV+Q8q1zku8FK5DYHpbGNkm+UiUO6AnqImpGevGypU'+\
'GlCaoERlDy\nQT4LaFizEOLdixdhrGyjo8BoLd1DhASRvswkTX9QDvG85dG5v'+\
'vybCZy0e1FgJjLo/XsW1vlYNmHy\n1YH7Menky2DU3ZOPP1kcxG52+gRSXnTm'+\
'0z3jlqAQ7CAwPBqAnsfdBP8Nt/ihdjJrU8HTr8rFOJq2\nMABZG7me013JNE9'+\
'inn5QbieTaR4uXCDk+ifknntXt95x1wqjZc2Ke5vvNu5Zseru5caqO9a0GgY'+\
'e\nw24YYqXW8KdotKzFHxnNrXffE0kWJB8tKwNDTU1UROJvpxjhx8t83N8ONa'+\
'jOiY9oGnGkkDcKIXEb\nbOktKNVbmhoCyF9S4oNI9FRimM37xrRInPqAjG0Ol'+\
'ZSeZOL32zk+9tjgemaGtmxdWiMLc8tHayYa\nVJcY6QWfTTNuSUrJgDlc73rr'+\
'g0CIt52vj4qyEpiTELZCeP1sikf0WU/jdtO7y07mLXMlX9SR8uev\n3vtasa0'+\
'k6aNQLzCLAQEf/oclI/TKN8tPW8ArVjcryuo0446sRMEiXlPwfeq3TJuWsSk'+\
'QP5ybDRYH\nBcDfHTDoQxLQv+1OoXi+DWVQMpJybeDP4x0mt5ZC3FU06y+AB6'+\
'udvH+ktS+SlT/FGuk32GkIdFXI\nHGqcnVUDEdsCfgsRG4mFDQLAcqW9iHIOV'+\
'UQl6IeUvuoXpI9vwkR1g3YhjSkj9LeqotKiGrsaWblF\n2GS/sqKfE98hkxRC'+\
'G4cSBY1WpLFIoE8hIHrwUNhPkIjJn6H6DW2qgg7XCcNU6s1AT6LYzTPkTyUW'+\
'\n2iC/4ivVzn8xIHjoL8UKX+BRGoBsLCIzYUjZtaKG7G/8y83WkrVIOuUGxdd'+\
'YgZWU+yHJ+sjqFRvu\nilXyH/C1V7mZCY2LtiIrnYZmGFjz0WmUEVVNYkfT9y'+\
'iWLmgUGJtnTYt6WIBdMi1v0VNbVPFMS5L0\n6cupzPvUjdZ/KYZNUa3PbOOUD'+\
'Kh21H99K6TpKrRc/ls0/wcmnlFE\n'




# Drop libtcc.dll
if not os.path.exists (TCC_DLL_PATH):
    
    print "----  Dropping libtcc.dll to  ----", repr (TCC_DLL_PATH)
    binary_hash = '>Al\xde\x7fzM\xd1=\x8e\xd4\x01\xed\n\xdf\xce'
    new_hash = md5 (____binary).digest ()
    assert (new_hash == binary_hash), "Cannot create libtcc.dll. Binary data has been corrupted."    
    libtcc_binary = ____binary.decode ("base64")
    libtcc_binary = decompress (libtcc_binary)

    try:
        f = open (TCC_DLL_PATH, "wb")
        f.write (libtcc_binary)
        f.close ()
        del libtcc_binary, binary_hash, new_hash
    except Exception, error:
        try:    f.close ()
        except:    pass
        raise error



del ____binary




tcc = cdll.LoadLibrary (TCC_DLL_PATH)
tcc.__del__ = tcc.free = lambda *args: FreeLibrary (tcc._handle)






__all__ = ["pycast", "tcc", "pytcc"]
#cad.


if __name__ == "__main__":

    c_code = "int c_function (int a, int b) {return a + b;}"
    print "c_code: %s" % repr (c_code)
    context = pytcc ()
    print "C compiler context created: %s" % context
    context (c_code)
    print "c_code compiled."
    c_function = context.get_function ("c_function", argtypes=[c_int, c_int])
    print "Prototyped C function: %s" % c_function    
    print "Calling C function: 123 + 321 = %s." % c_function (123, 321)