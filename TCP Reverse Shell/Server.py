import socket
import sys


def connect(server_ip, server_port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, server_port))
        server.listen(1)
        print("Listening for incoming connection on {0}:{1}".format(server_ip, server_port))
        conn, addr = server.accept()
        print("[+] Got connection from {}:{}".format(addr[0], addr[1]))

        while True:
            command = input("Shell> ")
            if command.strip() == "":
                continue
            try:
                if command.strip() == "exit":
                    conn.close()
                    server.close()
                    break
                else:
                    conn.send(command.encode())
                    print((conn.recv(1024)).decode())
            except KeyboardInterrupt:
                print("\nPressed CTRL+C")
                conn.close()
                server.close()
                sys.exit(0)

    except KeyboardInterrupt:
        print("\nPressed CTRL+C")
        conn.close()
        server.close()
        sys.exit(0)
    except Exception as e:
        print(f"Exception occurred: {e}")
        conn.close()
        server.close()
        sys.exit(1)


def main():
    server_ip = "127.0.0.1"
    server_port = 9999
    connect(server_ip, server_port)


if __name__ == "__main__":
    main()
