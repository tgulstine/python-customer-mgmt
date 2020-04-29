import sqlite3
import os

from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.core.validators import RegexValidator
from django.core.files.storage import FileSystemStorage

class CustomerForm(forms.Form):
    name = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    states = [('', 'Please Select'),('AL','Alabama'),('AK','Alaska'),('AZ','Arizona'),('IL','Illinois'),('ONT','Ontario')]
    state_province = forms.ChoiceField(choices=states, label="State/Province")      
    is_tax_exempt= forms.BooleanField(label="Tax Exempt")
    paymentTerms = [('NET15','NET 15 '),('NET30','NET 30 '),('NET60','NET 60 ')]
    payment_terms = forms.ChoiceField(choices=paymentTerms,widget=forms.RadioSelect)
    location = forms.FileField(required=False)

def manageCustomersWithValidation(request):
    if request.method == 'GET':
        form = CustomerForm()
    else:
        form = CustomerForm(request.POST)
        if form.is_valid():
            uploadExists = request.FILES.get('location', False)    
            if uploadExists:
                uploadedFile = request.FILES['location']    
                fs = FileSystemStorage()
                filename = fs.save(uploadedFile.name, uploadedFile)
            addCustomer(request)
            form = CustomerForm()

    customers = getAllCustomers()

    return render(request, 'manage_customers_with_validation.html', { 'form': form, 'customers': customers  })

def addCustomer(request):
    baseDirectory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dbPath = os.path.join(baseDirectory, 'db.sqlite3')
    connection = sqlite3.connect(dbPath) 

    with connection:
        dbCursor = connection.cursor()
 
        sql = "INSERT INTO customers " + \
                "(name, address, city, state_province, payment_terms, is_tax_exempt, location) " + \
                    " VALUES (?, ?, ?, ?, ?, ?, ?)"

        is_tax_exempt = request.POST.get('is_tax_exempt', 0)
        is_tax_exempt = 1 if is_tax_exempt == 'on' else 0
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state_province = request.POST.get('state_province', '')
        payment_terms = request.POST.get('payment_terms', '')
        location = request.POST.get('location', '')
 
        
        values = (name, address, city, state_province, 
                    payment_terms, is_tax_exempt, location)        
        dbCursor.execute(sql, values)

def manageCustomers(request):
    context = getAllCustomers()
    return render(request, 'manage_customers.html', { 'Customers' : context } )

def getCustomers(request):
    context = getAllCustomers()
    return render(request, 'display_customers.html', context)

def getAllCustomers():
    baseDirectory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dbPath = os.path.join(baseDirectory, 'db.sqlite3')
    connection = sqlite3.connect(dbPath) 

    with connection:
        dbCursor = connection.cursor()
        dbCursor.execute("SELECT * FROM customers")
        rows = dbCursor.fetchall()

        customers = []
        context = {}

        for row in rows:
            customers.append({ 'Id': row[0], 'Name' : row[1], 'Address' : row[2], 'City': row[3], 'StateProvince': row[4],
                                'PaymentTerms': row[5], 'TaxExempt': row[6], 'Location':  row[7] })

        return customers
