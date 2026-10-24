from rest_framework import status, views, permissions
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apps.users.serializers import UserSerializer, UserDetailSerializer
from .serializers import (
    SignInSerializer,
    SignUpSerializer,
    RefreshTokenSerializer,
    ChangePasswordSerializer,
)


class SignInView(views.APIView):
    """Autentica o usuário e retorna os tokens JWT de acesso e atualização."""

    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    @extend_schema(
        summary="Login / Autenticação de Usuário",
        request=SignInSerializer,
        responses={200: SignInSerializer},
        tags=["Auth"],
    )
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class SignUpView(views.APIView):
    """Permite o autocadastro de um novo usuário na plataforma."""

    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    @extend_schema(
        summary="Cadastro de Novo Usuário",
        request=SignUpSerializer,
        responses={201: UserSerializer},
        tags=["Auth"],
    )
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class RefreshTokenView(views.APIView):
    """Renova o token JWT de acesso utilizando um token de atualização válido."""

    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    @extend_schema(
        summary="Renovação de Token JWT",
        request=RefreshTokenSerializer,
        responses={200: RefreshTokenSerializer},
        tags=["Auth"],
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MeView(views.APIView):
    """Retorna os dados do usuário atualmente autenticado via JWT ou Chave de API."""

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Perfil do Usuário Autenticado",
        responses={200: UserDetailSerializer},
        tags=["Auth"],
    )
    def get(self, request):
        serializer = UserDetailSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(views.APIView):
    """Altera a senha do usuário atualmente autenticado."""

    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    @extend_schema(
        summary="Alteração de Senha",
        request=ChangePasswordSerializer,
        responses={200: dict},
        tags=["Auth"],
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {'message': 'Senha alterada com sucesso.'},
            status=status.HTTP_200_OK
        )
