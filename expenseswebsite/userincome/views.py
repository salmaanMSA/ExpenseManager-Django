from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
# Create your views here.

@login_required(login_url='/authentication/login')
def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')

        income = UserIncome.objects.filter(amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)

        data = income.values()

        return JsonResponse(list(data),safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income,2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    currency = UserPreference.objects.get(user=request.user).currency

    contexts = {
        'income' : income,
        'page_obj' : page_obj,
        'currency' : currency
    }

    return render(request,'income/index.html', contexts)

def add_income(request):
    sources = Source.objects.all()

    contexts = {
        'sources' : sources,
        'values': request.POST
    }
    if request.method == "GET":
        return render(request, 'income/add_income.html',contexts)

    if request.method == "POST":
        amount = request.POST['amount']

        if not amount:
            messages.error(request, "Amount is Required")
            return render(request, 'income/add_income.html',contexts)

        description = request.POST['description']

        if not description:
            messages.error(request, "Description is Required")
            return render(request, 'income/add_income.html',contexts)

        source = request.POST['source']

        if not source:
            messages.error(request, "Source is Required")
            return render(request, 'income/add_income.html',contexts)

        date = request.POST['income_date']

        if not date:
            messages.error(request, "Date is Required")
            return render(request, 'income/add_income.html',contexts)

        UserIncome.objects.create(owner=request.user,amount=amount,description=description,source=source,date=date)
        messages.success(request, "Income Saved Successfully")

        return redirect('income')

@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()

    contexts = {
        'income' : income,
        'values' : income,
        'sources' : sources
    }

    if request.method == "GET":
        return render(request, 'income/edit_income.html',contexts)

    if request.method == "POST":
        amount = request.POST['amount']

        if not amount:
            messages.error(request, "Amount is Required")
            return render(request, 'income/edit_income.html',contexts)

        description = request.POST['description']

        if not description:
            messages.error(request, "Description is Required")
            return render(request, 'income/edit_income.html',contexts)

        source = request.POST['source']

        if not source:
            messages.error(request, "Source is Required")
            return render(request, 'income/edit_income.html',contexts)

        date = request.POST['income_date']

        if not date:
            messages.error(request, "Date is Required")
            return render(request, 'income/edit_income.html',contexts)

        income.owner = request.user
        income.amount = amount
        income.description = description
        income.source = source
        income.date = date

        income.save()
        messages.success(request, "Income Have Been Edited Successfully")


        return redirect('income')

@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income Has Deleted Successfully")
    return redirect('income')