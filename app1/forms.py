from .models import bank
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    class meta:
        model = bank
        fields = ['Ac_no', 'password']
        exclude = ['last_login']