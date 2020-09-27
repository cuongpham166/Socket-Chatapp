#!/usr/bin/env python3
#verbindungsorientierte Kommunikation, aufsetzend auf TCP = SOCK_STREAM
#Kommunikation zwischen TCP/IP-Netz verteilten Prozessen = AF_INET
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter          # für die GUI
import os
from time import sleep

#-------------------------------------------------------
class Chatter_cl():
#-------------------------------------------------------
    #-------------------------------------------------------
    def __init__(self):
    #-------------------------------------------------------
        self.name = input('Name: ')
        ZIEL = input("Default Server? y or n: ")
        if ZIEL == "n":                 # möchte der Client keinen Default nutzen, 
            HOST = input('Host: ')      # dann muss er separat Host und Port eingeben
            PORT = input('Port(1): ')
            PORT2 = input('Port(2): ')
            self.PORT = int(PORT)
            self.HOST = HOST
            self.PORT2 = PORT2  
        else:                           
            self.PORT = 5050
            self.HOST = "127.0.0.1"
            self.PORT2 = 5060

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)
        self.ADDR2 = (self.HOST, self.PORT2)
        self.VER = True

    #-------------------------------------------------------
    """
    def receive(self):
    #-------------------------------------------------------
        # verarbeitet das Erhalten der Nachrichten
        while True:
            try:
                if self.VER == True:        # besteht eine Verbindung?
                    msg = client_socket.recv(self.BUFSIZ).decode("utf8")    #recv
                    
                    # Prüft ob msg keinen Wert hat
                    if msg == "":
                        print("1")
                        self.VER = False
                        client_socket.close()
                    elif msg != "{PING}":
                        print("2")
                        msg_list.insert(tkinter.END, msg)
                else:
                    msg = client_socket2.recv(self.BUFSIZ).decode("utf8")
                    print(f"2.Server {msg}") 
                    print("3")  
                    if msg != "{PING}":
                        print("4")
                        msg_list.insert(tkinter.END, msg)
            except OSError:     # Client hat den Chat verlassen
                break
    """
    def receive(self):
        while True:
            try:
                if self.VER == True:
                    while True:
                        try:
                            msg = client_socket.recv(self.BUFSIZ).decode("utf8")
                            if msg == "":
                                self.VER = False
                                client_socket.close()
                            elif msg != "{PING}":
                                #print("1")
                                msg_list.insert(tkinter.END,msg)
                        except OSError:
                            msg = client_socket2.recv(self.BUFSIZ).decode("utf8")
                            if msg != "{PING}":
                                #print("2")
                                if "[Aus 2.Server]" in msg:
                                    msg_list.insert(tkinter.END,msg)                                
                else:
                    msg = client_socket2.recv(self.BUFSIZ).decode("utf8")
                    if msg != "{PING}":
                        #print("3")
                        msg_list.insert(tkinter.END,msg)
            except OSError:
                break
                    

    #-------------------------------------------------------
    def send(self,event=None):  # event is passed by binders.
    #-------------------------------------------------------
        # verarbeitet das Senden der Nachrichten
        msg = my_msg.get()
        my_msg.set("")      # nachdem die Nachricht gesendet wurde, wird das Einagbefeld geleert
        if self.VER == True:
            #client_socket.send(bytes(msg, "utf8"))  
            try:
                client_socket.send(bytes(msg,"utf8"))
            except OSError:
                client_socket2.send(bytes(msg, "utf8"))
        else:
            client_socket2.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            sleep(1)
            client_socket2.close()                    #close
            top.quit()
    #-------------------------------------------------------
    def on_closing(self,event=None):
    #-------------------------------------------------------
        # schließt das Fenster
        my_msg.set("{quit}")
        self.send()
        top.destroy()

    #-------------------------------------------------------
    def sendName(self):
    # -------------------------------------------------------
        if self.VER == True:
            client_socket.send(bytes(self.name, "utf8"))
        client_socket2.send(bytes(self.name, "utf8"))
        
    #-------------------------------------------------------
    #def close():
    #-------------------------------------------------------
        # schließt das Fenster
     #   window.destroy()  

# hier die Erstellung der GUI: 
chat = Chatter_cl()
top = tkinter.Tk()      # Grafische Oberfläche erstellen

top.title("Chatter von " + chat.name)

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()        # die Nachrichten, die gesendet werden sollen
scrollbar = tkinter.Scrollbar(messages_frame)  # zum Navigieren, zum Lesen der zuvorigen Nachrichten

# Nachrichten
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

# erstellt Eingabefeld
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", chat.send)
entry_field.pack()

# erstellt Send Button
send_button = tkinter.Button(top, text="Senden", command=chat.send)
send_button.pack()

# Erstellt Quit Button
quit_button = tkinter.Button(top, text="Chat verlassen", command=chat.on_closing)
quit_button.pack(side="right")


top.protocol("WM_DELETE_WINDOW", chat.on_closing)

# Socket-Port
try:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(chat.ADDR)
    client_socket.settimeout(30)
except:
    print("Server 1 nicht erreichbar")
    chat.VER = False
client_socket2 = socket(AF_INET, SOCK_STREAM)   #socket
client_socket2.connect(chat.ADDR2)              #connect
client_socket2.settimeout(30)


chat.sendName()
receive_thread = Thread(target=chat.receive)
receive_thread.start()
tkinter.mainloop()  # startet die GUI-Ausführung
