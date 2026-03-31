from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('mes-annonces/', views.mes_annonces, name='mes_annonces'),
    path('ajouter/', views.add, name='add'),
    path('annonce/<int:id>/', views.detail, name='detail'),
    path('categorie/<slug:slug>/', views.category_list, name='category_list'),
    path('annonce/<int:id>/editer/', views.edit, name='edit'),
    path('annonce/<int:id>/supprimer/', views.delete, name='delete'),
]