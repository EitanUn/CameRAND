"""
Author: Nir Dweck
Date: 25/10/21
Description: a SSL server
"""
import socket
import ssl

IP_ADDR = '0.0.0.0'
PORT = 8443
QUEUE_LEN = 1
PACKET_LEN = 1024
CERT_FILE = 'certificate.crt'
KEY_FILE = 'privateKey.key'
MSG = 'have a nice day'
EXIT_CMD = 'exit'
EXIT_RES = 'by by'


def main():
    """
    listens for a single client connection.
    receives commands from the client and answers with a single response.
    once receives the 'exit' command, responses with 'by by' and exit's
    :return: None
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERT_FILE, KEY_FILE)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP_ADDR, PORT))
        server_socket.listen(QUEUE_LEN)
        ssock = context.wrap_socket(server_socket, server_side=True)
        conn, addr = ssock.accept()
        try:
            msg = conn.recv(PACKET_LEN).decode()
            while msg != EXIT_CMD:
                print('received ' + msg)
                conn.send(MSG.encode())
                msg = conn.recv(PACKET_LEN).decode()
            conn.send(EXIT_RES.encode())
            print('exiting')
        except socket.error as sock_err:
            print(sock_err)
        finally:
            conn.close()
    except socket.error as sock_err:
        print(sock_err)
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()