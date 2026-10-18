from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from apps.users.models import User, UserRole
from apps.users.serializers import UserSerializer


class SignInSerializer(serializers.Serializer):
    """Serializer for user authentication via email or username + password."""

    login = serializers.CharField(
        required=False,
        help_text="E-mail ou nome de usuário",
        write_only=True
    )
    email = serializers.EmailField(required=False, write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        login_input = attrs.get('login') or attrs.get('email')
        password = attrs.get('password')

        if not login_input:
            raise serializers.ValidationError('É necessário informar o e-mail ou nome de usuário.')

        login_input = login_input.strip()

        # Find user by email or username
        user = None
        if '@' in login_input:
            user = User.objects.filter(email__iexact=login_input).first()
        else:
            user = User.objects.filter(username__iexact=login_input).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError('Credenciais inválidas. Verifique seu login e senha.')

        if not user.is_active:
            raise serializers.ValidationError('Esta conta de usuário está desativada.')

        # Generate JWT tokens with custom claims
        refresh = RefreshToken.for_user(user)
        refresh['name'] = user.name
        refresh['username'] = user.username
        refresh['email'] = user.email
        refresh['role'] = user.role

        return {
            'user': UserSerializer(user).data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            # Also provide standard camelCase keys for frontend simple-app
            'accessToken': str(refresh.access_token),
            'refreshToken': str(refresh),
        }


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for self-registration of a new standard user."""

    password = serializers.CharField(write_only=True, min_length=6, required=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password']

    def validate_username(self, value):
        value = value.strip().lower()
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('Este nome de usuário já está em uso.')
        return value

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Este e-mail já está cadastrado.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data['name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=UserRole.USER,
        )
        return user


class RefreshTokenSerializer(serializers.Serializer):
    """Serializer to refresh access tokens."""

    refresh_token = serializers.CharField(required=False, write_only=True)
    refreshToken = serializers.CharField(required=False, write_only=True)
    refresh = serializers.CharField(required=False, write_only=True)

    def validate(self, attrs):
        raw_token = attrs.get('refresh_token') or attrs.get('refreshToken') or attrs.get('refresh')
        if not raw_token:
            raise serializers.ValidationError('O token de atualização (refresh_token) é obrigatório.')

        try:
            token = RefreshToken(raw_token)
            user_id = token.payload.get('user_id')
            user = User.objects.filter(id=user_id, is_active=True).first()

            if not user:
                raise serializers.ValidationError('Usuário associado ao token não encontrado ou inativo.')

            new_access_token = str(token.access_token)
            new_refresh_token = str(token)

            return {
                'access_token': new_access_token,
                'refresh_token': new_refresh_token,
                'accessToken': new_access_token,
                'refreshToken': new_refresh_token,
            }
        except (TokenError, InvalidToken) as exc:
            raise serializers.ValidationError(f'Token de atualização inválido ou expirado: {str(exc)}')


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing current user's password."""

    current_password = serializers.CharField(required=False, write_only=True)
    currentPassword = serializers.CharField(required=False, write_only=True)
    new_password = serializers.CharField(required=False, min_length=6, write_only=True)
    newPassword = serializers.CharField(required=False, min_length=6, write_only=True)

    def validate(self, attrs):
        current_pwd = attrs.get('current_password') or attrs.get('currentPassword')
        new_pwd = attrs.get('new_password') or attrs.get('newPassword')

        if not current_pwd:
            raise serializers.ValidationError('A senha atual é obrigatória.')
        if not new_pwd:
            raise serializers.ValidationError('A nova senha é obrigatória.')
        if current_pwd == new_pwd:
            raise serializers.ValidationError('A nova senha não pode ser idêntica à senha atual.')

        user = self.context['request'].user
        if not user.check_password(current_pwd):
            raise serializers.ValidationError('A senha atual informada está incorreta.')

        return {'new_password': new_pwd}
