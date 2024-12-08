from django.urls import path

from tracker import views


app_name = "tracker"

urlpatterns = [
    path("", views.TransactionListView.as_view()),
    path("category/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail")
]
