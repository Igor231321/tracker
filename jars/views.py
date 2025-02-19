from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
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


class JarCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = "jars/create.html"
    form_class = JarCreateForm
    success_url = reverse_lazy("jars:jars_list")
    success_message = "Банка успішно створена"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class JarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Jar
    template_name = "jars/detail.html"
    context_object_name = "jar"

    def get_object(self, queryset=None):
        return get_object_or_404(Jar, user=self.request.user, slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_deposits"] = self.get_object().operations.filter(user=self.request.user)
        return context


class JarAddMoney(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'jars/jar_operation.html'
    form_class = JarOperationCreateForm
    success_url = reverse_lazy("jars:jars_list")
    success_message = "Банка успішно поповнена"

    def form_valid(self, form):
        jar = Jar.objects.get(slug=self.kwargs['slug'])
        form.instance.jar = jar
        form.instance.user = self.request.user
        
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()

        initial["jar"] = Jar.objects.get(slug=self.kwargs["slug"])
        return initial
