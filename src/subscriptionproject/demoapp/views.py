from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SubscriptionPlan, Subscription, Invoice, Customer
from .forms import SignupForm, LoginForm
from django.db.models import Sum
from django.utils import timezone


def home(request):
    """
    Render the home page.
    """
    return render(request, 'index.html')


def about(request):
    """
    Render the about page.
    """
    return render(request, 'about.html')


@login_required
def my_account(request):
    """
    Render the user's account page, showing their subscriptions and invoices.
    """
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
    """
    Handle user login.

    If the user submits a valid form, authenticate the user and redirect to their account page.
    Otherwise, render the login form.
    """
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
    """
    Handle user registration.

    If the user submits a valid form, create a new user account, log the user in, and redirect to their account page.
    Otherwise, render the registration form.
    """
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
    """
    Log the user out and redirect to the login page.
    """
    logout(request)
    return redirect('login')


def display_plan_item(request, pk=None):
    """
    Render the page for a specific subscription plan.

    If the plan PK is provided in the URL, show the plan.
    """
    if pk:
        plan_item = SubscriptionPlan.objects.get(pk=pk)
    else:
        plan_item = ''
    return render(request, 'plan_item.html', {"plan_item": plan_item})


def subscribe(request, pk=None):
    """
    Handle new subscriptions.

    If the user is already subscribed to this plan, show an error message and redirect to the plan page.
    Otherwise, create a new subscription and invoice, and redirect to the user's account page.
    """
    plan = SubscriptionPlan.objects.get(pk=pk)
    customer = request.user
    current_time = timezone.now()

    if request.method == 'POST':
        if Subscription.objects.filter(customer=customer, plan=plan, is_active=True).exists():
            messages.error(request, 'You already have an active subscription for this plan.')
            return redirect('plan_item', pk=pk)

        subscription = Subscription.objects.create(
            customer = customer,
            plan = plan,
            is_active = True,
        )

        invoice = Invoice.objects.create(
            start_date = current_time,
            end_date = current_time + timezone.timedelta(minutes=10),
            subscription = subscription,
            amount = subscription.plan.price
        )

        return redirect('my_account')


@login_required
def my_statistics(request):
    """
    Handle customer statistics.

    Fetches all subscriptions associated with the current user and calculates
    the total number of invoices and spending per plan.
    The results are returned in the dictionary.
    """
    subscriptions = Subscription.objects.filter(customer=request.user)
    total_invoices = 0
    total_spending = 0
    context = {}

    # Iterate over all subscriptions associated with the user
    for subscription in subscriptions:
        invoices = Invoice.objects.filter(subscription=subscription)
        invoices_quantity = invoices.count()

        # If the subscription has any invoices
        if invoices_quantity != 0:
            total_invoices += invoices_quantity

            # Calculate the total spending for the subscription
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
    """
    View function for displaying a list of subscription plans.
    """
    plans_data = SubscriptionPlan.objects.all()
    main_data = {"plans": plans_data}
    return render(request, 'plans.html', main_data)


def change_subscription_status(request, pk=None):
    """
    Change the active status of a subscription.
    """
    subscription = Subscription.objects.get(pk=pk)
    if request.method == 'POST':
        subscription.is_active = not subscription.is_active
        subscription.save()
        messages.success(request, 'Subscription status updated successfully!')
        return redirect('my_account')


@login_required
def refresh_invoices(request):
    """
    Refreshes the invoices of the user's active subscriptions by creating new invoices if necessary.
    """
    user = request.user
    subscriptions = Subscription.objects.filter(customer=user)
    # Define the time period for generating new invoices
    period = 600

    for subscription in subscriptions:
        if subscription.is_active:
            latest_invoice = Invoice.objects.filter(subscription=subscription).order_by('-end_date').first()

            if latest_invoice:
                current_time = timezone.now()
                # Generate new invoices until the current time
                while latest_invoice and latest_invoice.end_date < current_time:
                    start_date = latest_invoice.end_date
                    end_date = start_date + timezone.timedelta(seconds=period)
                    # Create a new invoice with the next period
                    new_invoice = Invoice.objects.create(
                        start_date=start_date,
                        end_date=end_date,
                        subscription=subscription,
                        amount=subscription.plan.price
                    )
                    # Update the latest invoice to the new invoice
                    latest_invoice = new_invoice

                return redirect('my_account')

            return redirect('my_account')
