import numpy as np

def doolittle(A,b):
    n = A.shape[0]
    L = np.eye(n)  
    U = np.zeros_like(A)

    for i in range(n):
        for j in range(i, n):
            U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
        for j in range(i + 1, n):
            L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]

    print("Matriz L (Doolittle):")
    print(L)
    print("\nMatriz U (Doolittle):")
    print(U)

    y = sustitucion_progresiva(L, b)


    x = sustitucion_regresiva(U, y)
    print("\nSolución final x (Doolittle):")
    print(x)

    return L, U

def sustitucion_progresiva(L, b):
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - sum(L[i][j] * y[j] for j in range(i))) / L[i][i] 
    return y

def sustitucion_regresiva(U, y):
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x


A = np.array([[4, -1, 0, 3], [1, 15.5, 3, 8], [0, -1.3, -4, 1.1], [14, 5, -2, 30]])
b = np.array([1, 1, 1, 1])

L, U = doolittle(A,b)

