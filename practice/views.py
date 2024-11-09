from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
import stripe
from djstripe.models import Customer, APIKey
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .decorator import *

key = APIKey.objects.filter(livemode=False).first()
stripe.api_key = key.secret

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request, "Passwords don't match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=pass1)
        user.save()
        auth_login(request,user)
        return redirect('payment')
        
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username1 = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = authenticate(username=username1, password=pass1)
        if user is not None:
            auth_login(request, user)
            return redirect('Home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')

def payment(request):
    return render(request, 'payment.html')

def choose_plan(request):
    try:
        products = stripe.Product.list()
        plan_data = []
        for product in products['data']:
            price = stripe.Price.retrieve(product["default_price"])
            plan_data.append({
                'name': product["name"],
                'description': product["description"],
                'price': price.unit_amount / 100,
                'currency': price.currency.upper(),
                'interval': price.recurring.interval if price.recurring else "one-time",
                'plan_duration': "monthly" if price.recurring.interval == "month" else "yearly",
                'price_id': product["default_price"]
            })
        return render(request, 'choose_plan.html', {'plans': plan_data})

    except stripe.error.StripeError as e:
        return render(request, 'error.html', {'error': str(e)})

def buy_plan(request, price_id):
    user = request.user
    print(user)
    user_email = user.email
    print(user_email)
    try:
        stripe_customer = Customer.objects.get(subscriber=user)
    except Customer.DoesNotExist:
        stripe_customer = stripe.Customer.create(email=user_email)
        Customer.sync_from_stripe_data(stripe_customer)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            customer=stripe_customer.id,
            line_items=[{'price': price_id, 'quantity': 1}],
            success_url=request.build_absolute_uri(reverse('Home')),
            cancel_url=request.build_absolute_uri(reverse('subscription_failed')),
        )
        return redirect(checkout_session.url)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def subscription_failed(request):
    return render(request, 'subscription_failed.html')

def logout(request):
    auth_logout(request)
    return redirect('index')
@plan_required
def Home(request):
  return render(request,'home.html')

