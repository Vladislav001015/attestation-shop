from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from product.views import ProductList
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('admin/', admin.site.urls),

    path('cart/', include('cart.urls', namespace='cart')),

    path('', ProductList.as_view(), name='index'),
    path('register/', include('accounts.urls')),
    path('product/', include('product.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
