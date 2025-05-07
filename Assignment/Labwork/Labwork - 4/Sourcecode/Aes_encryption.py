# this is to basically calling on the following librarys to help do the commands 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# generate random bytes, specifically 32 bytes 
key = os.urandom(32)  # 256-bit key
iv = os.urandom(16)   # AES block size
message = b"Cryptography Lab by Haziq@NWS0200!"

# since aes require a message to be in a block, this helps to make sure the number of bits is enough by adding padding
while len(message) % 16 != 0:
    message += b' '

cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(message) + encryptor.finalize()

decryptor = cipher.decryptor()
decrypted = decryptor.update(ciphertext) + decryptor.finalize()

print("Original:", message)
print("Encrypted:", ciphertext.hex())
print("Decrypted:", decrypted)
