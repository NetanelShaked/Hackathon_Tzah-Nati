import socket
import struct


if __name__ == '__main__':
    print("Client started, listening for offer requests...")
    UPD_PORT = 13117
    cache_anointment = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cache_anointment.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    cache_anointment.bind(('', UPD_PORT))
    stop = False
    data = None
    while not stop:
        data, addr = cache_anointment.recvfrom(1024)
        if data is None:
            continue
        try:
            msg_rec = struct.unpack('ibh', data)
            if msg_rec[0] == -17973521 and msg_rec[1] == 2:
                stop = True
        except:
            continue
    cache_anointment.close()
    print("Received offer from " + str(addr[0]) + " attempting to connect...")
    portnum = msg_rec[2]
    print("Port num " + str(int(portnum)))

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((socket.gethostname(), 5112))

    tcp_socket.sendall(bytes("THE TZAH'S", "utf-8"))

    print(tcp_socket.recv(1024).decode("utf-8"))
    server_message = None
    while server_message is None:
        message = input("Enter:")
        tcp_socket.sendall(bytes(message, "utf-8"))
        try:
            tcp_socket.settimeout(0.00001)
            server_message = tcp_socket.recv(1024)
        except:
            pass
    print(server_message.decode("utf-8"))
    tcp_socket.close()
