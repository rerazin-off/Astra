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