from django.urls import path
from . import views

app_name = "newsletter"

urlpatterns = [
    path("inscription/", views.SubscribeView.as_view(), name="subscribe"),
    path("succes/", views.SubscribeSuccessView.as_view(), name="success"),
    path("desabonnement/", views.UnsubscribeView.as_view(), name="unsubscribe"),
]
