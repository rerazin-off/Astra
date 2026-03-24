from django.shortcuts import render, get_object_or_404, redirect  # Утилиты для работы с представлениями
from django.db.models import Q  # Для сложных запросов с OR (логическое ИЛИ)
from django.contrib import messages  # Для отображения уведомлений пользователю

# Главная страница - вывод статистики и информации
def home(request):
    total_books = 4  # Все книги
    total_authors = 4  # Все авторы.count()  # Только доступные
    
    # Контекст для передачи в шаблон
    context = {
        'total_books': total_books,
        'total_authors': total_authors
    }
    return render(request, 'Astra/home.html', context)
