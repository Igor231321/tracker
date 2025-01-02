from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from jars.forms import JarCreateForm, JarOperationCreateForm
from jars.models import Jar


class JarsListView(LoginRequiredMixin, generic.ListView):
    model = Jar
    template_name = "jars/index.html"
    context_object_name = "jars"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class JarCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "jars/create.html"
    form_class = JarCreateForm
    success_url = reverse_lazy("jars:jars_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class JarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Jar
    template_name = "jars/detail.html"
    context_object_name = "jar"

    def get_object(self, queryset=None):
        return get_object_or_404(Jar, user=self.request.user, slug=self.kwargs["slug"])


class JarAddMoney(LoginRequiredMixin, generic.CreateView):
    template_name = 'jars/jar_operation.html'
    form_class = JarOperationCreateForm
    success_url = reverse_lazy("jars:jars_list")

    def form_valid(self, form):
        jar_slug = self.kwargs['slug']
        jar = Jar.objects.get(slug=jar_slug)
        form.instance.jar = jar
        jar.add_money(form.cleaned_data['amount'])

        return super().form_valid(form)
