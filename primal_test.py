def isPrime(n, k=5): # miller-rabin
    from random import randint
    if n < 2: return False
    for p in [2,3,5,7,11,13,17,19,23,29]:
        if n % p == 0: return n == p
    s, d = 0, n-1
    #print "s: %s"%s
    #print "d: %s"%d
    while d % 2 == 0:
        s, d = s+1, d/2
        #print "s: %s"%s
        #print "d: %s"%d
    #print 'llego al for'
    #print "s: %s"%s
    #print "d: %s"%d
    for i in range(k):
        x = pow(randint(2, n-1), d, n)
        print "Valor de x: %s" %x
        print "Valor de n: %s" %n;
        if x == 1 or x == n-1: continue
        for r in range(1, s):
            x = (x * x) % n
            if x == 1: return False
            if x == n-1: break
        else: return False
    return True

print isPrime(31)
#print isPrime(982451653)
c=[ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 37,53, 61,73, 79, 83,
 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,181, 191,
 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307,
 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431,
 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]
#for num in c:
#    print "Num: %s es primo: %s"%(num,isPrime(num))