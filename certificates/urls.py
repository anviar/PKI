from django.conf.urls import url
from django.urls import path
from django.conf.urls import include    
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title='PKI API')


urlpatterns = [
    path('users/', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    path('api/', schema_view),
    url(r'^api/domain/$', views.DomainList.as_view()),
    url(r'^api-auth/',  include('rest_framework.urls')),
    path('api/domain/<str:pk>/', views.DomainDetail.as_view()),
    path('api/certificate/<str:pk>/', views.CertificateDetail.as_view()),
]
