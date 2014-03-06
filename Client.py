import os,socket,sys,select,string

if __name__ == "__main__":
	if len(sys.argv) != 3 or not sys.argv[2].isdigit():
		print("Usage: client.py <server_IP_address> <port>")

	# Connects to the server socket.
	sock = socket.socket()
	PORT = int(sys.argv[2])
	HOST = sys.argv[1]
	sock.connect((HOST, PORT))

	while True:
		socket_list = [sys.stdin, sock]

		readSock, writeSock, errSock = select.select(socket_list, [], [])

		for s in readSock:
			if s == sys.stdin: # If input is given from client
				message = sys.stdin.readline()
				sock.send(message)
				sys.stdout.flush()
			else : # Input is given from server
				inbox = sock.recv(1024)
				if inbox:
					sys.stdout.write(inbox)
					sys.stdout.flush()
				else :
					# Disconnects.
					print '\nDisconnected.'
					sys.exit()
	
