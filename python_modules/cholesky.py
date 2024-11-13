import numpy as np


# Función para pedir datos
def solicitar_matriz(mensaje, filas, columnas):
    print(mensaje)
    matriz = []
    for i in range(filas):
        fila = list(map(float, input(f"Fila {i + 1}: ").split()))
        if len(fila) != columnas:
            raise ValueError(f"La fila debe tener {columnas} valores.")
        matriz.append(fila)
    return matriz


def solicitar_vector(mensaje, tamanio):
    print(mensaje)
    vector = list(map(float, input(f"Ingrese {tamanio} valores separados por espacio: ").split()))
    if len(vector) != tamanio:
        raise ValueError(f"Debe tener {tamanio} valores.")
    return vector


# Método de descomposición de Cholesky manual (basado en pseudocódigo)
def cholesky_method(matrix_a, vector_b):
    A = np.array(matrix_a, dtype=np.complex128)
    b = np.array(vector_b).reshape((-1, 1))

    # Verificar que A sea una matriz simétrica
    if not np.allclose(A, A.T):
        print(
            "Advertencia: La matriz A no es simétrica. La factorización de Cholesky puede no funcionar correctamente.")

    # Descomposición de Cholesky manual
    n = A.shape[0]
    L = np.zeros((n, n), dtype=np.complex128)
    U = np.zeros((n, n), dtype=np.complex128)
    etapas = []

    for k in range(n):
        # Calcular L[k][k]
        sum1 = sum(L[k][p] * U[p][k] for p in range(k))
        L[k][k] = np.sqrt(A[k][k] - sum1)
        U[k][k] = L[k][k]

        # Calcular L[i][k] para i > k
        for i in range(k + 1, n):
            sum2 = sum(L[i][r] * U[r][k] for r in range(k))
            L[i][k] = (A[i][k] - sum2) / U[k][k]

        # Calcular U[k][j] para j > k
        for j in range(k + 1, n):
            sum3 = sum(L[k][s] * U[s][j] for s in range(k))
            U[k][j] = (A[k][j] - sum3) / L[k][k]

        # Guardar la etapa actual
        etapas.append({
            "etapa": k + 1,
            "L": L.copy(),
            "U": U.copy()
        })

    # Resolviendo Ly = b (sustitución progresiva)
    y = np.zeros_like(b, dtype=np.complex128)
    for i in range(n):
        y[i] = (b[i] - sum(L[i][j] * y[j] for j in range(i))) / L[i][i]

    # Resolviendo Ux = y (sustitución regresiva)
    x = np.zeros_like(b, dtype=np.complex128)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

    return {
        "solution": x.flatten().tolist(),
        "lower_triangular_matrix": L.tolist(),
        "upper_triangular_matrix": U.tolist(),
        "stages": etapas
    }


def format_matrix(matrix):
    formatted = []
    for row in matrix:
        formatted_row = [f"{elem.real:.6f}" if elem.imag == 0 else f"{elem:.6f}" for elem in row]
        formatted.append("  ".join(formatted_row))
    return "\n".join(formatted)


if __name__ == "__main__":
    try:
        filas = int(input("Ingrese el número de filas de la matriz A: "))
        columnas = int(input("Ingrese el número de columnas de la matriz A: "))

        if filas != columnas:
            raise ValueError("La matriz A debe ser cuadrada para aplicar Cholesky.")

        matriz_a = solicitar_matriz("Ingrese la matriz A (cada fila debe tener valores separados por espacio):", filas,
                                    columnas)
        vector_b = solicitar_vector("Ingrese el vector b:", filas)

        resultado = cholesky_method(matriz_a, vector_b)

        # Mostrar los resultados
        print("\nResultados del Método de Cholesky:")
        for etapa in resultado["stages"]:
            print(f"\nEtapa {etapa['etapa']}:")
            print(f"L:\n{format_matrix(etapa['L'])}")
            print(f"U:\n{format_matrix(etapa['U'])}")
        print(f"\nSolución final: {resultado['solution']}")

    except ValueError as e:
        print(f"Error: {e}")