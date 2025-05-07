# hashing.py
import hashlib

message1 = b"hello world"
message2 = b"hello World"  # Slightly different

hash1 = hashlib.sha256(message1).hexdigest()
hash2 = hashlib.sha256(message2).hexdigest()

print("Hash of message1:", hash1)
print("Hash of message2:", hash2)
