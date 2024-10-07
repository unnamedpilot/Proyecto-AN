
from sympy import *
def raicesMultiples():

    eqn_ = input("Introduce la ecuación f(x): ")
    eqn1_ = input("Introduce la derivada f'(x): ")
    eqn2_ = input("Introduce la segunda derivada f''(x): ")
    xo = float(input("Introduce el valor inicial xo: "))
    tol = float(input("Introduce la tolerancia: "))

    eqn=sympify(eqn_)
    f = lambda x:eqn.subs({'x':x})
    eqn1=sympify(eqn1_)
    _f = lambda x:eqn1.subs({'x':x})
    eqn2=sympify(eqn2_)
    __f = lambda x:eqn2.subs({'x':x})
    
    niter = 100000
    cont = 0
    err = tol + 1

    while((err > tol) and (niter > cont)):
        fxo = f(xo)
        _fxo = _f(xo)
        __fxo = __f(xo)
        xn = xo - (fxo*_fxo)/((_fxo**2)-(fxo*__fxo))
        err = abs(xn-xo)
        xo = xn
        cont = cont + 1

    if(err <= tol):
        return("se encontró una raíz en: " + str(xo) + " \nen: " +str(cont) + " iteraciones")
    else:
        return("\nEl método no logró converger")
    
resultado = raicesMultiples()
print(resultado)