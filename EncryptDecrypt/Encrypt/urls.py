from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('decrypt/', decrypt_view, name='decrypt_view'),

]
