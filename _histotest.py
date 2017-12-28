def _histogram(seq):
    hist = {};
    def f(a):
        if a in hist:
            hist[a]+=1
        else:
            hist[a]=1
    map(f,seq)
    return hist;

print _histogram([1,1,3,4,5,5,5,6,6,8,8,3,3,3,3,3,3,4,5,6,2,9,0,1,2,8,7])

print _histogram(["gato","perro","gato","gato","perro","conejo"])