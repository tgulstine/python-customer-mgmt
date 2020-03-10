from django.http import HttpResponse 
from django.template import Context, loader
from django.shortcuts import render
from django.template.loader import render_to_string, get_template

def home(request):
    return render(request, 'find_person.html', { "Name": "Tim Gulstine"})

def get(request):
    name = request.GET['Name']
    html = render_to_string('get_result.html', { 'Name': name })
    return HttpResponse(html)

def post(request):
    name = request.POST['Name']
    html = render_to_string('post_result.html', { 'Name': name })
    return HttpResponse(html)
    
def displayOrder(request):
    items = [ 
                { 'ItemName': 'Patio Table', 'ItemPrice': 129.99 },
                { 'ItemName': 'Plates - Set of 8', 'ItemPrice': 79.99 }
            ]
    orderContext = { 'Name': 'Bob Hill', 'Address': '123 Elm', 'City': 'New York City', 'StateProvince': 'NY', 'Items': items }
    return render(request,'display_order.html', orderContext)
