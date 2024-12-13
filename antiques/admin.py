from django.contrib import admin
from .models import Antique

class AntiqueAdmin(admin.ModelAdmin):
    # Menampilkan kolom utama di daftar admin
    list_display = ('title', 'price', 'maker', 'category', 'stocks', 'stocks_available', 'modified_on')
    # Menentukan kolom yang bisa diklik untuk membuka detail
    list_display_links = ('title', 'price', 'category')
    # Kolom hanya-baca
    readonly_fields = ('created_on', 'modified_on')
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
            'fields': ('title', 'slug', 'category', 'price', 'stocks', 'stocks_available')
        }),
        ("Detail Barang", {
            'fields': ('maker', 'description', 'origin', 'material', 'year_made', 'condition')
        }),
        ("Tanggal", {
            'fields': ('created_on', 'modified_on')
        }),
    )

    # Menampilkan relasi dalam tampilan inline (jika ada relasi)
    class RelatedModelInline(admin.TabularInline):
        model = None  # Ganti dengan model terkait jika ada
        extra = 1

    # Aksi cepat untuk admin
    actions = ['mark_as_available', 'mark_as_unavailable', 'clear_stocks']

    # Aksi cepat untuk menandai barang tersedia
    def mark_as_available(self, request, queryset):
        updated = queryset.update(stocks_available=True)
        self.message_user(request, f"{updated} item(s) marked as available.")
    mark_as_available.short_description = "Mark selected items as available"

    # Aksi cepat untuk menandai barang tidak tersedia
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(stocks_available=False)
        self.message_user(request, f"{updated} item(s) marked as unavailable.")
    mark_as_unavailable.short_description = "Mark selected items as unavailable"

    # Aksi cepat untuk mengosongkan stok
    def clear_stocks(self, request, queryset):
        updated = queryset.update(stocks=0)
        self.message_user(request, f"{updated} item(s) stocks cleared.")
    clear_stocks.short_description = "Clear stocks for selected items"

# Mendaftarkan model dan konfigurasi ke admin site
admin.site.register(Antique, AntiqueAdmin)

