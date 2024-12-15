from django.urls import path

from tracker import views


app_name = "tracker"

urlpatterns = [
    path("", views.TransactionListView.as_view(), name="index"),
    path("analytics/", views.AnalyticsListView.as_view(), name="analytics"),
    path("category/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("create/", views.TransactionCreateView.as_view(), name="create")
]
