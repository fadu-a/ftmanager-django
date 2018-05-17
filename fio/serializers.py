from django.db import transaction
from rest_framework import serializers

from . import models


class JobSerializer(serializers.HyperlinkedModelSerializer):
    testcase_name = serializers.ReadOnlyField(source='testcase.name')

    class Meta:
        model = models.Job
        fields = ('testcase_id', 'testcase_name', 'order')


class TestcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Testcase
        fields = ('url', 'id', 'name', 'extra')


class ScenarioSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(source='job_set', many=True)

    class Meta:
        model = models.Scenario
        fields = ('url', 'id', 'name', 'jobs')

    @transaction.atomic
    def create(self, validated_data):
        jobs_data = validated_data.pop('job_set')
        scenario = models.Scenario.objects.create(**validated_data)
        for job_data in jobs_data:
            models.Job.objects.create(
                scenario=scenario,
                testcase_id=job_data['testcase_id'],
                order=job_data['order']
            )
        return scenario


class PresetSerializer(serializers.ModelSerializer):
    scenario = ScenarioSerializer()

    class Meta:
        model = models.Preset
        fields = ('url', 'id', 'name', 'scenario')


class ClientIoLogSerializer(serializers.ModelSerializer):
    job_order = serializers.ReadOnlyField(source='job.order')
    job_testcase_id = serializers.ReadOnlyField(source='job.testcase.id')
    job_testcase_name = serializers.ReadOnlyField(source='job.testcase.name')

    class Meta:
        model = models.IoLog
        fields = ('id', 'job_order', 'job_testcase_id', 'job_testcase_name', 'data')


class ClientResultSerializer(serializers.ModelSerializer):
    io_logs = ClientIoLogSerializer(many=True, read_only=True)

    class Meta:
        model = models.Result
        fields = ('url', 'id', 'status', 'test_date', 'runner', 'scenario', 'io_logs')

    @transaction.atomic
    def create(self, validated_data):
        result = models.Result.objects.create(**validated_data)
        for job in result.scenario.job_set.all():
            models.IoLog.objects.create(job=job, result=result)
        return result


class RunnerIoLogSerializer(serializers.ModelSerializer):
    job_order = serializers.ReadOnlyField(source='job.order')
    job_testcase_name = serializers.ReadOnlyField(source='job.testcase.name')
    job_testcase_extra = serializers.ReadOnlyField(source='job.testcase.extra')

    class Meta:
        model = models.IoLog
        fields = ('id', 'job_order', 'job_testcase_name', 'job_testcase_extra')


class RunnerResultSerializer(serializers.ModelSerializer):
    scenario_name = serializers.ReadOnlyField(source='scenario.name')
    testcases = RunnerIoLogSerializer(source='io_logs', many=True)

    class Meta:
        model = models.Result
        fields = ('id', 'scenario_name', 'testcases')
