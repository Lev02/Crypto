
from django.contrib import admin
from django.urls import path, include
from backend.views import *

app_name = 'cryptoparser'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_coin)
]
