import ctypes
import os
import sys
import timeit
import psutil
import platform

lib_name = 'fibonacci_sequence.so'

script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, lib_name)

try:
    fib_lib = ctypes.CDLL(lib_path)
    print(f"Successfully loaded C library: {lib_path}")
except OSError as e:
    print(f"Error loading C library: {e}")
    sys.exit(1)


try:
    c_fib_sequence_func = fib_lib.fibonacci_sequence
except AttributeError:
    print(f"Error: Function 'fibonacci_sequence' not found in library {lib_name}.")
    sys.exit(1)


c_fib_sequence_func.argtypes = [
    ctypes.c_int,                         
    ctypes.POINTER(ctypes.c_ulonglong),   
    ctypes.c_int                          
]


c_fib_sequence_func.restype = ctypes.c_int



def get_fibonacci_sequence_from_c(n_value):
    """
    Calls the C function to get the Fibonacci sequence up to n_value.

    Args:
        n_value (int): The maximum index (inclusive) for the sequence.

    Returns:
        list: A list of Fibonacci numbers [F(0)...F(n)], or None if an error occurred.
    """
    if not isinstance(n_value, int) or n_value < 0:
        print("Error: Input must be a non-negative integer.")
        return None

    
    size = n_value + 1

    
    
    ULongLongArray = ctypes.c_ulonglong * size
    
    result_buffer = ULongLongArray() 

    
    print(f"\nCalling C function for n = {n_value}...")
    status = c_fib_sequence_func(n_value, result_buffer, size)

    
    if status == 0:
        print("C function executed successfully.")
        
        
        py_list = list(result_buffer)
        return py_list
    elif status == -1:
        print("Error returned from C function: Buffer size was insufficient (this shouldn't happen with correct size calculation).")
        return None
    else:
        print(f"Error returned from C function: Unknown status code {status}")
        return None


def fibonacci_sequence_py(n):
    if not isinstance(n, int) or n < 0:
        return None
    if n == 0:
        return [0]
    if n == 1:
        return [0, 1]

    result_list = [0] * (n + 1)
    result_list[0] = 0
    result_list[1] = 1
    i = 2
    while i <= n:
        result_list[i] = result_list[i - 1] + result_list[i - 2]
        i += 1
    return result_list



n_value = 15
num_runs = 10000 



print(f"Comparing execution time for n={n_value} (runs={num_runs})...")

c_time = timeit.timeit(
    lambda: get_fibonacci_sequence_from_c(n_value),
    number=num_runs
)

py_time = timeit.timeit(
    lambda: fibonacci_sequence_py(n_value),
    number=num_runs
)

print(f"C function via ctypes: {c_time:.6f} seconds")
print(f"Pure Python function:  {py_time:.6f} seconds")
if c_time < py_time:
    print(f"C version was approx {py_time / c_time:.2f} times faster.")
else:
     print(f"Python version was approx {c_time / py_time:.2f} times faster.")



print(f"\nComparing resource usage for a single run (n={n_value})...")

process = psutil.Process(os.getpid())


mem_before_c = process.memory_info().rss
cpu_before_c = process.cpu_times()
result_c = get_fibonacci_sequence_from_c(n_value) 
cpu_after_c = process.cpu_times()
mem_after_c = process.memory_info().rss
cpu_delta_c = (cpu_after_c.user - cpu_before_c.user) + \
              (cpu_after_c.system - cpu_before_c.system)
mem_delta_c = mem_after_c - mem_before_c


mem_before_py = process.memory_info().rss
cpu_before_py = process.cpu_times()
result_py = fibonacci_sequence_py(n_value) 
cpu_after_py = process.cpu_times()
mem_after_py = process.memory_info().rss
cpu_delta_py = (cpu_after_py.user - cpu_before_py.user) + \
               (cpu_after_py.system - cpu_before_py.system)
mem_delta_py = mem_after_py - mem_before_py






print("\nResource Usage Comparison:")
print(f"C function (CPU time):   {cpu_delta_c:.6f} seconds")
print(f"Pure Python (CPU time):  {cpu_delta_py:.6f} seconds")
print(f"C function (Mem delta):  {mem_delta_c / 1024:,.2f} KB") 
print(f"Pure Python (Mem delta): {mem_delta_py / 1024:,.2f} KB") 

print(f"\nSystem Info: {platform.system()} {platform.machine()}")


