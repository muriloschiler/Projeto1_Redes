import ssl
import socket
import time

# Configurações do servidor IMAP (substitua com suas credenciais e servidor)
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
EMAIL = 'murilo.teste.email.dev@gmail.com'
PASSWORD = 'ailg zgbk shqc psng'

# Estabelecer conexão com o servidor IMAP via SSL
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wrapped_socket = ssl.wrap_socket(clientSocket)
wrapped_socket.connect((IMAP_SERVER, IMAP_PORT))

# Receber resposta inicial do servidor
print(wrapped_socket.recv(1024).decode())

# Autenticação
print("COMEÇANDO A AUTORIZAÇÃO")
login_command = 'a1 LOGIN "' + EMAIL + '" "' + PASSWORD + '"\r\n'
wrapped_socket.send(login_command.encode('ascii'))
print(wrapped_socket.recv(1024).decode())

# Listar caixas de correio
wrapped_socket.send(b'a2 LIST "" *\r\n')
print(wrapped_socket.recv(1024).decode())

# Selecionar a caixa de entrada (inbox)
print("SELECIONANDO CAIXA DE ENTRADA")
wrapped_socket.send(b'a3 SELECT INBOX\r\n')
print(wrapped_socket.recv(1024).decode())

# Buscar e-mails não lidos
print("BUSCAR E-MAILS NÃO LIDOS ")
wrapped_socket.send(b'a4 SEARCH UNSEEN\r\n')
unread_response = wrapped_socket.recv(1024).decode()
print(unread_response)
email_nums = unread_response.split()
indices = [item for item in email_nums if item.isdigit()]

# Se há e-mails não lidos, buscar o conteúdo deles
if indices:
    print("EMAILS NÃO LIDOS")   
    email_data = b""

    for num in indices:
        command = 'a5 FETCH ' + num + ' (RFC822)\r\n'
        wrapped_socket.send(command.encode('ascii'))
        response = wrapped_socket.recv(1024)
        email_data += response
        response = wrapped_socket.recv(1024)
        email_data += response

    for num in indices:
        response = wrapped_socket.recv(1024)
        email_data += response
    
    print(email_data.decode('utf-8'))

# Encerrar a conexão
print("LOGOUT")
wrapped_socket.send(b'a6 LOGOUT\r\n')
print(wrapped_socket.recv(1024).decode())
wrapped_socket.close()
