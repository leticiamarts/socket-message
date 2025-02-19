import socket # biblioteca padrão do Python para comunicação em rede
import threading # biblioteca para permitir múltiplos clientes simultaneamente
# threading permite rodar várias funções ao mesmo tempo de maneira independente.
from dotenv import load_dotenv
import os
import time

# Sockets -> pontos finais de comunicação. Como toda comunicação envolve duas extremidades, temos: o Socket do Cliente e o Socket do Se

# carrega as variáveis do arquivo .env
load_dotenv()
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

clients = [] # lista para armazenar clientes conectados
shutdown_event = threading.Event() # evento para controlar o encerramento do servidor

# função para gerenciar a conexão com um cliente específico
def manage_client(conn, addr): # conn = novo socket q representa a conexão entre cliente e servidor, addr = (ip, porta)
    print(f"[NEW CONNECTION] Client found: {addr}", flush=True)
    clients.append(conn) # adiciona cliente a lista de conexões ativas
    while not shutdown_event.is_set(): # loop para troca de mensagens - enquanto server estiver ativo
        try:
            message = conn.recv(1024).decode('utf-8').strip() # recebe msg do cliente
            if not message: # se nao houver msg, encerra a conexão
                break

            print(f"[{addr}] {message}", flush=True) # exibe mensagem do cliente

            response = f"Message received: {message}" # responde ao cliente confirmando recebimento da mensagem
            conn.send(response.encode('utf-8'))

        # exceptions:
        except ConnectionResetError: # caso a conexão seja interrompida
            print(f"[ERROR] Connection to {addr} has been interrupted.", flush=True)
            break
        except Exception as e:
            print(f"[ERROR] An error occurred: {e}", flush=True)
            break

    conn.close() # fecha a conexão
    clients.remove(conn) # remove cliente da lista de conexões ativas
    print(f"[DISCONNECTED] Client {addr} disconnected", flush=True)

# alguns tratamentos para comunicação mais fluida entre cliente e servidor
def wait_for_shutdown(server_socket): # função agurda um comando de desligamento de server
    while True:
        command = input() # aguarda comando no terminal
        if command.lower() == 'shutdown': # caso o comando seja "shutdown", o servidor se encerra
            print("[SHUTTING DOWN] Server is shutting down...", flush=True)
            shutdown_event.set() # aviso para encerramento dos subprocessos
            
            for conn in clients: # envia comunicado de desligamento aos clientes
                try:
                    conn.send("Host desconectando...".encode('utf-8'))
                except:
                    continue

            time.sleep(1)

            for conn in clients: # fecha conexões ativas
                try:
                    conn.close()
                except:
                    continue
            
            server_socket.close() # fecha o socket por parte do server
            print("[SERVER CLOSED] Server has been shut down gracefully.", flush=True)
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria um socket TCP/IP usando o protocolo IPV4
    server.bind((HOST, PORT)) # associa o socket ao IP e porta específicos
    server.listen() # servidor entra em modo escuta para conexões de clientes
    print(f"[WAITING CONNECTION] Server listening at {HOST}:{PORT}", flush=True)
    
    # cria uma thread para aguardar o comando de desligamento (thread permite que mais de uma função seja executada ao mesmo tempo)
    shutdown_thread = threading.Thread(target=wait_for_shutdown, args=(server,))
    shutdown_thread.start()
    
    while not shutdown_event.is_set(): # entquanto server nao for encerrado
        try:
            server.settimeout(1.0)
            conn, addr = server.accept() # recebe conexão do cliente
            thread = threading.Thread(target=manage_client, args=(conn, addr)) # cria uma thread para gerenciar esse cliente específico
            # para que o manage_client seja executado em paralelo com outras funções (inclusive outros manage_client)
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}", flush=True)
        except socket.timeout: # se o tempo limite expirar, continua verificando o estado do server
            continue
        except OSError: # se cair em algum erro (ou for encerrado), encerra o loop
            break

    print("[SERVER CLOSED] Server socket has been closed.", flush=True)

if __name__ == "__main__":
    start_server()
