# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.urls import reverse


class Status(models.TextChoices):
    INCOME = "income", "Надходження"
    EXPENSE = "expense", "Витрати"


class CustomQuerySet(models.QuerySet):
    def income(self):
        return self.filter(status=Status.INCOME)

    def expense(self):
        return self.filter(status=Status.EXPENSE)

    def total_income(self):
        return self.income().aggregate(total_sum=models.Sum("amount")).get('total_sum')

    def total_expense(self):
        return self.expense().aggregate(total_sum=models.Sum("amount")).get("total_sum")


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="SLUG_URL")
    status = models.CharField(
        choices=Status.choices,
        default=Status.EXPENSE,
        max_length=8,
        verbose_name="Статус",
    )

    objects = CustomQuerySet().as_manager()

    class Meta:
        db_table = "category"
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def get_absolute_url(self):
        return reverse("tracker:category_detail", args=[self.slug])

    def __str__(self):
        return self.title


class Transaction(models.Model):
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Количество"
    )
    description = models.CharField("Опис", max_length=50)
    created_at = models.DateTimeField(verbose_name="Дата")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transactions",
        verbose_name="Категорія",
    )
    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.EXPENSE,
        verbose_name="Статус",
    )

    objects = CustomQuerySet().as_manager()

    class Meta:
        db_table = "transaction"
        verbose_name = "Транзакція"
        verbose_name_plural = "Транзакції"
        ordering = ["-created_at"]

    def __str__(self):
        return self.description
