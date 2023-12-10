from django.forms import ModelForm
from .models import Booking, Order_Transection


# Code added for loading form data on the Booking page
class OrderForm(ModelForm):
    class Meta:
        model = Order_Transection
        fields = "__all__"

# Code added for loading form data on the Booking page
class TransectionForm(ModelForm):
    class Meta:
        model = Order_Transection
        fields = "__all__"


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"



