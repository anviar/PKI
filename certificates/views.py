from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework import generics

from .models import Domain, Certificate
from .serializers import CertificateSerializer, DomainSerializer, UserSerializer


@csrf_exempt
def domainapi(request):

    if request.method == "GET":
        domains = Domain.objects.all()
        serializer = DomainSerializer(domains, many=True)
        return JsonResponse(serializer.data, safe=False)


class DomainList(generics.ListCreateAPIView):
    queryset = Domain.objects.annotate(certs_number=Count('certificate')).all()
    serializer_class = DomainSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DomainDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Domain.objects.annotate(certs_number=Count('certificate')).all()
    serializer_class = DomainSerializer


class CertificateList(generics.ListCreateAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

    def get_object(self):
        return super().get_object()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(domain_name=self.kwargs['domain'])


class CertificateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
