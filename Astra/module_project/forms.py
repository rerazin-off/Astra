from django import forms
from .models import Attribute, Cards, Rarity, User_Inventory, Users_System

class CardForm(forms.ModelForm):
    class Meta:
        model=Cards
        fields=['title','cover_image','description','strenth',
        'health','defence','attribute','rarity','price_points','author','is_active']
        """
        """
        widgets={
            'title': forms.TextInput(attrs={
                'class': 'form-control',  
                'placeholder': 'Название карточки'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4, 
                'placeholder': 'Описание карточки'
            }),
            'strenth': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сила карточки (1-9999)',
                'min': 1,
                'max': 9999
            }),
            'health': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Здоровье карточки (1-9999)',
                'min': 1,
                'max': 9999
            }),
            'defence': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Защита карточки (0-9999)',
                'min': 0,
                'max': 9999
            }),
            'attribute': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите атрибут'
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
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['attribute'].queryset = Attribute.objects.filter(is_active=True)
        self.fields['rarity'].queryset = Rarity.objects.all()
    
    def clean_strenth(self):
        strenth = self.cleaned_data.get('strenth')
        if strenth and (strenth < 1 or strenth > 9999):
            raise forms.ValidationError('Сила должна быть от 1 до 9999')
        return strenth
    
    def clean_health(self):
        health = self.cleaned_data.get('health')
        if health and (health < 1 or health > 9999):
            raise forms.ValidationError('Здоровье должно быть от 1 до 9999')
        return health
    
    def clean_price_points(self):
        price = self.cleaned_data.get('price_points')
        if price and price < 10:
            raise forms.ValidationError('Цена должна быть не менее 10 очков')
        return price

class UsersSystemForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        }),
        label='Подтверждение пароля'
    )
    
    class Meta:
        model = Users_System
        fields = ['nikname', 'name', 'last_name', 'email', 'password']
        
        widgets = {
            'nikname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Никнейм'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }),
        }
    
    def clean_nikname(self):
        nikname = self.cleaned_data.get('nikname')
        if Users_System.objects.filter(nikname=nikname).exists():
            raise forms.ValidationError('Пользователь с таким никнеймом уже существует')
        return nikname
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users_System.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        ##user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Users_System
        fields = ['nikname', 'name', 'last_name', 'email']
        
        widgets = {
            'nikname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Никнейм'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }


class RarityForm(forms.ModelForm):
    class Meta:
        model = Rarity
        fields = ['name', 'color', 'multiplier', 'order']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название редкости'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'placeholder': '#FFFFFF'
            }),
            'multiplier': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Множитель шанса (0.1-10.0)',
                'step': 0.1,
                'min': 0.1,
                'max': 10.0
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Порядок сортировки'
            })
        }


class CardFilterForm(forms.Form):
    title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Название карточки'
        }),
        label='Название'
    )
    
    rarity = forms.ModelChoiceField(
        queryset=Rarity.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Редкость'
    )
    
    attribute = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Атрибут'
        }),
        label='Атрибут'
    )
    
    min_power = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Мин. сила'
        }),
        label='Минимальная сила',
        min_value=0
    )
    
    max_power = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Макс. сила'
        }),
        label='Максимальная сила',
        min_value=0
    )
    
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Только активные',
        initial=True
    )


class AddPointsForm(forms.Form):
    points = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Количество очков'
        }),
        label='Очки',
        min_value=1,
        max_value=10000
    )


class GachaForm(forms.Form):
    GACHA_TYPES = [
        ('single', 'Одиночное открытие (100 очков)'),
        ('ten', '10 открытий (1000 очков)'),
    ]
    
    gacha_type = forms.ChoiceField(
        choices=GACHA_TYPES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Тип открытия'
    )


class BattleForm(forms.Form):
    user_card = forms.ModelChoiceField(
        queryset=User_Inventory.objects.none(), 
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите карточку для боя'
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_card'].queryset = User_Inventory.objects.filter(
            user=user
        ).select_related('card')

        