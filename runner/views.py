import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Runner
from .serializers import RunnerSerializer


class RunnerViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating runners"""

    queryset = Runner.objects.order_by('host')
    serializer_class = RunnerSerializer

    @action(detail=True)
    def check(self, request, pk=None):
        """API to check runner status"""

        runner = self.get_object()
        req_url = runner.status_request_url()

        try:
            resp = requests.get(req_url)
            serializer = self.get_serializer(runner, data=resp.json(), partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        except requests.ConnectionError:
            content = {'error': 'internal server error'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
