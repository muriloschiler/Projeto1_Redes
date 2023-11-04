from getpass import getpass
import ssl
import ssl
from base64 import b64encode
from socket import socket, AF_INET, SOCK_STREAM
from models.message import Message

class GmailSMTP:

    def SendMesage(self, message: Message):
        YOUR_EMAIL = "murilo.teste.email.dev@gmail.com"
        YOUR_PASSWORD = "ailg zgbk shqc psng"
        YOUR_DESTINATION_EMAIL = message.Destination_email
        YOUR_SUBJECT_EMAIL = message.Subject_email
        YOUR_BODY_EMAIL = message.Body

        endmsg = '\r\n.\r\n'

        mailServer = 'smtp.gmail.com'
        mailPort = 587

        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((mailServer, mailPort))

        recv = clientSocket.recv(1024)
        print(recv)
        if recv[:3] != b'220':
            print('220 reply not received from server.')

        heloCommand = 'HELO Server\r\n'.encode()
        clientSocket.send(heloCommand)
        recv1 = clientSocket.recv(1024)
        print(recv1)
        if recv1[:3] != b'250':
            print('250 reply not received from server.')

        print("COMEÇANDO A AUTORIZAÇÃO")
        strtlscmd = "STARTTLS\r\n".encode()
        clientSocket.send(strtlscmd)
        recv2 = clientSocket.recv(1024)

        sslClientSocket = ssl.wrap_socket(clientSocket)

        EMAIL_ADDRESS = b64encode(YOUR_EMAIL.encode())
        EMAIL_PASSWORD = b64encode(YOUR_PASSWORD.encode())

        authorizationcmd = "AUTH LOGIN\r\n"

        print("COMANDO AUTH LOGIN")
        sslClientSocket.send(authorizationcmd.encode())
        recv2 = sslClientSocket.recv(1024)
        print(recv2)

        print("EMAIL_ADDRESS")
        sslClientSocket.send(EMAIL_ADDRESS + "\r\n".encode())
        recv3 = sslClientSocket.recv(1024)
        print(recv3)

        print("EMAIL_PASSWORD")
        sslClientSocket.send(EMAIL_PASSWORD + "\r\n".encode())
        recv4 = sslClientSocket.recv(1024)
        print(recv4)

        mailfrom = "MAIL FROM: <{}>\r\n".format(YOUR_EMAIL)
        sslClientSocket.send(mailfrom.encode())
        recv5 = sslClientSocket.recv(1024)
        print(recv5)

        rcptto = "RCPT TO: <{}>\r\n".format(YOUR_DESTINATION_EMAIL)
        sslClientSocket.send(rcptto.encode())
        recv6 = sslClientSocket.recv(1024)

        data = 'DATA\r\n'
        sslClientSocket.send(data.encode())
        recv7 = sslClientSocket.recv(1024)
        print(recv7)

        sslClientSocket.send("Subject: {}\n\n{}".format(YOUR_SUBJECT_EMAIL, YOUR_BODY_EMAIL).encode())

        sslClientSocket.send(endmsg.encode())
        recv8 = sslClientSocket.recv(1024)
        print(recv8)

        quitcommand = 'QUIT\r\n'
        sslClientSocket.send(quitcommand.encode())
        recv9 = sslClientSocket.recv(1024)
        print(recv9)

        sslClientSocket.close()
        print('Was successful!')

                
        
        