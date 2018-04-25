from django import forms
from .models import *


class DomainsForm(forms.Form):
    domain_name = forms.CharField(widget=forms.TextInput, label='')


class ManageForm(forms.Form):
    private_key = forms.CharField()
    openssl_conf = forms.Textarea()
    csr = forms.CheckboxInput()
    crt = forms.CheckboxInput()
    intermediate = forms.CheckboxInput()
    # valid = forms.DateTimeField()
