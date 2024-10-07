import sympy as sp

def secant_method_verbose(f, x0, x1, tol=1e-6, max_iter=100):
    x = sp.symbols('x')  # Symbol for variable in the equation
    f_expr = sp.sympify(f)  # Convert input function to sympy expression
    f_lambdified = sp.lambdify(x, f_expr)  # Lambdify the expression for numeric evaluation

    print(f"{'Iteration':<10}{'x_n':<20}{'f(x_n)':<20}{'Error':<20}")
    for i in range(max_iter):
        # Evaluate the function at the current points
        f_x0 = f_lambdified(x0)
        f_x1 = f_lambdified(x1)
        
        if abs(f_x1) < tol:
            print(f"{i:<10}{x1:<20}{f_x1:<20}{0.0:<20}")
            return x1, i  # If f(x1) is sufficiently close to zero, we've found a solution
        
        # Update x using the secant formula
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        error = abs(x2 - x1)
        
        # Print iteration data
        print(f"{i:<10}{x1:<20}{f_x1:<20}{error:<20}")
        
        # Check if the update is within tolerance
        if error < tol:
            return x2, i
        
        # Move to the next points
        x0, x1 = x1, x2
    
    raise ValueError("Secant method did not converge")


def get_user_input():
    f = input("Enter the function f(x): ")
    
    x0 = float(input("Enter the first initial guess (x0): "))
    x1 = float(input("Enter the second initial guess (x1): "))
    
    tol = float(input("Enter the tolerance (default 1e-6): ") or "1e-6")
    max_iter = int(input("Enter the maximum iterations (default 100): ") or "100")
    
    return f, x0, x1, tol, max_iter

if __name__ == "__main__":
    f, x0, x1, tol, max_iter = get_user_input()

    try:
        root, iterations = secant_method(f, x0, x1, tol, max_iter)
        print(f"Root: {root}, found in {iterations} iterations")
    except ValueError as e:
        print(e)
