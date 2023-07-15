from django.urls import path
from . import views

# URL Configuration
urlpatterns = [
    path('', views.index, name='order list page'),
    path('order/<str:pk>', views.ViewOrder, name='order detail page'),
]