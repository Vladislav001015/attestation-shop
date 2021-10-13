from django.contrib import messages

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import RegistrationForm, AccountForm

from .models import CustomUser


class RegisterView(SuccessMessageMixin, CreateView):
    model = CustomUser
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')
    success_message = 'Successfully registered'


class SignInView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy()
    success_message = 'Successfully login'


def profile(request):
    return render(request, 'profile.html')


class AccountUpdateView(UpdateView):
    model = CustomUser
    template_name = 'update_account.html'
    form_class = AccountForm
    success_url = reverse_lazy('profile')


@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    user = CustomUser.objects.get(id=id)
    logout(request)
    user.delete()
    messages.add_message(request, messages.SUCCESS, 'Successfully deleted')
    return redirect("index")
