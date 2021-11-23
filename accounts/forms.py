from django import forms 
from .models import OrderModel
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class orderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['customer_name', 'service_charge' , 'parts_cost' , 'refreshment_cost']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'service_charge': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'parts_cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'refreshment_cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        }


# class loginForm(ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'
#         widgets = {
#             'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'name': 'cname'}),
#             'password': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
#         }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user