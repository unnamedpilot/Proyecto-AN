import numpy as np

def splineLineal(x, y):
    trazadores = []
    n = len(x)
    
    for i in range(n - 1):
     
        m = (y[i + 1] - y[i]) / (x[i + 1] - x[i]) 
        b = y[i] - m * x[i] 
        trazadores.append(f"{m:.6f}x + {b:.6f}")
    
    return trazadores


x = np.array([-1, 0, 3, 4])
y = np.array([15.5, 3, 8, 1])


trazadores = splineLineal(x, y)


print("Trazadores:")
for trazador in trazadores:
    print(trazador)
