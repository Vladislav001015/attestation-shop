from django.urls import path
from .views import *
urlpatterns = [
    path('create/', ProductCreate.as_view(), name='product_create'),
    path('create/category/', CategoryCreate.as_view(), name='category_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDelete.as_view(), name='product_delete'),
    path('add-like/<int:id>/', AddLikeView.as_view(), name='add-like'),
    path('delete-like/<int:like_id>/', DeleteLikeView.as_view(), name='delete-like'),
    # path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),

    path('product_detail/<int:pk>/', ProductDetailView, name='detail'),

#

    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category'),

    path('contact/', ContactView.as_view(), name='contact'),



]