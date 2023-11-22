from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
import os

#Generacion clave privada
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
#Serializacion privada
pem = private_key.private_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.PKCS8,
   encryption_algorithm=serialization.BestAvailableEncryption(bytes(os.getenv("passw_restaurante"), 'ascii'))
)

with open("./clave_privada.pem", "wb") as key_file:
    key_file.write(pem)

key_file.close()

#Creacion clave publica
public_key = private_key.public_key()

#Serializacion clave publica
pem = public_key.public_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open("./clave_publica.pem", "wb") as key_file:
    key_file.write(pem)

key_file.close()

