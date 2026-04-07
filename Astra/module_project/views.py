
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Users_System, User_Inventory, Cards
from .forms import UsersSystemForm, UserProfileForm, AddPointsForm

def home(request):
    """Временная заглушка для главной страницы"""
    return HttpResponse("""
        <h1>Космическая ККИ</h1>
        <p>Проект в разработке...</p>
        <p>Модели созданы, дальше будет добавлен функционал</p>
    """)

def register(request):
    """Страница регистрации нового пользователя"""
    if request.method == 'POST':
        form = UsersSystemForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.total_points = 500 
            user.current_points = 500
            user.save()
            request.session['user_id'] = user.id
            request.session['user_nikname'] = user.nikname
            
            messages.success(request, f'Добро пожаловать, {user.nikname}!')
            return redirect('module_project:dashboard')
    else:
        form = UsersSystemForm()
    
    return render(request, 'module_project/register.html', {'form': form})

def login_view(request):
    """Страница входа в систему"""
    if request.method == 'POST':
        nikname = request.POST.get('nikname')
        password = request.POST.get('password')
        
        try:
            user = Users_System.objects.get(nikname=nikname)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_nikname'] = user.nikname
                messages.success(request, f'С возвращением, {user.nikname}!')
                return redirect('module_project:dashboard')
            else:
                messages.error(request, 'Неверный пароль')
        except Users_System.DoesNotExist:
            messages.error(request, 'Пользователь не найден')
    
    return render(request, 'module_project/login.html')

def dashboard(request):
    """Личный кабинет пользователя после регистрации/входа"""
    if 'user_id' not in request.session:
        messages.warning(request, 'Пожалуйста, войдите в систему')
        return redirect('module_project:login')
    
    user = Users_System.objects.get(id=request.session['user_id'])
    
    total_cards = User_Inventory.objects.filter(user=user).count()
    favorite_cards = User_Inventory.objects.filter(user=user, is_favorite=True).count()
    equipped_cards = User_Inventory.objects.filter(user=user, is_equipped=True).count()
    
    from .models import Battle_History
    recent_battles = Battle_History.objects.filter(user=user)[:5]
    wins = Battle_History.objects.filter(user=user, is_victory=True).count()
    total_battles = Battle_History.objects.filter(user=user).count()
    win_rate = (wins / total_battles * 100) if total_battles > 0 else 0
    
    from .models import Gacha_History
    recent_gacha = Gacha_History.objects.filter(user=user).select_related('card')[:5]
    
    points_form = AddPointsForm()
    
    if request.method == 'POST' and 'add_points' in request.POST:
        points_form = AddPointsForm(request.POST)
        if points_form.is_valid():
            points = points_form.cleaned_data['points']
            user.current_points += points
            user.total_points += points
            user.save()
            messages.success(request, f'На ваш счёт добавлено {points} очков!')
            return redirect('module_project:dashboard')
    
    context = {
        'user': user,
        'total_cards': total_cards,
        'favorite_cards': favorite_cards,
        'equipped_cards': equipped_cards,
        'recent_battles': recent_battles,
        'recent_gacha': recent_gacha,
        'wins': wins,
        'total_battles': total_battles,
        'win_rate': round(win_rate, 1),
        'points_form': points_form,
    }
    
    return render(request, 'module_project/dashboard.html', context)

def logout_view(request):
    """Выход из системы"""
    request.session.flush()
    messages.info(request, 'Вы вышли из системы')
    return redirect('module_project:login')

def profile_edit(request):
    """Редактирование профиля"""
    if 'user_id' not in request.session:
        return redirect('module_project:login')
    
    user = Users_System.objects.get(id=request.session['user_id'])
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            request.session['user_nikname'] = user.nikname
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('module_project:dashboard')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'module_project/profile_edit.html', {'form': form, 'user': user})

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