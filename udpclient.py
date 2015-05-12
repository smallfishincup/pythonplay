import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 1111))
s.listen(2048)
print ("Listening on port 1111.. ")
(client, (ip, port)) = s.accept()
print (" recived connection from : ", ip)
while True:
    command = input('~$ ')
    encode = bytearray(command.encode('utf-8'))
    for i in range(len(encode)):
        encode[i] ^= 0x41    
    client.send(encode)
    en_data = client.recv(2048) 
    decode = bytearray(en_data)
    for i in range(len(decode)):
        decode[i] ^= 0x41
    print (str(decode))
client.close()
s.close()
