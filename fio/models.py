from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.utils.translation import ugettext_lazy as _


class Testcase(models.Model):
    name = models.CharField(max_length=64)
    extra = JSONField(null=True)


class Scenario(models.Model):
    name = models.CharField(max_length=64)
    testcases = models.ManyToManyField('Testcase', through='Job')


class Job(models.Model):
    testcase = models.ForeignKey('Testcase', on_delete=models.CASCADE)
    scenario = models.ForeignKey('Scenario', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()


class Preset(models.Model):
    name = models.CharField(max_length=64)
    scenario = models.OneToOneField('Scenario', on_delete=models.CASCADE)


class Result(models.Model):
    STATUS_STARTED = 0
    STATUS_FINISHED = 1
    STATUS_FAILED = 2

    STATUS_CHOICES = (
        (STATUS_STARTED, _('Started')),
        (STATUS_FINISHED, _('Finished')),
        (STATUS_FAILED, _('Failed')),
    )

    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_STARTED
    )
    test_date = models.DateTimeField(auto_now_add=True)
    scenario = models.ForeignKey('Scenario', on_delete=models.CASCADE)
    runner = models.ForeignKey('runner.Runner', on_delete=models.CASCADE)


class IoLog(models.Model):
    result = models.ForeignKey('Result', related_name='io_logs', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    data = ArrayField(models.TextField(), default=[])
