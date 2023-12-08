from django.db import models

class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f"{self.customer_id} : {self.name} : {self.description[:20]}"
    
class Supplier(models.Model):
    supplier_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f"{self.supplier_id} : {self.name} : {self.description[:20]}"
    
class Location(models.Model):
    location_id = models.IntegerField(primary_key=True)
    location_type = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f"{self.supplier_id} : {self.name} : {self.description[:20]}"
    
class Item(models.Model):
    item_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=4,max_digits=8)
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f"{self.item_id} : {self.name} : {self.description[:20]}"
    
class Order_Transection(models.Model):
    
    #Customer part
    order_id = models.IntegerField(primary_key=True,max_length=8)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,  on_delete=models.CASCADE)
    target_location = models.ForeignKey(Location,  on_delete=models.CASCADE)
    receive_phone = models.IntegerField(max_length=12)
    delivery_date = models.DateField()
    delivery_number = models.CharField(max_length=20)
    receive_name = models.CharField(max_length=100)
    q_sale = models.DecimalField(decimal_places=4,max_digits=8)
    sale_price = models.DecimalField(decimal_places=4,max_digits=8)
    toal_sale_amount = models.DecimalField(decimal_places=4,max_digits=8)
    PAY_RECEIVE_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('qrscan', 'QR Scan'),
        ('credit', 'Credit'),
        ('check', 'Check'),
    ]
    # Define receive_method field with choices
    receive_method = models.CharField(max_length=20, choices=PAY_RECEIVE_METHOD_CHOICES)
    sale_vat = models.CharField(max_length=30)
    pay_receive_date = models.DateField()
    












# Add code to create Menu model
class Menu(models.Model):
   name = models.CharField(max_length=200) 
   price = models.IntegerField(null=False) 
   menu_item_description = models.TextField(max_length=1000, default='') 

   def __str__(self):
      return self.name

# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

    def __str__(self): 
        return self.first_name
