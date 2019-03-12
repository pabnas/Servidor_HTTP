import socket
import base64
import random
import netifaces as ni

TCP_IP = ni.ifaddresses('wlp3s0')[ni.AF_INET][0]['addr']
TCP_PORT = 1027
print("server in " + TCP_IP + ":" + str(TCP_PORT))
BUFFER_SIZE = 1024

bombillo = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

while 1:
    conn, addr = s.accept()
    data = conn.recv(BUFFER_SIZE)
    msg = data.decode('ascii')
    #print("received data:", msg)
    request_method = msg.split(' ')[0]

    if request_method == "GET":
        file_requested = msg.split(' ')
        file_requested = file_requested[1]
        file_requested = file_requested.split('?')[0]

        msg = ""
        cabecera = "HTTP/1.1 200 OK" + '\n'
        if (file_requested == '/'):
            file_requested = '/index.html'

        if (file_requested.endswith("html")):
            cabecera += "Content-Type: text/html" + '\n' + '\n'
        elif (file_requested.endswith("css")):
            cabecera += "Content-Type: text/css" + '\n' + '\n'
        elif (file_requested.endswith("js")):
            cabecera += "Content-Type: text/js" + '\n' + '\n'
        elif (file_requested.endswith("ico")):
            cabecera += "Content-Type: image/ico" + '\n' + '\n'
        elif (file_requested.endswith("png")):
            cabecera += "Content-Type: image/png" + '\n' + '\n'
        elif (file_requested.endswith("jpg")):
            cabecera += "Content-Type: image/jpg" + '\n' + '\n'
        elif (file_requested.endswith("jpeg")):
            cabecera += "Content-Type: image/jpeg" + '\n' + '\n'
        elif (file_requested.endswith("bool")):
            cabecera += "Content-Type: text/plain" + '\n' + '\n'
        else:
            cabecera += "Content-Type: text/html" + '\n' + '\n'


        print("Se pidio " + file_requested)

        file_requested = "www" + file_requested
        try:
            if file_requested.endswith("png") | file_requested.endswith("ico")| file_requested.endswith("gif") | file_requested.endswith("jpeg") | file_requested.endswith("jpg"):
                image_data = open(file_requested, 'rb')
                bytes = image_data.read()
                content = bytes
                image_data.close()
                msg = content
            elif file_requested.endswith("bool"):
                var = file_requested.split('.')[0]
                if var.endswith("b"):
                    bombillo = not(bombillo)
                    if bombillo == True:
                        msg = "on"
                    else:
                        msg = "off"
                elif var.endswith("t_d"):
                    if random.randint(0, 1) == 0:
                        msg = "off"
                    else:
                        msg = "on"
                msg = msg.encode()
            else:
                with open(file_requested, 'r') as f:
                    archivo =f.read()
                archivo = [x.strip('\t') for x in archivo]
                archivo = [x.strip('\n') for x in archivo]
                archivo = ''.join(archivo)
                archivo = filter(None, archivo.split("  "))
                archivo = ''.join(archivo)
                msg = str(archivo) + '\n'
                msg=msg.encode()

        except Exception as ex:
            cabecera = "HTTP/1.1 404 Not Found" + '\n'
            msg = "Connection: close" + '\n' + '\n'
            msg = msg.encode()
            print(ex)

        msg = cabecera.encode() + msg
        conn.send(msg)
        conn.close()

while True:
    conn, addr = s.accept()

    print("Got connection from:", addr)

    data = conn.recv(1024) #receive data from client
    string = bytes.decode(data) #decode it to string

    #determine request method  (HEAD and GET are supported)
    request_method = string.split(' ')[0]
    print ("Method: ", request_method)
    print ("Request body: ", string)

     #if string[0:3] == 'GET':
    if (request_method == 'GET') | (request_method == 'HEAD'):
         #file_requested = string[4:]

         # split on space "GET /file.html" -into-> ('GET','file.html',...)
         file_requested = string.split(' ')
         file_requested = file_requested[1] # get 2nd element

         #Check for URL arguments. Disregard them
         file_requested = file_requested.split('?')[0]  # disregard anything after '?'

         if (file_requested == '/'):  # in case no file is specified by the browser
             file_requested = 'pagina.html' # load index.html by default

         file_requested = " "+ file_requested
         print ("Serving web page [",file_requested,"]")

         ## Load file content
         try:
             file_handler = open(file_requested,'rb')
             if (request_method == 'GET'):  #only read the file when GET
                 response_content = file_handler.read() # read file content
             file_handler.close()

             response_headers = "HTTP/1.1 200 OK"

         except Exception as e: #in case file was not found, generate 404 page
             print ("Warning, file not found. Serving response code 404\n", e)
             response_headers = "HTTP/1.1 404 OK"

             if (request_method == 'GET'):
                response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"

         server_response =  response_headers.encode() # return headers for GET and HEAD
         if (request_method == 'GET'):
             server_response +=  response_content  # return additional content for GET only

         conn.send(server_response)
         print ("Closing connection with client")
         conn.close()

    else:
        print("Unknown HTTP request method:", request_method)