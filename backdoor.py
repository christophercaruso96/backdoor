#IL CODICE NON FUNZIONEREBBE CORRETTAMENTE, MANCANO ALCUNI MESSAGGI E VERIFICHE
#GESTIONE DEL SOCKET INCOMPLETA
#GESTIONE ITERAZIONE INCOMPLETA

#import dei seguenti moduli
#socket --> modulo per accesso/gestione interfaccia socket
#platform --> modulo per l'identificazione della piattaforma sottostante
#os --> modulo che mette a disposizione le funzionalità del sistema operativo
import socket, platform, os

#inizializzazione variabili per IP e PORTA
SRV_ADDR = ""
SRV_PORT = 1234

#creazione nuovo socket, AF_INET = IPV4, SOCK_STREAM = connessione TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#biding (collegamento socket all'indirizzo e alla porta), accetta come parametro una tupla () non modificabile
s.bind((SRV_ADDR, SRV_PORT))

#configura il socket per ascoltare sulla coppia IP:PORTA indicata (tra parentesi il num. max di connessioni in coda)
#s.listen(backlog)
s.listen(1)

#metodo accept() per accettare e stabilire la connessione con il client che tenterà di connettersi al servizio
#restituisce due argomenti
# - connection: socket verrà usato per scambio dati (identificativo della connessione che verrà usata per lo scambio dati)
# - address: IPV4 del client che si collegherà
connection, address = s.accept()

#stampo la connessione avvenuta stampando l'indirizzo del client collegato
print("client connected: ", address)

#ciclo while sempre vero per lo scambio dati
while 1:
    #try-catch, se si verifica l'eccezione continuo nel ciclo con l'iterazione successiva
    try:
        #connection.recv(1024) per riceve i dati dal client, 1024 grandezza del buffer in byte
        #data: contiene i dati ricevuti dal client
        #recv restituisce un byte object
        data = connection.recv(1024)
    except:continue
    #metodo decode per la decodifica in utf-8, il client invia dati in utf-8
    #verifico se il dato inserito dal client è 1
    if(data.decode('utf-8') == '1'):
        #platform.platform restituisce una stringa che identifica la piattaforma sottostante
        #platform.machine restituisce una stringa con il tipo di macchina e.g. 'AMD64' o stringa vuota se non è determinabile
        #le due stringhe vengono concatenate e assegnate alla variabile tosend
        tosend = platform.platform() + " " + platform.machine()
        #invia a tutti i partecipanti un messaggio contenente le informazioni sulla piattaforma
        #il metodo encode è di default settato con utf-8
        connection.sendall(tosend.encode())
    #metodo decode per la decodifica in utf-8, il client invia dati in utf-8
    #verifico se il dato inserito dal client è 2
    elif(data.decode('utf-8') == '2'):
        #connection.recv(1024) per ricevere i dati dal client, 1024 grandezza del buffer in byte
        #data: contiene i dati ricevuti dal client
        #recv restituisce un byte object
        #qui sto richiedendo perchè dovrà essere inserito un path
        data = connection.recv(1024)
        #try-catch, se si verifica l'eccezione esegue un blocco istruzioni diverso
        try:
            #os.listdir restituisce un elenco del contenuto della directory specificata come parametro
            #data.decode('utf-8') per decodificare il messaggio ricevuto dal client come path
            filelist = os.listdir(data.decode('utf-8'))
            tosend = ""
            #itero per tutti i file contenuti nella directory indicata e costruisco la stringa da inviare
            for x in filelist:
                tosend += "," + x
        except:
            #in caso di eccezione la stringa da inviare contiene il messaggio "path errato"
            tosend = "Wrong path"
        #viene inviato a tutti i partecipanti il messaggio costruito in base al costrutto try-catch
        connection.sendall(tosend.encode())
    #metodo decode per la decodifica in utf-8, il client invia dati in utf-8
    #verifico se il dato inserito dal client è 0
    elif(data.decode('utf-8') == '0'):
        #se il dato inserito è 0 chiudo la connessione
        connection.close()
        #questo pezzo non andrebbe messo perchè permette di accettare una nuova connessione
        #andrebbe inserito s.close() 
        connection, address = s.accept()
