from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import Group, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from allauth.account.models import EmailAddress

from theme.models import Theme
from .managers import UserManager


def get_sentinel_theme():
    return Theme.objects.get(default=True)


class User(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField(_('email address'), unique=True)
    username    = models.CharField(max_length=32, unique=True, blank=False)
    first_name  = models.CharField(_('first name'), max_length=30, blank=True)
    last_name   = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    theme       = models.ForeignKey(Theme, blank=True, null=True, on_delete=models.SET(get_sentinel_theme))
    timezone    = models.CharField(max_length=64, default=str(timezone.get_default_timezone()))
    is_active   = models.BooleanField(_('active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_staff(self):
        return False

    def is_verified(self):
        if EmailAddress.objects.filter(user=self.id, verified=True).exists():
            return True
        return False

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('custom_auth:account_detail', args=[str(self.id)])
