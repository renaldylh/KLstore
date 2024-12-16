from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone', 'is_active', 'last_active', 'registered_on')
    readonly_fields = ('last_active', 'registered_on')
    list_display_links = ('email', 'username', 'phone', 'is_active')
    ordering = ('-last_active',)

    def get_readonly_fields(self, request, obj=None):
        # Jika pengguna adalah staff, semua field menjadi readonly
        if request.user.is_staff and not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def has_add_permission(self, request):
        # Staff tidak diizinkan menambahkan data baru
        if request.user.is_staff and not request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Staff tidak diizinkan menghapus data
        if request.user.is_staff and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def get_queryset(self, request):
        # Staff hanya bisa melihat data tertentu jika diperlukan
        queryset = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            # Contoh: Batasi hanya data aktif
            return queryset.filter(is_active=True)
        return queryset

# Register model dan admin configuration
admin.site.register(Account, AccountAdmin)
