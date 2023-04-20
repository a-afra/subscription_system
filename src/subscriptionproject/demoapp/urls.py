from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('my_account/', views.my_account, name="my_account"),
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/signup/', views.signup_view, name="signup"),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('plan_item/<int:pk>', views.display_plan_item, name="plan_item"),
    path('subscribe/<int:pk>', views.subscribe, name="subscribe"),
    path('my-statistics/', views.my_statistics, name='my_statistics'),
    path('plans/', views.plans, name='plans'),
    path('change_subscription_status/<int:pk>/', views.change_subscription_status, name='change_subscription_status'),
    path('refresh_invoices/<int:pk>/', views.refresh_invoices, name='refresh_invoices'),
]