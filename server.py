import socket
import struct
import threading
import time


def send_broadcast_suggestion(socket_udp):
    message = struct.pack('Ibh', 0xfeedbeef, 0x2, 5112)
    socket_udp.sendto(message, ("<broadcast>", 13117))


def thread_send_enouncments(socket_udp):
    threading.Timer(1.0, thread_send_enouncments, args=[socket_udp]).start()
    send_broadcast_suggestion(upd_socket)


def start_new_game(clientsocket):
    print(clientsocket)
    start_time = time.time()
    char_counter = 0
    while time.time() - start_time < 10:
        clientsocket.settimeout(10)
        try:
            message = clientsocket.recv(1024)
            char_counter += len(message)

        except:
            pass
    print(char_counter)
    answer=bytes("you hit"+str(char_counter)+" chars","utf-8")
    clientsocket.sendall(answer)
    clientsocket.close()


if __name__ == '__main__':
    SERVER_IP = socket.gethostname()
    PORT_NUM = 5112
    print("Server started,listening on IP address 172.1.0.3")
    upd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    upd_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sending_segestions_thread = threading.Thread(target=thread_send_enouncments, args=[upd_socket])
    sending_segestions_thread.start()
    # while True:
    #     pass
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((SERVER_IP, PORT_NUM))
    tcp_socket.listen(2)
    while True:
        (clientsocket, address) = tcp_socket.accept()
        game = threading.Thread(target=start_new_game, args=[clientsocket])
        game.start()
