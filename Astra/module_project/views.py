
from django.db import transaction as db_transaction

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.db.models import Q
from .models import Users_System, User_Inventory, Cards, Rarity, Gacha_History, Attribute
from .forms import UsersSystemForm, UserProfileForm, AddPointsForm, CardForm, GachaForm
import random
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

@login_required
def create_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            # Автоматическое назначение автора
            card = form.save(commit=False)
            card.author = request.user
            card.save()
            messages.success(request, 'Карта успешно создана!')
            return redirect('module_project:card_detail', pk=card.pk)
    else:
        form = CardForm()
    return render(request, 'module_project/create_card.html', {'form': form})


def card_catalog(request):
    """Каталог всех карточек"""
    cards = Cards.objects.filter(is_active=True).select_related('rarity', 'attribute', 'author')
    
    # Фильтрация
    rarity_id = request.GET.get('rarity')
    attribute_id = request.GET.get('attribute')
    search = request.GET.get('search', '')
    
    if rarity_id:
        cards = cards.filter(rarity_id=rarity_id)
    if attribute_id:
        cards = cards.filter(attribute_id=attribute_id)
    if search:
        cards = cards.filter(Q(title__icontains=search) | Q(description__icontains=search))
    
    rarities = Rarity.objects.all()
    attributes = Attribute.objects.filter(is_active=True)
    
    context = {
        'cards': cards,
        'rarities': rarities,
        'attributes': attributes,
    }
    return render(request, 'module_project/card_catalog.html', context)

def card_detail(request, card_id):
    """Детальная информация о карточке"""
    card = get_object_or_404(Cards, id=card_id)
    
    # Проверяем, есть ли у пользователя эта карточка
    has_card = False
    if 'user_id' in request.session:
        has_card = User_Inventory.objects.filter(
            user_id=request.session['user_id'],
            card=card
        ).exists()
    
    context = {
        'card': card,
        'has_card': has_card,
    }
    return render(request, 'module_project/card_detail.html', context)
def gacha(request):
    """Система гачи (выбивание карточек)"""
    if 'user_id' not in request.session:
        messages.warning(request, 'Войдите в систему')
        return redirect('module_project:login')
    
    user = Users_System.objects.get(id=request.session['user_id'])
    form = GachaForm()
    
    if request.method == 'POST':
        form = GachaForm(request.POST)
        if form.is_valid():
            gacha_type = form.cleaned_data['gacha_type']
            
            # Определяем количество открытий и стоимость
            if gacha_type == 'single':
                pulls = 1
                cost = 100
            else: 
                pulls = 10
                cost = 1000
            
            if user.current_points < cost:
                messages.error(request, f'Недостаточно очков! Нужно {cost}, у вас {user.current_points}')
                return redirect('module_project:gacha')
            
            available_cards = Cards.objects.filter(is_active=True).select_related('rarity')
            
            if not available_cards.exists():
                messages.error(request, 'Нет доступных карточек для открытия')
                return redirect('module_project:gacha')
            
            cards_with_weights = []
            for card in available_cards:
                weight = card.rarity.multiplier if card.rarity else 1.0
                cards_with_weights.append((card, weight))
            
            user.current_points -= cost
            user.save()
            
            obtained_cards = []
            with db_transaction.atomic():
                for _ in range(pulls):
                    card = random.choices(
                        [c[0] for c in cards_with_weights],
                        weights=[c[1] for c in cards_with_weights]
                    )[0]
                    
                    inventory_item, created = User_Inventory.objects.get_or_create(
                        user=user,
                        card=card,
                        defaults={'quantity': 1}
                    )
                    
                    if not created:
                        inventory_item.quantity += 1
                        inventory_item.save()
                    
                    Gacha_History.objects.create(
                        user=user,
                        card=card,
                        points_spent=cost // pulls
                    )
                    
                    obtained_cards.append(card)
            
            unique_cards = set(obtained_cards)
            new_cards = [card for card in obtained_cards if obtained_cards.count(card) == 1]
            
            if pulls == 1:
                card = obtained_cards[0]
                messages.success(request, f'Вы получили: {card.title} ({card.rarity.name if card.rarity else "Обычная"})!')
            else:
                messages.success(request, f'Открыто {pulls} карточек! Новых: {len(new_cards)}, всего уникальных: {len(unique_cards)}')
            
            request.session['last_gacha_result'] = {
                'cards': [{
                    'id': c.id,
                    'title': c.title,
                    'rarity': c.rarity.name if c.rarity else 'Обычная',
                    'rarity_color': c.rarity.color if c.rarity else '#6c757d',
                    'cover_image': c.cover_image.url if c.cover_image else None,
                } for c in obtained_cards],
                'cost': cost,
                'pulls': pulls
            }
            
            return redirect('module_project:gacha_result')
    
    gacha_history = Gacha_History.objects.filter(user=user).select_related('card')[:20]
    
    context = {
        'form': form,
        'user': user,
        'gacha_history': gacha_history,
    }
    return render(request, 'module_project/gacha.html', context)

def gacha_result(request):
    """Страница с результатами гачи"""
    if 'user_id' not in request.session:
        return redirect('module_project:login')
    
    result = request.session.get('last_gacha_result')
    if not result:
        return redirect('module_project:gacha')
    
    del request.session['last_gacha_result']
    
    return render(request, 'module_project/gacha_result.html', {'result': result})

def my_collection(request):
    """Моя коллекция карточек"""
    if 'user_id' not in request.session:
        return redirect('module_project:login')
    
    user = Users_System.objects.get(id=request.session['user_id'])
    inventory = User_Inventory.objects.filter(user=user).select_related('card__rarity', 'card__attribute')
    
    rarity_id = request.GET.get('rarity')
    attribute_id = request.GET.get('attribute')
    favorite_only = request.GET.get('favorite') == 'on'
    
    if rarity_id:
        inventory = inventory.filter(card__rarity_id=rarity_id)
    if attribute_id:
        inventory = inventory.filter(card__attribute_id=attribute_id)
    if favorite_only:
        inventory = inventory.filter(is_favorite=True)
    
    rarities = Rarity.objects.all()
    attributes = Attribute.objects.filter(is_active=True)

    total_count = inventory.count()
    legendary_count = inventory.filter(card__rarity__name__icontains='легенд').count()
    epic_count = inventory.filter(card__rarity__name__icontains='эпич').count()
    rare_count = inventory.filter(card__rarity__name__icontains='редк').count()

    collection_cards_payload = []
    for inv in inventory:
        c = inv.card
        r = c.rarity
        a = c.attribute
        collection_cards_payload.append({
            'inventory_id': inv.id,
            'card_id': c.id,
            'title': c.title,
            'description': c.description or '',
            'cover_url': c.cover_image.url if c.cover_image else '',
            'rarity_name': r.name if r else '',
            'rarity_color': r.color if r else '#6c757d',
            'attribute_name': a.name if a else '',
            'attribute_color': a.color if a else '',
            'strength': c.strenth or 0,
            'health': c.health or 0,
            'defence': c.defence or 0,
            'obtained_at': inv.obtained_at.isoformat() if inv.obtained_at else '',
            'quantity': inv.quantity,
        })

    context = {
        'inventory': inventory,
        'user_cards': inventory,
        'rarities': rarities,
        'attributes': attributes,
        'total_count': total_count,
        'legendary_count': legendary_count,
        'epic_count': epic_count,
        'rare_count': rare_count,
        'collection_cards_payload': collection_cards_payload,
    }
    return render(request, 'module_project/my_collection.html', context)

def edit_card(request, card_id):
    return HttpResponse(f"Редактирование карточки {card_id} - в разработке")

def delete_card(request, card_id):
    return HttpResponse(f"Удаление карточки {card_id} - в разработке")


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