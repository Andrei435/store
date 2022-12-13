from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect

from common.views import TitleMixin
from .models import User
from products.models import Basket
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm
from .models import EmailVerificatiom


class UserLoginView(TitleMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Авторизация'


class UserRegisterView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    title = "Регистрация"
    success_message = 'Вы успешно зарегистрировались'


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.object, )
        return context


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - Подтверждение электронной почты'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerificatiom.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))