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
    socket_udp.sendto(message, ("172.1.255.255", 13117))


def thread_send_Announcements(socket_udp):
    threading.Timer(1.0, thread_send_Announcements, args=[socket_udp]).start()
    send_broadcast_suggestion(socket_udp)


def get_all_tcp_connection(tcpSocket):
    """

    :param tcpSocket: pointer to our tcp server socket
    :return: list of tuples (Socket, group_name) for each client connected to our tcp server
    """
    tcp_connections = []
    cur_time = time.time()
    while time.time() - cur_time < 10:
        try:
            tcpSocket.settimeout(0.2)
            (clientside, address) = tcpSocket.accept()
            group_name = clientside.recv(1024).decode("utf-8").split('\n')[0]
            tcp_connections.append((clientside, group_name))
            print(group_name + " is connected")
        except:
            pass
    return tcp_connections


def start_new_game(clientside):
    start_time = time.time()
    char_counter = 0
    while time.time() - start_time < 10:
        try:
            clientside.settimeout(0.1)
            message = clientside.recv(1024)
            char_counter += len(message)
        except:
            pass
    print(char_counter)
    return char_counter


if __name__ == '__main__':
    sockets_list = []
    SERVER_IP = socket.gethostname()
    PORT_NUM = 5112

    print("Server started,listening on IP address 172.1.0.3")

    upd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    upd_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sending_suggestions_thread = multiprocessing.Process(target=thread_send_Announcements, args=(upd_socket,))
    sending_suggestions_thread.start()

    tcp_open = False
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    group_score = {}
    # Starting our tcp server
    while not tcp_open:
        try:
            tcp_socket.bind(('', PORT_NUM))
            tcp_socket.listen()
            tcp_open = True
        except OSError:
            print("SOMEONE DID SOMETHING NASTY AND STOLE MY PORT!!")
            time.sleep(1)


    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            try:

                print("Waiting for participation")
                sockets_list = get_all_tcp_connection(tcp_socket)
                if len(sockets_list) < 2:
                    if len(sockets_list)==1:
                        sockets_list[0][0].sendall(bytes("You are alone in this game, server restart and waiting again for connections",
                                                      "utf-8"))
                        sockets_list[0][0].close()
                    continue
                sending_suggestions_thread.terminate()



                random.shuffle(sockets_list)


                buddies1 = sockets_list[:len(sockets_list) // 2]
                buddies2 = sockets_list[len(sockets_list) // 2:]
                buddies1_names = '\n'.join([name for socket, name in buddies1])
                buddies2_names = '\n'.join([name for socket, name in buddies2])

                start_message = bytes(
                    "\033[93m"+"\033[01m"+"Welcome to Keyboard Spamming Battle Royale.\n"+"\033[35m"+"\033[01m"+"Group"
                    "1:\n==\n" + buddies1_names + "\n\n\033[33m"+"\033[01m"+"Group "
                                                  "2:\n==\n" + buddies2_names + "\n\n\033[93m"+"\033[01m"+"Start pressing keys on your keyboard "
                                                                                "as "
                                                                                "fast as you can!!\033[0m",
                    "utf-8")

                for client, group_name in sockets_list:
                    client.sendall(start_message)


                game = []
                results = []

                for socket, group in sockets_list:
                    game.append(executor.submit(start_new_game, socket))

                for i in range(len(sockets_list)):
                    results.append(game[i].result())
                    group_score[sockets_list[i][1]] = max(group_score.get(sockets_list[i][1], 0), results[i])
                buddies1_result = sum(results[:len(sockets_list) // 2])
                buddies2_result = sum(results[len(sockets_list) // 2:])
                buddies1_string_for_result_message = ' & '.join([name for socket, name in buddies1])
                buddies2_string_for_result_message = ' & '.join([name for socket, name in buddies2])
                result_message_buddies1 = buddies1_string_for_result_message + " get " + str(
                    buddies1_result) + " points\n"
                result_message_buddies2 = buddies2_string_for_result_message + " get " + str(
                    buddies2_result) + " points\n"

                if buddies1_result == buddies2_result:
                    print("TEKO")
                    result_message = bytes("\033[35m"+"\033[01m"+result_message_buddies1 +  "\n\n\033[33m"+"\033[01m" +
                                           result_message_buddies2 + "\033[93m"+"\033[01m" + "All Buddies get the same score, it a TEKO!" +
                                           "\033[0m", "utf-8")

                elif buddies1_result > buddies2_result:
                    print("Buddies 1 is winner")
                    result_message = bytes("\033[35m"+"\033[01m"+result_message_buddies1 + "\n\n\033[33m"+"\033[01m" +
                                           result_message_buddies2 + "\033[32m"+"\033[01m" +
                                           buddies1_string_for_result_message + " win\n" + "\033[12m"+"\033[01m"+ buddies2_string_for_result_message + " loss" + "\033[0m",
                                           "utf-8")

                else:
                    print("Buddies 2 is winner")
                    result_message = bytes("\033[35m"+"\033[01m"+result_message_buddies1 + "\n\n\033[33m"+"\033[01m" +
                                           result_message_buddies2 + "\033[32m"+"\033[01m" +
                                           buddies2_string_for_result_message + " win\n" + "\033[31m"+"\033[01m" + buddies1_string_for_result_message + " loss" + "\033[0m",
                                           "utf-8")

                statics = "\033[93m"+"\033[01m"+"\nbuddies 1 typed : " + str(buddies1_result / 10) + " per sec\nbuddies 2 typed : " + str(
                    buddies2_result / 10) + " per sec" + "\033[0m"
                mvp = "\033[93m"+"\033[01m" + "\nThe MVP is: " + [sockets_list[i][1] for i in range(len(results)) if results[i] == max(results)][
                    0] + " with: "+ str(max(group_score.values()))+ " chars!!!!" + "\033[0m"
                best_group_name=[group_name for group_name, score in group_score.items() if score == max(group_score.values())]
                if len(best_group_name)>0:
                    best_group = "\033[93m"+"\033[01m" + "\nbest group ever is " + best_group_name[0] + "\033[0m"
                else:
                    best_group=""


                result_message += bytes(statics + mvp + best_group,"utf-8")

                for client, group_name in sockets_list:
                    client.sendall(result_message)
                    client.close()

                sending_suggestions_thread = multiprocessing.Process(target=thread_send_Announcements, args=(upd_socket,))
                sending_suggestions_thread.start()
            except:
                pass
