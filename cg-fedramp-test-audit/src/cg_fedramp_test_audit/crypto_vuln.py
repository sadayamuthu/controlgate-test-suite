import hashlib

def store_password(password: str):
    # Vulnerability: Using weak cryptographic hash (MD5)
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    
    # Vulnerability: Using weak cryptographic hash (SHA1)
    sha1_hash = hashlib.sha1(password.encode()).hexdigest()
    
    print(f"Stored hashes: {md5_hash}, {sha1_hash}")
    return md5_hash
