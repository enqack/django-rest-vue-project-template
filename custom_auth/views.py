from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
)
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse

from allauth.account.models import EmailAddress

from .mixins import GroupRequiredMixin
from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'custom_auth.add_user'
    template_name = 'custom_auth/create.html'
    model = User
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('custom_auth:account_detail', kwargs={'pk':self.object.pk})


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'custom_auth.view_user'
    template_name = 'custom_auth/detail.html'
    model = User
    form_class = UserChangeForm


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'custom_auth.change_user'
    template_name = 'custom_auth/edit.html'
    model = User
    form_class = UserChangeForm

    def get_success_url(self):
        return reverse('custom_auth:account_detail', kwargs={'pk':self.object.pk})

    # allow user to edit own infomation as well
    def has_permission(self):
        perms = self.get_permission_required()
        if self.request.user.has_perms(perms):
            return True
        obj = self.get_object()
        if self.request.user.id == obj.id:
            return True
        return False


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'custom_auth.view_user'
    template_name = 'custom_auth/list.html'
    model = User
    queryset = User.objects.all().order_by('pk')


class UserProfileView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'custom_auth/profile.html'
    model = User
    form_class = UserChangeForm
    user_check_failure_path = reverse_lazy('custom_auth:account_create')

    def check_user(self, user):
        if user.is_active:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        if EmailAddress.objects.filter(user=obj, verified=True).exists():
            context['is_verified'] = True
        context['object'] = obj
        return context

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    def test_func(self):
        obj = self.get_object()
        return self.request.user.id == obj.id
