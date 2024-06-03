import rsa
from  Crypto.Cipher import AES
import os
import math
import tqdm
import socket

#CREATE_SOCKET-FUNC THAT RETURNS SOCKET TO SERVER
def Create_socket():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # IP="192.168.0.103"
    # port=9999
    return server



#GET-PRIVATE-KEY AND PUBLIC-KEY
def Get_public_and_private_keys()   :
    # with open("private.pem","rb") as f:
    #     private_key=rsa.PrivateKey.load_pkcs1(f.read())

    # with open("public.pem","rb") as f:
    #     public_key=rsa.PublicKey.load_pkcs1(f.read())
    
    # return public_key,private_key
    public_key,privatekey=rsa.newkeys(1024)
    return public_key,privatekey



def recieve(public_key,communication_socket,private_key) :
    public_key_to_be_sent=public_key.save_pkcs1()
    # print(len(public_key_to_be_sent))
    communication_socket.send(public_key_to_be_sent)

    #client send encrypted and encoded AES key

    key=rsa.decrypt(communication_socket.recv(128),private_key)
    nonce=rsa.decrypt(communication_socket.recv(128),private_key)
    return key,nonce



def run_server(server,communication_socket,key,nonce):   
    cipher=AES.new(key,AES.MODE_EAX,nonce)
    file_name,file_size,data=communication_socket.recv(1024).decode("latin-1").split("<seperator>")
    print(file_name)
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
        data =communication_socket.recv(1024)
        progress.update(1024)
    file.write(cipher.decrypt(file_bytes[:-5]))
    file.close()
    communication_socket.close()
    server.close()


def main():
    IP=input("provide IPv4 adress of the server: ")
    port=int(input("provide the port to operate: "))

    server=Create_socket()
    server.bind((IP,port))
    server.listen()
    communication_socket,add=server.accept()

    public_key,private_key=Get_public_and_private_keys()
    
    key,nonce=recieve(public_key,communication_socket,private_key)
    
    run_server(server,communication_socket,key,nonce)
   

main()







