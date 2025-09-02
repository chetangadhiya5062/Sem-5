import time
import math
from threading import Thread

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.sqrt(n))
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True

def sum_primes(start, end, result, idx):
    s = 0
    for i in range(start, end + 1):
        if is_prime(i):
            s += i
    result[idx] = s

start = time.time()
single_sum = 0
for i in range(2, 1000001):
    if is_prime(i):
        single_sum += i
end = time.time()

print("Without Thread")
print(f"Sum of primes : {single_sum}")
print(f"Time taken : {end - start} seconds\n")

print("With Threads")
result = {}
threads = [
    Thread(target=sum_primes, args=(2, 250000, result, 1)),
    Thread(target=sum_primes, args=(250001, 500000, result, 2)),
    Thread(target=sum_primes, args=(500001, 750000, result, 3)),
    Thread(target=sum_primes, args=(750001, 1000000, result, 4)),
]

start_time = time.time()
for t in threads: t.start()
for t in threads: t.join()

multi_sum = sum(result.values())
end_time = time.time()

print(f"Sum of primes : {multi_sum}")
print(f"Time taken with threads : {end_time - start_time} seconds")
