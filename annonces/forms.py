from django import forms
from .models import Annonce


class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = [
            'titre',
            'description',
            'prix',
            'categorie',
            'ville',
            'code_postal',
            'contact',
            'image',
        ]
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Titre de l\'annonce', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': 4}),
            'prix': forms.NumberInput(attrs={'placeholder': 'Prix en €', 'class': 'form-control', 'step': '0.01'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'placeholder': 'Ville', 'class': 'form-control'}),
            'code_postal': forms.TextInput(attrs={'placeholder': 'Code postal', 'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'placeholder': 'WhatsApp ou téléphone', 'class': 'form-control'}),
        }

    image = forms.ImageField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
