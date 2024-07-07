from django.urls import path
from .views import CreateCheckoutSessionView, SuccessView, CancelView,  stripe_webhook


urlpatterns = [
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('webhook/stripe/', stripe_webhook, name='stripe-webhook'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
]