from rest_framework import mixins, viewsets

from . import models, serializers


class ModelExceptUpdateViewSet(mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `destroy()` and `list()` actions.
    """
    pass


class TestcaseViewSet(ModelExceptUpdateViewSet):
    queryset = models.Testcase.objects.all()
    serializer_class = serializers.TestcaseSerializer


class ScenarioViewSet(ModelExceptUpdateViewSet):
    queryset = models.Scenario.objects.all()
    serializer_class = serializers.ScenarioSerializer


class PresetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Preset.objects.all()
    serializer_class = serializers.PresetSerializer
