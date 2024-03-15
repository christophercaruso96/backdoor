#Per comodità ho aggiunto commenti solo alle parti che differiscono dalla traccia originale
import socket, platform, os

SRV_ADDR = "172.19.87.138"
SRV_PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#metodo setsockopt per la modifica del comportamento del socket
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) --> costringe il S.O. a usare l'indirizzo passato a bind()
#anche se già occupato (SO_REUSEADDR)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SRV_ADDR, SRV_PORT))
s.listen(1)
print("Server avviato! In attesa di connessione ...")
connection, address = s.accept()
#inizializza tosend come stringa vuota fuori dal while
tosend = ""
print ("Connesso con: ", address)

while True:
	try:
		#introdotto messaggio di stato
		print ("In attesa di una nuova scelta operativa del client!\n")
		#Aggiunto messaggio a tutti i partecipanti per indicare la scelta da effettuare
		connection.sendall(b'Inserire\n 0 - chiudere la connessione e uscire dal programma\n 1 - per dettagli architettura\n 2 - per vedere il contenuto di un path\n\n')
		data = connection.recv(1024)
	except: continue
    #strip per rimuovere spazi iniziali e finali nella stringa
	c = data.decode('utf-8').strip()
	if(c == '1'):
		#introdotto messaggio di stato
		print ("Il client ha chiesto dettagli sull' architettura!\n")
		#aggiunto \n per leggibilità e migliore formattazione
		tosend = platform.platform() + " " + platform.machine() + "\n\n"
		connection.sendall(tosend.encode())
	elif(c == '2'):
		#invia a tutti i partecipanti il messaggio con "Path:" per suggerire l'inserimento di un path
		connection.sendall(b'Path: \n')
		data = connection.recv(1024)
		print ("Il client ha chiesto dettagli sul contenuto del path: \n", data.decode('utf-8').strip(), "\n")
		try:
			#strip per rimuovere spazi iniziali e finali nella stringa
			filelist =  os.listdir(data.decode('utf-8').strip())
			#aggiunto \n per leggibilità e migliore formattazione
			#usato metodo join per l'unione con chiamata composta
			#sorted per ordinare file list
			tosend = "\n".join(sorted(filelist)) + '\n\n'
		except:
			tosend = "Wrong path"
		connection.sendall(tosend.encode())
	elif(c == '0'):
		#introdotti messaggi di stato
		print ("Il client ha chiesto la chiusura! Bye bye!\n")
		connection.sendall(b'Bye bye!\n\n')
		connection.close()
		#introdotto nel caso di più thread attivi sul socket
		#deallocazione del socket con solo l'uso di socket.close
		#possibile solo se c'è solo un thread sul socket altrimenti antrebbe va messo a monte socket.shutdown()
		#socket.SHUT_RDWR - sia invio e ricezione disallowed
		s.shutdown(socket.SHUT_RDWR)
		s.close()
		#rimosso il codice che permette la riapertura della connessione: connection, address = s.accept()
		#introdotta uscita dal ciclo
		break