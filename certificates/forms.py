from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django import forms
from django.forms import Textarea

from .models import *


class DomainForm(forms.Form):
    domain_name = forms.CharField(
        widget=forms.TextInput,
        label='Enter domain name',
        required=True,
        validators=[
            RegexValidator(
                regex = r'^((?=[a-z0-9-]{1,63}\.)([a-z0-9]+|[a-z0-9][a-z0-9-]*[a-z0-9])*\.)+([a-z]|xn--[a-z0-9-]+){2,63}$',
                message = 'Invalid domain name',
                code = 'invalid_domain_name'
            )
        ]
    )     

class ManageForm(forms.Form):
    private_key = forms.CharField(label="PK")
    openssl_conf = forms.Textarea()
    csr = forms.CheckboxInput()
    crt = forms.CheckboxInput()
    intermediate = forms.CheckboxInput()
    # valid = forms.DateTimeField()

class CertificateForm(forms.ModelForm):

    class Meta:
        model = Certificate
        fields = ["private_key", "csr", "crt", "intermediate"]
        widgets = {
            "private_key":Textarea(attrs={'cols':80, 'rows':2}),
            "csr":Textarea(attrs={'cols':80, 'rows':2}),
            "crt":Textarea(attrs={'cols':80, 'rows':2}),
            "intermediate":Textarea(attrs={'cols':80, 'rows':2})
        }

    #Init data from instance
    @staticmethod
    def init_data(instance):
        initial = {}
        for key in CertificateForm.Meta.fields:
            initial.update({key:instance.__dict__[key]})
        return CertificateForm(initial=initial)
