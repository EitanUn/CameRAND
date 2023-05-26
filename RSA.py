"""
Author: Eitan Unger
Date: 18/04/23
description: A file for math- and RSA-related functions such as primality tests and key pair generation based on
2 primes, and all the other required functions
"""
from chaotic_source import Random
import logging


def rabin_miller(num, accuracy, rand: Random):
    """
    rabin-miller primality test
    :param num: number to test
    :param accuracy: number of trials (iterations)
    :param rand: RNG object
    :return: likely prime/not prime
    """

    logging.debug("RSA: Testing if %d is prime further" % num)
    # Returns True if num is a prime number.

    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s // 2
        t += 1

    for trials in range(accuracy):  # try to falsify num's primality
        a = rand.get_int_range(2, num - 1)
        v = pow(a, s, num)
        if v != 1:  # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    logging.debug("RSA: number is not prime")
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    logging.debug("RSA: %d is prime" % num)
    return True


def is_prime(num, rand: Random, accuracy=10):
    """
    basic small prime check, else calls the rabin-miller test
    :param num: number to test
    :param rand: RNG object for rabin-miller call
    :param accuracy: number of trials (iterations) for the rabin-miller call
    :return: likely prime/not prime
    """
    # Return True if num is a prime number. This function does a quicker
    # prime number check before calling rabinMiller().
    logging.debug("RSA: Testing if %d is prime" % num)
    if num < 2:
        logging.debug("RSA: number is not prime")
        return False  # 0, 1, and negative numbers are not prime

    # About 1/3 of the time we can quickly determine if num is not prime
    # by dividing by the first few dozen prime numbers. This is quicker
    # than rabinMiller(), but unlike rabinMiller() is not guaranteed to
    # prove that a number is prime.
    low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                  103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                  211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                  331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                  449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                  587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                  709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                  853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                  991, 997]

    if num in low_primes:
        logging.debug("RSA: %d is prime" % num)
        return True

    # See if any of the low prime numbers can divide num
    for prime in low_primes:
        if num % prime == 0:
            logging.debug("RSA: number is not prime")
            return False

    # If all else fails, call rabinMiller() to determine if num is a prime.
    logging.debug("RSA: Calling Rabin-miller test")
    return rabin_miller(num, accuracy, rand)


def gcd(a, b):
    """
    greatest common divisor function using Euclidean algorithm
    :param a: number 1
    :param b: number 2
    :return: greatest common divisor
    """
    while a > 0 and b > 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return max(a, b)


def lcm(a, b):
    """
    least common multiple function
    :param a: number 1
    :param b: number 2
    :return: least common multiple
    """
    return abs(a*b)//gcd(a, b)


def rsa(p, q):
    """
    a function to calculate all the required numbers for an RSA key
    :param p: prime 1
    :param q: prime 2
    :return: the three remaining numbers: modulus, public power and private power
    """
    logging.debug("RSA: Generating key pair for %d, %d" % (p, q))
    n = p * q
    lam_n = lcm(p-1, q-1)
    e = 65537
    assert gcd(e, lam_n) == 1
    d = pow(e, -1, lam_n)
    assert (e*d) % lam_n == 1
    logging.debug("RSA: keypair generated")
    return n, e, d


def get_prime(rand):
    """
    A function to get a prime number based on a randomly generated number
    :param rand: the random number generator object
    """
    logging.debug("RSA: Prime number requested")
    b = rand.get_rand_large(1024) | 1  # generate random int and make sure it is odd (only even prime is 2, not needed)
    while not is_prime(b, rand):
        b += 2  # if not prime, go to the next odd number until prime is found
    logging.debug("RSA: Found prime %d" % b)
    return b


if __name__ == '__main__':
    assert gcd(20057, 16261) == 1
    assert gcd(10000, 25000) == 5000
    assert lcm(122, 17) == 2074
    assert lcm(100, 555) == 11100
