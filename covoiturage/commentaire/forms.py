from django import forms
from django.core.exceptions import ValidationError
from .models import Commentaire
from evaluation.models import Evaluation

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['evaluation', 'texte']  # 'date_commentaire' n'est pas nécessaire ici
        widgets = {
            'texte': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    # Validation de la longueur du texte (min et max)
    def clean_texte(self):
        texte = self.cleaned_data.get('texte')

        # Si tu veux éviter les commentaires trop courts
        if texte and len(texte) < 10:
            raise ValidationError("Le commentaire doit contenir au moins 10 caractères.")
        
        # Si tu veux limiter la longueur du commentaire
        if texte and len(texte) > 500:
            raise ValidationError("Le commentaire ne peut pas dépasser 500 caractères.")
        
        return texte

    # Vérification de l'association avec une Evaluation valide (actif, ou dans un état spécifique)
    def clean_evaluation(self):
        evaluation = self.cleaned_data.get('evaluation')

        # Si l'évaluation est dans un état "résolue" ou "archivée", le commentaire ne peut pas être ajouté
        if evaluation and evaluation.etat == 'résolue':
            raise ValidationError("Vous ne pouvez pas ajouter de commentaire pour une évaluation déjà résolue.")
        
        return evaluation

    # Validation d'autres conditions : par exemple vérifier que l'utilisateur a effectué l'évaluation
    def clean(self):
        cleaned_data = super().clean()
        evaluation = cleaned_data.get('evaluation')
        utilisateur = self.instance.evaluation.evaluateur if self.instance else None  # L'utilisateur qui a effectué l'évaluation

        if evaluation and utilisateur != self.user:  # Vérifie si l'utilisateur qui soumet est bien celui qui a fait l'évaluation
            raise ValidationError("Vous ne pouvez commenter que vos propres évaluations.")
        
        return cleaned_data
