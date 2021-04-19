from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
import datetime
import xlwt
import csv

#from django.template.loader import render_to_string
#import tempfile
#from weasyprint import HTML
#from django.db.models import Sum

# Create your views here.

@login_required(login_url='/authentication/login')
def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)

        data = expenses.values()

        return JsonResponse(list(data),safe=False)




@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    currency = UserPreference.objects.get(user=request.user).currency

    contexts = {
        'expenses' : expenses,
        'page_obj' : page_obj,
        'currency' : currency
    }

    return render(request,'expenses/index.html', contexts)

@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()

    contexts = {
        'categories' : categories,
        'values': request.POST
    }
    if request.method == "GET":
        return render(request, 'expenses/add_expense.html',contexts)

    if request.method == "POST":
        amount = request.POST['amount']

        if not amount:
            messages.error(request, "Amount is Required")
            return render(request, 'expenses/add_expense.html',contexts)

        description = request.POST['description']

        if not description:
            messages.error(request, "Description is Required")
            return render(request, 'expenses/add_expense.html',contexts)

        category = request.POST['category']

        if not category:
            messages.error(request, "Category is Required")
            return render(request, 'expenses/add_expense.html',contexts)

        date = request.POST['expense_date']

        if not date:
            messages.error(request, "Date is Required")
            return render(request, 'expenses/add_expense.html',contexts)

        Expense.objects.create(owner=request.user,amount=amount,description=description,category=category,date=date)
        messages.success(request, "Expense Saved Successfully")

        return redirect('expenses')

@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()

    contexts = {
        'expense' : expense,
        'values' : expense,
        'categories' : categories
    }

    if request.method == "GET":
        return render(request, 'expenses/edit-expense.html',contexts)

    if request.method == "POST":
        amount = request.POST['amount']

        if not amount:
            messages.error(request, "Amount is Required")
            return render(request, 'expenses/edit-expense.html',contexts)

        description = request.POST['description']

        if not description:
            messages.error(request, "Description is Required")
            return render(request, 'expenses/edit-expense.html',contexts)

        category = request.POST['category']

        if not category:
            messages.error(request, "Category is Required")
            return render(request, 'expenses/edit-expense.html',contexts)

        date = request.POST['expense_date']

        if not date:
            messages.error(request, "Date is Required")
            return render(request, 'expenses/edit-expense.html',contexts)

        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date

        expense.save()
        messages.success(request, "Expenses Have Been Edited Successfully")


        return redirect('expenses')

@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense Has Deleted Successfully")
    return redirect('expenses')
    

def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')



def export_csv(request):

    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename = Expenses' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category','Date'])

    expenses = Expense.objects.filter(owner = request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response

def export_excel(request):

    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Expenses' + str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold= True

    columns = ['Amount', 'Description', 'Category','Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner = request.user).values_list('amount', 'description', 'category','date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


#def export_pdf(request):

    #response = HttpResponse(content_type = 'application/pdf')
    #response['Content-Disposition'] = 'attachment; filename = Expenses' + str(datetime.datetime.now()) + '.pdf'

    #response['content-Transfer-Encoding'] = 'binary'

    #html_string = render_to_string('expenses/pdf-output.html',{'expenses': [], 'total': 0})
    #html = HTML(string=html_string)

    #result = html.write_pdf()

    #with tempfile.NamedTemporaryFile(delete=True) as ouput:
        #output.write(result)
        #output.flush()

        #ouput = open(ouput.name,'rb')
        #response.write(output.read())

    #return response


