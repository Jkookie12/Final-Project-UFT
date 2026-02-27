from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SignUpForm

class UserRegister(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Registered successfully! You can now log in.")
        return response