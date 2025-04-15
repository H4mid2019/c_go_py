package main

import (
	"testing"
)

func BenchmarkFibonacciSequenceGo(b *testing.B) {
	nValue := 15

	for i := 0; i < b.N; i++ {
		_, _ = fibonacciSequenceGo(nValue)
	}
}
