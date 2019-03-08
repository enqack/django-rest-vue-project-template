from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Theme

def theme(request):
    # get user theme selection or default
    try:
        user = get_user_model().objects.get(id=request.user.id)
        theme = Theme.objects.get(id=user.theme.id)
    except:
        try:
            theme = Theme.objects.get(default=True)
        except:
            theme = lambda: None
            theme.file_name = ''

    return {
        'theme_file': settings.THEME_ROOT+theme.file_name
    }
