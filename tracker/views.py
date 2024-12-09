from django.db.models import Q, Sum, Count
from django.urls import reverse_lazy
from django.views import generic

from tracker.forms import TransactionForm
from tracker.models import Category, Transaction


class TransactionListView(generic.ListView):
    model = Transaction
    template_name = "tracker/index.html"
    context_object_name = "transations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories_with_total_income = Category.objects.annotate(
            total_amount=Sum(
                'transactions__amount',
                filter=Q(transactions__operation=Transaction.Operation.INCOME)  # Условие фильтрации
            ),
            total_transactions=Count("transactions")
        ).filter(total_amount__gt=0).order_by("-total_amount")

        categories_with_total_expense = Category.objects.annotate(
            total_amount=Sum(
                'transactions__amount',
                filter=Q(transactions__operation=Transaction.Operation.EXPENSE)  # Условие фильтрации
            ),
            total_transactions=Count("transactions")
        ).filter(total_amount__gt=0).order_by("-total_amount")

        context['categories_with_total_income'] = categories_with_total_income
        context['categories_with_total_expense'] = categories_with_total_expense

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
