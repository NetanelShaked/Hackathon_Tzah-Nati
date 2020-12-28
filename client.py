import socket

if __name__ == '__main__':
    print("Client started, listening for offer requests...")
    UDP_IP = '255.255.255.255'
    UPD_PORT = 5012
    cache_anointment = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cache_anointment.bind((UDP_IP, UPD_PORT))
    addr = None
    while addr is not None:
        data, addr = cache_anointment.recvfrom(1024)
    cache_anointment.close()

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect(addr)

