# from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import BookingForm, OrderForm
from .models import Menu
from django.core import serializers
from .models import Booking, Order_Transection
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
