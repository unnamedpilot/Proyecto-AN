import numpy as np



def obtener_polinomio(x, y):
    # Resolvemos el sistema V * a = y
    vandermonde = np.vander(x, increasing=True)
    coeficientes = np.linalg.solve(vandermonde, y)
    print(vandermonde)
    polinomio = " + ".join([f"{coef:.6f}x^{len(coeficientes)-i-1}" if len(coeficientes)-i-1 > 0 else f"{coef:.6f}" 
                       for i, coef in enumerate(coeficientes)])
    
    print("\nPolinomio:")
    print(polinomio)
    return coeficientes

# Datos de la tabla
x = np.array([-1, 0, 3, 4])
y = np.array([15.5, 3, 8, 1])



# Obtener los coeficientes del polinomio
coeficientes = obtener_polinomio(x, y)




