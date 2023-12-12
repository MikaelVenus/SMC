# from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import BookingForm, OrderForm, TransectionForm
from .models import Menu
from django.core import serializers
from .models import Booking, Order_Transection, Location,Supplier,Customer, Item
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.db.models import Max

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


def editorderitem(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'editorderitem.html', context)

@csrf_exempt
def ordering(request):
    if request.method == 'POST':
        data = json.load(request)

        customer_instance = Customer.objects.filter(customer_id=data['customer']).first()
        supplier_instance = Supplier.objects.filter(supplier_id=data['supplier']).first()
        item_instance = Item.objects.filter(item_id=data['item']).first()
        target_location_instance = Location.objects.filter(location_id=data['target_location']).first()
        receive_location_instance = Location.objects.filter(location_id=data['receive_location']).first()
        
        # date = request.GET.get('date',datetime.today().date())
        add_item = Order_Transection(
            order_id = data['order_id'],
            customer = customer_instance,
            supplier = supplier_instance,
            item = item_instance,
            target_location = target_location_instance,
            receive_phone = data['receive_phone'],
            delivery_date = convert_date_format(data['delivery_date']),
            delivery_number = data['delivery_number'],
            receive_name = data['receive_name'],
            q_sale = data['q_sale'],
            sale_price = data['sale_price'],
            total_sale_amount = data['total_sale_amount'],
            sale_pay_method = data['sale_pay_method'],        
            sale_vat_id = data['sale_vat_id'], 
            receive_date = convert_date_format(data['receive_date']), 
            receive_location = receive_location_instance, 
            q_buy = data['q_buy'], 
            buy_price = data['buy_price'],     
            delivery_price = data['delivery_price'],     
            remark = data['remark'],     
            buy_vat_id = data['buy_vat_id'],     
            total_buy_amount = data['total_buy_amount'],     
            buy_pay_method = data['buy_pay_method'],     
            pay_date = convert_date_format(data['pay_date']),     
        )
        add_item.save()

        

        order_item=Order_Transection.objects.all()
        order_item_json = serializers.serialize('json', order_item)
        return HttpResponse(order_item_json, content_type='application/json')


@csrf_exempt
def editorderitemviews(request):
    order_id = request.GET.get('order_id')
    print(order_id)
    order_data = json.dumps(get_transection_item_by_id(order_id))
    return HttpResponse(order_data, content_type='application/json')

def transection(request):
    # form = TransectionForm()
    # if request.method == 'POST':
    #     form = TransectionForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    context = {'form':'form'}
    return render(request, 'transection.html', context)

@csrf_exempt
def transectionviews(request):
    # form = TransectionForm()
    # if request.method == 'POST':
    #     form = TransectionForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    dropdownitem_json = json.dumps(get_transection_item())
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
    
    max_order_id = Order_Transection.objects.aggregate(max_order_id=Max('order_id'))
    max_order_id_str = str(max_order_id['max_order_id']) if max_order_id['max_order_id'] is not None else ''
    current_date = datetime.now()
    formatted_date = current_date.strftime("%y%m%d")

    running_order_id =''
    if max_order_id_str and formatted_date == max_order_id_str[:6]:
        running_order_id = str(int(max_order_id_str) + 1)
    else:
        running_order_id = formatted_date + '001'

    orderItemData = {
        'location': location_dict,
        'customer': customer_dict,
        'item' : item_dict, 
        'pay_method' : payment_methods_list,
        'supplier' : supplier_dict,
        'order_id' : max_order_id,
        'formatted_date' : formatted_date,
        'running_order_id': running_order_id,
    }

    return orderItemData


def get_edit_order_item():
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
    
    max_order_id = Order_Transection.objects.aggregate(max_order_id=Max('order_id'))
    max_order_id_str = str(max_order_id['max_order_id']) if max_order_id['max_order_id'] is not None else ''
    current_date = datetime.now()
    formatted_date = current_date.strftime("%y%m%d")

    running_order_id =''
    if max_order_id_str and formatted_date == max_order_id_str[:6]:
        running_order_id = str(int(max_order_id_str) + 1)
    else:
        running_order_id = formatted_date + '001'

    orderItemData = {
        'location': location_dict,
        'customer': customer_dict,
        'item' : item_dict, 
        'pay_method' : payment_methods_list,
        'supplier' : supplier_dict,
        'order_id' : max_order_id,
        'formatted_date' : formatted_date,
        'running_order_id': running_order_id,
    }

    return orderItemData


def get_transection_item():
    transection_sale_dict = {}
    transection_buy_dict = {}

    transection_data = Order_Transection.objects.all()

    for transection in transection_data:
        transection_sale_dict[transection.order_id] = {
        'order_id': transection.order_id,
        'customer': transection.customer.name,
        'supplier': transection.supplier.name,
        'item': transection.item.name,
        'delivery_date': transection.delivery_date.strftime("%y-%m-%d"),
        #Customer part
        'target_location': transection.target_location.name,
        'receive_phone': transection.receive_phone,
        'delivery_number': transection.delivery_number,
        'receive_name': transection.receive_name,
        'q_sale': str(transection.q_sale),
        'sale_price': str(transection.sale_price),
        'total_sale_amount': str(transection.total_sale_amount),
        'sale_pay_method' : transection.sale_pay_method,
        'sale_vat_id': transection.sale_vat_id,
        'delivery_number': transection.delivery_number,
        'receive_date': transection.receive_date.strftime("%y-%m-%d"),
    }
        
    for transection in transection_data:
        transection_buy_dict[transection.order_id] = {
        'order_id': transection.order_id,
        'customer': transection.customer.name,
        'supplier': transection.supplier.name,
        'item': transection.item.name,
        'delivery_date': transection.delivery_date.strftime("%y-%m-%d"),
        #Owner Part
        'receive_location': transection.receive_location.name,
        'q_buy': str(transection.q_buy),
        'buy_price': str(transection.buy_price),
        'delivery_price': str(transection.delivery_price),
        'remark': transection.remark,
        'buy_vat_id': transection.buy_vat_id,
        'total_buy_amount': str(transection.total_buy_amount),
        'buy_pay_method': transection.buy_pay_method,
        'pay_date': transection.pay_date.strftime("%y-%m-%d"),
    }



    transectionData = {
        'transection_sale': transection_sale_dict,
        'transection_buy': transection_buy_dict,
    }

    return transectionData


def get_transection_item_by_id(request_order_id):
    transection_sale_dict = {}
    transection_buy_dict = {}

    transection_data = Order_Transection.objects.filter(order_id=request_order_id)

    for transection in transection_data:
        transection_sale_dict[transection.order_id] = {
        'order_id': transection.order_id,
        'customer': transection.customer.name,
        'supplier': transection.supplier.name,
        'item': transection.item.name,
        'delivery_date': transection.delivery_date.strftime("%y-%m-%d"),
        #Customer part
        'target_location': transection.target_location.name,
        'receive_phone': transection.receive_phone,
        'delivery_number': transection.delivery_number,
        'receive_name': transection.receive_name,
        'q_sale': str(transection.q_sale),
        'sale_price': str(transection.sale_price),
        'total_sale_amount': str(transection.total_sale_amount),
        'sale_pay_method' : transection.sale_pay_method,
        'sale_vat_id': transection.sale_vat_id,
        'delivery_number': transection.delivery_number,
        'receive_date': transection.receive_date.strftime("%y-%m-%d"),
    }
        
    for transection in transection_data:
        transection_buy_dict[transection.order_id] = {
        'order_id': transection.order_id,
        'customer': transection.customer.name,
        'supplier': transection.supplier.name,
        'item': transection.item.name,
        'delivery_date': transection.delivery_date.strftime("%y-%m-%d"),
        #Owner Part
        'receive_location': transection.receive_location.name,
        'q_buy': str(transection.q_buy),
        'buy_price': str(transection.buy_price),
        'delivery_price': str(transection.delivery_price),
        'remark': transection.remark,
        'buy_vat_id': transection.buy_vat_id,
        'total_buy_amount': str(transection.total_buy_amount),
        'buy_pay_method': transection.buy_pay_method,
        'pay_date': transection.pay_date.strftime("%y-%m-%d"),
    }



    transectionData = {
        'transection_sale': transection_sale_dict,
        'transection_buy': transection_buy_dict,
    }

    return transectionData

def about(request):
    return render(request, 'about.html')


def convert_date_format(input_date):
    # Parse the input date string to a datetime object
    date_object = datetime.strptime(input_date, "%d-%m-%Y")

    # Format the datetime object to "yyyy mm dd" format
    formatted_date = date_object.strftime("%Y-%m-%d")

    return formatted_date















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
