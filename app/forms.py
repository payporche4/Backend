from django import forms
from django.conf import settings
from .models import TransactionRecord
User = settings.AUTH_USER_MODEL


class TransactionForm(forms.ModelForm):

    class Meta:
        model = TransactionRecord
        fields = ('sender', 'receiver', 'amount')
