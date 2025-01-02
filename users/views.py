from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserLoginForm, UserRegistrationForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("tracker:index")
    