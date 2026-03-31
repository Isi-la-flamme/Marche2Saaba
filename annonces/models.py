from django.db import models
from django.contrib.auth.models import User

class Annonce(models.Model):
    CATEGORIES = [
        ('voiture', 'Voiture'),
        ('telephone', 'Téléphone'),
        ('maison', 'Maison'),
    ]
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    image = models.ImageField(upload_to='annonces/')
    contact = models.CharField(max_length=20)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre