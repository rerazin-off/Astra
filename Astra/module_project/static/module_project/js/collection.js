// collection.js — коллекция: фильтры, сортировка, модальное окно карты

(function () {
    function debounce(fn, ms) {
        let t;
        return function () {
            clearTimeout(t);
            const args = arguments;
            t = setTimeout(function () {
                fn.apply(null, args);
            }, ms);
        };
    }

    function loadCollectionPayload() {
        const el = document.getElementById('collection-cards-data');
        if (!el) return {};
        try {
            const list = JSON.parse(el.textContent);
            const map = {};
            list.forEach(function (row) {
                map[String(row.inventory_id)] = row;
            });
            return map;
        } catch (e) {
            return {};
        }
    }

    function formatDateRu(iso) {
        if (!iso) return '—';
        const d = new Date(iso);
        if (isNaN(d.getTime())) return iso;
        return d.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
        });
    }

    function escapeHtml(s) {
        if (!s) return '';
        const div = document.createElement('div');
        div.textContent = s;
        return div.innerHTML;
    }

    function openCollectionModal(inventoryId, payloadById) {
        const data = payloadById[String(inventoryId)];
        if (!data) return;

        const modalEl = document.getElementById('collectionCardModal');
        if (!modalEl || typeof bootstrap === 'undefined') return;

        const titleEl = document.getElementById('collection-modal-title');
        const badgesEl = document.getElementById('collection-modal-badges');
        const imgEl = document.getElementById('collection-modal-image');
        const noImgEl = document.getElementById('collection-modal-no-image');
        const obtainedEl = document.getElementById('collection-modal-obtained');
        const qtyEl = document.getElementById('collection-modal-qty');
        const strEl = document.getElementById('collection-modal-str');
        const hpEl = document.getElementById('collection-modal-hp');
        const defEl = document.getElementById('collection-modal-def');
        const descWrap = document.getElementById('collection-modal-desc-wrap');
        const descEl = document.getElementById('collection-modal-desc');
        const linkEl = document.getElementById('collection-modal-detail-link');

        if (titleEl) titleEl.textContent = data.title || '';

        if (badgesEl) {
            badgesEl.innerHTML = '';
            if (data.rarity_name) {
                const b = document.createElement('span');
                b.className = 'badge text-white me-1';
                b.style.backgroundColor = data.rarity_color || '#6c757d';
                b.textContent = data.rarity_name;
                badgesEl.appendChild(b);
            }
            if (data.attribute_name) {
                const b = document.createElement('span');
                b.className = 'badge text-white';
                b.style.backgroundColor = data.attribute_color || '#6c757d';
                b.textContent = data.attribute_name;
                badgesEl.appendChild(b);
            }
        }

        if (data.cover_url) {
            if (imgEl) {
                imgEl.src = data.cover_url;
                imgEl.alt = data.title || '';
                imgEl.classList.remove('d-none');
            }
            if (noImgEl) noImgEl.classList.add('d-none');
        } else {
            if (imgEl) imgEl.classList.add('d-none');
            if (noImgEl) noImgEl.classList.remove('d-none');
        }

        if (obtainedEl) obtainedEl.textContent = 'Получена: ' + formatDateRu(data.obtained_at);
        if (qtyEl) qtyEl.textContent = String(data.quantity != null ? data.quantity : 1);
        if (strEl) strEl.textContent = String(data.strength != null ? data.strength : 0);
        if (hpEl) hpEl.textContent = String(data.health != null ? data.health : 0);
        if (defEl) defEl.textContent = String(data.defence != null ? data.defence : 0);

        const desc = (data.description || '').trim();
        if (descWrap && descEl) {
            if (desc) {
                descEl.innerHTML = escapeHtml(desc).replace(/\n/g, '<br>');
                descWrap.classList.remove('d-none');
            } else {
                descWrap.classList.add('d-none');
                descEl.textContent = '';
            }
        }

        if (linkEl && data.card_id != null) {
            linkEl.href = '/card/' + data.card_id + '/';
        }

        const refundHint = document.getElementById('collection-modal-refund-hint');
        if (refundHint) {
            var pp = data.price_points != null ? Number(data.price_points) : 0;
            refundHint.textContent =
                'При удалении одной копии карты на счёт вернётся ' +
                pp +
                ' очков (стоимость карты по каталогу).';
        }

        const deleteBtn = document.getElementById('collection-modal-delete-btn');
        if (deleteBtn) {
            deleteBtn.classList.remove('d-none');
            deleteBtn.dataset.inventoryId = String(inventoryId);
        }

        document.getElementById('collectionCardModalLabel').textContent = data.title || 'Карточка';

        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
    }

    document.addEventListener('DOMContentLoaded', function () {
        const searchInput = document.getElementById('collection-search');
        const rarityFilter = document.getElementById('collection-rarity-filter');
        const sortSelect = document.getElementById('collection-sort');
        const container = document.getElementById('collection-container');
        const payloadById = loadCollectionPayload();

        if (!container) return;

        const items = Array.from(document.querySelectorAll('.collection-item'));

        function filterAndSort() {
            const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
            const rarityValue = rarityFilter ? rarityFilter.value : '';

            let filtered = items.filter(function (item) {
                const titleMatch = (item.dataset.title || '').includes(searchTerm);
                const cardRid = String(item.dataset.rarityId || '');
                const rarityMatch = !rarityValue || cardRid === String(rarityValue);
                return titleMatch && rarityMatch;
            });

            const sortBy = sortSelect ? sortSelect.value : 'newest';
            filtered.sort(function (a, b) {
                switch (sortBy) {
                    case 'newest':
                        return (b.dataset.date || '').localeCompare(a.dataset.date || '');
                    case 'oldest':
                        return (a.dataset.date || '').localeCompare(b.dataset.date || '');
                    case 'power':
                        return parseInt(b.dataset.power || '0', 10) - parseInt(a.dataset.power || '0', 10);
                    case 'rarity': {
                        const ra = parseInt(a.dataset.rarityOrder || '0', 10);
                        const rb = parseInt(b.dataset.rarityOrder || '0', 10);
                        return rb - ra;
                    }
                    default:
                        return 0;
                }
            });

            container.innerHTML = '';

            if (filtered.length === 0) {
                container.innerHTML =
                    '<div class="col-12">' +
                    '<div class="text-center py-5">' +
                    '<i class="fas fa-search fa-3x mb-3 opacity-50"></i>' +
                    '<h4>Карты не найдены</h4>' +
                    '<p class="text-muted">Попробуйте изменить параметры поиска</p>' +
                    '</div></div>';
            } else {
                filtered.forEach(function (item) {
                    container.appendChild(item.cloneNode(true));
                });
            }

            if (window.applyBadgeBackgrounds) window.applyBadgeBackgrounds(container);

            const totalEl = document.getElementById('collection-total-count');
            if (totalEl) {
                totalEl.textContent = String(items.length);
            }
        }

        if (searchInput) {
            searchInput.addEventListener('input', debounce(filterAndSort, 300));
        }
        if (rarityFilter) {
            rarityFilter.addEventListener('change', filterAndSort);
        }
        if (sortSelect) {
            sortSelect.addEventListener('change', filterAndSort);
        }

        if (items.length > 0) {
            filterAndSort();
        }

        document.addEventListener('click', function (e) {
            const btn = e.target.closest('.btn-collection-modal');
            if (btn && container.contains(btn)) {
                e.preventDefault();
                e.stopPropagation();
                const id = btn.getAttribute('data-inventory-id');
                if (id) openCollectionModal(id, payloadById);
                return;
            }
            const tile = e.target.closest('.collection-card-tile');
            if (tile && container.contains(tile)) {
                const wrap = tile.closest('.collection-item');
                if (wrap && !e.target.closest('a')) {
                    const id = wrap.getAttribute('data-inventory-id');
                    if (id) openCollectionModal(id, payloadById);
                }
            }
        });

        document.addEventListener('keydown', function (e) {
            if (e.key !== 'Enter' && e.key !== ' ') return;
            const tile = e.target.closest('.collection-card-tile');
            if (!tile || !container.contains(tile)) return;
            if (e.target.closest('a') || e.target.closest('button')) return;
            e.preventDefault();
            const wrap = tile.closest('.collection-item');
            const id = wrap && wrap.getAttribute('data-inventory-id');
            if (id) openCollectionModal(id, payloadById);
        });

        const viewButtons = document.querySelectorAll('[data-view]');
        viewButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                const view = this.dataset.view;
                container.className = 'row g-4 view-' + view;
                viewButtons.forEach(function (btn) {
                    btn.classList.remove('active');
                });
                this.classList.add('active');
                localStorage.setItem('collectionView', view);
            });
        });

        const savedView = localStorage.getItem('collectionView');
        if (savedView) {
            const viewButton = document.querySelector('[data-view="' + savedView + '"]');
            if (viewButton) {
                viewButton.click();
            }
        }

        const deleteFromCollectionBtn = document.getElementById('collection-modal-delete-btn');
        if (deleteFromCollectionBtn) {
            deleteFromCollectionBtn.addEventListener('click', function () {
                const invId = this.dataset.inventoryId;
                if (!invId) return;
                if (!confirm('Удалить одну копию этой карты из коллекции? Стоимость карты будет зачислена на счёт.')) {
                    return;
                }
                const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
                if (!tokenInput || !tokenInput.value) {
                    alert('Не удалось получить CSRF. Обновите страницу.');
                    return;
                }
                fetch('/collection/remove/' + invId + '/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': tokenInput.value,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    credentials: 'same-origin',
                })
                    .then(function (r) {
                        return r.json().then(function (data) {
                            return { ok: r.ok, data: data };
                        });
                    })
                    .then(function (result) {
                        if (result.data && result.data.ok) {
                            if (typeof window.showNotification === 'function') {
                                window.showNotification(
                                    'Возвращено очков: ' +
                                        result.data.refund +
                                        '. Текущий баланс: ' +
                                        result.data.current_points,
                                    'success'
                                );
                            }
                            window.location.reload();
                        } else {
                            alert((result.data && result.data.error) || 'Не удалось удалить');
                        }
                    })
                    .catch(function () {
                        alert('Ошибка сети');
                    });
            });
        }
    });
})();
