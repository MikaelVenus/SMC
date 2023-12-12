from django.urls import path, include
from . import views

from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('home/', login_required(views.home), name="home"),
    path('about/', views.about, name="about"),
    path('orderitem/', views.orderitem, name="orderitem"),
    path('orderitemviews', views.orderitemviews, name="orderitemviews"),
    path('editorderitem/', views.editorderitem, name="editorderitem"),
    path('editorderitemviews/', views.editorderitemviews, name="editorderitemviews"),
    path('ordering', views.ordering, name="ordering"),
    path('editordering', views.editordering, name="editordering"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    path('bookings', views.bookings, name='bookings'), 
    path('transection', views.transection, name='transection'), 
    path('transectionviews', views.transectionviews, name='transectionviews'), 
    path('transectionviewscriteria', views.transectionviewscriteria, name='transectionviewscriteria'), 
]