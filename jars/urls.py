from django.urls import path

from jars import views

app_name = "jars"

urlpatterns = [
    path("", views.JarsListView.as_view(), name="jars_list"),
    path("create/", views.JarCreateView.as_view(), name="create"),
    path("<slug:slug>/detail/", views.JarDetailView.as_view(), name="detail"),
    path("<slug:slug>/add_money/", views.JarAddMoney.as_view(), name="add_money")
]
