from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .models import Subscriber


class SubscribeView(CreateView):
    model = Subscriber
    template_name = "newsletter/subscribe.html"
    fields = ["email"]
    success_url = reverse_lazy("newsletter:success")


class SubscribeSuccessView(TemplateView):
    template_name = "newsletter/success.html"


class UnsubscribeView(TemplateView):
    template_name = "newsletter/unsubscribe.html"
