from django.urls import path
from . import views

app_name = 'module_project'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    path('catalog/', views.card_catalog, name='card_catalog'),
    path('card/<int:card_id>/', views.card_detail, name='card_detail'),
    path('collection/', views.my_collection, name='my_collection'),
    path('collection/remove/<int:inventory_id>/', views.remove_inventory_card, name='remove_inventory_card'),
    path('card/create/', views.create_card, name='create_card'),
    path('card/<int:card_id>/edit/', views.edit_card, name='edit_card'),
    path('card/<int:card_id>/delete/', views.delete_card, name='delete_card'),
    path('gacha/', views.gacha, name='gacha'),
    path('gacha/result/', views.gacha_result, name='gacha_result'),
    path('battle/', views.battle, name='battle'),
    path('battle/history/', views.battle_history, name='battle_history'),
    path('favorite/<int:inventory_id>/', views.add_to_favorite, name='add_to_favorite'),
    
    path('api/cards/', views.api_filter_cards, name='api_filter_cards'),
    path('api/collection/', views.api_filter_collection, name='api_filter_collection'),
]