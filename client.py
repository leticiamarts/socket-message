import socket
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"[CONNECTED] Connected to server at {HOST}:{PORT}")

    try:
        while True:
            message = input("You: ")
            if message.lower() == 'exit':
                print("[DISCONNECTING] Ending connection...")
                client.close()
                break
            client.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("\n[DISCONNECTED] Client disconnected.")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
