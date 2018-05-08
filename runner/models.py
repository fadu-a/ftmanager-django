from django.db import models

from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _


class Runner(models.Model):
    """Test runner info"""

    STATUS_UNKNOWN = 0
    STATUS_IDLE = 1
    STATUS_BUSY = 2

    STATUS_CHOICES = (
        (STATUS_UNKNOWN, _('Unknown')),
        (STATUS_IDLE, _('Idle')),
        (STATUS_BUSY, _('Busy')),
    )

    host = models.GenericIPAddressField()
    port = models.IntegerField()
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_UNKNOWN
    )
    info = JSONField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def status_request_url(self):
        return f"http://{self.host}:{self.port}/status"

    def __str__(self):
        return _(f'Runner {self.host}:{self.port}')
