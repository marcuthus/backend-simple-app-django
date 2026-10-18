from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.common.permissions import IsAdminRole, IsOwnerOrAdmin
from apps.common.pagination import StandardResultsSetPagination
from .models import User
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)


@extend_schema_view(
    list=extend_schema(summary="Listar usuários (Apenas Admin)", tags=["Users"]),
    create=extend_schema(summary="Criar novo usuário (Apenas Admin)", tags=["Users"]),
    retrieve=extend_schema(summary="Obter detalhes de um usuário", tags=["Users"]),
    update=extend_schema(summary="Atualizar usuário", tags=["Users"]),
    partial_update=extend_schema(summary="Atualizar parcialmente usuário", tags=["Users"]),
    destroy=extend_schema(summary="Remover usuário (Apenas Admin)", tags=["Users"]),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para gerenciamento de usuários.
    """

    queryset = User.objects.all().order_by('-created_at')
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        if self.action in ['retrieve', 'regenerate_api_key']:
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            return [IsAdminRole()]
        return [IsOwnerOrAdmin()]

    def perform_destroy(self, instance):
        if str(instance.id) == str(self.request.user.id):
            raise ValidationError({'detail': 'Você não pode excluir a si mesmo.'})
        instance.delete()

    @extend_schema(
        summary="Regenerar Chave de API",
        description="Gera uma nova chave de API para o usuário especificado.",
        responses={200: UserDetailSerializer},
        tags=["Users"],
    )
    @action(detail=True, methods=['post'], url_path='regenerate-api-key')
    def regenerate_api_key(self, request, pk=None):
        user = self.get_object()
        user.regenerate_api_key()
        serializer = UserDetailSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
