# rsa_encryption.py
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

# Generate RSA keys with the value of 65537 and key at 2048 to be secure
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

message = b"Hello from RSA by Haziq!"

# encrypt the message using the generated public key,
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
) #OAEP stands for Optimal Asymmetric Encryption Padding, MGF is mask generation, 

# this part decrypt the file
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)


# gives output
print("Original:", message)
print("Encrypted:", ciphertext.hex())
print("Decrypted:", plaintext)


# Show keys in Privacy enchaned mail PEM format, basically readable format
print("\n[Private Key]")
print(private_key.private_bytes(
    encoding=serialization.Encoding.PEM, #specify the output format
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
