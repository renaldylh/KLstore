from django.contrib import admin
from .models import order, order_list, order_note_admin, invoice

class OrderAdmin(admin.ModelAdmin):
    # Menampilkan kolom utama di daftar admin
    list_display = ('order_id', 'client', 'order_status', 'date_created', 'date_updated')
    # Menentukan kolom yang dapat diklik
    list_display_links = ('order_id', 'client')
    # Pencarian berdasarkan ID pesanan dan klien
    search_fields = ('order_id', 'client__email')
    # Filter berdasarkan status pesanan dan tanggal
    list_filter = ('order_status', 'date_created', 'date_updated')
    # Menentukan jumlah item per halaman
    list_per_page = 20

class OrderListAdmin(admin.ModelAdmin):
    # Menampilkan kolom utama di daftar admin
    list_display = ('order_id', 'order_item', 'order_quantity', 'order_price')
    # Menentukan kolom yang dapat diklik
    list_display_links = ('order_id', 'order_item')
    # Pencarian berdasarkan ID pesanan atau barang antik
    search_fields = ('order_id__order_id', 'order_item__title')
    # Filter berdasarkan jumlah pesanan
    list_filter = ('order_quantity',)
    # Menentukan jumlah item per halaman
    list_per_page = 20

class OrderNoteAdmin(admin.ModelAdmin):
    # Menampilkan kolom utama di daftar admin
    list_display = ('order_id', 'message')
    # Menentukan kolom yang dapat diklik
    list_display_links = ('order_id',)
    # Pencarian berdasarkan ID pesanan dan pesan
    search_fields = ('order_id__order_id', 'message')
    # Menentukan jumlah item per halaman
    list_per_page = 20

class InvoiceAdmin(admin.ModelAdmin):
    # Menampilkan kolom utama di daftar admin
    list_display = ('invoice_id', 'order_id', 'invoice_status', 'total_price', 'transaction_method', 'transaction_id', 'date_created')
    # Menentukan kolom yang dapat diklik
    list_display_links = ('invoice_id', 'order_id')
    # Pencarian berdasarkan ID faktur, ID pesanan, dan metode transaksi
    search_fields = ('invoice_id', 'order_id__order_id', 'transaction_id')
    # Filter berdasarkan status faktur, metode transaksi, dan tanggal
    list_filter = ('invoice_status', 'transaction_method', 'date_created', 'date_updated')
    # Menentukan jumlah item per halaman
    list_per_page = 20
    # Menjadikan beberapa kolom hanya-baca
    readonly_fields = ('date_created', 'date_updated')

# Mendaftarkan model ke admin site
admin.site.register(order, OrderAdmin)
admin.site.register(order_list, OrderListAdmin)
admin.site.register(order_note_admin, OrderNoteAdmin)
admin.site.register(invoice, InvoiceAdmin)
