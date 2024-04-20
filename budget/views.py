import csv
from django.shortcuts import render
from .models import Transaction, Category
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from decimal import Decimal as decimal


# Create your views here.
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if csv_file:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                transaction = Transaction(
                    date = datetime.strptime(row['Posting Date'], '%m/%d/%Y').date(),
                    description = row['Description'],
                    amount = (decimal(row['Amount']) * -1),
                )
                transaction.save()
            return HttpResponseRedirect(reverse('budget:upload_csv'))
    return render(request, 'budget/upload_csv.html')