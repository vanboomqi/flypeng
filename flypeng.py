import socket
import argparse
import secrets
import os
import hashlib
from threading import Thread
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

def encrypt_rsa(public_key, message):

    rsakey = RSA.importKey(public_key)
    cipher = PKCS1_OAEP.new(rsakey)
    ciphertext = cipher.encrypt(message)
    return ciphertext


def decrypt_rsa(private_key, ciphertext):
    rsakey = RSA.importKey(private_key)
    cipher = PKCS1_OAEP.new(rsakey)
    message = cipher.decrypt(ciphertext)
    return message




class AesCrypto():
    def __init__(self, key, IV):
        self.key = key
        self.iv = IV
        self.mode = AES.MODE_CBC
    
    # 加密函数，text参数的bytes类型必须位16的倍数，不够的话，在末尾添加"\0"(函数内以帮你实现)
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv) # self.key的bytes长度是16的倍数即可， self.iv必须是16位
        length = 16
        count = len(text)
        if(count%length != 0):
            add = length-(count%length)
        else:
            add=0

        text = text+("\0".encode()*add)  # 这里的"\0"必须编码成bytes，不然无法和text拼接

        self.ciphertext = cryptor.encrypt(text)
        return (self.ciphertext)
    
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt((text)).decode()
        # return plain_text.rstrip("\0")  有的博客上有这句，其实decode解码之后"\0"自动就没有了
        return plain_text
    

def server():
    if os.path.isfile("private.pem") == False :
        print('Please wait for the rsa key pair to be generated...')
        random_generator = Random.new().read
        # rsa算法生成实例
        rsa = RSA.generate(4096, random_generator)
        # 私钥的生成
        private_pem = rsa.exportKey()
        with open("private.pem", "wb") as f:
            f.write(private_pem)
        # 公钥的生成
        public_pem = rsa.publickey().exportKey()
        with open("public.pem", "wb") as f:
            f.write(public_pem)
    with open("public.pem") as f:
        public_pem = f.read()
        print('Public key sha256: '+ hashlib.sha256(public_pem.encode()).hexdigest())
    with open("private.pem") as f:
        private_pem = f.read()
    s = socket.socket()
    s.bind((args.l, args.p))
    s.listen(1)
    conn, addr = s.accept()
    print('connected:', addr)
    conn.send(public_pem.encode())
    key = decrypt_rsa(private_pem,conn.recv(4096))
    def recv():
        while True:
            data = conn.recv(1024)
            if not data: break
            pc = AesCrypto(key, IV)
            data = pc.decrypt(data)  # 解密数据
            print("Received:"+data)
    def send():
        while True:
            pc = AesCrypto(key, IV)
            conn.send(pc.encrypt(input().encode()))

    Thread(target=recv).start()
    Thread(target=send).start()

def client():
    s = socket.socket()
    s.connect((args.r, args.p))
    data = s.recv(4096)
    sha_list = []
    sha256 = hashlib.sha256(data).hexdigest()
    if os.path.isfile("config.txt") == True :
        with open('config.txt', 'r') as f:
            sha_list = eval(f.read())
    if sha256 not in sha_list :
        y = input('Public key sha256: ' + sha256 + '  y/n?\n')
        if (y != 'Y' and y !='y') :
            exit(0)
        print('Add public key sha256 to config.txt.')
        sha_list.append(sha256)
        with open('config.txt', 'w') as f:
            f.write(str(sha_list))
    print('Connection succeeded!\n')
    key = secrets.token_bytes(16)
    s.send(encrypt_rsa(data,key))
    def recv():
        while True:
            data = s.recv(1024)
            if not data: break
            pc = AesCrypto(key, IV)
            data = pc.decrypt(data)  # 解密数据
            print("Received:"+data)
        exit(0)
    def send():
        while True:
            pc = AesCrypto(key, IV)
            s.send(pc.encrypt(input().encode()))

    Thread(target=recv).start()
    Thread(target=send).start()


if __name__== "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', type=str , help='rhost ip')
    parser.add_argument('-s', action='store_true',help='server')
    parser.add_argument('-l', type=str , default='0.0.0.0',help='listen ip')
    parser.add_argument('-p', type=int , default=10235, help='port')
    args = parser.parse_args()
    IV = b"GPk40oNBTGoXlW6r"
    if args.s :
        server()
    else :
        client()
