"""
Author: Eitan Unger
Date: 27/5/22
description: Client for Cow006, manages graphics, runs for the length of one game then shuts down
"""
import socket
from threading import Event
from tkinter import StringVar
import select


def client_thread(finished: Event, in_list: list, out_list: list):
    """
    The main function- handles the game running
    :return: none
    """
    ip = input("Enter server IP")
    port = input("Enter server port")
    server_socket = socket.socket()
    try:
        server_socket.connect((ip, port))
        while not finished.is_set():
            rlist, wlist, xlist = select.select([server_socket], [server_socket], [server_socket])
            if in_list:
                while len(wlist) != 1:
                    rlist, wlist, xlist = select.select([server_socket], [server_socket], [server_socket])
                for i in in_list:
                    server_socket.send(protocol_encode(i))
                    in_list.remove(i)
            else:
                if rlist:
                    out_list.append(protocol_read(server_socket))
    except socket.error as err:
        print("error: " + str(err))
    finally:
        server_socket.close()

# --------------------------- NETWORK FUNCS ---------------------------


def protocol_encode(line):
    """
    Encodes message according to the protocol (length prefix and type prefix)
    :param line: line to encode
    :return:
    """
    return str(len(line)).zfill(3) + line  # add a 3-digit length prefix for protocol_read()


def protocol_read(socket):
    """
    read the message (exact length) using the protocol
    :param socket: socket to read from
    :return: message read from socket, parsed
    """
    len = socket.recv(3).decode()  # get length
    if len == "" or len == b'':  # check for error
        return len
    return socket.recv(int(len)).decode()  # read the message


if __name__ == '__main__':

