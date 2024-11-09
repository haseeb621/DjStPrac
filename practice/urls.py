from practice.views import *
from django.urls import path

urlpatterns = [
    path('', index , name='index' ),
    path('register', register , name='register' ),
    path('login', login , name='login' ),
    path('logout', logout , name='logout' ),
    path('payment', payment , name='payment' ),
    path('choose_plan', choose_plan , name='choose_plan' ),
    path('Home', Home , name='Home' ),
    path('buy_plan/<str:price_id>', buy_plan , name='buy_plan' ),
    path('subscription_failed', subscription_failed , name='subscription_failed' ),
]
