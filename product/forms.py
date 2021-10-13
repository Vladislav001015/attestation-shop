from django import forms
from product.models import Product, Category, Image, Comment, Favorites, Like, Contact



class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'owner', 'product',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'descriptions', 'price', 'quantity', 'image', 'category',)


class FavoriteForms(forms.ModelForm):
    class Meta:
        model = Favorites
        fields = "__all__"


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


