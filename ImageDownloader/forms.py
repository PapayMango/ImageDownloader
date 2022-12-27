from email import message
from socket import fromshare
from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.core.exceptions import ValidationError
from django import forms

class search_form(forms.Form):
    url = forms.CharField(max_length=150,required=True,widget=forms.URLInput)
