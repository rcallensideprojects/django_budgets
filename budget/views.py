import csv
from django.shortcuts import render
from .models import Transaction, Category
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from decimal import Decimal as decimal
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import redirect
from collections import defaultdict


# Create your views here.
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if csv_file:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                hash_id = hash(''.join([row['Posting Date'], row['Description'], row['Amount']]))
                transaction = Transaction.objects.get_or_create(
                    date = datetime.strptime(row['Posting Date'], '%m/%d/%Y').date(),
                    description = row['Description'],
                    amount = (decimal(row['Amount']) * -1),
                    hash = hash_id
                )
                
            return HttpResponseRedirect(reverse('budget:index'))
    return render(request, 'budget/upload_csv.html')


def transactions_filtered(request, month, category):
    month = datetime.strptime(month, '%B %Y')
    if category == 'All':
        transactions = Transaction.objects.filter(date__month=month.month, date__year=month.year).order_by('-category', 'date', 'amount')
    elif category == 'None':
        transactions = Transaction.objects.filter(category=None, date__month=month.month, date__year=month.year).order_by('-date', '-amount')
    else:
        categories = Category.objects.filter(name=category)
        transactions = Transaction.objects.filter(category__in=categories, date__month=month.month, date__year=month.year).order_by('-date', '-amount')
    categories = Category.objects.all()
    return render(request, 'budget/transactions.html', {'transactions': transactions, 'categories': categories})

def create_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = Category(name=name)
        if 'order' in request.POST:
            category.order = request.POST['order']
        category.save()
        return HttpResponseRedirect(reverse('budget:transactions'))
    return render(request, 'budget/create_category.html')

def index(request):
    kpis = {}
    months_in_transactions = Transaction.objects.annotate(
        month=TruncMonth('date')
    ).values('month', 'category__name').annotate(
        total=Sum('amount')
    ).order_by('-month', 'category__order')
    # print(months_in_transactions)
    for item in months_in_transactions:
        month_name = item['month'].strftime('%B %Y')
        category = item['category__name']
        total = item['total']
        if month_name not in kpis:
            kpis[month_name] = {}
            kpis[month_name]['Total'] = 0
        if category not in kpis[month_name]:
            kpis[month_name][category] = total
            kpis[month_name]['Total'] += total
        else:
            kpis[month_name][category] += total
        if category == 'Income':
            kpis[month_name][category] *= -1
 
    return render(request, 'budget/index.html', {'kpis': kpis})


def update_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    if request.method == 'POST':
        category_id = request.POST['category_id']
        category = Category.objects.get(id=category_id)
        transaction.category = category
        transaction.note = request.POST['note']
        transaction.save()
        return redirect(request.META['HTTP_REFERER'])
    return redirect(request.META['HTTP_REFERER'])

def category_index(request):
    categories = Category.objects.all().order_by('order')
    return render(request, 'budget/category_index.html', {'categories': categories})

def update_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.order = request.POST['order']
        category.save()
        return redirect(request.META['HTTP_REFERER'])
    return redirect(request.META['HTTP_REFERER'])

def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect(request.META['HTTP_REFERER'])
