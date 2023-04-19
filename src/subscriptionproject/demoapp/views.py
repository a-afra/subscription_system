from django.shortcuts import render
from .models import SubscriptionPlan

# Create your views here.
def home(request):
    plans_data = SubscriptionPlan.objects.all()
    main_data = {"plans": plans_data}
    return render(request, 'index.html', main_data)

def about(request):
    return render(request, 'about.html')

def my_account(request):
    return render(request, 'my_account.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def display_plan_item(request, pk=None):
    if pk:
        plan_item = SubscriptionPlan.objects.get(pk=pk)
    else:
        plan_item = ''
    return render(request, 'plan_item.html', {"plan_item": plan_item})