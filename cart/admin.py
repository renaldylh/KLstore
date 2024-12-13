from django.contrib import admin
from .models import Cart, CartItems

class CartAdmin(admin.ModelAdmin):
    # Menampilkan kolom utama di daftar admin
    list_display = ('cart_session', 'add_date')
    # Menentukan kolom yang dapat diklik
    list_display_links = ('cart_session',)
    # Menentukan kolom hanya-baca
    readonly_fields = ('add_date',)
    # Pencarian berdasarkan sesi keranjang
    search_fields = ('cart_session',)
    # Filter berdasarkan tanggal
    list_filter = ('add_date',)
    # Urutan data berdasarkan tanggal tambah terbaru
    ordering = ('-add_date',)
    # Jumlah item per halaman
    list_per_page = 20

class CartItemsAdmin(admin.ModelAdmin):
    # Menampilkan kolom utama di daftar admin
    list_display = ('cart', 'antique', 'quantity', 'is_active')
    # Menentukan kolom yang dapat diklik
    list_display_links = ('cart', 'antique')
    # Pencarian berdasarkan sesi keranjang atau barang antik
    search_fields = ('cart__cart_session', 'antique__title')
    # Filter berdasarkan status aktif atau tidak
    list_filter = ('is_active', 'cart')
    # Menentukan jumlah item per halaman
    list_per_page = 20

# Mendaftarkan model ke admin site
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItems, CartItemsAdmin)
