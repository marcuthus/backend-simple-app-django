from django.core.management.base import BaseCommand
from django.conf import settings
from apps.users.models import User, UserRole
from apps.common.crypto import CryptoService


class Command(BaseCommand):
    help = 'Cria ou atualiza o usuário administrador padrão com base nas variáveis de ambiente.'

    def handle(self, *args, **options):
        email = getattr(settings, 'ADMIN_DEFAULT_EMAIL', 'admin@email.com')
        username = getattr(settings, 'ADMIN_DEFAULT_USERNAME', 'admin')
        password = getattr(settings, 'ADMIN_DEFAULT_PASSWORD', 'admin123456')
        name = getattr(settings, 'ADMIN_DEFAULT_NAME', 'Admin')
        raw_api_key = getattr(
            settings,
            'ADMIN_DEFAULT_API_KEY',
            'adm_15b7bb01a40ebf40789f23296ed348aed9ef161caa3634f1f0f8892151c10b4d' 
        )

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'name': name,
                'role': UserRole.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )

        # Update fields to match current defaults
        user.username = username
        user.name = name
        user.role = UserRole.ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.api_key = CryptoService.encrypt(raw_api_key)
        user.save()

        action = "criado" if created else "atualizado"
        self.stdout.write(
            self.style.SUCCESS(
                f"Usuário Administrador padrão {action} com sucesso!\n"
                f"  E-mail:    {email}\n"
                f"  Username:  {username}\n"
                f"  Senha:     {password}\n"
                f"  API Key:   {raw_api_key}\n"
            )
        )
