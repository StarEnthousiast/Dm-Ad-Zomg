import requests
import json
import threading
import random
import time
import sys
import websocket
import os
import glob

class SpamThread(threading.Thread):
    def __init__(self, token, channel, messages, delay):
        super().__init__()
        self.token = token
        self.channel = channel
        self.messages = messages
        self.delay = delay
        self.sent_messages = {}

    def run(self):
        channel_id = self.channel["id"]

        while True:
            for message in self.messages:
                send_message(self.token, channel_id, message)
                if channel_id not in self.sent_messages:
                    self.sent_messages[channel_id] = 0
                self.sent_messages[channel_id] += 1  # Increment the sent_messages count
                time.sleep(self.delay)

def on_message(ws, message):
    pass

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def send_message(token, channel_id, message):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Content-Type": "application/json"
    }
    data = {
        "content": message
    }
    requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, data=json.dumps(data))

def start_spamming():
    token_files = glob.glob("tokens/*.json")  # Assuming the JSON files are in a "tokens" directory
    threads = []

    for file in token_files:
        with open(file, encoding='utf-8') as json_file:
            token_data = json.load(json_file)

            for channel in token_data["channels"]:
                thread = SpamThread(token_data["token"], channel, channel["messages"], channel["delay"])
                thread.start()
                threads.append(thread)

    while True:
        os.system("cls")

        for file in token_files:
            with open(file, encoding='utf-8') as json_file:
                token_data = json.load(json_file)
                token = token_data["token"]
                print(f"Token: {token}:")
                
                for i, channel in enumerate(token_data["channels"]):
                    channel_id = channel["id"]
                    message = channel["messages"][0]
                    sent_messages = threads[i].sent_messages.get(channel_id, 0)  # Access the sent_messages count from the thread object
                    print(f"- Channel{i+1}: {channel_id}")
                
                print()

        time.sleep(1)

if __name__ == "__main__":
    start_spamming()
