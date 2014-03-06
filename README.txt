================================================================
This is a simple chat server and client written in Python 2.7.3.

Author	: Brian Yamamoto
UNI		: bky2102
Class	: Computer Networking
Term 	: Spring 2014

================================================================

a) This code creates a simple chat server and chat client.

	There are only two .py files that make up this project:

		server.py
		client.py

	The Server.py performs to specifications: that is, it is invoked via:

		python Server.py <port>

	and will create a server and listen for clients. All variable names
	(TIME_OUT, LAST_HOUR, BLOCK_TIME) will be listed in the main function
	near the bottom of the code.

	The Client.py also performs to specifications: it will be invoked via:

		python Client.py <ip-address> <port>

	and will connect to the server specified in the argument.

Notes on required functionality:

	whoelse 					- works as requested in assignment
	wholasthr					- works as requested in assignment
	broadcast <message>			- works as requested in assignment
	message <user> <message>	- works as requested (including off-line) in assignment
	block <user>				- works as requested in assignment
	unblock <user>				- works as requested in assignment
	logout						- works as requested in assignment

b) Development environment

This code was written in a UNIX OS, with Python 2.7.3. The code will NOT work in Windows
due to conflicting issues regarding Python's select.select() function. The compile method
was specified above.

c) How to run the code:

There are no special requests - each segment of the code should run as specified. The client
simply needs to type the command and <enter> in order to execute the command. Misspelled commands or other errors should not break the code.

d) 

SERVER
dyn-160-39-233-118:Py-Chat Yams$ python Server.py 4119
Socket create success.
Socket bind success.
Socket is listening ...

CLIENT
dyn-160-39-233-118:Py-Chat Yams$ python client.py 160.39.233.118 4119
You have successfully connected!
Username: foobar
Password: pass
Incorrect password. Attempts left: 2
Password: passpass
You have signed in!
Command: whoelse
foobar
Command: wholasthr
foobar
Command: block foobar
You cannot block yourself!
Command: block blah
That user does not exist!
Command: block wikipedia
That user is offline!
Command: block windows
You have blocked windows.
Command: message windows hahaha, I blocked you.
Command: broadcast Windows blows!
You yelled: Windows blows!
Command: unblock windows
You have unblocked windows.
Command: 
"windows": come on man, be cool 
Command: wholasthr
foobar
windows
Command: whoelse
foobar
windows
Command: logout
Logging off.
Disconnected.
dyn-160-39-233-118:Py-Chat Yams$ 

e) Additional functionalities.

1. When a user makes an error in logging in, the code passes the user the amount of attempts left.

2. If a user is locked out and attempts to log back in, the user is informed of his/her locked-out status as well as the elapsed time remaining before relog-in is allowed.

EXAMPLE CODE FOR 1 AND 2:

dyn-160-39-233-118:Py-Chat Yams$ python client.py 160.39.233.118 4119
You have successfully connected!
Username: foobar
Password: oh no 
Incorrect password. Attempts left: 2
Password: I forgot
Incorrect password. Attempts left: 1
Password: my password
Incorrect password. You are locked out for 60 seconds.
Logging off.
Disconnected.
dyn-160-39-233-118:Py-Chat Yams$ python client.py 160.39.233.118 4119
You have successfully connected!
Username: foobar
You are still locked out for 50.847901 seconds.
Logging off.
Disconnected.
dyn-160-39-233-118:Py-Chat Yams$ python client.py 160.39.233.118 4119
You have successfully connected!
Username: foobar
You are still locked out for 44.031821 seconds.
Logging off.
Disconnected.
dyn-160-39-233-118:Py-Chat Yams$ 


3. Users may also set other users as their 'favorites.' The command required is:

	addfavorite <user>

Users may list their current favorites as:

	listfavorite

Users may also remove favorites via:

	removefavorite <user>

All three commands will return confirmation if the action is carried out successfully.

Users should also be able to message only their favorites via:

	tofavorite <message>

Currently, there's an issue with passing the message, however.