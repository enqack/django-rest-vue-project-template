from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

import pytz

from allauth.account.forms import PasswordVerificationMixin
from passwords.fields import PasswordField

from theme.models import Theme
from .models import User


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(validators=[
        RegexValidator(r'[a-zA-Z0-9]+', _('Username can only contain letters and numbers.'))
    ])
    error_messages = {
        'password_mismatch': _("The two passwords didn't match."),
    }
    password1 = PasswordField(label='Password', widget=forms.PasswordInput)
    password2 = PasswordField(label='Password confirmation', widget=forms.PasswordInput,
                              help_text=_('Enter the same password as above, for verification.'))

    class Meta:
        model = User
        fields = ('email', 'username',)

    # def clean_username(self):
    #     data = self.cleaned_data['username']
    #     # if RegexValidator(r'^\S+$'):
    #     #     raise ValidationError(_('Username can not contain spaces.'))
    #     if RegexValidator(r'[^a-zA-Z0-9]+'):
    #         raise ValidationError(_('Username can only contain letters and numbers.'))
    #     return data

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    TIMEZONE_CHOICES = [
        (pytz.timezone(tz), tz.replace('_', ' '))
        for tz in pytz.common_timezones
    ]
    email = forms.EmailField()
    username = forms.CharField(max_length=32)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    last_login = forms.DateTimeField(required=False, disabled=True)
    date_joined = forms.DateTimeField(required=False, disabled=True)
    theme = forms.ModelChoiceField(required=False, queryset=Theme.objects.all(), empty_label="Default")
    timezone = forms.ChoiceField(choices=TIMEZONE_CHOICES)
    #is_active = forms.BooleanField(default=True)

    password = ReadOnlyPasswordHashField(label=_('Password'),
        help_text=_('Raw passwords are not stored, so there is no way to see '
                    "this user's password, but you can change the password "
                    'using <a href="/account/password/change/">this form</a>.'))

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'theme', 'timezone', 'last_login', 'date_joined',)
        #exclude = ('password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get('password')


class UserForm(forms.Form):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)


class ChangePasswordForm(PasswordVerificationMixin, UserForm):

    oldpassword = PasswordField(label=_('Current Password'))
    password1 = PasswordField(label=_('New Password'))
    password2 = PasswordField(label=_('Confirm New Password'))

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].user = self.user

    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get('oldpassword')):
            raise forms.ValidationError(_('Please type your current'
                                          ' password.'))
        return self.cleaned_data['oldpassword']

    def save(self):
        get_adapter().set_password(self.user, self.cleaned_data['password1'])

