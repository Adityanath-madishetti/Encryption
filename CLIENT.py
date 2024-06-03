import rsa
from  Crypto.Cipher import AES
import os
import math
import tqdm
import socket

def Create_socket():
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    return client

def generate_key_nonce():
    key = os.urandom(16)
    nonce=os.urandom(16)
    return key,nonce
# IP="192.168.0.103"
# port=9999

def send_key(client,key,nonce):
    pub_key=client.recv(251)
    public_key=rsa.PublicKey.load_pkcs1(pub_key)
    enc_key=rsa.encrypt(key,public_key)
    enc_nonce=rsa.encrypt(nonce,public_key)
    client.send(enc_key)
    client.send(enc_nonce)




def upload(client,key,nonce):
    cipher=AES.new(key,AES.MODE_EAX,nonce)
    filename=input("enter-filename (inclue format such as .txt)")
    file_size=os.path.getsize(filename)

    f=open(filename,"rb")
    data=f.read()
    f.close()

    encrypted_data=cipher.encrypt(data)

    client.send(f"{"recieved"+filename}<seperator>{file_size}<seperator>".encode("latin-1"))
    
    client.sendall(encrypted_data)
    client.send(b"<end>")

    client.close()


def main():   
    IP=input("provide IPv4 adress of the server : ")
    port=int(input("provide the port to operate : "))
    key,nonce=generate_key_nonce()
    client=Create_socket()
    client.connect((IP,port))
    send_key(client,key,nonce)
    upload(client,key,nonce)

main()