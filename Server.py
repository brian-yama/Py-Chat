import os,socket,select,sys

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
		
if __name__ == "__main__":
	# check validity of arguments
	if len(sys.argv) != 2 or not sys.argv[1].isdigit():
		print("YOU NEED JUST THE PORT")

	PORT 		= int(sys.argv[1])

	servSock 	= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create the socket object

	host		= socket.gethostname()		#Get local machine name
	servSock.bind((host, PORT)) 			#Bind to the port

	servSock.listen(10)							#Listen for a client

	#Create a hash table consisting of valid usernames and passwords
	account = {}
	with open("user_pass.txt") as f:
		for line in f:
			(name, pwd) = line.split()
			account[name] = pwd

	print account

	nameKey = ""

	while True:
		clntSock, addr = servSock.accept()	#
		print 'Got connection from', addr
		serv_send(clntSock, 'You have successfully connected!')
		serv_send(clntSock, 'Username:')
		nameKey = clntSock.recv(1024) 
		
		print nameKey

		while nameKey not in account.keys(): 
			print nameKey
			serv_send(clntSock, 'Incorrect username.')
			serv_send(clntSock, 'Username:')
			nameKey = clntSock.recv(1024)



		pwdKey = ""
		serv_send(clntSock, 'Password:')
		pwdKey = clntSock.recv(1024)
		while account[nameKey] != pwdKey: 
			serv_send(clntSock, 'Incorrect password.')
			serv_send(clntSock, 'Password:')
			pwdKey = clntSock.recv(1024) 

		serv_send(clntSock, 'You have successfully signed in!')

	clntSock.close()						#Close connection.