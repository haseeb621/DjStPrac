from functools import wraps
from django.shortcuts import redirect
from djstripe.models import Customer,APIKey,Subscription
import stripe
from django.contrib import messages

def plan_required(view_func):

  @wraps(view_func)
  def _wrap_view(request, *args, **kwargs):
      user = request.user
      email1 = user.email
      stripe_customer = stripe.Customer.list(email=email1)
      if not stripe_customer:
          messages.error(request, "No user found")
          return redirect('login')
      stripe_customer=stripe_customer['data'][0]
      customer_id=stripe_customer['id']
      subscriptions = stripe.Subscription.list(customer=customer_id)
      has_active_subscription = any(
       sub.status in ["active", "trialing"] for sub in subscriptions['data']
      )
      if has_active_subscription:
          return view_func(request, *args, **kwargs)
      else:
          messages.error(request, "Subscription has expired!")
          return redirect('choose_plan')  

  return _wrap_view
