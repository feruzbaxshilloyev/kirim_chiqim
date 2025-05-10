from django.urls import path
from .views import *

app_name = 'kirim'
urlpatterns = [
    path('hisobot/', umumiy_hisobot, name='hisobot'),
    path('add_kirim/', add_kirim, name='add_kirim'),
    path('add_chiqim/', add_chiqim, name='add_chiqim'),
    path('add_valyuta/', add_valyuta, name='add_valyuta'),
    path('add-uchun/', add_uchun, name='add_uchun'),
    path('add-kimdan/', add_kimdan, name='add_kimdan'),
    path('kurs_kiritish/', kurs_kiritish, name='kurs_kiritish'),
    path('kirim/', kirim, name='kirim'),
    path('chiqim/', chiqim, name='chiqim'),

]
