from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from tracker.forms import TransactionForm
from tracker.models import Category, Status, Transaction
from tracker.utils import get_categories, get_month_name


class AnalyticsListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "tracker/analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        month = self.request.GET.get("month", timezone.now().strftime("%m"))
        year = self.request.GET.get("year", timezone.now().strftime("%Y"))

        context["month"] = month
        context["year"] = year
        context["month_name"] = get_month_name(month)

        context["categories_income"] = get_categories(
            user=user, status="income", month=month, year=year
        )
        context["categories_expense"] = get_categories(
            user=user, status="expense", month=month, year=year
        )
        context["total_expenses"] = Transaction.objects.for_user(
            user=user, status=Status.EXPENSE, month=month, year=year
        ).total_sum()
        context["total_income"] = Transaction.objects.for_user(
            user=user, status=Status.INCOME, month=month, year=year
        ).total_sum()

        context["date_transactions"] = Transaction.objects.dates("created_at", "month")
        context["total_balance"] = context["total_income"] - context["total_expenses"]
        return context


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Category
    template_name = "tracker/category.html"
    context_object_name = "category"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Category, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        month = self.request.GET.get("month", timezone.now().strftime("%m"))
        year = self.request.GET.get("year", timezone.now().strftime("%Y"))

        transactions = self.object.transactions.for_user(
            user=user, month=month, year=year
        )

        if self.object.status == Status.EXPENSE:
            context["category_expense"] = True
        else:
            context["category_income"] = True

        context["transactions"] = transactions
        context["transactions_total_sum"] = transactions.total_sum()

        return context


class TransactionListView(LoginRequiredMixin, generic.ListView):
    template_name = "tracker/arhiv.html"
    context_object_name = "transactions"

    def get_queryset(self):
        status = self.request.GET.get("status")
        category = self.request.GET.getlist("category")
        date = self.request.GET.get("date")

        if status == "default" or not status:
            transactions = Transaction.objects.for_user(user=self.request.user)
        elif status == "income":
            transactions = Transaction.objects.for_user(
                user=self.request.user, status=Status.INCOME
            )
        elif status == "expense":
            transactions = Transaction.objects.for_user(
                user=self.request.user, status=Status.EXPENSE
            )

        if category:
            transactions = transactions.filter(category__slug__in=category)

        if date:
            try:
                month, year = map(int, date.split())
                transactions = transactions.filter(
                    created_at__month=month, created_at__year=year
                )
            except (ValueError, TypeError):
                pass

        return transactions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        transactions = context["transactions"].annotate(date=TruncDate("created_at"))

        # Группировка транзакций по дате
        grouped_transactions = defaultdict(list)
        for transaction in transactions:
            grouped_transactions[transaction.date].append(transaction)

        context["grouped_transactions"] = dict(grouped_transactions)

        context["statuses"] = [
            ("default", "Усі"),
            ("income", "Прибуток"),
            ("expense", "Витрати"),
        ]
        context["categorys"] = Category.objects.all()
        context["date_transactions"] = Transaction.objects.dates("created_at", "month")

        context["selected_categorys"] = self.request.GET.getlist("category")
        if self.request.GET.get("date"):
            context["date"] = self.request.GET.get("date").split()

        context["selected_status"] = self.request.GET.get("status", "default")
        context["selected_categories"] = self.request.GET.getlist("category")
        context["selected_date"] = self.request.GET.get("date")
        return context


class TransactionCreateView(
    LoginRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    template_name = "tracker/create.html"
    form_class = TransactionForm
    success_url = reverse_lazy("tracker:create")
    success_message = "Транзакція успішно добавлена"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories_income"] = Category.objects.income()
        context["categories_expense"] = Category.objects.expense()
        context["status"] = Status.choices
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class TransactionDeailView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = "tracker/create.html"
    form_class = TransactionForm
    success_url = reverse_lazy("tracker:create")
    success_message = "Транзакція успішно добавлена"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["status"] = Status.choices
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


def delete_transaction(request, id):
    if request.method == "POST":
        transaction = Transaction.objects.get(id=id)

        if transaction.status == Status.EXPENSE:
            request.user.balance += transaction.amount
        else:
            request.user.balance -= transaction.amount

        request.user.save()
        transaction.delete()

        messages.success(request, "Транзакція успішно видалена")
    return redirect("tracker:arhiv")


