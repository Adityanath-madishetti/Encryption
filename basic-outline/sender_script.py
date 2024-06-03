#client
from  Crypto.Cipher import AES
import os
import socket
key=b"TheAdityanathMaN"
nonce=b"abcdefghijklmnop"
# print(len(key))
# print(len(nonce))

cipher=AES.new(key,AES.MODE_EAX,nonce)

#creating socket object

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("localhost",9999))
file_size=os.path.getsize("TEST_FILE")

f=open("TEST_FILE","rb")
data=f.read()
f.close()

encrypted_data=cipher.encrypt(data)
print(type(encrypted_data))
print(encrypted_data)
client.send(f"TEST_FILE.txt<seperator>{file_size}<seperator>".encode("latin-1"))
# client.send(str(file_size).encode())
client.sendall(encrypted_data)
client.send(b"<end>")
client.close()

