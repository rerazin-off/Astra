
document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filter-form');
    const searchInput = document.getElementById('search-input');
    const raritySelect = document.getElementById('rarity-select');
    const attributeSelect = document.getElementById('attribute-select');
    const cardsContainer = document.getElementById('cards-container');
    const paginationContainer = document.getElementById('pagination-container');
    const loadingIndicator = document.getElementById('loading-indicator');
    //фильтрация и обновление каталога при изменениях, без загрузки страницы
    if (!filterForm) return;
    
    let searchTimeout;
    
    function applyFilters() {
        const formData = new FormData(filterForm);
        const searchParams = new URLSearchParams(formData).toString();
        
        if (loadingIndicator) loadingIndicator.style.display = 'block';
        if (cardsContainer) cardsContainer.style.opacity = '0.5';
        
        fetch(`?${searchParams}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (cardsContainer) {
                cardsContainer.innerHTML = data.cards_html;
                if (window.applyBadgeBackgrounds) window.applyBadgeBackgrounds(cardsContainer);
            }
            
            if (paginationContainer) {
                paginationContainer.innerHTML = data.pagination_html || '';
            }
            
            window.history.pushState(null, '', `?${searchParams}`);
            const cardCount = document.querySelectorAll('.card-item').length;
            if (cardCount === 0) {
                showNotification('Карты не найдены. Попробуйте изменить параметры поиска.', 'info');
            } else {
                showNotification(`Найдено карт: ${cardCount}`, 'success');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Произошла ошибка при фильтрации', 'danger');
        })
        .finally(() => {
            if (loadingIndicator) loadingIndicator.style.display = 'none';
            if (cardsContainer) cardsContainer.style.opacity = '1';
        });
    }

    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            applyFilters();
        });
    
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    applyFilters();
                }, 500);
            });
        }
    
        if (raritySelect) {
            raritySelect.addEventListener('change', applyFilters);
        }
        
        if (attributeSelect) {
            attributeSelect.addEventListener('change', applyFilters);
        }
    }
    
    document.addEventListener('click', function(e) {
        const pageLink = e.target.closest('.page-link');
        if (pageLink) {
            e.preventDefault();
            const pageUrl = pageLink.href;
            
            if (pageUrl && pageUrl !== '#') {
                if (loadingIndicator) loadingIndicator.style.display = 'block';
                if (cardsContainer) cardsContainer.style.opacity = '0.5';
                
                fetch(pageUrl, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (cardsContainer) {
                        cardsContainer.innerHTML = data.cards_html;
                        if (window.applyBadgeBackgrounds) window.applyBadgeBackgrounds(cardsContainer);
                    }
                    if (paginationContainer) {
                        paginationContainer.innerHTML = data.pagination_html || '';
                    }
                    window.history.pushState(null, '', pageUrl);
                    
                    window.scrollTo({
                        top: cardsContainer.offsetTop - 100,
                        behavior: 'smooth'
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification('Ошибка при загрузке страницы', 'danger');
                })
                .finally(() => {
                    if (loadingIndicator) loadingIndicator.style.display = 'none';
                    if (cardsContainer) cardsContainer.style.opacity = '1';
                });
            }
        }
    });
    
    const resetButton = document.getElementById('reset-filters');
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            if (searchInput) searchInput.value = '';
            if (raritySelect) raritySelect.value = '';
            if (attributeSelect) attributeSelect.value = '';
            applyFilters();
        });
    }
    
    function saveFilters() {
        const filters = {
            search: searchInput ? searchInput.value : '',
            rarity: raritySelect ? raritySelect.value : '',
            attribute: attributeSelect ? attributeSelect.value : ''
        };
        localStorage.setItem('catalogFilters', JSON.stringify(filters));
    }
    
    function loadFilters() {
        const saved = localStorage.getItem('catalogFilters');
        if (saved) {
            const filters = JSON.parse(saved);
            if (searchInput) searchInput.value = filters.search || '';
            if (raritySelect) raritySelect.value = filters.rarity || '';
            if (attributeSelect) attributeSelect.value = filters.attribute || '';
        }
    }
    
    loadFilters();
    
    window.addEventListener('beforeunload', saveFilters);
});