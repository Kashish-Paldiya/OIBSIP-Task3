import socket
import threading

HOST='127.0.0.1'
PORT=1234
LISTENER_LIMIT=5
active_clients=[]


def listen_for_messages(client,username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            msg = username + '~' + message
            send_messages(msg)
        else:
            print(f"The message send from client {username} is empty.")

def send_messages(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

    
def send_message_to_client(client, message):
    client.sendall(message.encode())



def client_handle(client):
    #server will listen for client message that will contain username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            break
        else:
            print("Client username is empty..")
    threading.Thread(target=listen_for_messages, args=(client,username, )).start()


def main():
    #Creating the socket class object
    #AF_INET: using IPv4 addresses
    #SOCK_STREAM : Using TCP packets  for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        #provide the server with an address in the form of hot IP and port
        server.bind((HOST,PORT))
        print(f"Running the server on {HOST}--{PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    #Set server limit
    server.listen(LISTENER_LIMIT)

    #Listening to client connections
    while 1:
        client,address = server.accept()
        print(f"Successfully connected to Client  {address[0]}--{address[1]}")

        threading.Thread(target=client_handle,args=(client, )).start()



if __name__ == "__main__":
    main()