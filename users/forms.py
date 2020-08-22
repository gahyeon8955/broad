from django import forms
from .models import User
from django.contrib.auth import get_user_model


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "password"]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={}))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 틀렸습니다"))
        except User.DoesNotExist:
            self.add_error("username", forms.ValidationError("계정이 존재하지 않습니다"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]

    password = forms.CharField(widget=forms.PasswordInput(attrs={}))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={}))

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다")
        else:
            return password

