from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    balance = models.DecimalField(max_digits=30, decimal_places=2, verbose_name="Баланс", default=0.00)

    class Meta:
        db_table = "user"
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self) :
        return f"{self.username} (Баланс: {self.balance})"
