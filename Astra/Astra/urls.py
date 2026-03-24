from django.urls import path
from . import views  # Импорт представлений из текущего приложения

# Пространство имен для URL-шаблонов приложения
# Позволяет использовать 'books:book_list' в шаблонах и представлениях
app_name = 'Astra'

# Список всех URL-маршрутов приложения
urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    # Пример использования в шаблоне: {% url 'books:home' %}
    
]