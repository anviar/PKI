from django.shortcuts import render
from .models import *
from .forms import *


def domains(request):
    if request.method == 'POST':
        domain_add_form = DomainsForm(request.POST)
        if domain_add_form.is_valid():
            new_domain = Domain(
                owner='oleg',
                domain_name=domain_add_form.cleaned_data['domain_name'])
            new_domain.save()
    else:
        domain_add_form = DomainsForm()
    return render(request,
                  'domains.html',
                  {
                      'domain_add_form': domain_add_form,
                      'domains': [d.__dict__
                                  for d in
                                  Domain.objects.filter(owner='oleg')]
                  })


def certificates(request):
    domain_name = request.path.split('/')[2]
    if 'create_crt' in request.GET:
        new_crt = Certificate(
            domain_name=domain_name,
        )
        new_crt.save()
    return render(request,
                  'certificates.html',
                  {
                      'domain_name': domain_name,
                      'certificates': [c.__dict__
                                       for c in
                                       Certificate.objects.filter(domain_name=domain_name)]
                  })


def manage(request):
    domain_name = request.path.split('/')[2]
    if request.method == 'POST':
        certificate_manage_form = ManageForm(request.POST)
    else:
        certificate_manage_form = ManageForm
    if 'create_crt' in request.GET:
        new_crt = Certificate(
            domain_name=domain_name,
        )
        new_crt.save()
    return render(request,
                  'manage.html',
                  {
                      'domain_name': domain_name,
                      'certificate_manage_form': certificate_manage_form
                  })