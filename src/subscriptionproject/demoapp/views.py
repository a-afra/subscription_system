from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import SubscriptionPlan
from .forms import SignupForm, LoginForm

# Create your views here.
def home(request):
    plans_data = SubscriptionPlan.objects.all()
    main_data = {"plans": plans_data}
    return render(request, 'index.html', main_data)

def about(request):
    return render(request, 'about.html')

@login_required
def my_account(request):
    return render(request, 'my_account.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            customer = authenticate(request, username=username, password=password)

            if customer is not None:
                login(request, customer)
                return redirect('my_account')

    elif request.method == 'GET':
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('my_account')
    elif request.method == 'GET':
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def display_plan_item(request, pk=None):
    if pk:
        plan_item = SubscriptionPlan.objects.get(pk=pk)
    else:
        plan_item = ''
    return render(request, 'plan_item.html', {"plan_item": plan_item})