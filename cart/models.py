from django.db import models
from antiques.models import Antique

class Cart(models.Model):
    cart_session = models.CharField(max_length=250)
    add_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.cart_session


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    antique = models.ForeignKey(Antique, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField()


