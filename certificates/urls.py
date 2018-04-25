from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.domains, name='domains'),
    re_path(r'^[a-z0-9*-.]{3,64}/[0-9]+', views.manage, name='manage certificate'),
    re_path(r'^[a-z0-9*-.]{3,64}', views.certificates, name='certificates'),
]