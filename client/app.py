import tkinter as tk
from tkinter import ttk
from tkinter import font

PORT = 5000
IP = ""

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat system")
        # self.geometry("250x250")
        # self.resizable(width=False, height=False)
        
        def send(event=None):
            message = send_entry.get()
            if message:
                ...
                # send message with socket
                
                
                
                # message_list.insert(tk.END, message + "\n")
                # send_entry.delete(0, tk.END)
                # message_list.see(tk.END)
        
        message_frame = ttk.Frame(self)
        message_frame.pack(expand=True, fill=tk.BOTH)
        
        scrollbar = ttk.Scrollbar(message_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        message_list = tk.Text(message_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
        message_list.pack(expand=True, fill=tk.BOTH)
        
        scrollbar.config(command=message_list.yview)
        
        message_list.see(tk.END)
        
        send_frame:ttk.Frame = ttk.Frame(self)
        send_frame.pack(anchor= tk.S, expand= True, fill= tk.X)
        
        send_frame.columnconfigure(0, weight=1)
        send_frame.columnconfigure(1, weight=0)
        
        send_entry = ttk.Entry(send_frame)
        send_entry.grid(row=0, column=0, sticky="ew", ipady= 1, padx= 1)
        send_entry.bind("<Return>", func= send)
        
        send_button = ttk.Button(send_frame, text= "Send", command= send)
        send_button.grid(row=0, column=1, sticky="w")

if __name__ == "__main__":
    Root = Root()
    Root.mainloop()