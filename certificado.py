from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives.serialization import load_pem_public_key

from cryptography.hazmat.primitives.asymmetric import padding
'''m
with open("./clave_privada.txt", "rb") as key_file:
    key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )
key_file.close()

# Generate a CSR
csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    # Provide various details about who we are.
    x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Madrid"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Leganes"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "UC3M"),
    x509.NameAttribute(NameOID.COMMON_NAME, "criptorestaurante.com"),
])).add_extension(
    x509.SubjectAlternativeName([
        # Describe what sites we want this certificate for.
        x509.DNSName("criptorestaurante.com"),
        x509.DNSName("www.criptorestaurante.com"),
        x509.DNSName("subdomain.criptorestaurante.com"),
    ]),
    critical=False,
# Sign the CSR with our private key.
).sign(key, hashes.SHA256())

# Write our CSR out to disk.
with open("CSR.pem", "wb") as f:
    f.write(csr.public_bytes(serialization.Encoding.PEM))
f.close()
'''
with open("./CSRcert.pem", "rb") as key_file:
   pem_data = key_file.read()
key_file.close()
cert = x509.load_pem_x509_certificate(pem_data)

with open("./ac1cert.pem", "rb") as key_file:
   pem_AC = key_file.read()
key_file.close()
certAc = x509.load_pem_x509_certificate(pem_AC)

#print(cert.serial_number)
#print(cert.version)
#cert.fingerprint(hashes.SHA256())

public_key_Ac = certAc.public_key()
#public_key= cert.public_key()
#print(isinstance(public_key, rsa.RSAPublicKey))

issuer_public_key = load_pem_public_key(pem_AC)
cert_to_check = x509.load_pem_x509_certificate(pem_AC)

issuer_public_key.verify(
    cert_to_check.signature,
    cert_to_check.tbs_certificate_bytes,
    # Depends on the algorithm used to create the certificate
    padding.PKCS1v15(),
    cert_to_check.signature_hash_algorithm,
)




