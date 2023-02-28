"""
Author: Eitan Unger
Date: 28/02/23
description: A file concentrating all functions that access files, write/read/create.
"""
from os.path import join
from Crypto.PublicKey import RSA
from pickle import dump, load
from chaotic_source import Random
from RSA import is_prime, rsa
from threading import Event
import cv2
from tkinter.filedialog import asksaveasfilename


def public_key(modulus, exponent, dir):
    """
    a function to generate an RSA public key using pycryptodome with pre-generated numbers
    :param modulus: the public modulus, which is the product of the two primes used in key generation
    :param exponent: the public exponent, namely e, which is 65537
    :param dir: where to save the key
    """
    key = RSA.construct((modulus, exponent))
    assert not key.has_private()
    with open(join(dir, "id_rsa.pub"), "wb") as file:
        file.write(key.exportKey(format='OpenSSH'))


def private_key(modulus, exponent, priv_exp, p, q, dir):
    """
    a function to generate an RSA private key using pycryptodome with pre-generated numbers
    :param modulus: the public modulus, which is the product of the two primes used in key generation
    :param exponent: the public exponent, namely e, which is 65537
    :param priv_exp: the private exponent, namely d, the modular multiplicative inverse of the exponent
    :param p: prime 1 used in key generation
    :param q: prime 2 used in key generation
    :param dir: where to save the key
    """
    key = RSA.construct((modulus, exponent, priv_exp, p, q))
    assert key.has_private()
    with open(join(dir, "id_rsa"), "wb") as file:
        file.write(key.exportKey())


def keygen(dir):
    """
    a function to call each step in key generation in order
    :param dir: where to save the keys
    """
    p, q = get_primes()
    n, e, d = rsa(p, q)
    public_key(n, e, dir)
    private_key(n, e, d, p, q, dir)


def add_prime(num):
    """
    a function to insert a prime number into the prime list, primes.bin
    :param num: number to insert
    """
    with open("primes.bin", "rb") as file:
        primes = load(file)
    primes.append(num)
    with open("primes.bin", "wb") as file:
        dump(primes, file)


def get_primes():
    """
    A function that returns two primes, either from primes.bin or if unavailable generate them on the spot
    :return: two prime numbers
    """
    rand = Random()
    with open("primes.bin", "rb") as file:
        primes = load(file)
    if len(primes) >= 2:
        a, b = primes.pop(0), primes.pop(1)
        with open("primes.bin", "wb") as file:
            dump(primes, file)
    elif len(primes) == 1:
        a = primes.pop(0)
        b = rand.get_rand_large()
        while not is_prime(b):
            b = rand.get_rand_large()
        with open("primes.bin", "wb") as file:
            dump([], file)
    else:
        a = rand.get_rand_large()
        while not is_prime(a):
            a = rand.get_rand_large()
        b = rand.get_rand_large()
        while not is_prime(b):
            b = rand.get_rand_large()
    rand.pause()
    return a, b


def idle_prime(event: Event):
    """
    A thread loop function to get large numbers, check their primality using a miller-rabin test and insert them in the
    list, in the background of the code
    :param event: a flag to check if the thread should stop
    """
    rand = Random()
    rand.pause()
    while True:
        rand.cont()
        num = rand.get_rand_large()
        rand.pause()
        if is_prime(num):
            add_prime(num)
        if event.is_set():
            return


def save_image(im):
    """
    a function to get an image's save path and save it there
    :param im: a numpy array containing an image
    """
    save_path = asksaveasfilename(defaultextension='.png',
                                  filetypes=[("png Files", "*.png")], title="Choose location")
    cv2.imwrite(save_path, cv2.imread(im))
