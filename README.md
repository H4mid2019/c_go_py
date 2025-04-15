# Fibonacci Performance Comparison: C vs. Go vs. Python

This repository contains code used to compare the performance of calculating a Fibonacci sequence (up to n=15) using different programming languages and techniques.

## Overview

The goal of this experiment was to observe and quantify the execution speed differences between:

1.  **Native C** (compiled with `-O3` optimization)
2.  **Native Go**
3.  **Pure Python** (CPython)
4.  **C called from Python** via the `ctypes` Foreign Function Interface (FFI)

The task involves generating all Fibonacci numbers from F(0) up to F(15).

## Implementations Included

* `fibonacci_sequence.c`: Contains the C implementation of `fibonacci_sequence` (fills a pre-allocated array) and a `main` function for native C benchmarking using `clock()`.
* `fibonacci_go.go`: Contains the Go implementation `fibonacciSequenceGo`.
* `fibonacci_go_test.go`: Contains the Go benchmark function `BenchmarkFibonacciSequenceGo` using the standard `testing` package.
* `compare_fib.py`: Python script that:
    * Loads the compiled C function from a shared library using `ctypes`.
    * Includes a pure Python implementation (`fibonacci_sequence_py`).
    * Uses `timeit` to compare the execution speed of the pure Python and C-via-ctypes versions.
    * Uses `psutil` to compare approximate resource usage (CPU/Memory delta) for a single run.

## Requirements

* **C Compiler:** GCC or Clang (tested with GCC).
* **Go:** Go compiler toolchain (tested with Go 1.x).
* **Python:** Python 3.x.
* **Python Libraries:**
    * `psutil`: Install via `pip install psutil`.

## How to Run the Comparisons

1.  **Clone the Repository:**
    ```bash
    git clone git@github.com:H4mid2019/c_go_py.git
    cd c_go_py
    ```

2.  **Compile C Code:**
    * **Shared Library (for Python `ctypes`)**:
        ```bash
        # Linux/macOS
        gcc -shared -o fibonacci_sequence.so -fPIC fibonacci_sequence.c

        # Windows (MinGW/MSYS2) - uncomment if needed
        gcc -shared -o fibonacci_sequence.dll fibonacci_sequence.c
        ```
    * **Executable (for Native C Benchmark)**:
        ```bash
        # Compile with optimization for accurate timing
        gcc -O3 fibonacci_sequence.c -o fib_c_runner
        ```

3.  **Run Python Comparison (`timeit` + `psutil`):**
    * Ensure `fibonacci_sequence.so` (or `.dll`) is in the same directory.
    * Ensure `psutil` is installed (`pip install psutil`).
    * Execute the script:
        ```bash
        python compare_fib.py
        ```
    * This will output the `timeit` results for Pure Python vs C-via-ctypes and the resource usage comparison.

4.  **Run Native C Benchmark:**
    ```bash
    ./fib_c_runner
    ```
    * This will output the CPU time measured using `clock()` for the native C execution.

5.  **Run Go Benchmark:**
    ```bash
    go test -bench=. -benchmem
    ```
    * This will output the benchmark results, including nanoseconds per operation (`ns/op`) and memory allocation statistics.

## Results Summary (Example)

Performance was measured as the average time per single function call for generating the sequence up to F(15). Lower is better.

| Implementation Method        | Measurement Tool   | Avg. Time per Operation (ns/op) | Relative Speed (Approx. vs Go) | Notes                                                        |
| :--------------------------- | :----------------- | :------------------------------ | :----------------------------- | :----------------------------------------------------------- |
| **Native C** | C `clock()`        | **~0.1 ns/op** | **~440x Faster than Go** | Compiled C (-O3 Opt) timed natively (CPU time). Very fast. |
| **Native Go** | `go test -bench`   | **~44.3 ns/op** | **1.0x** (Baseline)            | Compiled Go code benchmarked natively (Wall time).           |
| **Pure Python** | Python `timeit`    | **~1,785 ns/op** | **~40x Slower than Go** | Interpreted Python code (CPython).                           |
| **C via `ctypes` (Python)** | Python `timeit`    | **~40,000 ns/op** | **~900x Slower than Go** | C code called from Python via FFI overhead.                  |

*(Note: Your specific results will vary based on your hardware and software environment.)*

## Key Takeaways

* Native compiled code (C, Go) significantly outperforms interpreted Python for this CPU-bound task.
* Highly optimized C demonstrates exceptional speed.
* The overhead of Python's `ctypes` FFI can be substantial, potentially making it slower than pure Python for very fast, frequently called C functions. FFI is generally more beneficial for computationally heavier C functions.
* Benchmarking is essential to understand real-world performance characteristics.
