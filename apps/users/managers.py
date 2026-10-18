from django.contrib.auth.models import BaseUserManager
from apps.common.crypto import CryptoService, generate_api_key


class UserManager(BaseUserManager):
    """Custom user manager for User model."""

    def create_user(self, email, username, name, password=None, role='USER', **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório.')
        if not username:
            raise ValueError('O username é obrigatório.')
        if not name:
            raise ValueError('O nome é obrigatório.')

        email = self.normalize_email(email)
        username = username.strip().lower()

        # If api_key not provided, generate a new one and encrypt it
        raw_api_key = extra_fields.pop('raw_api_key', None)
        if not extra_fields.get('api_key'):
            prefix = 'adm_' if role == 'ADMIN' else 'dev_'
            raw_key = raw_api_key or generate_api_key(prefix=prefix)
            extra_fields['api_key'] = CryptoService.encrypt(raw_key)

        extra_fields.setdefault('is_active', True)
        if role == 'ADMIN':
            extra_fields.setdefault('is_staff', True)

        user = self.model(
            email=email,
            username=username,
            name=name,
            role=role,
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')

        return self.create_user(
            email=email,
            username=username,
            name=name,
            password=password,
            role='ADMIN',
            **extra_fields
        )
