from cryptography.fernet import Fernet 
import base64
import os

def encrypted(Password):
    key=bytes(os.getenv('fernet_key'), "utf8")
    
    fernet_ = Fernet(key)  
    encrypted_ = fernet_.encrypt(bytes(Password,"utf-8")) 
    incrypted_pass = base64.b64encode(encrypted_, altchars=None).decode("utf-8")
    return incrypted_pass


def dercypted(incrypted_pass):
    key=bytes(os.getenv('fernet_key'), "utf8")
    fernet_ = Fernet(key)
    decrypted_password = fernet_.decrypt(base64.b64decode(incrypted_pass))
    
    return decrypted_password.decode('utf-8')