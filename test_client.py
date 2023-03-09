"""
Author: Nir Dweck
Date: 25/10/21
Description: a SSL client
"""
import socket
import ssl

HOST_NAME = '127.0.0.1'
PORT = 8443
MSG_LEN = 1024
EXIT_CMD = 'by by'
USER_INPUT = 'please enter a command'


def main():
    """
    creates a secure connection with the server, receives commands, sends them ot the server and receives a response
    from the server.
    exits when receives the 'by by' response
    :return: None
    """
    # create the ssl context
    context = ssl.create_default_context()
    # allow self signed certificate
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    my_socket = socket.socket()
    conn = context.wrap_socket(my_socket, server_hostname=HOST_NAME)
    try:
        conn.connect((HOST_NAME, PORT))
        msg = input(USER_INPUT)
        while True:
            conn.send(msg.encode())
            answer = conn.read(MSG_LEN).decode()
            print(answer)
            if answer == EXIT_CMD:
                break
            msg = input(USER_INPUT)
        print('exiting')
    except socket.error as sock_err:
        print(sock_err)
    finally:
        conn.close()


if __name__ == '__main__':
    main()