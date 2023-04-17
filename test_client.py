"""
Author: Eitan Unger
Date: 27/5/22
description: Client for Cow006, manages graphics, runs for the length of one game then shuts down
"""
import socket
import tkinter.scrolledtext
from threading import Event
from chaotic_source import Random
from Crypto.Cipher import AES
from AES_new import AesNew
import select


def client_thread(server_addr: tuple, name,  finished: Event, in_list: list, text: tkinter.scrolledtext.ScrolledText):
    """
    The main function- handles the game running
    :return: none
    """
    server_socket = socket.socket()
    try:
        server_socket.connect(server_addr)
        server_socket.send(protocol_encode(name[0], "%in"))  # send name to the server
        server_socket.send(protocol_encode("key", "%pk"))  # request public key from server
        exponent = int(protocol_read(server_socket))
        num = int(protocol_read(server_socket))
        rand = Random()
        key = rand.get_rand_large(128)
        rand.pause()
        server_socket.send(protocol_encode(str(pow(key, exponent, num))))
        temp_cipher = AES.new(int_to_bytes(key), AES.MODE_EAX)
        server_socket.send(protocol_encode(temp_cipher.nonce, pre='bin'))
        cipher = AesNew(int_to_bytes(key), temp_cipher.nonce)
        out_list = []
        while not finished.is_set():
            rlist, wlist, xlist = select.select([server_socket], out_list, [server_socket], 0.05)

            if rlist:
                data = protocol_read(server_socket)
                if data == "":
                    text.configure(state="normal")
                    text.insert(tkinter.END, "---------------------------Server Closed------------------")
                    text.config(state="disabled")
                    break
                msg = cipher.decrypt(data)
                text.configure(state="normal")
                text.insert(tkinter.END, msg.decode() + "\n")
                text.config(state="disabled")

            if wlist:
                for i in in_list:
                    enc_msg = cipher.encrypt(i.encode())
                    server_socket.send(protocol_encode(enc_msg, 'bin'))
                    in_list.remove(i)
                out_list = []
            if in_list:
                out_list.append(server_socket)

    except socket.error as err:
        print("error: " + str(err))
    finally:
        server_socket.close()

# --------------------------- NETWORK FUNCS ---------------------------


def protocol_encode(line, pre=""):
    """
    Encodes message according to the protocol (length prefix and type prefix)
    :param line: line to encode
    :param pre: prefix to add to the message for special messages like key and name
    :return:
    """
    if pre == 'bin':
        return (pre + str(len(line)).zfill(3)).encode() + line
    return (pre + str(len(line)).zfill(3) + line).encode()  # add a 3-digit length prefix for protocol_read()


def protocol_read(socket):
    """
    read the message (exact length) using the protocol
    :param socket: socket to read from
    :return: message read from socket, parsed
    """
    len = socket.recv(3).decode()  # get length
    if len == "" or len == b'':  # check for error
        return len
    elif len == '%in':
        return 'n'
    elif len == '%pk':
        assert socket.recv(6).decode() == "003key"
        return 'pk'
    elif len == 'bin':
        len = socket.recv(3).decode()
        return socket.recv(int(len))
    len = int(len)
    return socket.recv(len).decode()  # read the message


def int_to_bytes(num):
    byte_list = []
    while num:
        byte_list.append(num % 256)
        num //= 256
    return bytes(byte_list)


if __name__ == '__main__':
    pass
