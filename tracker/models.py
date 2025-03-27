# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.urls import reverse

from users.models import User


class CustomQuerySet(models.QuerySet):
    def income(self):
        return self.filter(status=Status.INCOME)

    def expense(self):
        return self.filter(status=Status.EXPENSE)


class TransactionQuerySet(models.QuerySet):
    def for_user(self, user, month=None, year=None, status=None):
        queryset = self.filter(user=user)

        if month:
            queryset = queryset.filter(created_at__month=month, created_at__year=year)
        
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def income(self):
        return self.filter(status=Status.INCOME)

    def expense(self):
        return self.filter(status=Status.EXPENSE)

    def total_sum(self):
        return self.aggregate(total_sum=models.Sum("amount")).get("total_sum") or 0


class Status(models.TextChoices):
    INCOME = "income", "Надходження"
    EXPENSE = "expense", "Витрати"


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
        return f"{self.title} (Тип: {self.get_status_display().lower()})"


class Transaction(models.Model):
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма"
    )
    description = models.CharField("Опис", max_length=50)
    created_at = models.DateField(verbose_name="Дата")
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
        verbose_name="Тип (доход/витрата)",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Баланс на данний момент")

    objects = TransactionQuerySet().as_manager()

    class Meta:
        db_table = "transaction"
        verbose_name = "Транзакція"
        verbose_name_plural = "Транзакції"
        ordering = ["-created_at"]

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.status = self.category.status

        if self.pk:
            old_transaction = Transaction.objects.get(pk=self.pk)
            
            if old_transaction.status == Status.EXPENSE:
                self.user.balance += old_transaction.amount
            else:
                self.user.balance -= old_transaction.amount

        # Применяем новую транзакцию
        if self.status == Status.EXPENSE:
            self.user.balance -= self.amount

        elif self.status == Status.INCOME:
            self.user.balance += self.amount

        self.current_balance = self.user.balance
        self.user.save()
        super().save(*args, **kwargs)
