from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import*
from .models import *
from .utils import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import *
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard',request.user.id)
    else:
        return redirect('login')


def signup_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user  = authenticate(username=username,password=password)
            logged_user_id = User.objects.get(username=username)

            login(request,user)
            return redirect('dashboard', logged_user_id.id)
    contex = {
        'form':form,
    }
    return render(request,'accounts/signup.html',contex)

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect('dashboard',request.user.id)# Redirect to a success page.
    return render(request, 'accounts/login.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')  # redirect when user is not logged in
def dashboard(request, pk):
    # get weekday
    week_start,week_end = get_weeks()
    month_fday,month_lday = get_months()

    users = User.objects.get(username=request.user)
    orders_daily = users.ordermodel_set.filter(date_created__date=date.today()).order_by('-date_created')
    orders_weekly = users.ordermodel_set.filter(date_created__date__range=[
        week_start,week_end]).order_by('-date_created')
    orders_monthly = users.ordermodel_set.filter(date_created__date__range=[
        month_fday,month_lday]).order_by('-date_created')


    weekly_total_income = get_total(orders_weekly)
    monthly_total_income = get_total(orders_monthly)


    if request.method == "POST":
        form = orderForm(request.POST)
        form_record = form.save(commit=False)   #commit=False
        form_record.user = users

        if form.is_valid():
            form.save()
            return redirect('dashboard', pk)
    form = orderForm()
    contex = {
        'orders_daily': orders_daily,
        'form': form,
        'weekly': weekly_total_income,
        'monthly': monthly_total_income,
    }
    return render(request, 'accounts/dashboard.html', contex)

@login_required(login_url='login')
def delete_view(request,pk):
    users = User.objects.get(username=request.user)
    order = users.ordermodel_set.get(id = pk)
    order.delete()
    return redirect('dashboard',request.user.id)

@login_required(login_url='login')
def update_view(request,pk):
    users = User.objects.get(username=request.user)
    order = users.ordermodel_set.get(id = pk)
    form = orderForm(instance=order)
    if request.method == 'POST':
        form = orderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard',request.user.id)
    contex = {
        'form':form,
    }
    return render(request,'accounts/update.html',contex)

@login_required(login_url='login')
def orders_view(request,wm):
    users = User.objects.get(username=request.user)
    contex = {}

    if wm == 'weekly':
        week_start,week_end = get_weeks()
        orders= users.ordermodel_set.filter(date_created__date__range=[
            week_start,week_end]).order_by('-date_created')
        contex = {
            'orders': orders
        }

    if wm == 'monthly':
        month_fday,month_lday = get_months()

        orders = users.ordermodel_set.filter(date_created__date__range=[
        month_fday,month_lday]).order_by('-date_created')
        contex = {
            'orders': orders
        }
    return render(request,'accounts/orders_view.html',contex)

