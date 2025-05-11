from django.urls import path
from .views import home_view, contact

app_name = 'home'

urlpatterns = [
    path('', home_view, name='home'),
    path('contact/', contact, name='contact'),

]
