import stripe
from django.views import View
from store.models import Order
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://localhost:8000"
        
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        
        products = order.product_ids.all()

        line_items = []
        for product in products:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.product_name,
                    },
                    'unit_amount': int(product.price * 100),  # Stripe requires the amount in cents
                },
                'quantity': order.product_quantities.get(str(product.id)), 
            })

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
                client_reference_id=order_id,  # Pass the order ID
            )
            # Redirect the user to the Stripe Checkout page
            return redirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'success.html')

class CancelView(View):
    def get(self, request, *args, **kwargs):
        return render(request, '/cancel.html')

stripe.api_key = settings.STRIPE_SECRET_KEY



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase, e.g., update order status
        order_id = session['client_reference_id']
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'P'  # Mark order as Paid
            order.save()
        except Order.DoesNotExist:
            return HttpResponse(status=404)
    if event['type'] == 'checkout.session.expired':
        session = event['data']['object']

        # Fulfill the purchase, e.g., update order status
        order_id = session['client_reference_id']
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'F'  # Mark order as Failed
            order.save()
        except Order.DoesNotExist:
            return HttpResponse(status=404)


    return HttpResponse(status=200)