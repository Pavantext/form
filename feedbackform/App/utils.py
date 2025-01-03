import base64
import json
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Create Fernet instance
fernet = Fernet(settings.ENCRYPTION_KEY)

def encrypt_data(data):
    """Encrypt data dictionary to a URL-safe string"""
    try:
        json_data = json.dumps(data)
        encrypted_data = fernet.encrypt(json_data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    except Exception as e:
        logger.error(f"Encryption error: {str(e)}")
        raise

def decrypt_data(encrypted_data):
    """Decrypt URL-safe string back to data dictionary"""
    try:
        decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = fernet.decrypt(decoded_data)
        return json.loads(decrypted_data.decode())
    except InvalidToken:
        logger.error("Invalid encryption token")
        return None
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        return None 