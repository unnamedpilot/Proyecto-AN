package main

import (
	"bufio"
	"fmt"
	"strconv"
)

func getIntInput(reader *bufio.Reader, prompt string) int {
	fmt.Print(prompt)
	input, _ := reader.ReadString('\n')
	value, _ := strconv.Atoi(input[:len(input)-2])
	println(value)
	return value
}

func getFloatInput(reader *bufio.Reader, prompt string) (value float64) {
	fmt.Print(prompt)
	input, _ := reader.ReadString('\n')
	value, _ = strconv.ParseFloat(input[:len(input)-2], 64)
	println(value)
	return
}

func getStringInput(reader *bufio.Reader, prompt string) (input string) {
	fmt.Print(prompt)
	input, _ = reader.ReadString('\n')
	println(input)
	return
}

func calculateError(value float64, previousValue float64, typeOfError int) float64 {
	//Absolute error
	if typeOfError == 1 {
		return abs(value - previousValue)
	} else {
		return abs((value-previousValue)/value) * 100
	}
}

func abs(a float64) float64 {
	if a < 0 {
		return -a
	}
	return a
}

// Helper function to print the matrix and vector
func printMatrixAndVector(A [][]float64, b []float64) {
	n := len(A)
	for i := 0; i < n; i++ {
		for j := 0; j < len(A[i]); j++ {
			fmt.Printf("%f ", A[i][j])
		}
		fmt.Printf(" | %f\n", b[i])
	}
	fmt.Println()
}
