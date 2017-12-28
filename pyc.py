"""
Inserts C code directly into Python files, which can then be dynamically linked
in and called via ctypes.
"""
import atexit
import ctypes
import os
#import shlex
import sys
import tempfile

# try:
    # COMPILER = os.environ['CC']
# except KeyError:
    # print('CC environment variable must point to C compiler', file=sys.stderr)
    # sys.exit(1)


COMPILER="..\\..\\tcc\\tcc.exe"

# This is the C compiler command line, which is used to generate object files.
CMDLINE_C_TO_OBJ = '{compiler} -c -o {output} {input}'

# This is the C compiler command line, which is used to generate C shared
# libraries.
CMDLINE_OBJ_TO_SO = '{compiler} -shared -o {output} {input} {libraries}'

class C:
    r"""
    Compiles and loads C code into a Python program, optionally linking in other
    shared libraries along with the loaded code.

    >>> hello_world = C('''
    ... #include <stdio.h>
    ... 
    ... void say_hello() {
    ...     printf("Hello, World\n");
    ... }
    ... ''')
    ...
    >>> hello_world['say_hello']()
    Hello, World
    """
    def __init__(self, code, *shared_libs):
        self.library = None
        self._compile(code, shared_libs)

    def _compile(self, code, libs):
        """
        Compiles a hunk of C code into a shared library, and links it into the
        current program. Note that all libraries given (they are assumed to be
        shared libraries) are also linked into the shared library, and thus
        loaded into the current program as well.
        """
        # Dump the C code into a temporary file, and run the compiler to make
        # an object file
        # with tempfile.NamedTemporaryFile(mode='w', prefix='PYC', suffix='.c', 
                # delete=False) as temp_c_file:
            # temp_c_file_name = temp_c_file.name

            # temp_c_file.write(code)
            # temp_c_file.flush()
        temp_c_file_name="pyc_temporal.c"
        temp_c_file=open("pyc_temporal.c","w")
        temp_c_file.write(code)
        temp_c_file.close()

        obj_file_name="pyc_temporal.o"

        #obj_file_name = tempfile.mktemp(prefix='PYC', suffix='.o')
        cmdline=CMDLINE_C_TO_OBJ.format(compiler=COMPILER, 
            output=obj_file_name, 
            input=temp_c_file_name)
        #print 'cmdline: %s' % cmdline
        os.system(cmdline)
        os.remove(temp_c_file_name)

        # Run the compiler one more time to generate a shared library
        #so_file_name = tempfile.mktemp(prefix='PYC', suffix='.so')
        so_file_name="pyc_temporal.dll"
        library_cmd = ' '.join('-l' + lib for lib in libs)
        cmdline2=CMDLINE_OBJ_TO_SO.format(compiler=COMPILER,
            output=so_file_name,
            input=obj_file_name,
            libraries=library_cmd)
        #print 'cmdline2: %s' % cmdline2
        os.system(cmdline2)
        os.remove(obj_file_name)

        # Punt to ctypes so that we can get a loadable library from whatever
        # we just built
        self.library = ctypes.cdll.LoadLibrary(so_file_name)
        
        # Ensure that we clean up the temp files when the program is exiting
        #atexit.register(lambda: os.remove(so_file_name))
            
    def __getitem__(self, func):
        if self.library is None:
            assert False, "How did C.__getitem__ get called without loading the library?"

        return getattr(self.library, func)

if __name__ == '__main__':  
    my_lib = C('''
#include <windows.h>

#define DLL_EXPORT __declspec(dllexport)


DLL_EXPORT void message (void)
{
	MessageBox (0, "Hello World!", "From DLL", MB_ICONINFORMATION);
}
DLL_EXPORT int factorial(int x)
{
    int result = 1;
    while (x > 1)
    {
        result *= x;
        x--;
    }

    return result;
}
''')

    factorial_func = my_lib['factorial']
    print('5! =', factorial_func(5))
    print('4! =', factorial_func(4))
    saludar=my_lib["message"]
    saludar()
