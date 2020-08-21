from django import forms
from .models import User

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','nickname','password']
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 틀렸습니다"))
        except User.DoesNotExist:
            self.add_error("username", forms.ValidationError("계정이 존재하지 않습니다"))