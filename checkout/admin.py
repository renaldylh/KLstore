from django.contrib import admin
from .models import order, order_list, order_note_admin, invoice

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'client', 'order_status', 'date_created', 'date_updated')
    list_display_links = ('order_id', 'client')
    search_fields = ('order_id', 'client__email')
    list_filter = ('order_status', 'date_created', 'date_updated')
    list_per_page = 20

class OrderListAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_item', 'order_quantity', 'order_price')
    list_display_links = ('order_id', 'order_item')
    search_fields = ('order_id__order_id', 'order_item__title')
    list_filter = ('order_quantity',)
    list_per_page = 20

class OrderNoteAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'message')
    list_display_links = ('order_id',)
    search_fields = ('order_id__order_id', 'message')
    list_per_page = 20

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'order_id', 'invoice_status', 'total_price', 'transaction_method', 'transaction_id', 'date_created')
    list_display_links = ('invoice_id', 'order_id')
    search_fields = ('invoice_id', 'order_id__order_id', 'transaction_id')
    list_filter = ('invoice_status', 'transaction_method', 'date_created', 'date_updated')
    list_per_page = 20
    readonly_fields = ('date_created', 'date_updated')

admin.site.register(order, OrderAdmin)
admin.site.register(order_list, OrderListAdmin)
admin.site.register(order_note_admin, OrderNoteAdmin)
admin.site.register(invoice, InvoiceAdmin)
