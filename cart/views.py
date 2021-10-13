from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from product.models import Product
from .cart import Cart
from .forms import CartAddProductForm, OrderForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})



class OrderCreate(CreateView):
    model = Product
    template_name = 'shop-checkout.html'
    form_class = OrderForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = self.request.user
        product = form.save(commit=False)
        product.owner = user
        product.save()

        email = user
        text = f"Hello {product.first_name}, thank you for you order!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        to_email = email
        send_mail(
            'Subject here',
            text,
            'emirfortest@gmail.com',
            [to_email],
            fail_silently=False,
        )
        return super().form_valid(form)
