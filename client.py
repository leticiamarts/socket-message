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

            server_response = client.recv(1024).decode('utf-8')
            if server_response == "Host desconectando...":
                print(f"[SERVER] {server_response} Desconectando agora.")
                client.close()
                break
            print(f"[SERVER] {server_response}")

    except ConnectionResetError:
        print("\n[ERROR] Connection lost. Server might be down.")
    except KeyboardInterrupt:
        print("\n[DISCONNECTED] Client disconnected.")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
