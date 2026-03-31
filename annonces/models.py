from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Annonce(models.Model):
    CATEGORIES = [
        ('voiture', 'Voiture'),
        ('telephone', 'Téléphone'),
        ('maison', 'Maison'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='voiture')
    ville = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to='annonces/')
    contact = models.CharField(max_length=20)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('detail', kwargs={'id': self.id})
