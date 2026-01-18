from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'team', 'size', 'brand', 'type', 'price', 'is_retro', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }