import socket


def send_broadcast_suggestion(socket_udp):
    messege = bytes("offerAnnounment","utf-8")
    socket_udp.sendto(messege, ("<broadcast>",5012))

if __name__ == '__main__':
    print("Server started,listening on IP address 172.1.0.3")
    upd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        send_broadcast_suggestion(upd_socket)