from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import TemplateView
from django.utils import timezone

import pytz


class IndexView(TemplateView):
    template_name = 'base/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PermissionDeniedView(TemplateView):
    template_name = 'base/error_pages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_code'] = 403
        context['error_mesg'] = 'Forbidden'
        context['error_title'] = 'Permission Denied'
        return context


class PageNotFoundView(TemplateView):
    template_name = 'base/error_pages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_code'] = 404
        context['error_mesg'] = 'Not found'
        context['error_title'] = 'Page Not Found'
        return context


class BadRequestView(TemplateView):
    template_name = 'base/error_pages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_code'] = 400
        context['error_mesg'] = 'Bad Request'
        context['error_title'] = 'Bad Request'
        return context


class ServerErrorView(TemplateView):
    template_name = 'base/error_pages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_code'] = 500
        context['error_mesg'] = 'Server Error'
        context['error_title'] = 'Server Error'
        return context
