from django import forms
from .models import *

class LoginForm(forms.Form):
    patient_name = forms.CharField(label='Patient Name', max_length=25)

class RegisterForm(forms.ModelForm):
    class Meta:
        model=Registration
        fields='__all__'

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model=Login_patient
#         fields = '__all__'

class SlotForm(forms.ModelForm):
    class Meta:
        model = Slots
        fields= '__all__'

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class HistoryForm(forms.ModelForm):
    class Meta:
        model=history
        fields = '__all__'

# forms.py


# forms.py

from django import forms

class PaymentForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=10)
    stripe_token = forms.CharField(widget=forms.HiddenInput())


class AdminForm(forms.ModelForm):
    class Meta:
        model=admin_resource
        fields = '__all__'