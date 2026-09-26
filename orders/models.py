from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Order(models.Model):
    """
    Stores customer order information and order status.
    """

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='orders',
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    def calculate_total(self):
        """
        Recalculate the total amount from all order items.
        Uses the product price if an old order item has no saved price.
        """
        total = sum(
            item.quantity
            * (
                item.price
                if item.price is not None
                else item.product.price
            )
            for item in self.items.all()
        )

        self.total_amount = total

        self.save(
            update_fields=['total_amount'],
        )

        return total

    def __str__(self):
        return f'Order #{self.id} - {self.name}'


class OrderItem(models.Model):
    """
    Stores individual products belonging to an order.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    @property
    def item_total(self):
        """
        Return the total price for this order item.

        If an older order has no saved item price,
        use the current product price as a safe fallback.
        """
        item_price = (
            self.price
            if self.price is not None
            else self.product.price
        )

        return self.quantity * item_price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.order.calculate_total()

    def delete(self, *args, **kwargs):
        order = self.order

        super().delete(*args, **kwargs)

        order.calculate_total()

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

