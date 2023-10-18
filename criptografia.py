from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


def decodificar(key):
    key = bytes(key, 'ascii')
    key = base64.b64decode(key)
    return key

def codificar(key):
    key = base64.b64encode(key)
    key = key.decode('ascii')
    return key


def kdf_crear(salt):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2 ** 14,
        r=8,
        p=1,
    )
    return kdf

def pbk(salt_clave):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_clave,
        iterations=480000,
    )
    return kdf

def chacha_encri(chacha, fecha):
    fecha = str(fecha)
    data = bytes(fecha.encode('ascii'))
    nonce = os.urandom(12)
    ct = chacha.encrypt(nonce, data, None)
    return ct, nonce


def key_f(contrasena, salt_clave):
    kdf = pbk(salt_clave)
    key = kdf.derive(contrasena.encode('ascii'))
    return key