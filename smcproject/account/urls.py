from django.urls import path, include
from . import views

from django.contrib.auth.decorators import login_required


urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    # path('logout/', 'django.contrib.auth.views.logout'),    
    # path('home/', views.home, name="home"),
    path('home/', login_required(views.home), name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    path('bookings', views.bookings, name='bookings'), 
]