import socket
import struct
import threading
import time
import concurrent.futures
import random
import multiprocessing


def send_broadcast_suggestion(socket_udp):
    """

    :param socket_udp: udp_socket object
    :return:
    """
    message = struct.pack('Ibh', 0xfeedbeef, 0x2, 5112)
    socket_udp.sendto(message, ("172.1.0.255", 13117))


def thread_send_Announcements(socket_udp):
    threading.Timer(1.0, thread_send_Announcements, args=[socket_udp]).start()
    send_broadcast_suggestion(socket_udp)


def get_all_tcp_connection(tcpSocket):
    tcp_connectios = []
    cur_time = time.time()
    while time.time() - cur_time < 10:
        try:
            tcpSocket.settimeout(0.2)
            (clientside, address) = tcpSocket.accept()
            group_name = clientside.recv(1024).decode("utf-8")
            tcp_connectios.append((clientside, group_name))
            print("THZAAAAAAAAAAAAAAAAAAAAAAAAAAAGH")
        except:
            pass
    return tcp_connectios


def start_new_game(clientside):
    start_time = time.time()
    char_counter = 0
    while time.time() - start_time < 10:
        clientside.settimeout(10)
        try:
            message = clientside.recv(1024)
            char_counter += len(message)
        except:
            pass
    print(char_counter)
    # answer = bytes("************** you hit " + str(char_counter) + " chars **************", "utf-8")
    # clientside.sendall(answer)
    return char_counter


if __name__ == '__main__':
    sockets_list = []
    SERVER_IP = socket.gethostname()
    PORT_NUM = 5112
    print("Server started,listening on IP address 172.1.0.3")
    upd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # upd_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sending_suggestions_thread = multiprocessing.Process(target=thread_send_Announcements, args=(upd_socket,))
    sending_suggestions_thread.start()
    # while True:
    #     pass
    tcp_open=False
    while not tcp_open:
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.bind(('', PORT_NUM))
            tcp_socket.listen()
            tcp_open=True
        except OSError:
            print ("SOME DID SOMETHING NASTY AND STOLL MY PORT!!")
        
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            # tcp_socket.settimeout(30)
            # (clientside, address_1) = tcp_socket.accept()
            # group_name = clientside.recv(1024).decode("utf-8")
            # sockets_list.append((clientside, group_name))
            # print("Player 1 connected, waiting to Player 2 \ngroup name : " + group_name)
            #
            # (clientside, address_2) = tcp_socket.accept()
            # group_name = clientside.recv(1024).decode("utf-8")
            # sockets_list.append((clientside, group_name))
            # print("Player 2 connected, waiting to Player 3 \ngroup name : " + group_name)
            #
            # (clientside, address_1) = tcp_socket.accept()
            # group_name = clientside.recv(1024).decode("utf-8")
            # sockets_list.append((clientside, group_name))
            # print("Player 3 connected, waiting to Player 4 \ngroup name : " + group_name)
            #
            # (clientside, address_2) = tcp_socket.accept()
            sockets_list = get_all_tcp_connection(tcp_socket)
            # time.sleep(10)
            if len(sockets_list) < 2:
                continue
            sending_suggestions_thread.terminate()
            #
            # group_name = clientside.recv(1024).decode("utf-8")
            # sockets_list.append((clientside, group_name))
            # print("Last group is in, group name is " + group_name)

            # time.sleep(10)

            random.shuffle(sockets_list)

            # buddies1 = sockets_list[0][1] + " \n " + sockets_list[1][1]
            # buddies2 = sockets_list[2][1] + " \n " + sockets_list[3][1]
            buddies1 = sockets_list[:len(sockets_list) // 2]
            buddies2 = sockets_list[len(sockets_list) // 2:]
            buddies1_names = '\n'.join([name for socket, name in buddies1])
            buddies2_names = '\n'.join([name for socket, name in buddies2])
            start_message = bytes(
                "Welcome to Keyboard Spamming"
                " Battle Royale.\nGroup 1:\n==\n" + buddies1_names + "\n\nGroup "
                                                                     "2:\n==\n" + buddies2_names + "\n"
                                                                                                   "\nStart pressing keys on "
                                                                                                   "your keyboard as fast as "
                                                                                                   "you can!!",
                "utf-8")

            for client, group_name in sockets_list:
                client.sendall(start_message)

            # game1 = executor.submit(start_new_game, sockets_list[0][0])
            # game2 = executor.submit(start_new_game, sockets_list[1][0])
            # game3 = executor.submit(start_new_game, sockets_list[2][0])
            # game4 = executor.submit(start_new_game, sockets_list[3][0])
            #
            # game1_result = game1.result()
            # game2_result = game2.result()
            # game3_result = game3.result()
            # game4_result = game4.result()
            game = []
            results = []

            for socket, group in sockets_list:
                game.append(executor.submit(start_new_game, socket))

            for i in range(len(sockets_list)):
                results.append(game[i].result())

            buddies1_result = sum(results[:len(sockets_list) // 2])
            buddies2_result = sum(results[len(sockets_list) // 2:])
            buddies1_string_for_result_message = ' & '.join([name for socket, name in buddies1])
            buddies2_string_for_result_message = ' & '.join([name for socket, name in buddies2])
            result_message = buddies1_string_for_result_message + " get " + str(
                buddies1_result) + " points\n" \
                             + buddies2_string_for_result_message + " get " + str(
                buddies2_result) + " points\n"

            if buddies1_result == buddies2_result:
                print("TEKO")
                result_message = bytes(result_message + "All Buddies get the same score, it a TEKO!", "utf-8")

            elif buddies1_result > buddies2_result:
                print("Buddies 1 is winner")
                result_message = bytes(result_message +
                                       buddies1_string_for_result_message + " win\n" + buddies2_string_for_result_message + " loss",
                                       "utf-8")

            else:
                print("Buddies 2 is winner")
                result_message = bytes(result_message +
                                       buddies2_string_for_result_message + " win\n" + buddies1_string_for_result_message + " loss",
                                       "utf-8")

            for client, group_name in sockets_list:
                client.sendall(result_message)
                client.close()

            sending_suggestions_thread = multiprocessing.Process(target=thread_send_Announcements, args=(upd_socket,))
            sending_suggestions_thread.start()
