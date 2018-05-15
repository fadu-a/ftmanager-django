from django.db import transaction
from rest_framework import serializers

from . import models


class JobSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.ReadOnlyField(source='testcase.name')
    id = serializers.IntegerField(source='testcase_id')

    class Meta:
        model = models.Job
        fields = ('id', 'name', 'order')


class TestcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Testcase
        fields = ('url', 'id', 'name', 'extra')


class ScenarioSerializer(serializers.ModelSerializer):
    testcases = JobSerializer(source='job_set', many=True)

    class Meta:
        model = models.Scenario
        fields = ('url', 'id', 'name', 'testcases')

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


class IoLogReadSerializer(serializers.ModelSerializer):
    order = serializers.ReadOnlyField(source='job.order')
    testcase_id = serializers.ReadOnlyField(source='job.testcase.id')
    testcase_name = serializers.ReadOnlyField(source='job.testcase.name')

    class Meta:
        model = models.IoLog
        fields = ('id', 'order', 'testcase_id', 'testcase_name', 'data')


class ResultSerializer(serializers.ModelSerializer):
    io_logs = IoLogReadSerializer(many=True, read_only=True)

    class Meta:
        model = models.Result
        fields = ('url', 'id', 'status', 'test_date', 'runner', 'scenario', 'io_logs')

    @transaction.atomic
    def create(self, validated_data):
        result = models.Result.objects.create(**validated_data)
        for job in result.scenario.job_set.all():
            models.IoLog.objects.create(job=job, result=result)
        return result


class IoLogSerializer2(serializers.ModelSerializer):
    order = serializers.ReadOnlyField(source='job.order')
    name = serializers.ReadOnlyField(source='job.testcase.name')
    configs = serializers.ReadOnlyField(source='job.testcase.extra')

    class Meta:
        model = models.IoLog
        fields = ('id', 'order', 'name', 'configs')


class TestSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='scenario.name')
    testcases = IoLogSerializer2(source='io_logs', many=True)

    class Meta:
        model = models.Result
        fields = ('id', 'name', 'testcases')
