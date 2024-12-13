from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    # Menampilkan kolom utama di daftar admin
    list_display = ('category_name', 'slug', 'category_image', 'category_des')
    # Menentukan kolom yang dapat diklik
    list_display_links = ('category_name', 'slug')
    # Pencarian berdasarkan nama kategori dan deskripsi
    search_fields = ('category_name', 'category_des')
    # Pembuatan slug otomatis berdasarkan nama kategori
    prepopulated_fields = {'slug': ('category_name',)}
    # Filter berdasarkan nama kategori
    list_filter = ('category_name',)
    # Menentukan jumlah item per halaman
    list_per_page = 20

# Mendaftarkan model ke admin site
admin.site.register(Category, CategoryAdmin)
