from django import forms
from .models import User

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','nickname','password']