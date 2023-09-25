"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

import os
import re
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.static import serve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog/')),   # Root '/' redirects to 'catalog/'
    re_path("^catalog/static/(?P<path>.*)$", serve, {
                                            'document_root': settings.STATIC_ROOT, 
                                            'show_indexes': True
                                            }, name='static'),
    

]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL),   # to urlpath handled with serve
