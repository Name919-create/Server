# Server
Simple python ssh server

# Description
The Python script is designed to create an SSH server on a Linux system. 
It uses the Paramiko library to implement the SSH protocol, and allows clients to connect to 
the server and execute commands remotely.

The script generates an RSA key for the server, and listens for incoming connections on port 22 by default (or on a port number you choose). 
When a client connects, the server prompts the user for a username and password. The username and password are hard-coded into the script, 
but can be changed if desired.

Once authenticated, the client can execute commands on the server using an SSH client. 
The server will execute the commands and send the output back to the client. The server currently only accepts a limited number of commands, 
but can be customized to allow additional commands to be executed.


# Changing port number
1. Locate the line ssh_server = paramiko.Transport(('0.0.0.0', 22)).
2. Change the number 22 to the desired port number.

# Changing username/passowrd
1. Locate the check_auth_password function in the script.
2. Replace the string 'username' with the desired username and the string 'password' with the desired password.




