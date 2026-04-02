from django import forms
from .models import Cards

class CardForm(forms.ModelForm):
    class Meta:
        model=Cards
        fields=['title','cover_image','description','created_at','strenth',
        'health','defence','attribute','rarity','price_points','author','is_active']
        """
        """
        widgets={
            'title': forms.TextInput(attrs={
                'class': 'form-control',  
                'placeholder': 'Название карточки'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control' 
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4, 
                'placeholder': 'Описание карточки'
            }),
            'strenth': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сила карточки'
            }),
            'health': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Здоровье карточки'
            }),
            'defence': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Защита карточки'
            }),
            'title': forms.CharField(attrs={
                'class': 'form-control',  
                'placeholder': 'Атрибут карточки'
            }),
            'rarity': forms.Select(attrs={
                'class': 'form-control'  
            }),
            'price_points': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Стоимость карточки'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'  
            }),
            'is_active': forms.CheckboxInput(attr={
                'class': 'form-control'
            }),
        }

class UsersSystemForm(forms.ModelForm):
    class Meta:
        model=Cards
        fields=[]
        """
        """
        widgets={
            
        }

        