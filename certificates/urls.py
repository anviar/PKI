from django.urls import path, re_path

from . import views

urlpatterns = [
    path('domains/', views.manage, {"domain_name":"home", "id":0}),
    path('domains/<str:domain_name>/', views.manage, {"id":0}, name='domains' ),
    path('domains/<str:domain_name>/<int:id>/', views.manage, name='certificates'),
    path('add_domain/', views.add_domain, name='add_domain'),
    path('add_certificate/<str:domain_name>/<int:id>',
         views.add_certificte, name='add_certificate'),
]
