from Crypto.Cipher import AES
from hashlib import sha256
import os

# Rebuild the same key
KEY_STR = "BukanRahsiaLagi"
KEY = sha256(KEY_STR.encode()).digest()[:16]

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def decrypt_file(filepath):
    with open(filepath, "rb") as f:
        ciphertext = f.read()
    
    cipher = AES.new(KEY, AES.MODE_ECB)
    decrypted_padded = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted_padded)

    # Save decrypted file (remove .enc)
    output_path = filepath.replace(".enc", "_decrypted.txt")
    with open(output_path, "wb") as f:
        f.write(plaintext)
    print(f"✅ Decrypted: {output_path}")

# Decrypt all .enc files in the "locked_files" folder
target_folder = "locked_files"
for filename in os.listdir(target_folder):
    if filename.endswith(".enc"):
        decrypt_file(os.path.join(target_folder, filename))
