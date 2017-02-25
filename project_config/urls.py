"""museon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, static
from django.conf import settings
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from app.viewsets.media_viewset import MediaViewset
from utils.amuze_config import AmuzeConfig

router = DefaultRouter()
router.register(r'media', MediaViewset)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'v1/', include(router.urls)),
]

urlpatterns += static.static(AmuzeConfig.MEDIA_URL, document_root=AmuzeConfig.MEDIA_FOLDER)
urlpatterns += static.static(AmuzeConfig.THUMBNAIL_URL, document_root=AmuzeConfig.THUMBNAIL_FOLDER)
