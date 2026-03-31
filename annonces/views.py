from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Annonce
from .forms import AnnonceForm


def index(request):
    q = request.GET.get('q')
    ville = request.GET.get('ville')
    annonces = Annonce.objects.all()
    if q:
        annonces = annonces.filter(titre__icontains=q)
    if ville:
        annonces = annonces.filter(ville__icontains=ville)
    return render(request, 'annonces/index.html', {'annonces': annonces, 'query': q or '', 'ville': ville or ''})


def detail(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    return render(request, 'annonces/detail.html', {'annonce': annonce})


@login_required
def add(request):
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.auteur = request.user
            annonce.save()
            return redirect('detail', id=annonce.id)
    else:
        form = AnnonceForm()
    return render(request, 'annonces/add.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'annonces/signup.html', {'form': form})


@login_required
@login_required
def edit(request, id):
    annonce = get_object_or_404(Annonce, id=id, auteur=request.user)
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES, instance=annonce)
        if form.is_valid():
            form.save()
            return redirect('detail', id=annonce.id)
    else:
        form = AnnonceForm(instance=annonce)
    return render(request, 'annonces/edit.html', {'form': form, 'annonce': annonce})


@login_required
def delete(request, id):
    annonce = get_object_or_404(Annonce, id=id, auteur=request.user)
    if request.method == 'POST':
        annonce.delete()
        return redirect('index')
    return render(request, 'annonces/confirm_delete.html', {'annonce': annonce})


@login_required
def mes_annonces(request):
    annonces = Annonce.objects.filter(auteur=request.user).order_by('-date_creation')
    return render(request, 'annonces/mes_annonces.html', {'annonces': annonces})
