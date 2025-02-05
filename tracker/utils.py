from django.db.models import Q
from django.db.models import Count, Sum
from django.utils import timezone

from tracker.models import Category


def get_categories(status, user, month, year):
    # Проверка статуса и выбор категории
    if status == "income":
        categories = Category.objects.income()
    else:
        categories = Category.objects.expense()

    # Фильтрация по пользователю, месяцу и году
    categories = (
        categories.filter(
            transactions__user=user,
            transactions__created_at__month=month,
            transactions__created_at__year=year,
        )
        .annotate(
            total_amount=Sum("transactions__amount"),  # Сумма транзакций
            total_transactions=Count("transactions"),  # Количество транзакций
        )
        .filter(total_amount__gt=0)  # Исключение категорий с нулевой суммой
        .order_by("-total_amount")  # Сортировка по убыванию суммы
    )
    return categories



def get_month_name(month):
     months_list = [
            "Січень",
            "Лютий",
            "Березень",
            "Квітень",
            "Травень",
            "Червень",
            "Липень",
            "Серпень",
            "Вересень",
            "Жовтень",
            "Листопад",
            "Грудень",
        ]
     
     return months_list[int(month) - 1]
