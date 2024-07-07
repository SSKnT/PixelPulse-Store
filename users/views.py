from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .form import UserRegForm


class RegistrationFormView(FormView):
    form_class = UserRegForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('product-list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super(RegistrationFormView, self).form_valid(form)
