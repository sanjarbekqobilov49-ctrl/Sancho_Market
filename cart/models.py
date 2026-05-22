from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    is_active = models.BooleanField(default=True)
    fio = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    telegram = models.CharField(max_length=255, blank=True, help_text='Telegram username yoki raqam')
    created_at = models.DateTimeField(auto_now_add=True)

    def order_number(self):
        return Cart.objects.filter(is_active=False, user=self.user).count()

    def __str__(self):
        return f"Cart {self.id} - {self.user.username} ({'active' if self.is_active else 'inactive'})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
