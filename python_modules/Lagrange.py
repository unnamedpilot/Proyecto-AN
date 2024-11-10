import sympy as sp

#Ingresar cada uno de los puntos 
def ingresar_puntos():
    #Solicitar el número de puntos
    n = int(input("Ingresa el número de puntos: "))
    
    #Inicializar las listas vacias para almacenar los valores de "x" y "y"
    x_valor = []
    y_valor = []
    
    #Solicitar al usuario que ingrese los valores de cada punto de la matriz
    print("Ingrece los valores de la matriz (x, y) punto por punto: ")
    for i in range(n):
        x = float(input(f"x[{i}]: "))
        y = float(input(f"y[{i}]: "))
        x_valor.append(x)
        y_valor.append(y)
    
    return x_valor, y_valor

#Función para calcular el polinomio de Lagrange
def polinomio_lagrange(x_valor, y_valor):

    x = sp.Symbol('x')
    
    #Inicializa el polinomio en 0
    polinomio = 0
    n = len(x_valor)
    
    #Iteracion a través de todos los puntos para construir los polinomios de Lagrange
    for i in range(n):
        L_i = 1
        
        #Calcular el término L_i para cada valor de i
        for j in range(n):
            if i != j:
                L_i *= (x - x_valor[j]) / (x_valor[i] - x_valor[j])
        
        #Suma el término correspondiente al polinomio
        polinomio += y_valor[i] * L_i
    
    #Simplificacion de polinimio
    polinomio = sp.simplify(polinomio)
    
    return polinomio

# Función main
if __name__ == "__main__":
    #Obtenemos los puntos ingresados por el usuario
    x_valor, y_valor = ingresar_puntos()
    
    #Calcular el polinomio de Lagrange
    polinomio = polinomio_lagrange(x_valor, y_valor)
    
    #Mostrar el polinomio resultante
    print("\nEl polinomio de Lagrange es: ")
    print(polinomio)

    #Modificar el polinimio resultante para una mejor salida
    sp.pprint(polinomio, use_unicode=True)
