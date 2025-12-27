const TOTAL_GIFTS = 10;
let openedGifts = new Set();
let giftPositions = [];
let authGifts = [];  // Подарки, требующие авторизации
let isAuthenticated = false;

// Генерация подарков с фиксированными позициями
function renderGifts() {
    const grid = document.getElementById('gifts-grid');
    grid.innerHTML = '';
    
    for (let i = 1; i <= TOTAL_GIFTS; i++) {
        const giftBox = document.createElement('div');
        giftBox.className = 'gift-box';
        giftBox.id = `gift-${i}`;
        
        // Используем сохраненные позиции из сессии
        const position = giftPositions[i - 1];
        giftBox.style.left = position.left + '%';
        giftBox.style.top = position.top + '%';
        giftBox.style.transform = `rotate(${position.rotation}deg)`;
        
        // Используем реальные изображения
        // Добавляем замочек для подарков, требующих авторизации
        const isAuthRequired = authGifts.includes(i);
        const lockIcon = (isAuthRequired && !isAuthenticated) ? '<div class="gift-lock">🔒</div>' : '';
        
        giftBox.innerHTML = `
            <img src="/static/gift${i}.png" 
                 alt="Подарок ${i}" 
                 class="gift-image"
                 draggable="false">
            <div class="gift-number">${i}</div>
            ${lockIcon}
        `;
        giftBox.onclick = () => openGift(i);
        grid.appendChild(giftBox);
    }
}

// Обновление статуса
function updateStatus() {
    fetch('/lab9/gifts/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('opened-count').textContent = `Открыто: ${data.opened_count} / 3`;
            document.getElementById('available-count').textContent = `Доступно: ${data.available_count}`;
            
            // Обновляем визуально открытые подарки
            data.opened_gifts.forEach(giftId => {
                const box = document.getElementById(`gift-${giftId}`);
                if (box && !box.classList.contains('opened')) {
                    box.classList.add('opened');
                    openedGifts.add(giftId);
                }
            });
            
            // Отключаем все подарки, если открыто 3
            if (data.opened_count >= 3) {
                document.querySelectorAll('.gift-box:not(.opened)').forEach(box => {
                    box.classList.add('disabled');
                });
            }
        });
}

// Открытие подарка
function openGift(giftId) {
    const box = document.getElementById(`gift-${giftId}`);
    if (box.classList.contains('opened') || box.classList.contains('disabled')) {
        return;
    }
    
    fetch('/lab9/gifts/open', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ gift_id: giftId })
    })
    .then(response => response.json().then(data => ({status: response.status, body: data})))
    .then(({status, body}) => {
        if (status === 200) {
            // Успешно открыт
            box.classList.add('opened');
            openedGifts.add(giftId);
            showModal(body.message, body.image);
            updateStatus();
        } else {
            // Ошибка
            showError(body.error);
        }
    })
    .catch(error => {
        showError('Произошла ошибка при открытии подарка');
        console.error('Error:', error);
    });
}

// Показать модальное окно с поздравлением
function showModal(message, emoji) {
    document.getElementById('modal-emoji').textContent = emoji;
    document.getElementById('modal-message').textContent = message;
    document.getElementById('gift-modal').style.display = 'block';
}

// Закрыть модальное окно
function closeModal() {
    document.getElementById('gift-modal').style.display = 'none';
}

// Показать ошибку
function showError(message) {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-modal').style.display = 'block';
}

// Закрыть окно ошибки
function closeErrorModal() {
    document.getElementById('error-modal').style.display = 'none';
}

// Дед Мороз наполняет коробки снова
function callSanta() {
    if (!confirm('Позвать Деда Мороза, чтобы он наполнил все коробки снова?')) {
        return;
    }
    
    fetch('/lab9/gifts/santa', {
        method: 'POST'
    })
    .then(response => response.json().then(data => ({status: response.status, body: data})))
    .then(({status, body}) => {
        if (status === 200) {
            openedGifts.clear();
            document.querySelectorAll('.gift-box').forEach(box => {
                box.classList.remove('opened', 'disabled');
            });
            updateStatus();
            showModal(body.message, '🎅');
        } else {
            showError(body.error);
        }
    })
    .catch(error => {
        showError('Ошибка при вызове Деда Мороза');
        console.error('Error:', error);
    });
}

// Закрытие модальных окон по клику вне окна
window.onclick = function(event) {
    const giftModal = document.getElementById('gift-modal');
    const errorModal = document.getElementById('error-modal');
    if (event.target == giftModal) {
        closeModal();
    }
    if (event.target == errorModal) {
        closeErrorModal();
    }
}

// Инициализация при загрузке страницы
function initGifts(positions, authRequired = [], authenticated = false) {
    giftPositions = positions;
    authGifts = authRequired;
    isAuthenticated = authenticated;
    renderGifts();
    updateStatus();
}
