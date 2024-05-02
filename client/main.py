# That is a chat app
import os
import re
import socket
from threading import *
from  socket import AF_INET, SOCK_STREAM
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

def get_caches(cache_:str):
    if f"{cache_}.txt" not in os.listdir(".\\cache"):
        with open(f".\\cache\\{cache_}.txt", "a"): pass
    with open(f".\\cache\\{cache_}.txt", "r") as f:
        return f.read().split("\n")

def add_cache(cache_:str, value:str):
    if f"{cache_}.txt" not in os.listdir(".\\cache"):
        with open(f".\\cache\\{cache_}.txt", "a"): pass
    with open(f".\\cache\\{cache_}.txt", "a+") as f:
        f.seek(0)
        if len(f.read()) > 0:
            f.write("\n")
        f.write(value)
print(get_caches("address"))

def isAddress(address:str):
    return re.match(r"^(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}$",address)

class Client(socket.socket):
    def __init__(self):
        super().__init__(AF_INET, SOCK_STREAM)

class ChatApp(tk.Tk):
    font:tuple = ("Cascadia Code", 12)
    client = Client()
    def __init__(self):
        super().__init__()
        self.title("ChatApp | Join")
        self.resizable(width= False, height= False)

        self.join_frame:tk.Frame = tk.Frame(self)
        self.join_frame.pack()
        
        self.label_address = ttk.Label(self.join_frame, text= "Address:", font= self.font,)
        self.label_address.grid(row= 0, column= 0, padx= 5, pady= 5, sticky= tk.SW)
        
        self.entry_address = ttk.Combobox(self.join_frame, width= 28, font= self.font, 
                                          values= get_caches("address"))
        self.entry_address.grid(row= 0, column= 1, padx= 5, pady= 5)
        self.entry_address.focus()
        
        self.warning_label = tk.Label(self.join_frame,text= "🛈Invalid Address",fg= "#ff4d4d", font= self.font)
        self.warning_label.grid_forget()

        self.label_username = ttk.Label(self.join_frame, text= "Username:", font= self.font)
        self.label_username.grid(row= 1, column= 0, padx= 5, pady= 5, sticky= tk.SW)
        self.entry_username = ttk.Entry(self.join_frame, width= 30, font= self.font)
        self.entry_username.grid(row= 1, column= 1, padx= 5, pady= 5)
        
        self.entry_address.bind("<Return>", func= self.on_address_return)
        self.entry_address.bind("<<ComboboxSelected>>", self.on_address_return)
        self.entry_username.bind("<Return>", func= self.on_username_return)
        self.entry_username.bind("<FocusIn>", func= self.on_username_focus)
        
    
    def on_username_return(self, e):
        username, address= self.entry_username.get(), self.entry_address.get()
        if address not in get_caches("address"):
            add_cache("address", address)
        # a.b.c.d:pppp
        address:tuple = (lambda address: (address[0], int(address[1])))(address.split(":"))
        if not username:
            return
        Thread(target= self.connect, args= (address, username), daemon= True).start()
    
    def on_username_focus(self, e):
        address = self.entry_address.get()
        if not isAddress(address):
            self.warning_label.grid(row= 2, column= 0, columnspan= 2, padx= 5, pady= 5, sticky= tk.SW)
            self.entry_address.focus()
            return
        self.warning_label.grid_forget()

    def on_address_return(self, e):
        address = self.entry_address.get()
        if not isAddress(address):
            self.warning_label.grid( row= 2, column= 0, columnspan= 2, padx= 5, pady= 5, sticky= tk.SW)
            return
        self.warning_label.grid_forget()
        self.entry_username.focus()
    
    def connect(self, address:tuple, username:str):
        self.join_frame.pack_forget()
        pb = ttk.Progressbar(
                self,
                orient='horizontal',
                mode='indeterminate',
                length=280,maximum= 50,
            )
        pb.start()
        pb.pack(padx= 5, pady= 5)
        self.title("ChatApp | Connecting")
        # try:
        print(username)
        print(f"\033[92m connecting {address[0]}:{address[1]}", end= "\033[0m\n")
        try:
            self.client.connect(address)
        except IOError as e:
            print(e)
            print(f"\033[1m {address[0]}:{address[1]} Time out.", end= "\033[0m\n")
            pb.pack_forget()
            self.title("ChatApp | Join")
            self.join_frame.pack()
            showerror(title= "Time out connecting", message= "Please check your internet and try again,\nhave sure your address is correct.")
            return
        pb.pack_forget()
        print(f"\033[1m connected {address[0]}:{address[1]}", end= "\033[0m\n")
        self.client.sendall(f"username:{username}".encode("utf8"))
        self.create_chatGui()
        

    def listener(self):
        while True:
            data = self.client.recv(1024).decode("utf8")
            if not data:
                break
            print(data)
            prefix = data[:data.index(":")]
            content = data[data.index(":")+1:]
            print(content)
            match prefix:
                case "message":
                    self.message_list.insert(tk.END, content + "\n")
                    self.message_list.see(tk.END)
        print(f"\033[91m disconnected", end= "\033[0m\n")
    
    def create_chatGui(self):
        self.message_frame = ttk.Frame(self)
        self.message_frame.pack(expand=True, fill=tk.BOTH)
        
        self.scrollbar = ttk.Scrollbar(self.message_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.message_list = tk.Text(self.message_frame, yscrollcommand=self.scrollbar.set, wrap=tk.WORD, font= self.font)
        self.message_list.pack(expand=True, fill=tk.BOTH)
        
        self.scrollbar.config(command=self.message_list.yview)
        
        self.message_list.see(tk.END)
        
        self.send_frame:ttk.Frame = ttk.Frame(self)
        self.send_frame.pack(anchor= tk.S, expand= True, fill= tk.X)
        
        self.send_frame.columnconfigure(0, weight=1)
        self.send_frame.columnconfigure(1, weight=0)
        
        self.send_entry = ttk.Entry(self.send_frame, font= self.font)
        self.send_entry.grid(row=0, column=0, sticky="ew", ipady= 1, padx= 1)
        self.send_entry.bind("<Return>", func= self.send)
        
        self.send_button = ttk.Button(self.send_frame, text= "Send", command= self.send)
        self.send_button.grid(row=0, column=1, sticky="w")
        
        Thread(target= self.listener, daemon= True).start()
    
    def send(self, e = None):
        content:str = self.send_entry.get()
        if content:
            self.client.sendall(f"message:{content}".encode("utf8"))
            self.send_entry.delete(0, tk.END)

if __name__ == "__main__":
    ChatApp = ChatApp()
    ChatApp.mainloop()