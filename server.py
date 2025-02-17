import socket
import threading
from dotenv import load_dotenv
import os
import time

load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

clients = []
shutdown_event = threading.Event()

def manage_client(conn, addr):
    print(f"[NEW CONNECTION] Client found: {addr}", flush=True)
    clients.append(conn)
    while not shutdown_event.is_set():
        try:
            message = conn.recv(1024).decode('utf-8').strip()
            if not message:
                break
            print(f"[{addr}] {message}", flush=True)

            response = f"Message received: {message}"
            conn.send(response.encode('utf-8'))

        except ConnectionResetError:
            print(f"[ERROR] Connection to {addr} has been interrupted.", flush=True)
            break
        except Exception as e:
            print(f"[ERROR] An error occurred: {e}", flush=True)
            break

    conn.close()
    clients.remove(conn)
    print(f"[DISCONNECTED] Client {addr} disconnected", flush=True)

def wait_for_shutdown(server_socket):
    while True:
        command = input()
        if command.lower() == 'shutdown':
            print("[SHUTTING DOWN] Server is shutting down...", flush=True)
            shutdown_event.set()
            
            for conn in clients:
                try:
                    conn.send("Host desconectando...".encode('utf-8'))
                except:
                    continue

            time.sleep(1)

            for conn in clients:
                try:
                    conn.close()
                except:
                    continue
            
            server_socket.close()
            print("[SERVER CLOSED] Server has been shut down gracefully.", flush=True)
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[WAITING CONNECTION] Server listening at {HOST}:{PORT}", flush=True)
    
    shutdown_thread = threading.Thread(target=wait_for_shutdown, args=(server,))
    shutdown_thread.start()
    
    while not shutdown_event.is_set():
        try:
            server.settimeout(1.0)
            conn, addr = server.accept()
            thread = threading.Thread(target=manage_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}", flush=True)
        except socket.timeout:
            continue
        except OSError:
            break

    print("[SERVER CLOSED] Server socket has been closed.", flush=True)

if __name__ == "__main__":
    start_server()
