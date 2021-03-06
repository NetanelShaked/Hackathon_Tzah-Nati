import socket
import struct
import getch
import time

if __name__ == '__main__':
    MAGIC_COOKIE = -17973521
    MAGIC_KIND = 2

    UDP_PORT = 13117

    while True:
        try:
            # Start looking for breadcast invitation
            print("Client started, listening for offer requests...")
            cache_anointment = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            cache_anointment.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            cache_anointment.bind(('', UDP_PORT))
            stop = False
            data = None
            # this loop define to catch only a broadcast message packing by struct pack, and starting with magicCooky
            while not stop:
                data, addr = cache_anointment.recvfrom(1024)
                if data is None:
                    continue
                try:
                    msg_rec = struct.unpack('ibh', data)
                    if msg_rec[0] == MAGIC_COOKIE and msg_rec[1] == MAGIC_KIND:
                        stop = True
                except:
                    continue
            cache_anointment.close()
            print("Received offer from " + str(addr[0]) + " attempting to connect...")
            portnum = msg_rec[2]
            print("Port num " + str(int(portnum)))
            try:
                tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_socket.settimeout(3)
                tcp_socket.connect((addr[0], portnum))
                tcp_socket.settimeout(10)
                # Sending our group-name
                tcp_socket.sendall(bytes("KeysCannon", "utf-8"))
                tcp_socket.settimeout(10)
                server_message = tcp_socket.recv(1024)
                print(server_message.decode("utf-8"))
            except:
                print("Connection failed, trying again.")
                continue
            server_message = None
            timer = time.time()
            # This loop will iterate until server send some message or 10.5 second is done
            while server_message is None and time.time() - timer < 10.5:
                message = getch.getche()
                try:
                    tcp_socket.sendall(bytes(message, "utf-8"))
                    tcp_socket.settimeout(0.00001)
                    server_message = tcp_socket.recv(1024)
                except socket.timeout:
                    pass
                except ConnectionAbortedError:
                    server_message = bytes("your computer was delay, tcp connection is gone", "utf-8")
                except:
                    server_message = bytes("unreason error", "utf-8")
            print(server_message.decode("utf-8"))
            tcp_socket.close()
        except:
            pass
