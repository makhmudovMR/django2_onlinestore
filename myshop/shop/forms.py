from django import forms
from django.utils import timezone
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegsiterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_check = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password','password_check', 'email', 'first_name', 'last_name']

    def clean(self, *args, **kwargs):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password_check != password:
            raise forms.ValidationError('Passwords is not equi')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is exist')
        

    

class OrderForm(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()
    email = forms.EmailField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=([('self', 'Самовызов'), ('delivery', 'Доставка')]))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comment = forms.CharField(widget=forms.Textarea())