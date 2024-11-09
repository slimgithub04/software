# myapp/forms.py
from django import forms
from .models import Evaluation
from django.core.exceptions import ValidationError
from datetime import timedelta

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['score', 'comments']  # Inclut le champ de score et les commentaires
        widgets = {
            'score': forms.Select(choices=[(i, i) for i in range(1, 6)]),  # Dropdown pour choisir un score de 1 à 5
            'comments': forms.Textarea(attrs={'placeholder': 'Add your comments (optional)', 'rows': 3}),
        }
    def clean_date_evaluation(self):
        date_evaluation = self.cleaned_data['date_evaluation']
        trajet = self.cleaned_data['trajet']  # Assurer que 'trajet' est bien dans les données nettoyées

        # Appliquer la même logique de validation que précédemment
        if date_evaluation > (trajet.date_fin + timedelta(days=30)):
            raise ValidationError(f"L'évaluation doit avoir lieu dans les 30 jours suivant la fin du trajet.")
        
        return date_evaluation
    def clean(self):
        cleaned_data = super().clean()
        evaluateur = cleaned_data.get('evaluateur')
        evale = cleaned_data.get('evale')

        if evaluateur == evale:
            raise ValidationError("Vous ne pouvez pas évaluer vous-même.")
        
        # Autres validations peuvent être ajoutées si nécessaire, comme vérifier si l'évaluateur a fait le trajet.
        return cleaned_data
