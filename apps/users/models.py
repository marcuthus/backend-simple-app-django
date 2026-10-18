import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.common.crypto import CryptoService, generate_api_key
from .managers import UserManager


class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrador'
    USER = 'USER', 'Usuário'


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model matching the simple-app domain requirements."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Nome')
    username = models.CharField(max_length=16, unique=True, verbose_name='Nome de Usuário')
    email = models.EmailField(max_length=150, unique=True, verbose_name='E-mail')
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name='Papel / Cargo'
    )
    api_key = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Chave de API (Criptografada)'
    )

    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    is_staff = models.BooleanField(default=False, verbose_name='Acesso ao Painel Admin')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"

    def save(self, *args, **kwargs):
        # Synchronize is_staff if role is ADMIN
        if self.role == UserRole.ADMIN:
            self.is_staff = True
        elif not self.is_superuser:
            self.is_staff = False

        if not self.api_key:
            prefix = 'adm_' if self.role == UserRole.ADMIN else 'dev_'
            raw_key = generate_api_key(prefix=prefix)
            self.api_key = CryptoService.encrypt(raw_key)

        super().save(*args, **kwargs)

    @property
    def raw_api_key(self) -> str:
        """Returns the decrypted plain API key."""
        return CryptoService.decrypt(self.api_key)

    def regenerate_api_key(self, prefix: str = None) -> str:
        """Regenerates a new encrypted API key and returns the raw plain key."""
        if not prefix:
            prefix = 'adm_' if self.role == UserRole.ADMIN else 'dev_'
        raw_key = generate_api_key(prefix=prefix)
        self.api_key = CryptoService.encrypt(raw_key)
        self.save(update_fields=['api_key', 'updated_at'])
        return raw_key
