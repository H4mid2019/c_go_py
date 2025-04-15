package main

import (
	"errors"
	"fmt"
)

func fibonacciSequenceGo(n int) ([]uint64, error) {

	if n < 0 {
		return nil, errors.New("input n cannot be negative")
	}

	if n == 0 {
		return []uint64{0}, nil
	}

	results := make([]uint64, n+1)

	results[0] = 0
	if n >= 1 {
		results[1] = 1
	}
	i := 2
	for i <= n {
		results[i] = results[i-1] + results[i-2]
		i++
	}

	return results, nil
}

func main() {
	nValue := 15

	fmt.Printf("Calculating Fibonacci sequence in Go for n=%d...\n", nValue)

	fibSequence, err := fibonacciSequenceGo(nValue)

	if err != nil {
		fmt.Println("Error:", err)
	} else {

		fmt.Println("Result:", fibSequence)
	}
}
