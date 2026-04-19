from django.contrib import admin
from .models import Users_System, Rarity, Cards, User_Inventory, Battle_History, Gacha_History,Attribute

@admin.register(Users_System)
class Users_SystemAdmin(admin.ModelAdmin):
    list_display = ['nikname', 'name', 'last_name', 'email', 'current_points', 'created_at']
    list_filter = ['created_at']
    search_fields = ['nikname', 'name', 'email']
    readonly_fields = ['created_at']

@admin.register(Rarity)
class RarityAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'multiplier', 'order']
    list_editable = ['order']
    list_filter = ['name']

@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ['title', 'rarity', 'attribute', 'strenth', 'health', 'defence', 'author', 'is_active']
    list_filter = ['rarity', 'attribute', 'is_active', 'author']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']
    
    def save_model(self, request, obj, form, change):
        if not change and obj.author_id is None:
            linked = Users_System.objects.filter(email__iexact=request.user.email).first()
            if linked:
                obj.author = linked
        super().save_model(request, obj, form, change)

@admin.register(User_Inventory)
class User_InventoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'card', 'quantity', 'is_favorite', 'is_equipped']
    list_filter = ['is_favorite', 'is_equipped']
    search_fields = ['user__nikname', 'card__title']

@admin.register(Battle_History)
class Battle_HistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_victory', 'points_earned', 'battle_date']
    list_filter = ['is_victory', 'battle_date']
    search_fields = ['user__nikname']

@admin.register(Gacha_History)
class Gacha_HistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'card', 'points_spent', 'obtained_at']
    list_filter = ['obtained_at']
    search_fields = ['user__nikname', 'card__title']

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'strength_bonus', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'icon', 'color', 'is_active')
        }),
        ('Игровые параметры', {
            'fields': ('strength_bonus', 'order'),
            'description': 'Настройки влияющие на геймплей'
        }),
    )