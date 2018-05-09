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
        print(validated_data)
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
