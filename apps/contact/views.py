from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .models import ContactMessage


class ContactView(CreateView):
    model = ContactMessage
    template_name = "contact/contact.html"
    fields = ["name", "email", "subject", "message"]
    success_url = reverse_lazy("contact:success")


class ContactSuccessView(TemplateView):
    template_name = "contact/success.html"
