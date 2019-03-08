from __future__ import unicode_literals
from django.db import transaction
from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=32)
    file_name = models.CharField(max_length=1024)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.default:
            Theme.objects.filter(default=True).update(default=False)
        super(Theme, self).save(*args, **kwargs)

