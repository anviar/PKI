from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import DomainForm, CertificateForm
from .models import Domain, Certificate


# Receive domain list for current user
def domains(owner):
    return {'domains':[domain for domain in Domain.objects.filter(owner=owner)]}
    
# Add new domain
def add_domain(request):

    if request.method == "POST":
        domain = DomainForm(request.POST)
        if domain.is_valid():
            domain_name = domain.cleaned_data["domain_name"]
            new_domain = Domain(owner='oleg', domain_name = domain_name)
            new_domain.save()
            return HttpResponseRedirect(reverse("domains", args=(domain_name,)))
        else:
            context = {'domain_form':domain, 'domain_name':0, "certificate_id":0}
            return render(request, "layout.html", context)

#Receive certificate list for domain
def certificates(domain_name):
    return {'certificates':[certificate for certificate in Certificate.objects.filter(domain_name=domain_name)]}

# Add new certificate to domain
def add_certificte(request, domain_name, id):

    if request.method == "POST":
        if id != 0:
            certificate = Certificate.objects.get(id=id)
        else:
            certificate = Certificate(domain_name=Domain.objects.get(domain_name=domain_name))
        certificate_form = CertificateForm(request.POST, instance=certificate)
        if certificate_form.is_valid():
            certificate_form.save()
        return HttpResponseRedirect(reverse("certificates", args=((domain_name, id ))))

# View for manage domains and certificates
def manage(request, domain_name='', user='oleg', id=0):
    context = {"domain_name":domain_name, "owner":user, "certificate_id":id}
    context.update(domains(user))
    context.update(certificates(domain_name))
    if id !=0: certificate_form = CertificateForm.init_data(Certificate.objects.get(id=id))
    else: certificate_form = CertificateForm()
    context.update({"domain_form": DomainForm(), "certificate_form": certificate_form})

    return render(request, "layout.html", context)