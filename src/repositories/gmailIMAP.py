import ssl
import socket
import re
import json

class GmailIMAP:

        def GetInboxList(self):
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
            imap_response = wrapped_socket.recv(1024).decode()
            print(imap_response)
            
            # Encerrar a conexão
            print("LOGOUT")
            wrapped_socket.send(b'a6 LOGOUT\r\n')
            print(wrapped_socket.recv(1024).decode())
            wrapped_socket.close()

            #Parser da resposta 
            lines = imap_response.strip().split('\r\n')
            info_lines = lines[:-1]
            mailboxes = []
            for line in info_lines:
                match = re.match(r'\* LIST \((.*?)\) "(.+)" "(.+)"', line)
                if match:
                    flags = match.group(1)
                    delimiter = match.group(2)
                    name = match.group(3)
                    mailbox_info = {
                        "flags": flags.split(),
                        "delimiter": delimiter,
                        "name": name
                    }
                    mailboxes.append(mailbox_info)
            # Convertendo para JSON
            json_data = json.dumps(mailboxes, indent=2)
            print("JSON:")
            print(json_data)
            
            return json_data
        
        def PostSelectInbox(self):
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
            
            # Selecionar a caixa de entrada (inbox)
            print("SELECIONANDO CAIXA DE ENTRADA")
            wrapped_socket.send(b'a3 SELECT INBOX\r\n')
            print(wrapped_socket.recv(1024).decode())

            # Encerrar a conexão
            print("LOGOUT")
            wrapped_socket.send(b'a6 LOGOUT\r\n')
            print(wrapped_socket.recv(1024).decode())
            wrapped_socket.close()
        
        def GetUnreadEMails(self):
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
            imap_response = b""
            # Se há e-mails não lidos, buscar o conteúdo deles
            if indices:
                print("EMAILS NÃO LIDOS")   

                for num in indices:
                    command = 'a5 FETCH ' + num + ' (RFC822)\r\n'
                    wrapped_socket.send(command.encode('ascii'))
                    response = wrapped_socket.recv(1024)
                    imap_response += response
                    response = wrapped_socket.recv(1024)
                    imap_response += response

                for num in indices:
                    response = wrapped_socket.recv(1024)
                    imap_response += response

                print(imap_response.decode('utf-8'))
                
            # Encerrar a conexão
            print("LOGOUT")
            wrapped_socket.send(b'a6 LOGOUT\r\n')
            print(wrapped_socket.recv(1024).decode())
            wrapped_socket.close()

            #Parser da resposta 
            imap_response = imap_response[1:-1]
            emails_data = re.split(r'\* \d+ FETCH ', imap_response.decode('utf-8'))
            emails = []
            for email_info in emails_data:
                match = re.search(r'RFC822 \{(\d+)\}(.+?)FLAGS', email_info, re.DOTALL)
                if match:
                    email_body = match.group(2).strip()
                    email = {
                        "RFC822_Size": int(match.group(1)),
                        "Email": email_body
                    }
                    emails.append(email)

            # Convertendo para JSON
            json_data = json.dumps(emails, indent=2)
            print("JSON:")
            print(json_data)

            return json_data

            


        