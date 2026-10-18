from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model
from .crypto import CryptoService


class ApiKeyAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication using encrypted API Key.
    Accepts:
      - Header 'X-API-Key: <key>'
      - Header 'Authorization: Api-Key <key>'
    """

    keyword = 'Api-Key'

    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            auth_header = request.headers.get('Authorization', '').split()
            if len(auth_header) == 2 and auth_header[0] == self.keyword:
                api_key = auth_header[1]

        if not api_key:
            return None

        encrypted_key = CryptoService.encrypt(api_key)
        User = get_user_model()

        try:
            user = User.objects.get(api_key=encrypted_key, is_active=True)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Chave de API inválida ou usuário inativo.')

        return (user, None)
