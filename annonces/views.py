from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Annonce
from .forms import AnnonceForm


def index(request):
    q = request.GET.get('q', '')
    ville = request.GET.get('ville', '')
    categorie = request.GET.get('categorie', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    annonces = Annonce.objects.all()
    if q:
        annonces = annonces.filter(titre__icontains=q)
    if ville:
        annonces = annonces.filter(ville__icontains=ville)
    if categorie:
        annonces = annonces.filter(categorie=categorie)
    if min_price:
        try:
            annonces = annonces.filter(prix__gte=Decimal(min_price))
        except InvalidOperation:
            pass
    if max_price:
        try:
            annonces = annonces.filter(prix__lte=Decimal(max_price))
        except InvalidOperation:
            pass

    return render(
        request,
        'annonces/index.html',
        {
            'annonces': annonces,
            'query': q,
            'ville': ville,
            'categorie': categorie,
            'categories': Annonce.CATEGORIES,
            'min_price': min_price,
            'max_price': max_price,
        },
    )


def category_list(request, slug):
    annonces = Annonce.objects.filter(categorie=slug)
    category_label = dict(Annonce.CATEGORIES).get(slug, slug.replace('-', ' ').title())
    return render(
        request,
        'annonces/category.html',
        {
            'annonces': annonces,
            'category_label': category_label,
            'categories': Annonce.CATEGORIES,
        },
    )


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
