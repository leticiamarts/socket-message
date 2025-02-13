import socket
import threading
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

def manage_client(conn, addr):
    print(f"[NEW CONNECTION] Client found: {addr}", flush=True)
    while True:
        try:
            message = conn.recv(1024).decode('utf-8').strip()
            if not message:
                break
            print(f"[{addr}] {message}", flush=True)
        except ConnectionResetError:
            print(f"[ERROR] Connection to {addr} has been interrupted.", flush=True)
            break
        except Exception as e:
            print(f"[ERROR] An error occurred: {e}", flush=True)
            break
    conn.close()
    print(f"[DISCONNECTED] Client {addr} disconnected", flush=True)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[WAITING CONNECTION] Server listening at {HOST}:{PORT}", flush=True)
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=manage_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}", flush=True)

if __name__ == "__main__":
    start_server()
