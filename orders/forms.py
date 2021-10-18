from django import forms
from .models import Order
from localflavor.us.forms import USZipCodeField
from localflavor.ir.forms import IRPostalCodeField
from django.utils.translation import gettext_lazy as _


class OrderCreateForm(forms.ModelForm):
    #postal_code = USZipCodeField(label=_("Postal code"))
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address','postal_code', 'city']

    def __init__(self, language_code='en', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if language_code=='en':
            self.fields['postal_code']=USZipCodeField(label=_("Postal code"))
        if language_code=='fa':
            self.fields['postal_code']=IRPostalCodeField(label=_("Postal code"))
