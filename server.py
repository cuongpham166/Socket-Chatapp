#verbindungsorientierte Kommunikation, aufsetzend auf TCP = SOCK_STREAM
#Kommunikation zwischen TCP/IP-Netz verteilten Prozessen = AF_INET, Internet IP Protokoll
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread,Semaphore
import sys
from time import sleep

#-------------------------------------------------------
class Server_cl():
#-------------------------------------------------------
    #-------------------------------------------------------
    def __init__(self,host,port):
    #-------------------------------------------------------
        self.addresses = {}
        self.clients = {}
        self.HOST = host
        self.PORT = port

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)           #(localhost: '127.0.0.1', Port:5050 oder 5060)

        self.SERVER = socket(AF_INET, SOCK_STREAM)   #socket
        self.SERVER.bind(self.ADDR)                  #bind
        self.HAUPTSERVER = True                      #läuft über den Server 1
    #-------------------------------------------------------
    def accept_incoming_connections(self):
    #-------------------------------------------------------
        #wartet auf neue Clienten mit Server Accept, auf Clientseite Connect
        while True:

            client, client_address = self.SERVER.accept()       #accept
            print(str(client_address) + " ist verbunden.")
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()   #Thread wird gestartet,multithreading
    #-------------------------------------------------------
    def ping(self,client):
    #-------------------------------------------------------
        #überprüft, ob Clienten verbunden
        while True:
            if self.clients[client] == client:
                sleep(20)
                print("PING")
                client.send(bytes("{PING}", "utf8"))
            else:
                break
    #-------------------------------------------------------
    def handle_client(self,client):  # Client-Socket als Argument
    #-------------------------------------------------------
        # verarbeitet eine Client-Verbindung
        # Fragt nach Namen
        name = client.recv(self.BUFSIZ).decode("utf8")      #recv
        if self.HAUPTSERVER == True:
            welcome = "Hallo " + name                       
            client.send(bytes(welcome, "utf8"))             #send
            msg = name + " ist dem Chat beigetreten!"
            print(msg)
            self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name
        print(str(len(self.clients)) + " Clienten sind verbunden.")
        
        while True:
            msg = client.recv(self.BUFSIZ)
            # Sende Nachricht an alle
            if msg != bytes("{quit}", "utf8"):
                self.broadcast(msg, name + ": ")
                # Falls per Konsole aufgerufen, Nachricht ausgeben
                if self.HAUPTSERVER == False:
                    #print(msg.decode("utf-8"))
                    message = msg.decode("utf-8")
                    print(f"{name}: {message}")

                    mess = f"[Aus 2.Server] {name} : {message}"
                    self.broadcast(bytes(mess,"utf8"))
                    
            # Falls 'Chat verlassen' eingeben wird, wird Verbindung beendet
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del self.clients[client]
                self.broadcast(bytes(name + " hat den Chat verlassen.", "utf8"))
                print(name + " hat den Chat verlassen.")
                print(str(len(self.clients)) + " Clienten sind verbunden.")
                break
    #-------------------------------------------------------
    def broadcast(self,msg, prefix=""):  # prefix ist für name identification.
    #-------------------------------------------------------
        #Broadcasts eine Nachricht an alle Clients.
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)
      
#-------------------------------------------------------
if __name__ == "__main__":
#-------------------------------------------------------
    sev = None
    # Prüft, ob Port angegeben wurde
    if len(sys.argv) == 1:
        sev = Server_cl('127.0.0.1',5050)
        print("Verbinde zu 127.0.0.1:5050")
    elif len(sys.argv) == 2:
        #sev = Server_cl('127.0.0.1', int(sys.argv[1]))
        sev = Server_cl('127.0.0.1', 5060)
        sev.HAUPTSERVER = False
        #print("Verbinde zu " + '127.0.0.1' + ":" + str(sys.argv[1]))
        print("Verbinde zu 127.0.0.1:5060")
    else:
        print("Nur Port oder nichts.")
        exit()

    sev.SERVER.listen(5)                #listen
    print("Warte auf Verbindung...")
    ACCEPT_THREAD = Thread(target=sev.accept_incoming_connections)  # neuer Thread erzeugt
    ACCEPT_THREAD.start()               # starte Thread
    ACCEPT_THREAD.join()                # wartet auf das Ende des anderen Threads
    sev.SERVER.close()                  #close