from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Attribute(models.Model):
    """
    Модель атрибутов карточек (стихии/типы)
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название атрибута"
    )
    
    icon = models.ImageField(
        upload_to='attributes_icons/',
        verbose_name="Иконка атрибута",
        blank=True,
        null=True
    )
    
    color = models.CharField(
        max_length=7,
        default="#FFFFFF",
        verbose_name="Цвет атрибута в HEX",
        help_text="Например: #FF0000 для красного"
    )
    
    strength_bonus = models.FloatField(
        default=1.0,
        verbose_name="Бонус к силе",
        help_text="Множитель силы для карт этого атрибута"
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name="Порядок сортировки"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    
    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.color.startswith('#'):
            self.color = '#' + self.color
        super().save(*args, **kwargs)
class Users_System(models.Model):
    """
    Модель для хранения информации о пользователях.
    """
    nikname = models.CharField(
        max_length=100, 
        verbose_name="Никнейм",
        unique=True
    )
    name = models.CharField(
        max_length=100, 
        verbose_name="Имя пользователя"
    )
    last_name = models.CharField(
        max_length=150, 
        verbose_name="Фамилия пользователя"
    )
    password = models.CharField(
        max_length=100, 
        verbose_name="Пароль"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата регистрации"
    )
    email = models.CharField(
        max_length=200, 
        verbose_name="Почта пользователя"
    )
    total_points = models.IntegerField(
        default=0,
        verbose_name="Всего очков",
        validators=[MinValueValidator(0)]
    )
    current_points = models.IntegerField(
        default=0,
        verbose_name="Текущие очки",
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.nikname or self.name
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Rarity(models.Model):
    """
    Модель редкости карточек (добавлена для баланса)
    """
    name = models.CharField(
        max_length=50,
        verbose_name="Название редкости"
    )
    color = models.CharField(
        max_length=7,
        default="#FFFFFF",
        verbose_name="Цвет в HEX"
    )
    multiplier = models.FloatField(
        default=1.0,
        verbose_name="Множитель шанса выпадения"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Порядок сортировки"
    )
    
    class Meta:
        verbose_name = "Редкость"
        verbose_name_plural = "Редкости"
        ordering = ['order']
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.color and not self.color.startswith('#'):
            self.color = '#' + self.color
        super().save(*args, **kwargs)


class Cards(models.Model):
    """
    Модель карточки
    """
    title = models.CharField(
        max_length=100,
        verbose_name="Название карточки"
    )
    cover_image = models.ImageField(
        upload_to='covers_card/',  
        verbose_name="Обложка карточки", 
        blank=True, 
        null=True 
    )
    description = models.TextField(
        verbose_name="Описание", 
        blank=True  
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )
    strenth = models.IntegerField( 
        verbose_name="Сила карты",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(9999)]
    )
    health = models.IntegerField(
        verbose_name="Жизни карты",
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(9999)]
    )
    defence = models.IntegerField(
        verbose_name="Защита карты",
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)]
    )
    attribute = models.ForeignKey(
        Attribute, # type: ignore
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cards',
        verbose_name="Атрибут карточки"
    )
    
    rarity = models.ForeignKey(
        Rarity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cards',
        verbose_name="Редкость"
    )
    
    price_points = models.IntegerField(
        default=100,
        verbose_name="Цена в очках",
        validators=[MinValueValidator(10)]
    )
    
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,  
        null=True,
        blank=True,
        related_name='cards',
        verbose_name="Автор карточки"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
    )
    
    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"
        ordering = ['-created_at']
    
    def __str__(self):
        rarity_name = f" ({self.rarity.name})" if self.rarity else ""
        return f"{self.title}{rarity_name}"
    
    def get_total_power(self):
        """Расчет общей силы карты"""
        return (self.strenth or 0) + (self.health or 0) + (self.defence or 0)


class User_Inventory(models.Model):
    """
    Модель инвентаря пользователя (карточки, принадлежащие пользователю)
    """
    user = models.ForeignKey(
        Users_System,
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name="Пользователь"
    )
    card = models.ForeignKey(
        Cards,
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name="Карточка"
    )
    
    quantity = models.IntegerField(
        default=1,
        verbose_name="Количество",
        validators=[MinValueValidator(1)]
    )
    is_favorite = models.BooleanField(
        default=False,
        verbose_name="В избранном"
    )
    is_equipped = models.BooleanField(
        default=False,
        verbose_name="Экипирована"
    )
    
    times_won = models.IntegerField(
        default=0,
        verbose_name="Количество побед"
    )
    
    obtained_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата получения"
    )
    class Meta:
        verbose_name = "Карточка в инвентаре"
        verbose_name_plural = "Карточки в инвентаре"
        unique_together = ['user', 'card']  # Пользователь не может иметь две одинаковые карточки
        ordering = ['-obtained_at']
    
    def __str__(self):
        return f"{self.user.nikname} - {self.card.title} (x{self.quantity})"
    
    def use_card(self):
        """Использовать карточку в бою"""
        self.times_used += 1
        self.last_used_at = timezone.now()
        self.save()
    
    def win_with_card(self):
        """Победа с использованием этой карточки"""
        self.times_won += 1
        self.use_card()
    
    def get_win_rate(self):
        """Процент побед с карточкой"""
        if self.times_used == 0:
            return 0
        return (self.times_won / self.times_used) * 100


class Battle_History(models.Model):
    """
    История боев пользователя
    """
    user = models.ForeignKey(
        Users_System,
        on_delete=models.CASCADE,
        related_name='battles',
        verbose_name="Пользователь"
    )
    user_card = models.ForeignKey(
        User_Inventory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='battles_as_user',
        verbose_name="Карточка пользователя"
    )
    robot_card = models.ForeignKey(
        Cards,
        on_delete=models.SET_NULL,
        null=True,
        related_name='battles_as_robot',
        verbose_name="Карточка робота"
    )
    
    is_victory = models.BooleanField(
        verbose_name="Победа"
    )
    points_earned = models.IntegerField(
        default=0,
        verbose_name="Заработано очков",
        validators=[MinValueValidator(0)]
    )
    
    user_power = models.IntegerField(
        default=0,
        verbose_name="Сила пользователя"
    )
    robot_power = models.IntegerField(
        default=0,
        verbose_name="Сила робота"
    )
    
    battle_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата боя"
    )
    
    class Meta:
        verbose_name = "История боя"
        verbose_name_plural = "История боев"
        ordering = ['-battle_date']
    
    def __str__(self):
        result = "Победа" if self.is_victory else "Поражение"
        return f"{self.user.nikname} - {result} - {self.points_earned} очков"


class Gacha_History(models.Model):
    """
    История открытия гачи
    """
    user = models.ForeignKey(
        Users_System,
        on_delete=models.CASCADE,
        related_name='gacha_history',
        verbose_name="Пользователь"
    )
    card = models.ForeignKey(
        Cards,
        on_delete=models.CASCADE,
        related_name='gacha_history',
        verbose_name="Полученная карточка"
    )
    points_spent = models.IntegerField(
        verbose_name="Потрачено очков",
        validators=[MinValueValidator(0)]
    )
    obtained_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата получения"
    )
    
    class Meta:
        verbose_name = "История гачи"
        verbose_name_plural = "История гачи"
        ordering = ['-obtained_at']
    
    def __str__(self):
        return f"{self.user.nikname} - {self.card.title} - {self.points_spent} очков"
