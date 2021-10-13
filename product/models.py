from django.db import models
from accounts.models import CustomUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        if not self.parent:
            return self.name
        else:
            return f"{self.parent} --> {self.name}"

    def get_children(self):
        if self.children:
            return self.children.all()
        return False


class Product(models.Model):
    title = models.CharField(max_length=150)
    descriptions = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    owner = models.ForeignKey(CustomUser, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    like_id = models.IntegerField(default=0, blank=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} --> {self.product}'


class Like(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ['owner', 'product']

    def __str__(self):
        return str(self.id)



class Favorites(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorites = models.BooleanField()

    def __str__(self):
        return self.owner.email


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.name

