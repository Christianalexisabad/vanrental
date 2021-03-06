from django.contrib.auth.forms import UserCreationForm, UserChangeForm  
from django.db.models import fields  
from django import forms  
from .models import CustomUser  
from django.contrib.auth import get_user_model  



class CustomUserCreationForm(UserCreationForm):  
 
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )  
   
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )  
 
    class Meta:  
        model = CustomUser  
        fields = ['email']
     
    def clean_email(self):  
   
        email = self.cleaned_data.get('email')  
        qs = CustomUser.objects.filter(email=email)  
   
        if qs.exists():  
            raise forms.ValidationError("Email is already taken")  
        return email  
   
    def clean(self):  
        cleaned_data = super().clean()  
        password1 = cleaned_data.get("password1")  
        password2 = cleaned_data.get("password2")  
         
        if password1 is not None and password1 != password2:  
           
            self.add_error(
                "password2",
                "Your passwords must match"
            )  
       
        return cleaned_data
    def save(self, commit=True):  
       
        user = super().save(commit=False)  
        user.set_password(self.cleaned_data["password1"])  
       
        if commit:  
            user.save()  
       
        return user