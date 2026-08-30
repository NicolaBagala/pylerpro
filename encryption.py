import os 
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt 
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

FILE_MAGIC = b"PYLERPRO0.4"

# Scrypt parameters recommended/default values
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_LENGTH = 32
COST_PARAMETER = 2**14
BLOCK_SIZE = 8
PARALLELIZATION = 1

def derive_key(password, salt):
    """
    Derive the encryption key from a password for a given salt and default Scrypt parameters.
    password is any string. salt is a random bytes object of length SALT_SIZE.
    Return a bytes object of length KEY_LENGTH (the encryption key).
    """
    kdf = Scrypt(
        salt = salt,
        length = KEY_LENGTH,
        n = COST_PARAMETER, 
        r = BLOCK_SIZE,
        p = PARALLELIZATION
    )

    return kdf.derive(password.encode("utf-8"))

def encrypt(key, data):
    """
    Encrypt data via AESGCM using key as an encryption key.
    key is a KEY_LENGTH bytes object. data is plain text.
    Return a tuple containing the encrypted data and the nonce, both in bytes.    
    """

    data = data.encode("utf-8")
    nonce = os.urandom(NONCE_SIZE)

    aesgcm = AESGCM(key)
    encrypted_data = aesgcm.encrypt(nonce, data, None)
    return encrypted_data, nonce

def decrypt(key, nonce, encrypted_data):    
    """
        Decrypt encrypted_data via AESGCM using the given nonce and key as a decryption key.
        key is a KEY_LENGTH bytes object. nonce is a bytes object of length NONCE_SIZE. 
        encrypted_data is a bytes_object.
        Return decrypted_data in plain text string format.
    """

    aesgcm = AESGCM(key)    
    decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)    
    return decrypted_data.decode("utf-8")

def serialize_encrypted_vault(salt, nonce, encrypted_data):    
    """
        Serialize an encrypted vault from its four constituents.
        FILE_MAGIC is a bytes string. 
        salt and nonce are bytes object of length SALT_SIZE and NONCE_SIZE respectively. 
        encrypted_data is a bytes object. 
        Return the concatenated constituents.
    """
    return FILE_MAGIC + salt + nonce + encrypted_data


def deserialize_encrypted_vault(vault_file):
    """
        Deserialize an encrypted vault by parsing its representation in bytes.
        vault_file is a bytes object representing a serialized encrypted vault.
        Return a quadruple of bytes objects extracted from vault_file (magic, salt, nonce, and encrypted_data)
    """

    
    offset = len(FILE_MAGIC)    
    magic = vault_file[0:offset]

    salt = vault_file[offset:offset + SALT_SIZE]
    offset += SALT_SIZE
    
    nonce = vault_file[offset:offset + NONCE_SIZE]
    offset += NONCE_SIZE

    encrypted_data = vault_file[offset:]

    return magic, salt, nonce, encrypted_data
