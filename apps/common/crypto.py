import os
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from django.conf import settings


class CryptoService:
    """Service to handle AES-256-CBC encryption and decryption."""

    @classmethod
    def _get_key_and_iv(cls):
        key_hex = getattr(settings, 'ENCRYPTION_KEY', '')
        iv_hex = getattr(settings, 'ENCRYPTION_IV', '')

        if not key_hex or not iv_hex:
            # Fallback default for development if not configured
            key_hex = '305b4d83eae2e3e00484336539a8ecd29c841a86f1087e5768cf4f09344266f6'
            iv_hex = '18859ed3ccba5ece96c6f7fb3edf3b94'

        return bytes.fromhex(key_hex), bytes.fromhex(iv_hex)

    @classmethod
    def encrypt(cls, text: str) -> str:
        """Encrypts plain text and returns a hex-encoded string."""
        if not text:
            return ''

        key, iv = cls._get_key_and_iv()
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(text.encode('utf-8')) + padder.finalize()

        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return encrypted.hex()

    @classmethod
    def decrypt(cls, encrypted_hex: str) -> str:
        """Decrypts a hex-encoded cipher text back to plain text."""
        if not encrypted_hex:
            return ''

        try:
            key, iv = cls._get_key_and_iv()
            backend = default_backend()
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
            decryptor = cipher.decryptor()

            encrypted_bytes = bytes.fromhex(encrypted_hex)
            decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()

            unpadder = padding.PKCS7(128).unpadder()
            decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
            return decrypted.decode('utf-8')
        except Exception:
            return ''


def generate_api_key(prefix: str = 'dev_', random_chars_length: int = 32) -> str:
    """Generates a secure API key with prefix and random hex characters."""
    token = secrets.token_hex(random_chars_length // 2)
    return f"{prefix}{token}"
