import socket
from threading import Thread
import time

host = socket.gethostbyname(socket.gethostname())
port = 4444

client = socket.socket(
    
    socket.AF_INET,
    socket.SOCK_STREAM,
    
)

client.connect((host, port))


def sending_message(client):
    quit = False
    client_time = time.strftime("%d-%m-%Y / %H:%M:%S", time.localtime())
    while not quit:
        try:
            client_message = input(">>>")
            client.send(client_message.encode("utf-8"))
            print(f"{client_time} : {client_message} ")
        except KeyboardInterrupt:
            print("\n[Connection to client stopped]")
            client.close()   
            quit = False 
            
    
def read_server_response(client):
    quit = False
    while not quit:
        message = client.recv(2048)
        print(message.decode("utf-8"))
    
    
Thread(target=read_server_response, args=(client,)).start()
Thread(target=sending_message, args=(client,)).start()
    
    