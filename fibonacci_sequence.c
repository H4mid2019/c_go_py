#include <stdio.h>
#include <stdlib.h> 
#include <time.h> 


/**
 * @brief Calculates Fibonacci numbers from F(0) to F(n) and stores them in a pre-allocated array.
 *
 * @param n The maximum index of the Fibonacci sequence to calculate (inclusive).
 * @param result_array Pointer to an array allocated by the caller. Must be large enough
 * to hold n + 1 elements (indices 0 to n).
 * @param array_size The number of elements the result_array can hold.
 * @return int 0 on success, -1 if the provided array is too small.
 */
int fibonacci_sequence(int n, unsigned long long* result_array, int array_size) {
    if (array_size < n + 1) {
        return -1; 
    }

    if (n >= 0) {
        result_array[0] = 0;
    }
    if (n >= 1) {
        result_array[1] = 1;
    }

    int i = 2;
    while (i <= n) {
        result_array[i] = result_array[i - 1] + result_array[i - 2];
        i++;
    }

    return 0;
}


int main() {
    int n_value = 15;
    int num_runs = 10000;
    int status;

    int size = n_value + 1;
    unsigned long long* result_buffer = (unsigned long long*)malloc(size * sizeof(unsigned long long));

    if (result_buffer == NULL) {
        fprintf(stderr, "Error: Failed to allocate memory for the result buffer.\n");
        return 1;
    }

    printf("Timing C function fibonacci_sequence for n=%d (runs=%d)...\n", n_value, num_runs);

    clock_t start_time, end_time;
    double cpu_time_used;

    start_time = clock();

    for (int i = 0; i < num_runs; ++i) {
        status = fibonacci_sequence(n_value, result_buffer, size);
        if (status != 0) {
             fprintf(stderr, "Warning: fibonacci_sequence failed on run %d\n", i);
        }
    }

    end_time = clock();

    cpu_time_used = ((double)(end_time - start_time)) / CLOCKS_PER_SEC;

    printf("Total CPU time used for %d runs: %f seconds\n", num_runs, cpu_time_used);
    printf("Average CPU time per run:        %f seconds\n", cpu_time_used / num_runs);

    free(result_buffer); 

    return 0; 
}