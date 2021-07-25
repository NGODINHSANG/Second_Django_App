from account.decorators import unauthenticated_user
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from .models import *
from .forms import CustomerForm, OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import Group
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_only, allowed_users, unauthenticated_user

def registerPage(reponse):
    if reponse.user.is_authenticated:
	    return redirect('dashboard')
    else:
        form = CreateUserForm()
        if reponse.method == 'POST':
            form = CreateUserForm(reponse.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
            
                messages.success(reponse, 'Account was created for' + username)

                return redirect('login')

        context = {'form':form}
        return render(reponse, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(reponse):
    if reponse.method == 'POST':
        username = reponse.POST.get('username')
        password =reponse.POST.get('password')

        user = authenticate(reponse, username=username, password=password)

        if user is not None:
            login(reponse, user)
            return redirect('dashboard')
        else:
            messages.info(reponse, 'Username OR password is incorrect')

    context = {}
    return render(reponse, 'accounts/login.html', context)
def logoutUser(reponse):
    logout(reponse)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(reponse):

    orders = reponse.user.customer.order_set.all()
    total_or = orders.count()
    Delivered = orders.filter(status='Delivered').count()
    Pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'total_or':total_or, 'Delivered':Delivered, 'Pending':Pending}
    return render(reponse, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSetting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@admin_only
def dashboard(reponse):

    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_ct = customers.count()
    total_or = orders.count()
    Delivered = orders.filter(status='Delivered').count()
    Pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'customers':customers, 'total_ct':total_ct, 'total_or':total_or, 'Delivered':Delivered, 'Pending':Pending}
    return render(reponse, "accounts/dashboard.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(reponse, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(reponse.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(reponse, "accounts/customer.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(reponse):
    products = Product.objects.all()
    return render(reponse, "accounts/product.html", {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(reponse, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if reponse.method == 'POST':
        #form = OrderForm(reponse.POST)
        formset = OrderFormSet(reponse.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/dashboard')
    context = {'formset':formset}
    return render(reponse, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(reponse, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if reponse.method == 'POST':
        form = OrderForm(reponse.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context = {'form':form}
    return render(reponse, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(reponse, pk):
    order = Order.objects.get(id=pk)
    if reponse.method == 'POST':
        order.delete()
        return redirect('/dashboard')
    context = {'item':order}
    return render(reponse, 'accounts/delete.html', context)
