# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="SLUG_URL")

    class Meta:
        db_table = "category"
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def get_absolute_url(self):
        return reverse("tracker:category_detail", args=[self.slug])

    def __str__(self):
        return self.title


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = "income", "Доход"
        EXPENSE = "expense", "Расход"
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")
    description = models.CharField("Опис", max_length=50)
    date =  models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="transactions", verbose_name="Категорія")
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices, default=TransactionType.INCOME)

    class Meta:
        db_table = 'transaction'
        verbose_name = "Витрати"
        verbose_name_plural = "Витрати"
    
    def __str__(self):
        return self.description
