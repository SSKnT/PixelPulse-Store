from django.urls import path
from .views import ( ProductListView, ProductDetailView, CartView, Add_to_Cart, Remove_from_Cart,
 confirm_order, OrderView, AllProductListView, BudgetProductListView, SearchView, about_view, MyOrderView)    

urlpatterns = [
    path('',ProductListView.as_view(),name='product-list'),
    path('about/',about_view, name='about'),
    path('all/',AllProductListView.as_view(),name='all-product-list'),
    path('budget/',BudgetProductListView.as_view(),name='budget-product-list'),
    path('detail/<int:pk>/',ProductDetailView.as_view(),name='product-detail'),
    path('cart/',CartView.as_view(),name='cart'),
    path('add-to-cart/<int:product_id>/',Add_to_Cart,name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/',Remove_from_Cart,name='remove-from-cart'),
    path('confirm-order',confirm_order,name='confirm-order'),
    path('order/<int:pk>',OrderView.as_view(),name='order-list'),
    path('search/',SearchView.as_view(),name='search'),
    path('my_order/',MyOrderView.as_view(),name='my-order'),
]