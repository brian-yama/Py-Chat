import os,socket,select,sys,string,time,datetime
from thread import *
from threading import Timer

# Closes a socket
def socket_closed(clntSock):
	print('Socket closed')
	clntSock.close()

# Sends a message to a given socket.
def serv_send(clntSock,message):
	try:
		clntSock.send(message)
	except IOError:
		socket_closed(clntSock)

# Receives a message from a given socket.
def serv_recv(clntSock):
	try:
		print clntSock.recv(1024)
	except IOError:
		socket_closed(clntSock)

# Receives a filename and creates a dictionary with
# associated usernames and passwords in the file.
def make_account(filename):
	account = {}
	with open("user_pass.txt") as f:
		for line in f:
			(name, pwd) = line.split()
			account[name] = pwd
	return account

# The client thread that runs upon connection.
def client_thread(clntSock, addr):
	#Username authentication
	serv_send(clntSock, '\nUsername: ')
	nameKey = ""
	nameKey = clntSock.recv(1024) 
	nameKey = nameKey.rstrip()
	while nameKey not in account.keys() or nameKey in usernames: 
		serv_send(clntSock, 'Invalid username.')
		serv_send(clntSock, '\nUsername: ')
		nameKey = clntSock.recv(1024)
		nameKey = nameKey.rstrip()

	# Appends the username to the active users directory.
	usernames.append(nameKey)

	# Client hashtable
	# Key = username
	# {<Number of successive log-in attempts>,
	# <socket>, <addr>, <IP address>, <block status> }
	clients[nameKey] = [0, clntSock, addr[1], addr[0], 0] 

	# Checks if the user and IP address combination is locked out.
	if nameKey in lockedAcc.keys():
		if addr[0] == lockedAcc[nameKey][1]:
			elapsed_time = (datetime.datetime.now() - lockedAcc[nameKey][0]).total_seconds()
			if elapsed_time > BLOCK_TIME:
				pass
			else:
				serv_send(clntSock, 'You are still locked out for ' + str(60 - elapsed_time) + ' seconds.\n')
				logout(clntSock, nameKey)

	try:			
		#Password authentication
		pwdKey = ""
		serv_send(clntSock, 'Password: ')
		pwdKey = clntSock.recv(1024)
		pwdKey = pwdKey.rstrip()
		while account[nameKey] != pwdKey and clients[nameKey][0] < 2:
			serv_send(clntSock, 'Incorrect password. Attempts left: ' + str(2 - clients[nameKey][0]))
			serv_send(clntSock, '\nPassword: ')
			pwdKey = clntSock.recv(1024) 
			pwdKey = pwdKey.rstrip()
			clients[nameKey][0] += 1

		# Locking out protocol
		if account[nameKey] != pwdKey:
			lockedAcc[nameKey] = [datetime.datetime.now(), addr[0]] #Log the time and ip address of user
			serv_send(clntSock, 'Incorrect password. You are locked out for ' + str(BLOCK_TIME) + ' seconds.\n')
			logout(clntSock, nameKey)

		serv_send(clntSock, 'You have signed in!\n')

		# Passes any messages sent while user was offline.
		if nameKey in offlineMsg.keys():
			serv_send(clntSock, 'Messages sent while you were offline:')
			for i in offlineMsg[nameKey]:
				serv_send(clntSock, i)
			del offlineMsg[nameKey]
			serv_send(clntSock, '\n')

		command = ""
		while True:
			# Timer to check if user times out before giving a command.
			t = Timer(TIME_OUT, time_kick, (clntSock,nameKey,))
			t.start()
			serv_send(clntSock, "Command: ")
			command = clntSock.recv(1024)
			t.cancel() # If received something, cancel timer
			command = command.rstrip()
			commandKey = command.split(' ', 1)[0]
			commandKey = commandKey.strip()
			if any(commandKey in s for s in COMMANDS):
				run_command(commandKey, command, clntSock, nameKey)
			else:
				serv_send(clientSocket, 'Invalid command!')
	except:
		#client socket already closed
		clntSock.close()
		print "A client " + str(addr) + " has logged off."

# Function that runs in time-out event.
def time_kick(clientSocket, nameKey):
	serv_send(clientSocket, '\nUser timed out. Type anything to disconnect.\n')
	logout(clientSocket, nameKey)

# Logout function - removes user from any active directory,
# logs the logout time, and closes the socket.
def logout(clientSocket, nameKey):
	serv_send(clientSocket, "Logging off.")
	logoutRec[nameKey] = datetime.datetime.now()
	connections.remove(clientSocket)
	usernames.remove(nameKey)
	clients.pop(nameKey, 0)
	clientSocket.close()

# If command is given to server, runs the command.
def run_command(commandKey, command, clientSocket, nameKey):
	# Adds a favorite to the user's favorites list.
	if commandKey == 'addfavorite':
		mail = []
		mail = command.split(' ')
		if nameKey in group.keys():
			group[nameKey].append(str(mail[1]))
		else:
			group[nameKey] = [mail[1]]
		serv_send(clientSocket, 'You have added ' + str(mail[1]) + ' to your list of favorites.\n')

	# Sends a message to all favorites on the list.
	if commandKey == 'tofavorite':
		mail = []
		mail = command.split(' ')
		if nameKey in group:
			for i in group[nameKey]:
				if i in usernames:
					(clients[i][1]).send('\n"' + nameKey + '" said to favorites: ')
					for i in range(2, len(mail)):
						(clients[i][1]).send(str(mail[i]) + ' ')
					(clients[i][1]).send('\nCommand: ')
				else:
					if i in offlineMsg:
						offlineMsg[i][1].append('\n"' + nameKey + '" said to favorites: ')
					else:
						offlineMsg[i] = ['\n"' + nameKey + '" said to favorites: ']
					for i in range(2, len(mail)):
						offlineMsg[i].append(str(mail[i]) + ' ')
		else:
			serv_send(clientSocket, 'You do not have anyone in your favorites!\n')

	# Removes a favorite from the list.
	if commandKey == 'removefavorite':
		mail = []
		mail = command.split(' ')
		if nameKey in group:
			try:
				group[nameKey].remove(mail[1])
				serv_send(clientSocket, 'You have removed ' + str(mail[1]) + ' from your list of favorites.\n')
			except ValueError:
				serv_send(clientSocket, 'That user is not one of your favorites.\n')
				pass

	# Lists all favorites.
	if commandKey == 'listfavorite':
		if nameKey in group:
			for favorites in group[nameKey]:
				serv_send(clientSocket, str(favorites))
				serv_send(clientSocket, '\n')
		else:
			serv_send(clientSocket, 'You do not have any favorites!\n')

	# Lists any other active user.
	if commandKey == 'whoelse':
		for i in range (0, len(usernames)):
			serv_send(clientSocket, str(usernames[i]))
			if i < len(usernames):
				serv_send(clientSocket, '\n')

	# Lists any users that was active in the last specified timeframe (LAST_HOUR)
	elif commandKey == 'wholasthr':
		for i in range (0, len(usernames)):
			serv_send(clientSocket, str(usernames[i]))
			if i < len(usernames):
				serv_send(clientSocket, '\n')
		for key in logoutRec:
			if ((datetime.datetime.now() - logoutRec[key]).total_seconds()) < LAST_HOUR:
				if key not in usernames: #Prevent double entries
					serv_send(clientSocket, str(key) + '\n')

	# Blocks specified user from invoking the 'message' command.
	elif commandKey == 'block':
		mail = []
		mail = command.split(' ')
		if mail[1] == nameKey:
			serv_send(clientSocket, 'You cannot block yourself!\n')
		elif mail[1] not in account.keys(): 
			serv_send(clientSocket, 'That user does not exist!\n')
		elif mail[1] not in clients:
			serv_send(clientSocket, 'That user is offline!\n')
		elif clients[mail[1]][4] == 1:
			serv_send(clientSocket, 'You have already blocked that user.\n')
		else:
			clients[mail[1]][4] = 1
			serv_send(clientSocket, 'You have blocked ' + mail[1] + '.\n')

	# Unblocks the user from invoking the 'message' command.
	elif commandKey == 'unblock':
		mail = []
		mail = command.split(' ')
		if mail[1] == nameKey:
			serv_send(clientSocket, 'You cannot unblock yourself!\n')
		elif mail[1] not in account.keys(): 
			serv_send(clientSocket, 'That user does not exist!\n')
		elif mail[1] not in clients:
			serv_send(clientSocket, 'That user is offline!\n')
		elif clients[mail[1]][4] == 0:
			serv_send(clientSocket, 'That user is already unblocked.\n')
		else:
			clients[mail[1]][4] = 0	
			serv_send(clientSocket, 'You have unblocked ' + mail[1] + '.\n')

	# Sends a message to another specified user.
	elif commandKey == 'message':
		if clients[nameKey][4] == 0:
			mail = []
			mail = command.split(' ')
			if mail[1] in usernames:
				(clients[mail[1]][1]).send('\n"' + nameKey + '": ')
				for i in range(2, len(mail)):
					(clients[mail[1]][1]).send(str(mail[i]) + ' ')
				(clients[mail[1]][1]).send('\nCommand: ')
			else:
				if mail[1] in offlineMsg:
					offlineMsg[mail[1]].append('\n"' + nameKey + '": ')
				else:
					offlineMsg[mail[1]] = ['\n"' + nameKey + '": ']
				for i in range(2, len(mail)):
					offlineMsg[mail[1]].append(str(mail[i]) + ' ')

		else:
			serv_send(clientSocket, 'You are blocked.\n')

	# Broadcasts a message to all active users.
	elif commandKey == 'broadcast':
		mail = []
		mail = command.split(' ', 1)[1]
		for s in connections:
			if s != servSock:
				try:
					if s != clientSocket:
						s.send('\n"' + nameKey + '" broadcasted: ' + mail + '\nCommand: ')
					else:
						s.send('You yelled: ' + mail + '\n')
				except:
					s.close()
					connections.remove(s)

	# Logs the current user out.
	elif commandKey == 'logout':
		logout(clientSocket, nameKey)

if __name__ == "__main__":
	# check validity of arguments
	if len(sys.argv) != 2 or not sys.argv[1].isdigit():
		print("Usage: python Server.py <port>")

	# Initialize arrays, lists, and values
	PORT 		= int(sys.argv[1])
	connections	= []
	COMMANDS	= ["addfavorite", "tofavorite", "removefavorite", "listfavorite", "whoelse", "wholasthr", "broadcast", "message", "block", "unblock", "logout"]
	usernames  	= [] 
	clients  	= {}
	logoutRec	= {}
	lockedAcc	= {}
	offlineMsg	= {}
	group		= {}

	# Constant times are listed in seconds.
	BLOCK_TIME	= 60
	LAST_HOUR	= 3600 
	TIME_OUT	= 1800 

	# Set up the initial socket object
	servSock 	= socket.socket()
	print 'Socket create success.'
	host		= socket.gethostname()		#Get local machine name
	servSock.bind((host, PORT)) 			#Bind to the port
	print 'Socket bind success.'
	servSock.listen(10)							#Listen for a client
	print 'Socket is listening ...'

	#Append the server socket as a readable connection
	connections.append(servSock)

	# Creates the list of acconts from the given file.
	account = make_account("user_pass.txt")

	while True:
		try:
			readSock, writeSock, errSock = select.select(connections, [], [])
		except KeyboardInterrupt:
			servSock.close()
		except:
			# Error in socket removal from connections
			time.sleep(5)

		for s in readSock:
			if s == servSock:
				#Accept a connection from a client
				clntSock, addr = servSock.accept()	#
				print 'Got connection from', addr
				serv_send(clntSock, 'You have successfully connected!')
				connections.append(clntSock)
				start_new_thread(client_thread, (clntSock, addr))
						
	servSock.close()

