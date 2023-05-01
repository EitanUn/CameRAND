"""
Author: Eitan Unger
Date: 18/04/23
description: Client for CameRAND secure chat communication, can send and receive messages in the background of the chat
GUI on a thread
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
    The main function- handles the communication for the ChatClient class
    :param server_addr: the server address (ip, port)
    :param name: display name for client in the chat
    :param finished: event shared between client and thread to mark the end of communication
    :param in_list: the list of messages to send to the server
    :param text: the text field of the GUI
    """
    server_socket = socket.socket()
    try:
        server_socket.connect(server_addr)
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
        enc_name = cipher.encrypt(name[0].encode())
        server_socket.send(protocol_encode(enc_name, 'bin'))  # send name to the server
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
        server_socket.send(protocol_encode("", "end"))
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
    :return: protocol encoded message
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
    elif len == '%pk':  # private key message prefix
        assert socket.recv(6).decode() == "003key"
        return 1
    elif len == 'bin':  # binary data message prefix (do not decode data)
        len = socket.recv(3).decode()
        return socket.recv(int(len))
    elif len == 'end':  # client disconnect message prefix
        return 0
    len = int(len)
    return socket.recv(len).decode()  # read the message


def int_to_bytes(num):
    """
    func to turn an integer into bytes object
    :param num: integer variable
    :return: bytes form of num
    """
    byte_list = []
    while num:
        byte_list.append(num % 256)
        num //= 256
    return bytes(byte_list)


if __name__ == '__main__':
    pass
