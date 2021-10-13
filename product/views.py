from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from django.db.models import Q

from accounts.models import CustomUser
from product.forms import ProductForm, CategoryForm, ContactForm
from product.models import Product, Category, Like, Contact
from django.utils import timezone
from datetime import timedelta

from product.services import send
from .tasks import send_spam_email



class ProductCreate(CreateView):
    model = Product
    template_name = 'add_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = self.request.user
        product = form.save(commit=False)
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductDelete(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('index')


class CategoryCreate(CreateView):
    model = Category
    template_name = 'add_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('index')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.id = kwargs.get('pk', None)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category_id=self.id)
        return context

    def form_valid(self, form):

        user = self.request.user
        product = form.save(commit=False)
        product.user = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'add_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('index')

PAGE = 0

class ProductList(ListView):
    model = Product
    template_name = 'index.html'
    paginate_by = 3
    context_object_name = 'products'

    def get_template_names(self):
        template_name = super(ProductList, self).get_template_names()
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')

        if search:
            template_name = 'search.html'
        elif filter:
            template_name = 'new_product.html'
        return template_name

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        global PAGE
        PAGE = context.get(("page_obj")).number
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        context['is_empty'] = False

        if search:
            context['products'] = Product.objects.filter(Q(title__icontains=search)|
                                                       Q(descriptions__icontains=search))
        elif filter:
            start_date = timezone.now() - timedelta(days=1)
            context['products'] = Product.objects.filter(created_at__gte=start_date)

        if context.get('products'):
            for id, product in enumerate(context.get('products')):
                product.is_liked = False
                try:
                    for like in product.likes.filter(product_id=product.id):
                        if like.owner == self.request.user:
                            product.is_liked = True
                        else:
                            continue
                except AttributeError:
                    continue
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context



class AddLikeView(ListView):
    model = Like
    template_name = 'index.html'
    pk_url_kwarg = 'id'
    paginate_by = 3

    def create_like(self):
        user_id = self.request.user.id
        user = CustomUser.objects.get(id=user_id)
        product_id = self.request.get_raw_uri().split('/')[-2]
        product = Product.objects.get(id=int(product_id))
        like = Like.objects.create(owner=user, product=product)
        Product.objects.filter(id=int(product_id)).update(like_id = like.id)


    def get(self, *args, **kwargs):
        self.create_like()
        if PAGE and PAGE != 1:
            return redirect(reverse_lazy("index") + f"?page={PAGE}")
        return redirect(reverse_lazy('index'))


class DeleteLikeView(DeleteView):
    model = Like
    template_name = 'index.html'
    pk_url_kwarg = 'like_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.product.is_liked = False
        self.object.delete()

    def get(self, *args, **kwargs):
        self.delete(self.request, *args, **kwargs)
        if PAGE and PAGE != 1:
            return redirect(reverse_lazy("index") + f"?page={PAGE}")
        return redirect(reverse_lazy('index'))

from cart.forms import CartAddProductForm
from django.shortcuts import render, get_object_or_404

# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'product_detail.html'
#     cart_product_form = CartAddProductForm()
#     context_object_name = 'product'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(context)
#         return context

def ProductDetailView(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_product_form = CartAddProductForm()
    return render(request, 'product_detail.html', {'product': product, 'cart_product_form': cart_product_form})


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    template_name = 'main/contact.html'

    def form_valid(self, form):
        form.save()
        # send(form.instance.email)
        send_spam_email.delay(form.instance.email)
        return super().form_valid(form)

