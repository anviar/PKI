from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import permissions

from .models import Certificate, Domain

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404

from .openssl import generate_pkey, generate_req, get_pkey, get_req


class DomainSerializer(serializers.Serializer):
    domain_name = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=Domain.objects.all()),
            RegexValidator(
                regex=r'^((?=[a-z0-9-]{1,63}\.)([a-z0-9]+|[a-z0-9][a-z0-9-]*[a-z0-9])*\.)+([a-z]|xn--[a-z0-9-]+){2,63}$',
                message='Invalid domain name',
                code='invalid_domain_name'
            )
        ]
    )

    email = serializers.EmailField(allow_blank=True, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    # owner = serializers.ReadOnlyField(required=False)
    owner = serializers.ReadOnlyField(source='owner.username')
    certs_number = serializers.IntegerField(required=False)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, validated_data):
        new_domain = Domain.objects.create(owner=validated_data["owner"],
                                           email=validated_data["email"],
                                           domain_name=validated_data["domain_name"],
                                           )
        pk = generate_pkey()
        req = generate_req(pk, validated_data["domain_name"])
        Certificate.objects.create(domain_name=new_domain, private_key=get_pkey(pk),
                                   csr=get_req(req))
        return new_domain

    def update(self, instance, validated_data):
        for key in validated_data.keys():
            setattr(instance, key, validated_data[key])
        instance.save()
        return instance

    def delete(self, validate_data):
        domain = Domain.objects.get(domain_name=validate_data["domain_name"])
        return domain.objects.update(deleted=True)


class CertificateListSerializer(serializers.Serializer):
    certificate = serializers.CharField(required=True)


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ("private_key", "csr", "crt", "intermediate")

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, validated_data):
        domain = get_object_or_404(validated_data["request"])
        return Certificate.objects.create(domain_name=domain, **validated_data)


class UserSerializer(serializers.ModelSerializer):
    domains = serializers.PrimaryKeyRelatedField(many=True, queryset=Domain.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'domains')
