from django.urls import path

from . import views

urlpatterns = [
    path('domains/', views.domains, name="domains"),
    path('domain/<str:domain_name>/certificates/', views.certificates, name='certificates'),
    path('domain/<str:domain_name>/<int:cert_id>', views.certificate, name='certificate'),
    path('download/<str:domain_name>/<int:cert_id>/<str:filetype>/', views.download, name='download'),
]
