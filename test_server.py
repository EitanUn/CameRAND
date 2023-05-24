"""
Author: Eitan Unger
Date: 18/04/23
description: Server for CameRAND secure chat, for now requires a directory named server_keys in the
current working directory
"""

import socket
import select
from Crypto.PublicKey import RSA
from AES_new import AesNew

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
    main loop, checks for new connections, errors, disconnects and messages (in this order), also makes secure
    connections using an SSH key pair and an AES encryption. appends clients names to messages.
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
                    open_client_sockets.append(client_socket)
                    print("new client added")
                    break
                else:
                    # receive data
                    data = protocol_read(current_socket)
                    if data == 0:
                        open_client_sockets.remove(current_socket)
                        if current_socket in client_addrs.keys():
                            name = client_addrs[current_socket]
                            print("client %s disconnected" % name)
                            client_addrs.pop(current_socket)
                            if open_client_sockets:
                                data = name + " has left the chat."
                                send_available(open_client_sockets)
                                for i in open_client_sockets:
                                    enc_msg = client_keys[i].encrypt(data.encode())
                                    i.send(protocol_encode(enc_msg, "bin"))
                        if current_socket in client_keys.keys():
                            client_keys.pop(current_socket)
                        current_socket.close()

                    elif data == 1:
                        current_socket.send(protocol_encode(str(private.e)))
                        current_socket.send(protocol_encode(str(private.n)))
                        en_key = int(protocol_read(current_socket))
                        key = pow(en_key, private.d, private.n)
                        nonce = protocol_read(current_socket)
                        cipher = AesNew(int_to_bytes(key), nonce)
                        client_keys.update({current_socket: cipher})
                        name_enc = protocol_read(current_socket)
                        name = cipher.decrypt(name_enc).decode()
                        client_addrs.update({current_socket: name})
                        others = []
                        others.extend(open_client_sockets)
                        others.remove(current_socket)
                        if others:
                            data = name + " has entered the chat."
                            send_available(others)
                            for i in others:
                                enc_msg = client_keys[i].encrypt(data.encode())
                                i.send(protocol_encode(enc_msg, "bin"))
                    # check if connection was aborted
                    elif data == "" or data == b'':
                        # socket was closed
                        open_client_sockets.remove(current_socket)
                        current_socket.close()
                    else:
                        assert current_socket in client_keys.keys()
                        msg = client_keys[current_socket].decrypt(data).decode()
                        data = client_addrs[current_socket] + ": " + msg
                        send_available(open_client_sockets)
                        for i in open_client_sockets:
                            enc_msg = client_keys[i].encrypt(data.encode())
                            i.send(protocol_encode(enc_msg, "bin"))
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
    elif len == '%in':  # name message prefix
        return 'n'
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


def send_available(open_client_sockets):
    """
    function to check if all sockets are open to send a message to
    :param open_client_sockets: a list of sockets to check
    """
    rlist, wlist, xlist = select.select(open_client_sockets,
                                        open_client_sockets, open_client_sockets, 0.01)
    for err in xlist:
        open_client_sockets.remove(err)
        err.close()
    while len(wlist) != len(open_client_sockets):  # check if all sockets are available (wlist)
        rlist, wlist, xlist = select.select(open_client_sockets,
                                            open_client_sockets, open_client_sockets, 0.01)
        for err in xlist:
            open_client_sockets.remove(err)
            err.close()


def abort(sockets):
    """
    function to close all sockets
    :param sockets: list of sockets to close
    """
    for i in sockets:
        i.close()


if __name__ == '__main__':
    main()
