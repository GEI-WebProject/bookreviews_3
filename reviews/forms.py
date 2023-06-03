from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    CHOICES = [(i, str(i)) for i in range(1, 5+1)]
    
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'rows': 1,
        'cols': 2,
        }), max_length=Review._meta.get_field('title').max_length)
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 4,
        'cols': 3,
        }))
    rating = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    class Meta:
        model = Review
        fields = ['title', 'body', 'rating']
        