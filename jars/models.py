from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Jar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    title = models.CharField(max_length=155)
    slug = models.SlugField(unique=True, max_length=155, verbose_name="SLUG_URL")
    balance = models.DecimalField(max_digits=25, decimal_places=2, default=0)
    goal = models.DecimalField(max_digits=25, decimal_places=2)

    class Meta:
        db_table = "jar"
        verbose_name = "Банка"
        verbose_name_plural = "Банки"

    def __str__(self):
        return f"{self.title} (Баланс: {self.balance})"

    def add_money(self, amount):
        self.balance += amount
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
