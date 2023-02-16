from os.path import join
from Crypto.PublicKey import RSA
from pickle import dump, load
from chaotic_source import Random
from RSA import is_prime, rsa
from threading import Event
import cv2
from tkinter.filedialog import asksaveasfilename


def public_key(modulus, exponent, dir):
    key = RSA.construct((modulus, exponent))
    assert not key.has_private()
    with open(join(dir, "id_rsa.pub"), "wb") as file:
        file.write(key.exportKey(format='OpenSSH'))


def private_key(modulus, exponent, priv_exp, p, q, dir):
    key = RSA.construct((modulus, exponent, priv_exp, p, q))
    assert key.has_private()
    with open(join(dir, "id_rsa"), "wb") as file:
        file.write(key.exportKey())


def keygen(dir):
    p, q = get_primes()
    n, e, d = rsa(p, q)
    public_key(n, e, dir)
    private_key(n, e, d, p, q, dir)


def add_prime(num):
    with open("primes.bin", "rb") as file:
        primes = load(file)
    primes.append(num)
    with open("primes.bin", "wb") as file:
        dump(primes, file)


def get_primes():
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
    rand = Random()
    while True:
        num = rand.get_rand_large()
        if is_prime(num):
            add_prime(num)
        if event.is_set():
            break
    rand.pause()


def save_image(im):
    save_path = asksaveasfilename(defaultextension='.png',
                                  filetypes=[("png Files", "*.png")], title="Choose location")
    cv2.imwrite(save_path, cv2.imread(im))
