from django import forms
from django.utils import timezone
# TODO

class OrderForm(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()
    email = forms.EmailField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=([('self', 'Самовызов'), ('delivery', 'Доставка')]))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comment = forms.CharField(widget=forms.Textarea())