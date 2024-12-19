from django.db.models import Case, Count, Sum, Value, When
from django.db.models.base import Model as Model
from django.db.models.functions import ExtractMonth
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from tracker.forms import TransactionForm
from tracker.models import Category, Status, Transaction


class AnalyticsListView(generic.ListView):
    model = Transaction
    template_name = "tracker/analytics.html"
    context_object_name = "transations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories_with_total_income = (
            Category.objects.income()
            .annotate(
                total_amount=Sum(
                    "transactions__amount",
                ),
                total_transactions=Count("transactions"),
            )
            .filter(total_amount__gt=0)
            .order_by("-total_amount")
        )

        categories_with_total_expense = (
            Category.objects.expense()
            .annotate(
                total_amount=Sum(
                    "transactions__amount",
                ),
                total_transactions=Count("transactions"),
            )
            .filter(total_amount__gt=0)
            .order_by("-total_amount")
        )

        context["categories_with_total_income"] = categories_with_total_income
        context["categories_with_total_expense"] = categories_with_total_expense
        context["transations_expense_total"] = Transaction.objects.total_expense()

        return context


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = "tracker/category.html"
    context_object_name = "category"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Category, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.status == "expense":
            context["transactions_expense_sum"] = self.object.transactions.total_expense()
        else:
            context["transactions_income_sum"] = self.object.transactions.total_income()

        context["transactions"] = self.object.transactions.all()
        return context


class TransactionCreateView(generic.CreateView):
    template_name = "tracker/create.html"
    form_class = TransactionForm
    success_url = reverse_lazy("tracker:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["status"] = Status.choices
        return context


class TransactionListView(generic.ListView):
    template_name = "tracker/index.html"
    context_object_name = "transactions"

    def get_queryset(self):
        status = self.request.GET.get("status")
        category = self.request.GET.getlist("category")
        month = self.request.GET.get("month")

        if status == "default" or not status:
            transactions = Transaction.objects.all()
        elif status == "income":
            transactions = Transaction.objects.income()
        elif status == "expense":
            transactions = Transaction.objects.expense()

        if category:
            transactions = transactions.filter(category__slug__in=category)

        if month:
            transactions = transactions.filter(created_at__month=month)

        return transactions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        months_dict = {
            1: "Січень",
            2: "Лютий",
            3: "Березень",
            4: "Квітень",
            5: "Травень",
            6: "Червень",
            7: "Липень",
            8: "Серпень",
            9: "Вересень",
            10: "Жовтень",
            11: "Листопад",
            12: "Грудень",
        }

        transaction_month = (
            Transaction.objects.annotate(month_num=ExtractMonth("created_at"))
            .annotate(
                month_name=Case(
                    *[
                        When(month_num=num, then=Value(name))
                        for num, name in months_dict.items()
                    ]
                )
            )
            .values("month_num", "month_name")
            .distinct()
            .order_by("month_num")
        )

        transactions = context["transactions"]
        grouped_transactions = {}

        for transaction in transactions:
            created_at_key = transaction.created_at.date()

            if created_at_key not in grouped_transactions:
                grouped_transactions[created_at_key] = []

            grouped_transactions[created_at_key].append(transaction)

        context["grouped_transactions"] = grouped_transactions
        context["categorys"] = Category.objects.all()
        context["selected_categorys"] = self.request.GET.getlist("category")
        context["month"] = int(self.request.GET.get("month", 0))
        context["months"] = transaction_month
        return context
