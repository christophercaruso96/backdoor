#Per comodità ho aggiunto commenti solo alle parti che differiscono dalla traccia originale
import socket, platform, os

SRV_ADDR = ""
SRV_PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#metodo setsockopt per la modifica del comportamento del socket
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) --> costringe il S.O. a usare l'indirizzo passato a bind()
#anche se già occupato (SO_REUSEADDR)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SRV_ADDR, SRV_PORT))
s.listen(1)
connection, address = s.accept()
#inizializza tosend come stringa vuota fuori dal while
tosend = ""
print ("Connesso con: ", address)
#introduzione variabile boolean running per controllo iterazione
running = True
while running:
	try:
		data = connection.recv(1024)
	except: continue
    #strip per rimuovere spazi iniziali e finali nella stringa
	c = data.decode('utf-8').strip()
	if(c == '1'):
		#aggiunto \n per leggibilità e migliore formattazione
		tosend = platform.platform() + " " + platform.machine() + "\n"
		connection.sendall(tosend.encode())
	elif(c == '2'):
		#invia a tutti i partecipanti il messaggio con "Path:" per suggerire l'inserimento di un path
		connection.sendall(b'Path: ')
		data = connection.recv(1024)
		try:
			#strip per rimuovere spazi iniziali e finali nella stringa
			filelist =  os.listdir(data.decode('utf-8').strip())
			#aggiunto \n per leggibilità e migliore formattazione
			#usato metodo join per l'unione con chiamata composta
			#sorted per ordinare file list
			tosend = "\n".join(sorted(filelist)) + '\n'
		except:
			tosend = "Wrong path"
		connection.sendall(tosend.encode())
	elif(c == '0'):
		connection.close()
		#qui è rimasto il codice che permette la riapertura della connessione
		connection, address = s.accept()
	#introdotto controllo input utente per uscire dal ciclo 
	#(se utente inserisce '9', running va a False e l'esecuzione passa alla prima istruzione che segue il costrutto while)
	elif(c == '9'): running = False #delete after debug
#qui viene introdotto un controllo
#Se l'identificativo della connessione è valorizzato
#Chiusura connessione connection.close()
#Deallocazione del socket con socket.close (possibile solo se c'è solo un thread sul socket altrimenti antrebbe messo a monte socket.shutdown())
if connection: connection.close()
s.close()