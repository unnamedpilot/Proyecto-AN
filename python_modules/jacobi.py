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

# Método de Jacobi adaptado
def jacobi_method(matrix_a, vector_b, x0, tol, niter):
    A = np.array(matrix_a)
    b = np.array(vector_b).reshape((-1, 1))
    x0 = np.array(x0).reshape((-1, 1))

    D = np.diag(np.diag(A))
    L = -1 * np.tril(A) + D
    U = -1 * np.triu(A) + D
    T = np.linalg.inv(D) @ (L + U)
    C = np.linalg.inv(D) @ b

    spectral_radius = max(abs(np.linalg.eigvals(T)))
    converges = spectral_radius < 1

    iterations = []
    xP = x0
    for i in range(niter):
        xA = T @ xP + C
        error = np.linalg.norm(xP - xA)
        xP = xA

        iterations.append({"step": i + 1, "x": xA.flatten().tolist(), "error": error})
        if error < tol:
            break

    return {
        "transition_matrix": T.tolist(),
        "coefficient_matrix": C.tolist(),
        "spectral_radius": spectral_radius,
        "iterations": iterations,
        "converges": converges,
    }

if __name__ == "__main__":
    try:
        filas = int(input("Ingrese el número de filas de la matriz A: "))
        columnas = int(input("Ingrese el número de columnas de la matriz A: "))

        matriz_a = solicitar_matriz("Ingrese la matriz A (cada fila debe tener valores separados por espacio):", filas, columnas)
        vector_b = solicitar_vector("Ingrese el vector b:", filas)
        x0 = solicitar_vector("Ingrese el vector inicial x0:", filas)
        tol = float(input("Ingrese la tolerancia: "))
        niter = int(input("Ingrese el número máximo de iteraciones: "))

        resultado = jacobi_method(matriz_a, vector_b, x0, tol, niter)

        # Mostrar los resultados
        print("\nResultados del Método de Jacobi:")
        print(f"Transition Matrix: {resultado['transition_matrix']}")
        print(f"Coefficient Matrix: {resultado['coefficient_matrix']}")
        print(f"Spectral Radius: {resultado['spectral_radius']}")
        print(f"Converges: {'Yes' if resultado['converges'] else 'No'}")
        print("\nIteraciones:")
        for iteracion in resultado["iterations"]:
            print(f"Paso {iteracion['step']}: x = {iteracion['x']}, error = {iteracion['error']}")

    except ValueError as e:
        print(f"Error: {e}")