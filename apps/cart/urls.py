from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.CartDetailView.as_view(), name="cart_detail"),
    path("ajouter/<int:product_id>/", views.CartAddView.as_view(), name="cart_add"),
]
