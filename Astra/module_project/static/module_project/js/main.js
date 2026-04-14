document.querySelectorAll('.rarity-badge').forEach(badge => {
    const color = badge.dataset.color;
    badge.style.background = color;
});