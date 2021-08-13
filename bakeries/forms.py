from django import forms
from .models import Review


class WriteReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "body"]

