import socket
import  tqdm
import os
from  Crypto.Cipher import AES

key=b"TheAdityanathMaN"
nonce=b"abcdefghijklmnop"
# print(len(key))
# print(len(nonce))

cipher=AES.new(key,AES.MODE_EAX,nonce)
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("localhost",9999))
server.listen()

client,addr=server.accept()


file_name,file_size,data=client.recv(1024).decode("latin-1").split("<seperator>")
file=open(file_name,"wb")
file_bytes=b""
progress=tqdm.tqdm(unit="B",unit_scale=True,unit_divisor=1000,
                   total=int(file_size))

data = data.encode("latin-1")
done=False
while(not done):
    
    if file_bytes[-5:]==b"<end>":
        done=True
    else:
        file_bytes+=data
    data =client.recv(1024)
    progress.update(1024)
file.write(cipher.decrypt(file_bytes[:-5]))
file.close()
client.close()
server.close()
