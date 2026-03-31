from django.shortcuts import render, redirect, get_object_or_404
from .models import Annonce

def index(request):
    q = request.GET.get('q')
    annonces = Annonce.objects.filter(titre__icontains=q) if q else Annonce.objects.all()
    return render(request, "annonces/index.html", {"annonces": annonces})

def detail(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    return render(request, "annonces/detail.html", {"annonce": annonce})

def add(request):
    if request.method == "POST":
        Annonce.objects.create(
            titre=request.POST["titre"],
            prix=request.POST["prix"],
            description=request.POST["description"],
            contact=request.POST["contact"],
            image=request.FILES["image"],
        )
        return redirect("/")
    return render(request, "annonces/add.html")