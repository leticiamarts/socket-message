import socket # biblioteca padrão do Python para comunicação em rede
from dotenv import load_dotenv
import os

# carrega as variáveis do arquivo .env
load_dotenv()
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

def start_client():
    # cria um socket TCP/IP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """
    socket.AF_INET: especifica que o protocolo IPv4 (endereço IP + porta) está sendo usado
    socket.SOCK_STREAM: indica que o socket será do tipo TCP (Transmission Control Protocol)
    """
    # conecta ao servidor no IP e porta específicas
    client.connect((HOST, PORT)) # socket local é criado para cliente. Quando cliente pede para se conectar a um servidor, o SO escolhe uma porta para o cliente
    print(f"[CONNECTED] Connected to server at {HOST}:{PORT}")

    try:
        while True: # loop para troca de mensagens
            message = input("You: ") # solicita mensagem a usuário
            if message.lower() == 'exit': # se "exit" for digitado, a conexão se encerra
                print("[DISCONNECTING] Ending connection...")
                client.close() # fecha o socket
                break
            client.send(message.encode('utf-8')) # envia mensagem (codificada) ao server

            server_response = client.recv(1024).decode('utf-8') # aguarda resposta do server
            if server_response == "Host desconectando...": # se a resposta do server for uma mensagem de desconexão, o client encerra
                print(f"[SERVER] {server_response} Desconectando agora.")
                client.close()
                break
            print(f"[SERVER] {server_response}")

    # tratamento de exceções:
    except ConnectionResetError: # tratamento caso o servidor se desconecte de forma inesperada
        print("\n[ERROR] Connection lost. Server might be down.")
    except KeyboardInterrupt: # tratamento caso "ctrl + c" seja pressionado para encerramento
        print("\n[DISCONNECTED] Client disconnected.")
    finally: # finaliza o socket ao sair
        client.close()

if __name__ == "__main__":
    start_client()
