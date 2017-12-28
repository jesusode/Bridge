def invert(A):    
    ''' Returns the inverse of A, where  A is a square matrix in the form of a nested list of lists. '''
    A = [A[i]+[int(i==j) for j in range(len(A))] for i in range(len(A))]  	
    for i in range(len(A)):
        A[i:] = sorted(A[i:], key=lambda r: -abs(r[i]))
        A[i] = [A[i][j]/A[i][i] for j in range(len(A)*2)]
        A = [[A[j][k] if i==j else A[j][k]-A[i][k]*A[j][i] for k in range(len(A)*2)] for j in range(len(A))]
    return [A[i][-len(A):] for i in range(len(A))]