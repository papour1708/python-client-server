#Voici un exemple de code Python utilisant les sockets pour créer un système client-serveur permettant à plusieurs utilisateurs de se connecter au serveur et de communiquer entre eux.
import socket
import threading

# Configuration du serveur
HOST = '127.0.0.1'  # Adresse IP du serveur
PORT = 9999  # Port d'écoute du serveur

# Création du socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Liste des clients connectés
clients = []
clients_lock = threading.Lock()

# Fonction de gestion des clients
def handle_client(client_socket, client_address):
    while True:
        try:
            # Réception des données du client
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                # Transmission des données aux autres clients
                with clients_lock:
                    for client in clients:
                        if client != client_socket:
                            client.sendall(data.encode('utf-8'))
            else:
                # Déconnexion du client
                with clients_lock:
                    clients.remove(client_socket)
                    print('Client {} déconnecté.'.format(client_address))
                    break
        except:
            # Déconnexion du client en cas d'erreur
            with clients_lock:
                clients.remove(client_socket)
                print('Client {} déconnecté.'.format(client_address))
            break

# Fonction principale du serveur
def main():
    server_socket.listen(5)
    print('Le serveur écoute sur {}:{}'.format(HOST, PORT))

    while True:
        # Attente d'une connexion client
        client_socket, client_address = server_socket.accept()
        print('Nouvelle connexion de :', client_address)

        # Ajout du client à la liste des clients
        with clients_lock:
            clients.append(client_socket)

        # Création d'un thread pour gérer le client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == '__main__':
    main()
