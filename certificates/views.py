from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import DomainForm, CertificateForm
from .models import Domain, Certificate


def domains(request):

    user = request.user
    domain_form = DomainForm()

    if request.method == "POST":
        dn = DomainForm(request.POST)
        if dn.is_valid():
            add_dn = Domain(owner=user, domain_name=dn.cleaned_data["domain_name"])
            add_dn.save()
            return HttpResponseRedirect(reverse("domains"))
        else:
            domain_form = dn

    domains_list = Domain.objects.filter(owner=user)
    context = {"domain_form": domain_form, "owner": user, "domains": domains_list}
    return render(request, "certificate/domains.html", context)


def certificates(request, domain_name):

    user = request.user
    certs = [cert for cert in Certificate.objects.filter(domain_name=domain_name)]
    context = {'certificates': certs, "domain_name": domain_name, "user": user}

    return render(request, "certificate/certificates.html", context)


def certificate(request, domain_name, cert_id):

    user = request.user
    certificate_form = CertificateForm()

    if request.method == "POST":
        if cert_id != 0:
            cert = get_object_or_404(Certificate, id=cert_id)
        else:
            cert = Certificate(domain_name=Domain.objects.get(domain_name=domain_name))
            cert.save()
            cert_id = cert.id
        certificate_form = CertificateForm(request.POST, instance=cert)

        if certificate_form.is_valid():
            certificate_form.save()
            return HttpResponseRedirect(reverse("certificate", args=(domain_name, cert_id)))

    context = {'certificate_form': certificate_form, 'domain_name': domain_name, "owner": user}
    return render(request, "certificate/certificate.html", context)
