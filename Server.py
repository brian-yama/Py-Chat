import os,socket,select,sys,string
from thread import *

def socket_closed(clntSock):
	print('Socket closed')
	clntSock.close()

def serv_send(clntSock,message):
	try:
		clntSock.send(message)
	except IOError:
		socket_closed(clntSock)

def serv_recv(clntSock):
	try:
		print clntSock.recv(1024)
	except IOError:
		socket_closed(clntSock)

def make_account(filename):
	account = {}
	with open("user_pass.txt") as f:
		for line in f:
			(name, pwd) = line.split()
			account[name] = pwd
	return account

def client_thread(clientSocket, address, username):
	clientSocket.send('You have signed in!')
	command = ""
	while True:
		#TODO- clientSocket.recv(stuff)
		serv_send(clientSocket, "COMMAND: ")
		command = clientSocket.recv(1024)
		command = command.rstrip()
		commandKey = command.split(' ', 1)[0]
		if any(commandKey in s for s in COMMANDS):
			run_command(commandKey, command, clientSocket)

	clientSocket.close()

def run_command(commandKey, command, clientSocket):
	print commandKey

def broadcast(socket, message):
	for s in CONNCTIONS:
		if s != servSock and s != socket:
			try:
				s.send(message)
			except:
				s.close()
				CONNECTIONS.remove(s)

if __name__ == "__main__":
	# check validity of arguments
	if len(sys.argv) != 2 or not sys.argv[1].isdigit():
		print("YOU NEED JUST THE PORT")

	PORT 		= int(sys.argv[1])
	CONNECTIONS	= []
	COMMANDS	= {"whoelse", "wholasthr", "broadcast", "message", "block", "unblock", "logout"}

	# Set up the initial socket object
	servSock 	= socket.socket() #Create the socket object
	print 'Socket create success.'
	host		= socket.gethostname()		#Get local machine name
	servSock.bind((host, PORT)) 			#Bind to the port
	print 'Socket bind success.'
	servSock.listen(10)							#Listen for a client
	print 'Socket is listening ...'

	#Append the server socket as a readable connection
	CONNECTIONS.append(servSock)

	account = make_account("user_pass.txt")

	while True:
		readSock, writeSock, errSock = select.select(CONNECTIONS, [], [])

		for s in readSock:
			if s == servSock:
				#Accept a connection from a client
				clntSock, addr = servSock.accept()	#
				print 'Got connection from', addr
				serv_send(clntSock, '\nYou have successfully connected!')

				#Username authentication
				serv_send(clntSock, '\nUsername?')
				nameKey = ""
				nameKey = clntSock.recv(1024) 
				nameKey = nameKey.rstrip()
				while nameKey not in account.keys(): 
					serv_send(clntSock, '\nIncorrect username.')
					serv_send(clntSock, '\nUsername?')
					nameKey = clntSock.recv(1024)
					nameKey = nameKey.rstrip()

				#Password authentication
				pwdKey = ""
				serv_send(clntSock, '\nPassword?')
				pwdKey = clntSock.recv(1024)
				pwdKey = pwdKey.rstrip()
				while account[nameKey] != pwdKey: 
					serv_send(clntSock, '\nIncorrect password.')
					serv_send(clntSock, '\nPassword?')
					pwdKey = clntSock.recv(1024) 
					pwdKey = pwdKey.rstrip()

				CONNECTIONS.append(clntSock)
				client_thread(clntSock, addr, nameKey)

			# handles messages sent by a client
			# else:
			# 	try:
			# 		message = s.recv(1024)
			# 		if message:
			# 			broadcast(s, "\r" + '"' + str(s.getpeername()) + '": ' + message)
			# 	except:
			# 		broadcast(s, "")
						
	servSock.close()

