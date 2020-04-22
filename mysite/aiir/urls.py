from django.urls import path
from . import views


urlpatterns = [
    path('calculations/', views.calculation_list),
    path('calculations/<int:pk>/', views.calculation_detail),
]