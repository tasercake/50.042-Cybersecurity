#!/usr/bin/env python3
"""
50.042 FCS Lab 6 template
Year 2019

Krishna Penukonda - 1001781
"""
import random


def square_multiply(a, x, n):
    y = 1
    for i in range(x.bit_length(), -1, -1):
        y = (y ** 2) % n
        if (x >> i) & 1:
            y = (a * y) % n
    return y


def is_composite(a, d, n, r):
    if square_multiply(a, d, n) == 1:
        return False
    for i in range(r):
        if square_multiply(a, 2 ** i * d, n) == (n - 1):
            return False
    return True


def miller_rabin(n, k):
    # Express n as (2^r * d) + 1
    r = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        r += 1
    assert n == 2 ** r * d + 1

    for i in range(k):
        a = random.randint(2, n - 2)
        if is_composite(a, d, n, r):
            return False
    return True


def gen_prime_candidate(n):
    out = 1 << n - 1
    for i in range(n - 1):
        bit = random.randint(0, 1)
        if bit:
            out += bit << i
    return out


def gen_prime_nbits(n):
    while True:
        candidate = gen_prime_candidate(n)
        if miller_rabin(candidate, 8):
            return candidate


if __name__ == "__main__":
    print('29^6 mod 401')
    predicted = square_multiply(29, 6, 401)
    expected = pow(29, 6, 401)
    print(f"Expected {expected} | Got {predicted}")
    assert predicted == expected

    print('Is 561 a prime?')
    print(miller_rabin(561, 2))
    print('Is 27 a prime?')
    print(miller_rabin(27, 2))
    print('Is 61 a prime?')
    print(miller_rabin(61, 2))
    print('Random number (100 bits):')
    print(gen_prime_nbits(100))

    print('Random number (80 bits):')
    gen = gen_prime_nbits(80)
    print(gen)
    print("Checking that the generated number contains 80 bits...")
    assert len(bin(gen)[2:]) == 80
    print("Checking that the generated number is a prime...")
    assert miller_rabin(gen, 32)
    print("Passed!")
