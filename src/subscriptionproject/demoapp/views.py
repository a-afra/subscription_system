from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SubscriptionPlan, Subscription, Invoice
from .forms import SignupForm, LoginForm
from django.db.models import Sum

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def my_account(request):
    user = request.user
    subscriptions = Subscription.objects.filter(customer=user)
    invoices = Invoice.objects.filter(subscription__customer=user)
    context = {
        'user': user,
        'subscriptions': subscriptions,
        'invoices': invoices
    }
    return render(request, 'my_account.html', context)

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


def subscribe(request, pk=None):
    plan = SubscriptionPlan.objects.get(pk=pk)
    customer = request.user

    if request.method == 'POST':
        if Subscription.objects.filter(customer=customer, plan=plan, is_active=True).exists():
            messages.error(request, 'You already have an active subscription for this plan.')
            return redirect('plan_item', pk=pk)

        subscription = Subscription.objects.create(
            customer = customer,
            plan = plan,
            is_active = True,
        )
        invoice = Invoice()
        invoice.subscription = subscription
        invoice.save()
        return redirect('my_account')


@login_required
def my_statistics(request):
    subscriptions = Subscription.objects.filter(customer=request.user)
    total_invoices = 0
    total_spending = 0
    context = {}
    for subscription in subscriptions:
        invoices = Invoice.objects.filter(subscription=subscription)
        invoices_quantity = invoices.count()
        if invoices_quantity != 0:
            total_invoices += invoices_quantity
            cost_per_plan = invoices.aggregate(Sum('amount'))['amount__sum']
            if cost_per_plan is not None:
                total_spending += cost_per_plan
            context[subscription.plan.name] = {
                'invoices_quantity': invoices_quantity,
                'cost_per_plan': cost_per_plan
                }

    total = {
        'total_invoices': total_invoices,
        'total_spending': total_spending
    }

    return render(request, 'my_statistics.html', {'statistics': context, 'total': total})


def plans(request):
    plans_data = SubscriptionPlan.objects.all()
    main_data = {"plans": plans_data}
    return render(request, 'plans.html', main_data)


def change_subscription_status(request, pk=None):
    subscription = Subscription.objects.get(pk=pk)
    if request.method == 'POST':
        subscription.is_active = not subscription.is_active
        subscription.save()
        messages.success(request, 'Subscription status updated successfully!')
        return redirect('my_account')