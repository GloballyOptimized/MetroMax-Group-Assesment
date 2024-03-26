from django import forms
from .models import Category
from .models import Product
from .models import Comment
from .models import Review

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content', 'rating')