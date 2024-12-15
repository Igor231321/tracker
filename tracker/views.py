from django.db.models import Q, Case, Sum, Count, Value, When
from django.db.models.functions import ExtractMonth
from django.urls import reverse_lazy
from django.views import generic

from tracker.forms import TransactionForm
from tracker.models import Category, Transaction


class AnalyticsListView(generic.ListView):
    model = Transaction
    template_name = "tracker/analytics.html"
    context_object_name = "transations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories_with_total_income = (
            Category.objects.annotate(
                total_amount=Sum(
                    "transactions__amount",
                    filter=Q(
                        transactions__operation=Transaction.Operation.INCOME
                    ),  # Условие фильтрации
                ),
                total_transactions=Count("transactions"),
            )
            .filter(total_amount__gt=0)
            .order_by("-total_amount")
        )

        categories_with_total_expense = (
            Category.objects.annotate(
                total_amount=Sum(
                    "transactions__amount",
                    filter=Q(
                        transactions__operation=Transaction.Operation.EXPENSE
                    ),  # Условие фильтрации
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = self.object.transactions.all()

        if self.object.title in ["Работа", "Стипендія"]:
            context["transactions_income"] = self.object.transactions.total_income()
        else:
            context["transactions_expense"] = self.object.transactions.total_expense()

        return context


class TransactionCreateView(generic.CreateView):
    template_name = "tracker/create.html"
    form_class = TransactionForm
    success_url = reverse_lazy("tracker:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["operations"] = Transaction.Operation.choices
        return context


class TransactionListView(generic.ListView):
    template_name = "tracker/index.html"
    context_object_name = "transactions"

    def get_queryset(self):
        operation = self.request.GET.get("operation")
        category = self.request.GET.getlist("category")
        month = self.request.GET.get("month")

        if operation == "default" or not operation:
            transactions = Transaction.objects.all()
        elif operation == "income":
            transactions = Transaction.objects.income()
        elif operation == "expense":
            transactions = Transaction.objects.expense()

        if category:
            transactions = transactions.filter(category__slug__in=category)

        if month:
            transactions = transactions.filter(date__month=month)
            
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
            Transaction.objects.annotate(month_num=ExtractMonth("date"))
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
            date_key = transaction.date.date()

            if date_key not in grouped_transactions:
                grouped_transactions[date_key] = []

            grouped_transactions[date_key].append(transaction)

        context["grouped_transactions"] = grouped_transactions
        context["categorys"] = Category.objects.all()
        context["selected_categorys"] = self.request.GET.getlist("category")
        context["month"] = int(self.request.GET.get("month", 0))
        context["months"] = transaction_month
        return context
