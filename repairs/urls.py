from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('repair/<str:pk>/', views.repair_detail, name='repair_detail'),
]
