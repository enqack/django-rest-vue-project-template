from django.conf import settings
from django.utils import timezone

import pytz


class TimezoneMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            timezone_selected = request.user.timezone
            if not timezone_selected:
                timezone_selected = settings.TIME_ZONE
            timezone.activate(timezone_selected)
        else:
            timezone.deactivate()
        return self.get_response(request)
