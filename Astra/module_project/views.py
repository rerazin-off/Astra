
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Временная заглушка для главной страницы"""
    return HttpResponse("""
        <h1>Космическая ККИ</h1>
        <p>Проект в разработке...</p>
        <p>Модели созданы, дальше будет добавлен функционал</p>
    """)

def card_catalog(request):
    return HttpResponse("Каталог карточек - в разработке")

def card_detail(request, card_id):
    return HttpResponse(f"Детальная информация о карточке {card_id} - в разработке")

def my_collection(request):
    return HttpResponse("Моя коллекция - в разработке")

def create_card(request):
    return HttpResponse("Создание карточки - в разработке")

def edit_card(request, card_id):
    return HttpResponse(f"Редактирование карточки {card_id} - в разработке")

def delete_card(request, card_id):
    return HttpResponse(f"Удаление карточки {card_id} - в разработке")

def gacha(request):
    return HttpResponse("Гача - в разработке")

def battle(request):
    return HttpResponse("Бой с роботом - в разработке")

def battle_history(request):
    return HttpResponse("История боев - в разработке")

def add_to_favorite(request, inventory_id):
    return HttpResponse(f"Добавить в избранное {inventory_id} - в разработке")

def api_filter_cards(request):
    return HttpResponse("API фильтрации карточек - в разработке")

def api_filter_collection(request):
    return HttpResponse("API фильтрации коллекции - в разработке")