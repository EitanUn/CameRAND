from Crypto.PublicKey import RSA


def str_to_int(my_string):
    num = 0
    for ch in my_string:
        num = (num << 8) + ord(ch)
    return num


def int_to_str(num):
    str = ""
    while num:
        str += chr(num % 256)
        num //= 256
    return str[::-1]


with open("keys/id_rsa", 'r') as file:
    private = RSA.importKey(file.read())

with open("keys/id_rsa.pub", 'r') as file:
    public = RSA.importKey(file.read())

message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut " \
          "labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris,"
print(message)
print(str_to_int(message))
encrypted = pow(str_to_int(message), public.e, public.n)
print(encrypted)
message = pow(encrypted, private.d, private.n)
print(message)
print(int_to_str(message))
