"""ftmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from runner.views import RunnerViewSet
from fio.views import PresetViewSet, ScenarioViewSet, TestcaseViewSet, ResultViewSet, IoLogViewSet

router = DefaultRouter()
router.register(r'runners', RunnerViewSet)
router.register(r'fio/presets', PresetViewSet)
router.register(r'fio/scenarios', ScenarioViewSet)
router.register(r'fio/testcases', TestcaseViewSet)
router.register(r'fio/results', ResultViewSet)
router.register(r'fio/io_logs', IoLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    url(r'^api/', include(router.urls)),
]
