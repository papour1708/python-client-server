import socket
import threading

# Configuration du client
HOST = '127.0.0.1'  # Adresse IP du serveur
PORT = 9999  # Port d'écoute du serveur

# Fonction de réception des messages du serveur
def receive_messages(client_socket):
    while True:
        try:
            # Réception des données du serveur
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(data)
        except:
            # Déconnexion en cas d'erreur
            print('Connexion au serveur perdue.')
            break

# Fonction principale du client
def main():
    # Connexion au serveur
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print('Connecté au serveur.')

    # Création d'un thread pour recevoir les messages du serveur
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Envoi des messages au serveur
    while True:
        message = input()
        client_socket.sendall(message.encode('utf-8'))

if __name__ == '__main__':
    main()
