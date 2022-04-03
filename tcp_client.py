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
    try:
        quit = False
    
        while not quit:
            
            client_message = input(">>>")
            client.send(client_message.encode("utf-8"))
            
    except:    
        client.close()   
            
    
def read_server_response(client):
    try:
        quit = False
        client_time = time.strftime("%d-%m-%Y / %H:%M:%S", time.localtime())
        while not quit:
            message = client.recv(2048)
            message = message.decode('utf-8')
            
            print( f'{client_time} :', f'{message}')
    except ConnectionAbortedError:
        print('Server connection closed')
        
        
reader = Thread(target=read_server_response, args=(client,))
reader.demon = True
reader.start()

if __name__ == '__main__':
    sending_message(client)
    
    
    