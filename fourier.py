import math
import cmath
import sys
 
def dft(data, inverse=False):
    """Return Discrete Fourier Transform (DFT) of a complex data vector"""
    N = len(data)
    transform = [ 0 ] * N
    for k in range(N):
        for j in range(N):
            angle = 2 * math.pi * k * j / float(N)
            if inverse:
                angle = -angle
            transform[k] += data[j] * cmath.exp(1j * angle)
    if inverse:
        for k in range(N):
            transform[k] /= float(N)
    return transform
 
def fft(data, inverse=False):
    """Return Fast Fourier Transform (FFT) using Danielson-Lanczos Lemma"""
    N = len(data)
    if N == 1:               # transform is trivial
        return [data[0]]
    elif N % 2 == 1:         # N is odd, lemma does not apply
        return dft(data, inverse)
    # perform even-odd decomposition and transform recursively
    even = fft([data[2*j] for j in range(N//2)], inverse)
    odd  = fft([data[2*j+1] for j in range(N//2)], inverse)
    W = cmath.exp(1j * 2 * math.pi / N)
    if inverse:
        W = 1.0 / W
    Wk = 1.0
    transform = [ 0 ] * N
    for k in range(N):
        transform[k] = even[k % (N//2)] + Wk * odd[k % (N//2)]
        Wk *= W
    if inverse:
        for k in range(N):
            transform[k] /= 2.0
    return transform
 
def sine_fft(data, inverse=False):
    """Return Fast Sine Transform of N data values starting with zero."""
    N = len(data)
    if data[0] != 0.0:
        raise Exception("data[0] != 0.0")
    extend_data = [ 0.0 ] * (2*N)
    for j in range(1, N):
        extend_data[j] = data[j]
        extend_data[2*N-j] = -data[j]
    transform = fft(extend_data)
    sineft = [ 0.0 ] * N
    for k in range(N):
        sineft[k] = transform[k].imag / 2.0
        if inverse:
            sineft[k] *= 2.0 / N
    return sineft
 
def cosine_fft(data, inverse=False):
    """Return Fast Cosine Transform of (N+1) data values
       including two boundary points with index 0, N.
    """
    N = len(data)-1
    extend_data = [ 0.0 ] * (2*N)
    extend_data[0] = data[0]
    for j in range(1, N):
        extend_data[j] = data[j]
        extend_data[2*N-j] = data[j]
    extend_data[N] = data[N]
    transform = fft(extend_data)
    cosineft = [ 0.0 ] * (N+1)
    for k in range(N+1):
        cosineft[k] = transform[k].real / 2.0
        if inverse:
            cosineft[k] *= 2.0 / N
    return cosinef