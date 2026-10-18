from rest_framework import serializers
from .models import User, UserRole


class UserSerializer(serializers.ModelSerializer):
    """Public representation of a user without sensitive data."""

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'username',
            'email',
            'role',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user representation including decrypted API key (accessible by owner or admin)."""

    api_key = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'username',
            'email',
            'role',
            'api_key',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'api_key', 'created_at', 'updated_at']

    def get_api_key(self, obj) -> str:
        # Only owner or admin can view raw API key
        request = self.context.get('request')
        if request and (
            request.user.role == UserRole.ADMIN
            or request.user.is_staff
            or str(request.user.id) == str(obj.id)
        ):
            return obj.raw_api_key
        return '••••••••'


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user."""

    password = serializers.CharField(write_only=True, min_length=6, required=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'role']

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
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'role']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'name': {'required': False},
            'role': {'required': False},
        }

    def validate_role(self, value):
        # Only admin can change roles
        request = self.context.get('request')
        if request and request.user.role != UserRole.ADMIN and not request.user.is_staff:
            raise serializers.ValidationError('Você não tem permissão para alterar seu cargo.')
        return value

    def validate_username(self, value):
        value = value.strip().lower()
        instance = getattr(self, 'instance', None)
        if User.objects.filter(username__iexact=value).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError('Este nome de usuário já está em uso.')
        return value

    def validate_email(self, value):
        value = value.strip().lower()
        instance = getattr(self, 'instance', None)
        if User.objects.filter(email__iexact=value).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError('Este e-mail já está cadastrado.')
        return value
