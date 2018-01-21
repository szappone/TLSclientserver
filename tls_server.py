#import socket module
from socket import *
import ssl

context = ssl.create_default_context()
context.check_hostname = False
#context.load_cert_chain(certfile='server.crt', keyfile="server.key")
serverSocket = socket(AF_INET, SOCK_STREAM)
certval = ssl.CERT_NONE

#Prepare a sever socket

sslsock = ssl.wrap_socket(serverSocket, server_side=True, cert_reqs=ssl.CERT_NONE, certfile='server.crt', keyfile="server.key")
sslsock.bind(('127.0.0.1', 12345))
sslsock.listen(5)
while True: 
	#Establish the connection
	print 'Ready to serve...'
	connectionSock, address = sslsock.accept()
	try:
		message = connectionSock.recv(1024)
		filename = message.split()[1]
		file = open(filename[1:])
		outputdata = file.read()
		file.close()
		#Send one HTTP header line into socket 
		connectionSock.send('HTTP/1.1 200 OK')
		#Send the content of the requested file to the client 
		print 'sending what you requested'
		for i in range(0, len(outputdata)):
			connectionSock.send(outputdata[i])
		connectionSock.close()
	except IOError:
		print 'cannot find'
		#Send response message for file not found
		connectionSock.send('404 File Not Found')
		#Close client socket 
		connectionSock.close()
sslsock.close()
serverSocket.close()