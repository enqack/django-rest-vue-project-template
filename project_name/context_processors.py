from django.conf import settings
from django.utils import timezone


def project(request):
    return {
        'head_title': settings.PROJECT_NAME,
        'project_name': settings.PROJECT_NAME,
        'current_time': timezone.now(),
    }
