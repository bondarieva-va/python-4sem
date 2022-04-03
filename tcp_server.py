mport socket
from threading import Thread
import time
import bcrypt
import select
host = socket.gethostbyname(socket.gethostname())
port = 4444
 
server = socket.socket(
    
    socket.AF_INET,
    socket.SOCK_STREAM,
    
)
server.bind((host, port)) #резервируем порт
server.listen(5) #сколько соединений ждет
print('Server is listening')
clients =  []
message_history = []
def add_to_message_history(message):
    if len(message_history) <= 10:
        message_history.append(message)
    else:
        message_history.pop(0)
        message_history.append(message)
    
    
def print_messages(message_history,client_socket):
    for message in message_history:
        time.sleep(0.5)
        client_socket.send(message)
        
        
    
def send_all(message, client_socket): #посылаем сообщение всем клиентам сервера
    for client in clients:
        cs = client.get('uuid')
        if client_socket != cs:
            cs.send(message)
def listen_client(client, time, address, client_socket): #принимаем информацию от клиента
    try:
        print('Listening client')
        while True:
            message = client.recv(2048)
            add_to_message_history(message)
            print("[" +address[0]+ "] "+time+" : ",end="")
            print(message.decode('utf-8'))
            send_all(message, client_socket)
    except ConnectionResetError:
        print('Client closed a connection')
        
        
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
def check_if_client_on_server(client_socket):
    login = client_socket.recv(1024)
    if find_client_data_by_login(login):
        authorization(client_socket, login)
    else:
        registration(client_socket, login)
    
def authorization(client_socket, login):
    # auth_dict = [{'uuid':"",'login':"", 'password':"", 'history_of_messages':""}, {}] # user_data
    
    if find_client_by_param(value=login, param='login'):
        client_data = find_client_data_by_login(login)
        client_socket.send('You are logged in. Enter your password: '.encode('utf-8'))
        password = client_socket.recv(1024)
        if bcrypt.checkpw(password, client_data.get('password')):
            client_socket.send('Authorization was successful! '.encode('utf-8'))
            print_messages(message_history,client_socket)
    else:
        registration(client_socket, login)
        
    
def registration(client_socket,login):
    client_socket.send('No such user exists. Create a password for registration: '.encode('utf-8'))
    password = client_socket.recv(1024)
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    clients.append(
        {
            'uuid': client_socket,
            'login': login,
            'password': hashed_password,
            #'history_of_messages': []
        })
    client_socket.send('Registration was successful!'.encode('utf-8'))
    
def start_server():
    quit = True
    while quit == True:
        try:
            r, _, _ = select.select((server,), (), (), 1)
            for _ in r:
                client_socket, address = server.accept() #берем клиента из очереди
                client_socket.send('Welcome to pretty server. Enter login '.encode('utf-8'))#оповещаем клиента, что он законектился
                
                check_if_client_on_server(client_socket)
                
                print(f'Client <{address[0]}> connected!') #Выводим информацию на сервере, что подсоединился клиент с [ip]
                
                server_time = time.strftime("%d-%m-%Y / %H:%M:%S", time.localtime())
            
                listener = Thread(target=listen_client, args=(client_socket,server_time,address,client_socket,))
                listener.demon = True
                listener.start()
            
        except KeyboardInterrupt:
            print('\n[Server stopped]')
            server.close()   
            quit = False 
        
          
if __name__ == '__main__':
    start_server()
