from django.db import models
from django.contrib.postgres.fields import JSONField


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
