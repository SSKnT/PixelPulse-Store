from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, Cart, Order
from django.contrib import messages

#Featured
class ProductListView(ListView):
    model = Product
    template_name = 'store/index.html'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.order_by('-date_posted')[:10]

#All Products
class AllProductListView(ListView):
    model =Product
    template_name = 'store/all.html'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.all()

#Budget Ballers 
class BudgetProductListView(ListView):
    model = Product
    template_name = 'store/budget.html'
    paginate_by = 12
    
    def get_queryset(self):
        return Product.objects.filter(price__lte=500)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'


class CartView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Cart
    template_name = 'store/cart.html'
    context_object_name = 'cart_items'
    
    def get_queryset(self):
        return Cart.objects.all().filter(user_id=self.request.user).select_related('product_id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']

        # Calculate the total price for all cart items
        total_price = sum(item.total_price() for item in cart_items)
        context['total_price'] = total_price
        return context

    def test_func(self):
        cart = Cart.objects.filter(user_id=self.request.user).first()
        if cart is None:
            return True
        else:
            return cart.user_id == self.request.user


@login_required
def Add_to_Cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        cart, created = Cart.objects.get_or_create(product_id=product, user_id=request.user, defaults={'quantity': 1})
        if not created:
            
            cart.quantity += 1
            cart.save()
        messages.success(request, f'{product.product_name} added to cart')
        return redirect('cart')
    else:
        return render(request, 'store/index.html')

# create button for cart removal
@login_required
def Remove_from_Cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        cart = Cart.objects.get(product_id=product, user_id=request.user)
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()
        return redirect('cart')
    else:
        return redirect('product-list')

@login_required
def confirm_order(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user_id=request.user)
        if cart_items.exists():
            order = Order.objects.create(user_id=request.user)
            product_ids = cart_items.values_list('product_id', flat=True)
            products = Product.objects.filter(pk__in=product_ids)
            order.product_ids.add(*products)
            
            # Populate product quantities dictionary
            product_quantities = {}
            for cart_item in cart_items:
                product_quantities[cart_item.product_id.id] = cart_item.quantity
            order.product_quantities = product_quantities
            
            order.total_price = sum(item.total_price() for item in cart_items)
            order.total_quantity = sum(item.quantity for item in cart_items)
            order.save()
            cart_items.delete()
            return redirect('order-list', pk=order.id)
    return redirect('product-list')


class OrderView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Order
    template_name = 'store/checkout.html'
    context_object_name = 'order'
    
    def test_func(self):
        order = Order.objects.filter(user_id=self.request.user).first()

        if order is not None and order.user_id == self.request.user:
            return True
        else:
            return False
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = context['order']
        context['order_paid'] = order.status == 'P'
        return context

    
class SearchView(ListView):
    model = Product
    template_name = 'store/search.html'
    paginate_by = 12
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = Product.objects.all()
        search_query = self.request.GET.get('query')
        category = self.request.GET.get('category')

        if search_query:
            queryset = queryset.filter(product_name__icontains=search_query)
        
        if category:
            queryset = queryset.filter(category=category)

        return queryset


    
def about_view(request):
    return render(request, 'store/base.html')

class MyOrderView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = 'store/my_order.html'
    context_object_name = 'orders'

    def test_func(self):
        order = Order.objects.filter(user_id=self.request.user).first()

        if order is not None and order.user_id == self.request.user:
            return True
        else:
            return False

# cd Desktop\Django\DJ-2(store)
# vir_env_2\Scripts\activate






