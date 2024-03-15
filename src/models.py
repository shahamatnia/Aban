from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def deduct_balance(self, amount):
        """
        Deducts the specified amount from the account balance if sufficient funds are available.
        Raises a ValidationError if funds are insufficient.
        """
        if self.balance < amount:
            raise ValidationError("Insufficient funds in account.")
        self.balance -= amount
        self.save()

    def __str__(self):
        return f"{self.user.username}'s account"


class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def cost(self):
        return self.amount * self.cryptocurrency.price

    def __str__(self):
        return f"{self.user.username}'s order of {self.amount} {self.cryptocurrency.name}"
