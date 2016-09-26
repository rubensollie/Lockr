"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class AddBluetoothDeviceForm(forms.Form):
    bluetoothaddress = forms.CharField(max_length=17, min_length=17, widget=forms.TextInput({ 'class': 'form-control', 'placeholder':'Bluetooth device',  'style':'margin-top:10px' }))
    displayname = forms.CharField(max_length=50, min_length=1, widget=forms.TextInput({ 'class': 'form-control', 'placeholder':'Display name' }))
