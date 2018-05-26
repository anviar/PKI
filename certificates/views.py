from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import DomainForm, CertificateForm
from .models import Domain, Certificate
from .openssl import generate_pkey, generate_req, get_req, get_pkey


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

    if cert_id != 0:
        cert = get_object_or_404(Certificate, id=cert_id)
        certificate_form = CertificateForm(instance=cert)
    else:

        pk = generate_pkey()
        req = generate_req(pk, domain_name)
        data = {"private_key": get_pkey(pk), "csr": get_req(req)}
        certificate_form = CertificateForm(initial=data)

    if request.method == "POST":
        if cert_id == 0:
            cert_id = Certificate.objects.last().id + 1
            cert = Certificate(domain_name=Domain.objects.get(domain_name=domain_name), id=cert_id)
        certificate_form = CertificateForm(request.POST, instance=cert)
        if certificate_form.is_valid():
            certificate_form.save()
            return HttpResponseRedirect(reverse("certificate", args=(domain_name, cert_id)))

    context = {'certificate_form': certificate_form,
               'domain_name': domain_name,
               "owner": user,
               "cert_id": cert_id
               }

    return render(request, "certificate/certificate.html", context)

def download(request, domain_name, cert_id, filetype):

    fyletypes = {"pem":"private_key", "csr":"csr"}
    data = getattr(get_object_or_404(Certificate, id=cert_id), fyletypes[filetype])
    response = HttpResponse(data, content_type="application/pem")
    response['Content-Disposition'] = 'attachment; filename={}{}.{}'.format(domain_name,cert_id,filetype)
    return response