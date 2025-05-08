# rsa_encryption.py
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

# Generate RSA keys
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

message = b"Hello from RSA by Haziq!"

# this part encrypt the file
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

# this part decrypt the file
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)



print("Original:", message)
print("Encrypted:", ciphertext.hex())
print("Decrypted:", plaintext)


# Show keys in PEM format (for proof)
print("\n[Private Key]")
print(private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
).decode())

print("[Public Key]")
print(public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode())

# Simulate using a wrong private key
wrong_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

try:
    broken = wrong_private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("Decrypted with wrong key:", broken)
except Exception as e:
    print("❌ Decryption failed with wrong key:", str(e))
