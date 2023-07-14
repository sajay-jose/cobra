from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import bank
from .forms import LoginForm

# Create your views here.


def display(request):
    return render(request, 'home.html')

def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['Ac_no']
            password = form.cleaned_data['password']
            user = bank.objects.get(Ac_no=account_number)
            if user.password == password:
            # user = authenticate(request, Ac_no=account_number, password=password)
                print(user)
                if user is not None:
                    # login user
                    login(request, user)
                    request.session['id'] = account_number
                    return redirect('display')
                else:
                    # show error message
                    return render(request, 'my_login.html', {'return': "Invalid login"})
    else:
        form = LoginForm
        return render(request, 'my_login.html', {'form': form})

def reg(request):
    if request.method == 'POST':
        account_number = int(request.POST['account_number'])
        password = request.POST['password']
        name = request.POST['name']
        amount = int(request.POST['amount'])
        phone = int(request.POST['phone'])
        if amount < 1000:
            return render(request, 'register.html',{'return':"Amount should be greater than or equal to 1000"})
        try:
            data = bank.objects.create(Ac_no=account_number, password=password, name=name, amount=amount, phone=phone)
            data.save()

            return render(request, 'my_login.html',{'return':"Your account has been created."})
        except Exception:
            return render(request, 'register.html',{'return':"Account number already exists."})
    else:
        return render(request,'register.html')

def balance(request):
    account_number = request.session['id']
    if request.method == 'POST':
        account_number = request.POST['account_number']
        try:
            data = bank.objects.get(Ac_no=account_number)
            return render(request, 'home.html', {'return': data.amount})
        except Exception:
            return HttpResponse(" error")
    else:
        return render(request,'home.html')


def deposite(request):
    account_number = request.session['id']
    if request.method == "POST":
        deposit_amount = int(request.POST['deposit_amount'])
        try:
          data = bank.objects.get(Ac_no=account_number)
          data.amount += deposit_amount
          data.save()
          return render(request, 'home.html',{'return': 'your amount '+str(deposit_amount)+' has deposited'})
        except Exception as e:
            return HttpResponse("Error: {}".format(str(e)))

def withdraw(request):
    account_number = request.session['id']
    if request.method == "POST":
        withdraw_amount = int(request.POST['withdraw_amount'])
        if withdraw_amount % 100 != 0 and withdraw_amount % 200 != 0 and withdraw_amount % 500 != 0:
            return render(request, 'home.html',{'return': 'Invalid amount. Withdraw amount should be multiple of 100,200,500'})
        try:
          data = bank.objects.get(Ac_no=account_number)
          data.amount -= withdraw_amount
          data.save()
          return render(request, 'home.html',{'return': 'your amount '+str(withdraw_amount)+' has been withdrawn'})
        except Exception as e:
            return HttpResponse("Error: {}".format(str(e)))