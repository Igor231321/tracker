from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from users.models import User


class Jar(models.Model):
    class Status(models.TextChoices):
        EMPTY = "E", "Пуста"
        HAS_MONEY = "HM", "Є гроші"
        FULL = "F", "Заповнена"

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    title = models.CharField(max_length=155)
    slug = models.SlugField(unique=True, max_length=155, verbose_name="SLUG_URL")
    status = models.CharField(choices=Status.choices, default=Status.EMPTY, max_length=2, verbose_name="Статус")
    balance = models.DecimalField(max_digits=25, decimal_places=2, default=0)
    goal = models.DecimalField(max_digits=25, decimal_places=2)

    class Meta:
        db_table = "jar"
        verbose_name = "Банка"
        verbose_name_plural = "Банки"

    def __str__(self):
        return f"{self.title} (Баланс: {self.balance}, Статус: {self.get_status_display()})"    

    def add_money(self, amount):
        self.balance += amount
        if self.balance > 0 and self.status != Jar.Status.HAS_MONEY:
            self.status = Jar.Status.HAS_MONEY
        
        self.save()

    def progress(self):
        if self.balance == 0:
            return 0
        return int((self.balance / self.goal) * 100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)


class JarOperation(models.Model):
    jar = models.ForeignKey(Jar, on_delete=models.CASCADE, verbose_name="Банка")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    amount = models.DecimalField(
        max_digits=50, decimal_places=2, verbose_name="Кількість грошей"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        db_table = "jar_operations"
        verbose_name = "Операція з банкою"
        verbose_name_plural = "Операції з банкою"

    def __str__(self) -> str:
        return f"{self.jar.title} (Додано: {self.amount})"

    def save(self, *args, **kwargs):
        self.jar.add_money(self.amount)
        super().save(*args, **kwargs)
