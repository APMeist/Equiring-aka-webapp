from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import SetPasswordForm

from supports.models import SupporTicket
from .models import User, Contracts, Companies


class PrimaryUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','email', 'phone_number', 'message']

class CreateTicketForm(ModelForm):
    class Meta:
        model = SupporTicket
        fields = ['contract', 'description']
        widgets = {'contract': forms.Select()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['contract'].queryset = Companies.objects.filter(
                founder=user,
                status='approved'
            )

class CreateCompanyForm(ModelForm):
    class Meta:
        model = Companies
        fields = ['INN', 'OGRN', 'name_company']

class CreateContractForm(forms.ModelForm):
    class Meta:
        model = Contracts
        fields = ['name_contract', 'company']
        widgets = {
            'company': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['company'].queryset = Companies.objects.filter(
                founder=user,
                status='approved',
            )