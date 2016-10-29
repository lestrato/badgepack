from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.conf import settings
from community.models import Community

class BadgeClass(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=140)
    # imagefield is why we need PILLOW installed
    # image = models.ImageField(upload_to='uploads/%Y/%m/%d/',height_field=150, width_field=150,)

    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    # creator = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_on = models.DateField(default=datetime.now)
    is_available = models.BooleanField(default=False)
    # discontinued_by = models.ManyToManyField(settings.AUTH_USER_MODEL)


    class Meta:
        verbose_name = 'badgeclass'
        verbose_name_plural = 'badgeclasses'
        db_table = 'badgeclass'

    def __str__(self):
        return self.name
