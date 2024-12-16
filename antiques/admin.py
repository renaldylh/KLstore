from django.utils.html import format_html
from django.contrib import admin
from .models import Antique

class AntiqueAdmin(admin.ModelAdmin):
    # Menampilkan kolom utama di daftar admin
    list_display = ('title', 'price', 'image_tag', 'maker', 'category', 'stocks', 'stocks_available', 'modified_on')
    # Menentukan kolom yang bisa diklik untuk membuka detail
    list_display_links = ('title', 'price', 'category')
    # Kolom hanya-baca
    readonly_fields = ('created_on', 'modified_on', 'image_tag')
    # Urutan tampilan data
    ordering = ('-modified_on',)
    # Pembuatan slug otomatis
    prepopulated_fields = {'slug': ('title',)}
    # Kolom yang dapat difilter
    list_filter = ('category', 'stocks_available', 'condition', 'year_made')
    # Pencarian berdasarkan beberapa kolom
    search_fields = ('title', 'maker', 'category__name', 'origin', 'material', 'condition')
    # Jumlah item per halaman
    list_per_page = 20

    # Pengelompokan bidang di formulir admin
    fieldsets = (
        ("Informasi Utama", {
            'fields': ('title', 'slug', 'category', 'price', 'stocks', 'stocks_available', 'image_tag', 'image')
        }),
        ("Detail Barang", {
            'fields': ('maker', 'description', 'origin', 'material', 'year_made', 'condition')
        }),
        ("Tanggal", {
            'fields': ('created_on', 'modified_on')
        }),
    )

    # Menambahkan tampilan gambar di daftar admin
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image'

    # Aksi cepat untuk admin
    actions = ['mark_as_available', 'mark_as_unavailable', 'clear_stocks']

    def mark_as_available(self, request, queryset):
        updated = queryset.update(stocks_available=True)
        self.message_user(request, f"{updated} item(s) marked as available.")
    mark_as_available.short_description = "Mark selected items as available"

    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(stocks_available=False)
        self.message_user(request, f"{updated} item(s) marked as unavailable.")
    mark_as_unavailable.short_description = "Mark selected items as unavailable"

    def clear_stocks(self, request, queryset):
        updated = queryset.update(stocks=0)
        self.message_user(request, f"{updated} item(s) stocks cleared.")
    clear_stocks.short_description = "Clear stocks for selected items"

# Mendaftarkan model dan konfigurasi ke admin site
admin.site.register(Antique, AntiqueAdmin)
