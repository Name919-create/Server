import socket
import threading
import paramiko

host_key = paramiko.RSAKey.generate(2048)
ssh_server = paramiko.Transport(('0.0.0.0', 22))
ssh_server.add_server_key(host_key)

class SSHServerHandler(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        if username == 'username' and password == 'password':
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        else:
            return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_exec_request(self, channel, command):
        if command == 'exit':
            channel.send('Goodbye.\r\n')
            channel.close()
            return True
        else:
            channel.send('Unknown command.\r\n')
            return False

    def check_channel_shell_request(self, channel):
        return True

def handle_client(client_socket):
    ssh_session = ssh_server.accept(20)
    if ssh_session is None:
        return
    ssh_session.set_name('SSH')
    server_handler = SSHServerHandler()
    ssh_session.start_server(server_handler)
    channel = ssh_session.accept(20)
    channel.send('Welcome to the SSH server.\r\n')
    while True:
        command = channel.recv(1024)
        if not command:
            break
        server_handler.check_channel_exec_request(channel, command.decode('utf-8'))
    channel.close()
    ssh_session.close()
    client_socket.close()

def start_server():
    ssh_server.listen(100)
    print('Listening for SSH connections on port 22...')
    while True:
        client_socket, address = ssh_server.accept()
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    start_server()
