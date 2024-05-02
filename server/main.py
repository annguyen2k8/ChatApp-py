import sys
import socket
from threading import *
from  socket import AF_INET, SOCK_STREAM
from config import *

class ClientThreat():
    def __init__(self,clients:dict , conn:socket.socket, addr:tuple):
        self.clients = clients
        self.conn = conn
        self.addr = addr
    
    def listener(self):
        while True:
            try:
                data = self.conn.recv(1024).decode("utf8")
                print(data)
            except:
                break
            if not data:
                break
            prefix:str = data[:data.index(":")]
            match prefix:
                case "username":
                    username:str = data[data.index(":")+1:]
                    self.clients[self.conn] = username
                    self.send_message(f"{username} is joining.")
                case "message":
                    content:str = data[data.index(":")+1:]
                    username:str = self.clients[self.conn]
                    self.send_message(f"<{username}> {content}")    
        self.on_disconnect()
    
    def on_disconnect(self):
        self.conn.close()
        username = self.clients.pop(self.conn)
        print(f"\033[91m  {self.addr[0]}:{self.addr[1]} disconnect", end= "\033[0m\n")
        self.send_message(f"{username} is left.")
    
    def send_message(self, content:str):
        Thread(target= lambda content: [conn_.send((f"message:{content}").encode("utf8")) for conn_ in self.clients], args= (content,), daemon= True).start()

class Server(socket.socket):
    clients:dict = {}
    def __init__(self, host:str, port:int=5050, limit_connect:int=0)->None:
        super().__init__(AF_INET, SOCK_STREAM)
        self.limit_connect:int = limit_connect
        self.address:tuple = (host, port)

    def run(self):
        self.bind(self.address)
        self.listen(self.limit_connect)
        print(f"\033[1m Server listening on address {':'.join(map(str,self.address))}", end= "\033[0m\n")
        while True:
            type client = socket.socket
            type addr = tuple
            conn, addr = self.accept()
            Thread(target= self.on_client, args= (conn, addr)).start()
    
    def on_client(self, conn:socket.socket, addr:tuple):
        print(f"\033[92m  {addr[0]}:{addr[1]} connecting", end= "\033[0m\n")
        self.clients[conn] = None
        client = ClientThreat(self.clients, conn, addr)
        Thread(target= client.listener, daemon= True).start()

if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.run()