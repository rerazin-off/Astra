document.querySelectorAll('.rarity-badge').forEach(badge => {
    const color = badge.dataset.color;
    badge.style.background = color;
});
// static/module_project/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filter-form');
    const cardsContainer = document.querySelector('.row.g-4'); // Контейнер с картами
    const paginationContainer = document.querySelector('.pagination'); // Контейнер пагинации

    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(filterForm);
            const searchParams = new URLSearchParams(formData).toString();
            
            // Показываем индикатор загрузки
            cardsContainer.style.opacity = '0.5';
            
            fetch(`?${searchParams}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Обновляем HTML карточек
                cardsContainer.innerHTML = data.cards_html;
                
                // Обновляем пагинацию если она есть
                if (paginationContainer) {
                    paginationContainer.innerHTML = data.pagination_html || '';
                }
                
                // Обновляем URL без перезагрузки
                window.history.pushState(null, '', `?${searchParams}`);
            })
            .catch(error => console.error('Error:', error))
            .finally(() => {
                cardsContainer.style.opacity = '1';
            });
        });
    }
});
// main.js - Общие функции для всего приложения

document.addEventListener('DOMContentLoaded', function() {
    
    // Автоматическое скрытие алертов через 5 секунд
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Активация всех всплывающих подсказок
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });
    
    // Активация всех поповеров
    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    popovers.forEach(popover => {
        new bootstrap.Popover(popover);
    });
    
    // Функция для форматирования чисел
    window.formatNumber = function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    };
    
    // Функция для отображения уведомлений
    window.showNotification = function(message, type = 'info') {
        const notificationContainer = document.createElement('div');
        notificationContainer.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notificationContainer.style.top = '20px';
        notificationContainer.style.right = '20px';
        notificationContainer.style.zIndex = '9999';
        notificationContainer.style.minWidth = '300px';
        notificationContainer.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(notificationContainer);
        
        setTimeout(() => {
            notificationContainer.remove();
        }, 5000);
    };
    
    // Подтверждение удаления
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.dataset.confirm || 'Вы уверены?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
    
    // Мобильное меню - автоматическое закрытие при клике
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse.classList.contains('show')) {
                const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                bsCollapse.hide();
            }
        });
    });
    
    // Ленивая загрузка изображений
    const lazyImages = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback для старых браузеров
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        });
    }
    
    // Анимация счетчиков
    const counters = document.querySelectorAll('[data-count]');
    counters.forEach(counter => {
        const target = parseInt(counter.dataset.count);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const updateCounter = () => {
            current += step;
            if (current < target) {
                counter.textContent = Math.round(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(counter);
    });
});

// Функция для AJAX запросов
window.ajaxRequest = function(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    };
    
    if (data) {
        if (data instanceof FormData) {
            options.body = data;
        } else {
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(data);
        }
    }
    
    return fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
};

// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Дебаунс функция для оптимизации поиска
window.debounce = function(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Показать индикатор загрузки
window.showLoader = function() {
    const loader = document.getElementById('loading-indicator');
    if (loader) {
        loader.style.display = 'block';
    }
};

// Скрыть индикатор загрузки
window.hideLoader = function() {
    const loader = document.getElementById('loading-indicator');
    if (loader) {
        loader.style.display = 'none';
    }
};