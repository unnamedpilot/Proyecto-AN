import sympy as sp

#Ingresar cada uno de los puntos
def ingresar_puntos():
    #Solicitar el numero de puntos
    n = int(input("Ingresa el número de puntos: "))
    
    #Inicializar las listas vacias para almacenar los valores de "x" y "y"
    x_valor = []
    y_valor = []
    
    #Solicitar al usuario que ingrese los valores de cada punto de la matriz
    print("Ingresa los valores de la matriz (x, y) punto por punto: ")
    for i in range(n):
        x = float(input(f"x[{i}]: "))
        y = float(input(f"y[{i}]: "))
        x_valor.append(x)
        y_valor.append(y)
    
    return x_valor, y_valor

#Función para calcular el polinomio de Newton
def polinomio_newton(x_valor, y_valor):

    x = sp.Symbol('x')
    
    #Calcular las diferencias divididas
    n = len(x_valor)
    diferencias_divididas = [[0 for _ in range(n)] for _ in range(n)]
    
    #Inicializar la primera columna con los valores de y
    for i in range(n):
        diferencias_divididas[i][0] = y_valor[i]
    
    #Calcular las diferencias divididas
    for j in range(1, n):
        for i in range(n - j):
            denominador = (x_valor[i + j] - x_valor[i])
            if denominador == 0:
                raise ValueError(f"División por cero al calcular las diferencias divididas: x[{i + j}] y x[{i}] son iguales")
            diferencias_divididas[i][j] = (diferencias_divididas[i + 1][j - 1] - diferencias_divididas[i][j - 1]) / denominador
    
    #Polinomio de Newton
    polinomio = diferencias_divididas[0][0]
    termino = 1
    for i in range(1, n):
        termino *= (x - x_valor[i - 1])
        polinomio += diferencias_divididas[0][i] * termino
    
    #Simplificar el polinomio
    polinomio = sp.simplify(polinomio)
    
    return polinomio

#Función main
if __name__ == "__main__":
    try:
        #Obtenemos los puntos ingresados por el usuario
        x_valor, y_valor = ingresar_puntos()
        
        #Calcular el polinomio de Newton
        polinomio = polinomio_newton(x_valor, y_valor)
        
        #Mostrar el polinomio resultante
        print("\nEl polinomio de Newton es: ")
        polinomio_str = str(polinomio).replace('**', '^')
        print(polinomio_str)
    except ValueError as e:
        print(f"Error: {e}")
