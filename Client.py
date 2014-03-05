import os,socket,sys,select,string

def socket_closed(sock):
	print('Socket closed')
	sock.close()

def clnt_send(sock, message):
	try:
		sock.send(message)
	except IOError:
		socket_closed(sock)

def clnt_recv(sock):
	try:
		print sock.recv(1024)
	except IOError:
		socket_closed(sock)

if __name__ == "__main__":
	if len(sys.argv) != 2 or not sys.argv[1].isdigit():
		print("Usage: client.py <server_IP_address> <port>")

	sock = socket.socket()
	host = socket.gethostname()#TODO you want to get the ip address from the sys.argv
	sock.connect((host, int(sys.argv[1])))

	while True:
		socket_list = [sys.stdin, sock]

		readSock, writeSock, errSock = select.select(socket_list, [], [])

		for s in readSock:
			if s == sys.stdin:
				message = sys.stdin.readline()
				sock.send(message)
				#sys.stdout.write('\n')
				sys.stdout.flush()
			else :
				inbox = sock.recv(1024)
				if inbox:
					sys.stdout.write(inbox + '\n')
					sys.stdout.flush()
				else :
					print '\nDisconnected.'
					sys.exit()
	
