from email import message
from socket import fromshare
from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.core.exceptions import ValidationError
from django import forms
import re

def check_url(value):
    if not re.match('^https?//[^\./]+.*',value):
        raise ValidationError('URL Validation Error')
class search_form(forms.Form):
    url = forms.CharField(max_length=150,required=True,widget=forms.URLInput,validators=[check_url])
