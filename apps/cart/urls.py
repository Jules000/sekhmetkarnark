from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.CartDetailView.as_view(), name="cart_detail"),
    path("ajouter/<int:product_id>/", views.CartAddView.as_view(), name="cart_add"),
    path("donnees/", views.CartDataView.as_view(), name="cart_data"),
    path("supprimer/<int:item_id>/", views.CartRemoveView.as_view(), name="cart_remove"),
    path("mettre-a-jour/<int:item_id>/", views.CartUpdateView.as_view(), name="cart_update"),
]
