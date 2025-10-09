#!/usr/bin/env python3
"""Print the 10th prime number to stdout as a single integer."""

def nth_prime(n: int) -> int:
    if n < 1:
        raise ValueError("n must be >= 1")
    primes = []
    num = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    return primes[-1]


if __name__ == "__main__":
    print(nth_prime(10))
