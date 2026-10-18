# 🚀 backend-simple-app-django

Template profissional de backend utilizando **Django**, **Django REST Framework (DRF)**, **Poetry** e **Django Admin**, inspirado na arquitetura e funcionalidades do ecossistema `simple-app`.

---

## 📋 Recursos Principais

- 🐍 **Django 4.2 LTS + Django REST Framework** com tipagem e arquitetura limpa.
- 📦 **Gerenciamento com Poetry**: controle de dependências moderno, determinístico e com `pyproject.toml`.
- 👑 **Django Admin Completo e Customizado**:
  - Badges visuais para papéis (`ADMIN` e `USER`).
  - Chave de API criptografada com visualização decriptografada para administradores.
  - Ações em lote: regenerar chaves de API, ativar/desativar usuários.
  - Filtros por papel, status e data de criação.
- 🔐 **Autenticação Dupla**:
  - **JWT (SimpleJWT)**: tokens de acesso e refresh com claims personalizadas (`role`, `email`, `name`).
  - **Chave de API (X-API-Key)**: autenticação segura via header `X-API-Key` ou `Authorization: Api-Key <key>`, com chaves armazenadas no banco criptografadas com **AES-256-CBC**.
- 👤 **Custom User Model**:
  - Chave primária UUID (`id`).
  - Papéis (`ADMIN`, `USER`).
  - E-mail único e username único.
- 📄 **Paginação Padronizada**: Envelope `{ data: [...], meta: { total, last_page, current_page, per_page, prev, next } }`.
- 📖 **Documentação OpenAPI 3.0 Automática**:
  - **Swagger UI** interativo em `/api/docs/`
  - **Redoc** em `/api/redoc/`
  - **Schema OpenAPI** em `/api/schema/`
- 🌱 **Comando de Seed de Admin Automático**: `python manage.py seed_admin` cria ou atualiza o usuário inicial baseado no `.env`.
- 🐳 **Pronto para VPS e Docker**: `Dockerfile` otimizado e `docker-compose.yml` com **PostgreSQL**.

---

## 🛠️ Pré-requisitos

- **Python**: `>= 3.9`
- **Poetry**: `>= 1.8` (ou `2.x`)

---

## 🚀 Inicialização Rápida

### 1. Clonar e Instalar Dependências

```bash
# Instalar dependências com Poetry
poetry install
```

### 2. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux / Mac
cp .env.example .env
```

Por padrão, a aplicação roda em SQLite local (`dev.db`), dispensando instalação prévia de banco de dados para desenvolvimento.

### 3. Rodar Migrações e Seed do Admin

```bash
# Aplicar as migrações no banco de dados
poetry run python manage.py migrate

# Criar o usuário administrador padrão
poetry run python manage.py seed_admin
```

O comando acima criará o administrador com as credenciais padrão do `.env`:
- **E-mail:** `admin@email.com`
- **Username:** `admin`
- **Senha:** `DVbOwTVuszzkCcZ1cB9RiSIzSHaPdWZo`
- **API Key:** `adm_19b7bb01a40ebf40789f23296ed348aed9ef161caa3634f1f0f8892151c10b4d`

### 4. Executar o Servidor de Desenvolvimento

```bash
poetry run python manage.py runserver
```

A API estará disponível em: [http://localhost:8000](http://localhost:8000)

---

## 🖥️ Django Admin

Acesse [http://localhost:8000/admin/](http://localhost:8000/admin/) com as credenciais do administrador para gerenciar o sistema diretamente pela interface visual:

- Criar novos usuários com permissões específicas.
- Gerar ou regenerar chaves de API automaticamente.
- Visualizar os tokens decriptografados com segurança.
- Executar ações em lote na listagem.

---

## 📚 Documentação da API

- **Swagger UI**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **Redoc**: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)
- **Schema OpenAPI**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

---

## 🔌 Rotas da API

### Autenticação (`/api/auth/`)
| Método | Endpoint | Descrição | Autenticação |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/sign-in/` | Login com e-mail/username e senha | Pública |
| `POST` | `/api/auth/sign-up/` | Autocadastro de usuário comum | Pública |
| `POST` | `/api/auth/refresh-token/` | Renovação de token de acesso JWT | Pública |
| `GET` | `/api/auth/me/` | Perfil do usuário atual | JWT ou API Key |
| `POST` | `/api/auth/change-password/` | Alterar a senha atual | JWT ou API Key |

### Usuários (`/api/users/`)
| Método | Endpoint | Descrição | Permissão |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/users/` | Listar usuários (paginado) | Apenas Admin |
| `POST` | `/api/users/` | Criar usuário | Apenas Admin |
| `GET` | `/api/users/<id>/` | Detalhes do usuário | Dono ou Admin |
| `PATCH` | `/api/users/<id>/` | Atualizar dados do usuário | Dono ou Admin |
| `DELETE` | `/api/users/<id>/` | Remover usuário | Apenas Admin |
| `POST` | `/api/users/<id>/regenerate-api-key/` | Regenerar chave de API | Dono ou Admin |

---

## 🧪 Testes

Para executar a suíte de testes automatizados com `pytest`:

```bash
poetry run pytest
```

---

## 🐳 Executando com Docker (VPS / Produção)

O projeto inclui suporte imediato a Docker com PostgreSQL:

```bash
# Subir banco de dados e aplicação
docker-compose up -d --build
```

Isso irá:
1. Iniciar o container PostgreSQL (`simple_app_db`).
2. Rodar automaticamente `migrate`, `seed_admin` e `collectstatic`.
3. Iniciar a API com Gunicorn na porta `8000`.

---

## 📂 Estrutura do Projeto

```text
backend-simple-app-django/
├── apps/
│   ├── authentication/     # Endpoints e serializers de auth (sign-in, sign-up, me, refresh)
│   ├── common/             # Crypto AES-256, autenticação API Key, permissões e paginação
│   └── users/              # Model customizado, managers, admin completo e views
├── core/
│   ├── settings.py         # Configurações do Django, SimpleJWT, CORS e drf-spectacular
│   ├── urls.py             # Roteamento geral, Swagger e Admin
│   ├── wsgi.py
│   └── asgi.py
├── tests/                  # Testes automatizados com pytest
├── Dockerfile              # Imagem Docker de produção
├── docker-compose.yml      # Orquestração com PostgreSQL
├── manage.py
├── pyproject.toml          # Dependências do Poetry
└── README.md
```

---

## 📄 Licença

Este template é de código aberto sob a licença MIT.
