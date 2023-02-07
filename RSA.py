import base64
import os.path

from chaotic_source import get_int_range as rand


def rabin_miller(num, webcam, accuracy):
    # Returns True if num is a prime number.

    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s // 2
        t += 1

    for trials in range(accuracy):  # try to falsify num's primality
        a = rand(webcam, 2, num - 1)
        v = pow(a, s, num)
        if v != 1:  # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def is_prime(num, webcam, accuracy=100):
    # Return True if num is a prime number. This function does a quicker
    # prime number check before calling rabinMiller().

    if num < 2:
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
        return True

    # See if any of the low prime numbers can divide num
    for prime in low_primes:
        if num % prime == 0:
            return False

    # If all else fails, call rabinMiller() to determine if num is a prime.
    return rabin_miller(num, webcam, accuracy)


def gcd(a, b):
    while a > 0 and b > 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return max(a, b)


def lcm(a, b):
    return abs(a*b)//gcd(a, b)


def extended_euclidean_algorithm(a, b):
    """
    extended_euclidean_algorithm(a, b)

    The result is the largest common divisor for a and b.

    :param a: integer number
    :param b: integer number
    :return:  the largest common divisor for a and b
    """

    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_euclidean_algorithm(b % a, a)
        return g, x - (b // a) * y, y


def modular_inverse(e, t):
    """
    modular_inverse(e, t)

    Counts modular multiplicative inverse for e and t.

    :param e: in this case e is a public key exponent
    :param t: and t is an Euler function
    :return:  the result of modular multiplicative inverse for e and t
    """

    g, x, y = extended_euclidean_algorithm(e, t)

    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % t


def rsa(p, q, dir):
    n = p * q
    lam_n = lcm(p-1, q-1)
    e = 65537
    assert gcd(e, lam_n) == 1
    d = pow(e, -1, lam_n)
    public_key(e, n, dir)
    private_key(d, n, dir)


def public_key(exponent, modulus, dir):
    key = 'ssh-rsa'
    key += str(len(hex(exponent)) / 2).zfill(8) + str(hex(exponent))
    key += str(len(hex(modulus)) / 2).zfill(8) + str(hex(modulus))
    key_bytes = key.encode('ascii')
    base64_bytes = base64.b64encode(key_bytes)
    key_base64 = base64_bytes.decode('ascii')
    with open(os.path.join(dir, "id_rsa.pub"), "w") as file:
        file.write("---- BEGIN SSH2 PUBLIC KEY ----\nssh-rsa")
        file.write(key_base64)
        file.write("\n---- END SSH2 PUBLIC KEY ----")


def private_key(exponent, modulus, dir):
    key = '00000007' + 'ssh-rsa'
    key += str(len(hex(exponent)) / 2).zfill(8) + str(hex(exponent))
    key += str(len(hex(modulus)) / 2).zfill(8) + str(hex(modulus))
    key_bytes = key.encode('ascii')
    base64_bytes = base64.b64encode(key_bytes)
    key_base64 = base64_bytes.decode('ascii')
    with open(os.path.join(dir, "id_rsa"), "w") as file:
        file.write(key_base64)
