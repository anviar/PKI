import re

#from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from django import forms
from django.forms import Textarea

from .models import *

# Validation domain name
#def validate_domain(input_domain):
#    if not re.match('^((?=[a-z0-9-]{1,63}\.)([a-z0-9]+|[a-z0-9][a-z0-9-]*[a-z0-9])*\.)+([a-z]|xn--[a-z0-9-]+){2,63}$', input_domain.replace('*.', '') ):
#        raise ValidationError(
#            _('%(input_domain)s is incorrect domain name'),
#            params={'input_domain': input_domain},
#        )

class DomainForm(forms.Form):
    #domain_name = forms.CharField(widget=forms.TextInput, label='Enter domen name', validators=[validate_domain], error_messages={'invalid': _(u'Enter a valid domain name.')})
    domain_name = forms.CharField(
        widget=forms.TextInput,
        label='Enter domain name',
        error_messages={'invalid_domain_name': 'Domain name not match regex'},
        validators=[RegexValidator(r'^((?=[a-z0-9-]{1,63}\.)([a-z0-9]+|[a-z0-9][a-z0-9-]*[a-z0-9])*\.)+([a-z]|xn--[a-z0-9-]+){2,63}$', 'Enter a valid domain name')]
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
