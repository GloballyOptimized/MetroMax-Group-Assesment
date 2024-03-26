from django.urls import path
from core.views import product_list
urlpatterns = [  
    path('',product_list)
]
