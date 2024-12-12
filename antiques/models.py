from django.db import models
from django.shortcuts import get_object_or_404
from category.models import Category

class Antique(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    image = models.ImageField(upload_to="images/antiques/")
    maker = models.CharField(max_length=200, blank=True)  # Pembuat barang (jika diketahui)
    description = models.TextField(max_length=3000, blank=True)  # Deskripsi barang
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Kategori barang
    origin = models.CharField(max_length=200, blank=True)  # Asal usul barang
    material = models.CharField(max_length=200, blank=True)  # Bahan barang antik (misalnya kayu, perak, dll.)
    year_made = models.IntegerField(blank=True, null=True)  # Tahun pembuatan (jika diketahui)
    condition = models.CharField(max_length=100, blank=True)  # Kondisi barang (Baik, Rusak, dll.)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)  # Harga barang
    stocks = models.IntegerField(blank=False)  # Jumlah stok barang
    stocks_available = models.BooleanField(default=True)  # Apakah barang tersedia
    modified_on = models.DateTimeField(auto_now=True)  # Tanggal terakhir dimodifikasi
    created_on = models.DateTimeField(auto_now_add=True)  # Tanggal barang ditambahkan

    def _str_(self):
        return self.title
