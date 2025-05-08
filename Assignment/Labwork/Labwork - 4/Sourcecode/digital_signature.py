# telling the code we want to import the following stuff from the library to help us make the code work
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Generate keys
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

message = b"This message is signed by Haziq."

# Sign
signature = private_key.sign(
    message,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

# Tamper with the message (simulate attacker)
tampered_message = b"This message is NOT signed by Haziq."

try:
    public_key.verify(
        signature,
        tampered_message,  
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("❌ Tampered message verified (this should NOT happen!)")
except:
    print("🚨 Verification failed: Message has been altered!")

# Verify
try:
    public_key.verify(
        signature,
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    print("✅ Signature is valid!")
except:
    print("❌ Signature is invalid.")
