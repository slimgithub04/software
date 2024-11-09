from django import forms
from .models import Reclamation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['utilisateur', 'trajet', 'sujet', 'description', ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'etat': forms.Select(choices=[('en attente', 'En attente'), ('résolue', 'Résolue')], default='en attente')
        }

    def __init__(self, *args, **kwargs):
        super(ReclamationForm, self).__init__(*args, **kwargs)
        # Si tu veux filtrer les utilisateurs qui peuvent être associés à la réclamation, tu peux le faire ici.
        self.fields['utilisateur'].queryset = User.objects.all()  # Exemple pour tous les utilisateurs
        # Assure-toi que le champ 'utilisateur' est rempli uniquement par l'utilisateur connecté
        if 'utilisateur' in self.fields:
            self.fields['utilisateur'].initial = kwargs.get('initial', {}).get('utilisateur', None)
    
    # Ajouter une méthode de validation si nécessaire
    def clean(self):
        cleaned_data = super().clean()
        sujet = cleaned_data.get('sujet')
        description = cleaned_data.get('description')

        # Exemple de validation si 'sujet' et 'description' sont vides
        if not sujet or not description:
            raise forms.ValidationError("Le sujet et la description sont obligatoires.")
        
        return cleaned_data
    
    def clean_sujet(self):
        sujet = self.cleaned_data.get('sujet')
        if len(sujet) < 5:
            raise ValidationError("Le sujet de la réclamation doit comporter au moins 5 caractères.")
        return sujet
    
    def clean_trajet(self):
        trajet = self.cleaned_data.get('trajet')
        if trajet.date_arrivee < timezone.now():
            raise ValidationError("Vous ne pouvez pas faire une réclamation pour un trajet déjà terminé.")
        return trajet
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise ValidationError("La description ne peut pas être vide.")
        if len(description) > 1000:
            raise ValidationError("La description ne peut pas dépasser 1000 caractères.")
        return description
