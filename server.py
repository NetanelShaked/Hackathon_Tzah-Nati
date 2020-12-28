import socket
import struct
import threading
import time
import concurrent.futures


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
    answer = bytes("************** you hit " + str(char_counter) + " chars **************", "utf-8")
    clientsocket.sendall(answer)
    return char_counter


if __name__ == '__main__':
    group_name1, group_name2 = '', ''
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
    tcp_socket.bind(('', PORT_NUM))
    tcp_socket.listen(2)
    with concurrent.futures.ThreadPoolExecutor(2) as executor:
        while True:
            (clientsocket_1, address_1) = tcp_socket.accept()
            group_name1 = clientsocket_1.recv(1024).decode("utf-8")

            print("Player 1 connected, waiting to Player 2 \n group name : " + group_name1)

            (clientsocket_2, address_2) = tcp_socket.accept()
            group_name2 = clientsocket_2.recv(1024).decode("utf-8")
            print("Player 2: %s is connected, starting game!" % group_name2)

            time.sleep(10)

            start_message = bytes(
                "Welcome to Keyboard Spamming"
                " Battle Royale.\nGroup 1:\n==\n" + group_name1 + "\n\nGroup "
                                                                  "2:\n==\n" + group_name2 + "\n"
                                                                                             "\nStart pressing keys on "
                                                                                             "your keyboard as fast as "
                                                                                             "you can!!",
                "utf-8")
            clientsocket_1.sendall(start_message)
            clientsocket_2.sendall(start_message)

            game1 = executor.submit(start_new_game, clientsocket_1)
            game2 = executor.submit(start_new_game, clientsocket_2)

            game1_result = game1.result()
            game2_result = game2.result()

            if game1_result == game2_result:
                print("TEKO")
            elif game1_result > game2_result:
                print("Player 1 is winner")
            else:
                print("Player 2 is winner")

            clientsocket_2.close()
            clientsocket_1.close()
