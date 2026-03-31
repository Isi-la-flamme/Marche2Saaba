from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('annonce/<int:id>/', views.detail, name='detail'),
    path('ajouter/', views.add, name='add'),
]