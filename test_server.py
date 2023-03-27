"""
Author: Eitan Unger
Date: 27/5/22
description: Server for Cow006, manages game, runs infinitely
"""

import socket
import select
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

# --------------------------- CONSTANTS ---------------------------
SERVER_IP = '0.0.0.0'
SERVER_PORT = 20003
LISTEN_SIZE = 5
READ_SIZE = 3
TIMEOUT = 60
socket.setdefaulttimeout(TIMEOUT)

# --------------------------- MAIN ---------------------------


def main():
    """
    every time a game is finished or aborted, set up a new game
    :return: none
    """
    while True:
        main_loop()


def main_loop():
    """
    the main server loop, split into log in phase and game phase, with setup in between
    restarts when an error is encountered or a game is finished
    :return: None
    """
    open_client_sockets = []
    client_addrs = {}
    client_keys = {}
    server_socket = socket.socket()
    with open("server_keys/id_rsa", 'r') as file:
        private = RSA.importKey(file.read())
    # log-in phase:
    try:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen(LISTEN_SIZE)
        while True:
            rlist, wlist, xlist = select.select([server_socket] + open_client_sockets,
                                                [], open_client_sockets, 0.01)
            # check for exception
            for current_socket in xlist:
                open_client_sockets.remove(current_socket)
                current_socket.close()
            for current_socket in rlist:
                # check for new connection
                if current_socket is server_socket:
                    client_socket, client_address = current_socket.accept()
                    name_msg = protocol_read(client_socket)
                    assert name_msg == 'n'
                    name = protocol_read(client_socket)
                    client_addrs.update({client_socket: name})
                    open_client_sockets.append(client_socket)
                    print("new client added")
                    break
                else:
                    # receive data
                    data = protocol_read(current_socket)
                    if data == 1:
                        current_socket.send(protocol_encode(str(private.e)))
                        current_socket.send(protocol_encode(str(private.n)))
                        en_key = int(protocol_read(current_socket))
                        key = pow(en_key, private.d, private.n)
                        nonce = protocol_read(current_socket)
                        cipher = AES.new(int_to_bytes(key), AES.MODE_EAX, nonce)
                        client_keys.update({current_socket: cipher})
                    print("Received: " + data)
                    # check if connection was aborted
                    if data == "" or data == b'':
                        # socket was closed
                        open_client_sockets.remove(current_socket)
                        current_socket.close()
                    else:
                        msg = str(client_keys[current_socket].decrypt(data))
                        data = client_addrs[current_socket] + ": " + msg
                        send_available(open_client_sockets)
                        for i in open_client_sockets:
                            enc_msg = client_keys[i].encrypt(data.encode())
                            i.send(protocol_encode(enc_msg))
    except socket.error as err:
        abort(open_client_sockets)
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
        return 1
    len = int(len)
    if len < 1024:
        return socket.recv(len).decode()  # read the message
    else:
        ret = ""
        while len > 1024:
            ret += socket.recv(1024).decode()
            len -= 1024
        ret += socket.recv(len).decode()
        return ret


def send_available(open_client_sockets):
    rlist, wlist, xlist = select.select(open_client_sockets,
                                        open_client_sockets, open_client_sockets, 0.01)
    for err in xlist:
        open_client_sockets.remove(err)
        err.close()
    while len(wlist) != len(open_client_sockets):
        rlist, wlist, xlist = select.select(open_client_sockets,
                                            open_client_sockets, open_client_sockets, 0.01)
        for err in xlist:
            open_client_sockets.remove(err)
            err.close()


def abort(sockets):
    for i in sockets:
        i.close()


def int_to_bytes(num):
    byte_list = []
    while num:
        byte_list.append(num % 8)
        num //= 8
    return bytes(byte_list)


if __name__ == '__main__':
    main()
