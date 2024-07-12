import socket
import sys
import argparse

def connect(server_ip, server_port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, server_port))
        server.listen(1)
        print(f"Listening for incoming connection on {server_ip}:{server_port}")
        
        conn, addr = server.accept()
        print(f"[+] Got connection from {addr[0]}:{addr[1]}")

        while True:
            command = input("Shell> ")
            if command.strip() == "":
                continue
            try:
                if command.strip().lower() == "exit":
                    print("Closing connection...")
                    conn.close()
                    break
                else:
                    conn.send(command.encode())
                    response = conn.recv(1024).decode()
                    print(response)
            except KeyboardInterrupt:
                print("\nPressed CTRL+C, closing connection...")
                conn.close()
                break

    except KeyboardInterrupt:
        print("\nPressed CTRL+C, shutting down server...")
        server.close()
        sys.exit(0)
    except Exception as e:
        print(f"Exception occurred: {e}")
        conn.close()
        server.close()
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Simple TCP Command Server")
    parser.add_argument('--ip', type=str, default="127.0.0.1", help="Server IP address to bind")
    parser.add_argument('--port', type=int, default=9999, help="Server port to bind")

    args = parser.parse_args()

    connect(args.ip, args.port)

if __name__ == "__main__":
    main()
