from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',index,name="expenses"),
    path('add-expense',add_expense,name="add-expense"),
    path('edit-expense/<int:id>',expense_edit,name="expense-edit"),
    path('expense-delete/<int:id>',delete_expense,name="expense-delete"),
    path('search-expenses',csrf_exempt(search_expenses),name="search-expenses"),
    path('expense_category_summary', expense_category_summary, name="expense_category_summary"),
    path('stats', stats_view , name="stats"),
    path('export_csv', export_csv , name="export-csv"),
    path('export_excel', export_excel , name="export-excel"),
    #path('export_pdf', export_pdf , name="export-pdf")
]
