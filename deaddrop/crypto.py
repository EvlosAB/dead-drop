from cryptography.fernet import Fernet


def encrypt(text: str) -> tuple:
    """
    Encrypt a message

    :param text: text to encrypt
    :type text: str
    :returns: tuple with key and token
    :rtype: tuple
    """
    key = Fernet.generate_key()
    fernet = Fernet(key)
    token = fernet.encrypt(text.encode('UTF-8'))

    # Key: bytes, token: bytes
    return (key, token)


def decrypt(key: bytes, token: bytes) -> str:
    """
    Decrypt a message with a key

    :param key:
    :type key: bytes
    :param token:
    :type token: bytes
    :returns: decrypted message
    :rtype: str
    """
    fernet = Fernet(key)
    message = fernet.decrypt(token)

    return message.decode('UTF-8')
