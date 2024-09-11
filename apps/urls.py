"""
URL configuration for apps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.http import HttpResponse
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dotenv import load_dotenv, dotenv_values
import os

from apps.recognition.views import RecognitionView

load_dotenv()
schema_view = get_schema_view(
    openapi.Info(
        title="Mi API",
        default_version='v1',
        description="Descripción de mi API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('apps.parents.urls')),
    path('', include('apps.therapists.urls')),
    path('', include('apps.child.urls')),
    path('recognition/', RecognitionView.as_view()),
]