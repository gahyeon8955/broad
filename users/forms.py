from django import forms
from .models import User
from django.contrib.auth import get_user_model


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["nickname"]
        widgets = {
            "nickname": forms.TextInput(
                attrs={"class": "profile_update_input", "placeholder": "선택입력"}
            ),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "profile_update_input", "placeholder": "비밀번호"}
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "profile_update_input", "placeholder": "비밀번호 재입력"}
        )
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다")
        else:
            return password


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "login_id_button", "placeholder": "이메일"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "login_password_button", "placeholder": "비밀번호"}
        )
    )

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
        fields = ["email", "nickname"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "signup_input", "placeholder": "@example.com"}
            ),
            "nickname": forms.TextInput(
                attrs={"class": "signup_input", "placeholder": "선택입력"}
            ),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "signup_input", "placeholder": "비밀번호"}
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "signup_input", "placeholder": "비밀번호 재입력"}
        )
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다")
        else:
            return password

class UpdateProfileImageForm(forms.ModelForm):
     class Meta:
        model = User
        fields = ['avatar']
