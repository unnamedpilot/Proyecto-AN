package main

import (
	"fmt"
	"github.com/Knetic/govaluate"
	"math"
)

func iterateNumericMethod(req requestPackage) (float64, error) {
	switch req.TypeOfFunction {
	case "PUN":
		data := req.FunctionData.(FixedPointData)
		result, err := iterateFixedPointMethod(data, req.MaxIterations, req.Tolerance, req.TypeOfError)

		if err != nil {
			return 0, err
		}

		return result, nil
	case "BUS":
		data := req.FunctionData.(SearchData)
		err := iterateSearchMethod(data, req.MaxIterations, req.Tolerance, req.TypeOfError)
		if err != nil {
			return 0, err
		}
		return 0, nil
	case "FAL":
		data := req.FunctionData.(FalsePositionData)
		return iterateFalsePositionMethod(data, req.MaxIterations, req.Tolerance, req.TypeOfError)
	case "NEW":
		data := req.FunctionData.(NewtonData)
		return iterateNewtonMethod(data, req.MaxIterations, req.Tolerance, req.TypeOfError)
	case "BIS":
		data := req.FunctionData.(BisectionData)
		return iterateBisectionMethod(data, req.MaxIterations, req.Tolerance, req.TypeOfError)
	case "SEC":
		data := req.FunctionData.(SecantData)
		return iterateSecantMethod(data, req.MaxIterations, req.Tolerance, req.TypeOfError)
	case "MUL":
		data := req.FunctionData.(MultipleRootsData)
		return iterateMultipleRootsMethod(data, req.MaxIterations, req.Tolerance, req.TypeOfError)
	case "SIM":
		data := req.FunctionData.(GaussianData)
		return iterateSimpleGaussianEliminationMethod(data, req.MaxIterations, req.Tolerance, req.TypeOfError)
	case "PIVP":
		data := req.FunctionData.(GaussianData)
		return iteratePartialPivotMethod(data, req.MaxIterations, req.Tolerance, req.TypeOfError)
	case "PIVF":
		data := req.FunctionData.(GaussianData)
		return iterateFullPivotMethod(data, req.MaxIterations, req.Tolerance, req.TypeOfError)
	default:
		return 0, fmt.Errorf("unknown method")
	}
}

func iterateFixedPointMethod(data FixedPointData, maxIterations int, tolerance float64, typeOfError int) (float64, error) {
	x := data.InitialValue
	var previousX float64

	// Loop over each rearranged function (g(x)) provided
	for _, gFunction := range data.RearrangedFunctions {
		fmt.Printf("\nEvaluating with rearranged function: %s\n", gFunction)

		for i := 0; i < maxIterations; i++ {
			// Calculate the new value x_(i+1) using g(x)
			newX, err := evaluateFunction(gFunction, x)
			if err != nil {
				return 0, err
			}

			// Calculate error based on the difference between x and previousX
			var errorValue float64
			if i > 0 {
				errorValue = calculateError(newX, previousX, typeOfError)
			} else {
				// Ensure at least one iteration
				errorValue = tolerance + 1
			}

			// Evaluate f(x_i) using the original function f(x)
			fx, err := evaluateFunction(data.Function, x)
			if err != nil {
				return 0, err
			}

			// Display iteration info
			fmt.Printf("Iteration %d: x = %.11f, f(x) = %.11f, g(x) = %.11f, Error = %.1f\n", i+1, x, fx, newX, errorValue)

			// Check for convergence
			if errorValue < tolerance {
				fmt.Printf("Converged after %d iterations with g(x) = %s\n", i+1, gFunction)
				return newX, nil
			}

			// Update previousX and x for the next iteration
			previousX = x
			x = newX
		}
	}

	return 0, fmt.Errorf("method did not converge after %d iterations", maxIterations)
}

func iterateFalsePositionMethod(data FalsePositionData, maxIterations int, tolerance float64, typeOfError int) (float64, error) {
	a := data.Interval[0]
	b := data.Interval[1]
	var previousX float64

	for i := 0; i < maxIterations; i++ {
		fa, err := evaluateFunction(data.Function, a)
		if err != nil {
			return 0, err
		}
		fb, err := evaluateFunction(data.Function, b)
		if err != nil {
			return 0, err
		}

		newX := b - (fb*(b-a))/(fb-fa)

		fc, err := evaluateFunction(data.Function, newX)
		if err != nil {
			return 0, err
		}

		var errorValue float64
		if i > 0 {
			errorValue = calculateError(newX, previousX, typeOfError)
		} else {
			errorValue = tolerance + 1
		}

		fmt.Printf("Iteration %d: a = %.11f, b = %.11f, c = %.11f, f(c) = %.11f, Error = %.1f\n", i+1, a, b, newX, fc, errorValue)

		if errorValue < tolerance {
			fmt.Printf("Converged after %d iterations\n", i+1)
			return newX, nil
		}

		if fa*fc < 0 {
			b = newX
		} else {
			a = newX
		}

		previousX = newX
	}

	return 0, fmt.Errorf("method did not converge after %d iterations", maxIterations)
}

func iterateSearchMethod(data SearchData, maxIterations int, tolerance float64, typeOfError int) error {
	x := data.InitialValue
	delta := data.Delta
	var previousFx float64
	var previousX float64

	for i := 0; i < maxIterations; i++ {
		fx, err := evaluateFunction(data.Function, x)
		if err != nil {
			return err
		}
		if fx*previousFx < 0 {
			fmt.Printf("Iteration %d: x = %g, f(x) = %g, There is a root between %g and %g\n", i, x, fx, previousX, x)
		} else {
			fmt.Printf("Iteration %d: x = %g, f(x) = %g\n", i, x, fx)
		}
		previousFx = fx
		previousX = x
		x = x + delta
	}
	return nil
}

func iterateNewtonMethod(data NewtonData, maxIterations int, tolerance float64, typeOfError int) (float64, error) {
	x := data.InitialValue
	var previousX float64

	for i := 0; i < maxIterations; i++ {
		newX, err := evaluateNewton(data.Function, data.Derivative, x)
		if err != nil {
			return 0, err
		}

		// Calculate error
		var errorValue float64
		if i > 0 {
			errorValue = calculateError(x, previousX, typeOfError)
		} else {
			// For the first iteration, force at least one iteration
			errorValue = tolerance + 1
		}

		// Evaluate f(x) for display
		fx, _ := evaluateFunction(data.Function, x)

		// Display iteration info
		fmt.Printf("Iteration %d: x = %.11f, f(x) = %.11f, Error = %.11f\n", i+1, x, fx, errorValue)

		// Check for convergence
		if errorValue < tolerance {
			fmt.Printf("Converged after %d iterations\n", i+1)
			return newX, nil
		}

		// Update previousX and x for the next iteration
		previousX = x
		x = newX
	}

	return 0, fmt.Errorf("method did not converge after %d iterations", maxIterations)
}

func iterateBisectionMethod(data BisectionData, maxIterations int, tolerance float64, typeOfError int) (float64, error) {
	a := data.Interval[0]
	b := data.Interval[1]
	var previousC float64

	for i := 0; i < maxIterations; i++ {
		c := (a + b) / 2.0
		fc, err := evaluateFunction(data.Function, c)
		if err != nil {
			return 0, err
		}

		var errorValue float64
		if i > 0 {
			errorValue = calculateError(c, previousC, typeOfError)
		} else {
			errorValue = tolerance + 1
		}

		if abs(fc) < tolerance {
			fmt.Printf("Converged after %d iterations\n", i+1)
			return c, nil
		}

		fa, err := evaluateFunction(data.Function, a)
		if err != nil {
			return 0, err
		}

		if fa*fc < 0 {
			b = c
		} else {
			a = c
		}

		fmt.Printf("Iteration %d: a = %.11f, b = %.11f, c = %.11f, f(c) = %.11f, Error = %.11f\n", i+1, a, b, c, fc, errorValue)

		previousC = c
	}

	return 0, fmt.Errorf("method did not converge after %d iterations", maxIterations)
}

func iterateSecantMethod(data SecantData, maxIterations int, tolerance float64, typeOfError int) (float64, error) {
	x0 := data.InitialValue1
	x1 := data.InitialValue2

	for i := 0; i < maxIterations; i++ {
		fx0, err := evaluateFunction(data.Function, x0)
		if err != nil {
			return 0, err
		}

		fx1, err := evaluateFunction(data.Function, x1)
		if err != nil {
			return 0, err
		}

		if i == 0 {
			fmt.Printf("Iteration %d: x = %g, f(x) = %g\n", 0, x0, fx0)
			fmt.Printf("Iteration %d: x = %g, f(x) = %g\n", 1, x1, fx1)
		} else {
			errorValue := calculateError(x1, x0, typeOfError)
			fmt.Printf("Iteration %d: x = %g, f(x) = %g, error = %g\n", i+1, x1, fx1, errorValue)
		}

		// Secant formula: x2 = x1 - f(x1)*(x1 - x0)/(f(x1) - f(x0))
		x2 := x1 - fx1*(x1-x0)/(fx1-fx0)

		if abs(x2-x1) < tolerance {
			fmt.Printf("Converged after %d iterations\n", i+1)
			return x2, nil
		}

		x0 = x1
		x1 = x2
	}

	return 0, fmt.Errorf("method did not converge after %d iterations", maxIterations)
}

func iterateMultipleRootsMethod(data MultipleRootsData, maxIterations int, tolerance float64, typeOfError int) (float64, error) {
	x := data.InitialValue
	var newX float64

	for i := 0; i < maxIterations; i++ {
		fx, err := evaluateFunction(data.Function, x)
		if err != nil {
			return 0, err
		}

		dfx, err := evaluateFunction(data.FirstDerivative, x)
		if err != nil {
			return 0, err
		}

		d2fx, err := evaluateFunction(data.SecondDerivative, x)
		if err != nil {
			return 0, err
		}
		errorValue := calculateError(newX, x, typeOfError)

		// Multiple Roots formula: x_new = x - (f(x) * f'(x)) / ((f'(x))^2 - f(x) * f''(x))
		newX = x - (fx*dfx)/((dfx*dfx)-(fx*d2fx))

		fmt.Printf("Iteration %d: x = %g, f(x) = %g, f'(x) = %g, f''(x) = %g, error = %g\n", i, x, fx, dfx, d2fx, errorValue)

		if abs(newX-x) < tolerance {
			fmt.Printf("Converged after %d iterations\n", i+1)
			return newX, nil
		}

		x = newX
	}

	return 0, fmt.Errorf("method did not converge after %d iterations", maxIterations)
}

func gaussianElimination(A [][]float64, b []float64) []float64 {
	n := len(A)

	// Forward elimination
	for k := 0; k < n-1; k++ {
		for i := k + 1; i < n; i++ {
			factor := A[i][k] / A[k][k]
			for j := k; j < n; j++ {
				A[i][j] = A[i][j] - factor*A[k][j]
			}
			b[i] = b[i] - factor*b[k]
		}
	}

	// Backward substitution
	x := make([]float64, n)
	for i := n - 1; i >= 0; i-- {
		sum := 0.0
		for j := i + 1; j < n; j++ {
			sum += A[i][j] * x[j]
		}
		x[i] = (b[i] - sum) / A[i][i]
	}

	return x
}

func customFunctions() map[string]govaluate.ExpressionFunction {
	functions := map[string]govaluate.ExpressionFunction{
		"pow": func(args ...interface{}) (interface{}, error) {
			base := args[0].(float64)
			exponent := args[1].(float64)
			return math.Pow(base, exponent), nil
		},
		"exp": func(args ...interface{}) (interface{}, error) {
			exponent := args[0].(float64)
			return math.Exp(exponent), nil
		},
		"ln": func(args ...interface{}) (interface{}, error) {
			x := args[0].(float64)
			return math.Log(x), nil
		},
		"sin": func(args ...interface{}) (interface{}, error) {
			x := args[0].(float64)
			return math.Sin(x), nil
		},
		"cos": func(args ...interface{}) (interface{}, error) {
			x := args[0].(float64)
			return math.Cos(x), nil
		},
	}
	return functions
}

func evaluateFunction(functionStr string, x float64) (float64, error) {
	processedFunctionStr := preprocessExpression(functionStr)

	expression, err := govaluate.NewEvaluableExpressionWithFunctions(processedFunctionStr, customFunctions())
	if err != nil {
		return 0, fmt.Errorf("error parsing function: %v", err)
	}

	parameters := make(map[string]interface{})
	parameters["x"] = x

	result, err := expression.Evaluate(parameters)
	if err != nil {
		return 0, fmt.Errorf("error evaluating function: %v", err)
	}

	return result.(float64), nil
}

func evaluateNewton(functionStr string, derivativeStr string, x float64) (float64, error) {
	fx, err := evaluateFunction(functionStr, x)
	if err != nil {
		return 0, err
	}

	dfx, err := evaluateFunction(derivativeStr, x)
	if err != nil {
		return 0, err
	}

	if dfx == 0 {
		return 0, fmt.Errorf("derivative is zero at x = %.11f, cannot proceed with division", x)
	}

	newX := x - fx/dfx
	return newX, nil
}
func iterateSimpleGaussianEliminationMethod(data GaussianData, maxIterations int, tolerance float64, typeOfError int) (float64, error) {
	A := data.Matrix
	b := data.Vector
	n := len(A)

	// Forward elimination
	for k := 0; k < n-1; k++ {
		for i := k + 1; i < n; i++ {
			factor := A[i][k] / A[k][k]
			for j := k; j < n; j++ {
				A[i][j] = A[i][j] - factor*A[k][j]
			}
			b[i] = b[i] - factor*b[k]
		}
	}

	// Backward substitution
	x := make([]float64, n)
	for i := n - 1; i >= 0; i-- {
		sum := 0.0
		for j := i + 1; j < n; j++ {
			sum += A[i][j] * x[j]
		}
		x[i] = (b[i] - sum) / A[i][i]
	}

	return x[0], nil
}

func iteratePartialPivotMethod(data GaussianData, maxIterations int, tolerance float64, typeOfError int) (float64, error) {
	A := data.Matrix
	b := data.Vector
	n := len(A)
	var _ float64

	// Forward elimination with partial pivoting
	for k := 0; k < n-1; k++ {
		// Find the row with the largest pivot element in column k
		maxIndex := k
		for i := k + 1; i < n; i++ {
			if abs(A[i][k]) > abs(A[maxIndex][k]) {
				maxIndex = i
			}
		}
		// Swap rows in both A and b
		A[k], A[maxIndex] = A[maxIndex], A[k]
		b[k], b[maxIndex] = b[maxIndex], b[k]

		for i := k + 1; i < n; i++ {
			factor := A[i][k] / A[k][k]
			for j := k; j < n; j++ {
				A[i][j] = A[i][j] - factor*A[k][j]
			}
			b[i] = b[i] - factor*b[k]
		}
	}

	// Backward substitution
	x := make([]float64, n)
	for i := n - 1; i >= 0; i-- {
		sum := 0.0
		for j := i + 1; j < n; j++ {
			sum += A[i][j] * x[j]
		}
		x[i] = (b[i] - sum) / A[i][i]
	}

	return x[0], nil
}

func iterateFullPivotMethod(data GaussianData, maxIterations int, tolerance float64, typeOfError int) (float64, error) {
	A := data.Matrix
	b := data.Vector
	n := len(A)
	// Track column swaps
	columnSwap := make([]int, n)
	for i := range columnSwap {
		columnSwap[i] = i
	}

	// Forward elimination with full pivoting
	for k := 0; k < n-1; k++ {
		// Find the largest pivot element in the submatrix
		maxRow, maxCol := k, k
		for i := k; i < n; i++ {
			for j := k; j < n; j++ {
				if abs(A[i][j]) > abs(A[maxRow][maxCol]) {
					maxRow, maxCol = i, j
				}
			}
		}
		// Swap rows and columns
		A[k], A[maxRow] = A[maxRow], A[k]
		for i := 0; i < n; i++ {
			A[i][k], A[i][maxCol] = A[i][maxCol], A[i][k]
		}
		b[k], b[maxRow] = b[maxRow], b[k]
		columnSwap[k], columnSwap[maxCol] = columnSwap[maxCol], columnSwap[k]

		for i := k + 1; i < n; i++ {
			factor := A[i][k] / A[k][k]
			for j := k; j < n; j++ {
				A[i][j] = A[i][j] - factor*A[k][j]
			}
			b[i] = b[i] - factor*b[k]
		}
	}

	// Backward substitution
	x := make([]float64, n)
	for i := n - 1; i >= 0; i-- {
		sum := 0.0
		for j := i + 1; j < n; j++ {
			sum += A[i][j] * x[j]
		}
		x[i] = (b[i] - sum) / A[i][i]
	}

	// Adjust solution based on column swaps
	finalX := make([]float64, n)
	for i := 0; i < n; i++ {
		finalX[columnSwap[i]] = x[i]
	}

	return finalX[0], nil
}
