# from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import BookingForm, OrderForm
from .models import Menu
from django.core import serializers
from .models import Booking, Order_Transection, Location,Supplier,Customer, Item
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

# for login
def custom_login(request):
    return LoginView.as_view()(request)

def custom_logout(request):
    logout(request)
    context = {
        'message': 'You have been logged out successfully.'  # Example message
    }
    return render(request, 'registration/logout_page.html', context)



# Create your views here.
def bookings(request):
    data = json.load(request)
    exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
        reservation_slot = data['reservation_slot'].exists())
    if not exist :
        first_name = data['first_name']
        reservation_date = data['reservation_date']
        reservation_slot = data['reservation_slot']
    else:
        return HttpResponse({'error': 1}, content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)
    return HttpResponse(booking_json, content_type='application/json')


def home(request):
    return render(request, 'index.html')

def orderitem(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'orderitem.html', context)

def orderitemviews(request):

    dropdownitem_json = json.dumps(get_order_item())
    return HttpResponse(dropdownitem_json, content_type='application/json')


def get_order_item():
    location_dict = {}
    customer_dict = {}
    item_dict = {}
    supplier_dict = {}
    pay_method_dict = {}

    location_data = Location.objects.all()
    # Create a dictionary for each Location object and append it to dropdownitem
    for location in location_data:
        location_dict[location.location_id] = {
        'id': location.location_id,
        'name': location.name
    }

    customer_data = Customer.objects.all()
    # Create a dictionary for each Location object and append it to dropdownitem
    for customer in customer_data:
        customer_dict[customer.customer_id] = {
            'id': customer.customer_id,
            'name': customer.name
        }

    item_data = Item.objects.all()
    # Create a dictionary for each Location object and append it to dropdownitem
    for item in item_data:
        item_dict[item.item_id] = {
            'id': item.item_id,
            'name': item.name
        }
    
    supplier_data = Supplier.objects.all()
    # Create a dictionary for each Location object and append it to dropdownitem
    for supplier in supplier_data:
        supplier_dict[supplier.supplier_id] = {
            'id': supplier.supplier_id,
            'name': supplier.name
        }
    

    pay_method_dict = dict(Order_Transection.PAY_RECEIVE_METHOD_CHOICES)
    payment_methods_list = []

    # Convert the payment_methods_dict to a list of dictionaries with 'id' and 'name'
    for key, value in pay_method_dict.items():
        payment_methods_list.append({'id': key, 'name': value})
    
    orderItemData = {
        'location': location_dict,
        'customer': customer_dict,
        'item' : item_dict, 
        'pay_method' : payment_methods_list,
        'supplier' : supplier_dict,
    }

    return orderItemData

def about(request):
    return render(request, 'about.html')















def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')
