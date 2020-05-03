from django import forms
from .models import Portfolio


class StockForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['ticker']
