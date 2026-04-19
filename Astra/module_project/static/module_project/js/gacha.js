// Применение стилей к карточкам в результатах гачи
document.addEventListener('DOMContentLoaded', function() {
    applyCardStyles();
});

function applyCardStyles() {
    const cards = document.querySelectorAll('.result-card');
    
    cards.forEach(card => {
        // Применяем задержку анимации
        const index = card.dataset.index;
        if (index !== undefined) {
            card.style.animationDelay = `${index}00ms`;
        }
        
        // Применяем стили в зависимости от редкости
        const rarity = card.dataset.rarity;
        const rarityBadge = card.querySelector('.card-rarity');
        
        if (rarity && rarityBadge) {
            // Применяем цвет фона в зависимости от редкости
            const colors = {
                'Обычная': '#808080',
                'Редкая': '#00ff00',
                'Эпическая': '#0088ff',
                'Легендарная': '#ffd700'
            };
            
            rarityBadge.style.backgroundColor = colors[rarity] || '#808080';
            
            // Для легендарных карт меняем цвет текста
            if (rarity === 'Легендарная') {
                rarityBadge.style.color = '#000';
                rarityBadge.style.fontWeight = 'bold';
            }
        }
        
        // Добавляем класс для легендарных карт
        if (rarity === 'Легендарная') {
            card.classList.add('legendary-glow');
        }
    });
}

// Анимация появления карточек
const style = document.createElement('style');
style.textContent = `
    @keyframes revealCard {
        0% { 
            transform: scale(0) rotateY(0deg); 
            opacity: 0; 
        }
        50% { 
            transform: scale(1.1) rotateY(180deg); 
            opacity: 0.8; 
        }
        100% { 
            transform: scale(1) rotateY(360deg); 
            opacity: 1; 
        }
    }
    
    @keyframes legendaryPulse {
        0% { 
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5); 
        }
        50% { 
            box-shadow: 0 0 40px rgba(255, 215, 0, 0.8); 
        }
        100% { 
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5); 
        }
    }
    
    .result-card {
        animation: revealCard 0.8s ease-out;
    }
    
    .legendary-glow {
        animation: legendaryPulse 2s infinite;
    }
`;
document.head.appendChild(style);
// gacha.js - Функции для гача системы

document.addEventListener('DOMContentLoaded', function() {
    const gachaForm = document.getElementById('gacha-form');
    const gachaOptions = document.querySelectorAll('.gacha-option');
    
    // Если мы не на странице гачи - выходим
    if (!gachaForm) return;
    
    // Функция выбора опции
    window.selectOption = function(type) {
        gachaOptions.forEach(opt => {
            opt.classList.remove('selected');
        });
        
        const selectedOption = document.querySelector(`.gacha-option:has(input[value="${type}"])`);
        if (selectedOption) {
            selectedOption.classList.add('selected');
        }
        
        const radio = document.querySelector(`input[value="${type}"]`);
        if (radio) {
            radio.checked = true;
        }
    };
    
    // Выбираем первый вариант по умолчанию
    if (gachaOptions.length > 0) {
        gachaOptions[0].classList.add('selected');
    }
    
    // Анимация открытия
    gachaForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const selectedOption = document.querySelector('input[name="gacha_type"]:checked');
        const cost = selectedOption.value === 'single' ? 100 : 1000;
        
        // Проверка баланса
        const currentPoints = parseInt(document.querySelector('.fa-coins').nextElementSibling?.textContent || '0');
        
        if (currentPoints < cost) {
            showNotification('Недостаточно очков для открытия!', 'warning');
            return;
        }
        
        // Анимация кнопки
        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Открываем...';
        
        // Эффект тряски
        const gachaBanner = document.querySelector('.gacha-banner');
        if (gachaBanner) {
            gachaBanner.style.animation = 'shake 0.5s';
            setTimeout(() => {
                gachaBanner.style.animation = '';
            }, 500);
        }
        
        // Отправляем форму
        setTimeout(() => {
            this.submit();
        }, 1000);
    });
    
    // Добавляем стиль для анимации тряски
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
            20%, 40%, 60%, 80% { transform: translateX(10px); }
        }
    `;
    document.head.appendChild(style);
});

// Функции для страницы результатов гачи
document.addEventListener('DOMContentLoaded', function() {
    const resultCards = document.querySelectorAll('.result-card');
    
    if (resultCards.length === 0) return;
    
    // Последовательная анимация карт
    resultCards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('revealed');
        }, index * 200);
    });
    
    // Подсветка легендарных карт
    const legendaryCards = document.querySelectorAll('[data-rarity="Легендарная"]');
    legendaryCards.forEach(card => {
        card.classList.add('legendary-glow');
        
        // Звуковой эффект (опционально)
        // const audio = new Audio('/static/module_project/sounds/legendary.mp3');
        // audio.play();
    });
    
    // Конфетти для легендарных карт
    if (legendaryCards.length > 0) {
        createConfetti();
    }
    
    function createConfetti() {
        const colors = ['#ffd700', '#ff6b6b', '#4ecdc4', '#667eea'];
        
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.width = '10px';
            confetti.style.height = '10px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.top = '-10px';
            confetti.style.opacity = '0.8';
            confetti.style.pointerEvents = 'none';
            confetti.style.zIndex = '9999';
            confetti.style.transform = `rotate(${Math.random() * 360}deg)`;
            confetti.style.transition = 'all 3s ease-out';
            
            document.body.appendChild(confetti);
            
            setTimeout(() => {
                confetti.style.top = '100%';
                confetti.style.left = (parseFloat(confetti.style.left) + (Math.random() - 0.5) * 20) + '%';
            }, 10);
            
            setTimeout(() => {
                confetti.remove();
            }, 3000);
        }
    }
});