from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
import os

with open("./clave_privada.pem", "rb") as key_file:
    key = serialization.load_pem_private_key(
        key_file.read(), password=bytes(os.getenv("passw_restaurante"), 'ascii'),)
key_file.close()

# Generate un CSR y se firma con la clave privada del sistema
csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Madrid"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Leganes"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "UC3M"),
    x509.NameAttribute(NameOID.COMMON_NAME, "criptorestaurante.com"),
])).add_extension(
    x509.SubjectAlternativeName([
        x509.DNSName("criptorestaurante.com"),
        x509.DNSName("www.criptorestaurante.com"),
        x509.DNSName("subdomain.criptorestaurante.com"),
    ]),
    critical=False,
).sign(key, hashes.SHA256())

# Escribir el CSR en un pem
with open("csr.pem", "wb") as f:
    f.write(csr.public_bytes(serialization.Encoding.PEM))
f.close()


