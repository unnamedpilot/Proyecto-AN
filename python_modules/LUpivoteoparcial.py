import numpy as np

def lu_pivoteo(A):
    n = A.shape[0]
    P = np.eye(n)  # Matriz de permutación
    L = np.zeros_like(A)
    U = A.copy()

    for i in range(n):

        max_index = np.argmax(np.abs(U[i:, i])) + i
        if max_index != i:
          
            U[[i, max_index], :] = U[[max_index, i], :]
            P[[i, max_index], :] = P[[max_index, i], :]

            L[[i, max_index], :i] = L[[max_index, i], :i]
        
        L[i][i] = 1
        for j in range(i + 1, n):
            L[j][i] = U[j][i] / U[i][i]
            U[j] -= L[j][i] * U[i]
    
    return P, L, U

def sustitucion_progresiva(L, b):
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
    return y

def sustitucion_regresiva(U, y):
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x


A = np.array([[4, -1, 0, 3], [1, 15.5, 3, 8], [0, -1.3, -4, 1.1], [14, 5, -2, 30]])
b = np.array([1, 1, 1, 1])

P, L, U = lu_pivoteo(A)

print("Matriz P (Permutación):")
print(P)
print("\nMatriz L:")
print(L)
print("\nMatriz U:")
print(U)


y = sustitucion_progresiva(L, np.dot(P, b))  # Usar P*b para b permutado


x = sustitucion_regresiva(U, y)
print("\nSolución final x:")
print(x)
