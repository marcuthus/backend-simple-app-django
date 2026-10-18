from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.contrib import messages
from .models import User, UserRole


# Custom Admin site branding
admin.site.site_header = "Simple App Admin"
admin.site.site_title = "Painel Administrativo"
admin.site.index_title = "Gerenciamento do Sistema"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Rich Django Admin for User management."""

    list_display = (
        'name',
        'username',
        'email',
        'role_badge',
        'masked_api_key',
        'is_active',
        'is_staff',
        'created_at',
    )
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('name', 'username', 'email')
    ordering = ('-created_at',)

    readonly_fields = ('id', 'api_key_display', 'created_at', 'updated_at')

    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('name', 'username', 'email')
        }),
        ('Credenciais & Papel', {
            'fields': ('role', 'password')
        }),
        ('Chave de API', {
            'description': 'A chave de API é criptografada com AES-256 no banco de dados. Abaixo está o valor decriptografado para uso em integrações.',
            'fields': ('api_key_display',)
        }),
        ('Permissões & Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Metadados', {
            'classes': ('collapse',),
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        ('Criar Novo Usuário', {
            'classes': ('wide',),
            'fields': ('name', 'username', 'email', 'role', 'password1', 'password2', 'is_active'),
        }),
    )

    actions = ['regenerate_api_keys', 'activate_users', 'deactivate_users']

    @admin.display(description="Papel", ordering="role")
    def role_badge(self, obj):
        """Displays a modern styled badge according to user role."""
        if obj.role == UserRole.ADMIN:
            return format_html(
                '<span style="background-color: #ede9fe; color: #6d28d9; padding: 4px 10px; '
                'border-radius: 9999px; font-weight: 600; font-size: 11px; text-transform: uppercase;">'
                'Admin</span>'
            )
        return format_html(
            '<span style="background-color: #e0f2fe; color: #0369a1; padding: 4px 10px; '
            'border-radius: 9999px; font-weight: 600; font-size: 11px; text-transform: uppercase;">'
            'User</span>'
        )

    @admin.display(description="Chave de API")
    def masked_api_key(self, obj):
        """Masked representation of the user API key for the list table."""
        raw = obj.raw_api_key
        if not raw:
            return "-"
        prefix = raw[:8]
        return format_html(
            '<code style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 12px;">'
            '{}••••••••</code>',
            prefix
        )

    @admin.display(description="Chave de API Decriptografada")
    def api_key_display(self, obj):
        """Displays the plain decrypted key in the detail view with copy visual aid."""
        raw = obj.raw_api_key
        if not raw:
            return "Nenhuma chave disponível."
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<input type="text" value="{}" readonly style="width: 420px; font-family: monospace; font-size: 13px; '
            'padding: 6px 10px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px;" />'
            '<span style="color: #64748b; font-size: 12px;">(Pronta para uso com X-API-Key)</span>'
            '</div>',
            raw
        )

    @admin.action(description="Regenerar Chave de API dos usuários selecionados")
    def regenerate_api_keys(self, request, queryset):
        count = 0
        for user in queryset:
            user.regenerate_api_key()
            count += 1
        self.message_user(
            request,
            f"Chave de API regenerada com sucesso para {count} usuário(s).",
            messages.SUCCESS
        )

    @admin.action(description="Ativar usuários selecionados")
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} usuário(s) ativado(s) com sucesso.", messages.SUCCESS)

    @admin.action(description="Desativar usuários selecionados")
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} usuário(s) desativado(s) com sucesso.", messages.WARNING)
