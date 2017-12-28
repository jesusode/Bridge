import pytcc

program='''
/* Hello World program */

#include<stdio.h>

main()
{
    printf("Hello World");
    system("pause");

}
'''

# tcc=pytcc.TCCState(output_type=pytcc.TCC_OUTPUT_EXE)
# tcc.compile_string(program)
# tcc.set_options(" -v ")
# print 'aqui si'
# tcc.output_file("holaholita.exe")
# print 'aqui'
# tcc=pytcc.TCCState()
# tcc.set_options(" -v ")
# tcc.compile_string(program)
# print 'aqui si'
# tcc.run()
# print 'Terminado'
# print 'aqui'
tcc=pytcc.TCCState(output_type=pytcc.TCC_OUTPUT_EXE)
tcc.set_options(" -v ")
tcc.add_file("hello.c")
print 'aqui si'
tcc.output_file("holaholita.exe")
print 'Terminado'