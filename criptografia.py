from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


#Archido donde están todos los métodos de criptografía


def decodificar(key):
    key = bytes(key, 'ascii')
    key = base64.b64decode(key)
    return key

def codificar(key):
    key = base64.b64encode(key)
    key = key.decode('ascii')
    return key


#Metodo para poder derivar y verificar las contraseñas
def kdf_crear(salt):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2 ** 14,
        r=8,
        p=1,
    )
    return kdf

#Método para generar una clave, para poder encriptar los datos
def pbk(salt_clave):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_clave,
        iterations=480000,
    )
    return kdf

#Metodo para poder encriptar los datos, con el algoritmo chacha
def chacha_encri(chacha, fecha):
    fecha = str(fecha)
    data = bytes(fecha.encode('ascii'))
    nonce = os.urandom(12)
    ct = chacha.encrypt(nonce, data, None)
    return ct, nonce


#Metodo para derivar la contraseña original, para poder cifrar los datos
def key_derive(contrasena, salt_clave):
    kdf = pbk(salt_clave)
    key = kdf.derive(contrasena.encode('ascii'))
    return key
