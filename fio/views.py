from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import requests

from . import models, serializers


class ModelExceptUpdateViewSet(mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`,
    `destroy()` and `list()` actions.
    """
    pass


class ActionSerializerMixin(object):
    action_serializers = {}

    def get_serializer_class(self):
        if self.action in self.action_serializers:
            return self.action_serializers.get(self.action, None)
        else:
            return super().get_serializer_class()


class TestcaseViewSet(ModelExceptUpdateViewSet):
    queryset = models.Testcase.objects.all()
    serializer_class = serializers.TestcaseSerializer


class ScenarioViewSet(ModelExceptUpdateViewSet):
    queryset = models.Scenario.objects.all()
    serializer_class = serializers.ScenarioSerializer


class PresetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Preset.objects.all()
    serializer_class = serializers.PresetSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = models.Result.objects.all()
    serializer_class = serializers.ManagerResultSerializer

    def send_to_runner(self, result):
        serializer = serializers.RunnerResultSerializer(result)
        # TODO: request error handling
        url = result.test_request_url()
        requests.post(url, json=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        self.send_to_runner(result)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class IoLogViewSet(viewsets.GenericViewSet):
    queryset = models.IoLog.objects.all()
    # serializer_class = serializers.IoLogSerializer

    @action(methods=['put'], detail=True)
    def append(self, request, *args, **kwargs):
        # TODO: validation check
        io_log = self.get_object()
        io_log.data.append(request.data)
        io_log.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
