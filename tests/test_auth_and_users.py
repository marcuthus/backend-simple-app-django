import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.users.models import User, UserRole
from apps.common.crypto import CryptoService


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email="admin@test.com",
        username="admin_test",
        name="Admin Test",
        password="TestPassword123!",
    )


@pytest.fixture
def standard_user(db):
    return User.objects.create_user(
        email="user@test.com",
        username="user_test",
        name="User Test",
        password="TestPassword123!",
        role=UserRole.USER,
    )


@pytest.mark.django_db
def test_sign_in_success(client, standard_user):
    url = reverse('auth-sign-in')
    response = client.post(url, {
        'email': 'user@test.com',
        'password': 'TestPassword123!'
    }, format='json')

    assert response.status_code == 200
    data = response.json()
    assert 'accessToken' in data or 'access_token' in data
    assert 'refreshToken' in data or 'refresh_token' in data
    assert data['user']['email'] == 'user@test.com'


@pytest.mark.django_db
def test_sign_up_success(client):
    url = reverse('auth-sign-up')
    response = client.post(url, {
        'name': 'Novo Usuário',
        'username': 'novousuario',
        'email': 'novo@test.com',
        'password': 'SecurePassword123!'
    }, format='json')

    assert response.status_code == 201
    data = response.json()
    assert data['email'] == 'novo@test.com'
    assert data['username'] == 'novousuario'
    assert User.objects.filter(email='novo@test.com').exists()


@pytest.mark.django_db
def test_api_key_authentication(client, standard_user):
    url = reverse('auth-me')
    raw_key = standard_user.raw_api_key

    # Without API key -> 401
    res_unauth = client.get(url)
    assert res_unauth.status_code in [401, 403]

    # With X-API-Key header -> 200
    res_auth = client.get(url, HTTP_X_API_KEY=raw_key)
    assert res_auth.status_code == 200
    assert res_auth.json()['email'] == standard_user.email


@pytest.mark.django_db
def test_users_list_admin_only(client, admin_user, standard_user):
    url = reverse('user-list')

    # Standard user trying to list all users -> Forbidden
    client.force_authenticate(user=standard_user)
    res_forbidden = client.get(url)
    assert res_forbidden.status_code == 403

    # Admin user listing all users -> Success with pagination
    client.force_authenticate(user=admin_user)
    res_admin = client.get(url)
    assert res_admin.status_code == 200
    body = res_admin.json()
    assert 'data' in body
    assert 'meta' in body
    assert body['meta']['total'] >= 2


@pytest.mark.django_db
def test_swagger_schema(client):
    url = reverse('schema')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_root_redirect_to_docs(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.url == '/api/docs/'
