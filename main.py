from threading import Thread
from Client import client
from Server import server


def initiate_clients(url, port):
    """ start the clients running """
    num_clients = 2

    for i in range(num_clients):
        client_thread = Thread(target = client.start, args = (url, port))
        client_thread.start()

def initiate_server(url, port):
    """ start the server running """
    server_thread = Thread(target = server.start, args = (url, port))
    server_thread.start()

def main():
    url = '127.0.0.1'
    port = 8000

    # initiate server
    initiate_server(url, port)

    # initiate clients
    initiate_clients(url, port)
    

if __name__ == "__main__":
    main()
