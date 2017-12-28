from pyAsm import *

p = pyAsm(A_32BIT)      #We can alse use A_64BIT and A_16BIT!
p.update('xor eax,eax') #update the executed code
p.update('mov eax,1')
p.update('shl eax,10')

r = p.run()

print 'EAX is:',r.Eax