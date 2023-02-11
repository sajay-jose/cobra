from django.shortcuts import render
from django.http import HttpResponse
from .models import bank

# Create your views here.


def display(request):
    return render(request, 'home.html')


def reg(request):
    if request.method == 'POST':
        account_number = int(request.POST['account_number'])
        name = request.POST['name']
        amount = int(request.POST['amount'])
        phone = int(request.POST['phone'])
        if amount < 1000:
            return render(request, 'home.html',{'return':"Amount should be greater than or equal to 1000"})
        try:
          data = bank.objects.create(
              Ac_no=account_number, name=name, amount=amount, phone=phone)
          data.save()
          return render(request, 'home.html',{'return':"Your account has been created."})
        except Exception:
          return render(request, 'home.html',{'return':"Account number already exists."})
    else:
        return render(request,'home.html')

def balance(request):
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
    if request.method == "POST":
        account_number = request.POST['Ac_no']
        deposit_amount = int(request.POST['deposit_amount'])
        try:
          data = bank.objects.get(Ac_no=account_number)
          data.amount += deposit_amount
          data.save()
          return render(request, 'home.html',{'return': 'your amount '+str(deposit_amount)+' has deposited'})
        except Exception as e:
            return HttpResponse("Error: {}".format(str(e)))

def withdraw(request):
    if request.method == "POST":
        account_number = request.POST['Ac_no']
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