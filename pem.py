from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

contrasena = 12

#Generacion clave privada
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
#Serializacion privada
pem = private_key.private_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.PKCS8,
   encryption_algorithm=serialization.BestAvailableEncryption(bytes(contrasena))
)
pem.splitlines()[0]
with open("./clave_privada.txt", "wb") as key_file:
    for i in range(len(pem.splitlines())):
        key_file.write(pem.splitlines()[i])
        key_file.write(bytes('\n', 'ascii'))
key_file.close()
#Serializacion clave publica
public_key = private_key.public_key()
pem = public_key.public_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PublicFormat.SubjectPublicKeyInfo
)
pem.splitlines()[0]
with open("./clave_publica.txt", "wb") as key_file:
    for i in range(len(pem.splitlines())):
        key_file.write(pem.splitlines()[i])
        key_file.write(bytes('\n', 'ascii'))
key_file.close()

