================================================================
This is a simple chat server and client written in Python 2.7.3.

Written by Brian Yamamoto
Spring 2014

================================================================

This project consists of:

    server.py
    client.py
    user_pass.txt

  server.py is a simple server program. It is invoked with:

    python Server.py <port>

  and will create a server and listen for clients. All variable names
  (TIME_OUT, LAST_HOUR, BLOCK_TIME) will be listed in the main function
  near the bottom of the code.

  client.py is a simple client program. It is invoked with:

    python Client.py <ip-address> <port>

  and will connect to the server specified in the argument. Multiple instances
  of the client program (with each instance supporting one client) are supported.

  user_pass.txt is a textfile that contains valid combinations of usernames and passwords
  used to authenticate the clients. user_pass.txt must be in the same directory as the server.
  The format of the entries are:

    [Username] [Password]

    For example:

      foobar passpass
      windows withglass

Possible commands runnable by a client after connection:

  whoelse                   - displays names of other connected users
  wholasthr                 - displays names of only those users that connected within the last hour 
  broadcast <message>       - broadcasts <message> to all connected users
  message <user> <message>  - sends <message> privately to <user> 
  block <user>              - blocks <user> from sending any messages. If <user> is self, display error 
  unblock <user>            - unblocks <user> if blocked. If <user> not blocked, display error 
  logout                    - log out this user 

b) Development environment

This code was written in a UNIX OS, with Python 2.7.3. The code will NOT work in Windows
due to conflicting issues regarding Python's select.select() function. The compile method
was specified above.

c) Example output:

SERVER
dyn-[ip address]:Py-Chat Yams$ python Server.py 4119
Socket create success.
Socket bind success.
Socket is listening ...

CLIENT
dyn-[ip address]:Py-Chat Yams$ python client.py [ip address] 4119
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
dyn-[ip address]:Py-Chat Yams$ 
