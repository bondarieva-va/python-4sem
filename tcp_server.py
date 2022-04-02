from http import client
import socket
from threading import Thread
import time
import uuid
import bcrypt

host = socket.gethostbyname(socket.gethostname())
port = 4444
 
server = socket.socket(
    
    socket.AF_INET,
    socket.SOCK_STREAM,
    
)

server.bind((host, port)) #резервируем порт

server.listen(5) #сколько соединений ждет
print("Server is listening")

clients =  []

def send_all(message, client_socket): #посылаем сообщение всем клиентам сервера
    for client in clients:
        cs = client.get('uuid')
        if client_socket != cs:
            cs.send(message)

def listen_client(client, time, address, client_socket): #принимаем информацию от клиента
    print("Listening client")
    while True:
        message = client.recv(2048)
        print("[" +address[0]+ "] "+time+" : ",end="")
        print(message.decode("utf-8"))
        send_all(message, client_socket)
        
        
def find_client_by_param(value, param='ip'):
    for user_data in clients:
        if  user_data.get(param) == value:
            return True
    return False

def find_client_data_by_login(value):
    for user_data in clients:
        if  user_data.get('login') == value:
            return user_data
    return {}

def check_if_client_is_on_server(client_socket):
    login = client_socket.recv(1024)
    if find_client_data_by_login(login):
        authorization(client_socket, login)
    else:
        registration(client_socket, login)
    
def authorization(client_socket, login):
    # auth_dict = [{'uuid':"",'login':"", 'password':"", 'history_of_messages':""}, {}] # user_data
    
    if find_client_by_param(value=login, param='login'):
        client_data = find_client_data_by_login(login)
        password = ""
        while client_data.get("password") != password:
            client_socket.send("You are logged in. Enter your password:".encode("utf-8"))
            password = client_socket.recv(1024)
        client_socket.send("Authorization was successful! ".encode("utf-8"))
    else:
        registration(client_socket, login)
        
    
def registration(client_socket,login):
    client_socket.send("No such user exists. Сreate a password for registration: ".encode("utf-8"))
    password = client_socket.recv(1024)
    clients.append(
        {
            'uuid': client_socket,
            'login': login,
            'password': password,
            'history_of_messages': []
        })
    client_socket.send("Registration was successful! ".encode("utf-8"))
    

def start_server():
    quit = True
    while quit == True:
        try:
            client_socket, address = server.accept() #берем клиента из очереди
            client_socket.send("Welcome to pretty server. Enter login ".encode("utf-8"))#оповещаем клиента, что он законектился
            
            check_if_client_is_on_server(client_socket)
            
            print(f"Client <{address[0]}> connected!") #Выводим информацию на сервере, что подсоединился клиент с [ip]
            
            server_time = time.strftime("%d-%m-%Y / %H:%M:%S", time.localtime())
        
            Thread(target=listen_client, args=(client_socket,server_time,address,client_socket,)).start()
            
        except KeyboardInterrupt:
            print("\n[Server stopped]")
            server.close()   
            quit = False 
        
          
if __name__ == '__main__':
    start_server()